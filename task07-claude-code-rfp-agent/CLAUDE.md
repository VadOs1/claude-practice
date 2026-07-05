# CLAUDE.md — Task 07: RFP Agent + Strategy Evaluation

Guidance for working in `task07-claude-code-rfp-agent/`. This directory contains
two things that share one set of `.claude/` agents and skills:

1. **The RFP deal-desk agents/skills** (`.claude/`) — a Claude Code setup that
   turns an inbound RFP into a branded proposal (`.docx`) plus an internal risk
   dashboard (`.html`).
2. **`rfp_eval/`** — a Claude Agent SDK harness that runs the RFP through three
   strategies, measures real cost + quality, and renders a comparison report.
   This is Task A (comparison) and Task B (the SDK swarm) unified in one project.

---

## Quick start

```bash
# from task07-claude-code-rfp-agent/

# Run the full evaluation (spends real tokens — 3 agent runs + 1 judge run)
uv run python -m rfp_eval --rfp synthetic-data/rfp-acme-corp.md --out outputs
open outputs/eval/index.html

# Or drive it from Claude Code:
/rfp-eval

# Run the test suite (no tokens spent — every SDK call is faked)
uv run pytest -q
```

All Python/pytest runs go through `uv run ...` (uv project, Python ≥3.14).
`import rfp_eval` resolves via `pythonpath`/`testpaths` in the **repo-root**
`pyproject.toml` (`[tool.pytest.ini_options]`), so run pytest from the repo root.

---

## What it does (one paragraph)

The harness runs the Acme RFP through three Claude Code strategies —
**single agent**, an Agent-SDK coordinator→specialists **swarm**, and a
**dynamic workflow** — concurrently on the `claude-agent-sdk`. Each run's
terminal `ResultMessage` reports *real* cost and token usage, so the comparison
uses measured numbers, not estimates. An LLM judge scores each strategy's output
artifacts against a fixed rubric, and the results are rendered into a
self-contained Chart.js dashboard at `outputs/eval/index.html`.

---

## Directory layout

```
task07-claude-code-rfp-agent/
├── CLAUDE.md                      # this file
├── index.md                      # the original task description (A/B/C)
├── .claude/
│   ├── settings.json             # env: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
│   ├── commands/rfp-eval.md      # the /rfp-eval slash command
│   ├── agents/*.md               # RFP specialist agent definitions (Claude Code)
│   └── skills/*/SKILL.md         # pricing / legal / competitive / risk / docx
├── synthetic-data/               # sample RFP + past-wins.json + product-overview
├── outputs/                      # generated artifacts (git-ignored contents)
│   ├── runs/<strategy>/          # proposal.docx, risk-assessment.html, run.json
│   └── eval/                     # metrics.json, quality.json, index.html
├── rfp_eval/                     # the Python harness (see below)
└── tests/                        # one test module per rfp_eval module
```

---

## The `rfp_eval` package — module map

Each module has one responsibility. Data flows left→right:

```
strategies ─┬─▶ sdk_runner ─▶ metrics ─┐
   swarm ───┘                          ├─▶ report ─▶ index.html
                         judge ────────┘
                    orchestrator wires it all; __main__ is the CLI
```

