# Cost-Eval via Agent SDK Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reimplement `scripts/cost-eval.sh`'s pipeline (run the 3 RFP strategies, capture cost/token metrics, LLM-judge quality, render a comparison report) as a new, self-contained Python package that uses `claude_agent_sdk` instead of shelling out to the `claude` CLI, invoked by running a single Python script.

**Architecture:** A new package `sdk_eval/` (7 small modules, one responsibility each) plus a thin entry script `scripts/cost-eval-sdk.py`. Every place `cost-eval.sh` currently shells out to `claude -p ...` is replaced with `claude_agent_sdk.query()`, whose `ResultMessage` carries the same cost/usage fields the bash script currently extracts via `jq`. Strategy prompts are ported verbatim from `.claude/commands/rfp-0{1,2,3}-*.md` (with one path substitution — see Task 1). All new output lands under `outputs/runs-sdk/`, a sibling to the existing `outputs/runs/`, so nothing already committed is touched.

**Tech Stack:** Python 3.12 (this repo's `.venv`), `claude_agent_sdk` 0.2.112 (already installed, no new dependency), stdlib only otherwise (`json`, `re`, `argparse`, `asyncio`, `dataclasses`, `pathlib`, `datetime`, `unittest` for tests — no pytest, matching the "no new Python dependencies" pattern already established by this repo's `scripts/judge_quality.py`).

## Global Constraints

- No new Python dependencies beyond `claude_agent_sdk` (already installed in `.venv`) — tests use stdlib `unittest`, not pytest.
- All new output is written under `outputs/runs-sdk/` — never `outputs/runs/`.
- `scripts/cost-eval.sh`, `scripts/judge_quality.py`, `scripts/generate_comparison_report.py`, and every existing file under `outputs/runs/` are **not modified**.
- Rubric dimensions, verbatim and in this exact order: `completeness`, `specificity`, `actionability`, `risk_depth`, `correctness` (1–5 each).
- The 3 strategies are fixed: key `rfp-01-baseline` → dir `run-01-baseline` → label `Baseline`; key `rfp-02-agent-teams` → dir `run-02-agent-teams` → label `Agent Teams`; key `rfp-03-dynamic-workflow` → dir `run-03-dynamic-workflow` → label `Dynamic Workflow`.
- `ClaudeAgentOptions.setting_sources` is left at its SDK default (`None`, meaning "load all sources: user, project, local") — never explicitly narrowed to `["project"]`. This matches the `claude` CLI's own default discovery behavior when run from this directory, which is what makes `.claude/agents/*.md` and `.claude/skills/*` available to SDK-run strategies without any extra wiring.
- Strategies run **sequentially**, not concurrently — matches `cost-eval.sh`'s `for` loop.
- Every module in `sdk_eval/` takes its paths as parameters (no hardcoded `outputs/runs` constants inside the reusable logic) so it's unit-testable with tmp directories; only `sdk_eval/cli.py` hardcodes the real `outputs/runs-sdk` paths, as the single point where "real" defaults live.

---

## File Structure

```
task07-claude-code-rfp-agent/
├── sdk_eval/
│   ├── __init__.py
│   ├── strategies.py   # Strategy dataclass + the 3 ported prompts
│   ├── metrics.py       # ResultMessage -> cost-eval.metrics.json shape
│   ├── artifacts.py       # post-run artifact presence check
│   ├── runner.py            # SDK query wrapper: prompt -> ResultMessage
│   ├── judge.py                # LLM-judge quality rubric (SDK-based)
│   ├── report.py                  # REPORT_DATA builder + template render
│   └── cli.py                        # argparse + orchestration (uses all of the above)
├── scripts/
│   └── cost-eval-sdk.py                 # entry point: `python3 scripts/cost-eval-sdk.py`
└── tests/
    └── sdk_eval/
        ├── __init__.py
        ├── test_strategies.py
        ├── test_metrics.py
        ├── test_artifacts.py
        ├── test_runner.py
        ├── test_judge.py
        ├── test_report.py
        └── test_cli.py
```

Run all tests at any point with:

```bash
cd task07-claude-code-rfp-agent && python3 -m unittest discover -s tests -t . -v
```

---

### Task 1: `sdk_eval/strategies.py` — strategy definitions

**Files:**
- Create: `sdk_eval/__init__.py` (empty file)
- Create: `sdk_eval/strategies.py`
- Test: `tests/__init__.py` (empty file)
- Test: `tests/sdk_eval/__init__.py` (empty file)
- Test: `tests/sdk_eval/test_strategies.py`

**Interfaces:**
- Produces: `Strategy` (frozen dataclass: `key: str`, `label: str`, `dir_name: str`, `prompt: str`), `STRATEGIES: list[Strategy]` (exactly 3, in baseline/agent-teams/dynamic-workflow order), `get_strategy(key: str) -> Strategy` (raises `ValueError` for an unknown key). Consumed by every later task.

- [ ] **Step 1: Create the package and test scaffolding**

```bash
mkdir -p sdk_eval tests/sdk_eval
touch sdk_eval/__init__.py tests/__init__.py tests/sdk_eval/__init__.py
```

- [ ] **Step 2: Write the failing test**

Create `tests/sdk_eval/test_strategies.py`:

```python
import unittest

from sdk_eval.strategies import STRATEGIES, get_strategy


class StrategiesTests(unittest.TestCase):
    def test_exactly_three_strategies_with_unique_keys(self):
        keys = [s.key for s in STRATEGIES]
        self.assertEqual(len(keys), 3)
        self.assertEqual(len(set(keys)), 3)

    def test_expected_keys_dirs_and_labels(self):
        by_key = {s.key: s for s in STRATEGIES}
        self.assertEqual(by_key["rfp-01-baseline"].label, "Baseline")
        self.assertEqual(by_key["rfp-01-baseline"].dir_name, "run-01-baseline")
        self.assertEqual(by_key["rfp-02-agent-teams"].label, "Agent Teams")
        self.assertEqual(by_key["rfp-02-agent-teams"].dir_name, "run-02-agent-teams")
        self.assertEqual(by_key["rfp-03-dynamic-workflow"].label, "Dynamic Workflow")
        self.assertEqual(by_key["rfp-03-dynamic-workflow"].dir_name, "run-03-dynamic-workflow")

    def test_prompts_reference_the_sdk_output_dir_not_the_cli_one(self):
        # Regression guard: verbatim-ported prompts would tell the agent to
        # write into outputs/runs/, clobbering the committed CLI reference
        # runs. Every prompt must point at outputs/runs-sdk/ instead.
        for s in STRATEGIES:
            self.assertIn(f"outputs/runs-sdk/{s.dir_name}/", s.prompt)
            self.assertNotIn("outputs/runs/run-0", s.prompt)

    def test_get_strategy_returns_matching_strategy(self):
        found = get_strategy("rfp-02-agent-teams")
        self.assertEqual(found.key, "rfp-02-agent-teams")

    def test_get_strategy_raises_for_unknown_key(self):
        with self.assertRaises(ValueError):
            get_strategy("not-a-real-strategy")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_strategies -v`
