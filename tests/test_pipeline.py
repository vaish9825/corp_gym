from __future__ import annotations

import os
import unittest

from scripts._trajectory_utils import oracle_actions, replay_actions
from server.environment import CorpEnvironment
from server.verifiers import verify_e1, verify_m1


class PipelineSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["CORP_STUB_WORKERS"] = "1"
        os.environ["CORP_DISABLE_LLM_JUDGE"] = "1"

    def test_oracle_e1_replays_cleanly(self) -> None:
        result = replay_actions(
            example_id="test-e1",
            task_id="e1_launch_readiness",
            actions=oracle_actions("e1_launch_readiness"),
        )
        self.assertEqual(result.status, "clean")
        self.assertGreaterEqual(result.terminal_reward, 0.65)
        self.assertTrue(all(result.verifier_result.values()))

    def test_oracle_m1_replays_cleanly(self) -> None:
        result = replay_actions(
            example_id="test-m1",
            task_id="m1_budget_reallocation",
            actions=oracle_actions("m1_budget_reallocation"),
        )
        self.assertEqual(result.status, "clean")
        self.assertGreaterEqual(result.verifier_pass_rate, 5 / 6)

    def test_invalid_trajectory_is_rejected(self) -> None:
        result = replay_actions(
            example_id="bad",
            task_id="e1_launch_readiness",
            actions=[{"action_type": "finalize", "payload": "GO"}],
        )
        self.assertEqual(result.status, "rejected")

    def test_verifier_e1_requires_qa_and_final(self) -> None:
        env = CorpEnvironment()
        swd = env.reset(task_id="e1_launch_readiness").swd
        checks = verify_e1(swd)
        self.assertFalse(checks["qa_report_present"])
        self.assertFalse(checks["final_rec_valid"])

    def test_verifier_m1_budget_terms(self) -> None:
        swd = {
            "agent_reports": {"dev": "ok", "finance": "ok"},
            "conflicts_identified": [{"id": "c1"}],
            "conflict_resolutions": [{"conflict_id": "c1"}],
            "decisions": [],
            "reasoning_log": [{"turn": 1, "text": "budget and runway are constrained"}],
            "final_recommendation": {"phase_1": "limited GPU purchase"},
        }
        checks = verify_m1(swd)
        self.assertTrue(checks["required_agents_consulted"])
        self.assertTrue(checks["budget_constraint_acknowledged"])
        self.assertTrue(checks["phased_plan"])


if __name__ == "__main__":
    unittest.main()
