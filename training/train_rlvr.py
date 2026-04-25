"""Rejection-Sampling Fine-Tuning on verifiable rewards (RLVR) for CORP-ENV.

Motivation
----------
GRPO with small group size on CORP-ENV produced mostly-zero-variance batches
(``frac_reward_zero_std ≈ 1``): both sampled completions usually earned the
same verifier-derived reward, so the advantage was 0 and the gradient was
noise. Since the reward *is* deterministic and verifiable (strict JSON,
rule-based env step, pass-rate), a cleaner RLVR variant is:

1. Sample N completions per prompt at a non-zero temperature.
2. Score every completion with the real ``CorpEnvironment`` verifier.
3. Keep the best completion per prompt when it passes a reward threshold.
4. SFT the model on that curated set.
5. Repeat for ``--rounds`` outer iterations.

This is sometimes called "Rejection Sampling FT" / "Expert Iteration" and
is what Tülu 3 folds into its RLVR recipe for tasks with verifiable rewards.
The gradient signal is noise-free because we only learn from winning
completions, and the advantage-variance collapse in GRPO no longer applies.

Run (after SFT)::

    python training/train_rlvr.py \\
      --model Qwen/Qwen2.5-7B-Instruct \\
      --adapter outputs/sft_adapter \\
      --examples data/processed/e1_m1_clean.jsonl,data/processed/h1_seed_clean.jsonl \\
      --output outputs/rlvr_adapter \\
      --rounds 3 --n-samples 8 --max-prompts 64 \\
      --push-to-hub Navigam/corp-env-rlvr-qwen2.5-7b
"""

from __future__ import annotations

import argparse
import inspect
import json
import os
import random
import sys
import time
from dataclasses import fields
from pathlib import Path
from typing import Any, Dict, List, Tuple

import torch

try:
    import flash_attn.flash_attn_interface as _fa_mod

    _orig_fa_func = _fa_mod.flash_attn_func
    _orig_fa_var = getattr(_fa_mod, "flash_attn_varlen_func", None)

    def _fa_func_bf16(q, k, v, *args, **kwargs):
        if q.dtype not in (torch.bfloat16, torch.float16):
            q, k, v = q.to(torch.bfloat16), k.to(torch.bfloat16), v.to(torch.bfloat16)
        return _orig_fa_func(q, k, v, *args, **kwargs)

    def _fa_varlen_bf16(q, k, v, *args, **kwargs):
        if q.dtype not in (torch.bfloat16, torch.float16):
            q, k, v = q.to(torch.bfloat16), k.to(torch.bfloat16), v.to(torch.bfloat16)
        return _orig_fa_var(q, k, v, *args, **kwargs)

    _fa_mod.flash_attn_func = _fa_func_bf16
    if _orig_fa_var is not None:
        _fa_mod.flash_attn_varlen_func = _fa_varlen_bf16

    try:
        import unsloth.utils.attention_dispatch as _ad_mod
        _ad_mod.flash_attn_func = _fa_func_bf16
        if _orig_fa_var is not None and hasattr(_ad_mod, "flash_attn_varlen_func"):
            _ad_mod.flash_attn_varlen_func = _fa_varlen_bf16
    except Exception:
        pass
except ImportError:
    pass

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from training.train_grpo import build_prompt_dataset, environment_reward  # noqa: E402
from scripts._trajectory_utils import DEFAULT_TASKS  # noqa: E402


def _sft_config_field_names() -> set[str]:
    from trl import SFTConfig

    if hasattr(SFTConfig, "__dataclass_fields__"):
        return set(SFTConfig.__dataclass_fields__.keys())
    return {f.name for f in fields(SFTConfig)}


def length_filter(
    rows: List[Dict[str, Any]], tokenizer: Any, budget: int
) -> Tuple[List[Dict[str, Any]], int]:
    kept: List[Dict[str, Any]] = []
    skipped = 0
    for row in rows:
        ids = tokenizer.apply_chat_template(
            row["prompt"], tokenize=True, add_generation_prompt=True
        )
        if len(ids) <= budget:
            kept.append(row)
        else:
            skipped += 1
    return kept, skipped


