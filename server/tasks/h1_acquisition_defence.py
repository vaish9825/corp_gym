"""H1 - Hostile acquisition defence (hard, executive master tier)."""

from __future__ import annotations

from typing import Any, Dict

from server.agents.personas import AgentSlot
from server.tasks.base import CorpTask
from server.verifiers import verify_h1


class H1AcquisitionDefenceTask(CorpTask):
    task_id = "h1_acquisition_defence"
    description = (
        "As CEO, a competitor offers 2.3x valuation. Reconcile contradictory "
        "advisor views from the CTO, CFO, and CHRO into a single strategy: "
        "counter_offer, deadline, and retention_plan. Advance phase through "
        "execution, log multiple conflicts with typed resolutions, and "
        "maintain a dense reasoning_log across turns."
    )
    role = "Chief Executive Officer"
    difficulty = "hard"
    master_tier = "executive"
    agent_slots = [
        AgentSlot(id="cto", family="dev", tier="executive", title="Chief Technology Officer"),
        AgentSlot(id="cfo", family="finance", tier="executive", title="Chief Financial Officer"),
        AgentSlot(id="chro", family="hr", tier="executive", title="Chief People Officer"),
    ]
    token_budget = 16384

    def __init__(self) -> None:
        super().__init__()
        # Keyed by slot id so the environment can inject confidential intel
        # directly based on who the master is calling.
        self.intel_injections = {
            "cto": (
                "CONFIDENTIAL: Our stack is ~18 months ahead; acquirer cannot replicate quickly - "
                "strategic ask should be ~3.5x with extended IP lock-up."
            ),
            "cfo": (
                "CONFIDENTIAL: Cash runway ~7 months at current burn; board unlikely to approve "
                "3.5x ask - realistic ceiling ~2.6x without new financing."
            ),
            "chro": (
                "CONFIDENTIAL: Key engineering talent has competing offers; ~60% retention risk "
                "if the process drags beyond 90 days without retention incentives."
            ),
        }

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {
                    "id": "m1",
                    "label": "All three agent_reports present (dev, finance, hr)",
                    "due_by_turn": 6,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m2",
                    "label": ">=2 conflicts_identified referencing advisors",
                    "due_by_turn": 10,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m3",
                    "label": "conflict_resolutions entry includes resolution_type",
                    "due_by_turn": 15,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m4",
                    "label": "final_recommendation has counter_offer, deadline, retention_plan",
                    "due_by_turn": 20,
                    "status": "pending",
                    "owner": "master",
                    "output": None,
                },
                {
                    "id": "m5",
                    "label": "reasoning_log >=5 entries with distinct turn values",
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
        return verify_h1(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) for a in ("dev", "hr", "finance"))
        if milestone_id == "m2":
            conflicts = swd.get("conflicts_identified", []) or []
            if len(conflicts) < 2:
                return False
            ok = 0
            for c in conflicts:
                if not isinstance(c, dict):
                    continue
                txt = str(c).lower()
                if any(x in txt for x in ("dev", "cto", "hr", "chro", "finance", "cfo")):
                    ok += 1
            return ok >= 2
        if milestone_id == "m3":
            for r in swd.get("conflict_resolutions", []) or []:
                if isinstance(r, dict) and "resolution_type" in r:
                    return True
            return False
        if milestone_id == "m4":
            fr = swd.get("final_recommendation")
            if not isinstance(fr, dict):
                return False
            return (
                "counter_offer" in fr and "deadline" in fr and "retention_plan" in fr
            )
        if milestone_id == "m5":
            turns = []
            for e in swd.get("reasoning_log", []) or []:
                if isinstance(e, dict) and "turn" in e:
                    turns.append(e["turn"])
            return len(set(turns)) >= 5
        return False
