"""LLM-judge: score each strategy's outputs against a fixed rubric."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .sdk_runner import run_query

RUBRIC: list[tuple[str, str]] = [
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

RUBRIC_DIMS: list[str] = [dim for dim, _ in RUBRIC]

_ARTIFACT_NAMES = ["risk-assessment.html", "proposal.md", "proposal.txt"]


@dataclass
class QualityScore:
    strategy_key: str
    scores: dict[str, int]
    total: int
    rationale: str


def read_artifacts(out_dir: str | Path, *, max_chars: int = 12000) -> str:
    out_dir = Path(out_dir)
    if not out_dir.is_dir():
        return "(no artifacts found)"
    found: list[tuple[str, str]] = []
    for name in _ARTIFACT_NAMES:
        p = out_dir / name
        if p.exists():
            found.append((name, p.read_text(errors="replace")))
    docx = out_dir / "proposal.docx"
    if docx.exists():
        try:
            import pypandoc

            found.append(("proposal.docx", pypandoc.convert_file(str(docx), "plain")))
        except Exception:
            pass
    if not found:
        return "(no artifacts found)"
    # Give each artifact a fair share of the budget so a large artifact (e.g. a
    # self-contained HTML dashboard) can't starve the others of any space.
    per_artifact_budget = max(1, max_chars // len(found))
    chunks = [
        f"--- {name} ---\n{text[:per_artifact_budget]}" for name, text in found
    ]
    return "\n\n".join(chunks)[:max_chars]


def build_judge_prompt(artifacts: dict[str, str]) -> str:
    rubric_lines = "\n".join(f"- {dim}: {desc}" for dim, desc in RUBRIC)
    sections = "\n\n".join(
        f"### STRATEGY: {key}\n{text}" for key, text in artifacts.items()
    )
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


def parse_judge_output(text: str) -> list[QualityScore]:
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        return []
    data = json.loads(match.group(0))
    results: list[QualityScore] = []
    for item in data:
        scores = {d: int(item.get("scores", {}).get(d, 0)) for d in RUBRIC_DIMS}
        results.append(
            QualityScore(
                strategy_key=item["strategy"],
                scores=scores,
                total=sum(scores.values()),
                rationale=item.get("rationale", ""),
            )
        )
    return results


async def judge_quality(
    artifacts: dict[str, str],
    *,
    model: str = "sonnet",
    query_fn=None,
) -> list[QualityScore]:
    from claude_agent_sdk import ClaudeAgentOptions

    prompt = build_judge_prompt(artifacts)
    options = ClaudeAgentOptions(model=model, permission_mode="bypassPermissions")
    result = await run_query(prompt, options=options, key="judge", query_fn=query_fn)
    return parse_judge_output(result.result_text)