Expected: FAIL / ERROR — `ModuleNotFoundError: No module named 'sdk_eval.strategies'`

- [ ] **Step 4: Write the implementation**

Create `sdk_eval/strategies.py`:

```python
"""Strategy definitions ported from .claude/commands/rfp-0{1,2,3}-*.md.

Prompt text is copied verbatim from each command's body (everything after
the frontmatter), with one deliberate substitution: every occurrence of
the CLI reference runs' output path `outputs/runs/run-0N-...` is rewritten
to `outputs/runs-sdk/run-0N-...` so an SDK-run agent (which has real
Write/Bash tool access) never overwrites the already-committed CLI-based
reference outputs.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Strategy:
    key: str
    label: str
    dir_name: str
    prompt: str


_BASELINE_PROMPT = """Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

Produce:
1. A customer-facing proposal response covering: executive summary, our
   understanding of the customer's need, why we're the right fit, commercial
   proposal, contract approach, and risks/mitigations. Provide this as both a
   Markdown source file and a converted .docx.
2. An internal risk assessment (.html) — a self-contained interactive risk vs.
   revenue dashboard, for internal use only.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

## Expected artifacts

Save all outputs under `outputs/runs-sdk/run-01-baseline/`, producing exactly
these three files (`<customer>` and `<date>` reflect the customer name and
today's date):

- `outputs/runs-sdk/run-01-baseline/proposal-<customer>-<date>.docx`
- `outputs/runs-sdk/run-01-baseline/proposal-<customer>-<date>.md`
- `outputs/runs-sdk/run-01-baseline/risk-assessment-<customer>-<date>.html`
"""

_AGENT_TEAMS_PROMPT = """Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

Produce:
1. A customer-facing proposal response covering: executive summary, our
   understanding of the customer's need, why we're the right fit, commercial
   proposal, contract approach, and risks/mitigations. Provide this as both a
   Markdown source file and a converted .docx.
2. An internal risk assessment (.html) — a self-contained interactive risk vs.
   revenue dashboard, for internal use only.

Use the `deal-desk-orchestrator` agent to run this deal via agent team. The
orchestrator spawns five specialist teammates (Pricing Specialist, Legal
Reviewer, Technical Fit Specialist, Competitive Intel Analyst, Risk Assessment
Specialist), assigns each their scope, and synthesizes their findings. The
orchestrator must NOT perform the pricing, legal, technical-fit, competitive,
or risk-assessment analysis itself — delegate each to its specialist and
integrate their responses into the proposal and dashboard.

When the orchestrator delegates to the first four specialists (and later to
Risk Assessment), it must get two independent settings right:

- CONCURRENCY comes from batching: issue all four `Agent` calls as separate
  tool-use blocks in the SAME message. The harness runs them at the same
  time regardless of `run_in_background`.
- RETURN PATH comes from foreground vs. background: omit `run_in_background`
  (or set it to `false`) on every specialist call. Never set
  `run_in_background: true`. Foreground means each specialist's result lands
  back directly in the orchestrator's own conversation once ready.
  Background detaches the call — the orchestrator's turn ends immediately,
  and since the orchestrator is itself a spawned subagent, the completion
  notification does not come back to it directly; it surfaces to whatever
  session invoked the orchestrator, which then has to relay it second-hand.
  That relay is exactly what stalls the workflow (a dropped or delayed
  relay leaves the orchestrator waiting on a specialist that already
  finished).

So: same message (parallel), foreground (direct result, no relay). The
orchestrator must not end its turn while a specialist call is still
pending.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

## Expected artifacts

Save all outputs under `outputs/runs-sdk/run-02-agent-teams/`, producing exactly
these three files (`<customer>` and `<date>` reflect the customer name and
today's date):

- `outputs/runs-sdk/run-02-agent-teams/proposal-<customer>-<date>.docx`
- `outputs/runs-sdk/run-02-agent-teams/proposal-<customer>-<date>.md`
- `outputs/runs-sdk/run-02-agent-teams/risk-assessment-<customer>-<date>.html`
"""

_DYNAMIC_WORKFLOW_PROMPT = """Use a workflow to process the RFP at `synthetic-data/rfp-acme-corp.md`.

Orchestrate specialists to produce:
1. A customer-facing proposal response (.docx): executive summary, our
   understanding of need, fit, commercial proposal, contract approach,
   risks/mitigations.
2. An internal risk assessment (.html): interactive risk vs. revenue
   dashboard.

The workflow should dynamically decide which verification phases and agents
are needed based on RFP content. Reference `synthetic-data/past-wins.json`
and `synthetic-data/product-overview.md` as needed.

## Expected artifacts

Save all outputs under `outputs/runs-sdk/run-03-dynamic-workflow/`, producing
exactly these three files (`<customer>` and `<date>` reflect the customer
name and today's date):

- `outputs/runs-sdk/run-03-dynamic-workflow/proposal-<customer>-<date>.docx`
- `outputs/runs-sdk/run-03-dynamic-workflow/proposal-<customer>-<date>.md`
- `outputs/runs-sdk/run-03-dynamic-workflow/risk-assessment-<customer>-<date>.html`

Use ultracode.
"""

STRATEGIES = [
    Strategy(key="rfp-01-baseline", label="Baseline",
             dir_name="run-01-baseline", prompt=_BASELINE_PROMPT),
    Strategy(key="rfp-02-agent-teams", label="Agent Teams",
             dir_name="run-02-agent-teams", prompt=_AGENT_TEAMS_PROMPT),
    Strategy(key="rfp-03-dynamic-workflow", label="Dynamic Workflow",
             dir_name="run-03-dynamic-workflow", prompt=_DYNAMIC_WORKFLOW_PROMPT),
]


def get_strategy(key: str) -> Strategy:
    for s in STRATEGIES:
        if s.key == key:
            return s
    raise ValueError(
        f"unknown strategy key: {key!r} (expected one of {[s.key for s in STRATEGIES]})"
    )
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_strategies -v`
Expected: PASS (5 tests)

