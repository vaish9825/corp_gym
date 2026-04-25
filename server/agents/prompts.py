"""Frozen worker system prompts (same base capability, different roles)."""

from __future__ import annotations

from typing import Dict, Optional

WORKER_PROMPTS: Dict[str, str] = {
    "dev_agent": (
        "You are dev_agent: senior engineering lead. Answer concisely about technical "
        "feasibility, timelines, integration risks, and mitigation. Output plain prose, "
        "no JSON unless asked."
    ),
    "hr_agent": (
        "You are hr_agent: HR business partner. Answer about headcount, policy, "
        "compliance, and staffing constraints. Plain prose."
    ),
    "finance_agent": (
        "You are finance_agent: FP&A lead. Answer about budget, ROI, runway, and "
        "cost envelopes. Plain prose."
    ),
}


def normalize_worker_id(agent_id: Optional[str]) -> Optional[str]:
    """Map API ids to canonical worker keys (dev_agent, hr_agent, finance_agent)."""
    if agent_id is None:
        return None
    a = agent_id.strip().lower().replace("-", "_")
    mapping = {
        "dev": "dev_agent",
        "dev_agent": "dev_agent",
        "hr": "hr_agent",
        "hr_agent": "hr_agent",
        "finance": "finance_agent",
        "finance_agent": "finance_agent",
    }
    return mapping.get(a)


def swd_report_key(canonical_agent_id: str) -> str:
    """SWD agent_reports uses short keys dev / hr / finance."""
    return {
        "dev_agent": "dev",
        "hr_agent": "hr",
        "finance_agent": "finance",
    }[canonical_agent_id]
