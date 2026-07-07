# Cost-Eval via Agent SDK — Design

## Goal

`scripts/cost-eval.sh` currently runs the three RFP-processing strategies
(`rfp-01-baseline`, `rfp-02-agent-teams`, `rfp-03-dynamic-workflow`) by
shelling out to the `claude` CLI (`claude -p "/${cmd}" --output-format
json`), extracts cost/token metrics from the JSON via `jq`, then builds a
comparison report by shelling out to `claude` again for an LLM-judged
quality rubric (`scripts/judge_quality.py`) and rendering
`templates/report.html.tmpl` (`scripts/generate_comparison_report.py`).

This spec replaces every one of those `claude` CLI invocations with calls
through the Python `claude_agent_sdk` package (already installed in
`.venv`, version 0.2.112), packaged as a new, self-contained,
from-scratch Python module — not a port of any other branch's code —
invoked by running a single Python script. The observable behavior
(prompts sent, metrics captured, report produced) mirrors
`cost-eval.sh` as closely as the CLI → SDK swap allows; the *implementation*
is new.

## Architecture

A new top-level package `sdk_eval/`, plus a thin entry-point script
`scripts/cost-eval-sdk.py` that does argument parsing and orchestration
(mirroring `cost-eval.sh`'s shell logic in Python) and delegates to the
package for the actual work.

```
sdk_eval/
├── __init__.py
├── strategies.py     # the 3 strategy definitions (key, run dir, prompt text)
├── runner.py          # runs one strategy via claude_agent_sdk.query(), returns ResultMessage
├── metrics.py           # ResultMessage -> cost-eval.metrics.json shape
├── judge.py               # LLM-judge quality rubric, via SDK instead of subprocess
└── report.py                # REPORT_DATA builder + renders templates/report.html.tmpl
scripts/
└── cost-eval-sdk.py           # CLI entry point (argparse), mirrors cost-eval.sh usage
```

`claude_agent_sdk` itself works by spawning the `claude` CLI binary as a
subprocess under the hood (that's its transport) — so the `claude` CLI
still needs to be on `PATH`, but this codebase never shells out to it
directly; all invocation goes through the SDK's `query()` / `ResultMessage`
API.

## Components

### `sdk_eval/strategies.py`

A list of 3 `Strategy` records, one per RFP-processing approach:

```python
@dataclass
class Strategy:
    key: str        # "run-01-baseline" | "run-02-agent-teams" | "run-03-dynamic-workflow"
    label: str       # "Baseline" | "Agent Teams" | "Dynamic Workflow"
    prompt: str        # full prompt text, ported verbatim from the body of
                        # .claude/commands/rfp-0{1,2,3}-*.md (everything after
                        # the frontmatter) — same instructions Claude currently
                        # receives when the CLI expands the slash command
```

Porting the prompt text (not re-deriving it) is intentional: the whole
point of the comparison is that the *strategy* is held constant and only
the invocation mechanism (CLI vs. SDK) changes.

One deliberate substitution: each source `.md` instructs Claude to save
artifacts under `outputs/runs/run-0N-.../` (the CLI reference runs'
path). Ported verbatim, an SDK-run agent — which has real `Write`/`Bash`
tool access via `cwd=repo_root` — would overwrite those already-committed
reference files. Every occurrence of `outputs/runs/run-0N-...` in the
ported prompt text is rewritten to `outputs/runs-sdk/run-0N-...` before
being stored in `Strategy.prompt`, consistent with the "Output location"
section below. This is the only text change from the source `.md` files.

### `sdk_eval/runner.py`

```python
async def run_strategy(strategy: Strategy, repo_root: Path, permission_mode: str) -> ResultMessage:
```

Calls `claude_agent_sdk.query()` with:
- `prompt=strategy.prompt`
- `options=ClaudeAgentOptions(cwd=repo_root, permission_mode=permission_mode)`

`setting_sources` is deliberately left at its default (`None`), which the
SDK docs state loads all sources ("user", "project", "local") — this
matches the CLI's own default when run from this directory, so the SDK
session discovers this repo's `.claude/agents/*.md`, `.claude/skills/*`,
and `.claude/settings.json` (which sets
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) exactly the way `claude -p`
already does — the agent-teams and dynamic-workflow strategies still
delegate to `deal-desk-orchestrator` and its five specialists, unmodified.
Explicitly passing `setting_sources=["project"]` was considered but
rejected: it would *narrow* discovery relative to the CLI default
(dropping user/local settings), which is the opposite of "exactly the
same logic."

Drains the async message stream, keeping the final `ResultMessage`
(the SDK's analogue of the CLI's single JSON object). Raises if the stream
ends without a `ResultMessage`, or if `ResultMessage.is_error` is true
(surfacing `ResultMessage.errors` / `result` in the exception).

### `sdk_eval/metrics.py`

```python
def build_metrics(strategy: Strategy, result: ResultMessage) -> dict:
```

Reproduces the exact shape `cost-eval.sh`'s `jq` filter currently produces,
sourced from `ResultMessage.model_usage` (a `dict[model_name, {...}]` with
camelCase keys `inputTokens`, `outputTokens`, `cacheCreationInputTokens`,
`cacheReadInputTokens`, `costUSD` — confirmed against a real captured
`outputs/runs/run-01-baseline/cost-eval.json`) and `total_cost_usd`:

```json
{
  "command": "<strategy.key>",
  "cost_usd": <sum of costUSD across model_usage>,
  "orchestrator_cost_usd": <result.total_cost_usd>,
  "num_turns": <result.num_turns>,
  "duration_ms": <result.duration_ms>,
  "tokens": {
    "input_tokens": <sum inputTokens>,
    "output_tokens": <sum outputTokens>,
    "cache_creation_input_tokens": <sum cacheCreationInputTokens>,
    "cache_read_input_tokens": <sum cacheReadInputTokens>
  },
  "per_model": <result.model_usage, as-is>
}
```

Written to `<run_dir>/cost-eval.metrics.json`. The raw `ResultMessage`
(as a dict) is also dumped to `<run_dir>/cost-eval.json` for parity with
the CLI path and for debugging.

### `sdk_eval/judge.py`

Same 5-dimension rubric as `scripts/judge_quality.py`
(`completeness`, `specificity`, `actionability`, `risk_depth`,
`correctness`, 1–5 each, one combined prompt scoring all 3 strategies
together) — this rubric is this repo's own established evaluation
criteria, not another branch's implementation, so it's the correct
"same logic" to preserve. The one change: `invoke_judge()` calls
`claude_agent_sdk.query()` instead of
`subprocess.run(["claude", "-p", ...])`. Same cache file semantics:
skip re-judging if `<comparison_dir>/quality.json` exists, unless
`--force`.

### `sdk_eval/report.py`

Ports `build_report_data()` / `render()` from
`scripts/generate_comparison_report.py` unchanged in logic, parameterized
on the run directory root and strategy list instead of the hardcoded
`outputs/runs` constants, and reuses the existing generic
`templates/report.html.tmpl` (a `__REPORT_DATA__` string-replace template
with no CLI-specific assumptions).

### `scripts/cost-eval-sdk.py`

Argparse CLI mirroring `cost-eval.sh`'s usage:

```
python3 scripts/cost-eval-sdk.py                    # run all 3 strategies, then build comparison report
python3 scripts/cost-eval-sdk.py rfp-02-agent-teams  # run just one
python3 scripts/cost-eval-sdk.py --report-only       # rebuild report from existing outputs only
```

- `PERMISSION_MODE` env var (default `bypassPermissions`), same as the
  bash script.
- Resolves the repo root itself (`Path(__file__).resolve().parent.parent`)
  rather than requiring the caller's `cwd` to be
  `task07-claude-code-rfp-agent/` — unlike `cost-eval.sh`, which errors
  out unless run from that directory. `repo_root` is what gets passed as
  `ClaudeAgentOptions.cwd` in `runner.py`, so the SDK session's project
  discovery works regardless of where the script is invoked from.
- Runs strategies **sequentially** (not concurrently), matching
  `cost-eval.sh`'s `for cmd in "${COMMANDS[@]}"` loop — keeps the two
  pipelines directly comparable and avoids resource contention between
  concurrent SDK sessions.
- Prints the same per-strategy cost line and final summary table
  (`command | cost_usd | input_tok | output_tok | cache_creat |
  cache_read`) as the bash script.
- After all requested strategies complete (or immediately, under
  `--report-only`), builds the comparison report if all 3 runs' metrics
  files are present — same `check_report_inputs_ready()` gate as the bash
  script.

## Output location

Writes to **`outputs/runs-sdk/`**, not `outputs/runs/`:

```
outputs/runs-sdk/
├── run-01-baseline/
│   ├── cost-eval.json
│   ├── cost-eval.metrics.json
│   ├── proposal-<customer>-<date>.md
│   ├── proposal-<customer>-<date>.docx
│   └── risk-assessment-<customer>-<date>.html
├── run-02-agent-teams/        (same shape)
├── run-03-dynamic-workflow/   (same shape)
└── comparison-cost-eval/
    ├── quality.json
    ├── report-data.json
    └── report.html
```

This keeps the existing CLI-based reference runs under `outputs/runs/`
(already committed, already feeding the existing comparison report)
untouched — the SDK pipeline is fully independent and safe to run
repeatedly without risk of clobbering prior results.

## Error handling

- `claude_agent_sdk`'s own exceptions (`CLINotFoundError`,
  `CLIConnectionError`, `CLIJSONDecodeError`) propagate with the script
  exiting non-zero and printing the error to stderr — same failure mode
  as `cost-eval.sh` exiting on a failed `claude` invocation.
- A `ResultMessage.is_error` result (successful process exit, but the
  agent turn itself errored) is treated as a hard failure for that
  strategy: printed and the script exits non-zero rather than writing a
  metrics file with garbage data.
- `--report-only` checks all 3 `cost-eval.metrics.json` files exist
  under `outputs/runs-sdk/` before attempting to build the report,
  matching `check_report_inputs_ready()`.
- Missing expected artifacts (`proposal-*.md`, `proposal-*.docx`,
  `risk-assessment-*.html`) after a strategy run are reported as a
  warning (not a hard failure — the run may still be useful for
  cost comparison even if an artifact is missing), consistent with
  how `judge.py`'s `read_artifacts()` already tolerates missing files.

## Testing

- Unit tests (no network, no live `claude` calls) for the pure-logic
  pieces:
  - `metrics.py`'s `build_metrics()` against a fixture `ResultMessage`-shaped
    object, asserting the output dict matches the shape above.
  - `judge.py`'s prompt-building and JSON-response-parsing functions
    against fixture strings, including a response wrapped in a ```json
    fence (mirrors the existing regex-based parsing in
    `scripts/judge_quality.py`).
  - `report.py`'s `build_report_data()` against fixture metrics +
    quality JSON, asserting `winner_quality` / `winner_value` selection
    and `quality_per_dollar` rounding.
- One live smoke run: `python3 scripts/cost-eval-sdk.py rfp-01-baseline`
  end-to-end, confirming real artifacts land in
  `outputs/runs-sdk/run-01-baseline/` and `cost-eval.metrics.json` has
  non-zero, plausible values, before running all 3 strategies (which
  costs real API spend across ~9+ agent invocations for the agent-teams
  and dynamic-workflow strategies).

## Non-goals

- Not modifying `scripts/cost-eval.sh`, `scripts/judge_quality.py`, or
  `scripts/generate_comparison_report.py` — those remain the CLI-based
  reference pipeline, untouched.
- Not adding a new top-level comparison report that merges CLI-based and
  SDK-based runs side by side — that's a natural future step but out of
  scope here; this spec only reproduces cost-eval.sh's own pipeline via
  the SDK, writing to its own parallel output tree.
- Not changing the underlying RFP strategies, agent definitions
  (`.claude/agents/*.md`), or skills (`.claude/skills/*`) — those are
  reused as-is via the SDK's default `setting_sources` discovery.
