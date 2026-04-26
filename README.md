---
title: CORP-ENV
emoji: 💼
colorFrom: gray
colorTo: blue
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# CORP-ENV — Shared Workspace Governance for Corporate Planning Agents

[![OpenEnv](https://img.shields.io/badge/OpenEnv-corp--env-blue.svg)](https://github.com/meta-pytorch/OpenEnv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CORP-ENV** is a highly ambitious yet realistic reinforcement-learning environment designed for long-horizon **planning** in an enterprise. The agent steps into a **Master** role (PM, CFO, CEO) and maintains a **Shared Workspace Document (SWD)** : a structured JSON state while delegating tasks to heavily specialized frozen **worker** models (`dev_agent`, `hr_agent`, `finance_agent`). The environment boasts a rich, composable reward signal that is intentionally hard to game.

> 📖 **Read our story**: The [Blog.MD](Blog.MD) dives deep into our philosophy

## Training & Models

We've focused purely on training **Qwen 2.5** through a comprehensive Base → SFT → RLVR pipeline to demonstrate verifiable improvement in our environment.

- **Primary Architecture**: The Qwen 2.5-7B Instruct model was trained on H100 servers using the robust scripts provided in the `training/` directory. All training logs are safely preserved in `training_logs/`.
- **Google Colab Notebook (T4 Friendly)**: Check out [`notebooks/training.ipynb`](notebooks/training.ipynb). This notebook has been specifically tested on a T4 instance. To respect memory bounds (OOM issues), it utilizes the smaller Qwen 2.5 3B instruct model. 
  - *NOTE*: other notebooks for differnet models such as deepseek-14B, nemotron-30B in the repository are provided for reference but are **not guaranteed or tested** to function reliably on Google Colab free tiers.

### Qwen 2.5-7B Results (Average over 5 episodes)

Our latest comprehensive evaluation highlights the leap from Base to SFT and robustly to RLVR:

| Stage | E1 Reward | M1 Reward | H1 Reward | M1 Success |
|-------|-----------|-----------|-----------|------------|
| Base (Qwen 2.5-7B) | 0.910 | 0.707 | 0.761 | 0% |
| **SFT (Qwen 2.5-7B)** | **0.910** | **0.943** | **0.882** | **100%** |
| **RLVR (Qwen 2.5-7B)** | **0.910** | **0.932** | **0.779** | **80%** |

## Environment Actions

| Action | Meaning |
|--------|--------|
| `delegate` | Call a worker (`agent_id` + `payload` task text). |
| `update_swd` | RFC **6902 JSON Patch** on the SWD. |
| `query_swd` | Read-only **JSONPath** over the SWD. |
| `log_reasoning` | Append a structured reasoning note to the SWD. |
| `log_decision` | Append a decision note to the SWD. |
| `log_conflict` | Append a conflict object to `conflicts_identified`. |
| `log_resolution` | Append a conflict-resolution object to `conflict_resolutions`. |
| `advance_phase` | Move the SWD phase through `analysis`, `decision`, or `execution`. |
| `finalize` | End episode; terminal reward from rich verifiers and OpenEnv rubrics. |

## Shared Workspace Document (SWD) Structure

The SWD is a rigorous JSON schema defining the exact state of the enterprise episode. Agents must issue valid JSON patches against this structure:

```json
{
  "episode_id": "uuid",
  "scenario": "description of the problem",
  "phase": "discovery | analysis | decision | execution",
  "milestones": [
    {
      "id": "str",
      "label": "str",
      "due_by_turn": 10,
      "status": "pending",
      "owner": "agent_id",
      "output": null
    }
  ],
  "agent_reports": {
    "qa": null,
    "dev": null,
    "hr": null,
    "finance": null
  },
  "decisions": [],
  "conflicts_identified": [],
  "conflict_resolutions": [],
  "reasoning_log": [],
  "final_recommendation": null,
  "swd_version": 0
}
```

## Tasks

| ID | Difficulty | Summary |
|----|------------|---------|
| `e1_launch_readiness` | Easy | 48h product launch readiness (QA stability gate). |
| `m1_budget_reallocation` | Medium | Budget conflict across dev / HR / finance. |
| `h1_acquisition_defence` | Hard | Acquisition defence with injected contradictory intel. |

## Quick Start

```bash
# Using uv
uv venv && uv sync
uv run uvicorn server.app:app --host 0.0.0.0 --port 7860

# Or simply
uv run server
```

## Baseline Inference

Run a **deterministic E1 smoke test** using stub workers. We ensure 100% determinism via `CORP_STUB_WORKERS=1` and `CORP_DISABLE_LLM_JUDGE=1`:

```bash
uv run python inference.py
uv run python inference.py --tasks e1_launch_readiness --max-steps 25 --swd-trace logs/run.jsonl
```

## OpenEnv Validation

```bash
uv run openenv validate
```

## Docker

```bash
docker build -t corp-env .
docker run -p 7860:7860 --env-file .env.example corp-env
```

## License

MIT.
