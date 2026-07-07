#!/usr/bin/env python3
"""Build the cost/quality REPORT_DATA JSON and render it into templates/report.html.tmpl.

Must be run from the task07-claude-code-rfp-agent/ directory (relative
paths below assume it), same requirement as scripts/cost-eval.sh.

Quality scores come from outputs/runs/comparison-cost-eval/quality.json,
produced by scripts/judge_quality.py — run that first if it doesn't exist.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RUNS_DIR = Path("outputs/runs")
TEMPLATE_PATH = Path("templates/report.html.tmpl")
QUALITY_CACHE = Path("outputs/runs/comparison-cost-eval/quality.json")

STRATEGIES = [
    {"key": "run-01-baseline", "label": "Baseline", "dir": "run-01-baseline"},
    {"key": "run-02-agent-teams", "label": "Agent Teams", "dir": "run-02-agent-teams"},
    {"key": "run-03-dynamic-workflow", "label": "Dynamic Workflow", "dir": "run-03-dynamic-workflow"},
]

RUBRIC_DIMS = ["completeness", "specificity", "actionability", "risk_depth", "correctness"]

H1_RE = re.compile(r"<h1>(.*?)</h1>", re.S)


def find_risk_html(run_dir):
    matches = sorted(run_dir.glob("risk-assessment-*.html"))
    return matches[-1] if matches else None


def rfp_title_for(run_dir):
    risk_html = find_risk_html(run_dir)
    if risk_html is None:
        return "RFP Comparison"
    m = H1_RE.search(risk_html.read_text())
    return m.group(1).strip() if m else "RFP Comparison"


def load_metrics(run_dir):
    return json.loads((run_dir / "cost-eval.metrics.json").read_text())


def load_quality_scores():
    if not QUALITY_CACHE.exists():
        raise FileNotFoundError(
            f"{QUALITY_CACHE} not found — run scripts/judge_quality.py first"
        )
    scores = json.loads(QUALITY_CACHE.read_text())
    return {s["strategy_key"]: s for s in scores}


def build_report_data():
    quality_by_key = load_quality_scores()
    strategies = []
    rfp_title = None
    for s in STRATEGIES:
        run_dir = RUNS_DIR / s["dir"]
        metrics = load_metrics(run_dir)
        rfp_title = rfp_title or rfp_title_for(run_dir)
        tokens = metrics["tokens"]
        cost = metrics["cost_usd"]

        sc = quality_by_key.get(s["key"])
        quality = dict(sc["scores"]) if sc else {d: 0 for d in RUBRIC_DIMS}
        quality["total"] = sc["total"] if sc else 0
        quality["rationale"] = sc["rationale"] if sc else ""

        strategies.append({
            "strategy_key": s["key"],
            "label": s["label"],
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

    winner_quality = max(strategies, key=lambda s: s["quality"]["total"])["strategy_key"]
    winner_value = max(strategies, key=lambda s: s["quality_per_dollar"])["strategy_key"]

    return {
        "rfp": rfp_title,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rubric_dims": RUBRIC_DIMS,
        "winner_quality": winner_quality,
        "winner_value": winner_value,
        "strategies": strategies,
    }


def render(report_data, output_path):
    template = TEMPLATE_PATH.read_text()
    rendered = template.replace("__REPORT_DATA__", json.dumps(report_data, indent=2))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered)
    (output_path.parent / "report-data.json").write_text(json.dumps(report_data, indent=2))


def main():
    if len(sys.argv) != 2:
        print("usage: generate_comparison_report.py <output_html_path>", file=sys.stderr)
        sys.exit(1)
    output_path = Path(sys.argv[1])
    report_data = build_report_data()
    render(report_data, output_path)
    print(f"wrote {output_path}")
    print(f"wrote {output_path.parent / 'report-data.json'}")


if __name__ == "__main__":
    main()