- [ ] **Step 6: Commit**

```bash
git add sdk_eval/__init__.py sdk_eval/strategies.py tests/__init__.py tests/sdk_eval/__init__.py tests/sdk_eval/test_strategies.py
git commit -m "Add sdk_eval strategy definitions ported from .claude/commands"
```

---

### Task 2: `sdk_eval/metrics.py` — cost/token metrics extraction

**Files:**
- Create: `sdk_eval/metrics.py`
- Test: `tests/sdk_eval/test_metrics.py`

**Interfaces:**
- Consumes: `claude_agent_sdk.ResultMessage` (fields used: `total_cost_usd`, `num_turns`, `duration_ms`, `model_usage: dict[str, dict] | None` with per-model keys `inputTokens`, `outputTokens`, `cacheCreationInputTokens`, `cacheReadInputTokens`, `costUSD`).
- Produces: `build_metrics(strategy_key: str, result: ResultMessage) -> dict` (shape: `{"command", "cost_usd", "orchestrator_cost_usd", "num_turns", "duration_ms", "tokens": {"input_tokens","output_tokens","cache_creation_input_tokens","cache_read_input_tokens"}, "per_model"}`), `save_metrics(run_dir: Path, strategy_key: str, result: ResultMessage) -> dict` (writes `run_dir/cost-eval.json` (raw `ResultMessage` as JSON) and `run_dir/cost-eval.metrics.json` (the `build_metrics` output), creating `run_dir` if needed, and returns the metrics dict). Consumed by `sdk_eval/cli.py` (Task 7).

- [ ] **Step 1: Write the failing test**

Create `tests/sdk_eval/test_metrics.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

from claude_agent_sdk import ResultMessage

from sdk_eval.metrics import build_metrics, save_metrics


def make_result(**overrides) -> ResultMessage:
    defaults = dict(
        subtype="success",
        duration_ms=45000,
        duration_api_ms=40000,
        is_error=False,
        num_turns=7,
        session_id="sess-1",
        stop_reason="end_turn",
        total_cost_usd=0.5,
        usage={},
        result="ok",
        structured_output=None,
        model_usage={
            "claude-sonnet-5": {
                "inputTokens": 22,
                "outputTokens": 26825,
                "cacheReadInputTokens": 514670,
                "cacheCreationInputTokens": 50760,
                "costUSD": 0.4,
            },
            "claude-haiku-4-5-20251001": {
                "inputTokens": 523,
                "outputTokens": 14,
                "cacheReadInputTokens": 0,
                "cacheCreationInputTokens": 0,
                "costUSD": 0.1,
            },
        },
        permission_denials=None,
        deferred_tool_use=None,
        errors=None,
        api_error_status=None,
        uuid="u-1",
    )
    defaults.update(overrides)
    return ResultMessage(**defaults)


class BuildMetricsTests(unittest.TestCase):
    def test_sums_cost_and_tokens_across_models(self):
        result = make_result()
        metrics = build_metrics("rfp-01-baseline", result)
        self.assertEqual(metrics["command"], "rfp-01-baseline")
        self.assertAlmostEqual(metrics["cost_usd"], 0.5)
        self.assertEqual(metrics["orchestrator_cost_usd"], 0.5)
        self.assertEqual(metrics["num_turns"], 7)
        self.assertEqual(metrics["duration_ms"], 45000)
        self.assertEqual(metrics["tokens"], {
            "input_tokens": 22 + 523,
            "output_tokens": 26825 + 14,
            "cache_creation_input_tokens": 50760 + 0,
            "cache_read_input_tokens": 514670 + 0,
        })
        self.assertEqual(metrics["per_model"], result.model_usage)

    def test_empty_model_usage_yields_zero_cost(self):
        result = make_result(model_usage={}, total_cost_usd=0.0)
        metrics = build_metrics("rfp-01-baseline", result)
        self.assertEqual(metrics["cost_usd"], 0)
        self.assertEqual(metrics["tokens"]["input_tokens"], 0)

    def test_none_model_usage_yields_zero_cost(self):
        result = make_result(model_usage=None)
        metrics = build_metrics("rfp-01-baseline", result)
        self.assertEqual(metrics["cost_usd"], 0)


class SaveMetricsTests(unittest.TestCase):
    def test_writes_both_json_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run-01-baseline"
            result = make_result()
            metrics = save_metrics(run_dir, "rfp-01-baseline", result)

            raw = json.loads((run_dir / "cost-eval.json").read_text())
            self.assertEqual(raw["session_id"], "sess-1")
            self.assertEqual(raw["num_turns"], 7)

            written_metrics = json.loads((run_dir / "cost-eval.metrics.json").read_text())
            self.assertEqual(written_metrics, metrics)
            self.assertEqual(written_metrics["command"], "rfp-01-baseline")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_metrics -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'sdk_eval.metrics'`

- [ ] **Step 3: Write the implementation**

Create `sdk_eval/metrics.py`:

```python
"""Build the same cost-eval.metrics.json shape cost-eval.sh's jq filter
produces, sourced from a claude_agent_sdk.ResultMessage instead of the
claude CLI's raw JSON output.
"""
import json
from dataclasses import asdict
from pathlib import Path

from claude_agent_sdk import ResultMessage

_TOKEN_FIELDS = {
    "input_tokens": "inputTokens",
    "output_tokens": "outputTokens",
    "cache_creation_input_tokens": "cacheCreationInputTokens",
    "cache_read_input_tokens": "cacheReadInputTokens",
}


def build_metrics(strategy_key: str, result: ResultMessage) -> dict:
    model_usage = result.model_usage or {}
    cost_usd = sum((m.get("costUSD") or 0) for m in model_usage.values())
    tokens = {
        out_key: sum((m.get(sdk_key) or 0) for m in model_usage.values())
        for out_key, sdk_key in _TOKEN_FIELDS.items()
    }
    return {
        "command": strategy_key,
        "cost_usd": cost_usd,
        "orchestrator_cost_usd": result.total_cost_usd,
        "num_turns": result.num_turns,
        "duration_ms": result.duration_ms,
        "tokens": tokens,
        "per_model": model_usage,
    }


def save_metrics(run_dir: Path, strategy_key: str, result: ResultMessage) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "cost-eval.json").write_text(
        json.dumps(asdict(result), indent=2, default=str)
    )
    metrics = build_metrics(strategy_key, result)
    (run_dir / "cost-eval.metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_metrics -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add sdk_eval/metrics.py tests/sdk_eval/test_metrics.py
git commit -m "Add sdk_eval cost/token metrics extraction"
```

