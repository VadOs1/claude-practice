# Agent Teams Strategy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fourth `rfp_eval` strategy, "Agent Teams" (Task A's second option from `task07-claude-code-rfp-agent/index.md`), alongside the existing `single`, `swarm`, and `dynamic` strategies, so it runs through the same harness and its cost/tokens/quality automatically appear in `outputs/runs/agent_teams/` and in `outputs/eval/{metrics.json,quality.json,index.html}`.

**Architecture:** `rfp_eval` is already fully data-driven off `strategies.STRATEGY_KEYS` — `orchestrator.py` iterates it to launch runs concurrently, and `report.py` iterates it to build the dashboard. `single` and `dynamic` are implemented as pure prompt variants sharing one `ClaudeAgentOptions` shape (see `strategies.py:51-77`); `agent_teams` will be the same pattern — one more entry in `STRATEGY_KEYS`/`LABELS`/`_PREAMBLES`, with a preamble that asks Claude Code to spin up an agent team using the project's `.claude/agents/*.md` specialists (`deal-desk-orchestrator` + the five specialist agents), which are already loadable via the `setting_sources=["project"]` + `cwd=task_dir` options every strategy already sets, combined with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` already set in `.claude/settings.json`. **No changes to `orchestrator.py`, `report.py`, `metrics.py`, `sdk_runner.py`, or `judge.py` are required** — adding the strategy key is the entire production change; the rest of the plan is tests that lock in the data-driven behavior plus doc updates.

**Tech Stack:** Python 3.14, `uv`, `claude-agent-sdk`, `pytest` (no `pytest-asyncio` — async tests drive `asyncio.run(...)` directly with fake `query_fn` generators).

## Global Constraints

