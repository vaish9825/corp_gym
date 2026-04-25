"""Create hackathon result plots from CORP-ENV eval JSONL files or run folders."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


STAGE_ORDER = ("baseline", "base", "sft", "grpo", "oracle")
TASK_LABELS = {
    "e1_launch_readiness": "E1 Launch",
    "m1_budget_reallocation": "M1 Budget",
    "h1_acquisition_defence": "H1 Acquisition",
}
COLORS = {
    "baseline": "#8c8c8c",
    "base": "#4C78A8",
    "sft": "#54A24B",
    "grpo": "#F58518",
    "oracle": "#B279A2",
}


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


def stage_family(stage: str) -> str:
    low = stage.lower()
    for family in STAGE_ORDER:
        if family in low:
            return family
    return low


def stage_sort_key(stage: str) -> tuple:
    family = stage_family(stage)
    try:
        family_idx = STAGE_ORDER.index(family)
    except ValueError:
        family_idx = len(STAGE_ORDER)
    return (family_idx, stage)


def task_label(task_id: str) -> str:
    return TASK_LABELS.get(task_id, task_id.replace("_", " "))


def stage_label(stage: str) -> str:
    return stage.replace("_", " ").replace("-", " ")


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


def summary_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[tuple, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row.get("model_stage", "unknown")), str(row.get("task_id", "unknown")))].append(row)

    out: List[Dict[str, Any]] = []
    for (stage, task), vals in sorted(grouped.items(), key=lambda x: (stage_sort_key(x[0][0]), x[0][1])):
        steps = [float(v.get("steps", 0) or 0) for v in vals]
        invalid_rates = [
            float(v.get("invalid_action_count", 0) or 0) / max(float(v.get("steps", 0) or 0), 1.0)
            for v in vals
        ]
        out.append(
            {
                "model_stage": stage,
                "task_id": task,
                "episodes": len(vals),
                "avg_terminal_reward": round(sum(float(v.get("terminal_reward", 0.0)) for v in vals) / len(vals), 6),
                "avg_total_reward": round(sum(float(v.get("total_reward", 0.0)) for v in vals) / len(vals), 6),
                "avg_verifier_pass_rate": round(sum(float(v.get("verifier_pass_rate", 0.0)) for v in vals) / len(vals), 6),
                "success_rate": round(sum(1 for v in vals if v.get("success")) / len(vals), 6),
                "avg_invalid_action_rate": round(sum(invalid_rates) / len(invalid_rates), 6),
                "avg_steps": round(sum(steps) / len(steps), 3),
            }
        )
    return out


def write_summary(rows: List[Dict[str, Any]], output_dir: Path) -> None:
    summary = summary_rows(rows)
    csv_path = output_dir / "comparison_summary.csv"
    md_path = output_dir / "comparison_summary.md"
    if not summary:
        return
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    headers = [
        "Model Stage",
        "Task",
        "Episodes",
        "Terminal Reward",
        "Verifier Pass",
        "Success",
        "Invalid Rate",
        "Avg Steps",
    ]
    lines = [
        "# CORP-ENV Result Comparison",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in summary:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["model_stage"]),
                    task_label(str(row["task_id"])),
                    str(row["episodes"]),
                    f"{row['avg_terminal_reward']:.3f}",
                    f"{row['avg_verifier_pass_rate']:.3f}",
                    f"{row['success_rate']:.3f}",
                    f"{row['avg_invalid_action_rate']:.3f}",
                    f"{row['avg_steps']:.1f}",
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("Generated by `plot_results.py` from eval JSONL files.")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_grouped_bars(
    data: Dict[str, Dict[str, float]],
    title: str,
    ylabel: str,
    output: Path,
    *,
    clamp_unit: bool = True,
) -> None:
    import matplotlib.pyplot as plt

    plt.style.use("seaborn-v0_8-whitegrid")
    stages = sorted(data.keys(), key=stage_sort_key)
    tasks = sorted({task for by_task in data.values() for task in by_task})
    x = list(range(len(tasks)))
    width = 0.8 / max(len(stages), 1)

    fig, ax = plt.subplots(figsize=(max(10, len(tasks) * 2.2), 5.8))
    for idx, stage in enumerate(stages):
        vals = [data[stage].get(task, 0.0) for task in tasks]
        offsets = [pos - 0.4 + width / 2 + idx * width for pos in x]
        family = stage_family(stage)
        bars = ax.bar(
            offsets,
            vals,
            width,
            label=stage_label(stage),
            color=COLORS.get(family),
            edgecolor="white",
            linewidth=0.8,
        )
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + (0.015 if clamp_unit else 0.02),
                    f"{val:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    rotation=0,
                )
    ax.set_title(title, fontsize=15, weight="bold", pad=14)
    ax.set_xlabel("Task")
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels([task_label(t) for t in tasks], rotation=0, ha="center")
    if clamp_unit:
        ax.set_ylim(0, 1.05)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=max(1, min(len(stages), 4)), frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def plot_reward_curve(rows: List[Dict[str, Any]], output: Path) -> None:
    import matplotlib.pyplot as plt

    plt.style.use("seaborn-v0_8-whitegrid")
    grouped: Dict[tuple, List[List[float]]] = defaultdict(list)
    for row in rows:
        trace = [float(x) for x in (row.get("reward_trace") or [])]
        if trace:
            grouped[(str(row.get("model_stage", "model")), str(row.get("task_id", "task")))].append(trace)

    fig, ax = plt.subplots(figsize=(12, 6.5))
    plotted = bool(grouped)
    for (stage, task), traces in sorted(grouped.items(), key=lambda x: (stage_sort_key(x[0][0]), x[0][1])):
        max_len = max(len(t) for t in traces)
        means: List[float] = []
        mins: List[float] = []
        maxs: List[float] = []
        for idx in range(max_len):
            vals = [trace[idx] for trace in traces if idx < len(trace)]
            means.append(sum(vals) / len(vals))
            mins.append(min(vals))
            maxs.append(max(vals))
        xs = list(range(1, max_len + 1))
        family = stage_family(stage)
        label = f"{stage_label(stage)} · {task_label(task)}"
        color = COLORS.get(family)
        ax.plot(xs, means, marker="o", linewidth=2.2, markersize=4, label=label, color=color)
        if len(traces) > 1:
            ax.fill_between(xs, mins, maxs, alpha=0.12, color=color)
    if not plotted:
        ax.text(0.5, 0.5, "No reward traces found", ha="center", va="center")
    ax.axhline(0, color="#666666", linewidth=0.9, alpha=0.5)
    ax.set_title("Episode Reward Curve By Model Stage", fontsize=15, weight="bold", pad=14)
    ax.set_xlabel("Environment step")
    ax.set_ylabel("Step reward")
    ax.spines[["top", "right"]].set_visible(False)
    if plotted:
        ax.legend(fontsize=8, ncol=2, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12))
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
    write_summary(rows, out)
    print(f"Wrote plots to {out}")
    print(f"Wrote summaries to {out / 'comparison_summary.md'} and {out / 'comparison_summary.csv'}")


if __name__ == "__main__":
    main()
