import json
import tempfile
import unittest
from pathlib import Path

from sdk_eval.judge import (
    RUBRIC_DIMS,
    build_judge_prompt,
    load_quality_cache,
    parse_judge_output,
    read_artifacts,
    save_quality_cache,
)


class ReadArtifactsTests(unittest.TestCase):
    def test_no_artifacts_returns_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(read_artifacts(Path(tmp)), "(no artifacts found)")

    def test_reads_proposal_and_risk_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "proposal-acme-corp-2026-07-06.md").write_text("PROPOSAL BODY")
            (run_dir / "risk-assessment-acme-corp-2026-07-06.html").write_text("<h1>Risk</h1>")
            text = read_artifacts(run_dir)
            self.assertIn("PROPOSAL BODY", text)
            self.assertIn("<h1>Risk</h1>", text)
            self.assertIn("proposal-acme-corp-2026-07-06.md", text)


class BuildJudgePromptTests(unittest.TestCase):
    def test_includes_all_rubric_dims_and_strategy_keys(self):
        prompt = build_judge_prompt({"rfp-01-baseline": "text A", "rfp-02-agent-teams": "text B"})
        for dim in RUBRIC_DIMS:
            self.assertIn(dim, prompt)
        self.assertIn("rfp-01-baseline", prompt)
        self.assertIn("text A", prompt)
        self.assertIn("rfp-02-agent-teams", prompt)


class ParseJudgeOutputTests(unittest.TestCase):
    def test_parses_plain_json_array(self):
        text = json.dumps([
            {"strategy": "rfp-01-baseline", "scores": {d: 3 for d in RUBRIC_DIMS}, "rationale": "ok"}
        ])
        results = parse_judge_output(text)
        self.assertEqual(results[0]["strategy_key"], "rfp-01-baseline")
        self.assertEqual(results[0]["total"], 15)

    def test_parses_json_wrapped_in_fence(self):
        payload = json.dumps([
            {"strategy": "rfp-02-agent-teams", "scores": {d: 4 for d in RUBRIC_DIMS}, "rationale": "good"}
        ])
        text = f"Here you go:\n```json\n{payload}\n```"
        results = parse_judge_output(text)
        self.assertEqual(results[0]["strategy_key"], "rfp-02-agent-teams")

    def test_raises_when_no_json_array_present(self):
        with self.assertRaises(ValueError):
            parse_judge_output("no json here")


class QualityCacheTests(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "quality.json"
            self.assertIsNone(load_quality_cache(path))
            scores = [{"strategy_key": "rfp-01-baseline", "scores": {}, "total": 0, "rationale": ""}]
            save_quality_cache(path, scores)
            self.assertEqual(load_quality_cache(path), scores)


if __name__ == "__main__":
    unittest.main()
