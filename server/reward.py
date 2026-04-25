"""Multi-component reward, coherence, optional LLM judge, and anti-gaming penalties."""

from __future__ import annotations

import json
import os
import re
from typing import Any, Callable, Dict, List, Optional

from openai import OpenAI

from server.llm_env import openai_client_kwargs_judge
from server.swd import (
    REQUIRED_TOP_LEVEL,
    VALID_PHASES,
    conflict_ids_from_swd,
    validate_milestone_shapes,
)
from server.verifiers import check_no_verbatim_copy


def compute_swd_coherence(swd: Dict[str, Any]) -> float:
    """Deterministic structural coherence score in [0, 1]."""
    checks: List[bool] = []

    checks.append(all(k in swd for k in REQUIRED_TOP_LEVEL))
    checks.append(swd.get("phase") in VALID_PHASES)
    checks.append(validate_milestone_shapes(swd))

    conflict_ids = conflict_ids_from_swd(swd)
    res_ok = True
    for r in swd.get("conflict_resolutions", []) or []:
        if isinstance(r, dict) and r.get("conflict_id") is not None:
            if r["conflict_id"] not in conflict_ids:
                res_ok = False
                break
    checks.append(res_ok)

    v = swd.get("swd_version")
    checks.append(isinstance(v, int) and v >= 1)

    log = swd.get("reasoning_log", []) or []
    checks.append(
        all(isinstance(e, dict) and "turn" in e for e in log) if log else True
    )

    if not checks:
        return 0.0
    return sum(1 for c in checks if c) / len(checks)


def call_llm_judge(swd: Dict[str, Any], task_goal: str) -> float:
    """
    Fast LLM judge (optional). Returns score in [0, 1] from YES count / 3.
    Uses CORP_JUDGE_* then global API keys (see server/llm_env.py). No call without a key.
    """
    if os.getenv("CORP_DISABLE_LLM_JUDGE", "").lower() in ("1", "true", "yes"):
        return 0.0

    kwargs = openai_client_kwargs_judge()
    if not kwargs.get("api_key"):
        return 0.0

    model = os.getenv("CORP_JUDGE_MODEL", "Qwen/Qwen2.5-7B-Instruct")

    prompt = f"""
You are evaluating a corporate decision document. Answer each question with YES or NO only.

DOCUMENT:
{json.dumps(swd, indent=2)[:3000]}

TASK GOAL:
{task_goal}

QUESTIONS:
1. Does the final_recommendation address all three key stakeholder concerns present in the scenario?
2. Are the conflict_resolutions logically consistent with the agent_reports provided?
3. Does the reasoning_log show evidence of iterative thinking (not just a single dump)?

Respond in this exact format:
Q1: YES/NO
Q2: YES/NO
Q3: YES/NO
"""
    client = OpenAI(**kwargs)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=64,
        temperature=0.0,
    )
    text = (resp.choices[0].message.content or "").strip()
    yes_count = len(re.findall(r"Q\d:\s*YES", text, re.I))
    return yes_count / 3.0


def reasoning_log_is_duplicated(swd: Dict[str, Any]) -> bool:
    log = swd.get("reasoning_log", []) or []
    if len(log) < 2:
        return False
    texts = [str(e.get("text", e)) for e in log if isinstance(e, dict)]
    if len(set(texts)) < len(texts) * 0.5 and len(texts) >= 4:
        return True
    return False


REWARD_HACKING_PENALTIES: List[Callable[[Dict[str, Any], Dict[str, Any]], float]] = [
    lambda swd, ep: 0.3
    if ep.get("finalized") and int(swd.get("swd_version", 0)) < 4
    else 0.0,
    lambda swd, ep: 0.1 * float(ep.get("consecutive_same_agent_calls", 0)),
    lambda swd, ep: 0.25 if not check_no_verbatim_copy(swd) else 0.0,
    lambda swd, ep: 0.5 if ep.get("version_decreased") else 0.0,
    lambda swd, ep: 0.15 if reasoning_log_is_duplicated(swd) else 0.0,
]


def compute_reward(
    swd: Dict[str, Any],
    verify_result: Dict[str, bool],
    episode_metadata: Dict[str, Any],
    task_goal: str,
) -> float:
    """
    Weighted reward in roughly [-1, 1] after penalties (guide Part 2).
    verify_result: dict of bool criterion name -> passed.
    """
    if not verify_result:
        completion = 0.0
    else:
        completion = sum(verify_result.values()) / len(verify_result)

    coherence = compute_swd_coherence(swd)

    milestones = swd.get("milestones", []) or []
    turn_completed: Dict[str, int] = episode_metadata.get("turn_completed", {}) or {}
    completed_on_time = 0
    for m in milestones:
        mid = m.get("id")
        if m.get("status") == "complete" and mid is not None:
            done_turn = turn_completed.get(mid, 999)
            if done_turn <= int(m.get("due_by_turn", 999)):
                completed_on_time += 1
    milestone_score = completed_on_time / max(len(milestones), 1)

    log_entries = swd.get("reasoning_log", []) or []
    unique_turns: set = set()
    for e in log_entries:
        if isinstance(e, dict) and e.get("turn") is not None:
            unique_turns.add(e["turn"])
    reasoning_score = min(len(unique_turns) / 5.0, 1.0)

    llm_score = 0.0
    if episode_metadata.get("finalized"):
        llm_score = call_llm_judge(swd, task_goal)

    raw = (
        0.35 * completion
        + 0.25 * coherence
        + 0.20 * milestone_score
        + 0.10 * reasoning_score
        + 0.10 * llm_score
    )

    penalties = 0.0
    penalties += float(episode_metadata.get("invalid_json_count", 0)) * 0.15
    penalties += float(episode_metadata.get("wrong_agent_count", 0)) * 0.10
    penalties += 0.20 if episode_metadata.get("token_budget_exceeded") else 0.0
    penalties += sum(0.08 for m in milestones if m.get("status") == "missed")

    for fn in REWARD_HACKING_PENALTIES:
        penalties += fn(swd, episode_metadata)

    return max(0.0, min(1.0, raw - penalties))
