# Lightning AI H100 environment — reproduction artifacts

Files in this folder capture the exact, *working* stack we landed on for
`corp_gym` SFT/RLVR training. Use them to bring up a fresh Lightning AI
Studio (or any Linux H100 with driver >= 570, CUDA 12.8 runtime, Python 3.12).

## Contents

- `setup_lightning_h100.sh` — curated install script (recommended).
  Pins torch 2.7.1 + cu128, xformers 0.0.31.post1, FlashAttention 2.8.0.post2,
  unsloth 2026.4.8, trl 0.24.0, peft 0.19.1, torchao 0.17.0, transformers
  5.5.0, bitsandbytes 0.49.2, datasets 4.3.0, accelerate 1.13.0, plus
  `matplotlib>=3.10` and `numpy<3` for the plotting step.
- `requirements_lightning_h100.txt` — the same pins in a single pip file
  (grouped; read the top comments for the ordered install commands).
- `requirements_frozen.txt` — full `pip freeze` of the exact environment
  (treat as a ground truth, not a reinstall recipe — it does not know about
  `--index-url` or wheel URLs).

## Recommended Lightning Studio environment

- GPU: **1x NVIDIA H100 80GB**
- Runtime: Linux with CUDA **12.8** compatible driver (**>= 570.x**)
- Python: **3.12** (base Lightning image is fine)
- Start from a fresh Studio and run `bash env_artifacts/setup_lightning_h100.sh`

This is the fastest conflict-free path for Unsloth in this repo because it
pins a known-good torch/xformers/flash-attn intersection.

## Tested against

- GPU: **NVIDIA H100 80GB HBM3 (sm_90)**, driver **570.148.08**
- CUDA runtime: **12.8**
- Python: **3.12.11**

## Why these pins (not the defaults from `pyproject.toml`)

The factory Lightning image ships torch 2.5.0 (cu121). That trips a chain of
compat breaks:

1. `torchao >= 0.13` references `torch.int1` (added in torch 2.6).
2. `torchao >= 0.17` references `torch.utils._pytree.register_constant`
   (added in torch 2.7).
3. `peft 0.19.1` requires `torchao > 0.16` if any torchao is importable.
4. `unsloth_zoo 2026.4.9` hard-requires `torchao >= 0.13`.
5. `flash-attn` prebuilt wheels only cover torch 2.4–2.8; 2.9/2.10/2.11 must
   be compiled from source against nvcc (fragile and slow).
6. `xformers` couples tightly to both torch *and* a narrow flash-attn range.

Torch 2.7.1 + xformers 0.0.31.post1 + flash-attn 2.8.0.post2 is the
intersection where all four constraints (`int1`, `register_constant`,
`peft>torchao>0.16`, prebuilt FA2 wheel) are satisfied.

## One-shot bring-up

```bash
# In a fresh Lightning Studio with this repo checked out:
cd corp_gym
bash env_artifacts/setup_lightning_h100.sh
pip install -e .          # picks up project deps without touching the pinned torch stack

# Per-session exports (stick these in ~/.bashrc if you want):
export HF_HUB_ENABLE_HF_TRANSFER=1
export TOKENIZERS_PARALLELISM=false
export TRANSFORMERS_VERBOSITY=warning

huggingface-cli login   # once per container
```

## Resuming training from the previously-trained adapters

The prior run pushed both adapters to `Navigam/*`:

- `Navigam/corp-env-sft-qwen2.5-7b`

You can pull them locally on a new box with:

```bash
huggingface-cli download Navigam/corp-env-sft-qwen2.5-7b --local-dir outputs/sft_adapter
```

Then for a direct 14B RLVR run:

```bash
python training/train_rlvr.py \
  --model Qwen/Qwen3-14B-Instruct \
  --adapter outputs/sft_qwen3_14b \
  --examples data/processed/e1_m1_clean.jsonl,data/processed/h1_seed_clean.jsonl \
  --output outputs/rlvr_qwen3_14b \
  --rounds 3 --n-samples 8 --max-prompts 128 \
  --stats-file results/runs/rlvr_stats.jsonl \
  --push-to-hub <your-user-or-org>/corp-env-rlvr-qwen3-14b
```

## Notes / gotchas

- **First time only on any new box**: `unsloth` writes patched-trainer classes
  into `corp_gym/unsloth_compiled_cache/`. Delete that folder if you ever
  change TRL/unsloth versions to avoid stale compiled patches.
- **Flash-attn fp32 workaround**: this is now **legacy-only** for
  `training/train_grpo.py`. It is disabled by default and can be enabled only
  when needed via `CORP_ENABLE_FA2_BF16_PATCH=1`.
- `training/train_rlvr.py` now runs without this monkey patch on modern stacks.
- **max_prompt_length filter**: both legacy GRPO and RLVR scripts tokenise every
  prompt up-front and drop rows whose chat-template-encoded length exceeds
  `0.9 * max_prompt_length` (long H1 trajectories otherwise produce a causal
  mask / attention mask size mismatch at generation time).
