"""Build REPORT_DATA and render it into templates/report.html.tmpl — same
logic as scripts/generate_comparison_report.py, parameterized on the runs
directory instead of a hardcoded outputs/runs constant.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from .strategies import Strategy

RUBRIC_DIMS = ["completeness", "specificity", "actionability", "risk_depth", "correctness"]

H1_RE = re.compile(r"<h1>(.*?)</h1>", re.S)


def find_risk_html(run_dir: Path):
    matches = sorted(run_dir.glob("risk-assessment-*.html"))
    return matches[-1] if matches else None


def rfp_title_for(run_dir: Path) -> str:
    risk_html = find_risk_html(run_dir)
    if risk_html is None:
        return "RFP Comparison"
    m = H1_RE.search(risk_html.read_text())
    return m.group(1).strip() if m else "RFP Comparison"


def load_metrics(run_dir: Path) -> dict:
    return json.loads((run_dir / "cost-eval.metrics.json").read_text())


def load_quality_scores(quality_cache: Path) -> dict:
    if not quality_cache.exists():
        raise FileNotFoundError(f"{quality_cache} not found — run the judge step first")
    scores = json.loads(quality_cache.read_text())
    return {s["strategy_key"]: s for s in scores}


def build_report_data(runs_dir: Path, comparison_dir: Path, strategies: list[Strategy]) -> dict:
    quality_by_key = load_quality_scores(comparison_dir / "quality.json")
    strategy_rows = []
    rfp_title = None
    for s in strategies:
        run_dir = runs_dir / s.dir_name
        metrics = load_metrics(run_dir)
        rfp_title = rfp_title or rfp_title_for(run_dir)
        tokens = metrics["tokens"]
        cost = metrics["cost_usd"]

        sc = quality_by_key.get(s.key)
        if sc is None:
            print(f"warning: no quality score found for {s.key!r}", file=sys.stderr)
        quality = dict(sc["scores"]) if sc else {d: 0 for d in RUBRIC_DIMS}
        quality["total"] = sc["total"] if sc else 0
        quality["rationale"] = sc["rationale"] if sc else ""

        strategy_rows.append({
            "strategy_key": s.key,
            "label": s.label,
            "cost_usd": cost,
            "input_tokens": tokens["input_tokens"],
            "output_tokens": tokens["output_tokens"],
            "cache_read_tokens": tokens["cache_read_input_tokens"],
            "cache_creation_tokens": tokens["cache_creation_input_tokens"],
            "total_tokens": sum(tokens.values()),
            "num_turns": metrics["num_turns"],
            "duration_ms": metrics["duration_ms"],
            "quality": quality,
            "quality_per_dollar": round(quality["total"] / cost, 2) if cost else 0.0,
        })

    winner_quality = max(strategy_rows, key=lambda s: s["quality"]["total"])["strategy_key"]
    winner_value = max(strategy_rows, key=lambda s: s["quality_per_dollar"])["strategy_key"]

    return {
        "rfp": rfp_title,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rubric_dims": RUBRIC_DIMS,
        "winner_quality": winner_quality,
        "winner_value": winner_value,
        "strategies": strategy_rows,
    }


def render(report_data: dict, template_path: Path, output_path: Path) -> None:
    template = template_path.read_text()
    rendered = template.replace("__REPORT_DATA__", json.dumps(report_data, indent=2))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered)
    (output_path.parent / "report-data.json").write_text(json.dumps(report_data, indent=2))
