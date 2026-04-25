"""Import Python-generated CORP-ENV examples into verification JSONL.

This is a convenience bridge for files such as:

  data/raw/e1_to_e100_tasks.py
  data/raw/m1_to_m100_tasks.py

The importer looks for either:

1. list/tuple variables containing dictionaries, or
2. generated `CorpTask` subclasses.

For generated task classes, it synthesizes compatible action trajectories for
the current environment tracks (`e1_launch_readiness` and
`m1_budget_reallocation`) while preserving the generated task description as
metadata and prompt text.

Example:
  uv run python scripts/import_generated_examples.py \
    --inputs data/raw/e1_to_e100_tasks.py data/raw/m1_to_m100_tasks.py \
    --output data/raw/e1_m1_examples.jsonl
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
import inspect
import json
from typing import Any, Dict, Iterable, List, Type

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.tasks.base import CorpTask  # noqa: E402
from scripts._trajectory_utils import write_jsonl  # noqa: E402


TASK_HINTS = {
    "e1": "e1_launch_readiness",
    "m1": "m1_budget_reallocation",
    "h1": "h1_acquisition_defence",
}


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def infer_task_id(path: Path, obj: Dict[str, Any]) -> str:
    explicit = obj.get("task_id") or obj.get("task")
    if explicit:
        return str(explicit)
    lowered = path.stem.lower()
    for hint, task_id in TASK_HINTS.items():
        if lowered.startswith(hint) or f"_{hint}_" in lowered:
            return task_id
    return ""


def candidate_examples(module: Any) -> Iterable[Dict[str, Any]]:
    preferred_names = (
        "examples",
        "tasks",
        "trajectories",
        "E1_TASKS",
        "M1_TASKS",
        "E1_EXAMPLES",
        "M1_EXAMPLES",
    )
    seen_ids = set()
    for name in preferred_names + tuple(dir(module)):
        if name.startswith("__") or name in seen_ids:
            continue
        seen_ids.add(name)
        value = getattr(module, name, None)
        if isinstance(value, (list, tuple)) and value and all(isinstance(x, dict) for x in value):
            for item in value:
                yield dict(item)


def generated_task_classes(module: Any) -> Iterable[Type[CorpTask]]:
    for _, value in vars(module).items():
        if not inspect.isclass(value) or value is CorpTask:
            continue
        try:
            if issubclass(value, CorpTask):
                yield value
        except TypeError:
            continue


def is_e1_file(path: Path) -> bool:
    return path.stem.lower().startswith("e1")


def is_m1_file(path: Path) -> bool:
    return path.stem.lower().startswith("m1")


def synthesize_e1_actions(description: str) -> List[Dict[str, Any]]:
    return [
        {
            "action_type": "delegate",
            "agent_id": "qa_engineer",
            "payload": f"Assess launch readiness for this generated scenario: {description}",
        },
        {
            "action_type": "log_reasoning",
            "payload": (
                "Use the QA report as the primary launch gate and decide whether "
                "the release should proceed within the 48 hour window."
            ),
        },
        {
            "action_type": "log_decision",
            "payload": "Finalize based on QA stability, blockers, and launch gate evidence.",
        },
        {"action_type": "finalize", "payload": "NO_GO"},
    ]


def synthesize_m1_actions(description: str) -> List[Dict[str, Any]]:
    final = {
        "phase_1": "Approve a capped GPU allocation for the highest-priority training runs.",
        "phase_2": "Expand spend only after utilization and finance runway checks are reviewed.",
        "guardrail": "Track budget, cost, spend, cash runway, and burn every week.",
        "source_scenario": description[:300],
    }
    return [
        {
            "action_type": "delegate",
            "agent_id": "dev_lead",
            "payload": f"State the engineering requirement and minimum viable plan for: {description}",
        },
        {
            "action_type": "delegate",
            "agent_id": "fpa_manager",
            "payload": f"State finance constraints, budget limits, runway, and spend guardrails for: {description}",
        },
        {
            "action_type": "log_reasoning",
            "payload": (
                "The recommendation must balance engineering urgency against budget, "
                "cost, spend, cash runway, and burn constraints."
            ),
        },
        {
            "action_type": "log_conflict",
            "payload": json.dumps(
                {
                    "id": "c1",
                    "summary": "Engineering requirements exceed what finance should approve immediately.",
                    "source_agents": ["dev_lead", "fpa_manager"],
                }
            ),
        },
        {
            "action_type": "log_resolution",
            "payload": json.dumps(
                {
                    "conflict_id": "c1",
                    "resolution_type": "phased_budget",
                    "text": "Approve a capped phase_1 allocation with finance review before expansion.",
                }
            ),
        },
        {"action_type": "finalize", "payload": json.dumps(final)},
    ]


def examples_from_task_classes(path: Path, module: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for idx, cls in enumerate(generated_task_classes(module), start=1):
        generated_task_id = str(getattr(cls, "task_id", cls.__name__))
        description = str(getattr(cls, "description", generated_task_id))
        if is_e1_file(path):
            task_id = "e1_launch_readiness"
            actions = synthesize_e1_actions(description)
        elif is_m1_file(path):
            task_id = "m1_budget_reallocation"
            actions = synthesize_m1_actions(description)
        else:
            continue
        rows.append(
            {
                "example_id": f"{path.stem}-{idx:03d}",
                "task_id": task_id,
                "source_file": str(path),
                "source_kind": "generated_task_class",
                "source_class": cls.__name__,
                "generated_task_id": generated_task_id,
                "generated_description": description,
                "actions": actions,
            }
        )
    return rows


def import_file(path: Path) -> List[Dict[str, Any]]:
    module = load_module(path)
    rows: List[Dict[str, Any]] = []
    for idx, obj in enumerate(candidate_examples(module), start=1):
        task_id = infer_task_id(path, obj)
        if task_id:
            obj["task_id"] = task_id
        obj.setdefault("example_id", f"{path.stem}-{idx:03d}")
        obj.setdefault("source_file", str(path))
        rows.append(obj)
    if not rows:
        rows.extend(examples_from_task_classes(path, module))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Import generated Python examples to JSONL.")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--output", default="data/raw/e1_m1_examples.jsonl")
    args = parser.parse_args()

    rows: List[Dict[str, Any]] = []
    for input_path in args.inputs:
        path = Path(input_path)
        if not path.exists():
            raise SystemExit(f"Input not found: {path}")
        imported = import_file(path)
        print(f"{path}: imported {len(imported)} examples")
        rows.extend(imported)

    if not rows:
        raise SystemExit(
            "No examples found. Expected a module-level list of dictionaries "
            "or generated CorpTask subclasses."
        )

    write_jsonl(Path(args.output), rows)
    print(f"Wrote {len(rows)} examples to {args.output}")
    print("Next: run scripts/verify_examples.py on the JSONL output.")


if __name__ == "__main__":
    main()
