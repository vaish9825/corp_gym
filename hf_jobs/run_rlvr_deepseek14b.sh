#!/usr/bin/env bash
set -euxo pipefail

echo "Submitting DeepSeek 14B RLVR job..."
echo "Using verbose local shell tracing and verbose remote training logs."
GIT_REF="${GIT_REF:-main}"

hf jobs run --namespace Navigam --flavor a100-large --secrets HF_TOKEN --env HF_HUB_ENABLE_HF_TRANSFER=1 --env TOKENIZERS_PARALLELISM=false --env HF_HUB_VERBOSITY=debug --env TRANSFORMERS_VERBOSITY=info --env ACCELERATE_LOG_LEVEL=info --env GIT_REF="${GIT_REF}" huggingface/trl -- sh -c 'set -x; apt-get update; apt-get install -y --no-install-recommends git; rm -rf /var/lib/apt/lists/*; git clone --branch "${GIT_REF}" https://github.com/Navigam1108/corp_gym.git /workspace/corp_gym; cd /workspace/corp_gym; test -f training/train_rlvr_genral.py || { echo "Missing training/train_rlvr_genral.py on branch ${GIT_REF}. Push your local changes and rerun."; exit 1; }; pip install -U pip; pip install -e ".[training]"; python -u training/train_rlvr_genral.py --model deepseek-ai/DeepSeek-R1-Distill-Qwen-14B --adapter outputs/sft_deepseek_14b --dataset-repo Navigam/corp-env-data --examples-files e1_m1_clean.jsonl,h1_seed_clean.jsonl --output outputs/rlvr_deepseek_14b --hf-user Navigam --strict-json --rounds 3 --n-samples 8 --max-prompts 128 --stats-file results/runs/rlvr_deepseek_14b.jsonl'
