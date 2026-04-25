"""Run a structured CORP-ENV data pipeline for SFT -> RLVR.

This script standardizes where artifacts are written so data prep stays tidy:

- raw/imported: imported E1/M1 generated examples
- raw/synthetic: synthetic seed traces (H1 by default)
- processed/verified: clean/rejected outputs after strict verification
- sft/merged: final SFT chat JSONL

It wraps existing scripts and keeps compatibility by optionally writing the
legacy flat output files as copies.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], *, use_uv: bool) -> None:
    final_cmd = (["uv", "run"] + cmd) if use_uv else cmd
    print("+", " ".join(final_cmd))
    subprocess.run(final_cmd, check=True, cwd=ROOT)


def ensure_dirs(paths: list[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def copy_if_exists(src: Path, dst: Path) -> None:
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main() -> None:
    parser = argparse.ArgumentParser(description="Structured data pipeline for CORP-ENV.")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--use-uv",
        action="store_true",
        help="Run each pipeline stage with `uv run` to use the project environment.",
    )
    parser.add_argument("--h1-per-task", type=int, default=24)
    parser.add_argument("--h1-variant-stride", type=int, default=2)
    parser.add_argument("--min-pass-rate", type=float, default=0.85)
    parser.add_argument("--min-reasoning-steps", type=int, default=1)
    parser.add_argument("--min-conflict-steps", type=int, default=0)
    parser.add_argument("--min-resolution-steps", type=int, default=0)
    parser.add_argument("--max-per-task", type=int, default=0)
    parser.add_argument(
        "--write-legacy-copies",
        action="store_true",
        help="Also copy outputs to legacy flat paths for backward compatibility.",
    )
    args = parser.parse_args()

    data = ROOT / "data"
    raw_imported = data / "raw" / "imported"
    raw_synthetic = data / "raw" / "synthetic"
    processed_verified = data / "processed" / "verified"
    sft_merged = data / "sft" / "merged"
    summaries = ROOT / "results" / "data_pipeline"
    ensure_dirs([raw_imported, raw_synthetic, processed_verified, sft_merged, summaries])

    e1m1_raw = raw_imported / "e1_m1_examples.jsonl"
    h1_raw = raw_synthetic / "h1_seed.jsonl"
    e1m1_clean = processed_verified / "e1_m1_clean.jsonl"
    e1m1_rejected = processed_verified / "e1_m1_rejected.jsonl"
    h1_clean = processed_verified / "h1_seed_clean.jsonl"
    h1_rejected = processed_verified / "h1_seed_rejected.jsonl"
    sft_out = sft_merged / "e1_m1_h1_examples.jsonl"

    run(
        [
            args.python,
            "scripts/import_generated_examples.py",
            "--inputs",
            "data/raw/e1_to_e100_tasks.py",
            "data/raw/m1_to_m100_tasks.py",
            "--output",
            str(e1m1_raw),
        ],
        use_uv=args.use_uv,
    )
    run(
        [
            args.python,
            "scripts/generate_sft_data.py",
            "--tasks",
            "h1_acquisition_defence",
            "--per-task",
            str(args.h1_per_task),
            "--variant-stride",
            str(args.h1_variant_stride),
            "--output",
            str(h1_raw),
        ],
        use_uv=args.use_uv,
    )
    run(
        [
            args.python,
            "scripts/verify_examples.py",
            "--input",
            str(e1m1_raw),
            "--clean",
            str(e1m1_clean),
            "--rejected",
            str(e1m1_rejected),
            "--all-records",
            str(processed_verified / "e1_m1_all_records.jsonl"),
            "--summary",
            str(summaries / "e1_m1_summary.json"),
            "--strict-json",
            "--require-stepwise-deliberation",
        ],
        use_uv=args.use_uv,
    )
    run(
        [
            args.python,
            "scripts/verify_examples.py",
            "--input",
            str(h1_raw),
            "--clean",
            str(h1_clean),
            "--rejected",
            str(h1_rejected),
            "--all-records",
            str(processed_verified / "h1_seed_all_records.jsonl"),
            "--summary",
            str(summaries / "h1_seed_summary.json"),
            "--strict-json",
            "--require-stepwise-deliberation",
        ],
        use_uv=args.use_uv,
    )
    prep_cmd = [
        args.python,
        "scripts/prepare_sft_data.py",
        "--input",
        str(e1m1_clean),
        "--input",
        str(h1_clean),
        "--output",
        str(sft_out),
        "--min-pass-rate",
        str(args.min_pass_rate),
        "--min-reasoning-steps",
        str(args.min_reasoning_steps),
        "--min-conflict-steps",
        str(args.min_conflict_steps),
        "--min-resolution-steps",
        str(args.min_resolution_steps),
        "--require-stepwise-deliberation",
    ]
    if args.max_per_task > 0:
        prep_cmd.extend(["--max-per-task", str(args.max_per_task)])
    run(prep_cmd, use_uv=args.use_uv)

    if args.write_legacy_copies:
        copy_if_exists(e1m1_raw, data / "raw" / "e1_m1_examples.jsonl")
        copy_if_exists(h1_raw, data / "raw" / "h1_seed.jsonl")
        copy_if_exists(e1m1_clean, data / "processed" / "e1_m1_clean.jsonl")
        copy_if_exists(e1m1_rejected, data / "processed" / "e1_m1_rejected.jsonl")
        copy_if_exists(h1_clean, data / "processed" / "h1_seed_clean.jsonl")
        copy_if_exists(h1_rejected, data / "processed" / "h1_seed_rejected.jsonl")
        copy_if_exists(sft_out, data / "sft" / "e1_m1_h1_examples.jsonl")

    print("\nStructured data pipeline complete.")
    print(f"SFT dataset: {sft_out}")
    print(f"Summaries:   {summaries}")


if __name__ == "__main__":
    main()