---

### Task 3: `sdk_eval/artifacts.py` — post-run artifact presence check

**Files:**
- Create: `sdk_eval/artifacts.py`
- Test: `tests/sdk_eval/test_artifacts.py`

**Interfaces:**
- Produces: `check_expected_artifacts(run_dir: Path) -> list[str]` — returns one warning string per missing pattern among `proposal-*.md`, `proposal-*.docx`, `risk-assessment-*.html`; empty list if all present. Consumed by `sdk_eval/cli.py` (Task 7).

- [ ] **Step 1: Write the failing test**

Create `tests/sdk_eval/test_artifacts.py`:

```python
import tempfile
import unittest
from pathlib import Path

from sdk_eval.artifacts import check_expected_artifacts


class CheckExpectedArtifactsTests(unittest.TestCase):
    def test_empty_dir_reports_all_three_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            warnings = check_expected_artifacts(Path(tmp))
            self.assertEqual(len(warnings), 3)

    def test_all_present_reports_no_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "proposal-acme-corp-2026-07-06.md").write_text("x")
            (run_dir / "proposal-acme-corp-2026-07-06.docx").write_bytes(b"x")
            (run_dir / "risk-assessment-acme-corp-2026-07-06.html").write_text("x")
            self.assertEqual(check_expected_artifacts(run_dir), [])

    def test_partial_reports_only_missing_ones(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "proposal-acme-corp-2026-07-06.md").write_text("x")
            warnings = check_expected_artifacts(run_dir)
            self.assertEqual(len(warnings), 2)
            self.assertTrue(any("docx" in w for w in warnings))
            self.assertTrue(any("risk-assessment" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_artifacts -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'sdk_eval.artifacts'`

- [ ] **Step 3: Write the implementation**

Create `sdk_eval/artifacts.py`:

```python
"""Check that a strategy run produced the artifacts its prompt asked for."""
from pathlib import Path

EXPECTED_PATTERNS = ("proposal-*.md", "proposal-*.docx", "risk-assessment-*.html")


def check_expected_artifacts(run_dir: Path) -> list[str]:
    warnings = []
    for pattern in EXPECTED_PATTERNS:
        if not any(run_dir.glob(pattern)):
            warnings.append(f"missing expected artifact matching {pattern!r} in {run_dir}")
    return warnings
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_artifacts -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add sdk_eval/artifacts.py tests/sdk_eval/test_artifacts.py
git commit -m "Add sdk_eval post-run artifact presence check"
```

---

### Task 4: `sdk_eval/runner.py` — SDK query wrapper

**Files:**
- Create: `sdk_eval/runner.py`
- Test: `tests/sdk_eval/test_runner.py`

**Interfaces:**
- Consumes: `sdk_eval.strategies.Strategy` (Task 1), `claude_agent_sdk.{query, ClaudeAgentOptions, ResultMessage}`.
- Produces: `async def run_prompt(prompt: str, repo_root: Path, permission_mode: str) -> ResultMessage` (generic — runs any prompt through the SDK), `async def run_strategy(strategy: Strategy, repo_root: Path, permission_mode: str) -> ResultMessage` (thin wrapper over `run_prompt` using `strategy.prompt`). Both raise `RuntimeError` if the SDK stream ends without a `ResultMessage`, or if `ResultMessage.is_error` is true. Consumed by `sdk_eval/judge.py` (Task 5, via `run_prompt`) and `sdk_eval/cli.py` (Task 7, via `run_strategy`).

- [ ] **Step 1: Write the failing test**

Create `tests/sdk_eval/test_runner.py`:

```python
import unittest

from claude_agent_sdk import ResultMessage

from sdk_eval.runner import _collect_result


async def fake_stream(items):
    for item in items:
        yield item


def make_result(is_error=False, **overrides):
    defaults = dict(
        subtype="success",
        duration_ms=1000,
        duration_api_ms=900,
        is_error=is_error,
        num_turns=1,
        session_id="s1",
        result="done",
        errors=None,
    )
    defaults.update(overrides)
    return ResultMessage(**defaults)


class CollectResultTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_final_result_message(self):
        result = make_result()
        collected = await _collect_result(fake_stream(["not-a-result", result]))
        self.assertIs(collected, result)

    async def test_raises_when_no_result_message_seen(self):
        with self.assertRaisesRegex(RuntimeError, "ended without a ResultMessage"):
            await _collect_result(fake_stream(["not-a-result"]))

    async def test_raises_when_result_is_error(self):
        result = make_result(is_error=True, errors=["boom"], result="failed")
        with self.assertRaisesRegex(RuntimeError, "errored"):
            await _collect_result(fake_stream([result]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_runner -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'sdk_eval.runner'`

- [ ] **Step 3: Write the implementation**

Create `sdk_eval/runner.py`:

```python
"""Run a prompt through the Agent SDK and return the terminal ResultMessage.

This replaces cost-eval.sh's `claude -p "..." --output-format json` calls.
"""
from pathlib import Path
from typing import AsyncIterator

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from .strategies import Strategy


async def _collect_result(messages: AsyncIterator) -> ResultMessage:
    result = None
    async for message in messages:
        if isinstance(message, ResultMessage):
            result = message
    if result is None:
        raise RuntimeError("SDK message stream ended without a ResultMessage")
    if result.is_error:
        raise RuntimeError(
            f"strategy run errored (subtype={result.subtype!r}): "
            f"errors={result.errors!r} result={result.result!r}"
        )
    return result


async def run_prompt(prompt: str, repo_root: Path, permission_mode: str) -> ResultMessage:
    # setting_sources is left at its SDK default (None = load user + project +
    # local settings) to match the claude CLI's own default discovery of
    # .claude/agents/*.md and .claude/skills/* when run from repo_root.
    options = ClaudeAgentOptions(cwd=str(repo_root), permission_mode=permission_mode)
    return await _collect_result(query(prompt=prompt, options=options))


async def run_strategy(strategy: Strategy, repo_root: Path, permission_mode: str) -> ResultMessage:
    return await run_prompt(strategy.prompt, repo_root, permission_mode)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_runner -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add sdk_eval/runner.py tests/sdk_eval/test_runner.py
git commit -m "Add sdk_eval SDK query wrapper"
```

