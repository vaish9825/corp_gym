"""Create hackathon result plots from CORP-ENV eval JSONL files or run folders."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


def expand_inputs(inputs: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            paths.extend(sorted(path.rglob("*_eval.jsonl")))
            paths.extend(sorted(path.rglob("eval.jsonl")))
        elif path.exists():
            paths.append(path)
        else:
            matches = sorted(Path().glob(raw))
            paths.extend([m for m in matches if m.is_file()])
    # Preserve order but remove duplicates.
    seen = set()
    out: List[Path] = []
    for path in paths:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            out.append(path)
    return out


def read_rows(paths: Iterable[str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for path in expand_inputs(paths):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    row.setdefault("model_stage", path.stem.replace("_eval", ""))
                    if "run_id" not in row:
                        row["run_id"] = path.parent.name
                    steps = max(float(row.get("steps", 0) or 0), 1.0)
                    row["invalid_action_rate"] = float(row.get("invalid_action_count", 0) or 0) / steps
                    rows.append(row)
    return rows


def grouped_mean(rows: List[Dict[str, Any]], metric: str) -> Dict[str, Dict[str, float]]:
    grouped: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        stage = str(row.get("model_stage", "unknown"))
        task = str(row.get("task_id", "unknown"))
        grouped[stage][task].append(float(row.get(metric, 0.0)))
    return {
        stage: {task: sum(vals) / len(vals) for task, vals in by_task.items()}
        for stage, by_task in grouped.items()
    }


def plot_grouped_bars(
    data: Dict[str, Dict[str, float]],
    title: str,
    ylabel: str,
    output: Path,
    *,
    clamp_unit: bool = True,
) -> None:
    import matplotlib.pyplot as plt

    stages = list(data.keys())
    tasks = sorted({task for by_task in data.values() for task in by_task})
    x = list(range(len(tasks)))
    width = 0.8 / max(len(stages), 1)

    fig, ax = plt.subplots(figsize=(10, 5))
    for idx, stage in enumerate(stages):
        vals = [data[stage].get(task, 0.0) for task in tasks]
        offsets = [pos - 0.4 + width / 2 + idx * width for pos in x]
        ax.bar(offsets, vals, width, label=stage)
    ax.set_title(title)
    ax.set_xlabel("Task")
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(tasks, rotation=20, ha="right")
    if clamp_unit:
        ax.set_ylim(0, 1.05)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def plot_reward_curve(rows: List[Dict[str, Any]], output: Path) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 5))
    plotted = False
    for row in rows:
        trace = row.get("reward_trace") or []
        if not trace:
            continue
        label = f"{row.get('model_stage', 'model')}:{row.get('task_id', 'task')}:{row.get('episode_index', 0)}"
        ax.plot(list(range(1, len(trace) + 1)), trace, alpha=0.45, label=label)
        plotted = True
    if not plotted:
        ax.text(0.5, 0.5, "No reward traces found", ha="center", va="center")
    ax.set_title("Episode Reward Traces")
    ax.set_xlabel("Environment step")
    ax.set_ylabel("Step reward")
    if plotted:
        ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot CORP-ENV eval results.")
    parser.add_argument("--inputs", nargs="+", required=True, help="Eval JSONL files, folders, or glob patterns.")
    parser.add_argument("--output-dir", default="results")
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = read_rows(args.inputs)
    if not rows:
        raise SystemExit("No rows found in input files.")

    plot_grouped_bars(
        grouped_mean(rows, "terminal_reward"),
        "Average Terminal Reward By Model Stage",
        "Terminal reward",
        out / "model_comparison.png",
        clamp_unit=True,
    )
    plot_grouped_bars(
        grouped_mean(rows, "verifier_pass_rate"),
        "Verifier Pass Rate By Task",
        "Verifier pass rate",
        out / "success_by_task.png",
        clamp_unit=True,
    )
    plot_grouped_bars(
        grouped_mean(rows, "invalid_action_rate"),
        "Invalid Action Rate By Task",
        "Invalid actions / environment step",
        out / "invalid_action_rate.png",
        clamp_unit=True,
    )
    plot_reward_curve(rows, out / "reward_curve.png")
    print(f"Wrote plots to {out}")


if __name__ == "__main__":
    main()
