"""M1 — Cross-department budget reallocation (medium)."""

from __future__ import annotations

from typing import Any, Dict

from server.tasks.base import CorpTask
from server.verifiers import verify_m1


class M1BudgetReallocationTask(CorpTask):
    task_id = "m1_budget_reallocation"
    description = (
        "As Director of Engineering, you need to buy GPU cluster time for model "
        "training under strict finance constraints. Consult dev_agent and "
        "finance_agent, log one explicit requirement-vs-budget conflict, resolve it, "
        "and submit a phased recommendation."
    )
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
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
                    "due_by_turn": 6,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m2",
                    "label": "Exactly one conflict identified (dev requirement vs finance constraint)",
                    "due_by_turn": 12,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m3",
                    "label": "Conflict resolved and logged in conflict_resolutions",
                    "due_by_turn": 16,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m4",
                    "label": "Phased recommendation submitted",
                    "due_by_turn": 20,
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
            return len(swd.get("conflicts_identified", []) or []) == 1
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
