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


def bar_chart(mapping, title, ylabel, output_path):
    labels = list(mapping.keys())
    values = [mapping[label] for label in labels]
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color="#2563eb")
    plt.title(title)
    plt.ylabel(ylabel)
    plt.ylim(0, 1)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def mitigation_comparison(rows, output_path):
    grouped = defaultdict(list)
    for row in rows:
        key = row["mitigation"]
        grouped[key].append(float(row["leakage_score"]))
    mapping = {key: mean(value) for key, value in grouped.items()}
    bar_chart(mapping, "Leakage Score by Mitigation", "Mean leakage score", output_path)


def write_summary(rows, output_path):
    by_condition = group_mean(rows, "condition")
    by_category = group_mean(rows, "category")
    lines = ["# Experiment Summary", ""]
    lines.append("## Leakage by Condition")
    for key, value in by_condition.items():
        lines.append(f"- {key}: {value:.2f}")
    lines.append("")
    lines.append("## Leakage by Category")
    for key, value in by_category.items():
        lines.append(f"- {key}: {value:.2f}")
    lines.append("")
    lines.append("Dry-run results are pipeline checks only. Do not use them as final report evidence.")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    args = parse_args()
    records = load_records(args.input)
    ground_truth = load_ground_truth()
    scored = [score_record(record, ground_truth) for record in records]

    RESULTS_DIR.mkdir(exist_ok=True)
    save_csv(scored, RESULTS_DIR / "scored_results.csv")
    bar_chart(
        group_mean(scored, "condition"),
        "Leakage Score by Context Condition",
        "Mean leakage score",
        RESULTS_DIR / "leakage_by_condition.png",
    )
    bar_chart(
        group_mean(scored, "category"),
        "Leakage Score by Attribute Category",
        "Mean leakage score",
        RESULTS_DIR / "leakage_by_category.png",
    )
    mitigation_comparison(scored, RESULTS_DIR / "mitigation_comparison.png")
    write_summary(scored, RESULTS_DIR / "summary.md")
    print(f"Analyzed {len(scored)} records")


if __name__ == "__main__":
    main()

