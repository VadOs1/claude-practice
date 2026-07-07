# LLM-Judge Quality Rubric Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the invented Financial/Legal/Operational risk-category radar in `outputs/runs/comparison-cost-eval/report.html` with a genuine LLM-judged 5-dimension quality rubric (completeness, specificity, actionability, risk_depth, correctness), matching the reference implementation that already exists (and was already validated with tests) on sibling branches `impl-5`/`impl-6`/`impl-8` at `task07-claude-code-rfp-agent/rfp_eval/judge.py`.

**Architecture:** A new script, `scripts/judge_quality.py`, reads each of the three runs' real artifacts (`proposal-*.md`, `risk-assessment-*.html`), builds ONE combined prompt (all three strategies scored together, for relative consistency) using a rubric ported verbatim from the reference `judge.py`, invokes it via `subprocess.run(["claude", "-p", prompt, ...])` (this repo has no `claude_agent_sdk` dependency, so the CLI is used instead of the reference's SDK call — same underlying model, different invocation path), parses the JSON response, and caches it to `outputs/runs/comparison-cost-eval/quality.json`. The cache makes re-runs free: if `quality.json` already exists, the judge is not re-invoked. `scripts/generate_comparison_report.py` (from the prior plan) is simplified to drop its own clause-parsing risk-category logic entirely and instead load `quality.json` directly, merging it into `REPORT_DATA` exactly like the reference `rfp_eval/report.py` does. `templates/report.html.tmpl`'s panel/label copy is reverted from the previous plan's "Risk safety" wording back to the original "Quality" wording, since the data is genuine quality-rubric data again (of which `risk_depth` is one of five dimensions, not a separate concept). `scripts/cost-eval.sh`'s `generate_comparison_report()` function is updated to run the judge step before rendering.

**Tech Stack:** bash (existing), python3 stdlib only (`json`, `re`, `subprocess`, `sys`, `pathlib`, `datetime` — no new pip dependencies, no `claude_agent_sdk`), the `claude` CLI (already a hard requirement of this repo), the existing `templates/report.html.tmpl`.

## Global Constraints

- No new Python dependencies (no `claude_agent_sdk`, no `pypandoc`) — use `python3` stdlib + `subprocess` to shell out to the `claude` CLI, matching `scripts/cost-eval.sh`'s existing invocation pattern.
- Rubric dimensions and descriptions are ported **verbatim** from `impl-8:task07-claude-code-rfp-agent/rfp_eval/judge.py`'s `RUBRIC` list: `completeness`, `specificity`, `actionability`, `risk_depth`, `correctness` (in that exact order) — do not invent different wording.
- The judge prompt scores **all three strategies in one combined `claude` call** (not three separate calls), mirroring the reference's `build_judge_prompt` — this keeps relative scoring consistent and keeps API cost to one invocation per report build.
- `outputs/runs/comparison-cost-eval/quality.json` is a cache: if it already exists, `scripts/judge_quality.py` must skip invoking `claude` entirely (unless `--force` is passed) and exit 0 immediately.
- The three run directories/labels remain fixed: `run-01-baseline` → "Baseline", `run-02-agent-teams` → "Agent Teams", `run-03-dynamic-workflow` → "Dynamic Workflow" (unchanged from the prior plan).
- `templates/report.html.tmpl`'s Chart.js logic/data-field names must remain unchanged (as in the prior plan) — only the four pieces of visible copy that the prior plan changed to "Risk safety" wording are reverted to their original "Quality" wording.
- This plan builds directly on top of the previous plan's completed work (commits `2e56059`..`b339690` on branch `impl-9`) — do not redo Tasks 1-3 of `docs/superpowers/plans/2026-07-06-cost-eval-comparison-report.md`.

---

### Task 1: LLM-judge script with caching

**Files:**
- Create: `scripts/judge_quality.py`

**Interfaces:**
- Consumes: `outputs/runs/<dir>/proposal-*.md` and `outputs/runs/<dir>/risk-assessment-*.html` for each of the three run directories (confirmed present: `outputs/runs/run-01-baseline/proposal-acme-corp-2026-07-06.md`, `outputs/runs/run-01-baseline/risk-assessment-acme-corp-2026-07-06.html`, and the same pattern for `run-02-agent-teams` and `run-03-dynamic-workflow`). Consumes the `claude` CLI, invoked as `claude -p <prompt> --model sonnet --output-format json --permission-mode bypassPermissions`, whose stdout is a JSON envelope with a top-level `"result"` string field (confirmed via `outputs/runs/run-01-baseline/cost-eval.json`, which has key `result` among `type, subtype, is_error, ..., result, stop_reason, ...`).
- Produces: `outputs/runs/comparison-cost-eval/quality.json`, a JSON array of `{"strategy_key": str, "scores": {"completeness": int, "specificity": int, "actionability": int, "risk_depth": int, "correctness": int}, "total": int, "rationale": str}`, one object per strategy. Run as `python3 scripts/judge_quality.py` (no args) or `python3 scripts/judge_quality.py --force` (re-judges even if cache exists). Exits 0 whether it judged or skipped (cache hit); exits non-zero with an error on stderr if the `claude` CLI invocation fails or its output can't be parsed.