---

### Task 5: `sdk_eval/judge.py` — LLM-judge quality rubric

**Files:**
- Create: `sdk_eval/judge.py`
- Test: `tests/sdk_eval/test_judge.py`

**Interfaces:**
- Consumes: `sdk_eval.runner.run_prompt` (Task 4), `sdk_eval.strategies.Strategy` (Task 1).
- Produces: `RUBRIC_DIMS: list[str]` (`["completeness", "specificity", "actionability", "risk_depth", "correctness"]`), `read_artifacts(run_dir: Path, max_chars: int = 12000) -> str`, `build_judge_prompt(artifacts: dict[str, str]) -> str`, `parse_judge_output(text: str) -> list[dict]` (each dict: `{"strategy_key", "scores": {dim: int}, "total": int, "rationale": str}`), `async def judge_quality(runs_dir: Path, strategies: list[Strategy], repo_root: Path, permission_mode: str) -> list[dict]`, `load_quality_cache(path: Path) -> list[dict] | None`, `save_quality_cache(path: Path, scores: list[dict]) -> None`. Consumed by `sdk_eval/cli.py` (Task 7).

- [ ] **Step 1: Write the failing test**

Create `tests/sdk_eval/test_judge.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

from sdk_eval.judge import (
    RUBRIC_DIMS,
    build_judge_prompt,
    load_quality_cache,
    parse_judge_output,
    read_artifacts,
    save_quality_cache,
)


class ReadArtifactsTests(unittest.TestCase):
    def test_no_artifacts_returns_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(read_artifacts(Path(tmp)), "(no artifacts found)")

    def test_reads_proposal_and_risk_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "proposal-acme-corp-2026-07-06.md").write_text("PROPOSAL BODY")
            (run_dir / "risk-assessment-acme-corp-2026-07-06.html").write_text("<h1>Risk</h1>")
            text = read_artifacts(run_dir)
            self.assertIn("PROPOSAL BODY", text)
            self.assertIn("<h1>Risk</h1>", text)
            self.assertIn("proposal-acme-corp-2026-07-06.md", text)


class BuildJudgePromptTests(unittest.TestCase):
    def test_includes_all_rubric_dims_and_strategy_keys(self):
        prompt = build_judge_prompt({"rfp-01-baseline": "text A", "rfp-02-agent-teams": "text B"})
        for dim in RUBRIC_DIMS:
            self.assertIn(dim, prompt)
        self.assertIn("rfp-01-baseline", prompt)
        self.assertIn("text A", prompt)
        self.assertIn("rfp-02-agent-teams", prompt)


class ParseJudgeOutputTests(unittest.TestCase):
    def test_parses_plain_json_array(self):
        text = json.dumps([
            {"strategy": "rfp-01-baseline", "scores": {d: 3 for d in RUBRIC_DIMS}, "rationale": "ok"}
        ])
        results = parse_judge_output(text)
        self.assertEqual(results[0]["strategy_key"], "rfp-01-baseline")
        self.assertEqual(results[0]["total"], 15)

    def test_parses_json_wrapped_in_fence(self):
        payload = json.dumps([
            {"strategy": "rfp-02-agent-teams", "scores": {d: 4 for d in RUBRIC_DIMS}, "rationale": "good"}
        ])
        text = f"Here you go:\n```json\n{payload}\n```"
        results = parse_judge_output(text)
        self.assertEqual(results[0]["strategy_key"], "rfp-02-agent-teams")

    def test_raises_when_no_json_array_present(self):
        with self.assertRaises(ValueError):
            parse_judge_output("no json here")


class QualityCacheTests(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "quality.json"
            self.assertIsNone(load_quality_cache(path))
            scores = [{"strategy_key": "rfp-01-baseline", "scores": {}, "total": 0, "rationale": ""}]
            save_quality_cache(path, scores)
            self.assertEqual(load_quality_cache(path), scores)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_judge -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'sdk_eval.judge'`

- [ ] **Step 3: Write the implementation**

Create `sdk_eval/judge.py`:

```python
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
    result = await run_prompt(prompt, repo_root, permission_mode)
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_judge -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add sdk_eval/judge.py tests/sdk_eval/test_judge.py
git commit -m "Add sdk_eval LLM-judge quality rubric"
```

---

### Task 6: `sdk_eval/report.py` — comparison report builder

**Files:**
- Create: `sdk_eval/report.py`
- Test: `tests/sdk_eval/test_report.py`

**Interfaces:**
- Consumes: `sdk_eval.strategies.Strategy` (Task 1); reads `<runs_dir>/<strategy.dir_name>/cost-eval.metrics.json` and `<comparison_dir>/quality.json` from disk; reads `templates/report.html.tmpl` (existing repo file, untouched).
- Produces: `build_report_data(runs_dir: Path, comparison_dir: Path, strategies: list[Strategy]) -> dict` (raises `FileNotFoundError` if `quality.json` is missing), `render(report_data: dict, template_path: Path, output_path: Path) -> None` (writes `output_path` and a sibling `report-data.json`). Consumed by `sdk_eval/cli.py` (Task 7).

- [ ] **Step 1: Write the failing test**

