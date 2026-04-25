#!/usr/bin/env bash
# Reproduce the torch 2.7.1 + cu128 stack that worked on the previous
# Lightning AI H100 container for corp_gym SFT/GRPO/RLVR training.
#
# Target environment:
#   - NVIDIA H100 80GB HBM3 (sm_90), driver >= 570.x, CUDA runtime 12.8
#   - Python 3.12 (Miniconda cloudspace env is fine)
#
# Usage (from a fresh Lightning Studio, inside the corp_gym repo):
#   bash env_artifacts/setup_lightning_h100.sh
#
# If you already have this repo editable-installed, re-run its `pip install -e .`
# *after* this script so the torch/xformers/FA versions stick.

set -euo pipefail

log() { printf '\n\033[1;32m[setup]\033[0m %s\n' "$*"; }

PY_BIN="${PY_BIN:-python}"

log "python / torch versions before"
$PY_BIN --version
$PY_BIN -c "import torch; print('torch', torch.__version__)" 2>/dev/null || true

log "install hf_transfer for fast HF downloads"
pip install -q hf_transfer

log "pin torch 2.7.1 + torchvision 0.22.1 + torchaudio 2.7.1 (cu128 wheels)"
pip install -q --upgrade \
    torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1 \
    --index-url https://download.pytorch.org/whl/cu128

log "xformers matching torch 2.7 (force-reinstall to avoid stale torch deps)"
pip install -q --force-reinstall --no-deps xformers==0.0.31.post1

log "flash-attn 2.8.0.post2 wheel for cu12 + torch2.7 + cp312"
pip uninstall -y -q flash-attn 2>/dev/null || true
pip install -q --no-build-isolation \
    "https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.0.post2/flash_attn-2.8.0.post2+cu12torch2.7cxx11abiFALSE-cp312-cp312-linux_x86_64.whl"

log "training stack (unsloth/trl/peft/bitsandbytes/datasets/accelerate/transformers)"
pip install -q --upgrade \
    "unsloth==2026.4.8" \
    "unsloth_zoo>=2026.4.9" \
    "trl==0.24.0" \
    "peft==0.19.1" \
    "bitsandbytes==0.49.2" \
    "datasets==4.3.0" \
    "accelerate==1.13.0" \
    "transformers==5.5.0" \
    "torchao==0.17.0"

log "plotting stack (matplotlib needs upgrade for numpy 2.x compat)"
pip install -q --upgrade "matplotlib>=3.10" "numpy<3"

log "sanity check"
$PY_BIN - <<'PY'
import torch
print("torch", torch.__version__, "cuda", torch.version.cuda, "avail", torch.cuda.is_available())
print("register_constant:", hasattr(torch.utils._pytree, "register_constant"))
print("int1:", hasattr(torch, "int1"))
import flash_attn; print("flash_attn", flash_attn.__version__)
import xformers, xformers.ops; print("xformers", xformers.__version__, "ops OK")
import torchao; print("torchao", torchao.__version__)
from unsloth import FastLanguageModel  # noqa
from trl import SFTConfig, GRPOConfig   # noqa
print("unsloth + trl OK")
PY

log "done. Export env vars in your shell (rc file or per-session):"
cat <<'EOF'

  export HF_HUB_ENABLE_HF_TRANSFER=1
  export CORP_STUB_WORKERS=1
  export CORP_DISABLE_LLM_JUDGE=1
  export TOKENIZERS_PARALLELISM=false
  export TRANSFORMERS_VERBOSITY=warning

  # Auth once per container:
  #   huggingface-cli login
EOF