| Module | Responsibility | Key public API |
|---|---|---|
| `strategies.py` | What each non-swarm strategy is (prompt + options) | `STRATEGY_KEYS`, `LABELS`, `build_call(key, *, task_dir, rfp_path, out_dir, model=None) -> (prompt, ClaudeAgentOptions)`, `render_prompt` |
| `swarm.py` | **Task B** — the coordinator→specialists SDK swarm | `WORKERS: dict[str, AgentDefinition]`, `COORDINATOR_SYSTEM`, `build_swarm_call(...)` |
| `sdk_runner.py` | Run one `query()` to completion, normalize its result | `RunResult(key, result_text, raw)`, `result_to_dict(msg)`, `async run_query(prompt, *, options, key, query_fn) -> RunResult` |
| `metrics.py` | Cost/token math from a run's raw dict | `RunMetrics` (10 fields), `extract_metrics(key, raw)`, `metrics_as_dict(m)` |
| `judge.py` | LLM-judge output quality against a rubric | `RUBRIC`, `RUBRIC_DIMS`, `QualityScore`, `read_artifacts`, `build_judge_prompt`, `parse_judge_output`, `async judge_quality(...)` |
| `report.py` | Merge metrics+scores, render/write the dashboard | `build_report_data(...)`, `render_report(...)`, `write_report(...)`, `DEFAULT_TEMPLATE`, `rubric_dims()` |
| `templates/report.html.tmpl` | The HTML/JS/CSS shell (Chart.js via CDN) | `__REPORT_DATA__` injection marker |
| `orchestrator.py` | Async end-to-end flow | `async run_evaluation(*, task_dir, rfp_path, out_root, model, query_fn, judge_query_fn) -> Path` |
| `__main__.py` | argparse CLI | `main(argv=None) -> int` → `asyncio.run(run_evaluation(...))` |

---

## How a run works, step by step

1. `__main__.main()` parses `--rfp`/`--out`/`--task-dir`/`--model` and calls
   `asyncio.run(run_evaluation(...))`.
2. `run_evaluation` launches all three strategies **concurrently** with
   `asyncio.gather(..., return_exceptions=True)`. Each is one `_run_one(key)`.
3. `_run_one` asks `strategies.build_call(key, ...)` for a `(prompt, options)`
   pair (the `swarm` key delegates to `swarm.build_swarm_call`), then
   `sdk_runner.run_query` drives the `claude_agent_sdk.query()` to completion.
4. Each run writes its artifacts (`proposal.docx`, `risk-assessment.html`) and a
   `run.json` under `outputs/runs/<strategy>/`. A crashed run is normalized to a
   failed `RunResult(is_error=True)` so the other two still produce a report.
5. `metrics.extract_metrics` turns each `ResultMessage` into `RunMetrics` (real
   `total_cost_usd` + token counts) → `outputs/eval/metrics.json`.
6. `judge.read_artifacts` collects each run's outputs (HTML + docx→text via
   pandoc, budgeted per-artifact), `judge.judge_quality` scores them against the
   rubric → `outputs/eval/quality.json`.
7. `report.build_report_data` merges metrics + scores (adds `quality_per_dollar`,
   `winner_quality`, `winner_value`); `render_report` injects the JSON into the
   template; `write_report` writes `outputs/eval/index.html`.

---

## Key design decisions (do not break these)

- **Runs on the Agent SDK for *real* cost.** The whole point of using
  `claude-agent-sdk` over a markdown-only setup is that each run's
  `ResultMessage` returns actual `total_cost_usd` + `usage` in-process. Cost
  numbers in the report are measured, never estimated.

- **Strategies differ by prompt + options, not flags.** "Agent teams" is a
  session/settings toggle and "dynamic workflow" is prompt-driven — there is no
  per-run CLI flag for them. All differentiation lives in `strategies.py` /
  `swarm.py`. Keep it data-driven.

