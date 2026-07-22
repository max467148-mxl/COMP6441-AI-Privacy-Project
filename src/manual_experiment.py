import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from .data_loader import load_conditions, load_mitigations, load_profiles, load_questions
from .paths import RESULTS_DIR
from .prompt_builder import build_prompt


MANUAL_DIR = RESULTS_DIR / "manual_prompts"
RESPONSES_DIR = RESULTS_DIR / "manual_responses"
TRACKING_CSV = RESULTS_DIR / "manual_tracking.csv"
MANUAL_JSONL = RESULTS_DIR / "manual_raw_results.jsonl"


def parse_args():
    parser = argparse.ArgumentParser(description="Manual ChatGPT experiment workflow.")
    sub = parser.add_subparsers(dest="command", required=True)

    export = sub.add_parser("export", help="Export prompts for manual ChatGPT testing.")
    export.add_argument("--limit-profiles", type=int, default=3)
    export.add_argument(
        "--design",
        choices=["cartesian", "formal90"],
        default="cartesian",
        help="Use the normal Cartesian export or the 90-prompt formal study design.",
    )
    export.add_argument(
        "--mitigations",
        nargs="+",
        default=["none", "remove_exact_time_place", "memory_expiry", "sensitive_inference_warning"],
        help="Mitigations to include.",
    )
    export.add_argument("--output-dir", default=str(MANUAL_DIR))
    export.add_argument("--responses-dir", default=str(RESPONSES_DIR))
    export.add_argument("--tracking", default=str(TRACKING_CSV))
    export.add_argument("--instructions", default=str(RESULTS_DIR / "manual_instructions.md"))

    collect = sub.add_parser("collect", help="Collect manually saved responses into JSONL.")
    collect.add_argument("--tracking", default=str(TRACKING_CSV))
    collect.add_argument("--responses-dir", default=str(RESPONSES_DIR))
    collect.add_argument("--output", default=str(MANUAL_JSONL))
    collect.add_argument("--model-label", default="ChatGPT manual session")
    return parser.parse_args()


def export_prompts(args):
    RESULTS_DIR.mkdir(exist_ok=True)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    responses_dir = Path(args.responses_dir)
    responses_dir.mkdir(parents=True, exist_ok=True)

    profiles = load_profiles()[: args.limit_profiles]
    questions = load_questions()
    conditions = load_conditions()
    mitigations = load_mitigations()

    if args.design == "formal90":
        if args.limit_profiles != 3:
            raise ValueError("The formal90 design requires exactly 3 profiles.")
        combinations = [(condition_name, "none") for condition_name in conditions]
        combinations.extend(
            ("full_aggregated_memory", mitigation_name)
            for mitigation_name in ["remove_exact_time_place", "sensitive_inference_warning"]
        )
    else:
        combinations = [
            (condition_name, mitigation_name)
            for condition_name in conditions
            for mitigation_name in args.mitigations
        ]

    rows = []
    index = 1
    for profile in profiles:
        for condition_name, mitigation_name in combinations:
            if mitigation_name not in mitigations:
                raise ValueError(f"Unknown mitigation: {mitigation_name}")
            condition = conditions[condition_name]
            for question in questions:
                prompt = build_prompt(profile, condition_name, condition, question, mitigation_name)
                prompt_file = f"{index:03d}_{profile['id']}_{condition_name}_{mitigation_name}_{question['id']}.txt"
                response_file = prompt_file.replace(".txt", "_response.txt")
                (out_dir / prompt_file).write_text(prompt, encoding="utf-8")
                (responses_dir / response_file).write_text(
                    "PASTE CHATGPT RESPONSE HERE. Keep the JSON shape if possible.\n",
                    encoding="utf-8",
                )
                rows.append(
                    {
                        "id": f"{index:03d}",
                        "profile_id": profile["id"],
                        "condition": condition_name,
                        "mitigation": mitigation_name,
                        "question_id": question["id"],
                        "category": question["category"],
                        "prompt_file": str(out_dir / prompt_file),
                        "response_file": str(responses_dir / response_file),
                        "status": "pending",
                        "notes": "",
                    }
                )
                index += 1

    tracking_csv = Path(args.tracking)
    tracking_csv.parent.mkdir(parents=True, exist_ok=True)
    with tracking_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    instructions = Path(args.instructions)
    instructions.parent.mkdir(parents=True, exist_ok=True)
    instructions.write_text(build_instructions(len(rows)), encoding="utf-8")
    print(f"Exported {len(rows)} prompts to {out_dir}")
    print(f"Tracking sheet: {tracking_csv}")
    print(f"Response folder: {responses_dir}")
    print(f"Instructions: {instructions}")


def collect_responses(args):
    tracking = Path(args.tracking)
    responses_dir = Path(args.responses_dir)
    output = Path(args.output)

    rows = []
    with tracking.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    missing = []
    records = []
    for row in rows:
        response_path = Path(row["response_file"])
        if not response_path.exists():
            response_path = responses_dir / Path(row["response_file"]).name
        response_text = response_path.read_text(encoding="utf-8").strip() if response_path.exists() else ""
        if not response_text or response_text.startswith("PASTE CHATGPT RESPONSE HERE"):
            missing.append(row["id"])
            continue

        prompt_text = Path(row["prompt_file"]).read_text(encoding="utf-8")
        records.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "provider": "manual_chatgpt",
                "model": args.model_label,
                "profile_id": row["profile_id"],
                "condition": row["condition"],
                "mitigation": row["mitigation"],
                "question_id": row["question_id"],
                "category": row["category"],
                "prompt": prompt_text,
                "response": response_text,
            }
        )

    output.parent.mkdir(exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Collected {len(records)} responses into {output}")
    if missing:
        print(f"Missing or placeholder responses: {', '.join(missing[:20])}")
        if len(missing) > 20:
            print(f"... and {len(missing) - 20} more")


def build_instructions(prompt_count):
    return f"""# Manual ChatGPT Experiment Instructions

This folder contains {prompt_count} prompts for manual testing with ChatGPT Plus.

## Workflow

1. Open `results/manual_tracking.csv`.
2. Start with prompt `001`.
3. Open the prompt file listed in `prompt_file`.
4. Copy the full prompt into a new ChatGPT message.
5. Copy ChatGPT's full response.
6. Paste it into the matching file in `results/manual_responses/`.
7. Mark the row as complete in the tracking CSV if you want a progress record.
8. Save screenshots for several representative prompts and responses.

## Important

- Do not edit the prompt text before sending it.
- Do not use real personal data.
- Keep responses in JSON shape where possible.
- If ChatGPT refuses or answers in prose, save the full answer anyway.
- Do not use dry-run outputs as final evidence.

## After Responses Are Filled

Run:

```powershell
py -3 -m src.manual_experiment collect
py -3 -m analysis.analyze_results --input results/manual_raw_results.jsonl
```

The analysis script will produce:

- `results/scored_results.csv`
- `results/leakage_by_condition.png`
- `results/leakage_by_category.png`
- `results/mitigation_comparison.png`
- `results/summary.md`
"""


def main():
    args = parse_args()
    if args.command == "export":
        export_prompts(args)
    elif args.command == "collect":
        collect_responses(args)


if __name__ == "__main__":
    main()
