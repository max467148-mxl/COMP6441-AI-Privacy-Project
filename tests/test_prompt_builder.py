import unittest

from src.data_loader import load_conditions, load_profiles, load_questions
from src.prompt_builder import build_prompt, select_fragments


class PromptBuilderTests(unittest.TestCase):
    def test_no_memory_uses_one_fragment(self):
        profile = load_profiles()[0]
        question = load_questions()[0]
        condition = load_conditions()["no_memory"]
        fragments = select_fragments(profile, condition, question)
        self.assertEqual(len(fragments), 1)

    def test_prompt_contains_required_json_shape(self):
        profile = load_profiles()[0]
        question = load_questions()[0]
        condition = load_conditions()["limited_memory"]
        prompt = build_prompt(profile, "limited_memory", condition, question)
        self.assertIn("Return this exact JSON shape", prompt)
        self.assertIn('"confidence": 0.0', prompt)
        self.assertIn(profile["id"], prompt)


if __name__ == "__main__":
    unittest.main()