def sample_completions(
    model: Any,
    tokenizer: Any,
    prompt_messages: List[Dict[str, str]],
    n_samples: int,
    temperature: float,
    top_p: float,
    max_new_tokens: int,
) -> List[str]:
    """Generate ``n_samples`` candidates for one prompt with non-zero temperature."""
    input_ids = tokenizer.apply_chat_template(
        prompt_messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)
    attn_mask = torch.ones_like(input_ids)
    pad_id = tokenizer.pad_token_id
    if pad_id is None:
        pad_id = tokenizer.eos_token_id

    prev_mode = model.training
    model.eval()
    try:
        with torch.inference_mode():
            outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attn_mask,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=n_samples,
                pad_token_id=pad_id,
            )
    finally:
        if prev_mode:
            model.train()

    prompt_len = input_ids.shape[1]
    decoded: List[str] = []
    for i in range(outputs.shape[0]):
        text = tokenizer.decode(outputs[i, prompt_len:], skip_special_tokens=True)
        decoded.append(text.strip())
    return decoded


def rollout_round(
    model: Any,
    tokenizer: Any,
    rows: List[Dict[str, Any]],
    *,
    n_samples: int,
    temperature: float,
    top_p: float,
    max_new_tokens: int,
    reward_threshold: float,
    log_every: int = 10,
) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
    kept_rows: List[Dict[str, Any]] = []
    all_rewards: List[float] = []
    best_rewards: List[float] = []
    per_task_kept: Dict[str, int] = {}
    per_task_total: Dict[str, int] = {}

    t0 = time.time()
    for idx, row in enumerate(rows):
        task_id = row["task_id"]
        prefix_json = row["prefix_actions"]
        per_task_total[task_id] = per_task_total.get(task_id, 0) + 1

        try:
            completions = sample_completions(
                model,
                tokenizer,
                row["prompt"],
                n_samples=n_samples,
                temperature=temperature,
                top_p=top_p,
                max_new_tokens=max_new_tokens,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  [{idx}] {task_id}: generation error {exc!r}")
            continue

        rewards = environment_reward(
            completions=completions,
            task_id=[task_id] * len(completions),
            prefix_actions=[prefix_json] * len(completions),
        )
        all_rewards.extend(rewards)
        best_idx = max(range(len(rewards)), key=lambda j: rewards[j])
        best_r = float(rewards[best_idx])
        best_rewards.append(best_r)

        if best_r >= reward_threshold:
            kept_rows.append(
                {
                    "messages": list(row["prompt"])
                    + [{"role": "assistant", "content": completions[best_idx]}],
                    "task_id": task_id,
                    "reward": best_r,
                }
            )
            per_task_kept[task_id] = per_task_kept.get(task_id, 0) + 1

        if (idx + 1) % log_every == 0 or idx + 1 == len(rows):
            elapsed = time.time() - t0
            kept = len(kept_rows)
            mean_best = sum(best_rewards) / max(1, len(best_rewards))
            mean_r = sum(all_rewards) / max(1, len(all_rewards))
            print(
                f"  rollout {idx + 1}/{len(rows)}  kept={kept}  "
                f"mean_best={mean_best:.3f}  mean_any={mean_r:.3f}  "
                f"elapsed={elapsed:.1f}s"
            )

    stats = {
        "prompts_seen": float(len(rows)),
        "prompts_kept": float(len(kept_rows)),
        "keep_rate": len(kept_rows) / max(1, len(rows)),
        "mean_best_reward": sum(best_rewards) / max(1, len(best_rewards)),
        "mean_sample_reward": sum(all_rewards) / max(1, len(all_rewards)),
        "total_rollouts": float(len(all_rewards)),
        "seconds": time.time() - t0,
    }
    for tid in per_task_total:
        stats[f"keep_rate/{tid}"] = per_task_kept.get(tid, 0) / per_task_total[tid]
    return kept_rows, stats


def sft_on_winners(
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
) -> None:
    """Run a single SFT pass over the curated (prompt, best_completion) set."""
    from datasets import Dataset
    from trl import SFTConfig, SFTTrainer

    text_rows: List[Dict[str, str]] = []
    for row in kept_rows:
        text = tokenizer.apply_chat_template(
            row["messages"], tokenize=False, add_generation_prompt=False
        )
        text_rows.append({"text": text})
    if not text_rows:
        print("  no winners this round; skipping SFT pass")
        return

    dataset = Dataset.from_list(text_rows)
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
        "bf16": True,
        "report_to": "none",
        "dataset_text_field": "text",
        "push_to_hub": False,
    }
    kwargs = {k: v for k, v in candidate.items() if k in allowed}
    if "output_dir" not in kwargs:
        kwargs["output_dir"] = output_dir
    config = SFTConfig(**kwargs)

    sig = inspect.signature(SFTTrainer.__init__)
    init_kwargs: Dict[str, Any] = {
        "model": model,
        "args": config,
        "train_dataset": dataset,
    }
    if "processing_class" in sig.parameters:
        init_kwargs["processing_class"] = tokenizer
    elif "tokenizer" in sig.parameters:
        init_kwargs["tokenizer"] = tokenizer
    else:
        raise SystemExit("SFTTrainer: expected processing_class or tokenizer.")

    trainer = SFTTrainer(**init_kwargs)
    trainer.train()


