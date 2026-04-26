#!/usr/bin/env bash
set -euxo pipefail

echo "Submitting Nemotron 30B NVFP4 SFT job..."
echo "Using verbose local shell tracing and verbose remote training logs."
GIT_REF="${GIT_REF:-main}"

hf jobs run --namespace Navigam --flavor h100 --secrets HF_TOKEN --env HF_HUB_ENABLE_HF_TRANSFER=1 --env TOKENIZERS_PARALLELISM=false --env HF_HUB_VERBOSITY=debug --env TRANSFORMERS_VERBOSITY=info --env ACCELERATE_LOG_LEVEL=info --env GIT_REF="${GIT_REF}" huggingface/trl -- sh -c 'set -x; apt-get update; apt-get install -y --no-install-recommends git; rm -rf /var/lib/apt/lists/*; git clone --branch "${GIT_REF}" https://github.com/Navigam1108/corp_gym.git /workspace/corp_gym; cd /workspace/corp_gym; test -f training/train_sft_genral.py || { echo "Missing training/train_sft_genral.py on branch ${GIT_REF}. Push your local changes and rerun."; exit 1; }; pip install -U pip; pip install -e ".[training]"; python -u training/train_sft_genral.py --model nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4 --dataset-repo Navigam/corp-env-data --dataset-file e1_m1_h1_examples.jsonl --output outputs/sft_nemotron_30b_nvfp4 --hf-user Navigam --max-seq-length 4096 --epochs 2 --max-steps 200 --batch-size 1 --grad-accum 16 --target-modules q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj'
