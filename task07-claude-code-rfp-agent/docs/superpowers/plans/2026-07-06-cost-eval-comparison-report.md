# Cost/Risk Comparison Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `scripts/cost-eval.sh` so that, after running the three RFP strategies (or on demand via a new `--report-only` flag), it builds a cost/risk comparison report from each run's `cost-eval.metrics.json` + `risk-assessment-*.html` and renders it into `templates/report.html.tmpl`, saved to `outputs/runs/comparison-cost-eval/report.html`.

**Architecture:** A new Python helper (`scripts/generate_comparison_report.py`) reads the three fixed run directories (`run-01-baseline`, `run-02-agent-teams`, `run-03-dynamic-workflow`), parses cost/token metrics from their `cost-eval.metrics.json` and risk data by regex-extracting the embedded `const clauses = [...]` JS array out of their `risk-assessment-*.html`, buckets clause risk into three categories (Financial/Legal/Operational), turns each category into a 0–5 "risk safety score" (5 = no risk carried, 0 = worst case), and emits the `REPORT_DATA` JSON the existing template already expects (`strategies[].quality`, `.quality_per_dollar`, `rubric_dims`, `winner_quality`, `winner_value`). `cost-eval.sh` gets a `--report-only` mode that validates all three runs' outputs exist and (re)generates just the report, plus it now auto-generates the report at the end of a normal full run when all three runs' outputs are present.

**Tech Stack:** bash (existing), python3 (already present via `.venv`, no new dependencies), the existing `templates/report.html.tmpl` (Chart.js, loaded from CDN, unchanged JS logic).

## Global Constraints

- No new Python/bash dependencies — use only `python3` stdlib (`json`, `re`, `pathlib`, `datetime`) and existing `jq`.
- Must be run from `task07-claude-code-rfp-agent/` (same requirement as existing `cost-eval.sh`).
- The three run directories and their labels are fixed: `run-01-baseline` → "Baseline", `run-02-agent-teams` → "Agent Teams", `run-03-dynamic-workflow` → "Dynamic Workflow" (matches `run_dir_for()` in `scripts/cost-eval.sh:15-22`).
- Risk category assignment (fixed, derived from clause ids currently in `risk-assessment-*.html`): Financial = `discount, pricefreeze, net90, mfn`; Legal = `liability, ip, indemnity`; Operational = `termnotice, slaterm, subprocessor, audit, slalevel`.
- Output report path: `outputs/runs/comparison-cost-eval/report.html` (a sibling `report-data.json` is also written for auditability).
- Do not modify the Chart.js/JS logic in `templates/report.html.tmpl` — only retitle the two panel headers that currently say "Quality" so the rendered report reads as risk, not quality.

---

### Task 1: Python report-data builder

**Files:**
- Create: `scripts/generate_comparison_report.py`

**Interfaces:**
- Consumes: `outputs/runs/run-01-baseline/cost-eval.metrics.json` (and the two sibling run dirs), each with shape `{command, cost_usd, orchestrator_cost_usd, num_turns, duration_ms, tokens: {input_tokens, output_tokens, cache_creation_input_tokens, cache_read_input_tokens}, per_model}` (confirmed against `outputs/runs/run-01-baseline/cost-eval.metrics.json`). Consumes `outputs/runs/<dir>/risk-assessment-*.html`, each embedding a JS array literal `const clauses = [ {id: '...', name: '...', risk: <float>, severity: '...', state: 'accepted'|'counter'|'rejected', counter: '...', consequence?: '...'}, ... ];` (confirmed against `outputs/runs/run-01-baseline/risk-assessment-acme-corp-2026-07-06.html:277-360`).
- Produces: prints nothing; when run as `python3 scripts/generate_comparison_report.py <output_html_path>` it writes `<output_html_path>` (rendered report) and `<output_html_path's dir>/report-data.json` (raw `REPORT_DATA`). Exits non-zero with a message on `stderr` if any required input file is missing or unparseable.