Create `tests/sdk_eval/test_report.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

from sdk_eval.report import build_report_data, render
from sdk_eval.strategies import STRATEGIES


def write_metrics(run_dir: Path, cost: float, input_tok: int):
    run_dir.mkdir(parents=True)
    metrics = {
        "command": run_dir.name,
        "cost_usd": cost,
        "orchestrator_cost_usd": cost,
        "num_turns": 5,
        "duration_ms": 60000,
        "tokens": {
            "input_tokens": input_tok,
            "output_tokens": 100,
            "cache_creation_input_tokens": 10,
            "cache_read_input_tokens": 20,
        },
        "per_model": {},
    }
    (run_dir / "cost-eval.metrics.json").write_text(json.dumps(metrics))
    (run_dir / "risk-assessment-acme-corp-2026-07-06.html").write_text("<h1>ACME Corp RFP</h1>")


class BuildReportDataTests(unittest.TestCase):
    def test_picks_winners_and_computes_quality_per_dollar(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp) / "runs"
            comparison_dir = Path(tmp) / "comparison"
            write_metrics(runs_dir / "run-01-baseline", cost=1.0, input_tok=100)
            write_metrics(runs_dir / "run-02-agent-teams", cost=2.0, input_tok=200)
            write_metrics(runs_dir / "run-03-dynamic-workflow", cost=0.5, input_tok=50)
            comparison_dir.mkdir(parents=True)
            quality = [
                {"strategy_key": "rfp-01-baseline", "scores": {}, "total": 10, "rationale": "ok"},
                {"strategy_key": "rfp-02-agent-teams", "scores": {}, "total": 20, "rationale": "best"},
                {"strategy_key": "rfp-03-dynamic-workflow", "scores": {}, "total": 15, "rationale": "cheap"},
            ]
            (comparison_dir / "quality.json").write_text(json.dumps(quality))

            data = build_report_data(runs_dir, comparison_dir, STRATEGIES)

            self.assertEqual(data["rfp"], "ACME Corp RFP")
            self.assertEqual(data["winner_quality"], "rfp-02-agent-teams")
            self.assertEqual(data["winner_value"], "rfp-03-dynamic-workflow")
            by_key = {s["strategy_key"]: s for s in data["strategies"]}
            self.assertEqual(
                by_key["rfp-03-dynamic-workflow"]["quality_per_dollar"], round(15 / 0.5, 2)
            )

    def test_missing_quality_cache_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp) / "runs"
            comparison_dir = Path(tmp) / "comparison"
            write_metrics(runs_dir / "run-01-baseline", cost=1.0, input_tok=100)
            with self.assertRaises(FileNotFoundError):
                build_report_data(runs_dir, comparison_dir, STRATEGIES[:1])


class RenderTests(unittest.TestCase):
    def test_writes_html_and_report_data_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            template_path = Path(tmp) / "template.html.tmpl"
            template_path.write_text("<html>__REPORT_DATA__</html>")
            output_path = Path(tmp) / "out" / "report.html"
            data = {"rfp": "X", "strategies": []}

            render(data, template_path, output_path)

            html = output_path.read_text()
            self.assertIn(json.dumps(data, indent=2), html)
            report_data_json = json.loads((output_path.parent / "report-data.json").read_text())
            self.assertEqual(report_data_json, data)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_report -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'sdk_eval.report'`

- [ ] **Step 3: Write the implementation**

Create `sdk_eval/report.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_report -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add sdk_eval/report.py tests/sdk_eval/test_report.py
git commit -m "Add sdk_eval comparison report builder"
```

---

### Task 7: `sdk_eval/cli.py` + `scripts/cost-eval-sdk.py` — orchestration and entry point

**Files:**
- Create: `sdk_eval/cli.py`
- Create: `scripts/cost-eval-sdk.py`
- Test: `tests/sdk_eval/test_cli.py`

**Interfaces:**
- Consumes: `sdk_eval.strategies.{STRATEGIES, Strategy, get_strategy}` (Task 1), `sdk_eval.metrics.save_metrics` (Task 2), `sdk_eval.artifacts.check_expected_artifacts` (Task 3), `sdk_eval.runner.run_strategy` (Task 4), `sdk_eval.judge.{judge_quality, load_quality_cache, save_quality_cache}` (Task 5), `sdk_eval.report.{build_report_data, render}` (Task 6).
- Produces: `resolve_commands(command_keys: list[str]) -> list[Strategy]` (raises `ValueError` for an unknown key), `check_report_inputs_ready(runs_dir: Path, strategies: list[Strategy]) -> list[str]`, `format_summary_table(rows: list[dict]) -> str`, `parse_args(argv: list[str]) -> argparse.Namespace`, `main(argv: list[str] | None = None) -> int`. `scripts/cost-eval-sdk.py` calls `sdk_eval.cli.main()` and exits with its return code.

- [ ] **Step 1: Write the failing test**

Create `tests/sdk_eval/test_cli.py`:

```python
import tempfile
import unittest
from pathlib import Path

from sdk_eval.cli import (
    check_report_inputs_ready,
    format_summary_table,
    parse_args,
    resolve_commands,
)
from sdk_eval.strategies import STRATEGIES


class ResolveCommandsTests(unittest.TestCase):
    def test_no_args_returns_all_three_in_order(self):
        strategies = resolve_commands([])
        self.assertEqual([s.key for s in strategies], [s.key for s in STRATEGIES])

    def test_specific_key_returns_just_that_strategy(self):
        strategies = resolve_commands(["rfp-02-agent-teams"])
        self.assertEqual([s.key for s in strategies], ["rfp-02-agent-teams"])

    def test_unknown_key_raises(self):
        with self.assertRaises(ValueError):
            resolve_commands(["not-a-real-strategy"])


class CheckReportInputsReadyTests(unittest.TestCase):
    def test_reports_missing_metrics_and_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp)
            missing = check_report_inputs_ready(runs_dir, STRATEGIES)
            self.assertEqual(len(missing), len(STRATEGIES) * 2)

    def test_no_missing_when_all_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp)
            for s in STRATEGIES:
                run_dir = runs_dir / s.dir_name
                run_dir.mkdir(parents=True)
                (run_dir / "cost-eval.metrics.json").write_text("{}")
                (run_dir / "risk-assessment-acme-corp-2026-07-06.html").write_text("<h1>x</h1>")
            self.assertEqual(check_report_inputs_ready(runs_dir, STRATEGIES), [])


class FormatSummaryTableTests(unittest.TestCase):
    def test_includes_header_and_one_row_per_strategy(self):
        rows = [{
            "command": "rfp-01-baseline",
            "cost_usd": 0.861402,
            "tokens": {
                "input_tokens": 22,
                "output_tokens": 26825,
                "cache_creation_input_tokens": 50760,
                "cache_read_input_tokens": 514670,
            },
        }]
        table = format_summary_table(rows)
        lines = table.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("command", lines[0])
        self.assertIn("rfp-01-baseline", lines[1])


class ParseArgsTests(unittest.TestCase):
    def test_defaults(self):
        args = parse_args([])
        self.assertEqual(args.commands, [])
        self.assertFalse(args.report_only)

    def test_report_only_flag(self):
        args = parse_args(["--report-only"])
        self.assertTrue(args.report_only)

    def test_positional_commands(self):
        args = parse_args(["rfp-01-baseline", "rfp-02-agent-teams"])
        self.assertEqual(args.commands, ["rfp-01-baseline", "rfp-02-agent-teams"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_cli -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'sdk_eval.cli'`

