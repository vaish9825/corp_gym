"""Shared utilities for CORP-ENV data prep, verification, and evaluation."""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from corp_env.models import CorpAction, CorpObservation  # noqa: E402
from server.agents.master_prompts import build_system_prompt  # noqa: E402
from server.environment import CorpEnvironment  # noqa: E402


DEFAULT_TASKS = ("e1_launch_readiness", "m1_budget_reallocation", "h1_acquisition_defence")


@dataclass
class ReplayResult:
    example_id: str
    task_id: str
    status: str
    reject_reason: str
    actions: List[Dict[str, Any]]
    steps: int
    total_reward: float
    terminal_reward: float
    verifier_result: Dict[str, bool]
    missed_milestones: List[str]
    invalid_action_count: int
    env_error_count: int
    final_swd_version: int
    final_swd: Dict[str, Any]

    @property
    def verifier_pass_rate(self) -> float:
        if not self.verifier_result:
            return 0.0
        return sum(1 for v in self.verifier_result.values() if v) / len(self.verifier_result)

    def to_record(self) -> Dict[str, Any]:
        failed = [k for k, v in self.verifier_result.items() if not v]
        passed = [k for k, v in self.verifier_result.items() if v]
        return {
            "example_id": self.example_id,
            "task_id": self.task_id,
            "status": self.status,
            "reject_reason": self.reject_reason,
            "steps": self.steps,
            "total_reward": round(self.total_reward, 6),
            "terminal_reward": round(self.terminal_reward, 6),
            "verifier_pass_rate": round(self.verifier_pass_rate, 6),
            "passed_checks": passed,
            "failed_checks": failed,
            "missed_milestones": self.missed_milestones,
            "invalid_action_count": self.invalid_action_count,
            "env_error_count": self.env_error_count,
            "final_swd_version": self.final_swd_version,
            "actions": self.actions,
            "final_swd": self.final_swd,
        }


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                yield {
                    "example_id": f"{path.stem}:{line_no}",
                    "task_id": "",
                    "actions": [],
                    "_load_error": f"invalid JSONL line {line_no}: {exc}",
                }
                continue
            obj.setdefault("example_id", f"{path.stem}:{line_no}")
            yield obj


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract_json_object(text: str) -> Dict[str, Any]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```\s*$", "", cleaned).strip()
    try:
        obj = json.loads(cleaned)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    start = cleaned.find("{")
    if start == -1:
        raise ValueError("no JSON object found")
    depth = 0
    in_string = False
    escape_next = False
    for idx in range(start, len(cleaned)):
        ch = cleaned[idx]
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                obj = json.loads(cleaned[start : idx + 1])
                if not isinstance(obj, dict):
                    raise ValueError("extracted JSON is not an object")
                return obj
    raise ValueError("unbalanced JSON object")


def normalize_action_obj(raw: Any) -> Dict[str, Any]:
    if isinstance(raw, str):
        raw = extract_json_object(raw)
    if not isinstance(raw, dict):
        raise ValueError("action must be a JSON object or string containing one")
    raw = dict(raw)
    raw.pop("thought", None)
    if "payload" in raw and not isinstance(raw["payload"], str):
        raw["payload"] = json.dumps(raw["payload"], ensure_ascii=False)
    raw.setdefault("payload", "")
    if raw.get("agent_id") == "":
        raw["agent_id"] = None
    return CorpAction.model_validate(raw).model_dump(mode="json", exclude_none=True)


def extract_actions(example: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: Any = (
        example.get("actions")
        or example.get("trajectory")
        or example.get("steps")
        or example.get("messages")
    )
    if candidates is None:
        raise ValueError("example has no actions/trajectory/steps/messages")

    raw_actions: List[Any] = []
    if candidates and isinstance(candidates, list) and isinstance(candidates[0], dict):
        if "role" in candidates[0]:
            raw_actions = [
                m.get("content", "")
                for m in candidates
                if m.get("role") == "assistant" and m.get("content")
            ]
        elif "action" in candidates[0]:
            raw_actions = [step.get("action") for step in candidates]
        else:
            raw_actions = candidates
    elif isinstance(candidates, list):
        raw_actions = candidates
    else:
        raise ValueError("trajectory container must be a list")

    return [normalize_action_obj(action) for action in raw_actions]


def observation_message(step: int, obs: CorpObservation) -> str:
    parts = [
        f"--- Step {step} ---",
        f"Role: {obs.role} (tier: {obs.master_tier})",
        f"Task: {obs.task_description}",
        f"Available agents: {', '.join(obs.available_agents)}",
        f"Turn: {obs.turn} tokens_used: {obs.tokens_used}/{obs.token_budget}",
    ]
    if obs.available_actions:
        parts.append("Available actions:\n- " + "\n- ".join(obs.available_actions))
    if obs.next_step_hint:
        parts.append(f"Next-step hint: {obs.next_step_hint}")
    if obs.recent_actions:
        parts.append("Recent actions: " + " | ".join(obs.recent_actions))
    parts.append(f"SWD:\n{json.dumps(obs.swd, indent=2, ensure_ascii=False)[:12000]}")
    if obs.agent_last_output:
        parts.append(f"Last worker output:\n{obs.agent_last_output[:4000]}")
    if obs.query_result is not None:
        parts.append(f"Query result: {json.dumps(obs.query_result, ensure_ascii=False)[:2000]}")
    if obs.error:
        parts.append(f"Error: {obs.error}")
    parts.append(f"Reward (last step): {obs.reward}")
    parts.append("Respond with your next JSON action.")
    return "\n".join(parts)


def actions_to_sft_messages(task_id: str, actions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    env = CorpEnvironment()
    obs = env.reset(task_id=task_id)
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": build_system_prompt(obs.master_tier, obs.role)}
    ]
    for idx, action_obj in enumerate(actions):
        messages.append({"role": "user", "content": observation_message(idx, obs)})
        messages.append(
            {
                "role": "assistant",
                "content": json.dumps(action_obj, ensure_ascii=False),
            }
        )
        obs = env.step(CorpAction.model_validate(action_obj))
        if obs.done:
            break
    return messages


def keep_decision(task_id: str, terminal_reward: float, verifier: Dict[str, bool], missed: List[str]) -> str:
    pass_count = sum(1 for v in verifier.values() if v)
    total = max(len(verifier), 1)
    if missed:
        return "missed_milestones"
    if task_id == "e1_launch_readiness":
        if terminal_reward >= 0.65 and pass_count == total:
            return ""
        return "below_e1_threshold"
    if task_id == "m1_budget_reallocation":
        if terminal_reward >= 0.70 and pass_count >= 5:
            return ""
        return "below_m1_threshold"
    if task_id == "h1_acquisition_defence":
        if terminal_reward >= 0.65 and pass_count >= 7:
            return ""
        return "below_h1_threshold"
    return "" if terminal_reward >= 0.65 else "below_generic_threshold"


def replay_actions(
    *,
    example_id: str,
    task_id: str,
    actions: List[Dict[str, Any]],
    strict_thresholds: bool = True,
) -> ReplayResult:
    os.environ.setdefault("CORP_STUB_WORKERS", "1")
    os.environ.setdefault("CORP_DISABLE_LLM_JUDGE", "1")

    env = CorpEnvironment()
    obs = env.reset(task_id=task_id)
    total_reward = 0.0
    terminal_reward = 0.0
    invalid_action_count = 0
    env_error_count = 0
    reject_reason = ""

    for idx, action_obj in enumerate(actions, start=1):
        try:
            action = CorpAction.model_validate(action_obj)
        except Exception as exc:
            invalid_action_count += 1
            reject_reason = f"invalid_action_at_step_{idx}: {exc}"
            break

        obs = env.step(action)
        reward = float(obs.reward or 0.0)
        total_reward += reward
        terminal_reward = reward
        if obs.error:
            env_error_count += 1
        if obs.done:
            break

    final_swd = obs.swd
    verifier = env.task.verifier(final_swd)
    missed = [
        str(m.get("id"))
        for m in final_swd.get("milestones", []) or []
        if m.get("status") == "missed"
    ]
    if not reject_reason:
        if not actions:
            reject_reason = "empty_trajectory"
        elif not obs.done:
            reject_reason = "trajectory_did_not_terminate"
        elif actions[-1].get("action_type") != "finalize" and not env.episode_metadata.get("finalized"):
            reject_reason = "missing_finalize"
        elif env_error_count:
            reject_reason = "environment_errors"
        elif strict_thresholds:
            reject_reason = keep_decision(task_id, terminal_reward, verifier, missed)

    status = "clean" if not reject_reason else "rejected"
    return ReplayResult(
        example_id=example_id,
        task_id=task_id,
        status=status,
        reject_reason=reject_reason,
        actions=actions,
        steps=env.turn,
        total_reward=total_reward,
        terminal_reward=terminal_reward,
        verifier_result=verifier,
        missed_milestones=missed,
        invalid_action_count=invalid_action_count,
        env_error_count=env_error_count,
        final_swd_version=int(final_swd.get("swd_version", 0)),
        final_swd=final_swd,
    )


def oracle_actions(task_id: str, variant: int = 0) -> List[Dict[str, Any]]:
    if task_id == "e1_launch_readiness":
        rec = "NO_GO" if variant % 2 == 0 else "GO"
        return [
            {
                "action_type": "delegate",
                "agent_id": "qa_engineer",
                "payload": "Report launch test status, blockers, and gate recommendation.",
            },
            {
                "action_type": "log_reasoning",
                "payload": "QA evidence is the controlling launch gate; final call should reflect blocker risk.",
            },
            {
                "action_type": "log_decision",
                "payload": f"Use QA gate evidence and finalize as {rec}.",
            },
            {"action_type": "finalize", "payload": rec},
        ]
    if task_id == "m1_budget_reallocation":
        phase = {
            "phase_1": "Buy a constrained GPU block for the highest-priority training runs.",
            "phase_2": "Expand only after finance confirms runway and measured utilization.",
            "guardrail": "Cap spend, report weekly burn, and pause if runway drops below target.",
        }
        return [
            {
                "action_type": "delegate",
                "agent_id": "dev_lead",
                "payload": "Estimate minimum GPU capacity needed for the next model-training milestone.",
            },
            {
                "action_type": "delegate",
                "agent_id": "fpa_manager",
                "payload": "State the budget, runway, and spend constraints for GPU cluster time.",
            },
            {
                "action_type": "log_reasoning",
                "payload": "The plan must balance model training urgency with budget, cost, spend, cash, runway, and burn constraints.",
            },
            {
                "action_type": "log_conflict",
                "payload": json.dumps(
                    {
                        "id": "c1",
                        "summary": "Engineering wants more GPU capacity than finance can approve immediately.",
                        "source_agents": ["dev_lead", "fpa_manager"],
                    }
                ),
            },
            {
                "action_type": "log_resolution",
                "payload": json.dumps(
                    {
                        "conflict_id": "c1",
                        "resolution_type": "phased_budget",
                        "text": "Approve a capped phase_1 GPU purchase with weekly finance review.",
                    }
                ),
            },
            {"action_type": "finalize", "payload": json.dumps(phase)},
        ]
    if task_id == "h1_acquisition_defence":
        final = {
            "counter_offer": "Open at 3.2x with a board-approved walk-down floor near 2.6x.",
            "deadline": "Force a decision inside 45 days to preserve cash runway and reduce retention risk.",
            "retention_plan": "Offer retention grants and role clarity for critical engineering leaders.",
        }
        return [
            {"action_type": "delegate", "agent_id": "cto", "payload": "Assess IP leverage and technical moat."},
            {"action_type": "delegate", "agent_id": "cfo", "payload": "Assess cash runway and valuation ceiling."},
            {"action_type": "delegate", "agent_id": "chro", "payload": "Assess retention risk and people constraints."},
            {"action_type": "log_reasoning", "payload": "CTO input supports a higher counter because the IP moat is meaningful."},
            {
                "action_type": "log_conflict",
                "payload": json.dumps(
                    {
                        "id": "c1",
                        "summary": "CTO valuation ambition conflicts with CFO runway and cash constraints.",
                        "source_agents": ["cto", "cfo"],
                    }
                ),
            },
            {"action_type": "log_reasoning", "payload": "CFO input limits how long the negotiation can remain open."},
            {
                "action_type": "log_conflict",
                "payload": json.dumps(
                    {
                        "id": "c2",
                        "summary": "A slow process increases CHRO retention risk for key engineering talent.",
                        "source_agents": ["chro", "cto"],
                    }
                ),
            },
            {
                "action_type": "log_resolution",
                "payload": json.dumps(
                    {
                        "conflict_id": "c1",
                        "resolution_type": "bounded_counter",
                        "text": "Ask above the CFO ceiling but set a fast deadline and walk-down logic.",
                    }
                ),
            },
            {"action_type": "advance_phase", "payload": "analysis"},
            {"action_type": "log_reasoning", "payload": "The 7 month runway makes delay costly and should shape the deadline."},
            {"action_type": "advance_phase", "payload": "decision"},
            {"action_type": "log_decision", "payload": "Proceed with a counter that acknowledges 7 month runway and cash limits."},
            {"action_type": "log_reasoning", "payload": "Retention incentives are required before the market reads uncertainty."},
            {"action_type": "advance_phase", "payload": "execution"},
            {"action_type": "log_reasoning", "payload": "Final recommendation integrates valuation, deadline, and retention plan."},
            {"action_type": "finalize", "payload": json.dumps(final)},
        ]
    raise ValueError(f"unknown task_id: {task_id}")