- [ ] **Step 1: Write the script**

```python
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
    result = subprocess.run(
        ["claude", "-p", prompt, "--model", model, "--output-format", "json",
         "--permission-mode", "bypassPermissions"],
        capture_output=True, text=True, check=True,
    )
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
```

- [ ] **Step 2: Make it executable**

Run: `chmod +x scripts/judge_quality.py`

- [ ] **Step 3: Run it for real against the real, already-existing run artifacts**

Run: `cd /Users/vadim_dissa/dev/black-belt/codespaces/claude-practice/task07-claude-code-rfp-agent && python3 scripts/judge_quality.py`

This makes one real `claude` CLI call (costs a small amount of real API usage — acceptable, this is the actual feature being built and verified, not something to mock). Expected: prints `wrote outputs/runs/comparison-cost-eval/quality.json`, exit code 0. This may take up to a minute or two since it embeds ~36KB of prompt content across three strategies' artifacts.

- [ ] **Step 4: Sanity-check the judged output**

Run: `python3 -c "import json; d=json.load(open('outputs/runs/comparison-cost-eval/quality.json')); [print(s['strategy_key'], s['scores'], s['total'], '-', s['rationale']) for s in d]"`

Expected: exactly 3 entries, one per `run-01-baseline`, `run-02-agent-teams`, `run-03-dynamic-workflow` (strategy keys must match these three exactly — the judge prompt was built with these as the dict keys, so the LLM should echo them back verbatim), each with all 5 rubric dimensions scored 1-5, a `total` between 5 and 25, and a non-empty one-sentence `rationale`. If a strategy key doesn't match (e.g. the model renamed it), that's a real defect — report DONE_WITH_CONCERNS or BLOCKED, don't paper over it.

- [ ] **Step 5: Verify the cache actually skips re-judging**

Run: `python3 scripts/judge_quality.py`

