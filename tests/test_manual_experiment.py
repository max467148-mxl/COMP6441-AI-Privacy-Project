import tempfile
import unittest
from pathlib import Path

from src.manual_experiment import build_instructions


class ManualExperimentTests(unittest.TestCase):
    def test_instructions_include_collect_command(self):
        instructions = build_instructions(10)
        self.assertIn("py -3 -m src.manual_experiment collect", instructions)
        self.assertIn("10 prompts", instructions)


if __name__ == "__main__":
    unittest.main()

