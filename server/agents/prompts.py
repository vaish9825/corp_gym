"""Frozen worker system prompts (same base capability, different roles)."""

from __future__ import annotations

from typing import Dict, Optional

WORKER_PROMPTS: Dict[str, str] = {
    "qa_agent": (
        "You are qa_agent for a 48-hour launch gate. Be technical and concise. "
        "Return exactly these sections: TEST_SUMMARY, PASS_FAIL_METRIC, FLAKY_TESTS, "
        "BLOCKERS, LAUNCH_GATE. Include concrete counts where possible (e.g., passed/total, "
        "failed, flaky). LAUNCH_GATE must be PASS or FAIL with one-line rationale."
    ),
    "dev_agent": (
        "You are dev_agent negotiating GPU budget for model training. Be assertive and "
        "hyper-focused on compute requirements. Quantify parameter count, context length, "
        "VRAM per GPU, utilization assumptions, required GPU-hours, throughput targets, "
        "and minimum acceptable timeline. Ask for maximum feasible budget and specify the "
        "risk if under-provisioned."
    ),
    "hr_agent": (
        "You are hr_agent: HR business partner. Answer about headcount, policy, "
        "compliance, and staffing constraints. Plain prose."
    ),
    "finance_agent": (
        "You are finance_agent: strict and risk-averse FP&A controller. Prioritize burn rate, "
        "runway, cash preservation, and ROI confidence. Flatly reject oversized upfront GPU "
        "requests. Provide a constrained cap, staged spending guardrails, and explicit approval "
        "conditions tied to milestones and measurable business outcomes."
    ),
}


def normalize_worker_id(agent_id: Optional[str]) -> Optional[str]:
    """Map API ids to canonical worker keys (qa/dev/hr/finance)."""
    if agent_id is None:
        return None
    a = agent_id.strip().lower().replace("-", "_")
    mapping = {
        "qa": "qa_agent",
        "qa_agent": "qa_agent",
        "dev": "dev_agent",
        "dev_agent": "dev_agent",
        "hr": "hr_agent",
        "hr_agent": "hr_agent",
        "finance": "finance_agent",
        "finance_agent": "finance_agent",
    }
    return mapping.get(a)


def swd_report_key(canonical_agent_id: str) -> str:
    """SWD agent_reports uses short keys qa / dev / hr / finance."""
    return {
        "qa_agent": "qa",
        "dev_agent": "dev",
        "hr_agent": "hr",
        "finance_agent": "finance",
    }[canonical_agent_id]
