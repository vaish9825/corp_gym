"""GRPO/RLVR training for CORP-ENV with verifier rewards.

This script is intended for short Lightning AI H100 windows after SFT:

  python training/train_grpo.py \
    --model Qwen/Qwen2.5-7B-Instruct \
    --adapter outputs/sft_adapter \
    --examples data/processed/e1_m1_clean.jsonl \
    --output outputs/grpo_adapter

The reward function recreates the environment state from a verified action prefix,
applies the sampled next action, and returns the real environment reward plus
penalties for invalid JSON/actions.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

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


def build_prompt_dataset(examples_path: str, tasks: List[str], repeats: int) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    path = Path(examples_path)
    if path.exists():
        examples = list(read_jsonl(path))
        for example in examples:
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
    parser.add_argument("--adapter", default="outputs/sft_adapter")
    parser.add_argument("--examples", default="data/processed/e1_m1_clean.jsonl")
    parser.add_argument("--output", default="outputs/grpo_adapter")
    parser.add_argument("--tasks", default="e1_launch_readiness,m1_budget_reallocation")
    parser.add_argument("--repeats", type=int, default=128)
    parser.add_argument("--max-prompt-length", type=int, default=8192)
    parser.add_argument("--max-completion-length", type=int, default=1024)
    parser.add_argument("--lr", type=float, default=5e-6)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--generations", type=int, default=4)
    parser.add_argument("--max-steps", type=int, default=150)
    parser.add_argument("--push-to-hub", default="")
    args = parser.parse_args()

    os.environ.setdefault("CORP_STUB_WORKERS", "1")
    os.environ.setdefault("CORP_DISABLE_LLM_JUDGE", "1")

    try:
        from datasets import Dataset
        from peft import PeftModel
        from trl import GRPOConfig, GRPOTrainer
        from unsloth import FastLanguageModel
    except ImportError as exc:
        raise SystemExit(
            "GRPO training requires unsloth, trl, datasets, and peft. On Lightning AI, install with:\n"
            "  pip install -U unsloth trl datasets accelerate peft bitsandbytes transformers"
        ) from exc

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(DEFAULT_TASKS)
    rows = build_prompt_dataset(args.examples, tasks, args.repeats)
    dataset = Dataset.from_list(rows)

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_prompt_length + args.max_completion_length,
        dtype=None,
        load_in_4bit=True,
    )
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

    config = GRPOConfig(
        output_dir=args.output,
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        num_generations=args.generations,
        max_prompt_length=args.max_prompt_length,
        max_completion_length=args.max_completion_length,
        max_steps=args.max_steps,
        logging_steps=5,
        save_steps=25,
        save_total_limit=3,
        bf16=True,
        report_to="none",
    )
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
        trainer.push_to_hub(args.push_to_hub)


if __name__ == "__main__":
    main()
