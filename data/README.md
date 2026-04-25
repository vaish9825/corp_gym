# Data Layout

Use this layout for the SFT -> RLVR pipeline.

- `raw/imported/`: imported generated scenario examples (E1/M1)
- `raw/synthetic/`: synthetic seed trajectories (for example H1 seeds)
- `processed/verified/`: strict-clean and rejected trajectories plus all-records
- `sft/merged/`: final chat-format SFT training JSONL

## Recommended command

```powershell
uv run python scripts/run_data_pipeline.py --write-legacy-copies
```

This command creates structured outputs and also updates legacy flat paths used
by older scripts.
