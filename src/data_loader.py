import json
from pathlib import Path

from .paths import DATA_DIR, EXPERIMENTS_DIR, MITIGATIONS_DIR, QUESTIONS_DIR


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_profiles():
    return load_json(DATA_DIR / "profiles.json")


def load_ground_truth():
    return load_json(DATA_DIR / "ground_truth.json")


def load_questions():
    return load_json(QUESTIONS_DIR / "questions.json")


def load_conditions():
    return load_json(EXPERIMENTS_DIR / "conditions.json")


def load_mitigations():
    return load_json(MITIGATIONS_DIR / "mitigations.json")