- [ ] **Step 3: Write the implementation**

Create `sdk_eval/cli.py`:

```python
"""Orchestration + argument parsing — the Python equivalent of
scripts/cost-eval.sh, driving sdk_eval's strategy/metrics/judge/report
modules instead of shelling out to the claude CLI.
"""
import argparse
import asyncio
import os
import sys
from pathlib import Path

from . import artifacts as artifacts_mod
from . import judge as judge_mod
from . import metrics as metrics_mod
from . import report as report_mod
from .runner import run_strategy
from .strategies import STRATEGIES, Strategy, get_strategy

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "outputs" / "runs-sdk"
COMPARISON_DIR = RUNS_DIR / "comparison-cost-eval"
TEMPLATE_PATH = REPO_ROOT / "templates" / "report.html.tmpl"
DEFAULT_PERMISSION_MODE = "bypassPermissions"


def resolve_commands(command_keys: list[str]) -> list[Strategy]:
    if not command_keys:
        return list(STRATEGIES)
    return [get_strategy(key) for key in command_keys]


def check_report_inputs_ready(runs_dir: Path, strategies: list[Strategy]) -> list[str]:
    missing = []
    for s in strategies:
        run_dir = runs_dir / s.dir_name
        if not (run_dir / "cost-eval.metrics.json").exists():
            missing.append(f"missing: {run_dir / 'cost-eval.metrics.json'}")
        if not any(run_dir.glob("risk-assessment-*.html")):
            missing.append(f"missing: {run_dir}/risk-assessment-*.html")
    return missing


def format_summary_table(rows: list[dict]) -> str:
    header = (
        f"{'command':<24}{'cost_usd':>12}{'input_tok':>12}"
        f"{'output_tok':>12}{'cache_creat':>14}{'cache_read':>14}"
    )
    lines = [header]
    for m in rows:
        t = m["tokens"]
        lines.append(
            f"{m['command']:<24}{m['cost_usd']:>12.6f}{t['input_tokens']:>12}"
            f"{t['output_tokens']:>12}{t['cache_creation_input_tokens']:>14}"
            f"{t['cache_read_input_tokens']:>14}"
        )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run RFP strategies via the Agent SDK and build a cost/quality comparison report."
    )
    parser.add_argument("commands", nargs="*", help="strategy keys to run (default: all 3)")
    parser.add_argument(
        "--report-only", action="store_true",
        help="skip running strategies; just (re)build the comparison report",
    )
    return parser.parse_args(argv)


async def build_report(force_judge: bool, permission_mode: str) -> None:
    quality_path = COMPARISON_DIR / "quality.json"
    if force_judge or judge_mod.load_quality_cache(quality_path) is None:
        scores = await judge_mod.judge_quality(RUNS_DIR, STRATEGIES, REPO_ROOT, permission_mode)
        judge_mod.save_quality_cache(quality_path, scores)
        print(f"wrote {quality_path}")
    else:
        print(f"quality cache already exists at {quality_path}")
    report_data = report_mod.build_report_data(RUNS_DIR, COMPARISON_DIR, STRATEGIES)
    output_path = COMPARISON_DIR / "report.html"
    report_mod.render(report_data, TEMPLATE_PATH, output_path)
    print(f"wrote {output_path}")
    print(f"wrote {output_path.parent / 'report-data.json'}")


async def run_pipeline(command_keys: list[str], permission_mode: str, report_only: bool) -> int:
    if report_only:
        missing = check_report_inputs_ready(RUNS_DIR, STRATEGIES)
        if missing:
            for m in missing:
                print(m, file=sys.stderr)
            print(
                "error: --report-only requires cost-eval + risk-assessment "
                "outputs for all 3 runs", file=sys.stderr,
            )
            return 1
        await build_report(force_judge=False, permission_mode=permission_mode)
        return 0

    try:
        strategies = resolve_commands(command_keys)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Permission mode: {permission_mode} (override with PERMISSION_MODE env var)\n")

    rows = []
    for strategy in strategies:
        run_dir = RUNS_DIR / strategy.dir_name
        print(f"=== Running {strategy.key} ===")
        result = await run_strategy(strategy, REPO_ROOT, permission_mode)
        metrics = metrics_mod.save_metrics(run_dir, strategy.key, result)
        for warning in artifacts_mod.check_expected_artifacts(run_dir):
            print(f"  warning: {warning}", file=sys.stderr)
        print(
            f"  cost_usd (all agents): ${metrics['cost_usd']}  "
            f"(orchestrator-only: ${metrics['orchestrator_cost_usd']})  "
            f"-> {run_dir / 'cost-eval.metrics.json'}\n"
        )
        rows.append(metrics)

    print("=== Summary ===")
    print(format_summary_table(rows))
    print()

    missing = check_report_inputs_ready(RUNS_DIR, STRATEGIES)
    if not missing:
        print("=== Comparison report ===")
        await build_report(force_judge=True, permission_mode=permission_mode)
    else:
        print(
            "note: skipping comparison report — not all 3 strategy runs "
            "have outputs yet", file=sys.stderr,
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.report_only and args.commands:
        print("error: --report-only does not take additional arguments", file=sys.stderr)
        return 1
    permission_mode = os.environ.get("PERMISSION_MODE", DEFAULT_PERMISSION_MODE)
    return asyncio.run(run_pipeline(args.commands, permission_mode, args.report_only))


if __name__ == "__main__":
    sys.exit(main())
```

Create `scripts/cost-eval-sdk.py`:

