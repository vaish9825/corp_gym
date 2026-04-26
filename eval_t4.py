"""Evaluate CORP-ENV policies — T4 / Colab friendly HF path (FP16, local adapter checks).

Same behavior as ``eval.py`` for scripted/oracle/openai; ``--policy hf`` uses FP16 by default
on CUDA and refuses missing local adapter paths so PEFT does not treat ``outputs/...`` as a
Hub repo id.
"""

from __future__ import annotations

import argparse
import json
import os
import re
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
    def __init__(
        self,
        model: str,
        adapter: Optional[str],
        max_new_tokens: int,
        *,
        use_fp16: bool,
    ) -> None:
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
        if use_fp16 and not torch.cuda.is_available():
            print("Warning: --fp16 requested but CUDA unavailable; using float32 for HF model.")
            use_fp16 = False

        torch_dtype = torch.float16 if use_fp16 else torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float32

        self.tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model,
            device_map="auto",
            torch_dtype=torch_dtype,
            trust_remote_code=True,
        )
        if adapter:
            adapter_path = Path(adapter).expanduser().resolve()
            if not adapter_path.is_dir():
                raise SystemExit(
                    f"Adapter path is not a directory (refusing Hub fallback): {adapter_path}"
                )
            cfg = adapter_path / "adapter_config.json"
            if not cfg.is_file():
                raise SystemExit(
                    f"Missing adapter_config.json under local adapter directory: {adapter_path}\n"
                    "Train or copy a PEFT adapter here before running eval; "
                    "relative paths are resolved from the current working directory."
                )
            self.model = PeftModel.from_pretrained(self.model, str(adapter_path))
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


def slugify(value: str, fallback: str = "unknown") -> str:
    value = (value or "").strip()
    if not value:
        return fallback
    value = value.replace("\\", "/").rstrip("/")
    value = value.split("/")[-1] if "/" in value else value
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    value = value.strip("-._")
    return value or fallback


def default_output_path(args: argparse.Namespace) -> Path:
    stage = slugify(args.label or args.policy, "eval")
    model_slug = slugify(args.model, args.policy)
    adapter_slug = slugify(args.adapter, "no-adapter")
    if args.adapter:
        run_slug = f"{model_slug}__{adapter_slug}__{stage}"
    else:
        run_slug = f"{model_slug}__{stage}"
    return Path(args.results_root) / "runs" / run_slug / f"{stage}_eval.jsonl"


def write_run_metadata(path: Path, args: argparse.Namespace, rows: List[Dict[str, Any]]) -> None:
    by_task: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        by_task.setdefault(row["task_id"], []).append(row)
    summary = {
        "model_stage": args.label or args.policy,
        "policy": args.policy,
        "model": args.model,
        "adapter": args.adapter,
        "tasks": [t.strip() for t in args.tasks.split(",") if t.strip()],
        "episodes": args.episodes,
        "max_steps": args.max_steps,
        "max_new_tokens": args.max_new_tokens,
        "eval_file": str(path),
        "metrics_by_task": {},
        "hf_fp16": getattr(args, "fp16", True),
    }
    for task_id, task_rows in by_task.items():
        summary["metrics_by_task"][task_id] = {
            "avg_terminal_reward": round(
                sum(r["terminal_reward"] for r in task_rows) / len(task_rows), 6
            ),
            "avg_verifier_pass_rate": round(
                sum(r["verifier_pass_rate"] for r in task_rows) / len(task_rows), 6
            ),
            "success_rate": round(
                sum(1 for r in task_rows if r["success"]) / len(task_rows), 6
            ),
        }
    metadata_path = path.with_name("metadata.json")
    metadata_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate CORP-ENV (T4-friendly HF eval).")
    parser.add_argument("--policy", choices=["scripted_weak", "oracle", "openai", "hf"], default="scripted_weak")
    parser.add_argument("--label", default="", help="Model stage label written to each row.")
    parser.add_argument("--model", default="", help="OpenAI/HF model id or local model path.")
    parser.add_argument("--adapter", default="", help="Optional PEFT adapter path for --policy hf.")
    parser.add_argument("--tasks", default=",".join(DEFAULT_TASKS))
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--max-steps", type=int, default=30)
    parser.add_argument("--max-new-tokens", type=int, default=1536)
    parser.add_argument("--results-root", default="results", help="Root for auto-organized eval output.")
    parser.add_argument(
        "--output",
        default="",
        help="Explicit JSONL path. If omitted, writes under results/runs/<model-adapter-label>/.",
    )
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--fp16", dest="fp16", action="store_true", help="HF load/generate in FP16 (default on CUDA).")
    g.add_argument("--bf16", dest="fp16", action="store_false", help="Use BF16 for HF base model when supported.")
    parser.set_defaults(fp16=True)
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
        import torch

        use_fp16 = bool(args.fp16) and torch.cuda.is_available()
        policy = HFPolicy(args.model, args.adapter or None, args.max_new_tokens, use_fp16=use_fp16)

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
            row["policy"] = args.policy
            row["model"] = args.model
            row["adapter"] = args.adapter
            rows.append(row)

    out = Path(args.output) if args.output else default_output_path(args)
    write_jsonl(out, rows)
    write_run_metadata(out, args, rows)
    summarize(rows, args.label or args.policy)
    print(f"\nWrote {out}")
    print(f"Wrote {out.with_name('metadata.json')}")


if __name__ == "__main__":
    main()
