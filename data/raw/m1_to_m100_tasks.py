"""100 generated M1-style tasks for RL environments."""

from __future__ import annotations
from typing import Any, Dict
from server.tasks.base import CorpTask

# Dummy verifier generator
def create_verifier(task_id):
    def verify(swd: Dict[str, Any]) -> Dict[str, bool]:
        return {"success": True}
    return verify

class M1ConflictTask(CorpTask):
    task_id = "m1_conflict_core"
    description = "(Dept: Core) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M2ConflictTask(CorpTask):
    task_id = "m2_conflict_core"
    description = "(Dept: Core) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M3ConflictTask(CorpTask):
    task_id = "m3_conflict_core"
    description = "(Dept: Core) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M4ConflictTask(CorpTask):
    task_id = "m4_conflict_core"
    description = "(Dept: Core) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M5ConflictTask(CorpTask):
    task_id = "m5_conflict_core"
    description = "(Dept: Core) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M6ConflictTask(CorpTask):
    task_id = "m6_conflict_core"
    description = "(Dept: Core) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M7ConflictTask(CorpTask):
    task_id = "m7_conflict_core"
    description = "(Dept: Core) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M8ConflictTask(CorpTask):
    task_id = "m8_conflict_core"
    description = "(Dept: Core) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M9ConflictTask(CorpTask):
    task_id = "m9_conflict_core"
    description = "(Dept: Core) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M10ConflictTask(CorpTask):
    task_id = "m10_conflict_core"
    description = "(Dept: Core) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M11ConflictTask(CorpTask):
    task_id = "m11_conflict_growth"
    description = "(Dept: Growth) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M12ConflictTask(CorpTask):
    task_id = "m12_conflict_growth"
    description = "(Dept: Growth) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M13ConflictTask(CorpTask):
    task_id = "m13_conflict_growth"
    description = "(Dept: Growth) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M14ConflictTask(CorpTask):
    task_id = "m14_conflict_growth"
    description = "(Dept: Growth) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M15ConflictTask(CorpTask):
    task_id = "m15_conflict_growth"
    description = "(Dept: Growth) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M16ConflictTask(CorpTask):
    task_id = "m16_conflict_growth"
    description = "(Dept: Growth) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M17ConflictTask(CorpTask):
    task_id = "m17_conflict_growth"
    description = "(Dept: Growth) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M18ConflictTask(CorpTask):
    task_id = "m18_conflict_growth"
    description = "(Dept: Growth) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M19ConflictTask(CorpTask):
    task_id = "m19_conflict_growth"
    description = "(Dept: Growth) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M20ConflictTask(CorpTask):
    task_id = "m20_conflict_growth"
    description = "(Dept: Growth) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M21ConflictTask(CorpTask):
    task_id = "m21_conflict_enterprise"
    description = "(Dept: Enterprise) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M22ConflictTask(CorpTask):
    task_id = "m22_conflict_enterprise"
    description = "(Dept: Enterprise) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M23ConflictTask(CorpTask):
    task_id = "m23_conflict_enterprise"
    description = "(Dept: Enterprise) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M24ConflictTask(CorpTask):
    task_id = "m24_conflict_enterprise"
    description = "(Dept: Enterprise) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M25ConflictTask(CorpTask):
    task_id = "m25_conflict_enterprise"
    description = "(Dept: Enterprise) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M26ConflictTask(CorpTask):
    task_id = "m26_conflict_enterprise"
    description = "(Dept: Enterprise) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M27ConflictTask(CorpTask):
    task_id = "m27_conflict_enterprise"
    description = "(Dept: Enterprise) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M28ConflictTask(CorpTask):
    task_id = "m28_conflict_enterprise"
    description = "(Dept: Enterprise) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M29ConflictTask(CorpTask):
    task_id = "m29_conflict_enterprise"
    description = "(Dept: Enterprise) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M30ConflictTask(CorpTask):
    task_id = "m30_conflict_enterprise"
    description = "(Dept: Enterprise) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M31ConflictTask(CorpTask):
    task_id = "m31_conflict_mobile"
    description = "(Dept: Mobile) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M32ConflictTask(CorpTask):
    task_id = "m32_conflict_mobile"
    description = "(Dept: Mobile) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M33ConflictTask(CorpTask):
    task_id = "m33_conflict_mobile"
    description = "(Dept: Mobile) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M34ConflictTask(CorpTask):
    task_id = "m34_conflict_mobile"
    description = "(Dept: Mobile) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M35ConflictTask(CorpTask):
    task_id = "m35_conflict_mobile"
    description = "(Dept: Mobile) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M36ConflictTask(CorpTask):
    task_id = "m36_conflict_mobile"
    description = "(Dept: Mobile) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M37ConflictTask(CorpTask):
    task_id = "m37_conflict_mobile"
    description = "(Dept: Mobile) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M38ConflictTask(CorpTask):
    task_id = "m38_conflict_mobile"
    description = "(Dept: Mobile) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M39ConflictTask(CorpTask):
    task_id = "m39_conflict_mobile"
    description = "(Dept: Mobile) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M40ConflictTask(CorpTask):
    task_id = "m40_conflict_mobile"
    description = "(Dept: Mobile) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M41ConflictTask(CorpTask):
    task_id = "m41_conflict_web"
    description = "(Dept: Web) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M42ConflictTask(CorpTask):
    task_id = "m42_conflict_web"
    description = "(Dept: Web) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M43ConflictTask(CorpTask):
    task_id = "m43_conflict_web"
    description = "(Dept: Web) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M44ConflictTask(CorpTask):
    task_id = "m44_conflict_web"
    description = "(Dept: Web) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M45ConflictTask(CorpTask):
    task_id = "m45_conflict_web"
    description = "(Dept: Web) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M46ConflictTask(CorpTask):
    task_id = "m46_conflict_web"
    description = "(Dept: Web) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M47ConflictTask(CorpTask):
    task_id = "m47_conflict_web"
    description = "(Dept: Web) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M48ConflictTask(CorpTask):
    task_id = "m48_conflict_web"
    description = "(Dept: Web) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M49ConflictTask(CorpTask):
    task_id = "m49_conflict_web"
    description = "(Dept: Web) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M50ConflictTask(CorpTask):
    task_id = "m50_conflict_web"
    description = "(Dept: Web) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M51ConflictTask(CorpTask):
    task_id = "m51_conflict_backend"
    description = "(Dept: Backend) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M52ConflictTask(CorpTask):
    task_id = "m52_conflict_backend"
    description = "(Dept: Backend) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M53ConflictTask(CorpTask):
    task_id = "m53_conflict_backend"
    description = "(Dept: Backend) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M54ConflictTask(CorpTask):
    task_id = "m54_conflict_backend"
    description = "(Dept: Backend) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M55ConflictTask(CorpTask):
    task_id = "m55_conflict_backend"
    description = "(Dept: Backend) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M56ConflictTask(CorpTask):
    task_id = "m56_conflict_backend"
    description = "(Dept: Backend) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M57ConflictTask(CorpTask):
    task_id = "m57_conflict_backend"
    description = "(Dept: Backend) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M58ConflictTask(CorpTask):
    task_id = "m58_conflict_backend"
    description = "(Dept: Backend) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M59ConflictTask(CorpTask):
    task_id = "m59_conflict_backend"
    description = "(Dept: Backend) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M60ConflictTask(CorpTask):
    task_id = "m60_conflict_backend"
    description = "(Dept: Backend) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M61ConflictTask(CorpTask):
    task_id = "m61_conflict_ai"
    description = "(Dept: AI) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M62ConflictTask(CorpTask):
    task_id = "m62_conflict_ai"
    description = "(Dept: AI) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M63ConflictTask(CorpTask):
    task_id = "m63_conflict_ai"
    description = "(Dept: AI) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M64ConflictTask(CorpTask):
    task_id = "m64_conflict_ai"
    description = "(Dept: AI) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M65ConflictTask(CorpTask):
    task_id = "m65_conflict_ai"
    description = "(Dept: AI) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M66ConflictTask(CorpTask):
    task_id = "m66_conflict_ai"
    description = "(Dept: AI) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M67ConflictTask(CorpTask):
    task_id = "m67_conflict_ai"
    description = "(Dept: AI) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M68ConflictTask(CorpTask):
    task_id = "m68_conflict_ai"
    description = "(Dept: AI) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M69ConflictTask(CorpTask):
    task_id = "m69_conflict_ai"
    description = "(Dept: AI) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M70ConflictTask(CorpTask):
    task_id = "m70_conflict_ai"
    description = "(Dept: AI) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M71ConflictTask(CorpTask):
    task_id = "m71_conflict_infrastructure"
    description = "(Dept: Infrastructure) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M72ConflictTask(CorpTask):
    task_id = "m72_conflict_infrastructure"
    description = "(Dept: Infrastructure) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M73ConflictTask(CorpTask):
    task_id = "m73_conflict_infrastructure"
    description = "(Dept: Infrastructure) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M74ConflictTask(CorpTask):
    task_id = "m74_conflict_infrastructure"
    description = "(Dept: Infrastructure) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M75ConflictTask(CorpTask):
    task_id = "m75_conflict_infrastructure"
    description = "(Dept: Infrastructure) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M76ConflictTask(CorpTask):
    task_id = "m76_conflict_infrastructure"
    description = "(Dept: Infrastructure) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M77ConflictTask(CorpTask):
    task_id = "m77_conflict_infrastructure"
    description = "(Dept: Infrastructure) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M78ConflictTask(CorpTask):
    task_id = "m78_conflict_infrastructure"
    description = "(Dept: Infrastructure) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M79ConflictTask(CorpTask):
    task_id = "m79_conflict_infrastructure"
    description = "(Dept: Infrastructure) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M80ConflictTask(CorpTask):
    task_id = "m80_conflict_infrastructure"
    description = "(Dept: Infrastructure) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M81ConflictTask(CorpTask):
    task_id = "m81_conflict_global"
    description = "(Dept: Global) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M82ConflictTask(CorpTask):
    task_id = "m82_conflict_global"
    description = "(Dept: Global) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M83ConflictTask(CorpTask):
    task_id = "m83_conflict_global"
    description = "(Dept: Global) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M84ConflictTask(CorpTask):
    task_id = "m84_conflict_global"
    description = "(Dept: Global) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M85ConflictTask(CorpTask):
    task_id = "m85_conflict_global"
    description = "(Dept: Global) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M86ConflictTask(CorpTask):
    task_id = "m86_conflict_global"
    description = "(Dept: Global) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M87ConflictTask(CorpTask):
    task_id = "m87_conflict_global"
    description = "(Dept: Global) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M88ConflictTask(CorpTask):
    task_id = "m88_conflict_global"
    description = "(Dept: Global) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M89ConflictTask(CorpTask):
    task_id = "m89_conflict_global"
    description = "(Dept: Global) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M90ConflictTask(CorpTask):
    task_id = "m90_conflict_global"
    description = "(Dept: Global) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

