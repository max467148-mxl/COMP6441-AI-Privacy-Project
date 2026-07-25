import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKING = ROOT / "results" / "formal_tracking.csv"

CATEGORY_TERMS = {
    "Q1": ("live", "residen", "home", "area", "suburb", "rental", "housing", "location"),
    "Q2": ("away", "home", "time", "morning", "evening", "night", "afternoon", "weekday", "weekend"),
    "Q3": ("student", "study", "work", "occupation", "job", "employ", "role", "course"),
    "Q4": ("financial", "income", "budget", "cost", "rent", "mortgage", "wealth", "money", "spend"),
    "Q5": ("link", "combin", "together", "profile", "activities", "records", "pattern"),
}


def main():
    rows = list(csv.DictReader(TRACKING.open(encoding="utf-8-sig")))
    issues = []
    hashes = defaultdict(list)

    if len(rows) != 90:
        issues.append(f"Expected 90 tracking rows; found {len(rows)}.")
    if len({row["id"] for row in rows}) != len(rows):
        issues.append("Tracking IDs are not unique.")

    for row in rows:
        prompt_path = ROOT / row["prompt_file"]
        response_path = ROOT / row["response_file"]
        expected_stem = (
            f"{row['id']}_{row['profile_id']}_{row['condition']}_"
            f"{row['mitigation']}_{row['question_id']}"
        )

        if prompt_path.name != f"{expected_stem}.txt":
            issues.append(f"{row['id']}: prompt filename does not match tracking metadata.")
        if response_path.name != f"{expected_stem}_response.txt":
            issues.append(f"{row['id']}: response filename does not match tracking metadata.")
        if not prompt_path.exists() or not response_path.exists():
            issues.append(f"{row['id']}: prompt or response file is missing.")
            continue

        response_bytes = response_path.read_bytes()
        hashes[hashlib.sha256(response_bytes).hexdigest()].append(row["id"])
        try:
            response = json.loads(response_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"{row['id']}: response JSON failed to parse: {exc}.")
            continue

        required = {"answer", "evidence", "confidence", "refusal_or_uncertainty"}
        if not required.issubset(response):
            issues.append(f"{row['id']}: response is missing required fields.")
            continue

        question_match = re.fullmatch(r"Q[1-5]", row["question_id"])
        if not question_match:
            issues.append(f"{row['id']}: invalid question ID.")
            continue
        answer = str(response["answer"]).lower()
        if not any(term in answer for term in CATEGORY_TERMS[row["question_id"]]):
            issues.append(f"{row['id']}: answer needs manual category review.")

    duplicate_groups = [ids for ids in hashes.values() if len(ids) > 1]
    for ids in duplicate_groups:
        issues.append(f"Exact duplicate response content: {', '.join(ids)}.")

    print(f"Tracking rows checked: {len(rows)}")
    print(f"Response files parsed: {len(rows) - sum('failed to parse' in item for item in issues)}")
    print(f"Exact duplicate groups: {len(duplicate_groups)}")
    print(f"Audit issues: {len(issues)}")
    for issue in issues:
        print(f"- {issue}")

    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
