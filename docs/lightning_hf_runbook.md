# Lightning AI + Hugging Face Runbook

This runbook is optimized for short 3-4 hour H100 windows and Hugging Face credits. The judge-rerunnable notebook version is [`notebooks/corp_env_trl_unsloth_training.ipynb`](../notebooks/corp_env_trl_unsloth_training.ipynb). A minified (single-line) Colab export in the repo can be searched for `train_grpo` or `MAX_STEPS` to recover pins or a prior command line, then align with the defaults in `training/train_grpo.py` and `training/train_sft.py`.

## 1. Prepare Artifacts Locally

```powershell
uv sync --extra dev --extra plots
uv run python scripts/generate_sft_data.py --tasks h1_acquisition_defence --per-task 24 --variant-stride 2 --output data/raw/h1_seed.jsonl
uv run python scripts/verify_examples.py --input data/raw/e1_m1_examples.jsonl --clean data/processed/e1_m1_clean.jsonl --rejected data/processed/e1_m1_rejected.jsonl --strict-json --require-stepwise-deliberation
uv run python scripts/verify_examples.py --input data/raw/h1_seed.jsonl --clean data/processed/h1_seed_clean.jsonl --rejected data/processed/h1_seed_rejected.jsonl --strict-json --require-stepwise-deliberation
uv run python scripts/prepare_sft_data.py --min-pass-rate 0.85 --min-reasoning-steps 1 --min-conflict-steps 0 --min-resolution-steps 0 --require-stepwise-deliberation
```

Keep raw examples untouched. Train only from verified `data/processed/*_clean.jsonl` and `data/sft/*.jsonl`.

## 2. Upload Dataset To Hugging Face

```powershell
huggingface-cli login
huggingface-cli repo create corp-env-data --type dataset
huggingface-cli upload <your-user-or-org>/corp-env-data data/sft/e1_m1_h1_examples.jsonl data/sft/e1_m1_h1_examples.jsonl --repo-type dataset
huggingface-cli upload <your-user-or-org>/corp-env-data data/processed/e1_m1_clean.jsonl data/processed/e1_m1_clean.jsonl --repo-type dataset
huggingface-cli upload <your-user-or-org>/corp-env-data data/processed/h1_seed_clean.jsonl data/processed/h1_seed_clean.jsonl --repo-type dataset
```

Retire or mirror `e1_m1_examples.jsonl` in the same dataset if you need backward-compatible paths.

## 3. Lightning H100 Session 1: SFT

```bash
git clone <repo-url> corp_gym
cd corp_gym
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[training]"
huggingface-cli login
python training/train_sft.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --data data/sft/e1_m1_h1_examples.jsonl \
  --output outputs/sft_adapter \
  --epochs 2 \
  --max-steps 30 \
  --push-to-hub <your-user-or-org>/corp-env-sft-adapter
```

This uses Unsloth + TRL `SFTTrainer` with conversational `messages` JSONL (and optional `--packing` / `--dataloader-num-workers` on a strong box). If setup time is short, use a 7B model. For quality runs, target 14B with strict-clean traces. Remove `--max-steps 30` or raise it for a real run. Install a `flash-attn` wheel that matches the session’s `torch`+CUDA for best GRPO and long-context SFT step time.

### 14B SFT presets (smoke then full)

```bash
# Qwen3 14B smoke
python training/train_sft.py \
  --model Qwen/Qwen3-14B-Instruct \
  --data data/sft/e1_m1_h1_examples.jsonl \
  --output outputs/sft_qwen3_14b \
  --batch-size 1 --grad-accum 8 --max-steps 20

# Qwen3 14B fuller run
python training/train_sft.py \
  --model Qwen/Qwen3-14B-Instruct \
  --data data/sft/e1_m1_h1_examples.jsonl \
  --output outputs/sft_qwen3_14b \
  --epochs 2 --max-steps 200

# DeepSeek 14B smoke
python training/train_sft.py \
  --model deepseek-ai/DeepSeek-R1-Distill-Qwen-14B \
  --data data/sft/e1_m1_h1_examples.jsonl \
  --output outputs/sft_deepseek_14b \
  --batch-size 1 --grad-accum 8 --max-steps 20

# DeepSeek 14B fuller run
python training/train_sft.py \
  --model deepseek-ai/DeepSeek-R1-Distill-Qwen-14B \
  --data data/sft/e1_m1_h1_examples.jsonl \
  --output outputs/sft_deepseek_14b \
  --epochs 2 --max-steps 200
```

Use `--assistant-only` only when the model template supports assistant token masks end-to-end.

## 4. Lightning H100 Session 2: Eval SFT

```bash
pip install -e ".[training,plots]"
python eval.py --policy scripted_weak --label baseline --output results/baseline_eval.jsonl
python eval.py --policy hf \
  --label sft \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapter outputs/sft_adapter \
  --output results/sft_eval.jsonl
```

Push `results/*.jsonl` to Hugging Face or copy them back before the Lightning account expires.

## 5. Lightning H100 Session 3: RLVR

```bash
python training/train_rlvr.py \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapter outputs/sft_adapter \
  --examples data/processed/e1_m1_clean.jsonl,data/processed/h1_seed_clean.jsonl \
  --output outputs/rlvr_adapter \
  --strict-json \
  --min-reasoning-steps 2 \
  --rounds 3 \
  --n-samples 8 \
  --max-prompts 128 \
  --stats-file results/runs/rlvr_stats.jsonl \
  --push-to-hub <your-user-or-org>/corp-env-rlvr-adapter
```

This uses Unsloth + TRL RLVR rejection-sampling with the same strict CORP-ENV verifier path. The recommended production path is now SFT then RLVR.

## 6. Final Eval And Plots

```bash
python eval.py --policy hf \
  --label rlvr \
  --model Qwen/Qwen2.5-7B-Instruct \
  --adapter outputs/rlvr_adapter \
  --output results/rlvr_eval.jsonl
python plot_results.py \
  --inputs results/baseline_eval.jsonl results/sft_eval.jsonl results/rlvr_eval.jsonl \
  --output-dir results
```

Commit or upload the resulting PNGs:

- `results/model_comparison.png`
- `results/success_by_task.png`
- `results/invalid_action_rate.png`
- `results/reward_curve.png`

## 7. Hugging Face Space

Use HF credits for the official hosted OpenEnv environment:

```bash
uv run openenv validate
docker build -t corp-env .
```

After pushing the Space, validate it:

```bash
./validate-submission.sh https://<your-space>.hf.space .
```

On Windows, run the validator from WSL or Git Bash.
