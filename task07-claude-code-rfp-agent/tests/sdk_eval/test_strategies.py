import unittest

from sdk_eval.strategies import STRATEGIES, get_strategy


class StrategiesTests(unittest.TestCase):
    def test_exactly_three_strategies_with_unique_keys(self):
        keys = [s.key for s in STRATEGIES]
        self.assertEqual(len(keys), 3)
        self.assertEqual(len(set(keys)), 3)

    def test_expected_keys_dirs_and_labels(self):
        by_key = {s.key: s for s in STRATEGIES}
        self.assertEqual(by_key["rfp-01-baseline"].label, "Baseline")
        self.assertEqual(by_key["rfp-01-baseline"].dir_name, "run-01-baseline")
        self.assertEqual(by_key["rfp-02-agent-teams"].label, "Agent Teams")
        self.assertEqual(by_key["rfp-02-agent-teams"].dir_name, "run-02-agent-teams")
        self.assertEqual(by_key["rfp-03-dynamic-workflow"].label, "Dynamic Workflow")
        self.assertEqual(by_key["rfp-03-dynamic-workflow"].dir_name, "run-03-dynamic-workflow")

    def test_prompts_reference_the_sdk_output_dir_not_the_cli_one(self):
        # Regression guard: verbatim-ported prompts would tell the agent to
        # write into outputs/runs/, clobbering the committed CLI reference
        # runs. Every prompt must point at outputs/runs-sdk/ instead.
        for s in STRATEGIES:
            self.assertIn(f"outputs/runs-sdk/{s.dir_name}/", s.prompt)
            self.assertNotIn("outputs/runs/run-0", s.prompt)

    def test_get_strategy_returns_matching_strategy(self):
        found = get_strategy("rfp-02-agent-teams")
        self.assertEqual(found.key, "rfp-02-agent-teams")

    def test_get_strategy_raises_for_unknown_key(self):
        with self.assertRaises(ValueError):
            get_strategy("not-a-real-strategy")


if __name__ == "__main__":
    unittest.main()
