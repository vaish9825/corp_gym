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

**CORP-ENV** is a reinforcement-learning environment for long-horizon **planning** in a fictional enterprise. The agent acts as a **Master** role (PM, CFO, CEO) and maintains a **Shared Workspace Document (SWD)** — a structured JSON state — while delegating to frozen **worker** models (`dev_agent`, `hr_agent`, `finance_agent`). Rewards blend deterministic task checks, SWD coherence, milestone timing, reasoning density, and an optional lightweight LLM judge.

> 📖 **Read the full blog post**: [Blog.MD](Blog.MD) — problem statement, architecture deep-dive, training approach, and results.

## Models Trained

| Model | Size | SFT Script | RLVR Script | Notebook |
|-------|------|-----------|------------|----------|
| [Qwen 2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 7B | `train_sft.py` | `train_rlvr.py` | [qwen2_5_7b_sft_rlvr.ipynb](notebooks/qwen2_5_7b_sft_rlvr.ipynb) |
| [Nemotron-3-Nano-30B (NVFP4)](https://huggingface.co/unsloth/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4) | 30B | `train_sft_genral.py` | `train_rlvr_genral.py` | [nemotron_nano_30b_sft_rlvr.ipynb](notebooks/nemotron_nano_30b_sft_rlvr.ipynb) |
| [DeepSeek-R1-Distill-Qwen-14B (4-bit)](https://huggingface.co/unsloth/DeepSeek-R1-Distill-Qwen-14B-unsloth-bnb-4bit) | 14B | `train_sft_genral.py` | `train_rlvr_genral.py` | [deepseek_r1_qwen14b_sft_rlvr.ipynb](notebooks/deepseek_r1_qwen14b_sft_rlvr.ipynb) |

### Qwen 2.5-7B Results

| Stage | E1 Reward | M1 Reward | H1 Reward | M1 Success |
|-------|-----------|-----------|-----------|------------|
| Baseline (weak) | 0.590 | 0.198 | 0.257 | 0% |
| Base (pre-trained) | 0.910 | 0.765 | 0.810 | 0% |
| **SFT** | **0.910** | **0.943** | **0.889** | **100%** |
| **RLVR** | **0.910** | **0.932** | **0.779** | **80%** |

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

## Quick Start

```bash
# Using uv
uv venv && uv sync
uv run uvicorn server.app:app --host 0.0.0.0 --port 7860

# Or simply
uv run server
```

## Baseline Inference

Without an API key, `inference.py` runs a **deterministic E1 smoke test** using stub workers:

```bash
uv run python inference.py
uv run python inference.py --tasks e1_launch_readiness --max-steps 25 --swd-trace logs/run.jsonl
```

Set `CORP_MASTER_API_KEY` (or `HF_TOKEN` / `OPENAI_API_KEY`) to run the full LLM master agent. See [`.env.example`](.env.example).

## Training

### Qwen 2.5-7B Instruct (Primary)

```bash
pip install -e ".[training]"

# SFT
python training/train_sft.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --data data/sft/e1_m1_h1_examples.jsonl \
  --output outputs/sft_adapter --max-steps 30

# RLVR
python training/train_rlvr.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapter outputs/sft_adapter \
  --output outputs/rlvr_adapter \
  --strict-json --max-prompts 128 --rounds 3
```

### Other Models (General Scripts)

For Nemotron-3-Nano-30B and DeepSeek-R1-Distill-Qwen-14B, use the general HF-dataset scripts:

```bash
# SFT (downloads data from HF dataset repo)
python training/train_sft_genral.py \
  --model unsloth/DeepSeek-R1-Distill-Qwen-14B-unsloth-bnb-4bit \
  --dataset-repo Navigam/corp-env-data \
  --dataset-file e1_m1_h1_examples.jsonl \
  --output outputs/sft_deepseek_14b

# RLVR
python training/train_rlvr_genral.py \
  --model unsloth/DeepSeek-R1-Distill-Qwen-14B-unsloth-bnb-4bit \
  --adapter outputs/sft_deepseek_14b \
  --dataset-repo Navigam/corp-env-data \
  --output outputs/rlvr_deepseek_14b \
  --rounds 3
```

## Notebooks

End-to-end reproducible notebooks for each model variant:

- 📓 **Qwen 2.5-7B**: [`notebooks/qwen2_5_7b_sft_rlvr.ipynb`](notebooks/qwen2_5_7b_sft_rlvr.ipynb)
- 📓 **Nemotron-3-Nano-30B**: [`notebooks/nemotron_nano_30b_sft_rlvr.ipynb`](notebooks/nemotron_nano_30b_sft_rlvr.ipynb)
- 📓 **DeepSeek-R1-14B**: [`notebooks/deepseek_r1_qwen14b_sft_rlvr.ipynb`](notebooks/deepseek_r1_qwen14b_sft_rlvr.ipynb)
- 📓 **Original training notebook**: [`notebooks/corp_env_trl_unsloth_training.ipynb`](notebooks/corp_env_trl_unsloth_training.ipynb)

See [`docs/lightning_hf_runbook.md`](docs/lightning_hf_runbook.md) for the short-session H100 + Hugging Face workflow.

## Data Preparation

```bash
# Verify examples against CorpEnvironment
uv run python scripts/run_data_pipeline.py --write-legacy-copies

# Generate H1 seed data
uv run python scripts/generate_sft_data.py --tasks h1_acquisition_defence --per-task 8 --output data/raw/h1_seed.jsonl
uv run python scripts/verify_examples.py --input data/raw/h1_seed.jsonl --clean data/processed/h1_seed_clean.jsonl

# Merge into SFT dataset
uv run python scripts/prepare_sft_data.py
```

## Evaluation & Plots

```bash
uv run python eval.py --policy scripted_weak --label baseline
uv run python eval.py --policy oracle --label oracle
uv run python eval.py --policy hf --model <base_model> --adapter <adapter_path> --label sft
uv run python plot_results.py --inputs results/runs --output-dir results
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

Full submission validation (requires a live HF Space):

```bash
./validate-submission.sh https://your-space.hf.space
```

## Python Client

`CorpEnvClient` in [`client/client.py`](client/client.py) is an `EnvClient` for WebSocket sessions against a running server.

## Configuration

See [`.env.example`](.env.example) for master/worker/judge API routing, `CORP_TASK_ID`, `CORP_STUB_WORKERS`, and `CORP_SWD_TRACE_FILE`.

## License

MIT.
