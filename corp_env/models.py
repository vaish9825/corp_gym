"""Pydantic action and observation types for CORP-ENV."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class CorpAction(Action):
    """Structured corporate environment action."""

    action_type: Literal["delegate", "update_swd", "query_swd", "finalize"] = Field(
        ...,
        description="delegate | update_swd (RFC 6902 JSON array) | query_swd | finalize",
    )
    agent_id: Optional[str] = Field(
        default=None,
        description="Worker id for delegate: dev_agent, hr_agent, or finance_agent",
    )
    payload: str = Field(
        default="",
        description="Task text, JSON Patch string, JSONPath expression, or final recommendation (string or JSON)",
    )


class CorpObservation(Observation):
    """Observation including the Shared Workspace Document (SWD)."""

    task_description: str = Field(default="", description="Scenario instructions")
    role: str = Field(default="", description="Role the master agent plays (e.g. PM, CFO)")
    available_agents: List[str] = Field(
        default_factory=list,
        description="Worker agents available for this task",
    )
    swd: Dict[str, Any] = Field(default_factory=dict, description="Shared Workspace Document")
    agent_last_output: Optional[str] = Field(
        default=None,
        description="Text returned by the last delegate() call, if any",
    )
    query_result: Optional[Any] = Field(
        default=None,
        description="Result of query_swd when action_type was query_swd",
    )
    tokens_used: int = Field(default=0, ge=0)
    token_budget: int = Field(default=4096, ge=0)
    turn: int = Field(default=0, ge=0)
    error: Optional[str] = Field(default=None, description="Last validation or runtime error")
