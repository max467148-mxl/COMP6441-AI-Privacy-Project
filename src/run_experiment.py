import argparse
import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv

from .data_loader import load_conditions, load_mitigations, load_profiles, load_questions
from .model_client import dry_run_response, openai_response
from .paths import RESULTS_DIR
from .prompt_builder import build_prompt


def parse_args():
    parser = argparse.ArgumentParser(description="Run AI privacy leakage experiment.")
    parser.add_argument("--dry-run", action="store_true", help="Use deterministic placeholder responses.")
    parser.add_argument("--provider", choices=["openai"], default="openai")
    parser.add_argument("--model", default=None)
    parser.add_argument("--limit-profiles", type=int, default=None)
    parser.add_argument("--output", default=str(RESULTS_DIR / "raw_results.jsonl"))
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()
    model = args.model or os.environ.get("MODEL", "gpt-4.1-mini")

    profiles = load_profiles()
    if args.limit_profiles:
        profiles = profiles[: args.limit_profiles]

    questions = load_questions()
    conditions = load_conditions()
    mitigations = load_mitigations()

    RESULTS_DIR.mkdir(exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as out:
        for profile in profiles:
            for condition_name, condition in conditions.items():
                for mitigation_name in mitigations.keys():
                    for question in questions:
                        prompt = build_prompt(profile, condition_name, condition, question, mitigation_name)
                        if args.dry_run:
                            response_text = dry_run_response(profile["id"], condition_name, question)
                            provider = "dry_run"
                        else:
                            response_text = openai_response(prompt, model)
                            provider = args.provider

                        record = {
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "provider": provider,
                            "model": model if not args.dry_run else "dry-run-placeholder",
                            "profile_id": profile["id"],
                            "condition": condition_name,
                            "mitigation": mitigation_name,
                            "question_id": question["id"],
                            "category": question["category"],
                            "prompt": prompt,
                            "response": response_text,
                        }
                        out.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote results to {args.output}")


if __name__ == "__main__":
    main()

