#!/usr/bin/env python3
"""LLM-judge: score each strategy's RFP-response artifacts against a fixed
rubric, caching results to outputs/runs/comparison-cost-eval/quality.json.

Rubric ported from the reference implementation at
impl-8:task07-claude-code-rfp-agent/rfp_eval/judge.py. That reference uses
the claude_agent_sdk (not available here); this script gets equivalent
results by shelling out to the `claude` CLI instead, matching how
scripts/cost-eval.sh already invokes it.

Must be run from the task07-claude-code-rfp-agent/ directory (relative
paths below assume it), same requirement as scripts/cost-eval.sh.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RUNS_DIR = Path("outputs/runs")
QUALITY_CACHE = Path("outputs/runs/comparison-cost-eval/quality.json")

STRATEGIES = [
    {"key": "run-01-baseline", "dir": "run-01-baseline"},
    {"key": "run-02-agent-teams", "dir": "run-02-agent-teams"},
    {"key": "run-03-dynamic-workflow", "dir": "run-03-dynamic-workflow"},
]

RUBRIC = [
    ("completeness", "Covers all required sections (exec summary, understanding, "
        "fit, commercial, contract approach, risks)."),
    ("specificity", "Concrete numbers, cites past-wins.json / product facts, "
        "avoids vague filler."),
    ("actionability", "Clear recommendations and a decision the reader can act on."),
    ("risk_depth", "Risk assessment is rigorous: distinct clauses, severities, "
        "net-risk vs revenue, a usable dashboard."),
    ("correctness", "Internally consistent, no contradictions or hallucinated "
        "facts against the RFP."),
]
RUBRIC_DIMS = [dim for dim, _ in RUBRIC]


def read_artifacts(run_dir: Path, max_chars: int = 12000) -> str:
    found = []
    for pattern in ("proposal-*.md", "risk-assessment-*.html"):
        matches = sorted(run_dir.glob(pattern))
        if matches:
            found.append((matches[-1].name, matches[-1].read_text(errors="replace")))
    if not found:
        return "(no artifacts found)"
    per_artifact_budget = max(1, max_chars // len(found))
    chunks = [f"--- {name} ---\n{text[:per_artifact_budget]}" for name, text in found]
    return "\n\n".join(chunks)[:max_chars]


def build_judge_prompt(artifacts: dict) -> str:
    rubric_lines = "\n".join(f"- {dim}: {desc}" for dim, desc in RUBRIC)
    sections = "\n\n".join(f"### STRATEGY: {key}\n{text}" for key, text in artifacts.items())
    keys = ", ".join(artifacts)
    return (
        "You are an impartial evaluator comparing RFP-response outputs produced by "
        "different Claude Code strategies. Score each strategy on every rubric "
        "dimension from 1 (poor) to 5 (excellent).\n\n"
        f"RUBRIC:\n{rubric_lines}\n\n"
        f"OUTPUTS TO EVALUATE (strategies: {keys}):\n{sections}\n\n"
        "Respond with ONLY a JSON array (optionally in a ```json fence), one object "
        "per strategy, shaped exactly:\n"
        '[{"strategy":"<key>","scores":{'
        + ",".join(f'"{d}":<1-5>' for d in RUBRIC_DIMS)
        + '},"rationale":"<one sentence>"}]\n'
        "Do not include any other text."
    )


def parse_judge_output(text: str) -> list:
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        raise ValueError(f"no JSON array found in judge output: {text[:500]!r}")
    data = json.loads(match.group(0))
    results = []
    for item in data:
        scores = {d: int(item.get("scores", {}).get(d, 0)) for d in RUBRIC_DIMS}
        results.append({
            "strategy_key": item["strategy"],
            "scores": scores,
            "total": sum(scores.values()),
            "rationale": item.get("rationale", ""),
        })
    return results


def invoke_judge(prompt: str, model: str = "sonnet") -> str:
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--model", model, "--output-format", "json",
             "--permission-mode", "bypassPermissions"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr, file=sys.stderr)
        raise
    envelope = json.loads(result.stdout)
    return envelope["result"]


def judge_quality() -> list:
    artifacts = {}
    for s in STRATEGIES:
        run_dir = RUNS_DIR / s["dir"]
        artifacts[s["key"]] = read_artifacts(run_dir)
    prompt = build_judge_prompt(artifacts)
    response_text = invoke_judge(prompt)
    return parse_judge_output(response_text)


def main():
    force = "--force" in sys.argv[1:]
    if QUALITY_CACHE.exists() and not force:
        print(f"quality cache already exists at {QUALITY_CACHE} (use --force to re-judge)")
        return
    scores = judge_quality()
    QUALITY_CACHE.parent.mkdir(parents=True, exist_ok=True)
    QUALITY_CACHE.write_text(json.dumps(scores, indent=2))
    print(f"wrote {QUALITY_CACHE}")


if __name__ == "__main__":
    main()
