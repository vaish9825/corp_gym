"""E1 — Product launch readiness (easy)."""

from __future__ import annotations

from typing import Any, Dict

from server.tasks.base import CorpTask
from server.verifiers import verify_e1


class E1LaunchReadinessTask(CorpTask):
    task_id = "e1_launch_readiness"
    description = (
        "As PM, a new feature is scheduled to launch in 48h. Verify readiness using "
        "dev_agent and hr_agent. Maintain the SWD: delegate for specialist input, "
        "log decisions, then finalize with GO or NO_GO plus documented rationale."
    )
    role = "Product Manager"
    available_agents = ["dev_agent", "hr_agent"]
    token_budget = 4096

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {
                    "id": "m1",
                    "label": "Dev readiness captured in agent_reports.dev",
                    "due_by_turn": 4,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m2",
                    "label": "HR staffing sign-off in agent_reports.hr",
                    "due_by_turn": 7,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m3",
                    "label": "final_recommendation GO/NO_GO with rationale",
                    "due_by_turn": 10,
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
        return verify_e1(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return ar.get("dev") is not None
        if milestone_id == "m2":
            return ar.get("hr") is not None
        if milestone_id == "m3":
            fr = swd.get("final_recommendation")
            return fr is not None and fr in ("GO", "NO_GO")
        return False
