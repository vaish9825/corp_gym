"""CORP-ENV gym: SWD-centric corporate planning with delegate / patch / query / finalize."""

from __future__ import annotations

import json
import os
import random
from typing import Any, Dict, List, Optional, Tuple

from jsonpath_ng import parse as jsonpath_parse

from corp_env.models import CorpAction, CorpObservation
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import EnvironmentMetadata, State

from server.agents.personas import AgentSlot
from server.agents.prompts import normalize_worker_id, swd_report_key_for_family
from server.memory import append_master_episode, append_worker_episode
from server.reward import compute_reward, compute_swd_coherence
from server.swd import (
    VALID_PHASES,
    new_episode_id,
    try_apply_json_patch,
    validate_swd_structure,
)
from server.tasks import TASKS
from server.tasks.base import CorpTask
from server.worker_client import call_worker_model

SAFETY_MAX_TURNS = 256

_AVAILABLE_ACTIONS_HINT = [
    "delegate(agent_id, payload=task_prompt) -> consult a worker",
    "log_reasoning(payload=text) -> append a reasoning_log entry",
    "log_decision(payload=text) -> append to decisions",
    "log_conflict(payload=JSON {id?, summary, source_agents?}) -> append to conflicts_identified",
    "log_resolution(payload=JSON {conflict_id, resolution_type?, text?}) -> append to conflict_resolutions",
    "advance_phase(payload=\"analysis\"|\"decision\"|\"execution\")",
    "query_swd(payload=JSONPath) -> read the SWD",
    "update_swd(payload=RFC6902 JSON Patch string) -> power edits",
    "finalize(payload=GO|NO_GO|JSON object) -> end the episode",
]


