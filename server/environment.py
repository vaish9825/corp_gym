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

from server.agents.prompts import normalize_worker_id, swd_report_key
from server.reward import compute_reward, compute_swd_coherence
from server.swd import new_episode_id, try_apply_json_patch
from server.tasks import TASKS
from server.tasks.base import CorpTask
from server.worker_client import call_worker_model

SAFETY_MAX_TURNS = 256


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
            version="0.1.0",
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

        if action.action_type == "delegate":
            step_reward, agent_last_output, error = self._step_delegate(action)
        elif action.action_type == "update_swd":
            step_reward, error = self._step_update_swd(action)
        elif action.action_type == "query_swd":
            query_result, error = self._step_query_swd(action)
        elif action.action_type == "finalize":
            step_reward, done, error = self._step_finalize(action)
        else:
            error = f"unknown action_type {action.action_type}"

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
            available_agents=list(self.task.available_agents),
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

    def _step_delegate(self, action: CorpAction) -> Tuple[float, Optional[str], Optional[str]]:
        reward = 0.0
        canonical = normalize_worker_id(action.agent_id)
        if canonical is None or canonical not in self.task.available_agents:
            reward -= 0.10
            self.episode_metadata["wrong_agent_count"] += 1
            return reward, None, "invalid or unavailable agent_id for this task"

        if canonical == self.episode_metadata.get("last_agent"):
            self.episode_metadata["consecutive_same_agent_calls"] += 1
        else:
            self.episode_metadata["consecutive_same_agent_calls"] = 0
        self.episode_metadata["last_agent"] = canonical

        task_text = action.payload.strip()
        if self.task.task_id == "h1_acquisition_defence":
            extra = self.task.intel_injections.get(canonical)
            if extra:
                task_text = f"{task_text}\n\n{extra}".strip()

        key = swd_report_key(canonical)
        existing = self.swd.get("agent_reports", {}).get(key)
        if existing is None:
            reward += 0.1
        else:
            reward -= 0.02

        if self.episode_metadata["consecutive_same_agent_calls"] > 1:
            reward -= 0.05 * self.episode_metadata["consecutive_same_agent_calls"]

        out = call_worker_model(canonical, task_text or "Provide your assessment.")
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
        return terminal, True, None

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