def maybe_push_to_hub(output_dir: str, repo_id: str) -> None:
    if not repo_id:
        return
    try:
        from huggingface_hub import HfApi
    except ImportError:
        print(f"  huggingface_hub missing; local adapter saved to {output_dir}")
        return
    api = HfApi()
    api.create_repo(repo_id, exist_ok=True, private=False)
    api.upload_folder(
        repo_id=repo_id,
        folder_path=output_dir,
        commit_message="RLVR rejection-sampling FT adapter",
        ignore_patterns=["checkpoint-*/**", "runs/**", "events.out.*"],
    )
    print(f"  pushed {output_dir} -> {repo_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="RLVR / Rejection-Sampling FT for CORP-ENV.")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--adapter", default="outputs/sft_adapter",
                        help="Start from this LoRA adapter (usually SFT).")
    parser.add_argument(
        "--examples",
        default="data/processed/e1_m1_clean.jsonl,data/processed/h1_seed_clean.jsonl",
    )
    parser.add_argument(
        "--tasks",
        default="e1_launch_readiness,m1_budget_reallocation,h1_acquisition_defence",
    )
    parser.add_argument("--output", default="outputs/rlvr_adapter")
    parser.add_argument("--rounds", type=int, default=3,
                        help="Outer rollout -> filter -> SFT iterations.")
    parser.add_argument("--n-samples", type=int, default=8,
                        help="Candidates sampled per prompt per round.")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.95)
    parser.add_argument(
        "--reward-threshold", type=float, default=0.0,
        help="Keep the best completion per prompt only when its reward >= this.",
    )
    parser.add_argument("--max-prompts", type=int, default=0,
                        help="Cap prompts per round (0 = full dataset, shuffled).")
    parser.add_argument("--max-prompt-length", type=int, default=8192)
    parser.add_argument("--max-completion-length", type=int, default=512)
    parser.add_argument("--inner-lr", type=float, default=1e-4)
    parser.add_argument("--inner-epochs", type=float, default=1.0)
    parser.add_argument("--inner-max-steps", type=int, default=0,
                        help=">0 caps inner SFT steps per round.")
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--repeats", type=int, default=32)
    parser.add_argument("--seed", type=int, default=3407)
    parser.add_argument("--push-to-hub", default="")
    parser.add_argument(
        "--stats-file",
        default="",
        help="Optional JSONL to append per-round rollout stats to.",
    )
    args = parser.parse_args()

    os.environ.setdefault("CORP_STUB_WORKERS", "1")
    os.environ.setdefault("CORP_DISABLE_LLM_JUDGE", "1")

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    try:
        from unsloth import FastLanguageModel
        from peft import PeftModel
    except ImportError as exc:
        raise SystemExit(
            "RLVR training requires unsloth, trl, datasets, peft, bitsandbytes."
        ) from exc

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(DEFAULT_TASKS)
    full_rows = build_prompt_dataset(args.examples, tasks, args.repeats)
    print(f"Built {len(full_rows)} prompts from {args.examples}")

    max_seq_len = args.max_prompt_length + args.max_completion_length
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=max_seq_len,
        dtype=torch.bfloat16,
        load_in_4bit=True,
    )
    if getattr(tokenizer, "pad_token", None) is None and getattr(
        tokenizer, "eos_token", None
    ) is not None:
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
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                            "gate_proj", "up_proj", "down_proj"],
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
        )
        stats["round"] = round_idx
        print(
            f"  round {round_idx} summary: kept={int(stats['prompts_kept'])}/"
            f"{int(stats['prompts_seen'])}  keep_rate={stats['keep_rate']:.2%}  "
            f"mean_best={stats['mean_best_reward']:.3f}  "
            f"mean_any={stats['mean_sample_reward']:.3f}  "
            f"secs={stats['seconds']:.1f}"
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
