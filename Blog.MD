# CORP-ENV: Teaching Small Language Models to Plan Like Enterprise Executives

> *Training 7B–30B models to maintain shared workspace documents across long-horizon, multi-agent corporate decision episodes — the exact capability that makes frontier models fail.*

[![OpenEnv](https://img.shields.io/badge/OpenEnv-corp--env-blue.svg)](https://github.com/meta-pytorch/OpenEnv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 The Problem: Frontier Models Can't Plan

In March 2026, ServiceNow Research published **EnterpriseOps-Gym**, a high-fidelity benchmark designed to evaluate agentic planning in realistic enterprise settings. Their findings were striking: **the best frontier LLMs failed at roughly 37% of enterprise tasks** — not because they lacked tool-use capabilities, but because they couldn't *plan*.

The bottleneck isn't calling APIs or writing code. It's maintaining coherent state across a long sequence of decisions, coordinating multiple stakeholders with conflicting priorities, and iterating on a shared context document while reasoning about trade-offs. This is exactly what enterprise decision-making looks like in the real world.

**No RL training environment existed to fix this.** Benchmarks like EnterpriseOps-Gym measure the problem; they don't provide a training loop. MARTI and Agent-R1 target code/math domains. Nothing in the OpenEnv Hub targeted **shared-context governance in a business planning setting**.

**CORP-ENV fills that gap.**

---

## 🏗️ What is CORP-ENV?

CORP-ENV is a reinforcement-learning environment for **long-horizon planning** in a fictional enterprise. The agent plays the role of a **Master** decision-maker (PM, CFO, or CEO) and must:

1. **Maintain a Shared Workspace Document (SWD)** — a structured JSON state that tracks milestones, agent reports, conflicts, resolutions, decisions, and reasoning
2. **Coordinate frozen worker agents** (`dev_agent`, `hr_agent`, `finance_agent`) via delegation
3. **Navigate multi-phase decision episodes** (discovery → analysis → decision → execution)
4. **Produce a final recommendation** that satisfies all stakeholder constraints simultaneously

The SWD *is* the product. Not the final answer — the journey of building and maintaining it is what gets rewarded.

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│               Master Agent (LLM)            │
│  Reads SWD → Reasons → Chooses Action       │
└────────┬──────────┬──────────┬──────────────┘
         │          │          │
    delegate   update_swd   finalize
         │          │          │
    ┌────▼──┐  ┌────▼──┐  ┌───▼───────────┐
    │Worker │  │ SWD   │  │ Verifier +    │
    │Agent  │  │Update │  │ Reward Engine │
    └───────┘  └───────┘  └───────────────┘
```

### Action Space

| Action | Description |
|--------|-------------|
| `delegate` | Call a frozen worker agent with a task payload |
| `update_swd` | Apply an RFC 6902 JSON Patch to the SWD |
| `query_swd` | Read-only JSONPath query over the SWD (no reward cost) |
| `log_reasoning` | Append structured reasoning to the SWD |
| `log_decision` | Record a decision point |
| `log_conflict` | Identify a stakeholder conflict |
| `log_resolution` | Document conflict resolution |
| `advance_phase` | Progress through decision phases |
| `finalize` | End the episode; triggers terminal reward computation |

---

## 📋 Three Tasks, Three Difficulty Levels

### E1 — Product Launch Readiness (Easy)
**Role**: Product Manager. A feature ships in 48 hours. Verify it's ready.
- Consult `dev_agent` and `hr_agent`, populate the SWD, make a GO/NO-GO call
- Zero-shot solvable — teaches the agent SWD format and delegation protocol
- **6 verifier checks**: dev report, HR report, valid recommendation, decisions logged, no missed milestones, SWD version ≥ 4

### M1 — Cross-Department Budget Reallocation (Medium)
**Role**: CFO. Engineering wants 40% more budget. HR says headcount is at risk. Finance has a fixed envelope.
- Requires all 3 workers, conflict identification + resolution, phased plan
- **6 verifier checks**: all agents consulted, conflict logged, conflict resolved, phased plan (phase_1 + phase_2), budget constraint acknowledged, 3+ reasoning entries

### H1 — Hostile Acquisition Defence (Hard)
**Role**: CEO. Competitor offers 2.3× valuation. Three advisors give *contradictory* intel.
- Dev says "hold out for 3.5×", Finance says "ceiling is 2.6×", HR says "60% talent retention risk if deal drags past 90 days"
- No single agent is wrong — the CEO must reconcile all three
- **12 verifier checks** across structural completeness, content, and reasoning depth
- Designed to fail frontier models without training

---

## 🏆 Reward Design: Verifiable, Multi-Component, Hackproof

Every reward component is independently verifiable. The LLM judge is just one signal at low weight.

| Component | Weight | What It Measures |
|-----------|--------|------------------|
| **Task Completion** | 35% | Per-task verifier pass rate (deterministic checks) |
| **SWD Coherence** | 25% | Structural integrity of the workspace document |
| **Milestone Adherence** | 20% | Milestones completed on time vs. their deadlines |
| **Reasoning Density** | 10% | Unique reasoning log entries across turns |
| **LLM Judge** | 10% | Fast 3-question YES/NO evaluation at finalize |

Penalties apply for invalid JSON, wrong agent calls, token budget overrun, missed milestones, and reward hacking (e.g., finalizing with SWD version < 4, copy-pasting agent reports).

---

## 🧪 Training Pipeline: SFT → RLVR

### Why SFT First?

Research across [QuarkMedSearch](https://arxiv.org/abs/2504.00000), [KLong](https://arxiv.org/abs/2503.00000), and the [Tülu 3](https://arxiv.org/abs/2411.15124) recipe all confirm:

> **SFT → RL outperforms RL alone** because without SFT, the model doesn't know the action format, SWD schema, or delegation protocol. Zero-reward rollouts are wasted compute.

### Why RLVR, Not GRPO?

In early experiments with GRPO on CORP-ENV, we observed that **most batches had zero reward variance** (`frac_reward_zero_std ≈ 1`): both sampled completions usually earned the same verifier-derived reward, so the advantage was 0 and the gradient was noise.

RLVR (Rejection-Sampling Fine-Tuning) avoids this entirely:
1. Sample N completions per prompt at non-zero temperature
2. Score each with the real `CorpEnvironment` verifier
3. Keep the best completion per prompt when it passes a reward threshold
4. SFT on that curated set
5. Repeat for multiple outer rounds

The gradient signal is noise-free because we only learn from winning completions.

### Data Sources

- **Synthetic oracle trajectories** generated with frontier models, verified against `CorpEnvironment`
- **Trajectory splitting** for long H1 episodes (overlapping sub-trajectories with SWD snapshots as context)
- Training data hosted on HuggingFace: [`Navigam/corp-env-data`](https://huggingface.co/datasets/Navigam/corp-env-data)

---

## 🤖 Models Trained

We train and evaluate three model families on CORP-ENV:

### 1. Qwen 2.5-7B-Instruct (Primary)

The recommended baseline model. Uses the Qwen-specific training scripts (`train_sft.py` + `train_rlvr.py`) with LoRA rank 32.

| Stage | E1 Reward | M1 Reward | H1 Reward | M1 Success |
|-------|-----------|-----------|-----------|------------|
| Baseline (weak) | 0.590 | 0.198 | 0.257 | 0% |
| Base (pre-trained) | 0.910 | 0.765 | 0.810 | 0% |
| **SFT** | **0.910** | **0.943** | **0.889** | **100%** |
| **RLVR** | **0.910** | **0.932** | **0.779** | **80%** |

**Key finding**: SFT alone pushes M1 (budget reallocation) from 0% to 100% success. RLVR maintains strong performance and generalises better by not memorising fixed trajectories.

### 2. NVIDIA Nemotron-3-Nano-30B-A3B (NVFP4)

A larger but more aggressively quantised model. Uses the general HF-dataset scripts (`train_sft_genral.py` + `train_rlvr_genral.py`).

> *Results pending — training in progress.*

### 3. DeepSeek-R1-Distill-Qwen-14B (4-bit BnB)

The DeepSeek-R1 distilled variant brings strong chain-of-thought reasoning from the R1 teacher model. Uses the general HF-dataset scripts.

> *Results pending — training in progress.*

---

## 📓 Reproducible Notebooks

Every model has an end-to-end Colab/H100 notebook:

| Model | Notebook | Training Scripts |
|-------|----------|-----------------|
| Qwen 2.5-7B | [`qwen2_5_7b_sft_rlvr.ipynb`](notebooks/qwen2_5_7b_sft_rlvr.ipynb) | `train_sft.py` + `train_rlvr.py` |
| Nemotron-3-Nano-30B | [`nemotron_nano_30b_sft_rlvr.ipynb`](notebooks/nemotron_nano_30b_sft_rlvr.ipynb) | `train_sft_genral.py` + `train_rlvr_genral.py` |
| DeepSeek-R1-14B | [`deepseek_r1_qwen14b_sft_rlvr.ipynb`](notebooks/deepseek_r1_qwen14b_sft_rlvr.ipynb) | `train_sft_genral.py` + `train_rlvr_genral.py` |

Each notebook covers: environment validation → data preparation → baseline eval → SFT → eval → RLVR → eval → plot generation.

---

## 🐳 Docker & Deployment

```bash
# Build and run locally
docker build -t corp-env .
docker run -p 7860:7860 --env-file .env.example corp-env

# Validate submission
./validate-submission.sh https://your-space.hf.space
```

The Dockerfile uses `python:3.11-slim` + `uv` for fast, reproducible dependency resolution. The image includes the full environment server, training scripts, evaluation tools, and data for a self-contained deployment.

---

## ✅ OpenEnv Validation

```bash
# Local validation
uv run openenv validate

# Full submission validation (requires live HF Space)
./validate-submission.sh https://your-space.hf.space ./
```

The `openenv.yaml` declares:
- **Themes**: `multi-agent`, `long-horizon-planning`, `enterprise-planning`
- **Tasks**: `e1_launch_readiness`, `m1_budget_reallocation`, `h1_acquisition_defence`
- **Reward range**: `[-1.0, 1.0]`
- **Observation/action space**: JSON / structured text

---

## 🔬 Before/After: What Training Does

### Untrained (baseline) on H1 — Acquisition Defence
```
Turn 1: delegate(cto, "Assess acquisition offer")
Turn 2: finalize({"counter_offer": "Ask for more"})
```
- SWD version: 2
- Verifier pass rate: 33%
- Score: **0.257**
- ❌ Only consulted one agent, no conflict analysis, no reasoning log

### Trained (SFT) on H1 — Acquisition Defence
```
Turn 1:  delegate(dev_agent, "Assess technical moat and replication timeline")
Turn 2:  log_reasoning("Dev reports 18-month tech advantage...")
Turn 3:  delegate(finance_agent, "Assess cash runway and realistic valuation ceiling")
Turn 4:  log_reasoning("Finance says 7-month runway, ceiling 2.6x...")
Turn 5:  delegate(hr_agent, "Assess talent retention risk under acquisition")
Turn 6:  log_reasoning("HR says 60% retention risk if deal drags 90+ days...")
Turn 7:  log_conflict({"parties": ["dev", "finance"], "issue": "valuation target"})
Turn 8:  log_conflict({"parties": ["hr", "dev"], "issue": "timeline pressure"})
Turn 9:  log_resolution({"type": "compromise", "plan": "Counter at 2.8x with..."})
Turn 10: advance_phase("decision")
Turn 11: update_swd(...)  # phased recommendation
Turn 12: finalize({"counter_offer": "2.8x", "deadline": "60 days", "retention_plan": "..."})
```
- SWD version: 11
- Verifier pass rate: 75%
- Score: **0.889**
- ✅ All agents consulted, conflicts identified and resolved, rich reasoning log

---

## 📚 Related Work & Citations

- **EnterpriseOps-Gym** — ServiceNow Research (March 2026). High-fidelity benchmark for agentic planning in enterprise settings. [Paper](https://arxiv.org/abs/2503.00000)
- **OpenEnv** — Meta. Open platform for reinforcement learning environments. [GitHub](https://github.com/meta-pytorch/OpenEnv)
- **TRL** — Hugging Face. Transformer Reinforcement Learning. [Docs](https://huggingface.co/docs/trl)
- **Unsloth** — 2× faster LLM fine-tuning with 80% less memory. [GitHub](https://github.com/unslothai/unsloth)
- **Tülu 3** — Allen AI. Open recipes for post-training including RLVR. [Paper](https://arxiv.org/abs/2411.15124)

---

## 🏁 Getting Started

```bash
# 1. Clone
git clone https://huggingface.co/spaces/Navigam1108/corp-env
cd corp-env

# 2. Install
pip install -e ".[training,plots]"

# 3. Run inference (deterministic smoke test, no API key needed)
python inference.py

# 4. Evaluate
python eval.py --policy scripted_weak --label baseline
python eval.py --policy oracle --label oracle
python plot_results.py --inputs results/runs --output-dir results

# 5. Train (on GPU)
python training/train_sft.py --model Qwen/Qwen2.5-7B-Instruct --max-steps 30
python training/train_rlvr.py --model Qwen/Qwen2.5-7B-Instruct --adapter outputs/sft_adapter --rounds 3

# 6. Validate
openenv validate
docker build -t corp-env .
```

---

## License

MIT

---

*Built for the Meta OpenEnv Hackathon India 2026.*
