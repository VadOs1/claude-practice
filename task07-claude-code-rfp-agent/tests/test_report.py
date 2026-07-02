import json
import re

from rfp_eval import report
from rfp_eval.judge import QualityScore
from rfp_eval.metrics import RunMetrics


def _metrics():
    return [
        RunMetrics("single", 0.42, 1200, 8000, 150000, 30000, 189200, 6, 42000, False),
        RunMetrics("swarm", 1.10, 3000, 15000, 400000, 60000, 478000, 14, 90000, False),
        RunMetrics("dynamic", 0.75, 2000, 11000, 250000, 40000, 303000, 9, 65000, False),
    ]


def _scores():
    return [
        QualityScore("single", {"completeness": 3, "specificity": 3, "actionability": 4, "risk_depth": 2, "correctness": 4}, 16, "ok"),
        QualityScore("swarm", {"completeness": 5, "specificity": 4, "actionability": 4, "risk_depth": 5, "correctness": 4}, 22, "best"),
        QualityScore("dynamic", {"completeness": 4, "specificity": 4, "actionability": 5, "risk_depth": 3, "correctness": 4}, 20, "good"),
    ]


def test_build_report_data_merges_and_ranks():
    data = report.build_report_data(_metrics(), _scores(), rfp="rfp-acme-corp.md")
    assert [s["strategy_key"] for s in data["strategies"]] == ["single", "swarm", "dynamic"]
    swarm = next(s for s in data["strategies"] if s["strategy_key"] == "swarm")
    assert swarm["label"] == "Agent Swarm"
    assert swarm["quality"]["total"] == 22
    single = next(s for s in data["strategies"] if s["strategy_key"] == "single")
    assert round(single["quality_per_dollar"], 2) == round(16 / 0.42, 2)
    assert data["winner_quality"] == "swarm"
    assert data["winner_value"] == "single"
    assert data["rubric_dims"] == ["completeness", "specificity", "actionability", "risk_depth", "correctness"]


def test_build_report_data_zero_cost_no_div_error():
    m = [RunMetrics("single", 0.0, 0, 0, 0, 0, 0, 0, 0, True)]
    s = [QualityScore("single", {d: 0 for d in report.rubric_dims()}, 0, "err")]
    data = report.build_report_data(m, s)
    assert data["strategies"][0]["quality_per_dollar"] == 0.0


def test_render_report_embeds_data_and_no_marker():
    data = report.build_report_data(_metrics(), _scores(), rfp="rfp.md")
    html = report.render_report(data)
    assert "__REPORT_DATA__" not in html
    assert "Agent Swarm" in html
    assert "chart" in html.lower()
    m = re.search(r"const REPORT_DATA = (\{.*?\});", html, re.DOTALL)
    assert m and json.loads(m.group(1))["winner_quality"] == "swarm"


def test_write_report_creates_file(tmp_path):
    dest = report.write_report("<html>hi</html>", tmp_path / "eval" / "index.html")
    assert dest.exists() and dest.read_text() == "<html>hi</html>"
