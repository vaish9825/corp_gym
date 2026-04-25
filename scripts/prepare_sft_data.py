"""Convert verified CORP-ENV trajectories into chat-format SFT JSONL.

Pass one or more processed JSONLs (e.g. `e1_m1_clean` + `h1_seed_clean`) from
`scripts/verify_examples.py`. Each output row is TRL-style chat SFT data:

  {"task_id": "...", "example_id": "...", "messages": [...]}
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts._trajectory_utils import (  # noqa: E402
    actions_to_sft_messages,
    deliberation_features,
    extract_actions,
    read_jsonl,
    validate_stepwise_deliberation,
    write_jsonl,
)


def convert_example(
    example: Dict[str, Any],
    min_pass_rate: float,
    min_reasoning_steps: int,
    min_conflict_steps: int,
    min_resolution_steps: int,
    require_stepwise_deliberation: bool,
) -> Dict[str, Any] | None:
    if example.get("status") and example.get("status") != "clean":
        return None
    pass_rate = float(example.get("verifier_pass_rate", 1.0))
    if pass_rate < min_pass_rate:
        return None
    task_id = str(example.get("task_id") or example.get("task") or "")
    if not task_id:
        return None
    actions = extract_actions(example)
    if require_stepwise_deliberation:
        if validate_stepwise_deliberation(task_id, actions):
            return None
    features = deliberation_features(actions)
    if int(features["reasoning_steps"]) < min_reasoning_steps:
        return None
    if int(features["conflict_steps"]) < min_conflict_steps:
        return None
    if int(features["resolution_steps"]) < min_resolution_steps:
        return None
    messages = actions_to_sft_messages(task_id, actions)
    return {
        "example_id": str(example.get("example_id") or example.get("id") or "unknown"),
        "task_id": task_id,
        "messages": messages,
        "num_actions": len(actions),
        "terminal_reward": example.get("terminal_reward"),
        "verifier_pass_rate": example.get("verifier_pass_rate"),
        "reasoning_steps": int(features["reasoning_steps"]),
        "conflict_steps": int(features["conflict_steps"]),
        "resolution_steps": int(features["resolution_steps"]),
        "phase_progression_ok": bool(features["phase_progression_ok"]),
    }


def _parse_input_paths(raw: List[str]) -> List[Path]:
    """Expand comma-separated entries and return unique ordered paths."""
    out: List[Path] = []
    for part in raw:
        for p in part.split(","):
            p = p.strip()
            if p:
                out.append(Path(p))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare chat SFT data from verified examples.")
    default_inputs = (
        "data/processed/e1_m1_clean.jsonl,data/processed/h1_seed_clean.jsonl"
    )
    parser.add_argument(
        "--input",
        dest="inputs",
        action="append",
        default=None,
        metavar="PATH",
        help=(
            "Processed JSONL (repeat flag or use commas). "
            f"Default: {default_inputs}"
        ),
    )
    parser.add_argument("--output", default="data/sft/e1_m1_h1_examples.jsonl")
    parser.add_argument("--min-pass-rate", type=float, default=0.80)
    parser.add_argument("--min-reasoning-steps", type=int, default=1)
    parser.add_argument("--min-conflict-steps", type=int, default=0)
    parser.add_argument("--min-resolution-steps", type=int, default=0)
    parser.add_argument(
        "--require-stepwise-deliberation",
        action="store_true",
        help="Require task-specific SWD step-wise deliberation checks from verification utilities.",
    )
    parser.add_argument(
        "--max-per-task",
        type=int,
        default=0,
        help="Optional cap for kept SFT rows per task (0 = unlimited).",
    )
    args = parser.parse_args()
    raw_inputs = list(args.inputs) if args.inputs else [default_inputs]
    input_paths = _parse_input_paths(raw_inputs)

    rows: List[Dict[str, Any]] = []
    by_task_kept: Dict[str, int] = defaultdict(int)
    seen_ids: set[str] = set()
    skipped = 0
    for path in input_paths:
        if not path.is_file():
            print(f"warning: input missing, skip: {path}", file=sys.stderr)
            continue
        for example in read_jsonl(path):
            eid = str(example.get("example_id") or example.get("id") or "")
            if eid and eid in seen_ids:
                skipped += 1
                continue
            try:
                row = convert_example(
                    example,
                    args.min_pass_rate,
                    args.min_reasoning_steps,
                    args.min_conflict_steps,
                    args.min_resolution_steps,
                    args.require_stepwise_deliberation,
                )
            except Exception as exc:
                skipped += 1
                print(f"skip {example.get('example_id', 'unknown')}: {exc}")
                continue
            if row is None:
                skipped += 1
                continue
            if args.max_per_task > 0 and by_task_kept[row["task_id"]] >= args.max_per_task:
                skipped += 1
                continue
            rows.append(row)
            by_task_kept[row["task_id"]] += 1
            eid2 = str(row.get("example_id") or "unknown")
            if eid2 and eid2 != "unknown":
                seen_ids.add(eid2)

    write_jsonl(Path(args.output), rows)
    print(f"Wrote {len(rows)} SFT conversations to {args.output}; skipped {skipped}.")


if __name__ == "__main__":
    main()