- Strategies differ by **prompt + options only**, never by a new CLI flag — all differentiation lives in `rfp_eval/strategies.py` (per `task07-claude-code-rfp-agent/CLAUDE.md`'s "Key design decisions"). Do not add an `agent_teams`-specific branch to `orchestrator.py` or `report.py`.
- Every test must inject a fake `query_fn` (async generator yielding `SimpleNamespace` messages) — no real SDK/CLI calls in the test suite, no tokens spent.
- Run tests with `uv run pytest -q` from the repo root (`/Users/vadim_dissa/dev/black-belt/codespaces/claude-practice`) — `pytest` config (`pythonpath`/`testpaths`) lives in the repo-root `pyproject.toml`.
- Preserve exact existing SDK/report field names: `ResultMessage.total_cost_usd`, `.usage`, `.model_usage`, `.num_turns`, `.duration_ms`, `.is_error`, `.result`; `RunMetrics` field names; `strategy_key` as the dict key everywhere (never `strategy` or `name`).
- New strategy key: `agent_teams` (snake_case, matches the style of `risk_depth` etc. elsewhere in the codebase; the other three keys — `single`, `swarm`, `dynamic` — are single words so this is the first multi-word key).

---

### Task 1: Add the `agent_teams` strategy definition

**Files:**
- Modify: `task07-claude-code-rfp-agent/rfp_eval/strategies.py:7-43`
- Test: `task07-claude-code-rfp-agent/tests/test_strategies.py`

**Interfaces:**
- Consumes: nothing new — reuses the existing `render_prompt(preamble, rfp_path, out_dir)` and the generic branch of `build_call` (`strategies.py:66-77`), which already handles any key present in `_PREAMBLES` by building `ClaudeAgentOptions(cwd=task_dir, setting_sources=["project"], permission_mode="bypassPermissions", model=model)`.
- Produces: `STRATEGY_KEYS == ["single", "swarm", "dynamic", "agent_teams"]`, `LABELS["agent_teams"] == "Agent Teams"`. Everything downstream (`orchestrator.py`, `report.py`) consumes `STRATEGY_KEYS`/`LABELS` by name, so this is the only interface that matters for the rest of the plan.

- [ ] **Step 1: Write the failing tests**

Edit `task07-claude-code-rfp-agent/tests/test_strategies.py`:

```python
from rfp_eval import strategies as s


def test_strategy_keys_and_labels():
    assert s.STRATEGY_KEYS == ["single", "swarm", "dynamic", "agent_teams"]
    assert s.LABELS["swarm"] == "Agent Swarm"
    assert s.LABELS["agent_teams"] == "Agent Teams"
    assert set(s.LABELS) == set(s.STRATEGY_KEYS)


def test_render_prompt_embeds_paths():
    prompt = s.render_prompt("PREAMBLE-X", "synthetic-data/rfp-acme-corp.md", "outputs/runs/single")
    assert "PREAMBLE-X" in prompt
    assert "synthetic-data/rfp-acme-corp.md" in prompt
    assert "outputs/runs/single" in prompt
    assert "proposal.docx" in prompt
    assert "risk-assessment.html" in prompt


def test_build_call_single_no_delegation():
    prompt, options = s.build_call(
        "single", task_dir="/task", rfp_path="rfp.md", out_dir="/task/outputs/runs/single"
    )
    assert "single agent" in prompt.lower()
    assert "do not" in prompt.lower()  # forbids delegation
    assert str(options.cwd) == "/task"
    assert options.setting_sources == ["project"]
    assert options.permission_mode == "bypassPermissions"


def test_build_call_dynamic_prompt():
    prompt, _ = s.build_call("dynamic", task_dir="/task", rfp_path="rfp.md", out_dir="/o")
    assert "dynamic workflow" in prompt.lower()


def test_build_call_agent_teams_prompt():
    prompt, options = s.build_call(
        "agent_teams", task_dir="/task", rfp_path="rfp.md", out_dir="/task/outputs/runs/agent_teams"
    )
    assert "agent team" in prompt.lower()
    assert "coordinator" in prompt.lower()
    # names the project's specialist roster, per index.md: "be quite
    # specific which agents to include in the team"
    assert "deal-desk-orchestrator" in prompt
    assert "pricing" in prompt.lower()
    assert "risk-assessment" in prompt.lower()
    # same options shape as single/dynamic — no swarm-style `agents=` param
    assert str(options.cwd) == "/task"
    assert options.setting_sources == ["project"]
    assert options.permission_mode == "bypassPermissions"
    assert options.agents is None


def test_build_call_swarm_delegates_to_swarm_module():
    prompt, options = s.build_call(
        "swarm", task_dir="/task", rfp_path="rfp.md", out_dir="/task/outputs/runs/swarm"
    )
    assert "coordinator" in prompt.lower() or "swarm" in prompt.lower()
    assert options.agents is not None
    assert "pricing" in options.agents
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/vadim_dissa/dev/black-belt/codespaces/claude-practice
uv run pytest -q task07-claude-code-rfp-agent/tests/test_strategies.py
```

Expected: FAIL — `test_strategy_keys_and_labels` (list mismatch, missing `"agent_teams"` in `LABELS`) and `test_build_call_agent_teams_prompt` (`ValueError: unknown strategy key 'agent_teams'`).

- [ ] **Step 3: Implement the strategy**

Edit `task07-claude-code-rfp-agent/rfp_eval/strategies.py`:

```python
STRATEGY_KEYS: list[str] = ["single", "swarm", "dynamic", "agent_teams"]

LABELS: dict[str, str] = {
    "single": "Single Agent",
    "swarm": "Agent Swarm",
    "dynamic": "Dynamic Workflow",
    "agent_teams": "Agent Teams",
}
```

```python
_PREAMBLES = {
    "single": (
        "Handle this RFP entirely yourself as a single agent. Do NOT spawn "
        "sub-agents, agent teams, or workflows — rely only on skills and your "
        "own reasoning."
    ),
    "dynamic": (
        "Use a DYNAMIC WORKFLOW: first draft an explicit multi-step plan for "
        "handling this RFP end to end, then execute that workflow step by step, "
        "adapting the plan as results come in."
    ),
    "agent_teams": (
        "Use AGENT TEAMS for this RFP: spin up a team of agents where a "
        "coordinator distributes tasks to specialized sub-agents, and those "
        "agents pick up their work and proceed in parallel, communicating "
        "with each other as needed. Build the team from the project's "
        "specialist agents: deal-desk-orchestrator as the coordinator, plus "
        "pricing, legal, technical-fit, competitive, and risk-assessment as "
        "team members."
    ),
}
```

No other change to `strategies.py` is needed — `build_call`'s generic branch (`strategies.py:66-77`) already handles any key present in `_PREAMBLES` identically to `dynamic`.

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest -q task07-claude-code-rfp-agent/tests/test_strategies.py
```

Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add task07-claude-code-rfp-agent/rfp_eval/strategies.py task07-claude-code-rfp-agent/tests/test_strategies.py
git commit -m "feat(rfp-eval): add agent_teams strategy"
```

---

### Task 2: Update orchestrator tests for the four-strategy flow

**Files:**
- Modify: `task07-claude-code-rfp-agent/tests/test_orchestrator.py`

**Interfaces:**
- Consumes: `orchestrator.run_evaluation(..., query_fn=query_factory, judge_query_fn=judge_query) -> Path` (unchanged signature). `orchestrator.py` needs **no production code change** — it already derives its run list from `strategies.STRATEGY_KEYS` (`orchestrator.py:53,63`), which Task 1 grew to 4 entries. This task only updates test fixtures/assertions to match.
- Produces: confirms `outputs/runs/agent_teams/run.json` gets written and `outputs/eval/{metrics,quality}.json` contain 4 entries, locking in the "runs + eval folder" part of the requirement.

- [ ] **Step 1: Write the updated (currently-failing) tests**

Replace `task07-claude-code-rfp-agent/tests/test_orchestrator.py` in full:

```python
import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

from rfp_eval import orchestrator

JUDGE_TEXT = """```json
[
 {"strategy":"single","scores":{"completeness":3,"specificity":3,"actionability":4,"risk_depth":2,"correctness":4},"rationale":"ok"},
 {"strategy":"swarm","scores":{"completeness":5,"specificity":4,"actionability":4,"risk_depth":5,"correctness":4},"rationale":"best"},
 {"strategy":"dynamic","scores":{"completeness":4,"specificity":4,"actionability":5,"risk_depth":3,"correctness":4},"rationale":"good"},
 {"strategy":"agent_teams","scores":{"completeness":4,"specificity":3,"actionability":4,"risk_depth":3,"correctness":4},"rationale":"solid team output"}
]
```"""


def _run_result(out_dir):
    # simulate a strategy writing an artifact + returning a ResultMessage
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    (Path(out_dir) / "risk-assessment.html").write_text("<html>risk</html>")
    return SimpleNamespace(
        total_cost_usd=0.5, usage={"input_tokens": 100, "output_tokens": 200,
        "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        num_turns=4, duration_ms=1000, is_error=False, result="wrote files",
    )


def test_run_evaluation_end_to_end(tmp_path):
    def make_strategy_query(out_dir):
        async def fake_query(prompt, options=None):
            yield _run_result(out_dir)
        return fake_query

    # query_fn is chosen per-run using the run's out_dir (see orchestrator contract)
    def query_factory(out_dir):
        return make_strategy_query(out_dir)

    async def judge_query(prompt, options=None):
        yield SimpleNamespace(
            total_cost_usd=0.05, usage={}, num_turns=1, duration_ms=1,
            is_error=False, result=JUDGE_TEXT,
        )

    index = asyncio.run(
        orchestrator.run_evaluation(
            task_dir=tmp_path,
            rfp_path="rfp.md",
            out_root=tmp_path / "outputs",
            query_fn=query_factory,
            judge_query_fn=judge_query,
        )
    )
    assert index.exists() and index.name == "index.html"
    html = index.read_text()
    assert "Agent Swarm" in html
    assert "Agent Teams" in html
    metrics = json.loads((tmp_path / "outputs" / "eval" / "metrics.json").read_text())
    quality = json.loads((tmp_path / "outputs" / "eval" / "quality.json").read_text())
    assert len(metrics) == 4 and len(quality) == 4
    assert (tmp_path / "outputs" / "runs" / "swarm" / "run.json").exists()
    assert (tmp_path / "outputs" / "runs" / "agent_teams" / "run.json").exists()


def test_run_evaluation_survives_one_strategy_crashing(tmp_path):
    def make_strategy_query(out_dir):
        async def fake_query(prompt, options=None):
            yield _run_result(out_dir)
        return fake_query

    def crashing_query(out_dir):
        async def fake_query(prompt, options=None):
            raise RuntimeError("transport crashed")
            yield  # pragma: no cover - makes this an async generator
        return fake_query

    def query_factory(out_dir):
        if Path(out_dir).name == "dynamic":
            return crashing_query(out_dir)
        return make_strategy_query(out_dir)

    async def judge_query(prompt, options=None):
        yield SimpleNamespace(
            total_cost_usd=0.05, usage={}, num_turns=1, duration_ms=1,
            is_error=False, result=JUDGE_TEXT,
        )

    index = asyncio.run(
        orchestrator.run_evaluation(
            task_dir=tmp_path,
            rfp_path="rfp.md",
            out_root=tmp_path / "outputs",
            query_fn=query_factory,
            judge_query_fn=judge_query,
        )
    )
    assert index.exists() and index.name == "index.html"

    metrics = json.loads((tmp_path / "outputs" / "eval" / "metrics.json").read_text())
    quality = json.loads((tmp_path / "outputs" / "eval" / "quality.json").read_text())
    assert len(metrics) == 4 and len(quality) == 4

    by_key = {m["strategy_key"]: m for m in metrics}
    assert set(by_key) == {"single", "swarm", "dynamic", "agent_teams"}
    assert by_key["dynamic"]["is_error"] is True
    assert by_key["single"]["is_error"] is False
    assert by_key["swarm"]["is_error"] is False
    assert by_key["agent_teams"]["is_error"] is False

    assert (tmp_path / "outputs" / "runs" / "dynamic" / "run.json").exists()
    assert (tmp_path / "outputs" / "runs" / "single" / "run.json").exists()
    assert (tmp_path / "outputs" / "runs" / "swarm" / "run.json").exists()
    assert (tmp_path / "outputs" / "runs" / "agent_teams" / "run.json").exists()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/vadim_dissa/dev/black-belt/codespaces/claude-practice
uv run pytest -q task07-claude-code-rfp-agent/tests/test_orchestrator.py
```

Expected: FAIL on the old (pre-edit) file's `len(metrics) == 3` assertions once Task 1's `STRATEGY_KEYS` change is in place — confirming the test previously locked in the wrong (3-strategy) count. After pasting the Step 1 replacement above, re-run and confirm it fails for the *opposite* reason if you paste it before Task 1 lands (i.e. do Task 1 first); with Task 1 already committed, this step should already show PASS since `orchestrator.py` is fully data-driven — if so, skip straight to Step 4 and note in the commit message that no production fix was needed.

- [ ] **Step 3: No production code change**

`orchestrator.py` requires no edits — it already iterates `STRATEGY_KEYS` (`orchestrator.py:53,63,75`), so once `strategies.py` (Task 1) lists `agent_teams`, `run_evaluation` runs it, writes `outputs/runs/agent_teams/run.json`, includes it in `metrics.json`/`quality.json`, and `report.build_report_data` (unchanged) folds it into `index.html`.

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest -q task07-claude-code-rfp-agent/tests/test_orchestrator.py
```

Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add task07-claude-code-rfp-agent/tests/test_orchestrator.py
git commit -m "test(rfp-eval): cover agent_teams in orchestrator end-to-end flow"
```

---

### Task 3: Lock in `agent_teams` at the report layer

**Files:**
- Modify: `task07-claude-code-rfp-agent/tests/test_report.py`

**Interfaces:**
- Consumes: `report.build_report_data(metrics: list[RunMetrics], scores: list[QualityScore], *, rfp="", generated_at=None) -> dict` (unchanged). `report.py` needs **no production code change** — `build_report_data` already loops `for key in STRATEGY_KEYS` (`report.py:36`), so a 4th `RunMetrics`/`QualityScore` pair with `strategy_key="agent_teams"` flows through automatically, including into `winner_quality`/`winner_value` and `quality_per_dollar`.
- Produces: explicit confirmation that the dashboard's `index.html` (rendered from this same `build_report_data` output — see Task 2's `"Agent Teams" in html` check) will show all 4 strategies, plus verifies `PALETTE` in `templates/report.html.tmpl:49` (already sized to 4 colors: `['#3987e5', '#199e70', '#c98500', '#a371f7']`) needs no change.

