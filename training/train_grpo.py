"""Unsloth + Hugging Face TRL GRPO/RLVR training for CORP-ENV.

This is the hackathon RL training script. It uses:

- `unsloth.FastLanguageModel` for efficient 4-bit LoRA/QLoRA loading.
- `trl.GRPOTrainer` / `trl.GRPOConfig` for RLVR-style training.
- The actual `CorpEnvironment` verifier/reward path for reward computation.

Run on Colab, Lightning AI H100, or another GPU machine after SFT:

  python training/train_grpo.py \
    --model Qwen/Qwen2.5-7B-Instruct \
    --adapter outputs/sft_Qwen2.5-7B-Instruct \
    --examples data/processed/e1_m1_clean.jsonl,data/processed/h1_seed_clean.jsonl \
    --output outputs/grpo_Qwen2.5-7B-Instruct \
    --max-steps 150 \
    --push-to-hub your-org/corp-gym-grpo-qwen2.5-7b

The reward function recreates the environment state from a verified action prefix,
applies the sampled next action, and returns the real environment reward plus
penalties for invalid JSON/actions.

Optional speedups (Unsloth picks these up automatically when importable):

- **Flash Attention 2** (`flash_attn`): largest win for long contexts / GRPO rollouts.
  Install a wheel matching your **exact** `torch` and CUDA build, or compile with
  `CUDA_HOME` pointing at the **same** CUDA version PyTorch was built for (check
  `python -c "import torch; print(torch.version.cuda)"`). Mismatch (e.g. nvcc 13.0
  vs torch cu128) breaks the build; fix the toolkit or use an image with FA2 preinstalled.
- **xFormers**: already used as a fallback when FA2 is missing; still slower than FA2.
- **Qwen3.x “linear attention” fast path**: only for those architectures; not used for
  Qwen2.5 GRPO. See Unsloth logs if you train Qwen3.5+.

On a Linux H100 (e.g. Lightning), try **larger** `--batch-size` if memory allows, and
`--dataloader-num-workers 2`–`4` (Windows often keeps 0) so the `CorpEnvironment` rollouts
are not the only bottleneck. Use `--max-steps` (default 150) and `--generations` to trade
quality vs wall-clock.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

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

from corp_env.models import CorpAction  # noqa: E402
from scripts._trajectory_utils import (  # noqa: E402
    DEFAULT_TASKS,
    extract_actions,
    extract_json_object,
    observation_message,
    oracle_actions,
    read_jsonl,
)
from server.agents.master_prompts import build_system_prompt  # noqa: E402
from server.environment import CorpEnvironment  # noqa: E402


def prompt_for_prefix(task_id: str, prefix_actions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    env = CorpEnvironment()
    obs = env.reset(task_id=task_id)
    messages = [{"role": "system", "content": build_system_prompt(obs.master_tier, obs.role)}]
    for step, action_obj in enumerate(prefix_actions):
        messages.append({"role": "user", "content": observation_message(step, obs)})
        messages.append({"role": "assistant", "content": json.dumps(action_obj, ensure_ascii=False)})
        obs = env.step(CorpAction.model_validate(action_obj))
        if obs.done:
            break
    messages.append({"role": "user", "content": observation_message(len(prefix_actions), obs)})
    return messages


def _examples_paths(examples_path: str) -> List[Path]:
    return [Path(p.strip()) for p in examples_path.split(",") if p.strip()]


def build_prompt_dataset(examples_path: str, tasks: List[str], repeats: int) -> List[Dict[str, Any]]:
    """Load examples from one or more JSONLs (comma-separated). Falls back to oracle prefixes if all missing/empty."""
    rows: List[Dict[str, Any]] = []
    for path in _examples_paths(examples_path):
        if not path.exists():
            continue
        for example in read_jsonl(path):
            if example.get("status") and example.get("status") != "clean":
                continue
            task_id = str(example.get("task_id") or "")
            if task_id not in tasks:
                continue
            actions = extract_actions(example)
            for idx in range(len(actions)):
                prefix = actions[:idx]
                rows.append(
                    {
                        "prompt": prompt_for_prefix(task_id, prefix),
                        "task_id": task_id,
                        "prefix_actions": json.dumps(prefix, ensure_ascii=False),
                    }
                )
    if rows:
        return rows

    for _ in range(repeats):
        for task_id in tasks:
            actions = oracle_actions(task_id)
            for idx in range(len(actions)):
                prefix = actions[:idx]
                rows.append(
                    {
                        "prompt": prompt_for_prefix(task_id, prefix),
                        "task_id": task_id,
                        "prefix_actions": json.dumps(prefix, ensure_ascii=False),
                    }
                )
    return rows


def environment_reward(
    completions: List[Any],
    task_id: List[str],
    prefix_actions: List[str],
    **_: Any,
) -> List[float]:
    rewards: List[float] = []
    for completion, tid, prefix_raw in zip(completions, task_id, prefix_actions):
        env = CorpEnvironment()
        obs = env.reset(task_id=tid)
        try:
            prefix = json.loads(prefix_raw)
            for action_obj in prefix:
                obs = env.step(CorpAction.model_validate(action_obj))
                if obs.done:
                    break
        except Exception:
            rewards.append(-0.25)
            continue

        text = completion
        if isinstance(completion, list) and completion:
            text = completion[0].get("content", "")
        elif isinstance(completion, dict):
            text = completion.get("content", "")
        try:
            obj = extract_json_object(str(text))
            obj.pop("thought", None)
            if "payload" in obj and not isinstance(obj["payload"], str):
                obj["payload"] = json.dumps(obj["payload"], ensure_ascii=False)
            action = CorpAction.model_validate(obj)
        except Exception:
            rewards.append(-0.25)
            continue
        obs = env.step(action)
        reward = float(obs.reward or 0.0)
        if obs.error:
            reward -= 0.15
        rewards.append(max(-1.0, min(1.0, reward)))
    return rewards


def main() -> None:
    parser = argparse.ArgumentParser(description="Train CORP-ENV GRPO adapter.")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--adapter", default="outputs/sft_Qwen2.5-7B-Instruct")
    parser.add_argument(
        "--examples",
        default="data/processed/e1_m1_clean.jsonl,data/processed/h1_seed_clean.jsonl",
        help="One JSONL or comma-separated list of verified (clean) trajectory files.",
    )
    parser.add_argument("--output", default="outputs/grpo_Qwen2.5-7B-Instruct")
    parser.add_argument(
        "--tasks",
        default="e1_launch_readiness,m1_budget_reallocation,h1_acquisition_defence",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=32,
        help="When --examples is missing/empty, build this many synthetic oracle prefixes per task. Ignored if the JSONL yields rows.",
    )
    parser.add_argument("--max-prompt-length", type=int, default=8192)
    parser.add_argument("--max-completion-length", type=int, default=1024)
    parser.add_argument("--lr", type=float, default=5e-6)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument(
        "--generations",
        type=int,
        default=2,
        help="GRPO samples per prompt per step. Lower = faster steps, noisier gradients (try 2 for quick runs, 4 for fuller RL).",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=150,
        help="Optimizer steps (not env episodes). Default 150 for a fuller RL fit on H100-style runs.",
    )
    parser.add_argument(
        "--save-steps",
        type=int,
        default=None,
        help="Checkpoint every N steps. Default: min(25, max(5, max_steps//2)) so short runs still save.",
    )
    parser.add_argument("--optim", default="adamw_8bit")
    parser.add_argument(
        "--dataloader-num-workers",
        type=int,
        default=0,
        help="DataLoader workers (0 is safest on Windows; try 2–4 on Linux H100 if CPU allows).",
    )
    parser.add_argument(
        "--dataloader-prefetch-factor",
        type=int,
        default=None,
        help="When dataloader_num_workers>0, optional prefetch depth (e.g. 2).",
    )
    parser.add_argument("--push-to-hub", default="")
    args = parser.parse_args()

    os.environ.setdefault("CORP_STUB_WORKERS", "1")
    os.environ.setdefault("CORP_DISABLE_LLM_JUDGE", "1")

    try:
        from unsloth import FastLanguageModel, PatchFastRL
        from datasets import Dataset
        from peft import PeftModel
        from trl import GRPOConfig, GRPOTrainer
    except ImportError as exc:
        raise SystemExit(
            "GRPO training requires unsloth, trl, datasets, and peft. On Lightning AI, install with:\n"
            "  pip install -U unsloth trl datasets accelerate peft bitsandbytes transformers"
        ) from exc

    PatchFastRL("GRPO", FastLanguageModel)

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(DEFAULT_TASKS)
    rows = build_prompt_dataset(args.examples, tasks, args.repeats)

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_prompt_length + args.max_completion_length,
        dtype=torch.bfloat16,
        load_in_4bit=True,
    )
    if getattr(tokenizer, "pad_token", None) is None and getattr(
        tokenizer, "eos_token", None
    ) is not None:
        tokenizer.pad_token = tokenizer.eos_token

    _filtered_rows: List[Dict[str, Any]] = []
    _budget = int(args.max_prompt_length * 0.9)
    _skipped = 0
    for _row in rows:
        _ids = tokenizer.apply_chat_template(
            _row["prompt"], tokenize=True, add_generation_prompt=True
        )
        if len(_ids) <= _budget:
            _filtered_rows.append(_row)
        else:
            _skipped += 1
    print(
        f"GRPO dataset: kept {len(_filtered_rows)} / {len(rows)} prompts "
        f"(<= {_budget} tokens); skipped {_skipped} oversized prompts."
    )
    rows = _filtered_rows
    if not rows:
        raise SystemExit("No prompts remain after length filtering; raise --max-prompt-length.")
    dataset = Dataset.from_list(rows)

    save_steps = args.save_steps
    if save_steps is None:
        save_steps = min(25, max(5, args.max_steps // 2))

    if args.adapter:
        model = PeftModel.from_pretrained(model, args.adapter, is_trainable=True)
    else:
        model = FastLanguageModel.get_peft_model(
            model,
            r=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_alpha=32,
            lora_dropout=0.0,
            bias="none",
            use_gradient_checkpointing="unsloth",
            random_state=3407,
        )

    for _p in model.parameters():
        if _p.requires_grad and _p.dtype == torch.float32:
            _p.data = _p.data.to(torch.bfloat16)

    _gc_kwargs: Dict[str, Any] = {
        "output_dir": args.output,
        "learning_rate": args.lr,
        "per_device_train_batch_size": args.batch_size,
        "gradient_accumulation_steps": args.grad_accum,
        "num_generations": args.generations,
        "max_prompt_length": args.max_prompt_length,
        "max_completion_length": args.max_completion_length,
        "max_steps": args.max_steps,
        "logging_steps": 5,
        "save_steps": save_steps,
        "save_total_limit": 3,
        "optim": args.optim,
        "bf16": True,
        "report_to": "none",
        "push_to_hub": bool(args.push_to_hub),
        "hub_model_id": args.push_to_hub or None,
    }
    if args.dataloader_num_workers:
        _gc_kwargs["dataloader_num_workers"] = args.dataloader_num_workers
    if args.dataloader_prefetch_factor is not None and args.dataloader_num_workers:
        _gc_kwargs["dataloader_prefetch_factor"] = args.dataloader_prefetch_factor
    config = GRPOConfig(**_gc_kwargs)
    trainer = GRPOTrainer(
        model=model,
        processing_class=tokenizer,
        reward_funcs=environment_reward,
        args=config,
        train_dataset=dataset,
    )
    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)

    if args.push_to_hub:
        trainer.push_to_hub()


if __name__ == "__main__":
    main()
