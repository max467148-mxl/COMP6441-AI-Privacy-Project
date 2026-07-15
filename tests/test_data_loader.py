import unittest

from src.data_loader import load_conditions, load_ground_truth, load_profiles, load_questions


class DataLoaderTests(unittest.TestCase):
    def test_dataset_shape(self):
        profiles = load_profiles()
        truth = load_ground_truth()
        self.assertEqual(len(profiles), 10)
        self.assertTrue(all(len(profile["fragments"]) == 15 for profile in profiles))
        self.assertEqual(set(profile["id"] for profile in profiles), set(truth.keys()))

    def test_questions_and_conditions_exist(self):
        self.assertEqual(len(load_questions()), 5)
        self.assertEqual(
            set(load_conditions().keys()),
            {
                "no_memory",
                "limited_memory",
                "full_aggregated_memory",
                "compartmentalised_memory",
            },
        )


if __name__ == "__main__":
    unittest.main()
