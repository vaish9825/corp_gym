"""Generate small verifier-friendly seed trajectories for CORP-ENV.

This is not meant to replace your generated E1/M1 examples. Use it to create
missing coverage, especially H1 seeds, then pass the output through
`scripts/verify_examples.py` before SFT.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts._trajectory_utils import DEFAULT_TASKS, oracle_actions, write_jsonl  # noqa: E402


def build_examples(tasks: List[str], per_task: int) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for task_id in tasks:
        for idx in range(per_task):
            rows.append(
                {
                    "example_id": f"seed-{task_id}-{idx:03d}",
                    "task_id": task_id,
                    "source": "scripted_seed",
                    "actions": oracle_actions(task_id, idx),
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CORP-ENV seed trajectories.")
    parser.add_argument("--tasks", default="h1_acquisition_defence")
    parser.add_argument("--per-task", type=int, default=8)
    parser.add_argument("--output", default="data/raw/h1_seed.jsonl")
    args = parser.parse_args()

    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(DEFAULT_TASKS)
    rows = build_examples(tasks, args.per_task)
    write_jsonl(Path(args.output), rows)
    print(f"Wrote {len(rows)} seed trajectories to {args.output}")
    print("Next: run scripts/verify_examples.py on this file before using it for SFT.")


if __name__ == "__main__":
    main()
