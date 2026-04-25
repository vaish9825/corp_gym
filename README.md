---
title: Jira-To-Code Agent Environment
emoji: 🛠️
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🚀 Jira-To-Code: The Ultimate RL Coding Environment

[![OpenEnv Validated](https://img.shields.io/badge/OpenEnv-Validated-green.svg)](https://github.com/meta-pytorch/OpenEnv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Jira-To-Code** is a high-fidelity Reinforcement Learning (RL) environment designed for the **Meta/Hugging Face OpenEnv Hackathon**. It challenges AI agents to act as Senior Software Engineers by resolving real-world Jira tickets within a secure, sandboxed codebase.

---

## 🌟 Key Features

*   **⚡ ReAct Ready**: Built-in support for Thought-Action-Observation loops.
*   **🧠 Episodic Memory**: Maintains full conversational history for multi-turn reasoning.
*   **📊 22 Diverse Tasks**: From simple bug fixes to complex architecture, concurrency, and security.
*   **📈 Rich Reward Shaping**: Partial credit for passing tests, step penalties for efficiency, and shaping rewards for active coding.
*   **🛡️ Robust Parsing**: Resilient JSON extraction and self-correction prompt injection.

---

## 🏗️ Environment Architecture

Agents interact with the environment via a standardized FastAPI interface:

| Action | Description |
| :--- | :--- |
| `list_files` | Explore the workspace directory structure. |
| `read_file` | Read the content of a specific file. |
| `write_file` | Create or overwrite code in the workspace. |
| `run_tests` | Execute `pytest` and receive detailed traceback output. |
| `submit` | Finalize the task and receive the definitive score. |

---

## 🎯 Available Tasks (22 Total)

| Task ID | Level | Objective |
| :--- | :--- | :--- |
| `easy` | Easy | Fix off-by-one bug in `calculator.add()`. |
| `easy_2` | Easy | Fix case-sensitivity bug in `string_utils.count_vowels()`. |
| `easy_3` | Easy | API KeyError: use `.get()` with fallback for missing `phone_number`. |
| `easy_4` | Easy | Off-by-One Pagination: Fix math index logic in `get_page_bounds`. |
| `easy_5` | Easy | FastAPI Route Typo: Align `user_id` route param with function arg. |
| `medium` | Medium | Implement `format_user_data()` dictionary mapping specs. |
| `medium_2` | Medium | Implement complex `Email` and `Password` validation logic. |
| `medium_3` | Medium | Missing Auth Middleware: Apply `@require_auth` to `/api/billing`. |
| `medium_4` | Medium | ORM N+1 Problem: Rewrite fetches to use JOINs (`select_related`). |
| `medium_5` | Medium | Regex Validation: Fix email regex to allow plus sign (`+`). |
| `medium_6` | Medium | Error Handling: Add try/except fallback for currency rate timeouts. |
| `medium_7` | Medium | Stale Cache: Add Redis invalidation to `update_user_profile`. |
| `medium_8` | Medium | Timezone Naive: Make naive datetimes UTC aware. |
| `medium_9` | Medium | State Machine: Add transition guards (CANCELLED -> SHIPPED). |
| `medium_10` | Medium | Config Merge: Fix recursion logic for nested dict merges. |
| `hard` | Hard | Implement `LRUCache` with $O(1)$ time complexity. |
| `hard_2` | Hard | Implement `DirectedGraph` with BFS/DFS and Topological Sort. |
| `hard_3` | Hard | Circular Dependency: Refactor `models/utils/config` via `base.py`. |
| `hard_4` | Hard | Race Condition: Refactor threaded worker to use `queue.Queue`. |
| `hard_5` | Hard | OOM Generator: Rewrite `readlines()` loop to use `yield` generators. |
| `hard_6` | Hard | Implementation: Code `StripeGateway` matching `PaymentGateway` ABC. |
| `hard_7` | Hard | Async Deadlock: Fix lock release safety using async context managers. |

---

## 🚀 Getting Started

### 1. Local Setup
```bash
# Clone the repository
git clone https://huggingface.co/spaces/Navigam/jira-to-code
cd jira-to-code

# Create and activate environment
uv venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

# Install dependencies
uv pip install -e .
```

### 2. Run Inference
```bash
# Run the full baseline agent against all tasks
uv run python inference.py

# Run a specific task
uv run python inference.py --tasks easy_2,medium
```

### 3. Docker Deployment
```bash
docker build -t jira-to-code .
docker run -p 7860:7860 jira-to-code
```

---

## 🛠️ Deep Dive: Design & Rubric Alignment

### 🎨 Creativity & Novelty
*   **Real-World Software Engineering Domain**: While most RL environments focus on games or simplified logic, **Jira-To-Code** provides a high-stakes, documentation-driven coding domain. Agents are forced to interpret edge cases from docstrings (e.g., case-insensitivity in vowel counting) just like real developers.
*   **Non-Sparse Reward Mechanics**: We move away from binary "Pass/Fail" signals. The environment rewards "Progress Toward Solution" by parsing intermediate test results.

### 📈 Reward Signal Design
The environment provides a dense, informative reward signal to guide agent learning, ensuring all step scores are strictly continuously bounded:
*   **Strict Bounds (`0.01` to `0.99`)**: To comply with grading requirements, every step evaluated unconditionally maps to a boundary range strictly between 0 and 1. The literal 0.0 and 1.0 are actively bypassed.
*   **Action & Thinking Weightage**: The first 3 orientation steps (e.g., listing/reading files, thinking) receive a `+0.02` bonus shaping token to reward early planning.
*   **Efficiency Penalty**: For all steps beyond the 3rd step, a `-0.01` penalty is continuously applied to minimize rewards for agents taking excessively long.
*   **Linear Partial Credit**: Intermediate `run_tests` and the final `submit` rewards are calculated proportionally as `(passed_tests / total_tests)`.

### 🧱 Episode & Workspace Design
*   **Isolation & Reset**: Every `reset()` call generates a **cryptographically unique, isolated temporary directory**. This ensures the agent starts with a "Clean Slate" and prevents cross-contamination between tasks or episodes.
*   **Atomic Boundaries**: An episode concludes when the agent calls `submit` or reaches `MAX_STEPS`.
*   **Deterministic Grading**: Graders are based on hidden unit tests (`pytest`) that are immutable within the environment container, ensuring 100% reproducible scoring.

---

## 🏆 Scoring Rubric Alignment

This environment is optimized for high marks in the OpenEnv Hackathon:
*   **Real-world Utility**: Models a developer's daily workflow.
*   **Task/Grader Quality**: Deterministic `pytest` grading with partial credit.
*   **Environment Design**: Gymnasium-style API with comprehensive observation space.
*   **Code Quality**: Passes `openenv validate` and follows strict Pydantic typing.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ for the OpenEnv Hackathon by <a href="https://huggingface.co/Navigam">Navigam</a></sub>
</div>