class M91ConflictTask(CorpTask):
    task_id = "m91_conflict_regional"
    description = "(Dept: Regional) As Director of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and finance_agent, log one explicit (dev requirement vs finance constraint) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Engineering"
    available_agents = ["dev_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (dev requirement vs finance constraint)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

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

class M92ConflictTask(CorpTask):
    task_id = "m92_conflict_regional"
    description = "(Dept: Regional) As VP of Product, you need to manage a cross-functional initiative. Consult dev_agent and marketing_agent, log one explicit (feature timeline vs marketing launch window) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Product"
    available_agents = ["dev_agent", "marketing_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and marketing agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (feature timeline vs marketing launch window)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "marketing": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "marketing"))
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

class M93ConflictTask(CorpTask):
    task_id = "m93_conflict_regional"
    description = "(Dept: Regional) As Head of HR, you need to manage a cross-functional initiative. Consult hr_agent and finance_agent, log one explicit (hiring need vs budget freeze) conflict, resolve it, and submit a phased recommendation."
    role = "Head of HR"
    available_agents = ["hr_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "hr and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (hiring need vs budget freeze)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("hr", "finance"))
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

class M94ConflictTask(CorpTask):
    task_id = "m94_conflict_regional"
    description = "(Dept: Regional) As Chief Security Officer, you need to manage a cross-functional initiative. Consult dev_agent and ops_agent, log one explicit (security rollout vs system uptime) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Security Officer"
    available_agents = ["dev_agent", "ops_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and ops agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (security rollout vs system uptime)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "ops": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "ops"))
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

class M95ConflictTask(CorpTask):
    task_id = "m95_conflict_regional"
    description = "(Dept: Regional) As VP of Sales, you need to manage a cross-functional initiative. Consult sales_agent and legal_agent, log one explicit (deal closure vs compliance review) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Sales"
    available_agents = ["sales_agent", "legal_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and legal agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (deal closure vs compliance review)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "legal": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "legal"))
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

class M96ConflictTask(CorpTask):
    task_id = "m96_conflict_regional"
    description = "(Dept: Regional) As Chief Marketing Officer, you need to manage a cross-functional initiative. Consult marketing_agent and finance_agent, log one explicit (ad spend vs ROI target) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Marketing Officer"
    available_agents = ["marketing_agent", "finance_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "marketing and finance agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (ad spend vs ROI target)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"marketing": None, "finance": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("marketing", "finance"))
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

class M97ConflictTask(CorpTask):
    task_id = "m97_conflict_regional"
    description = "(Dept: Regional) As Head of Data, you need to manage a cross-functional initiative. Consult data_agent and dev_agent, log one explicit (data processing vs storage limit) conflict, resolve it, and submit a phased recommendation."
    role = "Head of Data"
    available_agents = ["data_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "data and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (data processing vs storage limit)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("data", "dev"))
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

class M98ConflictTask(CorpTask):
    task_id = "m98_conflict_regional"
    description = "(Dept: Regional) As Director of Ops, you need to manage a cross-functional initiative. Consult ops_agent and hr_agent, log one explicit (office expansion vs remote policy) conflict, resolve it, and submit a phased recommendation."
    role = "Director of Ops"
    available_agents = ["ops_agent", "hr_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "ops and hr agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (office expansion vs remote policy)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops": None, "hr": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("ops", "hr"))
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

class M99ConflictTask(CorpTask):
    task_id = "m99_conflict_regional"
    description = "(Dept: Regional) As VP of Engineering, you need to manage a cross-functional initiative. Consult dev_agent and qa_agent, log one explicit (urgent release vs testing coverage) conflict, resolve it, and submit a phased recommendation."
    role = "VP of Engineering"
    available_agents = ["dev_agent", "qa_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "dev and qa agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (urgent release vs testing coverage)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev": None, "qa": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("dev", "qa"))
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

class M100ConflictTask(CorpTask):
    task_id = "m100_conflict_regional"
    description = "(Dept: Regional) As Chief Strategy Officer, you need to manage a cross-functional initiative. Consult sales_agent and dev_agent, log one explicit (custom feature vs roadmap priority) conflict, resolve it, and submit a phased recommendation."
    role = "Chief Strategy Officer"
    available_agents = ["sales_agent", "dev_agent"]
    token_budget = 12288

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "sales and dev agent_reports populated", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Exactly one conflict identified (custom feature vs roadmap priority)", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
                {"id": "m3", "label": "Conflict resolved and logged in conflict_resolutions", "due_by_turn": 16, "status": "pending", "owner": "master", "output": None},
                {"id": "m4", "label": "Phased recommendation submitted", "due_by_turn": 20, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"sales": None, "dev": None},
            "decisions": [],
            "conflicts_identified": [],
            "conflict_resolutions": [],
            "reasoning_log": [],
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        ar = swd.get("agent_reports", {})
        if milestone_id == "m1":
            return all(ar.get(a) is not None for a in ("sales", "dev"))
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

