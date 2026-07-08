"""LLM-judge quality rubric — same 5-dimension rubric this repo already
uses in scripts/judge_quality.py, invoked through the Agent SDK
(sdk_eval.runner.run_prompt) instead of shelling out to the claude CLI.
"""
import json
import re
from pathlib import Path

from .runner import run_prompt
from .strategies import Strategy

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


async def judge_quality(
    runs_dir: Path, strategies: list[Strategy], repo_root: Path, permission_mode: str
) -> list:
    artifacts = {s.key: read_artifacts(runs_dir / s.dir_name) for s in strategies}
    prompt = build_judge_prompt(artifacts)
    result = await run_prompt(prompt, repo_root, permission_mode, model="sonnet")
    if result.result is None:
        raise RuntimeError("judge query returned no result text")
    return parse_judge_output(result.result)


def load_quality_cache(path: Path) -> list | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def save_quality_cache(path: Path, scores: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(scores, indent=2))
