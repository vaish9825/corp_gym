"""Per-task deterministic verification (from CORP-ENV implementation guide)."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Set


def _ngrams(text: str, n: int) -> List[str]:
    words = text.split()
    if len(words) < n:
        return []
    return [" ".join(words[i : i + n]) for i in range(len(words) - n + 1)]


def check_no_verbatim_copy(swd: Dict[str, Any]) -> bool:
    """Penalise if final_recommendation is mostly copy-paste from one agent report."""
    final = swd.get("final_recommendation")
    if final is None:
        return True
    final_str = str(final).lower()
    reports = swd.get("agent_reports") or {}
    for report in reports.values():
        if report and len(str(report)) > 50:
            report_grams = set(_ngrams(str(report).lower(), 5))
            final_grams = set(_ngrams(final_str, 5))
            if report_grams and final_grams:
                overlap = len(final_grams & report_grams) / min(
                    len(report_grams), len(final_grams)
                )
                if overlap > 0.6:
                    return False
    return True


def is_verbatim_copy(swd: Dict[str, Any]) -> bool:
    """Return True when final_recommendation appears to copy a worker report."""
    return not check_no_verbatim_copy(swd)


def verify_e1(swd: Dict[str, Any]) -> Dict[str, bool]:
    fr = swd.get("final_recommendation")
    fr_norm = (
        fr.strip().upper().replace("-", "_") if isinstance(fr, str) else ""
    )
    checks = {
        "qa_report_present": swd.get("agent_reports", {}).get("qa") is not None,
        "final_rec_valid": fr_norm in ("GO", "NO_GO"),
        "no_missed_milestones": all(
            m.get("status") != "missed" for m in (swd.get("milestones") or [])
        ),
    }
    return checks


_BUDGET_TERMS = ("budget", "cost", "spend", "cash", "runway", "burn")


def _text_of(entry: Any) -> str:
    if isinstance(entry, dict):
        return " ".join(str(v) for v in entry.values())
    return str(entry)


def verify_m1(swd: Dict[str, Any]) -> Dict[str, bool]:
    final = swd.get("final_recommendation") or {}
    if not isinstance(final, dict):
        final = {}
    decisions = swd.get("decisions", []) or []
    reasoning = swd.get("reasoning_log", []) or []
    budget_corpus = " ".join(
        _text_of(x).lower() for x in list(decisions) + list(reasoning)
    )
    checks = {
        "required_agents_consulted": all(
            swd.get("agent_reports", {}).get(a) is not None for a in ("dev", "finance")
        ),
        "conflict_logged": len(swd.get("conflicts_identified", []) or []) >= 1,
        "conflict_resolved": len(swd.get("conflict_resolutions", []) or []) >= 1,
        "phased_plan": "phase_1" in final,
        "budget_constraint_acknowledged": any(
            term in budget_corpus for term in _BUDGET_TERMS
        ),
        "reasoning_documented": len(reasoning) >= 1,
    }
    return checks


def verify_h1(swd: Dict[str, Any]) -> Dict[str, bool]:
    final = swd.get("final_recommendation") or {}
    if not isinstance(final, dict):
        final = {}
    resolutions = swd.get("conflict_resolutions", []) or []

    checks = {
        "all_agents_consulted": all(
            swd.get("agent_reports", {}).get(a) for a in ("dev", "hr", "finance")
        ),
        "multi_conflict_logged": len(swd.get("conflicts_identified", []) or []) >= 2,
        "conflict_explicitly_resolved": len(resolutions) >= 1,
        "resolution_has_type": any(
            isinstance(r, dict) and "resolution_type" in r for r in resolutions
        ),
        "rich_reasoning_log": len(swd.get("reasoning_log", []) or []) >= 5,
        "counter_offer_present": "counter_offer" in final,
        "deadline_present": "deadline" in final,
        "retention_addressed": "retention_plan" in final,
        "timeline_constraint_acknowledged": any(
            re.search(r"(7 month|runway|cash)", str(d), re.I)
            for d in (swd.get("decisions", []) or [])
        ),
        "no_single_agent_copied": check_no_verbatim_copy(swd),
        "all_phases_reached": swd.get("phase") == "execution",
        "swd_version_rich": int(swd.get("swd_version", 0)) >= 8,
    }
    return checks
