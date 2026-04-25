"""100 generated tasks for RL environments."""

from __future__ import annotations
from typing import Any, Dict
from server.tasks.base import CorpTask

# Dummy verifier generator
def create_verifier(task_id):
    def verify(swd: Dict[str, Any]) -> Dict[str, bool]:
        return {"success": True}
    return verify

class E1LaunchReadinessTask(CorpTask):
    task_id = "e1_launch_readiness_core"
    description = "(Core Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E2BugTriageTask(CorpTask):
    task_id = "e2_bug_triage_core"
    description = "(Core Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E3RegressionTestingTask(CorpTask):
    task_id = "e3_regression_testing_core"
    description = "(Core Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E4ModelEvaluationTask(CorpTask):
    task_id = "e4_model_evaluation_core"
    description = "(Core Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E5QuarterlyHiringTask(CorpTask):
    task_id = "e5_quarterly_hiring_core"
    description = "(Core Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E6CampaignLaunchTask(CorpTask):
    task_id = "e6_campaign_launch_core"
    description = "(Core Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E7DatabaseMigrationTask(CorpTask):
    task_id = "e7_database_migration_core"
    description = "(Core Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E8SecurityAuditTask(CorpTask):
    task_id = "e8_security_audit_core"
    description = "(Core Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E9ExpenseReconciliationTask(CorpTask):
    task_id = "e9_expense_reconciliation_core"
    description = "(Core Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E10OfficeRelocationTask(CorpTask):
    task_id = "e10_office_relocation_core"
    description = "(Core Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E11LaunchReadinessTask(CorpTask):
    task_id = "e11_launch_readiness_growth"
    description = "(Growth Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E12BugTriageTask(CorpTask):
    task_id = "e12_bug_triage_growth"
    description = "(Growth Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E13RegressionTestingTask(CorpTask):
    task_id = "e13_regression_testing_growth"
    description = "(Growth Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E14ModelEvaluationTask(CorpTask):
    task_id = "e14_model_evaluation_growth"
    description = "(Growth Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E15QuarterlyHiringTask(CorpTask):
    task_id = "e15_quarterly_hiring_growth"
    description = "(Growth Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E16CampaignLaunchTask(CorpTask):
    task_id = "e16_campaign_launch_growth"
    description = "(Growth Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E17DatabaseMigrationTask(CorpTask):
    task_id = "e17_database_migration_growth"
    description = "(Growth Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E18SecurityAuditTask(CorpTask):
    task_id = "e18_security_audit_growth"
    description = "(Growth Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E19ExpenseReconciliationTask(CorpTask):
    task_id = "e19_expense_reconciliation_growth"
    description = "(Growth Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E20OfficeRelocationTask(CorpTask):
    task_id = "e20_office_relocation_growth"
    description = "(Growth Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E21LaunchReadinessTask(CorpTask):
    task_id = "e21_launch_readiness_enterprise"
    description = "(Enterprise Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E22BugTriageTask(CorpTask):
    task_id = "e22_bug_triage_enterprise"
    description = "(Enterprise Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E23RegressionTestingTask(CorpTask):
    task_id = "e23_regression_testing_enterprise"
    description = "(Enterprise Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E24ModelEvaluationTask(CorpTask):
    task_id = "e24_model_evaluation_enterprise"
    description = "(Enterprise Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E25QuarterlyHiringTask(CorpTask):
    task_id = "e25_quarterly_hiring_enterprise"
    description = "(Enterprise Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E26CampaignLaunchTask(CorpTask):
    task_id = "e26_campaign_launch_enterprise"
    description = "(Enterprise Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E27DatabaseMigrationTask(CorpTask):
    task_id = "e27_database_migration_enterprise"
    description = "(Enterprise Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E28SecurityAuditTask(CorpTask):
    task_id = "e28_security_audit_enterprise"
    description = "(Enterprise Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E29ExpenseReconciliationTask(CorpTask):
    task_id = "e29_expense_reconciliation_enterprise"
    description = "(Enterprise Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E30OfficeRelocationTask(CorpTask):
    task_id = "e30_office_relocation_enterprise"
    description = "(Enterprise Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E31LaunchReadinessTask(CorpTask):
    task_id = "e31_launch_readiness_mobile"
    description = "(Mobile Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E32BugTriageTask(CorpTask):
    task_id = "e32_bug_triage_mobile"
    description = "(Mobile Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E33RegressionTestingTask(CorpTask):
    task_id = "e33_regression_testing_mobile"
    description = "(Mobile Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E34ModelEvaluationTask(CorpTask):
    task_id = "e34_model_evaluation_mobile"
    description = "(Mobile Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E35QuarterlyHiringTask(CorpTask):
    task_id = "e35_quarterly_hiring_mobile"
    description = "(Mobile Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E36CampaignLaunchTask(CorpTask):
    task_id = "e36_campaign_launch_mobile"
    description = "(Mobile Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E37DatabaseMigrationTask(CorpTask):
    task_id = "e37_database_migration_mobile"
    description = "(Mobile Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E38SecurityAuditTask(CorpTask):
    task_id = "e38_security_audit_mobile"
    description = "(Mobile Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E39ExpenseReconciliationTask(CorpTask):
    task_id = "e39_expense_reconciliation_mobile"
    description = "(Mobile Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E40OfficeRelocationTask(CorpTask):
    task_id = "e40_office_relocation_mobile"
    description = "(Mobile Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E41LaunchReadinessTask(CorpTask):
    task_id = "e41_launch_readiness_web"
    description = "(Web Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E42BugTriageTask(CorpTask):
    task_id = "e42_bug_triage_web"
    description = "(Web Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E43RegressionTestingTask(CorpTask):
    task_id = "e43_regression_testing_web"
    description = "(Web Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E44ModelEvaluationTask(CorpTask):
    task_id = "e44_model_evaluation_web"
    description = "(Web Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E45QuarterlyHiringTask(CorpTask):
    task_id = "e45_quarterly_hiring_web"
    description = "(Web Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E46CampaignLaunchTask(CorpTask):
    task_id = "e46_campaign_launch_web"
    description = "(Web Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E47DatabaseMigrationTask(CorpTask):
    task_id = "e47_database_migration_web"
    description = "(Web Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E48SecurityAuditTask(CorpTask):
    task_id = "e48_security_audit_web"
    description = "(Web Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E49ExpenseReconciliationTask(CorpTask):
    task_id = "e49_expense_reconciliation_web"
    description = "(Web Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E50OfficeRelocationTask(CorpTask):
    task_id = "e50_office_relocation_web"
    description = "(Web Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E51LaunchReadinessTask(CorpTask):
    task_id = "e51_launch_readiness_backend"
    description = "(Backend Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E52BugTriageTask(CorpTask):
    task_id = "e52_bug_triage_backend"
    description = "(Backend Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E53RegressionTestingTask(CorpTask):
    task_id = "e53_regression_testing_backend"
    description = "(Backend Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E54ModelEvaluationTask(CorpTask):
    task_id = "e54_model_evaluation_backend"
    description = "(Backend Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E55QuarterlyHiringTask(CorpTask):
    task_id = "e55_quarterly_hiring_backend"
    description = "(Backend Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E56CampaignLaunchTask(CorpTask):
    task_id = "e56_campaign_launch_backend"
    description = "(Backend Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E57DatabaseMigrationTask(CorpTask):
    task_id = "e57_database_migration_backend"
    description = "(Backend Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E58SecurityAuditTask(CorpTask):
    task_id = "e58_security_audit_backend"
    description = "(Backend Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E59ExpenseReconciliationTask(CorpTask):
    task_id = "e59_expense_reconciliation_backend"
    description = "(Backend Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E60OfficeRelocationTask(CorpTask):
    task_id = "e60_office_relocation_backend"
    description = "(Backend Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E61LaunchReadinessTask(CorpTask):
    task_id = "e61_launch_readiness_ai"
    description = "(AI Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E62BugTriageTask(CorpTask):
    task_id = "e62_bug_triage_ai"
    description = "(AI Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E63RegressionTestingTask(CorpTask):
    task_id = "e63_regression_testing_ai"
    description = "(AI Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E64ModelEvaluationTask(CorpTask):
    task_id = "e64_model_evaluation_ai"
    description = "(AI Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E65QuarterlyHiringTask(CorpTask):
    task_id = "e65_quarterly_hiring_ai"
    description = "(AI Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E66CampaignLaunchTask(CorpTask):
    task_id = "e66_campaign_launch_ai"
    description = "(AI Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E67DatabaseMigrationTask(CorpTask):
    task_id = "e67_database_migration_ai"
    description = "(AI Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E68SecurityAuditTask(CorpTask):
    task_id = "e68_security_audit_ai"
    description = "(AI Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E69ExpenseReconciliationTask(CorpTask):
    task_id = "e69_expense_reconciliation_ai"
    description = "(AI Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E70OfficeRelocationTask(CorpTask):
    task_id = "e70_office_relocation_ai"
    description = "(AI Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E71LaunchReadinessTask(CorpTask):
    task_id = "e71_launch_readiness_infrastructure"
    description = "(Infrastructure Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E72BugTriageTask(CorpTask):
    task_id = "e72_bug_triage_infrastructure"
    description = "(Infrastructure Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E73RegressionTestingTask(CorpTask):
    task_id = "e73_regression_testing_infrastructure"
    description = "(Infrastructure Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E74ModelEvaluationTask(CorpTask):
    task_id = "e74_model_evaluation_infrastructure"
    description = "(Infrastructure Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E75QuarterlyHiringTask(CorpTask):
    task_id = "e75_quarterly_hiring_infrastructure"
    description = "(Infrastructure Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E76CampaignLaunchTask(CorpTask):
    task_id = "e76_campaign_launch_infrastructure"
    description = "(Infrastructure Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E77DatabaseMigrationTask(CorpTask):
    task_id = "e77_database_migration_infrastructure"
    description = "(Infrastructure Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E78SecurityAuditTask(CorpTask):
    task_id = "e78_security_audit_infrastructure"
    description = "(Infrastructure Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E79ExpenseReconciliationTask(CorpTask):
    task_id = "e79_expense_reconciliation_infrastructure"
    description = "(Infrastructure Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E80OfficeRelocationTask(CorpTask):
    task_id = "e80_office_relocation_infrastructure"
    description = "(Infrastructure Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E81LaunchReadinessTask(CorpTask):
    task_id = "e81_launch_readiness_sales"
    description = "(Sales Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E82BugTriageTask(CorpTask):
    task_id = "e82_bug_triage_sales"
    description = "(Sales Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E83RegressionTestingTask(CorpTask):
    task_id = "e83_regression_testing_sales"
    description = "(Sales Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E84ModelEvaluationTask(CorpTask):
    task_id = "e84_model_evaluation_sales"
    description = "(Sales Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E85QuarterlyHiringTask(CorpTask):
    task_id = "e85_quarterly_hiring_sales"
    description = "(Sales Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E86CampaignLaunchTask(CorpTask):
    task_id = "e86_campaign_launch_sales"
    description = "(Sales Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E87DatabaseMigrationTask(CorpTask):
    task_id = "e87_database_migration_sales"
    description = "(Sales Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E88SecurityAuditTask(CorpTask):
    task_id = "e88_security_audit_sales"
    description = "(Sales Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E89ExpenseReconciliationTask(CorpTask):
    task_id = "e89_expense_reconciliation_sales"
    description = "(Sales Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E90OfficeRelocationTask(CorpTask):
    task_id = "e90_office_relocation_sales"
    description = "(Sales Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E91LaunchReadinessTask(CorpTask):
    task_id = "e91_launch_readiness_support"
    description = "(Support Dept) As PM, a new feature is launching in 48 hours. Check codebase stability. Consult qa_agent, capture test status, finalize with GO/NO_GO."
    role = "Product Manager"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "QA report captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "final_recommendation GO/NO_GO populated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E92BugTriageTask(CorpTask):
    task_id = "e92_bug_triage_support"
    description = "(Support Dept) A critical bug is reported in prod. Identify the root cause and prepare a hotfix. Consult dev_agent."
    role = "Software Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Root cause identified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Hotfix ready", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E93RegressionTestingTask(CorpTask):
    task_id = "e93_regression_testing_support"
    description = "(Support Dept) Run the full regression test suite for the new UI redesign. Consult dev_agent."
    role = "QA Engineer"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Test suite passed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Bug report filed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E94ModelEvaluationTask(CorpTask):
    task_id = "e94_model_evaluation_support"
    description = "(Support Dept) Evaluate the new recommendation model's A/B test results. Consult data_agent."
    role = "Data Scientist"
    available_agents = ["data_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Metrics captured", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Decision DEPLOY/ROLLBACK made", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"data_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("data_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E95QuarterlyHiringTask(CorpTask):
    task_id = "e95_quarterly_hiring_support"
    description = "(Support Dept) Finalize the hiring plan for Q3. Consult finance_agent for budget."
    role = "HR Manager"
    available_agents = ["finance_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Budget approved", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Headcount allocated", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"finance_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("finance_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E96CampaignLaunchTask(CorpTask):
    task_id = "e96_campaign_launch_support"
    description = "(Support Dept) Launch the summer marketing campaign. Consult dev_agent to verify landing page."
    role = "Marketing Lead"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Landing page verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Campaign launched", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E97DatabaseMigrationTask(CorpTask):
    task_id = "e97_database_migration_support"
    description = "(Support Dept) Migrate the user database to the new cluster. Consult qa_agent."
    role = "DevOps Engineer"
    available_agents = ["qa_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Backup verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Traffic routed", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"qa_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("qa_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E98SecurityAuditTask(CorpTask):
    task_id = "e98_security_audit_support"
    description = "(Support Dept) Perform a security audit on the new auth module. Consult dev_agent."
    role = "Security Analyst"
    available_agents = ["dev_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Vulnerabilities scanned", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Sign-off provided", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"dev_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("dev_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E99ExpenseReconciliationTask(CorpTask):
    task_id = "e99_expense_reconciliation_support"
    description = "(Support Dept) Reconcile Q2 cloud expenses. Consult ops_agent."
    role = "Finance Analyst"
    available_agents = ["ops_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Expenses verified", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Anomalies flagged", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"ops_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("ops_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

class E100OfficeRelocationTask(CorpTask):
    task_id = "e100_office_relocation_support"
    description = "(Support Dept) Finalize the office relocation plan. Consult hr_agent."
    role = "Operations Lead"
    available_agents = ["hr_agent"]
    token_budget = 8192

    def initial_swd(self, episode_id: str) -> Dict[str, Any]:
        return {
            "episode_id": episode_id,
            "scenario": self.description,
            "phase": "discovery",
            "milestones": [
                {"id": "m1", "label": "Lease signed", "due_by_turn": 6, "status": "pending", "owner": "master", "output": None},
                {"id": "m2", "label": "Moving date set", "due_by_turn": 12, "status": "pending", "owner": "master", "output": None},
            ],
            "agent_reports": {"hr_agent": None},
            "final_recommendation": None,
            "swd_version": 1,
        }

    def verifier(self, swd: Dict[str, Any]) -> Dict[str, bool]:
        return create_verifier(self.task_id)(swd)

    def milestone_complete(self, swd: Dict[str, Any], milestone_id: str) -> bool:
        if milestone_id == "m1":
            return swd.get("agent_reports", {}).get("hr_agent") is not None
        if milestone_id == "m2":
            return swd.get("final_recommendation") is not None
        return False