- [ ] **Step 1: Write the script**

```python
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
```

- [ ] **Step 2: Make it executable**

Run: `chmod +x scripts/generate_comparison_report.py`

- [ ] **Step 3: Run it against the real, already-existing run outputs and verify it succeeds**

Run: `cd /Users/vadim_dissa/dev/black-belt/codespaces/claude-practice/task07-claude-code-rfp-agent && python3 scripts/generate_comparison_report.py outputs/runs/comparison-cost-eval/report.html`

Expected: prints `wrote outputs/runs/comparison-cost-eval/report.html` and `wrote outputs/runs/comparison-cost-eval/report-data.json`, exit code 0.

- [ ] **Step 4: Sanity-check the generated data**

Run: `python3 -c "import json; d=json.load(open('outputs/runs/comparison-cost-eval/report-data.json')); print(d['rfp']); print(d['winner_quality'], d['winner_value']); [print(s['label'], s['cost_usd'], s['quality'], s['net_risk_pct']) for s in d['strategies']]"`

Expected: 3 strategy rows print with plausible cost (~$0.3–$1), `quality` dict with `Financial`, `Legal`, `Operational`, `total` keys each between 0 and 5, and `net_risk_pct` roughly matching the "NET RISK X%" values already visible in each `risk-assessment-*.html` (8.0, 8.3, 8.0 at time of writing — confirm the printed `net_risk_pct` for each strategy is close to those numbers, since this cross-checks the regex parser against the file's own JS-computed total).

- [ ] **Step 5: Verify missing-input handling**

Run: `mv outputs/runs/run-02-agent-teams/cost-eval.metrics.json /tmp/ && python3 scripts/generate_comparison_report.py outputs/runs/comparison-cost-eval/report.html; echo "exit: $?"; mv /tmp/cost-eval.metrics.json outputs/runs/run-02-agent-teams/`

Expected: a `FileNotFoundError` traceback printed to stderr and `exit: 1`. The final `mv` restores the file — confirm with `ls outputs/runs/run-02-agent-teams/cost-eval.metrics.json` that it's back before continuing.

- [ ] **Step 6: Commit**

```bash
git add scripts/generate_comparison_report.py
git commit -m "Add python builder for cost/risk comparison report data"
```

---

### Task 2: Wire `--report-only` into `cost-eval.sh` and auto-generate the report on a full run

**Files:**
- Modify: `scripts/cost-eval.sh` (full rewrite of the file's content, shown below)

**Interfaces:**
- Consumes: `scripts/generate_comparison_report.py <output_html_path>` from Task 1 (exit 0 on success, non-zero + stderr message on failure).
- Produces: `scripts/cost-eval.sh --report-only` (new invocation form) and unchanged existing invocation forms (`scripts/cost-eval.sh`, `scripts/cost-eval.sh rfp-02-agent-teams`, etc.) which now additionally attempt report generation at the end.

- [ ] **Step 1: Read the current file for reference**

The current file is `scripts/cost-eval.sh` (101 lines) — the version already read during planning. The rewrite below preserves every existing line's behavior and only adds: the `--report-only` flag parsing, two new functions (`check_report_inputs_ready`, `generate_comparison_report`), a report-only early-exit branch, a report attempt at the very end, and an updated usage comment.

- [ ] **Step 2: Replace the full file content**

Write the following as the complete new content of `scripts/cost-eval.sh`:

```bash
#!/usr/bin/env bash
#
# Usage:
#   scripts/cost-eval.sh                 # run all 3 strategies, then build comparison report
#   scripts/cost-eval.sh rfp-02-agent-teams # run just one (report only builds if all 3 exist)
#   scripts/cost-eval.sh --report-only   # skip running strategies; just (re)build the
#                                         # comparison report from existing run-01/02/03 outputs
#
# Requires: claude CLI, jq (not required for --report-only), python3
# Must be run from the task07-claude-code-rfp-agent/ directory (relative
# paths in the commands assume it).

set -euo pipefail

PERMISSION_MODE="${PERMISSION_MODE:-bypassPermissions}"

REPORT_ONLY=0
if [[ "${1:-}" == "--report-only" ]]; then
  REPORT_ONLY=1
  shift
  if [[ $# -gt 0 ]]; then
    echo "error: --report-only does not take additional arguments" >&2
    exit 1
  fi
fi

run_dir_for() {
  case "$1" in
    rfp-01-baseline) echo "run-01-baseline" ;;
    rfp-02-agent-teams) echo "run-02-agent-teams" ;;
    rfp-03-dynamic-workflow) echo "run-03-dynamic-workflow" ;;
    *) echo "cost/$1" ;;
  esac
}

REPORT_RUN_DIRS=(run-01-baseline run-02-agent-teams run-03-dynamic-workflow)
COMPARISON_OUT_DIR="outputs/runs/comparison-cost-eval"

check_report_inputs_ready() {
  local dir
  for dir in "${REPORT_RUN_DIRS[@]}"; do
    if [[ ! -f "outputs/runs/${dir}/cost-eval.metrics.json" ]]; then
      echo "missing: outputs/runs/${dir}/cost-eval.metrics.json" >&2
      return 1
    fi
    if ! compgen -G "outputs/runs/${dir}/risk-assessment-*.html" > /dev/null; then
      echo "missing: outputs/runs/${dir}/risk-assessment-*.html" >&2
      return 1
    fi
  done
  return 0
}

generate_comparison_report() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "error: python3 not found on PATH (required for report generation)" >&2
    return 1
  fi
  python3 scripts/generate_comparison_report.py "${COMPARISON_OUT_DIR}/report.html"
}

if [[ ! -d .claude/commands ]]; then
  echo "error: run this from task07-claude-code-rfp-agent/ (no .claude/commands here)" >&2
  exit 1
fi

if [[ $REPORT_ONLY -eq 1 ]]; then
  if ! check_report_inputs_ready; then
    echo "error: --report-only requires cost-eval + risk-assessment outputs for all 3 runs (${REPORT_RUN_DIRS[*]})" >&2
    exit 1
  fi
  generate_comparison_report
  exit 0
fi

COMMANDS=(
  rfp-01-baseline
  rfp-02-agent-teams
  rfp-03-dynamic-workflow
)

if [[ $# -gt 0 ]]; then
  COMMANDS=("$@")
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "error: claude CLI not found on PATH" >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq not found on PATH" >&2
  exit 1
fi

echo "Permission mode: $PERMISSION_MODE (override with PERMISSION_MODE=... env var)"
echo

for cmd in "${COMMANDS[@]}"; do
  if [[ ! -f ".claude/commands/${cmd}.md" ]]; then
    echo "error: no such command .claude/commands/${cmd}.md" >&2
    exit 1
  fi

  out_dir="outputs/runs/$(run_dir_for "$cmd")"
  mkdir -p "$out_dir"

  raw_file="${out_dir}/cost-eval.json"
  metrics_file="${out_dir}/cost-eval.metrics.json"

  echo "=== Running /${cmd} ==="
  claude -p "/${cmd}" \
    --output-format json \
    --permission-mode "$PERMISSION_MODE" \
    | jq '.' > "$raw_file"

  jq '{
    command: $cmd,
    cost_usd: ([.modelUsage[]] | map(.costUSD) | add // 0),
    orchestrator_cost_usd: .total_cost_usd,
    num_turns,
    duration_ms,
    tokens: (
      [.modelUsage[]] as $models
      | {
          input_tokens: ($models | map(.inputTokens) | add // 0),
          output_tokens: ($models | map(.outputTokens) | add // 0),
          cache_creation_input_tokens: ($models | map(.cacheCreationInputTokens) | add // 0),
          cache_read_input_tokens: ($models | map(.cacheReadInputTokens) | add // 0)
        }
    ),
    per_model: .modelUsage
  }' --arg cmd "$cmd" "$raw_file" > "$metrics_file"

  cost=$(jq -r '.cost_usd' "$metrics_file")
  orch_cost=$(jq -r '.orchestrator_cost_usd' "$metrics_file")
  echo "  cost_usd (all agents): \$${cost}  (orchestrator-only: \$${orch_cost})  ->  ${metrics_file}"
  echo
done

echo "=== Summary ==="
printf "%-24s %10s %12s %12s %14s %14s\n" \
  "command" "cost_usd" "input_tok" "output_tok" "cache_creat" "cache_read"
for cmd in "${COMMANDS[@]}"; do
  m="outputs/runs/$(run_dir_for "$cmd")/cost-eval.metrics.json"
  [[ -f "$m" ]] || continue
  jq -r '[.command, (.cost_usd|tostring), (.tokens.input_tokens|tostring), (.tokens.output_tokens|tostring), (.tokens.cache_creation_input_tokens|tostring), (.tokens.cache_read_input_tokens|tostring)] | @tsv' "$m" \
    | awk -F'\t' '{printf "%-24s %10s %12s %12s %14s %14s\n", $1, $2, $3, $4, $5, $6}'
done

echo
if check_report_inputs_ready; then
  echo "=== Comparison report ==="
  generate_comparison_report
else
  echo "note: skipping comparison report — not all 3 strategy runs have outputs yet" >&2
fi
```

- [ ] **Step 3: Verify script syntax**

Run: `bash -n scripts/cost-eval.sh`
Expected: no output, exit code 0.

- [ ] **Step 4: Run `--report-only` end-to-end against the real existing run outputs**

Run: `bash scripts/cost-eval.sh --report-only`
Expected output ends with:
```
wrote outputs/runs/comparison-cost-eval/report.html
wrote outputs/runs/comparison-cost-eval/report-data.json
```
exit code 0. Confirm with `ls outputs/runs/comparison-cost-eval/` that both files exist.

- [ ] **Step 5: Verify `--report-only` fails clearly when inputs are missing**

Run: `mv outputs/runs/run-03-dynamic-workflow outputs/runs/run-03-dynamic-workflow.bak && bash scripts/cost-eval.sh --report-only; echo "exit: $?"; mv outputs/runs/run-03-dynamic-workflow.bak outputs/runs/run-03-dynamic-workflow`

Expected: stderr shows `missing: outputs/runs/run-03-dynamic-workflow/cost-eval.metrics.json` followed by `error: --report-only requires cost-eval + risk-assessment outputs for all 3 runs (run-01-baseline run-02-agent-teams run-03-dynamic-workflow)`, and `exit: 1`. Confirm the final `mv` restored the directory with `ls outputs/runs/run-03-dynamic-workflow/`.

- [ ] **Step 6: Verify `--report-only` rejects extra arguments**

Run: `bash scripts/cost-eval.sh --report-only rfp-01-baseline; echo "exit: $?"`
Expected: `error: --report-only does not take additional arguments` on stderr, `exit: 1`.

- [ ] **Step 7: Commit**

```bash
git add scripts/cost-eval.sh
git commit -m "Add --report-only mode and auto-generated comparison report to cost-eval.sh"
```

---

### Task 3: Relabel the template's quality panels for a risk reading, and inspect the final report visually

**Files:**
- Modify: `templates/report.html.tmpl:39-40` (panel headers), `templates/report.html.tmpl:57-59` (winners banner labels)

**Interfaces:**
- Consumes: `REPORT_DATA` JSON produced by Task 1/2 (`strategies[].quality.{Financial,Legal,Operational,total}`, `.quality_per_dollar`, `winner_quality`, `winner_value`) — unchanged JS field names, only visible copy changes.
- Produces: `outputs/runs/comparison-cost-eval/report.html` that reads as a risk report rather than a quality report.

- [ ] **Step 1: Retitle the two panel headers**

In `templates/report.html.tmpl`, find:
```html
    <div class="card"><h2>Quality by rubric dimension</h2><canvas id="quality"></canvas></div>
    <div class="card"><h2>Quality per dollar</h2><canvas id="value"></canvas></div>
```
Replace with:
```html
    <div class="card"><h2>Risk safety by category (0=worst, 5=safest)</h2><canvas id="quality"></canvas></div>
    <div class="card"><h2>Risk safety per dollar</h2><canvas id="value"></canvas></div>
```

- [ ] **Step 2: Retitle the winners banner text**

In `templates/report.html.tmpl`, find:
```js
  (wq ? `<span class="winner">🏆 Best quality: ${wq.label}</span>` : '') +
  (wv ? `<span class="winner">💰 Best value: ${wv.label}</span>` : '');
```
Replace with:
```js
  (wq ? `<span class="winner">🏆 Safest: ${wq.label}</span>` : '') +
  (wv ? `<span class="winner">💰 Best value (safety/$): ${wv.label}</span>` : '');
```

- [ ] **Step 3: Retitle the summary table's "Quality" columns**

In `templates/report.html.tmpl`, find:
```js
  ['Quality', s => s.quality.total], ['Q/$', s => s.quality_per_dollar.toFixed(1)]];
```
Replace with:
```js
  ['Risk safety', s => s.quality.total], ['Safety/$', s => s.quality_per_dollar.toFixed(1)]];
```

- [ ] **Step 4: Regenerate the report with the relabeled template**

Run: `bash scripts/cost-eval.sh --report-only`
Expected: same success output as Task 2 Step 4.

- [ ] **Step 5: Visually inspect the report in a browser**

Run: `open outputs/runs/comparison-cost-eval/report.html` (macOS)

Confirm visually:
- Page title "RFP Strategy Comparison" with subtitle showing the RFP name and a generation timestamp.
- A winners line reading "🏆 Safest: <label>" and "💰 Best value (safety/$): <label>".
- Four charts render without console errors: Cost per strategy (bar), Token usage breakdown (stacked bar), "Risk safety by category" (radar, 3 axes: Financial/Legal/Operational), "Risk safety per dollar" (bar).
- The summary table at the bottom has columns Strategy, Cost $, Total tokens, Turns, Duration s, Risk safety, Safety/$ with 3 rows (Baseline, Agent Teams, Dynamic Workflow).

If any chart is blank or a console error appears, use `mcp__claude-in-chrome__read_console_messages` (load via `ToolSearch` first) to diagnose before proceeding.

- [ ] **Step 6: Commit**

```bash
git add templates/report.html.tmpl outputs/runs/comparison-cost-eval
git commit -m "Relabel report template for risk framing; commit generated comparison report"
```

---

## Self-Review Notes

- **Scope decision made without user confirmation** (the `AskUserQuestion` call was interrupted before the user answered): risk is broken into 3 categories (Financial/Legal/Operational) via a hardcoded clause-id map, normalized to a 0–5 "safety score" per category reusing the template's existing `quality`/`quality_per_dollar` JSON keys unchanged, with only visible panel/table copy relabeled from "Quality" to "Risk safety". If this mapping or the category groupings feel wrong once you see the rendered report in Task 3 Step 5, flag it — the clause→category map in `scripts/generate_comparison_report.py` (`RISK_CATEGORIES` dict) is the one place to adjust it.
- Output path `outputs/runs/comparison-cost-eval/report.html` matches your direct instruction.
- The `--report-only` flag hard-fails with a listing of exactly which run's files are missing, per "just generate cost/risk comparison if outputs/runs/run-01, run-02, run-03 folders and files exist."
