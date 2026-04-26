#!/usr/bin/env bash
set -euxo pipefail

echo "Submitting DeepSeek 14B SFT Eval job..."
GIT_REF="${GIT_REF:-main}"

hf jobs run --namespace Navigam --flavor a10g-large --secrets HF_TOKEN \
  --env HF_HUB_ENABLE_HF_TRANSFER=1 \
  --env TOKENIZERS_PARALLELISM=false \
  --env CORP_STUB_WORKERS=1 \
  --env CORP_DISABLE_LLM_JUDGE=1 \
  huggingface/trl -- sh -c '
    apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/* &&
    git clone --branch main https://github.com/Navigam1108/corp_gym.git /workspace/corp_gym &&
    cd /workspace/corp_gym &&
    pip install -U pip &&
    pip install -U "huggingface_hub>=0.35.0" &&
    pip install -e ".[training,plots]" &&
    python -u eval_genral.py --policy hf \
      --label base-deepseek-r1-14b \
      --model deepseek-ai/DeepSeek-R1-Distill-Qwen-14B \
      --episodes 3 --max-steps 30 &&
    python -u eval_genral.py --policy hf \
      --label sft-deepseek-r1-14b \
      --model deepseek-ai/DeepSeek-R1-Distill-Qwen-14B \
      --adapter Navigam/deepseek-r1-distill-qwen-14b_sft \
      --episodes 3 --max-steps 30 &&
    python -u plot_results.py --inputs results/runs --output-dir results/model_compare_deepseek_r1_14b
  '
