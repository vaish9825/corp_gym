# server/env.py
import os
import re
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Tuple, Dict, Any
import sys

from openenv.core.env_server import Environment, State
from src.jira_to_code.models import JiraCodeAction, JiraCodeObservation


class JiraToCodeEnv(Environment):
    TASKS = {
        "easy": {
            "dir": "src/jira_to_code/tasks/easy",
            "ticket": (
                "TICKET-101: Fix the off-by-one bug in calculator.add() function. "
                "It should correctly sum two numbers."
            ),
        },
        "easy_2": {
            "dir": "src/jira_to_code/tasks/easy_2",
            "ticket": (
                "TICKET-102: Fix the bug in string_utils.count_vowels(). "
                "It currently only counts lowercase vowels but should be case-insensitive."
            ),
        },
        "easy_3": {"dir": "src/jira_to_code/tasks/easy_3", "ticket": "TICKET-E3: The API endpoint crashes with a KeyError when a user payload doesn't contain an optional 'phone_number' field. Change dictionary indexing to .get() with a fallback."},
        "easy_4": {"dir": "src/jira_to_code/tasks/easy_4", "ticket": "TICKET-E4: Off-by-One Pagination. get_page_bounds(page, size) misses the 10th item on page 1. Fix the math index logic."},
        "easy_5": {"dir": "src/jira_to_code/tasks/easy_5", "ticket": "TICKET-E5: FastAPI Route Typo. Route signature is id instead of user_id. Fix the parameter mismatch."},
        "medium": {
            "dir": "src/jira_to_code/tasks/medium",
            "ticket": (
                "TICKET-201: Implement format_user_data in formatter.py. "
                "It should format dictionary data to 'LAST_NAME, First_name (Age: X)'. "
                "Handle missing age by defaulting to 'Unknown'."
            ),
        },
        "medium_2": {
            "dir": "src/jira_to_code/tasks/medium_2",
            "ticket": (
                "TICKET-202: Implement validate_email() and validate_password() in validator.py. "
                "Email: must have exactly one '@', at least 1 char before '@', a '.' after '@' with chars around it. "
                "Password: at least 8 chars, one uppercase, one lowercase, one digit."
            ),
        },
        "medium_3": {"dir": "src/jira_to_code/tasks/medium_3", "ticket": "TICKET-M3: Missing Authentication Middleware. A sensitive endpoint (/api/billing) is exposed. Import @require_auth from auth.py and apply it to the route in routes.py."},
        "medium_4": {"dir": "src/jira_to_code/tasks/medium_4", "ticket": "TICKET-M4: N+1 Database Problem. Rewrite the ORM query to use a JOIN (e.g., select_related)."},
        "medium_5": {"dir": "src/jira_to_code/tasks/medium_5", "ticket": "TICKET-M5: Flawed Regex Validation. validate_email rejects emails with a plus sign. Update regex to allow user+test@gmail.com."},
        "medium_6": {"dir": "src/jira_to_code/tasks/medium_6", "ticket": "TICKET-M6: Incomplete Error Handling. fetching currency rates crashes on timeout. Wrap in try/except and return a cached fallback value."},
        "medium_7": {"dir": "src/jira_to_code/tasks/medium_7", "ticket": "TICKET-M7: Stale Cache Bug. update_user_profile updates DB but forgets to call redis.delete('user:id'). Invalidate the cache."},
        "medium_8": {"dir": "src/jira_to_code/tasks/medium_8", "ticket": "TICKET-M8: Timezone Naive Conversion. Event scheduling function creates naive datetimes. Make them UTC aware."},
        "medium_9": {"dir": "src/jira_to_code/tasks/medium_9", "ticket": "TICKET-M9: State Machine Loophole. Cart state machine allows CANCELLED to SHIPPED. Add transition guards."},
        "medium_10": {"dir": "src/jira_to_code/tasks/medium_10", "ticket": "TICKET-M10: Config Merge Overwrite. YAML merge completely overwrites nested dictionaries. Fix recursion logic."},
        "hard": {
            "dir": "src/jira_to_code/tasks/hard",
            "ticket": (
                "TICKET-301: Implement an LRUCache class in lru_cache.py with put() and get() methods. "
                "O(1) time complexity expected. Evict least recently used when capacity is reached."
            ),
        },
        "hard_2": {
            "dir": "src/jira_to_code/tasks/hard_2",
            "ticket": (
                "TICKET-302: Implement a DirectedGraph class in graph.py with add_edge(), "
                "has_path() (BFS/DFS), and topological_sort() methods. "
                "topological_sort() must return an empty list if a cycle is detected."
            ),
        },
        "hard_3": {"dir": "src/jira_to_code/tasks/hard_3", "ticket": "TICKET-H3: Circular Dependency Resolution. models.py, utils.py, config.py. Extract shared logic into base.py."},
        "hard_4": {"dir": "src/jira_to_code/tasks/hard_4", "ticket": "TICKET-H4: Race Condition in Thread Worker. Refactor the architecture to use queue.Queue."},
        "hard_5": {"dir": "src/jira_to_code/tasks/hard_5", "ticket": "TICKET-H5: OOM Generator Fix. Readlines causes crash on 5GB file. Rewrite to yield generators."},
        "hard_6": {"dir": "src/jira_to_code/tasks/hard_6", "ticket": "TICKET-H6: Implement Abstract Base Class. Implement StripeGateway matching PaymentGateway abstract class."},
        "hard_7": {"dir": "src/jira_to_code/tasks/hard_7", "ticket": "TICKET-H7: Deadlock in Asyncio. Route acquires threading.Lock but forgets to release on exception. Use async context managers."},
    }

    # Reward configuration
    STEP_PENALTY = -0.01  # Small penalty per step to encourage efficiency
    GRACE_STEPS = 3       # No penalty for first N steps (orientation phase)

    def __init__(self):
        super().__init__()
        self.step_count = 0
        self.workspace_dir = None
        self.task_level = "easy"
        self.task_source_dir = None
        self.jira_ticket = ""

    def _get_file_tree(self) -> list[str]:
        if not self.workspace_dir:
            return []
        tree = []
        for root, _, files in os.walk(self.workspace_dir):
            for file in files:
                if "__pycache__" in root or file.endswith(".pyc"):
                    continue
                rel_path = Path(root) / file
                tree.append(str(rel_path.relative_to(self.workspace_dir)))
        return tree

    @staticmethod
    def _parse_pytest_results(output: str) -> tuple[int, int]:
        """Extract (passed, total) from pytest output for partial-credit scoring."""
        match_passed = re.search(r'(\d+) passed', output)
        passed = int(match_passed.group(1)) if match_passed else 0
        match_failed = re.search(r'(\d+) failed', output)
        failed = int(match_failed.group(1)) if match_failed else 0
        match_error = re.search(r'(\d+) error', output)
        errors = int(match_error.group(1)) if match_error else 0
        total = passed + failed + errors
        return passed, max(total, 1)

    def reset(self) -> JiraCodeObservation:
        self.step_count = 0
        if self.workspace_dir and Path(self.workspace_dir).exists():
            shutil.rmtree(self.workspace_dir)

        # Re-read task level from environment variable on every reset
        self.task_level = os.getenv("JIRA_TASK_LEVEL", "medium").lower()
        if self.task_level not in self.TASKS:
            self.task_level = "easy"

        self.task_source_dir = Path(self.TASKS[self.task_level]["dir"]).resolve()
        self.jira_ticket = self.TASKS[self.task_level]["ticket"]

        self.workspace_dir = tempfile.mkdtemp(prefix=f"jira_env_{self.task_level}_")

        if self.task_source_dir.exists():
            shutil.copytree(self.task_source_dir, self.workspace_dir, dirs_exist_ok=True)
        else:
            print(f"Warning: Task directory {self.task_source_dir} not found!")

        return JiraCodeObservation(
            jira_ticket=self.jira_ticket,
            file_tree=self._get_file_tree(),
        )

    def step(self, action: JiraCodeAction) -> Tuple[JiraCodeObservation, float, bool, Dict[str, Any]]:
        self.step_count += 1
        reward = 0.0
        done = False
        current_file_content = None
        test_output = None
        error = None

        workspace_path = Path(self.workspace_dir).resolve()

        try:
            if action.action_type == "list_files":
                current_file_content = "\n".join(self._get_file_tree())

            elif action.action_type in ["read_file", "write_file"]:
                if not action.file_path:
                    error = "file_path must be provided for read/write actions."
                else:
                    target_path = (workspace_path / action.file_path).resolve()
                    if not target_path.is_relative_to(workspace_path):
                        error = "Access denied: cannot access files outside workspace."
                    elif action.action_type == "read_file":
                        if target_path.exists():
                            current_file_content = target_path.read_text()
                        else:
                            error = f"File not found: {action.file_path}"
                    elif action.action_type == "write_file":
                        if action.content is None:
                            error = "content must be provided for write_file action."
                        else:
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            target_path.write_text(action.content)
                            current_file_content = action.content
                            reward = 0.05  # Small shaping reward for taking action

            elif action.action_type == "run_tests":
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", "-v"],
                    cwd=self.workspace_dir,
                    capture_output=True, text=True, timeout=30,
                )
                test_output = result.stdout + "\n" + result.stderr
                passed, total = self._parse_pytest_results(test_output)

                if result.returncode == 0:
                    # All tests pass — strong positive signal
                    reward = 0.1 + 0.4 * (passed / total)
                elif result.returncode == 1:
                    # Some tests fail — partial credit
                    reward = 0.1 * (passed / total)
                else:
                    # Collection error / crash
                    reward = -0.1

            elif action.action_type == "submit":
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", "-v"],
                    cwd=self.workspace_dir,
                    capture_output=True, text=True, timeout=30,
                )
                test_output = result.stdout + "\n" + result.stderr
                passed, total = self._parse_pytest_results(test_output)
                done = True

                if result.returncode == 0:
                    reward = 1.0  # Full marks
                else:
                    reward = 0.5 * (passed / total)  # Partial credit on submit

        except subprocess.TimeoutExpired:
            error = "Tests timed out after 30 seconds."
            test_output = "TIMEOUT"
            reward = -0.1
        except Exception as e:
            error = f"System error: {str(e)}"
            reward = -0.2

        # Apply shaping rewards based on step count
        if self.step_count <= 3:
            reward += 0.02
        else:
            reward -= 0.01

        # Enforce strictly bounded rewards for OpenEnv requirements (between 0.01 and 0.99)
        reward = max(0.01, min(0.99, reward))

        obs = JiraCodeObservation(
            jira_ticket=self.jira_ticket,
            file_tree=self._get_file_tree(),
            current_file_content=current_file_content,
            test_output=test_output,
            error=error,
        )
        return obs, reward, done, {}

    def state(self) -> State:
        return State(
            episode_id=f"jira-{self.task_level}-{self.step_count}",
            step_count=self.step_count,
        )

    def close(self):
        if self.workspace_dir and Path(self.workspace_dir).exists():
            shutil.rmtree(self.workspace_dir)