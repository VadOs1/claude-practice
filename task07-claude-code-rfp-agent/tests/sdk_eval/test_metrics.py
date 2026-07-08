import json
import tempfile
import unittest
from pathlib import Path

from claude_agent_sdk import ResultMessage

from sdk_eval.metrics import build_metrics, save_metrics


def make_result(**overrides) -> ResultMessage:
    defaults = dict(
        subtype="success",
        duration_ms=45000,
        duration_api_ms=40000,
        is_error=False,
        num_turns=7,
        session_id="sess-1",
        stop_reason="end_turn",
        total_cost_usd=0.5,
        usage={},
        result="ok",
        structured_output=None,
        model_usage={
            "claude-sonnet-5": {
                "inputTokens": 22,
                "outputTokens": 26825,
                "cacheReadInputTokens": 514670,
                "cacheCreationInputTokens": 50760,
                "costUSD": 0.4,
            },
            "claude-haiku-4-5-20251001": {
                "inputTokens": 523,
                "outputTokens": 14,
                "cacheReadInputTokens": 0,
                "cacheCreationInputTokens": 0,
                "costUSD": 0.1,
            },
        },
        permission_denials=None,
        deferred_tool_use=None,
        errors=None,
        api_error_status=None,
        uuid="u-1",
    )
    defaults.update(overrides)
    return ResultMessage(**defaults)


class BuildMetricsTests(unittest.TestCase):
    def test_sums_cost_and_tokens_across_models(self):
        result = make_result()
        metrics = build_metrics("rfp-01-baseline", result)
        self.assertEqual(metrics["command"], "rfp-01-baseline")
        self.assertAlmostEqual(metrics["cost_usd"], 0.5)
        self.assertEqual(metrics["orchestrator_cost_usd"], 0.5)
        self.assertEqual(metrics["num_turns"], 7)
        self.assertEqual(metrics["duration_ms"], 45000)
        self.assertEqual(metrics["tokens"], {
            "input_tokens": 22 + 523,
            "output_tokens": 26825 + 14,
            "cache_creation_input_tokens": 50760 + 0,
            "cache_read_input_tokens": 514670 + 0,
        })
        self.assertEqual(metrics["per_model"], result.model_usage)

    def test_empty_model_usage_yields_zero_cost(self):
        result = make_result(model_usage={}, total_cost_usd=0.0)
        metrics = build_metrics("rfp-01-baseline", result)
        self.assertEqual(metrics["cost_usd"], 0)
        self.assertEqual(metrics["tokens"]["input_tokens"], 0)

    def test_none_model_usage_yields_zero_cost(self):
        result = make_result(model_usage=None)
        metrics = build_metrics("rfp-01-baseline", result)
        self.assertEqual(metrics["cost_usd"], 0)


class SaveMetricsTests(unittest.TestCase):
    def test_writes_both_json_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run-01-baseline"
            result = make_result()
            metrics = save_metrics(run_dir, "rfp-01-baseline", result)

            raw = json.loads((run_dir / "cost-eval.json").read_text())
            self.assertEqual(raw["session_id"], "sess-1")
            self.assertEqual(raw["num_turns"], 7)

            written_metrics = json.loads((run_dir / "cost-eval.metrics.json").read_text())
            self.assertEqual(written_metrics, metrics)
            self.assertEqual(written_metrics["command"], "rfp-01-baseline")


if __name__ == "__main__":
    unittest.main()
