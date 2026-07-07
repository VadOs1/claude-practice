#!/usr/bin/env python3
"""Build the cost/risk REPORT_DATA JSON and render it into templates/report.html.tmpl.

Must be run from the task07-claude-code-rfp-agent/ directory (relative
paths below assume it), same requirement as scripts/cost-eval.sh.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RUNS_DIR = Path("outputs/runs")
TEMPLATE_PATH = Path("templates/report.html.tmpl")

STRATEGIES = [
    {"key": "run-01-baseline", "label": "Baseline", "dir": "run-01-baseline"},
    {"key": "run-02-agent-teams", "label": "Agent Teams", "dir": "run-02-agent-teams"},
    {"key": "run-03-dynamic-workflow", "label": "Dynamic Workflow", "dir": "run-03-dynamic-workflow"},
]

RISK_CATEGORIES = {
    "discount": "Financial",
    "pricefreeze": "Financial",
    "net90": "Financial",
    "mfn": "Financial",
    "liability": "Legal",
    "ip": "Legal",
    "indemnity": "Legal",
    "termnotice": "Operational",
    "slaterm": "Operational",
    "subprocessor": "Operational",
    "audit": "Operational",
    "slalevel": "Operational",
}

RUBRIC_DIMS = ["Financial", "Legal", "Operational"]

CLAUSE_RE = re.compile(
    r"id:\s*'([^']+)'.*?risk:\s*([0-9.]+).*?severity:\s*'([^']+)'.*?state:\s*'([^']+)'",
    re.S,
)
CLAUSES_ARRAY_RE = re.compile(r"const clauses = \[(.*?)\n\];", re.S)
H1_RE = re.compile(r"<h1>(.*?)</h1>", re.S)


def risk_for(risk, state):
    if state == "accepted":
        return risk
    if state == "counter":
        return risk * 0.5
    return 0.0


def find_risk_html(run_dir):
    matches = sorted(run_dir.glob("risk-assessment-*.html"))
    if not matches:
        raise FileNotFoundError(f"no risk-assessment-*.html in {run_dir}")
    return matches[-1]


def parse_risk_html(html_path):
    text = html_path.read_text()
    array_match = CLAUSES_ARRAY_RE.search(text)
    if not array_match:
        raise ValueError(f"could not find 'const clauses = [...]' in {html_path}")
    body = array_match.group(1)

    category_actual = {c: 0.0 for c in RUBRIC_DIMS}
    category_max = {c: 0.0 for c in RUBRIC_DIMS}
    net_risk = 0.0
    seen_ids = set()
    for match in CLAUSE_RE.finditer(body):
        clause_id, risk_str, _severity, state = match.groups()
        if clause_id in seen_ids:
            continue
        seen_ids.add(clause_id)
        category = RISK_CATEGORIES.get(clause_id)
        if category is None:
            continue
        risk = float(risk_str)
        actual = risk_for(risk, state)
        category_actual[category] += actual
        category_max[category] += risk
        net_risk += actual

    h1_match = H1_RE.search(text)
    title = h1_match.group(1).strip() if h1_match else "RFP Comparison"
    return category_actual, category_max, round(net_risk, 2), title


def safety_scores(category_actual, category_max):
    scores = {}
    for dim in RUBRIC_DIMS:
        max_r = category_max[dim]
        actual = category_actual[dim]
        scores[dim] = 5.0 if max_r <= 0 else round(5.0 * (1 - actual / max_r), 2)
    scores["total"] = round(sum(scores[d] for d in RUBRIC_DIMS), 2)
    return scores


def load_metrics(run_dir):
    return json.loads((run_dir / "cost-eval.metrics.json").read_text())


def build_report_data():
    strategies = []
    rfp_title = None
    for s in STRATEGIES:
        run_dir = RUNS_DIR / s["dir"]
        metrics = load_metrics(run_dir)
        risk_html = find_risk_html(run_dir)
        category_actual, category_max, net_risk, title = parse_risk_html(risk_html)
        rfp_title = rfp_title or title
        quality = safety_scores(category_actual, category_max)
        cost = metrics["cost_usd"]
        tokens = metrics["tokens"]

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
            "net_risk_pct": net_risk,
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
