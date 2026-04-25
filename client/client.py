"""WebSocket EnvClient for CORP-ENV."""

from __future__ import annotations

from typing import Any, Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from corp_env.models import CorpAction, CorpObservation


class CorpEnvClient(EnvClient[CorpAction, CorpObservation, State]):
    """Client for a running corp-env server (persistent WebSocket session)."""

    def _step_payload(self, action: CorpAction) -> Dict[str, Any]:
        return action.model_dump(mode="json", exclude_none=True)

    def _parse_result(self, payload: Dict[str, Any]) -> StepResult[CorpObservation]:
        obs_data = dict(payload.get("observation", {}))
        meta = obs_data.pop("metadata", {}) or {}
        observation = CorpObservation(
            **obs_data,
            reward=payload.get("reward"),
            done=bool(payload.get("done", False)),
            metadata=meta,
        )
        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=bool(payload.get("done", False)),
        )

    def _parse_state(self, payload: Dict[str, Any]) -> State:
        return State(
            episode_id=payload.get("episode_id"),
            step_count=int(payload.get("step_count", 0)),
        )