```python
#!/usr/bin/env python3
"""Run RFP strategies via the Agent SDK and build a cost/quality comparison
report — equivalent pipeline to scripts/cost-eval.sh, but every invocation
of Claude goes through claude_agent_sdk instead of shelling out to the
claude CLI directly.

Usage:
  python3 scripts/cost-eval-sdk.py                     # run all 3 strategies, then build report
  python3 scripts/cost-eval-sdk.py rfp-02-agent-teams   # run just one
  python3 scripts/cost-eval-sdk.py --report-only        # rebuild report from existing outputs

Requires: claude CLI on PATH (claude_agent_sdk spawns it under the hood),
the claude_agent_sdk pip package (already in .venv), python3.
Must be run with the .venv's python3 (or any interpreter with
claude_agent_sdk installed) — it locates the repo root relative to this
file, so it does not need to be run from any particular cwd.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sdk_eval.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
```

```bash
chmod +x scripts/cost-eval-sdk.py
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest tests.sdk_eval.test_cli -v`
Expected: PASS (9 tests)

- [ ] **Step 5: Run the full test suite**

Run: `cd task07-claude-code-rfp-agent && python3 -m unittest discover -s tests -t . -v`
Expected: PASS (all tests across all 7 test modules, 34 tests total — verified by running this exact plan's code during plan authoring)

- [ ] **Step 6: Commit**

```bash
git add sdk_eval/cli.py scripts/cost-eval-sdk.py tests/sdk_eval/test_cli.py
git commit -m "Add sdk_eval CLI orchestration and scripts/cost-eval-sdk.py entry point"
```

---

### Task 8: Live smoke test — one strategy end-to-end

**Files:**
- None created; this task exercises Tasks 1–7 against the real `claude` CLI/API.

**Interfaces:**
- Consumes: `scripts/cost-eval-sdk.py` (Task 7), a real `claude` CLI on `PATH`, real API credentials/spend.
- Produces: `outputs/runs-sdk/run-01-baseline/{cost-eval.json,cost-eval.metrics.json,proposal-*.md,proposal-*.docx,risk-assessment-*.html}` on disk.

- [ ] **Step 1: Confirm the `claude` CLI is on PATH**

Run: `which claude`
Expected: a path is printed (not "not found"). If missing, stop and tell the user — nothing further in this task can run.

- [ ] **Step 2: Run the baseline strategy through the new SDK pipeline**

Run: `cd task07-claude-code-rfp-agent && python3 scripts/cost-eval-sdk.py rfp-01-baseline`
Expected: prints `Permission mode: bypassPermissions ...`, then `=== Running rfp-01-baseline ===`, then a cost line, then `=== Summary ===` with one row, then a note that the comparison report is skipped (only 1 of 3 runs present). Exit code 0.

- [ ] **Step 3: Verify the artifacts landed in the right place**

Run: `ls -la outputs/runs-sdk/run-01-baseline/`
Expected: exactly `cost-eval.json`, `cost-eval.metrics.json`, `proposal-<customer>-<date>.md`, `proposal-<customer>-<date>.docx`, `risk-assessment-<customer>-<date>.html`, all non-empty. Confirm `outputs/runs/run-01-baseline/` (the CLI reference run) is byte-for-byte unchanged: `git status outputs/runs/` should show no modifications.

- [ ] **Step 4: Sanity-check the metrics values**

Run: `cat outputs/runs-sdk/run-01-baseline/cost-eval.metrics.json`
Expected: valid JSON; `cost_usd` and `orchestrator_cost_usd` are positive floats; `tokens.input_tokens` / `tokens.output_tokens` are positive integers; `command` equals `"rfp-01-baseline"`.

- [ ] **Step 5: Commit the smoke-test outputs**

```bash
git add outputs/runs-sdk/run-01-baseline/
git commit -m "Add SDK-run smoke-test outputs for rfp-01-baseline"
```

- [ ] **Step 6: Report back to the user before running the other two strategies**

Running `rfp-02-agent-teams` and `rfp-03-dynamic-workflow` (and then the LLM-judge step) triggers several more real, paid Claude invocations (the agent-teams strategy alone spawns 5 specialist subagents). Do not run them automatically — report the Task 8 results (cost_usd observed, artifact paths) back to the user and let them decide whether/when to run:

```bash
python3 scripts/cost-eval-sdk.py
```

to execute all 3 strategies and build the full `outputs/runs-sdk/comparison-cost-eval/report.html`.

---

## Self-Review

**Spec coverage:**
- Architecture (package + entry script) → Tasks 1–7 file structure. ✓
- `strategies.py` ported prompts with path substitution → Task 1 (with a dedicated regression test). ✓
- `runner.py` SDK query wrapper, default `setting_sources` → Task 4. ✓
- `metrics.py` shape parity with `cost-eval.sh`'s `jq` filter → Task 2 (test fixture uses the exact real field values captured from `outputs/runs/run-01-baseline/cost-eval.json`). ✓
- `judge.py` same rubric, SDK-based invocation, caching → Task 5. ✓
- `report.py` reusing `templates/report.html.tmpl` → Task 6. ✓
- `cli.py` argparse surface (`--report-only`, positional commands, `PERMISSION_MODE` env var), sequential execution, summary table → Task 7. ✓
- Output location `outputs/runs-sdk/` → baked into `sdk_eval/cli.py`'s `RUNS_DIR` constant and into every ported prompt (Task 1) and verified in the Task 8 smoke test. ✓
- Error handling (`is_error`, missing `ResultMessage`, missing artifacts as warnings, `--report-only` gate) → Tasks 4, 3, 7. ✓
- Testing section (unit tests for pure logic + one live smoke run) → Tasks 1–7 unit tests + Task 8. ✓
- Non-goals (don't touch `cost-eval.sh` / `judge_quality.py` / `generate_comparison_report.py` / `outputs/runs/`) → no task modifies any of those; Task 8 Step 3 explicitly verifies `outputs/runs/` is untouched. ✓

**Placeholder scan:** No TBD/TODO markers; every step has complete, runnable code or an exact command with expected output.

**Type consistency:** `Strategy(key, label, dir_name, prompt)` fields used identically across Tasks 1, 2, 4, 5, 6, 7. `build_metrics`/`save_metrics` signatures in Task 2 match their usage in Task 7's `run_pipeline`. `run_prompt`/`run_strategy` in Task 4 match their usage in Tasks 5 and 7. `judge_quality`/`load_quality_cache`/`save_quality_cache` in Task 5 match Task 7's `build_report`. `build_report_data`/`render` in Task 6 match Task 7's `build_report`.

---

## Execution Options

**Plan complete and saved to `docs/superpowers/plans/2026-07-07-cost-eval-agent-sdk.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
