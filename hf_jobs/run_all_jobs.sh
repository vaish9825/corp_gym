#!/usr/bin/env bash
set -euxo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${DIR}/run_sft_deepseek14b.sh"
bash "${DIR}/run_rlvr_deepseek14b.sh"
bash "${DIR}/run_sft_nemotron_nvfp4_30b.sh"
