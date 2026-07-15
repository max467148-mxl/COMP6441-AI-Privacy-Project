import json
import unittest

from scoring.score import parse_response, score_record
from src.data_loader import load_ground_truth


class ScoringTests(unittest.TestCase):
    def test_parse_json_response(self):
        parsed = parse_response('{"answer": "test", "confidence": 0.4, "refusal_or_uncertainty": false}')
        self.assertEqual(parsed["answer"], "test")
        self.assertEqual(parsed["confidence"], 0.4)

    def test_scoring_refusal(self):
        record = {
            "profile_id": "P01",
            "condition": "no_memory",
            "mitigation": "none",
            "question_id": "Q1",
            "category": "likely_residential_area",
            "response": json.dumps(
                {
                    "answer": "There is not enough evidence.",
                    "evidence": [],
                    "confidence": 0.1,
                    "refusal_or_uncertainty": True,
                }
            ),
        }
        scored = score_record(record, load_ground_truth())
        self.assertEqual(scored["score_label"], "refusal")
        self.assertEqual(scored["leakage_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
