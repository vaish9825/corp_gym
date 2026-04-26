"""Colab / T4 RLVR: rejection-sampling fine-tuning with FP16 and inner SFT using formatting_func.

Rollout / scoring reuse ``training.train_rlvr``; inner winner SFT uses the same TRL + Unsloth
pattern as ``training_sft_t4`` (messages + ``formatting_func``) for Colab-compatible stacks.
"""

from __future__ import annotations

import argparse
import inspect
import json
import os
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from training.train_grpo import REWARD_CFG, build_prompt_dataset  # noqa: E402
from training.train_rlvr import length_filter, maybe_push_to_hub, rollout_round  # noqa: E402
from training.training_sft_t4 import _formatting_func, _sft_config_field_names  # noqa: E402
from scripts._trajectory_utils import DEFAULT_TASKS  # noqa: E402


def _build_inner_trainer(
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


def sft_on_winners_t4(
    model: Any,
    tokenizer: Any,
    kept_rows: List[Dict[str, Any]],
    *,
    output_dir: str,
    lr: float,
    batch_size: int,
    grad_accum: int,
    epochs: float,
    max_steps: int,
    max_seq_length: int,
    use_fp16: bool,
    dataset_num_proc: int | None,
    dataloader_num_workers: int,
) -> None:
    from datasets import Dataset
    from trl import SFTConfig

    msg_rows = [{"messages": list(row["messages"])} for row in kept_rows]
    if not msg_rows:
        print("  no winners this round; skipping SFT pass")
        return

    dataset = Dataset.from_list(msg_rows)
    allowed = _sft_config_field_names()
    candidate: Dict[str, Any] = {
        "output_dir": output_dir,
        "max_length": max_seq_length,
        "per_device_train_batch_size": batch_size,
        "gradient_accumulation_steps": grad_accum,
        "num_train_epochs": epochs,
        "max_steps": max_steps if max_steps > 0 else -1,
        "learning_rate": lr,
        "warmup_ratio": 0.03,
        "lr_scheduler_type": "cosine",
        "logging_steps": 5,
        "save_steps": 10_000,
        "save_total_limit": 1,
        "optim": "adamw_8bit",
        "bf16": (not use_fp16) and torch.cuda.is_available(),
        "fp16": use_fp16 and torch.cuda.is_available(),
        "report_to": "none",
        "push_to_hub": False,
    }
    if dataset_num_proc is not None and "dataset_num_proc" in allowed:
        candidate["dataset_num_proc"] = dataset_num_proc
    if "dataloader_num_workers" in allowed:
        candidate["dataloader_num_workers"] = dataloader_num_workers

    kwargs = {k: v for k, v in candidate.items() if k in allowed}
    if "output_dir" not in kwargs:
        kwargs["output_dir"] = output_dir
    config = SFTConfig(**kwargs)
    trainer = _build_inner_trainer(model, tokenizer, config, dataset)
    trainer.train()


def main() -> None:
    parser = argparse.ArgumentParser(description="T4/Colab CORP-ENV RLVR (FP16 + inner formatting_func SFT).")
    parser.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct")
    parser.add_argument("--adapter", default="", help="LoRA adapter from SFT (directory with adapter_config.json).")
    parser.add_argument(
        "--examples",
        default="data/processed/e1_m1_clean.jsonl,data/processed/h1_seed_clean.jsonl",
    )
    parser.add_argument(
        "--tasks",
        default="e1_launch_readiness,m1_budget_reallocation,h1_acquisition_defence",
    )
    parser.add_argument("--output", default="outputs/rlvr_adapter")
    parser.add_argument("--push-to-hub", default="")
    parser.add_argument(
        "--target-modules",
        default="q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj",
        help="Comma-separated LoRA targets when starting without --adapter.",
    )
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--n-samples", type=int, default=4)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--reward-threshold", type=float, default=0.0)
    parser.add_argument("--max-prompts", type=int, default=0)
    parser.add_argument("--max-prompt-length", type=int, default=3072)
    parser.add_argument("--max-completion-length", type=int, default=512)
    parser.add_argument("--inner-lr", type=float, default=1e-4)
    parser.add_argument("--inner-epochs", type=float, default=1.0)
    parser.add_argument("--inner-max-steps", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--repeats", type=int, default=32)
    parser.add_argument("--seed", type=int, default=3407)
    parser.add_argument("--strict-json", action="store_true")
    parser.add_argument("--min-reasoning-steps", type=int, default=1)
    parser.add_argument("--stats-file", default="")
    parser.add_argument("--use-stub-workers", action="store_true")
    parser.add_argument("--disable-llm-judge", action="store_true")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--fp16", dest="fp16", action="store_true", help="FP16 (default for T4).")
    g.add_argument("--bf16", dest="fp16", action="store_false", help="BF16 on capable GPUs.")
    parser.set_defaults(fp16=True)
    parser.add_argument(
        "--dataset-num-proc",
        type=int,
        default=1,
        help="Inner SFT dataset workers; 0 -> None where supported.",
    )
    parser.add_argument("--dataloader-num-workers", type=int, default=0)
    args = parser.parse_args()

    if args.use_stub_workers:
        os.environ["CORP_STUB_WORKERS"] = "1"
    if args.disable_llm_judge:
        os.environ["CORP_DISABLE_LLM_JUDGE"] = "1"

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    try:
        from peft import PeftModel
        from unsloth import FastLanguageModel
    except ImportError as exc:
        raise SystemExit("RLVR requires unsloth, trl, datasets, peft, bitsandbytes.") from exc

    target_modules = [m.strip() for m in args.target_modules.split(",") if m.strip()]
    if not target_modules:
        raise SystemExit("No --target-modules.")

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(DEFAULT_TASKS)
    REWARD_CFG["strict_json"] = bool(args.strict_json)
    full_rows = build_prompt_dataset(
        args.examples,
        tasks,
        args.repeats,
        args.min_reasoning_steps,
    )
    print(f"Built {len(full_rows)} prompts from {args.examples}")

    max_seq_len = args.max_prompt_length + args.max_completion_length
    load_dtype = torch.float16 if args.fp16 else torch.bfloat16
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=max_seq_len,
        dtype=load_dtype,
        load_in_4bit=True,
    )
    if getattr(tokenizer, "pad_token", None) is None and getattr(tokenizer, "eos_token", None) is not None:
        tokenizer.pad_token = tokenizer.eos_token

    budget = int(args.max_prompt_length * 0.9)
    full_rows, skipped = length_filter(full_rows, tokenizer, budget)
    print(f"Length filter: kept {len(full_rows)} prompts (<= {budget} tokens); skipped {skipped}.")
    if not full_rows:
        raise SystemExit("No prompts left after length filter; raise --max-prompt-length.")

    if args.adapter:
        adapter_path = Path(args.adapter).expanduser().resolve()
        if not adapter_path.is_dir() or not (adapter_path / "adapter_config.json").is_file():
            raise SystemExit(
                f"Adapter not found or incomplete (need adapter_config.json): {adapter_path}"
            )
        model = PeftModel.from_pretrained(model, str(adapter_path), is_trainable=True)
        print(f"Loaded adapter: {adapter_path}")
    else:
        model = FastLanguageModel.get_peft_model(
            model,
            r=32,
            target_modules=target_modules,
            lora_alpha=32,
            lora_dropout=0.0,
            bias="none",
            use_gradient_checkpointing="unsloth",
            random_state=args.seed,
        )

    cast_dtype = torch.float16 if args.fp16 else torch.bfloat16
    for p in model.parameters():
        if p.requires_grad and p.dtype == torch.float32:
            p.data = p.data.to(cast_dtype)

    ds_num_proc: int | None = args.dataset_num_proc
    if ds_num_proc == 0:
        ds_num_proc = None

    stats_path = Path(args.stats_file) if args.stats_file else None
    if stats_path:
        stats_path.parent.mkdir(parents=True, exist_ok=True)

    for round_idx in range(1, args.rounds + 1):
        print(f"\n=== RLVR round {round_idx}/{args.rounds} ===")
        rng = random.Random(args.seed + round_idx)
        round_rows = list(full_rows)
        rng.shuffle(round_rows)
        if args.max_prompts > 0:
            round_rows = round_rows[: args.max_prompts]
        print(f"  using {len(round_rows)} prompts")

        kept_rows, stats = rollout_round(
            model,
            tokenizer,
            round_rows,
            n_samples=args.n_samples,
            temperature=args.temperature,
            top_p=args.top_p,
            max_new_tokens=args.max_completion_length,
            reward_threshold=args.reward_threshold,
            strict_json=args.strict_json,
        )
        stats["round"] = round_idx
        print(
            f"  round {round_idx} summary: kept={int(stats['prompts_kept'])}/"
            f"{int(stats['prompts_seen'])} keep_rate={stats['keep_rate']:.2%} "
            f"mean_best={stats['mean_best_reward']:.3f} "
            f"mean_any={stats['mean_sample_reward']:.3f} secs={stats['seconds']:.1f}"
        )
        if stats_path:
            with stats_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(stats) + "\n")

        round_out = f"{args.output}/round_{round_idx}"
        sft_on_winners_t4(
            model,
            tokenizer,
            kept_rows,
            output_dir=round_out,
            lr=args.inner_lr,
            batch_size=args.batch_size,
            grad_accum=args.grad_accum,
            epochs=args.inner_epochs,
            max_steps=args.inner_max_steps,
            max_seq_length=max_seq_len,
            use_fp16=bool(args.fp16),
            dataset_num_proc=ds_num_proc,
            dataloader_num_workers=args.dataloader_num_workers,
        )

    Path(args.output).mkdir(parents=True, exist_ok=True)
    if hasattr(model, "save_pretrained"):
        model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)
    print(f"\nSaved RLVR adapter to {args.output}")

    if args.push_to_hub:
        maybe_push_to_hub(args.output, args.push_to_hub)


if __name__ == "__main__":
    main()