- [ ] **Step 1: Write the failing test**

Append to `task07-claude-code-rfp-agent/tests/test_report.py`:

```python
def test_build_report_data_includes_agent_teams():
    metrics = _metrics() + [
        RunMetrics("agent_teams", 0.90, 1800, 9500, 220000, 35000, 266300, 10, 55000, False),
    ]
    scores = _scores() + [
        QualityScore(
            "agent_teams",
            {"completeness": 4, "specificity": 3, "actionability": 4, "risk_depth": 3, "correctness": 4},
            18,
            "solid team output",
        ),
    ]
    data = report.build_report_data(metrics, scores, rfp="rfp-acme-corp.md")
    assert [s["strategy_key"] for s in data["strategies"]] == ["single", "swarm", "dynamic", "agent_teams"]
    agent_teams = next(s for s in data["strategies"] if s["strategy_key"] == "agent_teams")
    assert agent_teams["label"] == "Agent Teams"
    assert agent_teams["quality"]["total"] == 18
    assert round(agent_teams["quality_per_dollar"], 2) == round(18 / 0.90, 2)


def test_render_report_embeds_all_four_strategy_labels():
    metrics = _metrics() + [
        RunMetrics("agent_teams", 0.90, 1800, 9500, 220000, 35000, 266300, 10, 55000, False),
    ]
    scores = _scores() + [
        QualityScore(
            "agent_teams",
            {"completeness": 4, "specificity": 3, "actionability": 4, "risk_depth": 3, "correctness": 4},
            18,
            "solid team output",
        ),
    ]
    data = report.build_report_data(metrics, scores, rfp="rfp.md")
    html = report.render_report(data)
    for label in ("Single Agent", "Agent Swarm", "Dynamic Workflow", "Agent Teams"):
        assert label in html
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/vadim_dissa/dev/black-belt/codespaces/claude-practice
uv run pytest -q task07-claude-code-rfp-agent/tests/test_report.py
```

