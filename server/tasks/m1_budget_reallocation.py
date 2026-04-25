"""M1 - Cross-department budget reallocation (medium, senior master tier)."""

from __future__ import annotations

from typing import Any, Dict

from server.agents.personas import AgentSlot
from server.tasks.base import CorpTask
from server.verifiers import verify_m1


class M1BudgetReallocationTask(CorpTask):
    task_id = "m1_budget_reallocation"
    description = (
        "As Director of Engineering, you need to buy GPU cluster time for "
        "model training under strict finance constraints. Consult both the "
        "dev_lead and the fpa_manager, log one explicit requirement-vs-budget "
        "conflict and its resolution, and submit a phased recommendation "
        "(at minimum phase_1 details)."
    )
    role = "Director of Engineering"
    difficulty = "medium"
    master_tier = "senior"
    agent_slots = [
        AgentSlot(id="dev_lead", family="dev", tier="senior", title="Senior Engineering Lead"),
        AgentSlot(id="fpa_manager", family="finance", tier="senior", title="FP&A Manager"),
    ]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {
                    "id": "m1",
                    "label": "dev and finance agent_reports populated",
                    "due_by_turn": 8,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m2",
                    "label": "One conflict logged and resolved (conflicts_identified + conflict_resolutions)",
                    "due_by_turn": 16,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m3",
                    "label": "Phased recommendation submitted (at least phase_1)",
                    "due_by_turn": 22,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
            ],
            "agent_reports": {"dev": None, "hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return verify_m1(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "finance"))
        if milestone_id == "m2":
            conflicts = swd.get("conflicts_identified", []) or []
            resolutions = swd.get("conflict_resolutions", []) or []
            if not conflicts or not resolutions:
                return False
            ids = {c.get("id") for c in conflicts if isinstance(c, dict)}
            for r in resolutions:
                if isinstance(r, dict) and (
                    r.get("conflict_id") in ids or not r.get("conflict_id")
                ):
                    return True
            return False
        if milestone_id == "m3":
            fr = swd.get("final_recommendation")
            return isinstance(fr, dict) and "phase_1" in fr
        return False
