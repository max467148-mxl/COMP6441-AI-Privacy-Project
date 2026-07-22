import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

from scoring.score import score_record
from src.data_loader import load_ground_truth
from src.paths import RESULTS_DIR


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze privacy leakage results.")
    parser.add_argument("--input", default=str(RESULTS_DIR / "raw_results.jsonl"))
    parser.add_argument("--output-dir", default=str(RESULTS_DIR))
    return parser.parse_args()


def load_records(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def mean(values):
    return sum(values) / len(values) if values else 0


def group_mean(rows, key):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(float(row["leakage_score"]))
    return {name: mean(scores) for name, scores in grouped.items()}


def save_csv(rows, path):
    fieldnames = [
        "profile_id",
        "condition",
        "mitigation",
        "question_id",
        "category",
        "confidence",
        "score_label",
        "leakage_score",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_group_metrics(rows, group_key, path):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[group_key]].append(row)

    metric_rows = []
    for name, group in grouped.items():
        metric_rows.append(
            {
                group_key: name,
                "n": len(group),
                "mean_leakage_score": mean([float(row["leakage_score"]) for row in group]),
                "mean_confidence": mean([float(row["confidence"]) for row in group]),
                "refusal_or_uncertainty_rate": mean(
                    [row["score_label"] in {"refusal", "uncertainty"} for row in group]
                ),
            }
        )

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metric_rows[0].keys())
        writer.writeheader()
        writer.writerows(metric_rows)


def bar_chart(mapping, title, ylabel, output_path):
    labels = list(mapping.keys())
    values = [mapping[label] for label in labels]
    colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]
    plt.figure(figsize=(9, 5))
    bars = plt.bar(labels, values, color=colors[: len(labels)])
    plt.title(title)
    plt.ylabel(ylabel)
    plt.ylim(0, 1)
    plt.xticks(rotation=25, ha="right")
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.025, f"{value:.2f}", ha="center")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def mitigation_comparison(rows, output_path):
    grouped = defaultdict(list)
    for row in rows:
        if row["condition"] != "full_aggregated_memory":
            continue
        key = row["mitigation"]
        grouped[key].append(float(row["leakage_score"]))
    mapping = {key: mean(value) for key, value in grouped.items()}
    bar_chart(mapping, "Leakage Score by Mitigation", "Mean leakage score", output_path)


def write_summary(rows, output_path, source_path):
    baseline_rows = [row for row in rows if row["mitigation"] == "none"]
    full_context_rows = [row for row in rows if row["condition"] == "full_aggregated_memory"]
    by_condition = group_mean(baseline_rows, "condition")
    by_category = group_mean(baseline_rows, "category")
    by_mitigation = group_mean(full_context_rows, "mitigation")
    lines = ["# Experiment Summary", ""]
    lines.append("## Leakage by Condition")
    for key, value in by_condition.items():
        lines.append(f"- {key}: {value:.2f}")
    lines.append("")
    lines.append("## Leakage by Category")
    for key, value in by_category.items():
        lines.append(f"- {key}: {value:.2f}")
    lines.append("")
    lines.append("## Leakage by Mitigation (Full Aggregated Context Only)")
    for key, value in by_mitigation.items():
        lines.append(f"- {key}: {value:.2f}")
    lines.append("")
    source_name = Path(source_path).name
    if source_name.startswith("formal_"):
        lines.append(
            "These are formal controlled-run results. Automated leakage scores remain "
            "subject to the planned human validation before final reporting."
        )
    elif source_name.startswith("manual_"):
        lines.append(
            "These are preliminary manual pilot results. Treat them as exploratory until "
            "the planned profiles, repetitions, mitigations, and human validation are complete."
        )
    else:
        lines.append("Dry-run results are pipeline checks only. Do not use them as final report evidence.")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    args = parse_args()
    records = load_records(args.input)
    ground_truth = load_ground_truth()
    scored = [score_record(record, ground_truth) for record in records]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    save_csv(scored, output_dir / "scored_results.csv")
    baseline_scored = [row for row in scored if row["mitigation"] == "none"]
    full_context_scored = [row for row in scored if row["condition"] == "full_aggregated_memory"]
    save_group_metrics(baseline_scored, "condition", output_dir / "condition_metrics.csv")
    save_group_metrics(full_context_scored, "mitigation", output_dir / "mitigation_metrics.csv")
    bar_chart(
        group_mean(baseline_scored, "condition"),
        "Leakage Score by Context Condition",
        "Mean leakage score",
        output_dir / "leakage_by_condition.png",
    )
    bar_chart(
        group_mean(baseline_scored, "category"),
        "Leakage Score by Attribute Category",
        "Mean leakage score",
        output_dir / "leakage_by_category.png",
    )
    mitigation_comparison(scored, output_dir / "mitigation_comparison.png")
    write_summary(scored, output_dir / "summary.md", args.input)
    print(f"Analyzed {len(scored)} records")


if __name__ == "__main__":
    main()
