# Hugging Face Jobs

This folder contains ready-to-run Hugging Face Jobs specs and launch scripts for:

- `training/train_sft_genral.py` (DeepSeek 14B)
- `training/train_rlvr_genral.py` (DeepSeek 14B)
- `training/train_sft_genral.py` (Nemotron 30B NVFP4)

## Nemotron 30B NVFP4 hardware note

From the model card of `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4`:

- Supported GPU microarchitectures include **H100-80GB** and **A100**.
- Default context in HF config is high (256k), and larger context needs more VRAM.

For adapter SFT with QLoRA in this repo, practical baseline is:

- **Recommended**: 1x `h100` (80GB).
- **Possible**: 1x `a100-large` (80GB) with smaller sequence length and conservative batch.

## Space vs Job

For 30B SFT, use **Hugging Face Jobs**, not Spaces.

- Spaces are better for serving/demo apps and short scripts.
- Long SFT runs with checkpoints and training dependencies are more reliable on Jobs.

## Quick start

Set your token once:

```bash
export HF_TOKEN=hf_xxx
```

Run individual scripts:

```bash
bash hf_jobs/run_sft_deepseek14b.sh
bash hf_jobs/run_rlvr_deepseek14b.sh
bash hf_jobs/run_eval_deepseek14b_base_sft.sh
bash hf_jobs/run_sft_nemotron_nvfp4_30b.sh
```

Or launch with YAML specs:

```bash
hf jobs run hf_jobs/job_sft_deepseek14b.yaml
hf jobs run hf_jobs/job_rlvr_deepseek14b.yaml
hf jobs run hf_jobs/job_eval_deepseek14b_base_sft.yaml
hf jobs run hf_jobs/job_sft_nemotron_nvfp4_30b.yaml
```
