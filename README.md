---
title: CORP-ENV
emoji: briefcase
colorFrom: gray
colorTo: blue
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# CORP-ENV — Shared workspace governance for corporate planning agents

[![OpenEnv](https://img.shields.io/badge/OpenEnv-corp--env-blue.svg)](https://github.com/meta-pytorch/OpenEnv)

**CORP-ENV** is a reinforcement-learning environment for long-horizon **planning** in a fictional enterprise. The agent acts as a **Master** role (PM, CFO, CEO) and maintains a **Shared Workspace Document (SWD)** — a structured JSON state — while delegating to frozen **worker** models (`dev_agent`, `hr_agent`, `finance_agent`). Rewards blend deterministic task checks, SWD coherence, milestone timing, reasoning density, and an optional lightweight LLM judge.

This repo replaces the earlier Jira-to-Code baseline (preserved as git tag `validated-jira-to-code-2026` on `main`) with the CORP-ENV design from `CORP_ENV_Implementation_Guide.md`.

## Actions

| Action | Meaning |
|--------|--------|
| `delegate` | Call a worker (`agent_id` + `payload` task text). |
| `update_swd` | RFC **6902 JSON Patch** on the SWD (`payload` = patch JSON array string). |
| `query_swd` | Read-only **JSONPath** over the SWD. |
| `finalize` | End episode; terminal reward from verifiers + rubric. |

## Tasks

| ID | Difficulty | Summary |
|----|------------|---------|
| `e1_launch_readiness` | Easy | 48h product launch readiness (dev + HR). |
| `m1_budget_reallocation` | Medium | Budget conflict across dev / HR / finance. |
| `h1_acquisition_defence` | Hard | Acquisition defence with injected contradictory intel. |

Select with env var `CORP_TASK_ID` or `reset(task_id=...)` over the API.

## Quick start (uv + uvicorn)

```powershell
cd corp_gym
uv venv
uv sync
uv run uvicorn server.app:app --host 0.0.0.0 --port 7860
```

Or:

```powershell
uv run server
```

## Baseline inference (master agent)

Requires `HF_TOKEN` or `OPENAI_API_KEY` for the **master** model. Without a key, `inference.py` runs a short **deterministic E1** smoke test using stub workers.

```powershell
uv run python inference.py
uv run python inference.py --tasks e1_launch_readiness --max-steps 25
```

## OpenEnv validation

```powershell
uv run openenv validate
```

## Docker

```powershell
docker build -t corp-env .
docker run -p 7860:7860 --env-file .env.example corp-env
```

## Python client

`CorpEnvClient` in [`client/client.py`](client/client.py) is an `EnvClient` for WebSocket sessions against a running server.

## Configuration

See [`.env.example`](.env.example) for `CORP_TASK_ID`, `CORP_STUB_WORKERS`, judge toggles, and API routing.

## License

MIT.