class CorpEnvironment(Environment[CorpAction, CorpObservation, State]):
    """Shared workspace document environment (master + frozen workers)."""

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self) -> None:
        super().__init__()
        self.task: CorpTask
        self.swd: Dict[str, Any] = {}
        self.turn = 0
        self.tokens_used = 0
        self.episode_metadata: Dict[str, Any] = {}
        self._episode_id: str = ""

    def get_metadata(self) -> EnvironmentMetadata:
        return EnvironmentMetadata(
            name="corp-env",
            description=(
                "Multi-agent corporate decision environment with shared workspace "
                "document (SWD) governance."
            ),
            version="0.2.0",
        )

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> CorpObservation:
        if seed is not None:
            random.seed(seed)

        tid = (
            kwargs.get("task_id")
            or os.environ.get("CORP_TASK_ID")
            or random.choice(list(TASKS.keys()))
        )
        if tid not in TASKS:
            tid = "e1_launch_readiness"

        self.task = TASKS[tid]
        self._episode_id = episode_id or new_episode_id()
        self.swd = self.task.initial_swd(self._episode_id)
        self.turn = 0
        self.tokens_used = 0
        self.episode_metadata = {
            "task_id": self.task.task_id,
            "invalid_json_count": 0,
            "wrong_agent_count": 0,
            "consecutive_same_agent_calls": 0,
            "last_agent": None,
            "finalized": False,
            "version_decreased": False,
            "turn_completed": {},
            "token_budget_exceeded": False,
            "recent_actions": [],
        }
        return self._observation(reward=0.0, done=False, agent_last_output=None, query_result=None)

    def step(
        self,
        action: CorpAction,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> CorpObservation:
        _ = timeout_s, kwargs
        self.turn += 1
        step_reward = 0.0
        done = False
        agent_last_output: Optional[str] = None
        query_result: Any = None
        error: Optional[str] = None

        self._add_tokens(action.payload + (action.agent_id or ""))

        at = action.action_type
        if at == "delegate":
            step_reward, agent_last_output, error = self._step_delegate(action)
        elif at == "update_swd":
            step_reward, error = self._step_update_swd(action)
        elif at == "query_swd":
            query_result, error = self._step_query_swd(action)
        elif at == "finalize":
            step_reward, done, error = self._step_finalize(action)
        elif at == "log_reasoning":
            step_reward, error = self._step_log_reasoning(action)
        elif at == "log_decision":
            step_reward, error = self._step_log_decision(action)
        elif at == "log_conflict":
            step_reward, error = self._step_log_conflict(action)
        elif at == "log_resolution":
            step_reward, error = self._step_log_resolution(action)
        elif at == "advance_phase":
            step_reward, error = self._step_advance_phase(action)
        else:
            error = f"unknown action_type {at}"

        self._push_recent_action(action, error)

        new_milestones = self._update_milestone_status()
        step_reward += 0.2 * len(new_milestones)
        step_reward -= 0.01

        if not done and self.tokens_used > self.task.token_budget:
            self.episode_metadata["token_budget_exceeded"] = True
            step_reward -= 0.20
            done = True

        if not done and self._all_milestones_missed():
            done = True
            step_reward -= 0.1

        if not done and self.turn >= SAFETY_MAX_TURNS:
            done = True
            error = (error or "") + "; safety max turns reached"

        return self._observation(
            reward=step_reward,
            done=done,
            agent_last_output=agent_last_output,
            query_result=query_result,
            error=error,
        )

    @property
    def state(self) -> State:
        return State(
            episode_id=str(self.swd.get("episode_id", self._episode_id)),
            step_count=self.turn,
        )

    def close(self) -> None:
        return None

    # --- internals ---

    def _add_tokens(self, text: str) -> None:
        self.tokens_used += max(8, len(text) // 4)

    def _push_recent_action(self, action: CorpAction, error: Optional[str]) -> None:
        summary = action.action_type
        if action.agent_id:
            summary += f":{action.agent_id}"
        if action.payload:
            snip = action.payload.replace("\n", " ")[:60]
            summary += f" '{snip}'"
        if error:
            summary += " [err]"
        recent: List[str] = self.episode_metadata.setdefault("recent_actions", [])
        recent.append(summary)
        if len(recent) > 5:
            del recent[:-5]

    def _next_step_hint(self) -> Optional[str]:
        """Return a one-line hint for the first pending milestone."""
        for m in self.swd.get("milestones", []) or []:
            if m.get("status") == "pending":
                mid = str(m.get("id", ""))
                label = str(m.get("label", ""))
                # Milestone-specific guidance keyed off the label.
                lbl = label.lower()
                if "agent_report" in lbl or "consult" in lbl or "populated" in lbl:
                    slot_ids = self.task.available_agents
                    missing = self._slots_missing_reports()
                    target = missing[0] if missing else (slot_ids[0] if slot_ids else "an advisor")
                    return (
                        f"Milestone {mid}: use delegate with agent_id='{target}' "
                        f"and a specific prompt about the task."
                    )
                if "conflict" in lbl and "resolv" in lbl:
                    return (
                        f"Milestone {mid}: call log_conflict then log_resolution "
                        f"(conflict_id matching the logged conflict)."
                    )
                if "conflict" in lbl:
                    return f"Milestone {mid}: call log_conflict with a short summary."
                if "phased" in lbl or "recommendation" in lbl or "final" in lbl:
                    return f"Milestone {mid}: call finalize with the required payload."
                if "reasoning_log" in lbl:
                    return (
                        f"Milestone {mid}: call log_reasoning a few more times "
                        f"(different turns) to build the reasoning_log."
                    )
                return f"Milestone {mid}: {label}"
        return "All milestones complete - call finalize with your recommendation."

    def _slots_missing_reports(self) -> List[str]:
        out: List[str] = []
        ar = self.swd.get("agent_reports", {}) or {}
        for slot in self.task.agent_slots:
            key = swd_report_key_for_family(slot.family)
            if ar.get(key) is None:
                out.append(slot.id)
        return out

    def _observation(
        self,
        *,
        reward: float,
        done: bool,
        agent_last_output: Optional[str],
        query_result: Any,
        error: Optional[str] = None,
    ) -> CorpObservation:
        return CorpObservation(
            task_description=self.task.description,
            role=self.task.role,
            master_tier=getattr(self.task, "master_tier", "senior"),
            available_agents=list(self.task.available_agents),
            available_actions=list(_AVAILABLE_ACTIONS_HINT),
            next_step_hint=self._next_step_hint(),
            recent_actions=list(self.episode_metadata.get("recent_actions", [])),
            swd=json.loads(json.dumps(self.swd)),
            agent_last_output=agent_last_output,
            query_result=query_result,
            tokens_used=self.tokens_used,
            token_budget=self.task.token_budget,
            turn=self.turn,
            reward=reward,
            done=done,
            error=error,
            metadata={"episode_metadata": dict(self.episode_metadata)},
        )

    def _step_delegate(
        self, action: CorpAction
    ) -> Tuple[float, Optional[str], Optional[str]]:
        reward = 0.0
        canonical = normalize_worker_id(action.agent_id)
        if canonical is None or canonical not in self.task.available_agents:
            reward -= 0.10
            self.episode_metadata["wrong_agent_count"] += 1
            return reward, None, "invalid or unavailable agent_id for this task"

        slot = self.task.get_slot(canonical)
        if slot is None:
            reward -= 0.10
            self.episode_metadata["wrong_agent_count"] += 1
            return reward, None, f"no slot registered for {canonical}"

        if canonical == self.episode_metadata.get("last_agent"):
            self.episode_metadata["consecutive_same_agent_calls"] += 1
        else:
            self.episode_metadata["consecutive_same_agent_calls"] = 0
        self.episode_metadata["last_agent"] = canonical

        task_text = action.payload.strip()
        extra = self.task.intel_injections.get(canonical)
        if extra:
            task_text = f"{task_text}\n\n{extra}".strip()

        key = swd_report_key_for_family(slot.family)
        existing = self.swd.get("agent_reports", {}).get(key)
        if existing is None:
            reward += 0.1
        else:
            reward -= 0.02

        if self.episode_metadata["consecutive_same_agent_calls"] > 1:
            reward -= 0.05 * self.episode_metadata["consecutive_same_agent_calls"]

        out = call_worker_model(
            slot,
            task_text or "Provide your assessment.",
            task_id=self.task.task_id,
            episode_id=self._episode_id,
            turn=self.turn,
        )
        self._add_tokens(out)
        self.swd.setdefault("agent_reports", {})[key] = out
        self.swd["swd_version"] = int(self.swd.get("swd_version", 0)) + 1
        return reward, out, None

    def _step_update_swd(self, action: CorpAction) -> Tuple[float, Optional[str]]:
        reward = 0.0
        try:
            ops = json.loads(action.payload)
            if not isinstance(ops, list):
                raise ValueError("JSON Patch must be a list of operations")
        except (json.JSONDecodeError, ValueError) as e:
            self.episode_metadata["invalid_json_count"] += 1
            reward -= 0.15
            return reward, f"invalid JSON patch: {e}"

        if not ops:
            reward -= 0.05

        old_phase = self.swd.get("phase")
        old_ver = int(self.swd.get("swd_version", 0))
        new_doc, err = try_apply_json_patch(self.swd, ops)
        if err:
            self.episode_metadata["invalid_json_count"] += 1
            reward -= 0.15
            return reward, err

        if new_doc != self.swd:
            reward += 0.05

        new_phase = new_doc.get("phase")
        if old_phase != new_phase:
            reward += 0.1

        if int(new_doc.get("swd_version", 0)) < old_ver:
            self.episode_metadata["version_decreased"] = True
            reward -= 0.5

        self.swd = new_doc
        reward += 0.15 * compute_swd_coherence(self.swd)
        log = self.swd.get("reasoning_log", []) or []
        if len(log) > 0:
            reward += 0.02
        return reward, None

    def _apply_patch_or_error(
        self, ops: List[Dict[str, Any]]
    ) -> Tuple[float, Optional[str]]:
        reward = 0.0
        new_doc, err = try_apply_json_patch(self.swd, ops)
        if err:
            self.episode_metadata["invalid_json_count"] += 1
            return reward - 0.15, err
        reward += 0.05
        self.swd = new_doc
        reward += 0.15 * compute_swd_coherence(self.swd)
        return reward, None

    def _step_log_reasoning(self, action: CorpAction) -> Tuple[float, Optional[str]]:
        text = (action.payload or "").strip()
        if not text:
            return -0.05, "log_reasoning requires non-empty payload"
        return self._apply_patch_or_error(
            [
                {
                    "op": "add",
                    "path": "/reasoning_log/-",
                    "value": {"turn": self.turn, "text": text},
                }
            ]
        )

    def _step_log_decision(self, action: CorpAction) -> Tuple[float, Optional[str]]:
        text = (action.payload or "").strip()
        if not text:
            return -0.05, "log_decision requires non-empty payload"
        return self._apply_patch_or_error(
            [
                {
                    "op": "add",
                    "path": "/decisions/-",
                    "value": {"turn": self.turn, "summary": text},
                }
            ]
        )

    def _step_log_conflict(self, action: CorpAction) -> Tuple[float, Optional[str]]:
        raw = (action.payload or "").strip()
        if not raw:
            return -0.05, "log_conflict requires non-empty payload"
        try:
            obj = json.loads(raw) if raw.startswith("{") else {"summary": raw}
            if not isinstance(obj, dict):
                return -0.15, "log_conflict payload must be a JSON object or plain string"
        except json.JSONDecodeError as e:
            return -0.15, f"log_conflict invalid JSON: {e}"

        existing = self.swd.get("conflicts_identified", []) or []
        if "id" not in obj or not obj.get("id"):
            obj["id"] = f"c{len(existing) + 1}"
        obj.setdefault("turn", self.turn)

        return self._apply_patch_or_error(
            [{"op": "add", "path": "/conflicts_identified/-", "value": obj}]
        )

    def _step_log_resolution(self, action: CorpAction) -> Tuple[float, Optional[str]]:
        raw = (action.payload or "").strip()
        if not raw:
            return -0.05, "log_resolution requires non-empty payload"
        try:
            obj = json.loads(raw) if raw.startswith("{") else {"text": raw}
            if not isinstance(obj, dict):
                return -0.15, "log_resolution payload must be a JSON object or plain string"
        except json.JSONDecodeError as e:
            return -0.15, f"log_resolution invalid JSON: {e}"

        # If conflict_id is missing, attach to the most recently logged conflict.
        if not obj.get("conflict_id"):
            conflicts = self.swd.get("conflicts_identified", []) or []
            if conflicts and isinstance(conflicts[-1], dict):
                last_id = conflicts[-1].get("id")
                if last_id:
                    obj["conflict_id"] = last_id
        obj.setdefault("turn", self.turn)

        return self._apply_patch_or_error(
            [{"op": "add", "path": "/conflict_resolutions/-", "value": obj}]
        )

    def _step_advance_phase(self, action: CorpAction) -> Tuple[float, Optional[str]]:
        phase = (action.payload or "").strip().lower()
        if phase not in VALID_PHASES:
            return -0.05, f"advance_phase payload must be one of {sorted(VALID_PHASES)}"
        old_phase = self.swd.get("phase")
        if phase == old_phase:
            return -0.02, f"already in phase {phase}"
        reward, err = self._apply_patch_or_error(
            [{"op": "replace", "path": "/phase", "value": phase}]
        )
        if err is None:
            reward += 0.1
        return reward, err

    def _step_query_swd(self, action: CorpAction) -> Tuple[Any, Optional[str]]:
        expr = action.payload.strip()
        if not expr:
            return None, "empty JSONPath expression"
        try:
            matches = [m.value for m in jsonpath_parse(expr).find(self.swd)]
            return matches, None
        except Exception as e:  # jsonpath parse errors
            return None, f"query_swd error: {e}"

    def _step_finalize(self, action: CorpAction) -> Tuple[float, bool, Optional[str]]:
        raw = action.payload.strip()
        if not raw:
            return -0.05, True, "finalize requires non-empty payload"

        final_val: Any
        try:
            if raw.startswith("{") or raw.startswith("["):
                final_val = json.loads(raw)
            else:
                final_val = raw
        except json.JSONDecodeError:
            final_val = raw

        self.swd["final_recommendation"] = final_val
        self.swd["swd_version"] = int(self.swd.get("swd_version", 0)) + 1
        self.episode_metadata["finalized"] = True

        verify_result = self.task.verifier(self.swd)
        terminal = compute_reward(
            self.swd,
            verify_result,
            self.episode_metadata,
            self.task.description,
        )
        ok, err = validate_swd_structure(self.swd)
        if not ok:
            terminal = max(0.0, terminal - 0.05)
            self._persist_episode_memory(verify_result, terminal)
            return terminal, True, f"finalize on structurally invalid SWD: {err}"

        self._persist_episode_memory(verify_result, terminal)
        return terminal, True, None

    def _persist_episode_memory(
        self, verify_result: Dict[str, bool], score: float
    ) -> None:
        """Write per-worker + master episode summaries to the memory store."""
        try:
            pass_rate = (
                sum(1 for v in verify_result.values() if v) / max(len(verify_result), 1)
            )
            milestones = self.swd.get("milestones", []) or []
            counts = {
                "total": len(milestones),
                "complete": sum(1 for m in milestones if m.get("status") == "complete"),
                "missed": sum(1 for m in milestones if m.get("status") == "missed"),
                "pending": sum(1 for m in milestones if m.get("status") == "pending"),
            }
            final_snip = self.swd.get("final_recommendation")
            if isinstance(final_snip, str) and len(final_snip) > 200:
                final_snip = final_snip[:200] + "..."

            append_master_episode(
                task_id=self.task.task_id,
                episode_id=self._episode_id,
                role=self.task.role,
                master_tier=getattr(self.task, "master_tier", "senior"),
                final_recommendation=final_snip,
                score=score,
                milestone_counts=counts,
                notes=f"verifier pass_rate={round(pass_rate, 3)}",
            )

            ar = self.swd.get("agent_reports", {}) or {}
            for slot in self.task.agent_slots:
                key = swd_report_key_for_family(slot.family)
                report = ar.get(key)
                if report is None:
                    continue
                summary = str(report)
                if len(summary) > 240:
                    summary = summary[:240] + "..."
                append_worker_episode(
                    task_id=self.task.task_id,
                    slot_id=slot.id,
                    episode_id=self._episode_id,
                    summary=summary,
                    verifier_pass_rate=pass_rate,
                    score=score,
                )
        except Exception:
            # Memory is best-effort and must never mask a real episode result.
            return

    def _update_milestone_status(self) -> List[str]:
        completed_now: List[str] = []
        for m in self.swd.get("milestones", []) or []:
            mid = m.get("id")
            if not mid or m.get("status") in ("complete", "missed"):
                continue
            if self.task.milestone_complete(self.swd, str(mid)):
                m["status"] = "complete"
                self.episode_metadata["turn_completed"][str(mid)] = self.turn
                completed_now.append(str(mid))
            elif self.turn > int(m.get("due_by_turn", 9999)):
                m["status"] = "missed"
        return completed_now

    def _all_milestones_missed(self) -> bool:
        ms = self.swd.get("milestones", []) or []
        if not ms:
            return False
        return all(m.get("status") == "missed" for m in ms)


# Silence unused import warnings from lints that don't see through reward / agent.
_ = AgentSlot
