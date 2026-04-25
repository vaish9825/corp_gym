"""E1 - Product launch readiness (easy, fresher master tier)."""

from __future__ import annotations

from typing import Any, Dict

from server.agents.personas import AgentSlot
from server.tasks.base import CorpTask
from server.verifiers import verify_e1


class E1LaunchReadinessTask(CorpTask):
    task_id = "e1_launch_readiness"
    description = (
        "As Associate Product Manager, a small feature is launching in 48 "
        "hours. Consult the qa_engineer once to get the current test status, "
        "log one short reasoning note, then finalize with GO or NO_GO."
    )
    role = "Associate Product Manager"
    difficulty = "easy"
    master_tier = "fresher"
    agent_slots = [
        AgentSlot(id="qa_engineer", family="qa", tier="fresher", title="QA Engineer I"),
    ]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {
                    "id": "m1",
                    "label": "Consult qa_engineer (agent_reports.qa filled)",
                    "due_by_turn": 6,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m2",
                    "label": "final_recommendation = GO or NO_GO",
                    "due_by_turn": 12,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
            ],
            "agent_reports": {"qa": None, "dev": None, "hr": None, "finance": None},
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
            return ar.get("qa") is not None
        if milestone_id == "m2":
            fr = swd.get("final_recommendation")
            if not isinstance(fr, str):
                return False
            return fr.strip().upper().replace("-", "_") in ("GO", "NO_GO")
        return False