Expected: prints `quality cache already exists at outputs/runs/comparison-cost-eval/quality.json (use --force to re-judge)`, exit code 0, and does **not** make another `claude` CLI call (you'll notice — no multi-second delay this time, and `quality.json`'s content/mtime is unchanged; check with `ls -la outputs/runs/comparison-cost-eval/quality.json` before and after to confirm the mtime didn't change).

- [ ] **Step 6: Commit**

```bash
git add scripts/judge_quality.py outputs/runs/comparison-cost-eval/quality.json
git commit -m "Add LLM-judge quality rubric script with caching"
```

---

### Task 2: Consume the rubric in the report builder, revert template wording, wire into cost-eval.sh

**Files:**
- Modify: `scripts/generate_comparison_report.py` (full rewrite of the file's content, shown below — drops all clause-parsing/risk-category logic from the prior plan, replaced with loading `quality.json`)
- Modify: `templates/report.html.tmpl` (revert 4 pieces of copy from "Risk safety" wording back to "Quality" wording — the exact opposite of the prior plan's Task 3 edits)
- Modify: `scripts/cost-eval.sh` (update `generate_comparison_report()` to run the judge step first)

**Interfaces:**
- Consumes: `outputs/runs/comparison-cost-eval/quality.json` from Task 1 (array of `{strategy_key, scores, total, rationale}`). Consumes `outputs/runs/<dir>/cost-eval.metrics.json` (unchanged shape from the prior plan). Consumes `outputs/runs/<dir>/risk-assessment-*.html` only to extract the `<h1>` title text for the report header (no clause parsing anymore).
- Produces: `outputs/runs/comparison-cost-eval/report.html` + `report-data.json`, now with `strategies[].quality` containing the 5 real rubric dimensions + `total` + `rationale` instead of the prior plan's Financial/Legal/Operational safety scores.

- [ ] **Step 1: Replace the full content of `scripts/generate_comparison_report.py`**

```python
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
```

- [ ] **Step 2: Revert the 4 pieces of template copy back to "Quality" wording**

In `templates/report.html.tmpl`, find:
```html
    <div class="card"><h2>Risk safety by category (0=worst, 5=safest)</h2><canvas id="quality"></canvas></div>
    <div class="card"><h2>Risk safety per dollar</h2><canvas id="value"></canvas></div>
```
Replace with:
```html
    <div class="card"><h2>Quality by rubric dimension</h2><canvas id="quality"></canvas></div>
    <div class="card"><h2>Quality per dollar</h2><canvas id="value"></canvas></div>
```

Find:
```js
  (wq ? `<span class="winner">🏆 Safest: ${wq.label}</span>` : '') +
  (wv ? `<span class="winner">💰 Best value (safety/$): ${wv.label}</span>` : '');
```
Replace with:
```js
  (wq ? `<span class="winner">🏆 Best quality: ${wq.label}</span>` : '') +
  (wv ? `<span class="winner">💰 Best value: ${wv.label}</span>` : '');
```

Find:
```js
  data: { labels, datasets: [{ label: 'Risk safety / $',
```
Replace with:
```js
  data: { labels, datasets: [{ label: 'Quality / $',
```

Find:
```js
  ['Risk safety', s => s.quality.total], ['Safety/$', s => s.quality_per_dollar.toFixed(1)]];
```
Replace with:
```js
  ['Quality', s => s.quality.total], ['Q/$', s => s.quality_per_dollar.toFixed(1)]];
```

- [ ] **Step 3: Update `generate_comparison_report()` in `scripts/cost-eval.sh` to run the judge first**

In `scripts/cost-eval.sh`, find:
```bash
generate_comparison_report() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "error: python3 not found on PATH (required for report generation)" >&2
    return 1
  fi
  python3 scripts/generate_comparison_report.py "${COMPARISON_OUT_DIR}/report.html"
}
```
Replace with:
```bash
generate_comparison_report() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "error: python3 not found on PATH (required for report generation)" >&2
    return 1
  fi
  if [[ ! -f "${COMPARISON_OUT_DIR}/quality.json" ]] && ! command -v claude >/dev/null 2>&1; then
    echo "error: claude CLI not found on PATH (required to judge quality — no cached ${COMPARISON_OUT_DIR}/quality.json found)" >&2
    return 1
  fi
  python3 scripts/judge_quality.py || return 1
  python3 scripts/generate_comparison_report.py "${COMPARISON_OUT_DIR}/report.html"
}
```

Also update the file's top-of-file usage comment: find the line `# Requires: claude CLI, jq (not required for --report-only), python3` and replace with `# Requires: claude CLI, jq (claude only needed the first time --report-only judges quality; cached afterward), python3`.

- [ ] **Step 4: Verify syntax**

Run: `bash -n scripts/cost-eval.sh`
Expected: no output, exit code 0.

- [ ] **Step 5: Regenerate the report end-to-end via `--report-only` (quality.json is already cached from Task 1, so this should NOT invoke `claude` again)**

Run: `bash scripts/cost-eval.sh --report-only`

Expected: prints the `quality cache already exists...` line from `judge_quality.py`, then `wrote outputs/runs/comparison-cost-eval/report.html` and `wrote outputs/runs/comparison-cost-eval/report-data.json`, exit code 0. This should complete in a few seconds (no new `claude` call).

- [ ] **Step 6: Verify the regenerated report contains real rubric data and no leftover "Risk safety" wording**

Run:
```bash
grep -n "Risk safety\|Safest\|safety/\$" templates/report.html.tmpl outputs/runs/comparison-cost-eval/report.html
```
Expected: **no matches** (both files should be clean of the prior plan's risk-safety wording).

Run:
```bash
python3 -c "
import json
d = json.load(open('outputs/runs/comparison-cost-eval/report-data.json'))
print('rubric_dims:', d['rubric_dims'])
print('winner_quality:', d['winner_quality'], '| winner_value:', d['winner_value'])
for s in d['strategies']:
    print(s['label'], s['quality'])
"
```
Expected: `rubric_dims` is exactly `['completeness', 'specificity', 'actionability', 'risk_depth', 'correctness']`; each strategy's `quality` dict has all 5 dims (1-5 each), a `total`, and a non-empty `rationale` string matching Task 1's judged output.

- [ ] **Step 7: Verify the missing-quality-cache error path**

Run: `mv outputs/runs/comparison-cost-eval/quality.json /tmp/quality.json.bak && python3 scripts/generate_comparison_report.py outputs/runs/comparison-cost-eval/report.html; echo "exit: $?"; mv /tmp/quality.json.bak outputs/runs/comparison-cost-eval/quality.json`

Expected: a `FileNotFoundError` mentioning "run scripts/judge_quality.py first" printed to stderr, `exit: 1`. Confirm the final `mv` restored the file with `ls outputs/runs/comparison-cost-eval/quality.json`.

- [ ] **Step 8: Commit**

```bash
git add scripts/generate_comparison_report.py scripts/cost-eval.sh templates/report.html.tmpl outputs/runs/comparison-cost-eval
git commit -m "Replace risk-category radar with LLM-judged quality rubric in comparison report"
```

---

## Self-Review Notes

- This plan intentionally supersedes the risk-category-radar design from the prior plan's Task 3 — that work is not wasted (the underlying `scripts/generate_comparison_report.py` structure, `cost-eval.sh` wiring, and output path all carry forward), but the specific Financial/Legal/Operational categorization and its regex-based clause parsing are removed entirely, resolving the earlier final-review's flagged concern about fragile JS-regex parsing as a side effect.
- The rubric wording is copied verbatim from a real, previously-tested reference implementation (`impl-8:task07-claude-code-rfp-agent/rfp_eval/judge.py`) rather than invented, per the user's explicit request to "use correctness, completeness, specificity, risk_depth, actionability approach."
- Running the real judge (Task 1 Step 3) incurs one real `claude` CLI call — this is the feature being verified, not something to mock, consistent with how every other verification step in this project's plans has run real commands against real data.