Expected: with Task 1 already committed, this should already PASS (no production gap — `report.py` is data-driven off `STRATEGY_KEYS`/`LABELS`). If it fails, the failure will point at a real gap in `report.py`'s iteration logic; investigate `build_report_data`'s loop (`report.py:36-60`) before changing anything else in this plan.

- [ ] **Step 3: No production code change expected**

If Step 2 passed already, skip to Step 4. `report.py` should not need edits for this task.

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest -q task07-claude-code-rfp-agent/tests/test_report.py
```

Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add task07-claude-code-rfp-agent/tests/test_report.py
git commit -m "test(rfp-eval): cover agent_teams in report data + rendering"
```

---

### Task 4: Update user-facing docs and CLI text

**Files:**
- Modify: `task07-claude-code-rfp-agent/CLAUDE.md`
- Modify: `task07-claude-code-rfp-agent/.claude/commands/rfp-eval.md`
- Modify: `task07-claude-code-rfp-agent/rfp_eval/__main__.py:16`

**Interfaces:** none — doc/string-only changes, no behavior.

- [ ] **Step 1: Update `CLAUDE.md`**

Edit the "What it does" paragraph (currently `CLAUDE.md:39-44`):

```markdown
The harness runs the Acme RFP through four Claude Code strategies —
**single agent**, an Agent-SDK coordinator→specialists **swarm**, an
**agent teams** run (project specialist sub-agents coordinated via Claude
Code's experimental Agent Teams mode), and a **dynamic workflow** —
concurrently on the `claude-agent-sdk`. Each run's terminal `ResultMessage`
reports *real* cost and token usage, so the comparison uses measured numbers,
not estimates. An LLM judge scores each strategy's output artifacts against a
fixed rubric, and the results are rendered into a self-contained Chart.js
dashboard at `outputs/eval/index.html`.
```

