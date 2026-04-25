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
| `log_reasoning` | Append a structured reasoning note to the SWD. |
| `log_decision` | Append a decision note to the SWD. |
| `log_conflict` | Append a conflict object to `conflicts_identified`. |
| `log_resolution` | Append a conflict-resolution object to `conflict_resolutions`. |
| `advance_phase` | Move the SWD phase through `analysis`, `decision`, or `execution`. |
| `finalize` | End episode; terminal reward from verifiers + rubric. |

## Tasks

| ID | Difficulty | Summary |
|----|------------|---------|
| `e1_launch_readiness` | Easy | 48h product launch readiness (QA stability gate). |
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

Requires a **master** API key (`CORP_MASTER_API_KEY`, or `HF_TOKEN` / `OPENAI_API_KEY` as fallback). Without it, `inference.py` runs a short **deterministic E1** smoke test using stub workers. Optional **per-worker** and **judge** keys/URLs are in [`.env.example`](.env.example). Set `CORP_SWD_TRACE_FILE` or pass `--swd-trace path.jsonl` to append SWD snapshots to a file separate from console logs.

```powershell
uv run python inference.py
uv run python inference.py --tasks e1_launch_readiness --max-steps 25 --swd-trace logs/run.jsonl
```

## Example verification and SFT data

Replay generated examples against the current environment before training:

```powershell
uv run python scripts/verify_examples.py --input data/raw/e1_m1_examples.jsonl --clean data/processed/e1_m1_clean.jsonl --rejected data/processed/e1_m1_rejected.jsonl
uv run python scripts/prepare_sft_data.py --input data/processed/e1_m1_clean.jsonl --output data/sft/e1_m1_examples.jsonl
```

Generate a small H1 seed set if needed:

```powershell
uv run python scripts/generate_sft_data.py --tasks h1_acquisition_defence --per-task 8 --output data/raw/h1_seed.jsonl
uv run python scripts/verify_examples.py --input data/raw/h1_seed.jsonl --clean data/processed/h1_seed_clean.jsonl --rejected data/processed/h1_seed_rejected.jsonl
```

## Training

Training scripts are intended for a GPU machine such as Lightning AI H100:

```bash
pip install -e ".[training]"
python training/train_sft.py --model Qwen/Qwen2.5-7B-Instruct --data data/sft/e1_m1_examples.jsonl --output outputs/sft_adapter
python training/train_grpo.py --model Qwen/Qwen2.5-7B-Instruct --adapter outputs/sft_adapter --output outputs/grpo_adapter
```

See [`docs/lightning_hf_runbook.md`](docs/lightning_hf_runbook.md) for the short-session H100 + Hugging Face workflow.

## Evaluation and plots

Evaluate all model stages through the same environment:

```powershell
uv run python eval.py --policy scripted_weak --label baseline --output results/baseline_eval.jsonl
uv run python eval.py --policy oracle --label oracle --output results/oracle_eval.jsonl
uv run python plot_results.py --inputs results/baseline_eval.jsonl results/oracle_eval.jsonl --output-dir results
```

For trained adapters on a GPU box, use `eval.py --policy hf --model <base_model> --adapter <adapter_path>`.

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

See [`.env.example`](.env.example) for master/worker/judge API routing, `CORP_TASK_ID`, `CORP_STUB_WORKERS`, and `CORP_SWD_TRACE_FILE`.

## License

MIT.