- **Project agents/skills are loaded via `setting_sources=["project"]` + `cwd`.**
  Every strategy's `ClaudeAgentOptions` sets `cwd=<task dir>` and
  `setting_sources=["project"]`, so runs pick up `.claude/agents`, `.claude/skills`,
  and `.claude/settings.json` (which sets `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).

- **`permission_mode="bypassPermissions"`.** Runs are unattended and must write
  files + run bash/skills. This is intentional and scoped to this task dir via
  `cwd` — never widen it.

- **Everything SDK is dependency-injected for token-free tests.** Functions that
  hit the SDK take a `query_fn` (defaulting to the real `query`, imported
  *lazily*). `run_evaluation`'s `query_fn` is a **factory** `(out_dir) -> query_fn`
  so tests vary behavior per run; `judge_query_fn` is a plain async query fn.
  When `None`, both fall through to the real SDK.

- **Messages are duck-typed.** A message is the result if it has a
  `total_cost_usd` attribute; assistant text is any message with a `content` list
  of blocks that may carry `.text`. This keeps tests free of SDK message classes
  (they use `types.SimpleNamespace`).

- **SDK field names that must stay exact:** `ResultMessage.total_cost_usd`,
  `.usage`, `.model_usage`, `.num_turns`, `.duration_ms`, `.is_error`,
  `.result`; usage token keys `input_tokens` / `output_tokens` /
  `cache_read_input_tokens` / `cache_creation_input_tokens`. `AgentDefinition(
  description, prompt, tools, model, skills)`. `ClaudeAgentOptions(agents,
  setting_sources, cwd, model, system_prompt, permission_mode, allowed_tools)`.

- **Token totals *and* cost are computed from `model_usage`, not the
  top-level `usage`/`total_cost_usd` fields, whenever `model_usage` is
  present.** `ResultMessage.usage` and `ResultMessage.total_cost_usd` only
  reflect the top-level query's own turns; neither includes tokens or cost
  spent by subagents dispatched via the Task tool (e.g. the swarm strategy's
  coordinator + specialists). `ResultMessage.model_usage` is a `{model_name:
  {inputTokens, outputTokens, cacheReadInputTokens, cacheCreationInputTokens,
  costUSD}}` map (camelCase — passed through unmodified from the CLI) that
  aggregates every model invoked during the call, including subagents.
  `metrics.extract_metrics` sums across `model_usage.values()` (tokens *and*
  `costUSD`) when non-empty, falling back to `usage`/`total_cost_usd` only
  when `model_usage` is absent (older cached `run.json` files, or fakes in
  tests). Without this, multi-agent strategies look artificially cheap on
  both tokens and cost on the dashboard despite driving up real spend —
  mirrors `scripts/cost-eval.sh`, which sums `modelUsage[].costUSD` for the
  same reason (the CLI's top-level `total_cost_usd` likewise excludes
  subagent cost).

---

## The swarm (Task B)

`swarm.py` defines five specialist workers as `AgentDefinition`s, each bound to a
project skill, coordinated by a system-prompted "Senior Partner" query:

| Worker | Skill | Notes |
|---|---|---|
| `pricing` | `pricing-playbook` | commercial terms |
| `legal` | `legal-checklist` | contract flags |
| `technical-fit` | `competitive-intel` | stand-in — no dedicated tech-fit skill exists |
| `competitive` | `competitive-intel` | positioning |
| `risk-assessment` | `risk-assessment` | has `Write` tool — produces the HTML dashboard |

`build_swarm_call` returns options with `agents=WORKERS` +
`system_prompt=COORDINATOR_SYSTEM`, so the coordinator delegates to the workers.

---

## Testing conventions

- **No real agent/CLI in the suite.** Every test injects a fake `query_fn`
  (async generator yielding `SimpleNamespace` messages) and drives async code via
  `asyncio.run(...)` — there is no `pytest-asyncio` dependency.
- **TDD.** One test module per source module in `tests/`. Add a failing test
  before implementing; keep test output pristine (no warnings).
- Run: `uv run pytest -q` (28 tests as of the last review).

---

## Outputs & git

`outputs/` is tracked but its generated contents are ignored via
`outputs/.gitignore` (`runs/`, `eval/`, `*.docx`, `*.html`), with `.gitkeep` and
`.gitignore` kept. The generated `index.html` is a deliverable but intentionally
untracked — regenerate it with a run.

---

## Gotchas

- **The live smoke run spends real tokens** (3 agent runs + 1 judge run, several
  minutes). Use it to validate end-to-end; the test suite does not exercise it.
- **A failed strategy still renders.** `run_evaluation` uses
  `return_exceptions=True`; a crashed run shows `is_error: true` and zeros rather
  than aborting the whole evaluation. Inspect that run's `run.json`.
- **`import rfp_eval` needs the root pytest config.** If imports fail, you're
  likely running from the wrong directory — pytest is configured at the repo root.
