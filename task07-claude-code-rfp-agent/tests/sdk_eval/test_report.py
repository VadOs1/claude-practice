import json
import tempfile
import unittest
from pathlib import Path

from sdk_eval.report import build_report_data, render
from sdk_eval.strategies import STRATEGIES


def write_metrics(run_dir: Path, cost: float, input_tok: int):
    run_dir.mkdir(parents=True)
    metrics = {
        "command": run_dir.name,
        "cost_usd": cost,
        "orchestrator_cost_usd": cost,
        "num_turns": 5,
        "duration_ms": 60000,
        "tokens": {
            "input_tokens": input_tok,
            "output_tokens": 100,
            "cache_creation_input_tokens": 10,
            "cache_read_input_tokens": 20,
        },
        "per_model": {},
    }
    (run_dir / "cost-eval.metrics.json").write_text(json.dumps(metrics))
    (run_dir / "risk-assessment-acme-corp-2026-07-06.html").write_text("<h1>ACME Corp RFP</h1>")


class BuildReportDataTests(unittest.TestCase):
    def test_picks_winners_and_computes_quality_per_dollar(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp) / "runs"
            comparison_dir = Path(tmp) / "comparison"
            write_metrics(runs_dir / "run-01-baseline", cost=1.0, input_tok=100)
            write_metrics(runs_dir / "run-02-agent-teams", cost=2.0, input_tok=200)
            write_metrics(runs_dir / "run-03-dynamic-workflow", cost=0.5, input_tok=50)
            comparison_dir.mkdir(parents=True)
            quality = [
                {"strategy_key": "rfp-01-baseline", "scores": {}, "total": 10, "rationale": "ok"},
                {"strategy_key": "rfp-02-agent-teams", "scores": {}, "total": 20, "rationale": "best"},
                {"strategy_key": "rfp-03-dynamic-workflow", "scores": {}, "total": 15, "rationale": "cheap"},
            ]
            (comparison_dir / "quality.json").write_text(json.dumps(quality))

            data = build_report_data(runs_dir, comparison_dir, STRATEGIES)

            self.assertEqual(data["rfp"], "ACME Corp RFP")
            self.assertEqual(data["winner_quality"], "rfp-02-agent-teams")
            self.assertEqual(data["winner_value"], "rfp-03-dynamic-workflow")
            by_key = {s["strategy_key"]: s for s in data["strategies"]}
            self.assertEqual(
                by_key["rfp-03-dynamic-workflow"]["quality_per_dollar"], round(15 / 0.5, 2)
            )

    def test_missing_quality_cache_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp) / "runs"
            comparison_dir = Path(tmp) / "comparison"
            write_metrics(runs_dir / "run-01-baseline", cost=1.0, input_tok=100)
            with self.assertRaises(FileNotFoundError):
                build_report_data(runs_dir, comparison_dir, STRATEGIES[:1])


class RenderTests(unittest.TestCase):
    def test_writes_html_and_report_data_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            template_path = Path(tmp) / "template.html.tmpl"
            template_path.write_text("<html>__REPORT_DATA__</html>")
            output_path = Path(tmp) / "out" / "report.html"
            data = {"rfp": "X", "strategies": []}

            render(data, template_path, output_path)

            html = output_path.read_text()
            self.assertIn(json.dumps(data, indent=2), html)
            report_data_json = json.loads((output_path.parent / "report-data.json").read_text())
            self.assertEqual(report_data_json, data)


if __name__ == "__main__":
    unittest.main()
