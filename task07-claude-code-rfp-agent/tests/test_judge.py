import asyncio
from pathlib import Path
from types import SimpleNamespace

from rfp_eval import judge

JUDGE_TEXT = """Here are my scores:
```json
[
 {"strategy":"single","scores":{"completeness":3,"specificity":3,"actionability":4,"risk_depth":2,"correctness":4},"rationale":"Shallow risk."},
 {"strategy":"swarm","scores":{"completeness":5,"specificity":4,"actionability":4,"risk_depth":5,"correctness":4},"rationale":"Deepest."},
 {"strategy":"dynamic","scores":{"completeness":4,"specificity":4,"actionability":5,"risk_depth":3,"correctness":4},"rationale":"Well planned."}
]
```
"""


def test_rubric_dims():
    assert judge.RUBRIC_DIMS == [
        "completeness", "specificity", "actionability", "risk_depth", "correctness",
    ]


def test_build_judge_prompt_has_artifacts_and_rubric():
    p = judge.build_judge_prompt({"single": "S-OUT", "swarm": "W-OUT"})
    assert "S-OUT" in p and "W-OUT" in p
    assert "risk_depth" in p
    assert "JSON" in p


def test_parse_judge_output():
    scores = judge.parse_judge_output(JUDGE_TEXT)
    by = {s.strategy_key: s for s in scores}
    assert set(by) == {"single", "swarm", "dynamic"}
    assert by["swarm"].scores["risk_depth"] == 5
    assert by["swarm"].total == 22
    assert "Deepest" in by["swarm"].rationale


def test_read_artifacts_reads_html_and_truncates(tmp_path):
    (tmp_path / "risk-assessment.html").write_text("<html>RISK</html>" * 2000)
    text = judge.read_artifacts(tmp_path, max_chars=100)
    assert "RISK" in text and len(text) <= 100


def test_read_artifacts_missing(tmp_path):
    assert "no artifacts" in judge.read_artifacts(tmp_path / "nope").lower()


def test_judge_quality_uses_injected_query_fn():
    async def fake_query(prompt, options=None):
        yield SimpleNamespace(
            total_cost_usd=0.05, usage={}, num_turns=1, duration_ms=1,
            is_error=False, result=JUDGE_TEXT,
        )

    scores = asyncio.run(
        judge.judge_quality({"single": "a", "swarm": "b", "dynamic": "c"}, query_fn=fake_query)
    )
    assert {s.strategy_key for s in scores} == {"single", "swarm", "dynamic"}
