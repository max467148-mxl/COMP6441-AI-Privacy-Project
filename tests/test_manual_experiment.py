import tempfile
import unittest
from pathlib import Path

from types import SimpleNamespace
from unittest.mock import patch

from src.manual_experiment import build_instructions, export_prompts


class ManualExperimentTests(unittest.TestCase):
    def test_instructions_include_collect_command(self):
        instructions = build_instructions(10)
        self.assertIn("py -3 -m src.manual_experiment collect", instructions)
        self.assertIn("10 prompts", instructions)

    def test_formal90_exports_ninety_prompts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            args = SimpleNamespace(
                limit_profiles=3,
                design="formal90",
                mitigations=["none"],
                output_dir=str(root / "prompts"),
                responses_dir=str(root / "responses"),
                tracking=str(root / "tracking.csv"),
                instructions=str(root / "instructions.md"),
            )
            with patch("src.manual_experiment.RESULTS_DIR", root):
                export_prompts(args)
            self.assertEqual(90, len(list((root / "prompts").glob("*.txt"))))
            self.assertEqual(90, len(list((root / "responses").glob("*.txt"))))


if __name__ == "__main__":
    unittest.main()
