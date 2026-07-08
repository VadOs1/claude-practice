import tempfile
import unittest
from pathlib import Path

from sdk_eval.cli import (
    check_report_inputs_ready,
    format_summary_table,
    parse_args,
    resolve_commands,
)
from sdk_eval.strategies import STRATEGIES


class ResolveCommandsTests(unittest.TestCase):
    def test_no_args_returns_all_three_in_order(self):
        strategies = resolve_commands([])
        self.assertEqual([s.key for s in strategies], [s.key for s in STRATEGIES])

    def test_specific_key_returns_just_that_strategy(self):
        strategies = resolve_commands(["rfp-02-agent-teams"])
        self.assertEqual([s.key for s in strategies], ["rfp-02-agent-teams"])

    def test_unknown_key_raises(self):
        with self.assertRaises(ValueError):
            resolve_commands(["not-a-real-strategy"])


class CheckReportInputsReadyTests(unittest.TestCase):
    def test_reports_missing_metrics_and_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp)
            missing = check_report_inputs_ready(runs_dir, STRATEGIES)
            self.assertEqual(len(missing), len(STRATEGIES) * 2)

    def test_no_missing_when_all_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp)
            for s in STRATEGIES:
                run_dir = runs_dir / s.dir_name
                run_dir.mkdir(parents=True)
                (run_dir / "cost-eval.metrics.json").write_text("{}")
                (run_dir / "risk-assessment-acme-corp-2026-07-06.html").write_text("<h1>x</h1>")
            self.assertEqual(check_report_inputs_ready(runs_dir, STRATEGIES), [])


class FormatSummaryTableTests(unittest.TestCase):
    def test_includes_header_and_one_row_per_strategy(self):
        rows = [{
            "command": "rfp-01-baseline",
            "cost_usd": 0.861402,
            "tokens": {
                "input_tokens": 22,
                "output_tokens": 26825,
                "cache_creation_input_tokens": 50760,
                "cache_read_input_tokens": 514670,
            },
        }]
        table = format_summary_table(rows)
        lines = table.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("command", lines[0])
        self.assertIn("rfp-01-baseline", lines[1])


class ParseArgsTests(unittest.TestCase):
    def test_defaults(self):
        args = parse_args([])
        self.assertEqual(args.commands, [])
        self.assertFalse(args.report_only)

    def test_report_only_flag(self):
        args = parse_args(["--report-only"])
        self.assertTrue(args.report_only)

    def test_positional_commands(self):
        args = parse_args(["rfp-01-baseline", "rfp-02-agent-teams"])
        self.assertEqual(args.commands, ["rfp-01-baseline", "rfp-02-agent-teams"])


if __name__ == "__main__":
    unittest.main()
