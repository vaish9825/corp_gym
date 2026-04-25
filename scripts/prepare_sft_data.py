"""Convert verified CORP-ENV trajectories into chat-format SFT JSONL.

Input should usually be `data/processed/e1_m1_clean.jsonl` from
`scripts/verify_examples.py`. Each output row is compatible with TRL-style chat
SFT datasets:

  {"task_id": "...", "example_id": "...", "messages": [...]}
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts._trajectory_utils import (  # noqa: E402
    actions_to_sft_messages,
    extract_actions,
    read_jsonl,
    write_jsonl,
)


def convert_example(example: Dict[str, Any], min_pass_rate: float) -> Dict[str, Any] | None:
    if example.get("status") and example.get("status") != "clean":
        return None
    pass_rate = float(example.get("verifier_pass_rate", 1.0))
    if pass_rate < min_pass_rate:
        return None
    task_id = str(example.get("task_id") or example.get("task") or "")
    if not task_id:
        return None
    actions = extract_actions(example)
    messages = actions_to_sft_messages(task_id, actions)
    return {
        "example_id": str(example.get("example_id") or example.get("id") or "unknown"),
        "task_id": task_id,
        "messages": messages,
        "num_actions": len(actions),
        "terminal_reward": example.get("terminal_reward"),
        "verifier_pass_rate": example.get("verifier_pass_rate"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare chat SFT data from verified examples.")
    parser.add_argument("--input", default="data/processed/e1_m1_clean.jsonl")
    parser.add_argument("--output", default="data/sft/e1_m1_examples.jsonl")
    parser.add_argument("--min-pass-rate", type=float, default=0.80)
    args = parser.parse_args()

    rows: List[Dict[str, Any]] = []
    skipped = 0
    for example in read_jsonl(Path(args.input)):
        try:
            row = convert_example(example, args.min_pass_rate)
        except Exception as exc:
            skipped += 1
            print(f"skip {example.get('example_id', 'unknown')}: {exc}")
            continue
        if row is None:
            skipped += 1
            continue
        rows.append(row)

    write_jsonl(Path(args.output), rows)
    print(f"Wrote {len(rows)} SFT conversations to {args.output}; skipped {skipped}.")


if __name__ == "__main__":
    main()
