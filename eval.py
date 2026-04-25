"""Evaluate CORP-ENV policies through the real OpenEnv environment.

Examples:
  uv run python eval.py --policy scripted_weak --output results/baseline_eval.jsonl
  uv run python eval.py --policy oracle --output results/oracle_eval.jsonl
  uv run python eval.py --policy openai --model Qwen/Qwen2.5-7B-Instruct
  uv run python eval.py --policy hf --model outputs/sft_adapter --adapter outputs/grpo_adapter
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from corp_env.models import CorpAction  # noqa: E402
from scripts._trajectory_utils import (  # noqa: E402
    DEFAULT_TASKS,
    extract_json_object,
    normalize_action_obj,
    observation_message,
    oracle_actions,
    write_jsonl,
)
from server.agents.master_prompts import build_system_prompt  # noqa: E402
from server.environment import CorpEnvironment  # noqa: E402
from server.llm_env import openai_client_kwargs_master  # noqa: E402


def weak_actions(task_id: str) -> List[Dict[str, Any]]:
    """A deliberately weak, deterministic baseline for no-GPU smoke comparisons."""
    if task_id == "e1_launch_readiness":
        return [
            {
                "action_type": "delegate",
                "agent_id": "qa_engineer",
                "payload": "Give launch status.",
            },
            {"action_type": "finalize", "payload": "GO"},
        ]
    if task_id == "m1_budget_reallocation":
        return [
            {
                "action_type": "delegate",
                "agent_id": "dev_lead",
                "payload": "Say whether we need GPUs.",
            },
            {"action_type": "finalize", "payload": json.dumps({"phase_1": "Buy GPUs now."})},
        ]
    return [
        {"action_type": "delegate", "agent_id": "cto", "payload": "Assess acquisition offer."},
        {
            "action_type": "finalize",
            "payload": json.dumps(
                {
                    "counter_offer": "Ask for more.",
                    "deadline": "Soon.",
                    "retention_plan": "Keep key staff.",
                }
            ),
        },
    ]


class HFPolicy:
    def __init__(self, model: str, adapter: Optional[str], max_new_tokens: int) -> None:
        try:
            import torch
            from peft import PeftModel
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise SystemExit(
                "HF evaluation requires torch, transformers, and peft. "
                "Install the training extras on the GPU machine."
            ) from exc

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )
        if adapter:
            self.model = PeftModel.from_pretrained(self.model, adapter)
        self.max_new_tokens = max_new_tokens

    def complete(self, messages: List[Dict[str, str]]) -> str:
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with self.torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        new_tokens = out[0][inputs["input_ids"].shape[1] :]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


class OpenAIPolicy:
    def __init__(self, model: str, max_new_tokens: int) -> None:
        load_dotenv()
        kwargs = openai_client_kwargs_master()
        if not kwargs.get("api_key"):
            raise SystemExit("Set CORP_MASTER_API_KEY, HF_TOKEN, or OPENAI_API_KEY for --policy openai.")
        self.client = OpenAI(**kwargs)
        self.model = model or os.getenv("CORP_MASTER_MODEL") or os.getenv("MODEL_NAME")
        if not self.model:
            raise SystemExit("Pass --model or set CORP_MASTER_MODEL/MODEL_NAME.")
        self.max_new_tokens = max_new_tokens

    def complete(self, messages: List[Dict[str, str]]) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0,
            max_tokens=self.max_new_tokens,
        )
        return (resp.choices[0].message.content or "").strip()


def run_scripted_episode(task_id: str, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
    env = CorpEnvironment()
    obs = env.reset(task_id=task_id)
    rewards: List[float] = []
    errors: List[str] = []
    for action_obj in actions:
        action = CorpAction.model_validate(action_obj)
        obs = env.step(action)
        rewards.append(float(obs.reward or 0.0))
        if obs.error:
            errors.append(obs.error)
        if obs.done:
            break
    verifier = env.task.verifier(obs.swd)
    return episode_record(task_id, "scripted", env, rewards, errors, obs.swd)


def run_model_episode(
    *,
    task_id: str,
    policy: Any,
    max_steps: int,
) -> Dict[str, Any]:
    env = CorpEnvironment()
    obs = env.reset(task_id=task_id)
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": build_system_prompt(obs.master_tier, obs.role)}
    ]
    rewards: List[float] = []
    errors: List[str] = []
    invalid_actions = 0

    for step in range(max_steps):
        messages.append({"role": "user", "content": observation_message(step, obs)})
        raw = policy.complete(messages)
        messages.append({"role": "assistant", "content": raw})
        try:
            action_obj = normalize_action_obj(extract_json_object(raw))
            action = CorpAction.model_validate(action_obj)
        except Exception as exc:
            invalid_actions += 1
            action = CorpAction(action_type="query_swd", payload="$.phase")
            errors.append(f"invalid_action: {exc}")
        obs = env.step(action)
        rewards.append(float(obs.reward or 0.0))
        if obs.error:
            errors.append(obs.error)
        if obs.done:
            break

    rec = episode_record(task_id, "model", env, rewards, errors, obs.swd)
    rec["invalid_action_count"] += invalid_actions
    return rec


def episode_record(
    task_id: str,
    policy_kind: str,
    env: CorpEnvironment,
    rewards: List[float],
    errors: List[str],
    swd: Dict[str, Any],
) -> Dict[str, Any]:
    verifier = env.task.verifier(swd)
    milestones = swd.get("milestones", []) or []
    completed = [m for m in milestones if m.get("status") == "complete"]
    missed = [m for m in milestones if m.get("status") == "missed"]
    terminal_reward = rewards[-1] if rewards else 0.0
    pass_rate = sum(1 for v in verifier.values() if v) / max(len(verifier), 1)
    return {
        "task_id": task_id,
        "policy_kind": policy_kind,
        "steps": env.turn,
        "total_reward": round(sum(rewards), 6),
        "terminal_reward": round(terminal_reward, 6),
        "reward_trace": rewards,
        "verifier_pass_rate": round(pass_rate, 6),
        "passed_checks": [k for k, v in verifier.items() if v],
        "failed_checks": [k for k, v in verifier.items() if not v],
        "milestones_total": len(milestones),
        "milestones_complete": len(completed),
        "milestones_missed": len(missed),
        "invalid_action_count": 0,
        "env_error_count": len(errors),
        "errors": errors,
        "final_swd_version": int(swd.get("swd_version", 0)),
        "success": bool(pass_rate >= 0.99 and not missed),
    }


def summarize(rows: List[Dict[str, Any]], label: str) -> None:
    by_task = {}
    for row in rows:
        by_task.setdefault(row["task_id"], []).append(row)
    print(f"\n[{label}] {len(rows)} episodes")
    for task_id, task_rows in by_task.items():
        avg_reward = sum(r["terminal_reward"] for r in task_rows) / len(task_rows)
        avg_pass = sum(r["verifier_pass_rate"] for r in task_rows) / len(task_rows)
        success = sum(1 for r in task_rows if r["success"]) / len(task_rows)
        print(
            f"- {task_id}: terminal_reward={avg_reward:.3f} "
            f"pass_rate={avg_pass:.3f} success={success:.3f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate CORP-ENV model stages.")
    parser.add_argument("--policy", choices=["scripted_weak", "oracle", "openai", "hf"], default="scripted_weak")
    parser.add_argument("--label", default="", help="Model stage label written to each row.")
    parser.add_argument("--model", default="", help="OpenAI/HF model id or local model path.")
    parser.add_argument("--adapter", default="", help="Optional PEFT adapter path for --policy hf.")
    parser.add_argument("--tasks", default=",".join(DEFAULT_TASKS))
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--max-steps", type=int, default=30)
    parser.add_argument("--max-new-tokens", type=int, default=1536)
    parser.add_argument("--output", default="results/eval.jsonl")
    args = parser.parse_args()

    os.environ.setdefault("CORP_STUB_WORKERS", "1")
    os.environ.setdefault("CORP_DISABLE_LLM_JUDGE", "1")

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    rows: List[Dict[str, Any]] = []
    policy: Any = None
    if args.policy == "openai":
        policy = OpenAIPolicy(args.model, args.max_new_tokens)
    elif args.policy == "hf":
        if not args.model:
            raise SystemExit("--policy hf requires --model")
        policy = HFPolicy(args.model, args.adapter or None, args.max_new_tokens)

    for ep in range(args.episodes):
        for task_id in tasks:
            if args.policy == "scripted_weak":
                row = run_scripted_episode(task_id, weak_actions(task_id))
            elif args.policy == "oracle":
                row = run_scripted_episode(task_id, oracle_actions(task_id, ep))
            else:
                max_steps = args.max_steps * 2 if task_id == "h1_acquisition_defence" else args.max_steps
                row = run_model_episode(task_id=task_id, policy=policy, max_steps=max_steps)
            row["episode_index"] = ep
            row["model_stage"] = args.label or args.policy
            row["model"] = args.model
            row["adapter"] = args.adapter
            rows.append(row)

    out = Path(args.output)
    write_jsonl(out, rows)
    summarize(rows, args.label or args.policy)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
