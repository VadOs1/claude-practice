import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

from rfp_eval import orchestrator

JUDGE_TEXT = """```json
[
 {"strategy":"single","scores":{"completeness":3,"specificity":3,"actionability":4,"risk_depth":2,"correctness":4},"rationale":"ok"},
 {"strategy":"swarm","scores":{"completeness":5,"specificity":4,"actionability":4,"risk_depth":5,"correctness":4},"rationale":"best"},
 {"strategy":"dynamic","scores":{"completeness":4,"specificity":4,"actionability":5,"risk_depth":3,"correctness":4},"rationale":"good"},
 {"strategy":"agent_teams","scores":{"completeness":4,"specificity":3,"actionability":4,"risk_depth":3,"correctness":4},"rationale":"solid team output"}
]
```"""


def _run_result(out_dir):
    # simulate a strategy writing an artifact + returning a ResultMessage
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    (Path(out_dir) / "risk-assessment.html").write_text("<html>risk</html>")
    return SimpleNamespace(
        total_cost_usd=0.5, usage={"input_tokens": 100, "output_tokens": 200,
        "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        num_turns=4, duration_ms=1000, is_error=False, result="wrote files",
    )


def test_run_evaluation_end_to_end(tmp_path):
    def make_strategy_query(out_dir):
        async def fake_query(prompt, options=None):
            yield _run_result(out_dir)
        return fake_query

    # query_fn is chosen per-run using the run's out_dir (see orchestrator contract)
    def query_factory(out_dir):
        return make_strategy_query(out_dir)

    async def judge_query(prompt, options=None):
        yield SimpleNamespace(
            total_cost_usd=0.05, usage={}, num_turns=1, duration_ms=1,
            is_error=False, result=JUDGE_TEXT,
        )

    index = asyncio.run(
        orchestrator.run_evaluation(
            task_dir=tmp_path,
            rfp_path="rfp.md",
            out_root=tmp_path / "outputs",
            query_fn=query_factory,
            judge_query_fn=judge_query,
        )
    )
    assert index.exists() and index.name == "index.html"
    html = index.read_text()
    assert "Agent Swarm" in html
    assert "Agent Teams" in html
    metrics = json.loads((tmp_path / "outputs" / "eval" / "metrics.json").read_text())
    quality = json.loads((tmp_path / "outputs" / "eval" / "quality.json").read_text())
    assert len(metrics) == 4 and len(quality) == 4
    assert (tmp_path / "outputs" / "runs" / "swarm" / "run.json").exists()
    assert (tmp_path / "outputs" / "runs" / "agent_teams" / "run.json").exists()


def test_run_evaluation_survives_one_strategy_crashing(tmp_path):
    def make_strategy_query(out_dir):
        async def fake_query(prompt, options=None):
            yield _run_result(out_dir)
        return fake_query

    def crashing_query(out_dir):
        async def fake_query(prompt, options=None):
            raise RuntimeError("transport crashed")
            yield  # pragma: no cover - makes this an async generator
        return fake_query

    def query_factory(out_dir):
        if Path(out_dir).name == "dynamic":
            return crashing_query(out_dir)
        return make_strategy_query(out_dir)

    async def judge_query(prompt, options=None):
        yield SimpleNamespace(
            total_cost_usd=0.05, usage={}, num_turns=1, duration_ms=1,
            is_error=False, result=JUDGE_TEXT,
        )

    index = asyncio.run(
        orchestrator.run_evaluation(
            task_dir=tmp_path,
            rfp_path="rfp.md",
            out_root=tmp_path / "outputs",
            query_fn=query_factory,
            judge_query_fn=judge_query,
        )
    )
    assert index.exists() and index.name == "index.html"

    metrics = json.loads((tmp_path / "outputs" / "eval" / "metrics.json").read_text())
    quality = json.loads((tmp_path / "outputs" / "eval" / "quality.json").read_text())
    assert len(metrics) == 4 and len(quality) == 4

    by_key = {m["strategy_key"]: m for m in metrics}
    assert set(by_key) == {"single", "swarm", "dynamic", "agent_teams"}
    assert by_key["dynamic"]["is_error"] is True
    assert by_key["single"]["is_error"] is False
    assert by_key["swarm"]["is_error"] is False
    assert by_key["agent_teams"]["is_error"] is False

    assert (tmp_path / "outputs" / "runs" / "dynamic" / "run.json").exists()
    assert (tmp_path / "outputs" / "runs" / "single" / "run.json").exists()
    assert (tmp_path / "outputs" / "runs" / "swarm" / "run.json").exists()
    assert (tmp_path / "outputs" / "runs" / "agent_teams" / "run.json").exists()

    dynamic_raw = json.loads(
        (tmp_path / "outputs" / "runs" / "dynamic" / "run.json").read_text()
    )
    assert "transport crashed" in dynamic_raw["error"]


def test_run_evaluation_crash_overwrites_stale_run_json(tmp_path):
    # A prior successful run left a run.json behind for "dynamic". If this
    # run's "dynamic" strategy crashes, the stale success data must not
    # survive on disk (it would otherwise be judged as if it were fresh).
    dynamic_dir = tmp_path / "outputs" / "runs" / "dynamic"
    dynamic_dir.mkdir(parents=True)
    (dynamic_dir / "run.json").write_text(
        json.dumps({"is_error": False, "total_cost_usd": 1.5, "result": "stale success"})
    )

    def make_strategy_query(out_dir):
        async def fake_query(prompt, options=None):
            yield _run_result(out_dir)
        return fake_query

    def crashing_query(out_dir):
        async def fake_query(prompt, options=None):
            raise RuntimeError("transport crashed")
            yield  # pragma: no cover - makes this an async generator
        return fake_query

    def query_factory(out_dir):
        if Path(out_dir).name == "dynamic":
            return crashing_query(out_dir)
        return make_strategy_query(out_dir)

    async def judge_query(prompt, options=None):
        yield SimpleNamespace(
            total_cost_usd=0.05, usage={}, num_turns=1, duration_ms=1,
            is_error=False, result=JUDGE_TEXT,
        )

    asyncio.run(
        orchestrator.run_evaluation(
            task_dir=tmp_path,
            rfp_path="rfp.md",
            out_root=tmp_path / "outputs",
            query_fn=query_factory,
            judge_query_fn=judge_query,
        )
    )

    dynamic_raw = json.loads((dynamic_dir / "run.json").read_text())
    assert dynamic_raw["is_error"] is True
    assert "stale success" not in json.dumps(dynamic_raw)
