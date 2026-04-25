"""Unsloth + Hugging Face TRL SFT for CORP-ENV action-format warm start.

This is the hackathon SFT training script. It uses:

- `unsloth.FastLanguageModel` for efficient 4-bit LoRA/QLoRA loading.
- `trl.SFTTrainer` / `trl.SFTConfig` for supervised fine-tuning.
- `messages`-format JSONL with TRL 0.2x conversational SFT (optional `--assistant-only` if the
  model chat template supports assistant token masks; Qwen2.5 Instruct defaults to off).

Run on Colab, Lightning AI H100, or another GPU machine:

  python training/train_sft.py \
    --model Qwen/Qwen2.5-7B-Instruct \
    --data data/sft/e1_m1_h1_examples.jsonl \
    --output outputs/sft_adapter \
    --max-steps 30 \
    --push-to-hub your-org/corp-env-sft-adapter
"""

from __future__ import annotations

import argparse
import inspect
import json
from dataclasses import fields
from pathlib import Path
from typing import Any, Dict, List

import torch  # imported before unsloth in main for dtype hooks


def _sft_config_field_names() -> set[str]:
    from trl import SFTConfig

    if hasattr(SFTConfig, "__dataclass_fields__"):
        return set(SFTConfig.__dataclass_fields__.keys())
    return {f.name for f in fields(SFTConfig)}


def load_conversation_rows(path: Path) -> List[Dict[str, Any]]:
    """TRL conversational format: each row has a `messages` list."""
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if "messages" not in obj:
                raise SystemExit(
                    f"{path}: SFT example missing 'messages' (use --legacy-text for old format)."
                )
            rows.append({"messages": obj["messages"]})
    return rows


def load_text_rows(path: Path, tokenizer: object) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            messages = obj["messages"]
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False,
            )
            rows.append({"text": text})
    return rows


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
    if args.legacy_text and "dataset_text_field" in allowed:
        candidate["dataset_text_field"] = "text"

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
    if "processing_class" in sig.parameters:
        return SFTTrainer(
            model=model,
            args=config,
            train_dataset=dataset,
            processing_class=tokenizer,
        )
    if "tokenizer" in sig.parameters:
        return SFTTrainer(
            model=model,
            args=config,
            train_dataset=dataset,
            tokenizer=tokenizer,
        )
    raise SystemExit("SFTTrainer: expected processing_class or tokenizer in __init__.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train CORP-ENV SFT LoRA adapter.")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--data", default="data/sft/e1_m1_h1_examples.jsonl")
    parser.add_argument("--output", default="outputs/sft_adapter")
    parser.add_argument("--max-seq-length", type=int, default=8192)
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--max-steps", type=int, default=-1, help="Positive value for quick judge/Colab smoke runs.")
    parser.add_argument("--save-steps", type=int, default=50)
    parser.add_argument("--optim", default="adamw_8bit")
    parser.add_argument("--push-to-hub", default="")
    parser.add_argument(
        "--fp16",
        action="store_true",
        help="Use fp16 instead of bf16 (bf16 is default on CUDA when available).",
    )
    parser.add_argument(
        "--legacy-text",
        action="store_true",
        help="Pre-tokenize to a single 'text' column (older path). Default: TRL messages format.",
    )
    parser.add_argument(
        "--assistant-only",
        action="store_true",
        help=(
            "Loss only on assistant tokens (requires tokenizer chat template with assistant masks). "
            "Qwen2.5 usually needs this off; use with templates that support {% generation %}."
        ),
    )
    parser.add_argument(
        "--packing",
        action="store_true",
        help="Sequence packing (faster; avoid for very long or uneven traces unless you know the tradeoffs).",
    )
    parser.add_argument(
        "--padding-free",
        action="store_true",
        help="With packing+bfd, TRL can use padding-free; requires FlashAttention-friendly setup.",
    )
    parser.add_argument(
        "--dataset-num-proc",
        type=int,
        default=4,
        help="Multiprocess dataset preprocessing; set 0 to disable where supported (default 4 for H100).",
    )
    parser.add_argument(
        "--dataloader-num-workers",
        type=int,
        default=2,
        help="DataLoader workers (default 2; increase on H100 if CPU allows).",
    )
    args = parser.parse_args()

    try:
        from unsloth import FastLanguageModel
        from datasets import Dataset
    except ImportError as exc:
        raise SystemExit(
            "SFT training requires datasets, trl, and unsloth. On Lightning AI, install with:\n"
            "  pip install -e \".[training]\""
        ) from exc

    allowed = _sft_config_field_names()
    if args.dataset_num_proc == 0 and "dataset_num_proc" in allowed:
        args = argparse.Namespace(**{**vars(args), "dataset_num_proc": None})

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )
    if getattr(tokenizer, "pad_token", None) is None and getattr(
        tokenizer, "eos_token", None
    ) is not None:
        tokenizer.pad_token = tokenizer.eos_token

    model = FastLanguageModel.get_peft_model(
        model,
        r=32,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_alpha=32,
        lora_dropout=0.0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
    )

    if args.legacy_text:
        rows = load_text_rows(Path(args.data), tokenizer)
    else:
        rows = load_conversation_rows(Path(args.data))
    if not rows:
        raise SystemExit(f"No training rows in {args.data!r}.")

    dataset = Dataset.from_list(rows)
    config = _build_sft_config(allowed, args.output, args.max_seq_length, args)
    trainer = _build_trainer(model, tokenizer, config, dataset)
    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)

    if args.push_to_hub:
        trainer.push_to_hub()


if __name__ == "__main__":
    main()
