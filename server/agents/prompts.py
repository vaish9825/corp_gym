"""Worker id normalization helpers.

Worker personas now live in :mod:`server.agents.personas`. This module only
normalizes incoming ``agent_id`` strings from the master and resolves them to
SWD ``agent_reports`` keys via the current task's slot catalog.
"""

from __future__ import annotations

from typing import Optional

# Legacy aliases kept so prompts trained on the old id space still work.
# Maps legacy family-style ids to a current task slot id when possible.
LEGACY_ALIAS = {
    "qa": "qa_engineer",
    "qa_agent": "qa_engineer",
    "dev": "dev_lead",
    "dev_agent": "dev_lead",
    "hr": "chro",
    "hr_agent": "chro",
    "finance": "fpa_manager",
    "finance_agent": "fpa_manager",
}


def normalize_worker_id(agent_id: Optional[str]) -> Optional[str]:
    """Lowercase + underscore-normalize an ``agent_id`` from master output.

    Returns the normalized id, or a legacy alias if the input matches an older
    family-style name. Returns None only if the input is None/empty. Caller is
    responsible for checking membership against ``task.available_agents``.
    """
    if agent_id is None:
        return None
    a = agent_id.strip().lower().replace("-", "_")
    if not a:
        return None
    return LEGACY_ALIAS.get(a, a)


def swd_report_key_for_family(family: str) -> str:
    """Return the SWD ``agent_reports`` key for a worker family."""
    family = family.strip().lower()
    if family not in ("qa", "dev", "hr", "finance"):
        # Strategy and other new families still need a bucket; use the family
        # name directly and let the environment create the key on demand.
        return family
    return family