Edit the intro bullet (currently `CLAUDE.md:9-10`):

```markdown
2. **`rfp_eval/`** — a Claude Agent SDK harness that runs the RFP through four
   strategies, measures real cost + quality, and renders a comparison report.
```

Edit the "How a run works" step 2 (currently `CLAUDE.md:99`):

```markdown
2. `run_evaluation` launches all four strategies **concurrently** with
   `asyncio.gather(..., return_exceptions=True)`. Each is one `_run_one(key)`.
```

- [ ] **Step 2: Update `.claude/commands/rfp-eval.md`**

Edit the Steps section (currently lines 18-21):

```markdown
   This runs four Claude Agent SDK evaluations concurrently — single agent,
   the coordinator→specialists swarm (Task B), an agent-teams run (Claude
   Code's experimental Agent Teams mode delegating to the project's
   specialist sub-agents), and a dynamic workflow — captures real cost +
   token usage from each run's `ResultMessage`, sends the outputs to an LLM
   judge, and writes `outputs/eval/index.html`.
```

- [ ] **Step 3: Update `rfp_eval/__main__.py`**

```python
    parser = argparse.ArgumentParser(
        prog="rfp_eval",
        description="Run the RFP through single / swarm / dynamic / agent-teams "
        "strategies on the Claude Agent SDK and build a charted cost/quality report.",
    )
```

