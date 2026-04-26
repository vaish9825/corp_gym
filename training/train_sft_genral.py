"""General HF-dataset-compatible SFT adapter training.

This variant downloads training JSONL from a Hugging Face dataset repo and then
runs Unsloth + TRL SFT exactly like `training/train_sft.py`.
"""

from __future__ import annotations

import argparse
import inspect
import json
import re
from dataclasses import fields
from pathlib import Path
from typing import Any, Dict, List

import torch


def _safe_model_name(model_name: str) -> str:
    leaf = model_name.split("/")[-1].strip().lower()
    return re.sub(r"[^a-z0-9._-]+", "-", leaf).strip("-")


def _default_push_to_hub(model_name: str, hf_user: str) -> str:
    return f"{hf_user}/{_safe_model_name(model_name)}_sft"


def _parse_target_modules(raw: str) -> List[str]:
    mods = [m.strip() for m in raw.split(",") if m.strip()]
    if not mods:
        raise SystemExit("No LoRA target modules provided. Use --target-modules.")
    return mods


def _download_dataset_file(dataset_repo: str, dataset_file: str) -> Path:
    try:
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise SystemExit("Please install huggingface_hub to download dataset files.") from exc
    local = hf_hub_download(
        repo_id=dataset_repo,
        filename=dataset_file,
        repo_type="dataset",
    )
    return Path(local)


def _sft_config_field_names() -> set[str]:
    from trl import SFTConfig

    if hasattr(SFTConfig, "__dataclass_fields__"):
        return set(SFTConfig.__dataclass_fields__.keys())
    return {f.name for f in fields(SFTConfig)}


def load_conversation_rows(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if "messages" not in obj:
                raise SystemExit(f"{path}: row missing 'messages'.")
            rows.append({"messages": obj["messages"]})
    return rows


def _messages_to_text(tokenizer: object, messages: List[Dict[str, Any]]) -> str:
    if hasattr(tokenizer, "apply_chat_template"):
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False,
        )
    rendered: List[str] = []
    for msg in messages:
        role = str(msg.get("role", "user"))
        content = str(msg.get("content", ""))
        rendered.append(f"{role}: {content}")
    return "\n".join(rendered)


def _formatting_func(tokenizer: object):
    def _format(example: Dict[str, Any]) -> Any:
        msgs = example.get("messages", [])
        if msgs and isinstance(msgs[0], list):
            return [_messages_to_text(tokenizer, m) for m in msgs]
        return [_messages_to_text(tokenizer, msgs)]

    return _format


def _build_sft_config(
    allowed: set[str],
    output_dir: str,
    max_seq: int,
    args: argparse.Namespace,
) -> Any:
    from trl import SFTConfig

    candidate: Dict[str, Any] = {
        "output_dir": output_dir,
        "max_length": max_seq,
        "per_device_train_batch_size": args.batch_size,
        "gradient_accumulation_steps": args.grad_accum,
        "num_train_epochs": args.epochs,
        "learning_rate": args.lr,
        "warmup_ratio": 0.05,
        "lr_scheduler_type": "cosine",
        "logging_steps": 5,
        "save_steps": args.save_steps,
        "save_total_limit": 3,
        "max_steps": args.max_steps,
        "optim": args.optim,
        "bf16": (not args.fp16) and torch.cuda.is_available(),
        "fp16": bool(args.fp16) and torch.cuda.is_available(),
        "packing": args.packing,
        "report_to": "none",
        "push_to_hub": bool(args.push_to_hub),
        "hub_model_id": args.push_to_hub or None,
        "assistant_only_loss": args.assistant_only,
    }
    if args.dataset_num_proc is not None and "dataset_num_proc" in allowed:
        candidate["dataset_num_proc"] = args.dataset_num_proc
    if args.dataloader_num_workers and "dataloader_num_workers" in allowed:
        candidate["dataloader_num_workers"] = args.dataloader_num_workers
    if args.packing and "padding_free" in allowed and args.padding_free:
        candidate["padding_free"] = True

    kwargs = {k: v for k, v in candidate.items() if k in allowed}
    if "output_dir" not in kwargs:
        kwargs["output_dir"] = output_dir
    return SFTConfig(**kwargs)


