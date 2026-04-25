"""Pydantic action and observation types for CORP-ENV."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from openenv.core.env_server.types import Action, Observation
from pydantic import Field


class CorpAction(Action):
    """Structured corporate environment action."""

    action_type: Literal[
        "delegate",
        "update_swd",
        "query_swd",
        "finalize",
        "log_reasoning",
        "log_conflict",
        "log_resolution",
        "log_decision",
        "advance_phase",
    ] = Field(
        ...,
        description=(
            "delegate | update_swd (RFC 6902 JSON array as string) | query_swd | "
            "finalize | log_reasoning | log_conflict | log_resolution | "
            "log_decision | advance_phase"
        ),
    )
    agent_id: Optional[str] = Field(
        default=None,
        description=(
            "Worker slot id for delegate (per-task; e.g. qa_engineer, dev_lead, "
            "fpa_manager, cto, cfo, chro)."
        ),
    )
    payload: str = Field(
        default="",
        description=(
            "Depending on action_type: plain task text (delegate), JSON Patch "
            "string (update_swd), JSONPath (query_swd), final recommendation "
            "(finalize), plain text (log_reasoning/log_decision), JSON object "
            "string (log_conflict/log_resolution), or phase name "
            "(advance_phase)."
        ),
    )


class CorpObservation(Observation):
    """Observation including the Shared Workspace Document (SWD)."""

    task_description: str = Field(default="", description="Scenario instructions")
    role: str = Field(default="", description="Role the master agent plays (e.g. PM, CFO)")
    master_tier: str = Field(
        default="senior",
        description="Master persona tier for this task (fresher | senior | executive)",
    )
    available_agents: List[str] = Field(
        default_factory=list,
        description="Worker slot ids available for this task",
    )
    available_actions: List[str] = Field(
        default_factory=list,
        description="One-line syntax hints for every legal action_type",
    )
    next_step_hint: Optional[str] = Field(
        default=None,
        description="Heuristic hint computed from the next pending milestone",
    )
    recent_actions: List[str] = Field(
        default_factory=list,
        description="Summaries of the last few master actions (most recent last)",
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
