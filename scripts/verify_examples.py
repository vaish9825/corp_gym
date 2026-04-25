"""Replay generated examples against the current CORP-ENV implementation.

The script keeps only trajectories that parse as `CorpAction`, run through
`CorpEnvironment`, terminate with `finalize`, and meet task-specific thresholds.

Example:
  uv run python scripts/verify_examples.py \
    --input data/raw/e1_m1_examples.jsonl \
    --clean data/processed/e1_m1_clean.jsonl \
    --rejected data/processed/e1_m1_rejected.jsonl \
    --summary results/example_verification_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts._trajectory_utils import (  # noqa: E402
    extract_actions,
    read_jsonl,
    replay_actions,
    write_jsonl,
)


def verify_one(example: Dict[str, Any], strict_thresholds: bool) -> Dict[str, Any]:
    example_id = str(example.get("example_id") or example.get("id") or "unknown")
    task_id = str(example.get("task_id") or example.get("task") or "")
    if example.get("_load_error"):
        return {
            "example_id": example_id,
            "task_id": task_id,
            "status": "rejected",
            "reject_reason": example["_load_error"],
            "actions": [],
        }
    if not task_id:
        return {
            "example_id": example_id,
            "task_id": task_id,
            "status": "rejected",
            "reject_reason": "missing_task_id",
            "actions": [],
        }
    try:
        actions = extract_actions(example)
    except Exception as exc:
        return {
            "example_id": example_id,
            "task_id": task_id,
            "status": "rejected",
            "reject_reason": f"action_extraction_failed: {exc}",
            "actions": [],
        }
    try:
        result = replay_actions(
            example_id=example_id,
            task_id=task_id,
            actions=actions,
            strict_thresholds=strict_thresholds,
        )
    except Exception as exc:
        return {
            "example_id": example_id,
            "task_id": task_id,
            "status": "rejected",
            "reject_reason": f"replay_failed: {exc}",
            "actions": actions,
        }
    return result.to_record()


def summarize(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_status = Counter(r["status"] for r in records)
    by_reason = Counter(r.get("reject_reason") or "clean" for r in records)
    by_task: Dict[str, Counter] = defaultdict(Counter)
    for row in records:
        by_task[row.get("task_id", "unknown")][row["status"]] += 1
    clean = [r for r in records if r["status"] == "clean"]
    return {
        "total": len(records),
        "by_status": dict(by_status),
        "by_reject_reason": dict(by_reason),
        "by_task": {task: dict(counts) for task, counts in by_task.items()},
        "clean_avg_terminal_reward": (
            round(sum(float(r.get("terminal_reward", 0.0)) for r in clean) / len(clean), 6)
            if clean
            else 0.0
        ),
        "clean_avg_verifier_pass_rate": (
            round(sum(float(r.get("verifier_pass_rate", 0.0)) for r in clean) / len(clean), 6)
            if clean
            else 0.0
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify generated CORP-ENV examples.")
    parser.add_argument("--input", required=True, help="Raw or normalized examples JSONL.")
    parser.add_argument("--clean", default="data/processed/e1_m1_clean.jsonl")
    parser.add_argument("--rejected", default="data/processed/e1_m1_rejected.jsonl")
    parser.add_argument("--all-records", default="results/example_verification_all.jsonl")
    parser.add_argument("--summary", default="results/example_verification_summary.json")
    parser.add_argument(
        "--lenient",
        action="store_true",
        help="Only require replay validity; do not apply task reward/pass thresholds.",
    )
    args = parser.parse_args()

    records = [
        verify_one(example, strict_thresholds=not args.lenient)
        for example in read_jsonl(Path(args.input))
    ]
    clean = [r for r in records if r["status"] == "clean"]
    rejected = [r for r in records if r["status"] != "clean"]

    write_jsonl(Path(args.clean), clean)
    write_jsonl(Path(args.rejected), rejected)
    write_jsonl(Path(args.all_records), records)

    summary = summarize(records)
    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nClean examples: {args.clean}")
    print(f"Rejected examples: {args.rejected}")


if __name__ == "__main__":
    main()
