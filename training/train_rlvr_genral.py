"""General HF-dataset-compatible RLVR adapter training.

This variant downloads verified trajectory JSONLs from a Hugging Face dataset
repo and then runs the same rejection-sampling RLVR loop as train_rlvr.py.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from training.train_grpo import REWARD_CFG, build_prompt_dataset
from training.train_rlvr import length_filter, maybe_push_to_hub, rollout_round, sft_on_winners
from scripts._trajectory_utils import DEFAULT_TASKS


def _safe_model_name(model_name: str) -> str:
    leaf = model_name.split("/")[-1].strip().lower()
    return re.sub(r"[^a-z0-9._-]+", "-", leaf).strip("-")


def _default_push_to_hub(model_name: str, hf_user: str) -> str:
    return f"{hf_user}/{_safe_model_name(model_name)}_rlvr"


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


def main() -> None:
    parser = argparse.ArgumentParser(description="General RLVR / Rejection-Sampling FT for CORP-ENV.")
    parser.add_argument("--model", default="deepseek-ai/DeepSeek-R1-Distill-Qwen-14B")
    parser.add_argument("--adapter", default="", help="Start from this LoRA adapter (usually SFT).")
    parser.add_argument("--dataset-repo", default="Navigam/corp-env-data")
    parser.add_argument("--examples-files", default="e1_m1_clean.jsonl,h1_seed_clean.jsonl")
    parser.add_argument(
        "--tasks",
        default="e1_launch_readiness,m1_budget_reallocation,h1_acquisition_defence",
    )
    parser.add_argument("--output", default="outputs/rlvr_adapter")
    parser.add_argument("--hf-user", default="", help="Used to auto-build push repo if --push-to-hub not set.")
    parser.add_argument("--push-to-hub", default="")
    parser.add_argument(
        "--target-modules",
        default="q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj",
        help="Comma-separated LoRA target module names (used when --adapter is empty).",
    )
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--n-samples", type=int, default=8)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument("--reward-threshold", type=float, default=0.0)
    parser.add_argument("--max-prompts", type=int, default=0)
    parser.add_argument("--max-prompt-length", type=int, default=4096)
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
    args = parser.parse_args()

    if args.use_stub_workers:
        os.environ["CORP_STUB_WORKERS"] = "1"
    if args.disable_llm_judge:
        os.environ["CORP_DISABLE_LLM_JUDGE"] = "1"
    if not args.push_to_hub and args.hf_user:
        args.push_to_hub = _default_push_to_hub(args.model, args.hf_user)
    target_modules = _parse_target_modules(args.target_modules)

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    try:
        from peft import PeftModel
        from unsloth import FastLanguageModel
    except ImportError as exc:
        raise SystemExit("RLVR training requires unsloth, trl, datasets, peft, bitsandbytes.") from exc

    local_example_paths: List[str] = []
    for file_name in [x.strip() for x in args.examples_files.split(",") if x.strip()]:
        local_path = _download_dataset_file(args.dataset_repo, file_name)
        local_example_paths.append(str(local_path))
        print(f"Downloaded {file_name} -> {local_path}")
    examples_path = ",".join(local_example_paths)

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(DEFAULT_TASKS)
    REWARD_CFG["strict_json"] = bool(args.strict_json)
    full_rows = build_prompt_dataset(
        examples_path,
        tasks,
        args.repeats,
        args.min_reasoning_steps,
    )
    print(f"Built {len(full_rows)} prompts from HF dataset files")

    max_seq_len = args.max_prompt_length + args.max_completion_length
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=max_seq_len,
        dtype=torch.bfloat16,
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
        model = PeftModel.from_pretrained(model, args.adapter, is_trainable=True)
        print(f"Loaded adapter: {args.adapter}")
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

    for p in model.parameters():
        if p.requires_grad and p.dtype == torch.float32:
            p.data = p.data.to(torch.bfloat16)

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
        sft_on_winners(
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