- [ ] **Step 4: Run the full suite as a sanity check**

```bash
cd /Users/vadim_dissa/dev/black-belt/codespaces/claude-practice
uv run pytest -q
```

Expected: PASS (docs/CLI string changes don't affect any test).

- [ ] **Step 5: Commit**

```bash
git add task07-claude-code-rfp-agent/CLAUDE.md task07-claude-code-rfp-agent/.claude/commands/rfp-eval.md task07-claude-code-rfp-agent/rfp_eval/__main__.py
git commit -m "docs(rfp-eval): document the agent_teams strategy"
```

---

### Task 5: Full regression + live smoke verification

**Files:** none (verification only).

- [ ] **Step 1: Run the full test suite**

```bash
cd /Users/vadim_dissa/dev/black-belt/codespaces/claude-practice
uv run pytest -q
```

Expected: PASS, all tests green (36 tests: the prior 32 + 4 new from Tasks 1 and 3).

- [ ] **Step 2 (optional, spends real tokens — confirm with the user before running): live smoke test**

```bash
cd task07-claude-code-rfp-agent
uv run python -m rfp_eval --rfp synthetic-data/rfp-acme-corp.md --out outputs
```

- [ ] **Step 3: Verify the four-strategy outputs on disk**

```bash
ls outputs/runs/agent_teams/          # expect: proposal.docx, proposal.md (or .txt), risk-assessment.html, run.json
python3 -c "import json; d=json.load(open('outputs/eval/metrics.json')); print([m['strategy_key'] for m in d])"
# expect: ['single', 'swarm', 'dynamic', 'agent_teams']
python3 -c "import json; d=json.load(open('outputs/eval/quality.json')); print([q['strategy_key'] for q in d])"
# expect: ['single', 'swarm', 'dynamic', 'agent_teams']
open outputs/eval/index.html
```

Confirm visually: the cost chart, token chart, quality radar, and summary table each show 4 bars/rows/series, and "Agent Teams" appears as a label. If `agent_teams`'s `run.json` shows `is_error: true` or the deal-desk-orchestrator's outputs land at its own hardcoded paths (`outputs/proposal-<customer>-<date>.docx` per `.claude/agents/deal-desk-orchestrator.md:47`) instead of `{out_dir}/proposal.docx`, the agent-teams delegation didn't respect the harness's file-path instructions in `strategies.COMMON_TASK` — investigate whether `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is actually honored by `claude_agent_sdk.query()` (vs. only the interactive CLI) before changing the preamble further.

---

## Self-Review Notes

- **Spec coverage:** "add agent teams in addition to dynamic, single and swarm" → Task 1. "same logic should apply" (data-driven, no special-casing) → confirmed via Tasks 2/3 requiring zero production changes to `orchestrator.py`/`report.py`. "reports should be generated in runs" → `outputs/runs/agent_teams/run.json` assertions in Task 2. "appear in eval folder" → `outputs/eval/metrics.json`/`quality.json` assertions in Task 2. "and resulting index.html" → `"Agent Teams" in html` assertions in Tasks 2 and 3, plus manual visual check in Task 5.
- **Placeholder scan:** no TBD/TODO; all code blocks are complete, copy-pasteable.
- **Type consistency:** `strategy_key` used consistently as the field name everywhere (never `strategy` or `name`) in new fixtures; `RunMetrics`/`QualityScore` positional args match the dataclass field order already used in `test_report.py`'s existing `_metrics()`/`_scores()` helpers.