def _build_trainer(
    model: object,
    tokenizer: object,
    config: object,
    dataset: object,
) -> Any:
    from trl import SFTTrainer

    sig = inspect.signature(SFTTrainer.__init__)
    formatting_func = _formatting_func(tokenizer)
    if "processing_class" in sig.parameters:
        return SFTTrainer(
            model=model,
            args=config,
            train_dataset=dataset,
            processing_class=tokenizer,
            formatting_func=formatting_func,
        )
    if "tokenizer" in sig.parameters:
        return SFTTrainer(
            model=model,
            args=config,
            train_dataset=dataset,
            tokenizer=tokenizer,
            formatting_func=formatting_func,
        )
    raise SystemExit("SFTTrainer: expected processing_class or tokenizer in __init__.")


def main() -> None:
    parser = argparse.ArgumentParser(description="General CORP-ENV SFT LoRA adapter trainer.")
    parser.add_argument("--model", default="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B")
    parser.add_argument("--dataset-repo", default="Navigam/corp-env-data")
    parser.add_argument("--dataset-file", default="e1_m1_h1_examples.jsonl")
    parser.add_argument("--output", default="outputs/sft_adapter")
    parser.add_argument("--hf-user", default="", help="Used to auto-build push repo if --push-to-hub not set.")
    parser.add_argument("--push-to-hub", default="")
    parser.add_argument(
        "--target-modules",
        default="q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj",
        help="Comma-separated LoRA target module names.",
    )
    parser.add_argument("--max-seq-length", type=int, default=4096)
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--max-steps", type=int, default=-1)
    parser.add_argument("--save-steps", type=int, default=50)
    parser.add_argument("--optim", default="adamw_8bit")
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--assistant-only", action="store_true")
    parser.add_argument("--packing", action="store_true")
    parser.add_argument("--padding-free", action="store_true")
    parser.add_argument("--dataset-num-proc", type=int, default=4)
    parser.add_argument("--dataloader-num-workers", type=int, default=2)
    args = parser.parse_args()

    try:
        from datasets import Dataset
        from unsloth import FastLanguageModel
    except ImportError as exc:
        raise SystemExit("SFT training requires datasets, trl, and unsloth.") from exc

    if not args.push_to_hub and args.hf_user:
        args.push_to_hub = _default_push_to_hub(args.model, args.hf_user)
    target_modules = _parse_target_modules(args.target_modules)

    data_path = _download_dataset_file(args.dataset_repo, args.dataset_file)
    print(f"Loaded dataset file from HF: {data_path}")

    allowed = _sft_config_field_names()
    if args.dataset_num_proc == 0 and "dataset_num_proc" in allowed:
        args = argparse.Namespace(**{**vars(args), "dataset_num_proc": None})

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )
    if getattr(tokenizer, "pad_token", None) is None and getattr(tokenizer, "eos_token", None) is not None:
        tokenizer.pad_token = tokenizer.eos_token

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=target_modules,
        lora_alpha=32,
        lora_dropout=0.0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
    )

    rows = load_conversation_rows(data_path)
    if not rows:
        raise SystemExit(f"No training rows in HF dataset file {args.dataset_file!r}.")

    dataset = Dataset.from_list(rows)
    config = _build_sft_config(allowed, args.output, args.max_seq_length, args)
    trainer = _build_trainer(model, tokenizer, config, dataset)
    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)

    if args.push_to_hub:
        trainer.push_to_hub()
        print(f"Pushed SFT adapter: {args.push_to_hub}")


if __name__ == "__main__":
    main()
