"""M1 — Cross-department budget reallocation (medium)."""

from __future__ import annotations

from typing import Any, Dict

from server.tasks.base import CorpTask
from server.verifiers import verify_m1


class M1BudgetReallocationTask(CorpTask):
    task_id = "m1_budget_reallocation"
    description = (
        "As CFO, engineering requests +40% infra budget while HR warns headcount is at "
        "risk if other lines are cut. Finance has a fixed envelope. Consult all three "
        "workers, log conflicts, resolve them, and finalize a phased plan (phase_1, "
        "phase_2) with budget rationale in decisions and a rich reasoning_log."
    )
    role = "Chief Financial Officer"
    available_agents = ["dev_agent", "hr_agent", "finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {
                    "id": "m1",
                    "label": "All three agent_reports populated",
                    "due_by_turn": 5,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m2",
                    "label": "At least one conflicts_identified (dev vs finance or hr vs finance)",
                    "due_by_turn": 10,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m3",
                    "label": "conflict_resolutions referencing a conflict id",
                    "due_by_turn": 14,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m4",
                    "label": "final_recommendation dict includes phase_1 and phase_2",
                    "due_by_turn": 18,
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
            return all(ar.get(a) is not None for a in ("dev", "hr", "finance"))
        if milestone_id == "m2":
            return len(swd.get("conflicts_identified", []) or []) >= 1
        if milestone_id == "m3":
            ids = {c.get("id") for c in (swd.get("conflicts_identified", []) or []) if isinstance(c, dict)}
            for r in swd.get("conflict_resolutions", []) or []:
                if isinstance(r, dict) and r.get("conflict_id") in ids:
                    return True
            return False
        if milestone_id == "m4":
            fr = swd.get("final_recommendation")
            return isinstance(fr, dict) and "phase_1" in fr and "phase_2" in fr
        return False
