# RFP Agent SDK Swarm + Strategy Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one Claude Agent SDK project that (Task B) implements the Acme RFP flow as a coordinator→specialists **swarm**, and (Task A) runs that swarm plus a single-agent and a dynamic-workflow variant, capturing real per-run cost/token usage from the SDK, LLM-judging output quality, and rendering a fancy `index.html` comparison dashboard. A project-level `/rfp-eval` slash command drives it.

**Architecture:** Everything runs on the `claude-agent-sdk` Python package, which executes the Claude Code agent loop in-process and returns a `ResultMessage` carrying real `total_cost_usd` + `usage` per run — so the comparison uses accurate cost, not estimates. `setting_sources=["project"]` + `cwd=<task dir>` make each run pick up the existing `.claude/agents`, skills, and `settings.json` (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). The **swarm** (Task B) is a first-class module that defines the specialist workers as SDK `AgentDefinition`s (each bound to a project skill) coordinated by a system-prompted coordinator query. The three **strategies** (Task A) are: `single` (one query, no delegation), `swarm` (the Task B module), `dynamic` (plan-then-execute query). An orchestrator runs the three concurrently with `asyncio.gather`, extracts metrics, sends artifacts to an LLM judge (another SDK query), and renders the dashboard (Chart.js). Every SDK boundary is injected via a `query_fn` parameter defaulting to the real `query`, so the pytest suite runs entirely on fakes — no real agent runs, no tokens spent.

**Tech Stack:** Python 3.14, `uv`, `claude-agent-sdk` (+ the `claude` CLI v2.1.198, already installed), `pytest` (dev dep, async tests driven via `asyncio.run` — no plugin), stdlib `asyncio`/`json`/`string`, `pypandoc-binary` (already present, docx→text for judging), Chart.js (CDN, in the report only).

## Global Constraints

- All new code lives under `task07-claude-code-rfp-agent/`. Package: `task07-claude-code-rfp-agent/rfp_eval/`. Tests: `task07-claude-code-rfp-agent/tests/`.
- Repo root is the working directory: `/Users/vadim_dissa/dev/black-belt/codespaces/claude-practice`. All commands run from repo root unless stated. Use `uv run ...` for every Python/pytest invocation — never a bare `python`/`pytest`.
- `claude-agent-sdk` API (verified against the current SDK): `query(prompt=..., options=ClaudeAgentOptions(...))` is an async generator yielding message objects; the terminal `ResultMessage` has fields `total_cost_usd: float | None`, `usage: dict | None`, `num_turns: int`, `duration_ms: int`, `is_error: bool`, `result: str | None`, `model_usage: dict | None`, `session_id: str`. `usage` uses the same token keys as the CLI: `input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`. Missing keys default to `0`/`False`, never raise.
- `ClaudeAgentOptions` fields used: `agents: dict[str, AgentDefinition]`, `setting_sources: list[str]` (values `"user"|"project"|"local"`; use `["project"]` to load `.claude/`), `cwd: str | Path`, `model: str | None`, `permission_mode: str` (use `"bypassPermissions"` for unattended file writes + bash), `system_prompt: str`, `allowed_tools: list[str]`, `max_turns: int | None`.
- `AgentDefinition` fields used: `description: str`, `prompt: str`, `tools: list[str] | None`, `model: str | None`, `skills: list[str] | None`.
- Strategy differentiation is by prompt + options (all data-driven in `strategies.py`/`swarm.py`), since agent-teams is a session/settings toggle and dynamic-workflow is prompt-driven — there is no per-strategy CLI flag. The project `settings.json` already sets `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, loaded via `setting_sources=["project"]`.
- Runs write files + run bash/skills and are unattended, hence `permission_mode="bypassPermissions"`. This is intentional and scoped to the task dir; never apply it elsewhere.
- No real `claude`/SDK subprocess may be spawned from the pytest suite. Every function that runs a query takes an injectable `query_fn` (async) defaulting to the SDK `query`; tests pass an async-generator fake yielding duck-typed message objects.
- Message inspection is duck-typed: a message is the result if it has a `total_cost_usd` attribute; assistant text is any message with a `content` list whose blocks may have `.text`. This keeps tests free of SDK message-class constructors.

## File Structure

- `task07-claude-code-rfp-agent/rfp_eval/__init__.py` — package marker.
- `rfp_eval/strategies.py` — the three strategy keys/labels + prompt/options builder for `single` and `dynamic`. Responsibility: *what each non-swarm strategy is*.
- `rfp_eval/swarm.py` — **Task B**: the SDK swarm — specialist `AgentDefinition`s + coordinator system prompt + `build_swarm_call`. Responsibility: *the Agent SDK swarm*.
- `rfp_eval/sdk_runner.py` — run one `query()` to completion, collect text + normalize the `ResultMessage`. Responsibility: *executing a query*.
- `rfp_eval/metrics.py` — normalize a run's raw dict into comparable `RunMetrics`. Responsibility: *cost/token math*.
- `rfp_eval/judge.py` — rubric, judge prompt, artifact collection, judge query + parse. Responsibility: *quality scoring*.
- `rfp_eval/report.py` — merge metrics+scores into report data, render/write `index.html`. Responsibility: *the report*.
- `rfp_eval/templates/report.html.tmpl` — the HTML/JS/CSS shell (Chart.js), data injected via a `__REPORT_DATA__` marker.
- `rfp_eval/orchestrator.py` — async: run the three strategies concurrently → metrics → judge → report. Responsibility: *end-to-end flow*.
- `rfp_eval/__main__.py` — argparse CLI (`uv run python -m rfp_eval`), wraps `asyncio.run`.
- `task07-claude-code-rfp-agent/tests/` — one test module per package module + `fixtures/`.
- `.claude/commands/rfp-eval.md` — the slash command.
- `outputs/.gitignore` — ignore generated runs/eval, keep the folder.
- Root `pyproject.toml` — add `claude-agent-sdk` dep, `pytest` dev dep, `[tool.pytest.ini_options]`.

---

## Task 1: Scaffold, deps, and non-swarm strategies

**Files:**
- Modify: `pyproject.toml` (repo root)
- Create: `task07-claude-code-rfp-agent/rfp_eval/__init__.py`
- Create: `task07-claude-code-rfp-agent/rfp_eval/strategies.py`
- Create: `task07-claude-code-rfp-agent/tests/__init__.py`
- Create: `task07-claude-code-rfp-agent/tests/test_strategies.py`

**Interfaces:**
- Consumes: `claude_agent_sdk.ClaudeAgentOptions` (imported lazily inside the builder so tests can run without a configured CLI).
- Produces:
  - `STRATEGY_KEYS: list[str]` = `["single", "swarm", "dynamic"]`.
  - `LABELS: dict[str, str]` = `{"single": "Single Agent", "swarm": "Agent Swarm", "dynamic": "Dynamic Workflow"}`.
  - `COMMON_TASK: str` — the shared deliverable instructions template with `{rfp_path}` / `{out_dir}` placeholders.
  - `build_call(key: str, *, task_dir, rfp_path, out_dir, model=None) -> tuple[str, ClaudeAgentOptions]` — for `single` and `dynamic` only (raises `ValueError` for `swarm`, which Task 4 wires in).
  - `render_prompt(preamble: str, rfp_path, out_dir) -> str`.

- [ ] **Step 1: Add dependencies**

Run:
```bash
uv add claude-agent-sdk
uv add --dev pytest
```
Expected: `pyproject.toml` gains `claude-agent-sdk` under `[project].dependencies` and `pytest` under `[dependency-groups].dev`; `uv.lock` updates.

- [ ] **Step 2: Add pytest config to `pyproject.toml`**

Append to the end of `pyproject.toml` (repo root):
```toml
[tool.pytest.ini_options]
testpaths = ["task07-claude-code-rfp-agent/tests"]
pythonpath = ["task07-claude-code-rfp-agent"]
addopts = "-q"
```

- [ ] **Step 3: Create package + test markers**

Create `task07-claude-code-rfp-agent/rfp_eval/__init__.py`:
```python
"""RFP Agent SDK swarm + strategy evaluation harness."""
```

Create `task07-claude-code-rfp-agent/tests/__init__.py`:
```python
```
(empty file)

- [ ] **Step 4: Write the failing test**

Create `task07-claude-code-rfp-agent/tests/test_strategies.py`:
```python
import pytest

from rfp_eval import strategies as s


def test_strategy_keys_and_labels():
    assert s.STRATEGY_KEYS == ["single", "swarm", "dynamic"]
    assert s.LABELS["swarm"] == "Agent Swarm"
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


def test_build_call_swarm_rejected_here():
    with pytest.raises(ValueError):
        s.build_call("swarm", task_dir="/task", rfp_path="rfp.md", out_dir="/o")
```

- [ ] **Step 5: Run test to verify it fails**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_strategies.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'rfp_eval.strategies'`.

- [ ] **Step 6: Write minimal implementation**

Create `task07-claude-code-rfp-agent/rfp_eval/strategies.py`:
```python
"""Non-swarm strategy definitions (single agent, dynamic workflow)."""

from __future__ import annotations

from pathlib import Path

STRATEGY_KEYS: list[str] = ["single", "swarm", "dynamic"]

LABELS: dict[str, str] = {
    "single": "Single Agent",
    "swarm": "Agent Swarm",
    "dynamic": "Dynamic Workflow",
}

COMMON_TASK = """\
You are processing an inbound RFP for the BTS-Synthetic Deal Desk.

RFP file: {rfp_path}
Reference data (read as needed): synthetic-data/past-wins.json, \
synthetic-data/product-overview.md

Produce BOTH deliverables and save them into the directory {out_dir}:
1. A customer-facing branded proposal at {out_dir}/proposal.docx (use the docx skill).
2. An internal risk-assessment dashboard at {out_dir}/risk-assessment.html \
(use the risk-assessment skill).

Use the available project skills: pricing-playbook, legal-checklist, \
competitive-intel, risk-assessment, docx. When finished, print a one-line \
confirmation naming the two files you wrote.
"""

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
}


def render_prompt(preamble: str, rfp_path: str | Path, out_dir: str | Path) -> str:
    task = COMMON_TASK.format(rfp_path=rfp_path, out_dir=out_dir)
    return f"{preamble}\n\n{task}"


def build_call(
    key: str,
    *,
    task_dir: str | Path,
    rfp_path: str | Path,
    out_dir: str | Path,
    model: str | None = None,
):
    """Return (prompt, ClaudeAgentOptions) for a non-swarm strategy."""
    if key not in _PREAMBLES:
        raise ValueError(f"build_call handles single/dynamic only, not {key!r}")
    from claude_agent_sdk import ClaudeAgentOptions

    prompt = render_prompt(_PREAMBLES[key], rfp_path, out_dir)
    options = ClaudeAgentOptions(
        cwd=str(task_dir),
        setting_sources=["project"],
        permission_mode="bypassPermissions",
        model=model,
    )
    return prompt, options
```

- [ ] **Step 7: Run test to verify it passes**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_strategies.py -q`
Expected: PASS (5 passed).

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml uv.lock task07-claude-code-rfp-agent/rfp_eval task07-claude-code-rfp-agent/tests
git commit -m "feat(rfp-eval): scaffold Agent SDK harness + single/dynamic strategies"
```

---

## Task 2: SDK query runner

**Files:**
- Create: `task07-claude-code-rfp-agent/rfp_eval/sdk_runner.py`
- Create: `task07-claude-code-rfp-agent/tests/test_sdk_runner.py`

**Interfaces:**
- Consumes: `claude_agent_sdk.query` (as the default `query_fn`).
- Produces:
  - `RunResult` dataclass: `key: str`, `result_text: str`, `raw: dict`.
  - `result_to_dict(result_msg) -> dict` — normalizes a `ResultMessage` (or `None`) into `{total_cost_usd, usage, num_turns, duration_ms, is_error, result}`.
  - `async run_query(prompt: str, *, options=None, key: str = "", query_fn=<sdk query>) -> RunResult`.

- [ ] **Step 1: Write the failing test**

Create `task07-claude-code-rfp-agent/tests/test_sdk_runner.py`:
```python
import asyncio
from types import SimpleNamespace

from rfp_eval import sdk_runner


def _fake_result():
    return SimpleNamespace(
        total_cost_usd=0.42,
        usage={
            "input_tokens": 1200,
            "output_tokens": 8000,
            "cache_read_input_tokens": 150000,
            "cache_creation_input_tokens": 30000,
        },
        num_turns=6,
        duration_ms=42000,
        is_error=False,
        result="Wrote proposal.docx and risk-assessment.html",
    )


def _text_msg(text):
    # duck-typed AssistantMessage: has .content list of blocks with .text
    return SimpleNamespace(content=[SimpleNamespace(text=text)])


def test_result_to_dict_normalizes():
    d = sdk_runner.result_to_dict(_fake_result())
    assert d["total_cost_usd"] == 0.42
    assert d["usage"]["output_tokens"] == 8000
    assert d["num_turns"] == 6
    assert d["is_error"] is False


def test_result_to_dict_none():
    assert sdk_runner.result_to_dict(None) == {}


def test_run_query_collects_result_and_text():
    async def fake_query(prompt, options=None):
        yield _text_msg("working...")
        yield _fake_result()

    result = asyncio.run(
        sdk_runner.run_query("do it", key="single", query_fn=fake_query)
    )
    assert result.key == "single"
    assert result.raw["total_cost_usd"] == 0.42
    # prefers ResultMessage.result text
    assert "proposal.docx" in result.result_text


def test_run_query_falls_back_to_assistant_text_when_no_result_text():
    fr = _fake_result()
    fr.result = None

    async def fake_query(prompt, options=None):
        yield _text_msg("only assistant text")
        yield fr

    result = asyncio.run(sdk_runner.run_query("p", query_fn=fake_query))
    assert result.result_text == "only assistant text"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_sdk_runner.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'rfp_eval.sdk_runner'`.

- [ ] **Step 3: Write minimal implementation**

Create `task07-claude-code-rfp-agent/rfp_eval/sdk_runner.py`:
```python
"""Run one Claude Agent SDK query to completion and normalize its result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RunResult:
    key: str
    result_text: str
    raw: dict


def result_to_dict(result_msg) -> dict:
    if result_msg is None:
        return {}
    return {
        "total_cost_usd": getattr(result_msg, "total_cost_usd", 0.0) or 0.0,
        "usage": getattr(result_msg, "usage", None) or {},
        "num_turns": getattr(result_msg, "num_turns", 0) or 0,
        "duration_ms": getattr(result_msg, "duration_ms", 0) or 0,
        "is_error": bool(getattr(result_msg, "is_error", False)),
        "result": getattr(result_msg, "result", None),
    }


def _default_query_fn():
    from claude_agent_sdk import query

    return query


async def run_query(prompt: str, *, options=None, key: str = "", query_fn=None) -> RunResult:
    if query_fn is None:
        query_fn = _default_query_fn()
    text_parts: list[str] = []
    result_msg = None
    async for msg in query_fn(prompt=prompt, options=options):
        if hasattr(msg, "total_cost_usd"):  # ResultMessage
            result_msg = msg
            continue
        content = getattr(msg, "content", None)
        if isinstance(content, list):
            for block in content:
                text = getattr(block, "text", None)
                if text:
                    text_parts.append(text)
    raw = result_to_dict(result_msg)
    result_text = raw.get("result") or "".join(text_parts)
    return RunResult(key=key, result_text=result_text, raw=raw)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_sdk_runner.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add task07-claude-code-rfp-agent/rfp_eval/sdk_runner.py task07-claude-code-rfp-agent/tests/test_sdk_runner.py
git commit -m "feat(rfp-eval): Agent SDK query runner + result normalization"
```

---

## Task 3: Metrics extraction

**Files:**
- Create: `task07-claude-code-rfp-agent/rfp_eval/metrics.py`
- Create: `task07-claude-code-rfp-agent/tests/test_metrics.py`

**Interfaces:**
- Consumes: a run's normalized `raw` dict (from `sdk_runner.result_to_dict`).
- Produces:
  - `RunMetrics` dataclass: `strategy_key: str`, `cost_usd: float`, `input_tokens: int`, `output_tokens: int`, `cache_read_tokens: int`, `cache_creation_tokens: int`, `total_tokens: int`, `num_turns: int`, `duration_ms: int`, `is_error: bool`.
  - `extract_metrics(strategy_key: str, raw: dict) -> RunMetrics`.
  - `metrics_as_dict(m: RunMetrics) -> dict`.

- [ ] **Step 1: Write the failing test**

Create `task07-claude-code-rfp-agent/tests/test_metrics.py`:
```python
import json

from rfp_eval import metrics

RAW = {
    "total_cost_usd": 0.42,
    "usage": {
        "input_tokens": 1200,
        "output_tokens": 8000,
        "cache_read_input_tokens": 150000,
        "cache_creation_input_tokens": 30000,
    },
    "num_turns": 6,
    "duration_ms": 42000,
    "is_error": False,
}


def test_extract_metrics():
    m = metrics.extract_metrics("single", RAW)
    assert m.strategy_key == "single"
    assert m.cost_usd == 0.42
    assert m.input_tokens == 1200
    assert m.output_tokens == 8000
    assert m.cache_read_tokens == 150000
    assert m.cache_creation_tokens == 30000
    assert m.total_tokens == 189200
    assert m.num_turns == 6
    assert m.duration_ms == 42000
    assert m.is_error is False


def test_extract_metrics_defaults_on_empty():
    m = metrics.extract_metrics("swarm", {})
    assert m.cost_usd == 0.0
    assert m.total_tokens == 0
    assert m.is_error is False


def test_metrics_as_dict_is_json_serializable():
    d = metrics.metrics_as_dict(metrics.extract_metrics("single", RAW))
    assert d["total_tokens"] == 189200
    assert json.dumps(d)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_metrics.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'rfp_eval.metrics'`.

- [ ] **Step 3: Write minimal implementation**

Create `task07-claude-code-rfp-agent/rfp_eval/metrics.py`:
```python
"""Normalize a run's raw dict into comparable metrics."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class RunMetrics:
    strategy_key: str
    cost_usd: float
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_creation_tokens: int
    total_tokens: int
    num_turns: int
    duration_ms: int
    is_error: bool


def extract_metrics(strategy_key: str, raw: dict) -> RunMetrics:
    usage = raw.get("usage") or {}
    inp = int(usage.get("input_tokens", 0) or 0)
    out = int(usage.get("output_tokens", 0) or 0)
    cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
    cache_creation = int(usage.get("cache_creation_input_tokens", 0) or 0)
    return RunMetrics(
        strategy_key=strategy_key,
        cost_usd=float(raw.get("total_cost_usd", 0.0) or 0.0),
        input_tokens=inp,
        output_tokens=out,
        cache_read_tokens=cache_read,
        cache_creation_tokens=cache_creation,
        total_tokens=inp + out + cache_read + cache_creation,
        num_turns=int(raw.get("num_turns", 0) or 0),
        duration_ms=int(raw.get("duration_ms", 0) or 0),
        is_error=bool(raw.get("is_error", False)),
    )


def metrics_as_dict(m: RunMetrics) -> dict:
    return asdict(m)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_metrics.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add task07-claude-code-rfp-agent/rfp_eval/metrics.py task07-claude-code-rfp-agent/tests/test_metrics.py
git commit -m "feat(rfp-eval): cost/token metrics extraction"
```

---

## Task 4: The Agent SDK swarm (Task B) + swarm strategy

**Files:**
- Create: `task07-claude-code-rfp-agent/rfp_eval/swarm.py`
- Modify: `task07-claude-code-rfp-agent/rfp_eval/strategies.py` (route `swarm` to `swarm.build_swarm_call`)
- Create: `task07-claude-code-rfp-agent/tests/test_swarm.py`
- Modify: `task07-claude-code-rfp-agent/tests/test_strategies.py` (swarm now builds instead of raising)

**Interfaces:**
- Consumes: `claude_agent_sdk.AgentDefinition`, `claude_agent_sdk.ClaudeAgentOptions`, `strategies.render_prompt`.
- Produces:
  - `WORKERS: dict[str, AgentDefinition]` — `pricing`, `legal`, `technical-fit`, `competitive`, `risk-assessment`, each bound to its project skill.
  - `COORDINATOR_SYSTEM: str` — the coordinator's system prompt (the Task B swarm coordinator).
  - `build_swarm_call(*, task_dir, rfp_path, out_dir, model=None) -> tuple[str, ClaudeAgentOptions]` — options carry `agents=WORKERS`, `setting_sources=["project"]`, `cwd`, `system_prompt=COORDINATOR_SYSTEM`, `permission_mode="bypassPermissions"`.
- Contract change: `strategies.build_call("swarm", ...)` now delegates to `build_swarm_call` (no longer raises).

- [ ] **Step 1: Update the swarm expectation in `test_strategies.py`**

In `task07-claude-code-rfp-agent/tests/test_strategies.py`, replace `test_build_call_swarm_rejected_here` with:
```python
def test_build_call_swarm_delegates_to_swarm_module():
    prompt, options = s.build_call(
        "swarm", task_dir="/task", rfp_path="rfp.md", out_dir="/task/outputs/runs/swarm"
    )
    assert "coordinator" in prompt.lower() or "swarm" in prompt.lower()
    assert options.agents is not None
    assert "pricing" in options.agents
```

- [ ] **Step 2: Write the failing swarm test**

Create `task07-claude-code-rfp-agent/tests/test_swarm.py`:
```python
from rfp_eval import swarm


def test_workers_cover_the_diagram_roles():
    assert set(swarm.WORKERS) == {
        "pricing",
        "legal",
        "technical-fit",
        "competitive",
        "risk-assessment",
    }


def test_each_worker_binds_a_skill():
    assert swarm.WORKERS["pricing"].skills == ["pricing-playbook"]
    assert swarm.WORKERS["legal"].skills == ["legal-checklist"]
    assert swarm.WORKERS["competitive"].skills == ["competitive-intel"]
    assert swarm.WORKERS["risk-assessment"].skills == ["risk-assessment"]
    # risk worker must be able to write its HTML dashboard
    assert "Write" in (swarm.WORKERS["risk-assessment"].tools or [])


def test_build_swarm_call_shapes_options():
    prompt, options = swarm.build_swarm_call(
        task_dir="/task", rfp_path="synthetic-data/rfp-acme-corp.md", out_dir="/task/outputs/runs/swarm"
    )
    assert "synthetic-data/rfp-acme-corp.md" in prompt
    assert "/task/outputs/runs/swarm" in prompt
    assert options.agents is swarm.WORKERS
    assert options.setting_sources == ["project"]
    assert str(options.cwd) == "/task"
    assert options.permission_mode == "bypassPermissions"
    assert "coordinator" in (options.system_prompt or "").lower()
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_swarm.py task07-claude-code-rfp-agent/tests/test_strategies.py -q`
Expected: FAIL — `test_swarm.py` with `ModuleNotFoundError: No module named 'rfp_eval.swarm'`; the updated strategies test fails because `build_call("swarm", ...)` still raises `ValueError`.

- [ ] **Step 4: Write the swarm module**

Create `task07-claude-code-rfp-agent/rfp_eval/swarm.py`:
```python
"""Task B — the RFP deal-desk swarm, built on the Claude Agent SDK.

A coordinator query delegates to specialist worker agents (each bound to a
project skill). Workers produce their findings; the coordinator synthesizes a
branded proposal (.docx) and commissions the risk-assessment dashboard (.html).
"""

from __future__ import annotations

from pathlib import Path

from .strategies import render_prompt

_SWARM_PREAMBLE = (
    "Run this RFP as an AGENT SWARM. You are the coordinator: delegate to your "
    "specialist agents (pricing, legal, technical-fit, competitive) in parallel, "
    "then synthesize their findings into the proposal, and finally delegate to "
    "the risk-assessment agent to produce the internal dashboard."
)

COORDINATOR_SYSTEM = (
    "You are the Senior Partner running the BTS-Synthetic Deal Desk. Orchestrate "
    "your specialist agents, synthesize their work into a single branded proposal, "
    "and commission an internal risk assessment before anything goes out. Delegate "
    "the first four specialists in parallel with narrow briefs; accept their "
    "replies; then produce the deliverables. Be decisive and move fast."
)


def _worker(description: str, prompt: str, skill: str, *, can_write: bool = False):
    from claude_agent_sdk import AgentDefinition

    tools = ["Read", "Grep", "Glob", "Bash"]
    if can_write:
        tools = ["Read", "Write", "Grep", "Glob", "Bash"]
    return AgentDefinition(
        description=description,
        prompt=prompt,
        tools=tools,
        model="sonnet",
        skills=[skill],
    )


def _build_workers():
    return {
        "pricing": _worker(
            "Commercial terms recommendation for an RFP.",
            "You are the Pricing Specialist. Recommend commercial terms: discount "
            "band and red-line concessions. Cite past-wins.json where relevant. "
            "Answer in one message (~300 words).",
            "pricing-playbook",
        ),
        "legal": _worker(
            "Contract flags and counter-positions for an RFP.",
            "You are the Legal Reviewer. Flag contractual risks with severities and "
            "give counter-positions. Answer in one message (~300 words).",
            "legal-checklist",
        ),
        "technical-fit": _worker(
            "Product capability fit for an RFP.",
            "You are the Technical Fit Specialist. Score product fit against the RFP "
            "requirements and note gaps. Answer in one message (~300 words).",
            "competitive-intel",  # reuses reference material; no dedicated tech skill
        ),
        "competitive": _worker(
            "Competitive positioning for an RFP.",
            "You are the Competitive Intel Analyst. Identify likely competitors and "
            "how to position against them. Answer in one message (~300 words).",
            "competitive-intel",
        ),
        "risk-assessment": _worker(
            "Internal risk vs. revenue dashboard (HTML) for an RFP.",
            "You are the Risk Assessment Specialist. Run your three-step risk "
            "framework and write a self-contained interactive HTML dashboard.",
            "risk-assessment",
            can_write=True,
        ),
    }


WORKERS = _build_workers()


def build_swarm_call(
    *,
    task_dir: str | Path,
    rfp_path: str | Path,
    out_dir: str | Path,
    model: str | None = None,
):
    from claude_agent_sdk import ClaudeAgentOptions

    prompt = render_prompt(_SWARM_PREAMBLE, rfp_path, out_dir)
    options = ClaudeAgentOptions(
        cwd=str(task_dir),
        setting_sources=["project"],
        permission_mode="bypassPermissions",
        model=model,
        system_prompt=COORDINATOR_SYSTEM,
        agents=WORKERS,
    )
    return prompt, options
```

Note: `technical-fit` binds `competitive-intel` as a stand-in reference skill because the repo has no dedicated technical-fit skill; the RFP + `product-overview.md` provide the fit context. The comment records why.

- [ ] **Step 5: Route `swarm` in `strategies.build_call`**

In `task07-claude-code-rfp-agent/rfp_eval/strategies.py`, replace the `if key not in _PREAMBLES:` guard block inside `build_call` with:
```python
    if key == "swarm":
        from . import swarm

        return swarm.build_swarm_call(
            task_dir=task_dir, rfp_path=rfp_path, out_dir=out_dir, model=model
        )
    if key not in _PREAMBLES:
        raise ValueError(f"unknown strategy key {key!r}")
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_swarm.py task07-claude-code-rfp-agent/tests/test_strategies.py -q`
Expected: PASS (3 + 5 passed).

- [ ] **Step 7: Commit**

```bash
git add task07-claude-code-rfp-agent/rfp_eval/swarm.py task07-claude-code-rfp-agent/rfp_eval/strategies.py task07-claude-code-rfp-agent/tests/test_swarm.py task07-claude-code-rfp-agent/tests/test_strategies.py
git commit -m "feat(rfp-eval): Agent SDK swarm (Task B) + swarm strategy"
```

---

## Task 5: LLM judge

**Files:**
- Create: `task07-claude-code-rfp-agent/rfp_eval/judge.py`
- Create: `task07-claude-code-rfp-agent/tests/test_judge.py`

**Interfaces:**
- Consumes: per-strategy artifact text; `sdk_runner.run_query`.
- Produces:
  - `RUBRIC: list[tuple[str, str]]`; `RUBRIC_DIMS: list[str]` = `["completeness", "specificity", "actionability", "risk_depth", "correctness"]`.
  - `QualityScore` dataclass: `strategy_key: str`, `scores: dict[str, int]`, `total: int`, `rationale: str`.
  - `read_artifacts(out_dir, *, max_chars=12000) -> str`.
  - `build_judge_prompt(artifacts: dict[str, str]) -> str`.
  - `parse_judge_output(text: str) -> list[QualityScore]`.
  - `async judge_quality(artifacts, *, model="sonnet", query_fn=None) -> list[QualityScore]`.

- [ ] **Step 1: Write the failing test**

Create `task07-claude-code-rfp-agent/tests/test_judge.py`:
```python
import asyncio
from pathlib import Path
from types import SimpleNamespace

from rfp_eval import judge

JUDGE_TEXT = """Here are my scores:
```json
[
 {"strategy":"single","scores":{"completeness":3,"specificity":3,"actionability":4,"risk_depth":2,"correctness":4},"rationale":"Shallow risk."},
 {"strategy":"swarm","scores":{"completeness":5,"specificity":4,"actionability":4,"risk_depth":5,"correctness":4},"rationale":"Deepest."},
 {"strategy":"dynamic","scores":{"completeness":4,"specificity":4,"actionability":5,"risk_depth":3,"correctness":4},"rationale":"Well planned."}
]
```
"""


def test_rubric_dims():
    assert judge.RUBRIC_DIMS == [
        "completeness", "specificity", "actionability", "risk_depth", "correctness",
    ]


def test_build_judge_prompt_has_artifacts_and_rubric():
    p = judge.build_judge_prompt({"single": "S-OUT", "swarm": "W-OUT"})
    assert "S-OUT" in p and "W-OUT" in p
    assert "risk_depth" in p
    assert "JSON" in p


def test_parse_judge_output():
    scores = judge.parse_judge_output(JUDGE_TEXT)
    by = {s.strategy_key: s for s in scores}
    assert set(by) == {"single", "swarm", "dynamic"}
    assert by["swarm"].scores["risk_depth"] == 5
    assert by["swarm"].total == 22
    assert "Deepest" in by["swarm"].rationale


def test_read_artifacts_reads_html_and_truncates(tmp_path):
    (tmp_path / "risk-assessment.html").write_text("<html>RISK</html>" * 2000)
    text = judge.read_artifacts(tmp_path, max_chars=100)
    assert "RISK" in text and len(text) <= 100


def test_read_artifacts_missing(tmp_path):
    assert "no artifacts" in judge.read_artifacts(tmp_path / "nope").lower()


def test_judge_quality_uses_injected_query_fn():
    async def fake_query(prompt, options=None):
        yield SimpleNamespace(
            total_cost_usd=0.05, usage={}, num_turns=1, duration_ms=1,
            is_error=False, result=JUDGE_TEXT,
        )

    scores = asyncio.run(
        judge.judge_quality({"single": "a", "swarm": "b", "dynamic": "c"}, query_fn=fake_query)
    )
    assert {s.strategy_key for s in scores} == {"single", "swarm", "dynamic"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_judge.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'rfp_eval.judge'`.

- [ ] **Step 3: Write minimal implementation**

Create `task07-claude-code-rfp-agent/rfp_eval/judge.py`:
```python
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
    chunks: list[str] = []
    seen = False
    for name in _ARTIFACT_NAMES:
        p = out_dir / name
        if p.exists():
            seen = True
            chunks.append(f"--- {name} ---\n{p.read_text(errors='replace')}")
    docx = out_dir / "proposal.docx"
    if docx.exists():
        try:
            import pypandoc

            seen = True
            chunks.append(
                f"--- proposal.docx ---\n{pypandoc.convert_file(str(docx), 'plain')}"
            )
        except Exception:
            pass
    if not seen:
        return "(no artifacts found)"
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_judge.py -q`
Expected: PASS (6 passed).

- [ ] **Step 5: Commit**

```bash
git add task07-claude-code-rfp-agent/rfp_eval/judge.py task07-claude-code-rfp-agent/tests/test_judge.py
git commit -m "feat(rfp-eval): LLM judge with rubric + artifact collection"
```

---

## Task 6: Report data + HTML rendering

**Files:**
- Create: `task07-claude-code-rfp-agent/rfp_eval/templates/report.html.tmpl`
- Create: `task07-claude-code-rfp-agent/rfp_eval/report.py`
- Create: `task07-claude-code-rfp-agent/tests/test_report.py`

**Interfaces:**
- Consumes: `metrics.RunMetrics` list, `judge.QualityScore` list, `judge.RUBRIC_DIMS`, `strategies.LABELS`, `strategies.STRATEGY_KEYS`.
- Produces:
  - `build_report_data(metrics, scores, *, rfp="", generated_at=None) -> dict` — merges by `strategy_key`; each entry has metric fields + `label`, `quality` (`{dim: int, ..., "total": int, "rationale": str}`), `quality_per_dollar: float`. Top-level: `strategies` (in `STRATEGY_KEYS` order), `rubric_dims`, `winner_quality`, `winner_value`, `rfp`, `generated_at`.
  - `render_report(data, *, template_path=None) -> str`.
  - `write_report(html, dest) -> Path`.
  - `DEFAULT_TEMPLATE: Path`.

> **Note for the implementer:** Before writing the template, consult the `dataviz` skill for palette + chart guidance. The template below uses a small brand-neutral palette consistent with it; keep or swap for the dataviz palette.

- [ ] **Step 1: Write the failing test**

Create `task07-claude-code-rfp-agent/tests/test_report.py`:
```python
import json
import re

from rfp_eval import report
from rfp_eval.judge import QualityScore
from rfp_eval.metrics import RunMetrics


def _metrics():
    return [
        RunMetrics("single", 0.42, 1200, 8000, 150000, 30000, 189200, 6, 42000, False),
        RunMetrics("swarm", 1.10, 3000, 15000, 400000, 60000, 478000, 14, 90000, False),
        RunMetrics("dynamic", 0.75, 2000, 11000, 250000, 40000, 303000, 9, 65000, False),
    ]


def _scores():
    return [
        QualityScore("single", {"completeness": 3, "specificity": 3, "actionability": 4, "risk_depth": 2, "correctness": 4}, 16, "ok"),
        QualityScore("swarm", {"completeness": 5, "specificity": 4, "actionability": 4, "risk_depth": 5, "correctness": 4}, 22, "best"),
        QualityScore("dynamic", {"completeness": 4, "specificity": 4, "actionability": 5, "risk_depth": 3, "correctness": 4}, 20, "good"),
    ]


def test_build_report_data_merges_and_ranks():
    data = report.build_report_data(_metrics(), _scores(), rfp="rfp-acme-corp.md")
    assert [s["strategy_key"] for s in data["strategies"]] == ["single", "swarm", "dynamic"]
    swarm = next(s for s in data["strategies"] if s["strategy_key"] == "swarm")
    assert swarm["label"] == "Agent Swarm"
    assert swarm["quality"]["total"] == 22
    single = next(s for s in data["strategies"] if s["strategy_key"] == "single")
    assert round(single["quality_per_dollar"], 2) == round(16 / 0.42, 2)
    assert data["winner_quality"] == "swarm"
    assert data["winner_value"] == "single"
    assert data["rubric_dims"] == ["completeness", "specificity", "actionability", "risk_depth", "correctness"]


def test_build_report_data_zero_cost_no_div_error():
    m = [RunMetrics("single", 0.0, 0, 0, 0, 0, 0, 0, 0, True)]
    s = [QualityScore("single", {d: 0 for d in report.__import_dims__()}, 0, "err")]
    data = report.build_report_data(m, s)
    assert data["strategies"][0]["quality_per_dollar"] == 0.0


def test_render_report_embeds_data_and_no_marker():
    data = report.build_report_data(_metrics(), _scores(), rfp="rfp.md")
    html = report.render_report(data)
    assert "__REPORT_DATA__" not in html
    assert "Agent Swarm" in html
    assert "chart" in html.lower()
    m = re.search(r"const REPORT_DATA = (\{.*?\});", html, re.DOTALL)
    assert m and json.loads(m.group(1))["winner_quality"] == "swarm"


def test_write_report_creates_file(tmp_path):
    dest = report.write_report("<html>hi</html>", tmp_path / "eval" / "index.html")
    assert dest.exists() and dest.read_text() == "<html>hi</html>"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_report.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'rfp_eval.report'`.

- [ ] **Step 3: Write minimal implementation**

Create `task07-claude-code-rfp-agent/rfp_eval/report.py`:
```python
"""Merge metrics + quality scores and render the comparison dashboard."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .judge import RUBRIC_DIMS, QualityScore
from .metrics import RunMetrics
from .strategies import LABELS, STRATEGY_KEYS

DEFAULT_TEMPLATE = Path(__file__).parent / "templates" / "report.html.tmpl"
_DATA_MARKER = "__REPORT_DATA__"


def __import_dims__() -> list[str]:
    """Expose rubric dims for callers/tests without importing judge directly."""
    return list(RUBRIC_DIMS)


def _quality_per_dollar(total: int, cost: float) -> float:
    return round(total / cost, 4) if cost > 0 else 0.0


def build_report_data(
    metrics: list[RunMetrics],
    scores: list[QualityScore],
    *,
    rfp: str = "",
    generated_at: str | None = None,
) -> dict:
    metrics_by = {m.strategy_key: m for m in metrics}
    scores_by = {s.strategy_key: s for s in scores}
    entries: list[dict] = []
    for key in STRATEGY_KEYS:
        m = metrics_by.get(key)
        if m is None:
            continue
        sc = scores_by.get(key)
        quality = {**(sc.scores if sc else {d: 0 for d in RUBRIC_DIMS})}
        quality["total"] = sc.total if sc else 0
        quality["rationale"] = sc.rationale if sc else ""
        entries.append(
            {
                "strategy_key": key,
                "label": LABELS.get(key, key),
                "cost_usd": m.cost_usd,
                "input_tokens": m.input_tokens,
                "output_tokens": m.output_tokens,
                "cache_read_tokens": m.cache_read_tokens,
                "cache_creation_tokens": m.cache_creation_tokens,
                "total_tokens": m.total_tokens,
                "num_turns": m.num_turns,
                "duration_ms": m.duration_ms,
                "is_error": m.is_error,
                "quality": quality,
                "quality_per_dollar": _quality_per_dollar(quality["total"], m.cost_usd),
            }
        )
    winner_quality = max(entries, key=lambda e: e["quality"]["total"], default=None)
    winner_value = max(entries, key=lambda e: e["quality_per_dollar"], default=None)
    return {
        "rfp": rfp,
        "generated_at": generated_at
        or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "rubric_dims": list(RUBRIC_DIMS),
        "strategies": entries,
        "winner_quality": winner_quality["strategy_key"] if winner_quality else None,
        "winner_value": winner_value["strategy_key"] if winner_value else None,
    }


def render_report(data: dict, *, template_path: Path | None = None) -> str:
    tmpl = (template_path or DEFAULT_TEMPLATE).read_text()
    return tmpl.replace(_DATA_MARKER, json.dumps(data))


def write_report(html: str, dest: str | Path) -> Path:
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    return dest
```

- [ ] **Step 4: Create the HTML template**

Create `task07-claude-code-rfp-agent/rfp_eval/templates/report.html.tmpl`:
```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>RFP Strategy Comparison</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root {
    --bg: #0d1117; --panel: #161b22; --line: #30363d;
    --ink: #e6edf3; --muted: #9198a1; --win: #5bd1a6;
  }
  * { box-sizing: border-box; }
  body { margin: 0; font: 15px/1.5 -apple-system, Segoe UI, Roboto, sans-serif;
    background: var(--bg); color: var(--ink); padding: 32px; }
  h1 { margin: 0 0 4px; font-size: 26px; }
  .sub { color: var(--muted); margin-bottom: 28px; }
  .grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
  .card { background: var(--panel); border: 1px solid var(--line);
    border-radius: 12px; padding: 20px; }
  .card h2 { margin: 0 0 14px; font-size: 15px; color: var(--muted);
    text-transform: uppercase; letter-spacing: .05em; }
  .winner { display: inline-block; background: rgba(91,209,166,.12);
    border: 1px solid var(--win); color: var(--win); border-radius: 999px;
    padding: 4px 12px; margin-right: 10px; font-size: 13px; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th, td { text-align: right; padding: 8px 10px; border-bottom: 1px solid var(--line); }
  th:first-child, td:first-child { text-align: left; }
  canvas { max-height: 300px; }
</style>
</head>
<body>
  <h1>RFP Strategy Comparison</h1>
  <div class="sub" id="meta"></div>
  <div id="winners" style="margin-bottom:24px"></div>
  <div class="grid">
    <div class="card"><h2>Cost per strategy (USD)</h2><canvas id="cost"></canvas></div>
    <div class="card"><h2>Token usage breakdown</h2><canvas id="tokens"></canvas></div>
    <div class="card"><h2>Quality by rubric dimension</h2><canvas id="quality"></canvas></div>
    <div class="card"><h2>Quality per dollar</h2><canvas id="value"></canvas></div>
  </div>
  <div class="card" style="margin-top:20px">
    <h2>Summary</h2>
    <table id="summary"></table>
  </div>
<script>
const REPORT_DATA = __REPORT_DATA__;
const D = REPORT_DATA;
const PALETTE = ['#4c9aff', '#5bd1a6', '#f2b45b'];
const labels = D.strategies.map(s => s.label);

document.getElementById('meta').textContent =
  `RFP: ${D.rfp || 'n/a'} · generated ${D.generated_at}`;

const wq = D.strategies.find(s => s.strategy_key === D.winner_quality);
const wv = D.strategies.find(s => s.strategy_key === D.winner_value);
document.getElementById('winners').innerHTML =
  (wq ? `<span class="winner">🏆 Best quality: ${wq.label}</span>` : '') +
  (wv ? `<span class="winner">💰 Best value: ${wv.label}</span>` : '');

new Chart(document.getElementById('cost'), {
  type: 'bar',
  data: { labels, datasets: [{ label: 'USD', data: D.strategies.map(s => s.cost_usd),
    backgroundColor: PALETTE }] },
  options: { plugins: { legend: { display: false } } }
});

const tokenKeys = ['input_tokens', 'output_tokens', 'cache_read_tokens', 'cache_creation_tokens'];
const tokenLabels = ['Input', 'Output', 'Cache read', 'Cache create'];
new Chart(document.getElementById('tokens'), {
  type: 'bar',
  data: { labels, datasets: tokenKeys.map((k, i) => ({
    label: tokenLabels[i], data: D.strategies.map(s => s[k]),
    backgroundColor: PALETTE[i % PALETTE.length] })) },
  options: { responsive: true, scales: { x: { stacked: true }, y: { stacked: true } } }
});

new Chart(document.getElementById('quality'), {
  type: 'radar',
  data: { labels: D.rubric_dims, datasets: D.strategies.map((s, i) => ({
    label: s.label, data: D.rubric_dims.map(d => s.quality[d]),
    borderColor: PALETTE[i], backgroundColor: PALETTE[i] + '33' })) },
  options: { scales: { r: { min: 0, max: 5 } } }
});

new Chart(document.getElementById('value'), {
  type: 'bar',
  data: { labels, datasets: [{ label: 'Quality / $',
    data: D.strategies.map(s => s.quality_per_dollar), backgroundColor: PALETTE }] },
  options: { plugins: { legend: { display: false } } }
});

const cols = [['Strategy', s => s.label], ['Cost $', s => s.cost_usd.toFixed(4)],
  ['Total tokens', s => s.total_tokens.toLocaleString()], ['Turns', s => s.num_turns],
  ['Duration s', s => (s.duration_ms / 1000).toFixed(0)],
  ['Quality', s => s.quality.total], ['Q/$', s => s.quality_per_dollar.toFixed(1)]];
const t = document.getElementById('summary');
t.innerHTML = '<tr>' + cols.map(c => `<th>${c[0]}</th>`).join('') + '</tr>' +
  D.strategies.map(s => '<tr>' + cols.map(c => `<td>${c[1](s)}</td>`).join('') + '</tr>').join('');
</script>
</body>
</html>
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_report.py -q`
Expected: PASS (4 passed).

- [ ] **Step 6: Commit**

```bash
git add task07-claude-code-rfp-agent/rfp_eval/report.py task07-claude-code-rfp-agent/rfp_eval/templates task07-claude-code-rfp-agent/tests/test_report.py
git commit -m "feat(rfp-eval): report data model + charted HTML dashboard"
```

---

## Task 7: Async orchestrator + CLI

**Files:**
- Create: `task07-claude-code-rfp-agent/rfp_eval/orchestrator.py`
- Create: `task07-claude-code-rfp-agent/rfp_eval/__main__.py`
- Create: `task07-claude-code-rfp-agent/tests/test_orchestrator.py`

**Interfaces:**
- Consumes: `strategies.build_call`, `sdk_runner.run_query`, `metrics.extract_metrics`, `judge.read_artifacts`/`judge_quality`, `report.*`.
- Produces:
  - `async run_evaluation(*, task_dir, rfp_path, out_root, model=None, query_fn=None, judge_query_fn=None) -> Path` — runs the three strategies concurrently, writes per-run `run.json`, `eval/metrics.json`, `eval/quality.json`, `eval/index.html`; returns the `index.html` path.
  - `main(argv=None) -> int` (in `__main__.py`), argparse flags: `--rfp` (default `synthetic-data/rfp-acme-corp.md`), `--out` (default `outputs`), `--task-dir` (default `.`), `--model`.

- [ ] **Step 1: Write the failing test**

Create `task07-claude-code-rfp-agent/tests/test_orchestrator.py`:
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
 {"strategy":"dynamic","scores":{"completeness":4,"specificity":4,"actionability":5,"risk_depth":3,"correctness":4},"rationale":"good"}
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
    metrics = json.loads((tmp_path / "outputs" / "eval" / "metrics.json").read_text())
    quality = json.loads((tmp_path / "outputs" / "eval" / "quality.json").read_text())
    assert len(metrics) == 3 and len(quality) == 3
    assert (tmp_path / "outputs" / "runs" / "swarm" / "run.json").exists()
```

Note the contract this test pins: `run_evaluation`'s `query_fn` is a **factory** `(out_dir) -> async query fn`, so tests can vary behavior per run and real usage can pass a factory that ignores `out_dir` and returns the SDK `query`.

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_orchestrator.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'rfp_eval.orchestrator'`.

- [ ] **Step 3: Write minimal implementation**

Create `task07-claude-code-rfp-agent/rfp_eval/orchestrator.py`:
```python
"""End-to-end async flow: run strategies concurrently, judge, build report."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict
from pathlib import Path

from . import judge, report
from .metrics import extract_metrics, metrics_as_dict
from .sdk_runner import run_query
from .strategies import STRATEGY_KEYS, build_call


async def _run_one(key, *, task_dir, rfp_path, runs_root, model, query_factory):
    out_dir = Path(runs_root) / key
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt, options = build_call(
        key, task_dir=task_dir, rfp_path=rfp_path, out_dir=out_dir, model=model
    )
    query_fn = query_factory(out_dir) if query_factory else None
    result = await run_query(prompt, options=options, key=key, query_fn=query_fn)
    (out_dir / "run.json").write_text(json.dumps(result.raw, indent=2))
    return out_dir, result


async def run_evaluation(
    *,
    task_dir: str | Path,
    rfp_path: str | Path,
    out_root: str | Path,
    model: str | None = None,
    query_fn=None,          # factory: (out_dir) -> async query fn; None → real SDK
    judge_query_fn=None,    # async query fn for the judge; None → real SDK
) -> Path:
    task_dir = Path(task_dir)
    out_root = Path(out_root)
    runs_root = out_root / "runs"
    eval_root = out_root / "eval"
    eval_root.mkdir(parents=True, exist_ok=True)

    results = await asyncio.gather(
        *(
            _run_one(
                key,
                task_dir=task_dir,
                rfp_path=rfp_path,
                runs_root=runs_root,
                model=model,
                query_factory=query_fn,
            )
            for key in STRATEGY_KEYS
        )
    )

    metrics = [extract_metrics(r.key, r.raw) for _, r in results]
    (eval_root / "metrics.json").write_text(
        json.dumps([metrics_as_dict(m) for m in metrics], indent=2)
    )

    artifacts = {r.key: judge.read_artifacts(out_dir) for out_dir, r in results}
    scores = await judge.judge_quality(artifacts, model=model or "sonnet", query_fn=judge_query_fn)
    (eval_root / "quality.json").write_text(
        json.dumps([asdict(s) for s in scores], indent=2)
    )

    data = report.build_report_data(metrics, scores, rfp=str(rfp_path))
    html = report.render_report(data)
    return report.write_report(html, eval_root / "index.html")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest task07-claude-code-rfp-agent/tests/test_orchestrator.py -q`
Expected: PASS (1 passed).

- [ ] **Step 5: Create the CLI entry point**

Create `task07-claude-code-rfp-agent/rfp_eval/__main__.py`:
```python
"""CLI: uv run python -m rfp_eval [--rfp ...] [--out ...] [--model ...]"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from .orchestrator import run_evaluation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="rfp_eval",
        description="Run the RFP through single / swarm / dynamic strategies on the "
        "Claude Agent SDK and build a charted cost/quality report.",
    )
    parser.add_argument("--rfp", default="synthetic-data/rfp-acme-corp.md")
    parser.add_argument("--out", default="outputs")
    parser.add_argument("--task-dir", default=".")
    parser.add_argument("--model", default=None)
    args = parser.parse_args(argv)

    index = asyncio.run(
        run_evaluation(
            task_dir=args.task_dir,
            rfp_path=args.rfp,
            out_root=args.out,
            model=args.model,
        )
    )
    print(f"Report written to: {Path(index).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 6: Run the full suite**

Run: `uv run pytest -q`
Expected: PASS (all tests from Tasks 1–7, ~24 passed).

- [ ] **Step 7: Commit**

```bash
git add task07-claude-code-rfp-agent/rfp_eval/orchestrator.py task07-claude-code-rfp-agent/rfp_eval/__main__.py task07-claude-code-rfp-agent/tests/test_orchestrator.py
git commit -m "feat(rfp-eval): async orchestrator + CLI entry point"
```

---

## Task 8: Slash command + docs + live smoke test

**Files:**
- Create: `task07-claude-code-rfp-agent/.claude/commands/rfp-eval.md`
- Create: `task07-claude-code-rfp-agent/outputs/.gitignore`
- Create: `task07-claude-code-rfp-agent/rfp_eval/README.md`

**Interfaces:**
- Consumes: `uv run python -m rfp_eval` (from Task 7).
- Produces: `/rfp-eval` slash command.

- [ ] **Step 1: Create the slash command**

Create `task07-claude-code-rfp-agent/.claude/commands/rfp-eval.md`:
```markdown
---
description: Run the Acme RFP through single-agent, agent-swarm (Agent SDK), and dynamic-workflow strategies and build a charted cost/quality comparison report.
argument-hint: "[--model <name>]"
allowed-tools: Bash(uv run python -m rfp_eval:*), Read
---

Run the RFP Agent SDK evaluation, then summarize the result.

## Steps

1. From the `task07-claude-code-rfp-agent` directory, run the harness (pass any
   extra flags from `$ARGUMENTS`):

   ```bash
   uv run python -m rfp_eval --rfp synthetic-data/rfp-acme-corp.md --out outputs $ARGUMENTS
   ```

   This runs three Claude Agent SDK evaluations concurrently — single agent, the
   coordinator→specialists swarm (Task B), and a dynamic workflow — captures real
   cost + token usage from each run's `ResultMessage`, sends the outputs to an LLM
   judge, and writes `outputs/eval/index.html`.

2. Read `outputs/eval/metrics.json` and `outputs/eval/quality.json` and give the
   user a short markdown table comparing cost, total tokens, and quality total per
   strategy, plus which strategy won on quality and which on value (quality/$).

3. Tell the user the report path (`outputs/eval/index.html`) and offer to open it:
   `open outputs/eval/index.html`.

## Notes

- The three runs each take a few minutes and cost real tokens; they run unattended
  (`permission_mode="bypassPermissions"`, scoped to this project via `cwd`).
- Per-strategy artifacts land in `outputs/runs/<strategy>/`.
```

- [ ] **Step 2: Ignore generated output but keep the folder**

Create `task07-claude-code-rfp-agent/outputs/.gitignore`:
```gitignore
# Generated by /rfp-eval — keep the folder, ignore the artifacts.
runs/
eval/
*.docx
*.html
!.gitkeep
!.gitignore
```

- [ ] **Step 3: Document the harness**

Create `task07-claude-code-rfp-agent/rfp_eval/README.md`:
```markdown
# rfp_eval

One Claude Agent SDK project covering Task A (strategy comparison) and Task B
(the RFP swarm).

## Run

```bash
# from task07-claude-code-rfp-agent/
uv run python -m rfp_eval --rfp synthetic-data/rfp-acme-corp.md --out outputs
```

Or via the slash command: `/rfp-eval`.

## What it does

1. Runs `single`, `swarm`, `dynamic` strategies concurrently on `claude-agent-sdk`
   (`sdk_runner.py`, `orchestrator.py`). Each is one `query()` whose `ResultMessage`
   carries real `total_cost_usd` + `usage`.
2. **Task B swarm** (`swarm.py`): a coordinator query delegates to specialist
   `AgentDefinition` workers (pricing / legal / technical-fit / competitive /
   risk-assessment), each bound to a project skill, producing the proposal.docx +
   risk-assessment.html.
3. Extracts real cost/token metrics (`metrics.py`).
4. An LLM judge scores each strategy's outputs against a rubric (`judge.py`).
5. Renders `outputs/eval/index.html` with cost, token, quality-radar, and
   quality-per-dollar charts (`report.py`).

Project agents/skills/settings load via `setting_sources=["project"]` + `cwd`.

## Outputs

- `outputs/runs/<strategy>/` — proposal.docx, risk-assessment.html, run.json
- `outputs/eval/metrics.json`, `outputs/eval/quality.json`, `outputs/eval/index.html`

## Tests

```bash
uv run pytest
```
The suite never runs a real agent — every `query()` boundary is faked.
```

- [ ] **Step 4: Confirm the CLI wires up (no real agent run)**

Run: `uv run python -m rfp_eval --help`
Expected: argparse usage listing `--rfp`, `--out`, `--task-dir`, `--model`. (Imports the whole package — proves wiring — without running an agent.)

- [ ] **Step 5: Full test suite green**

Run: `uv run pytest -q`
Expected: PASS (all tests, ~24 passed).

- [ ] **Step 6: (Manual, optional) live smoke run**

> Spends real tokens and takes several minutes; do it once to validate end-to-end, then inspect the report.

Run (from `task07-claude-code-rfp-agent/`):
```bash
uv run python -m rfp_eval --rfp synthetic-data/rfp-acme-corp.md --out outputs
open outputs/eval/index.html
```
Expected: three run dirs under `outputs/runs/`, `outputs/eval/index.html` opens with four charts populated and a summary table. If a run errors, its `run.json` shows `is_error: true` and that strategy shows zeros — inspect that run dir.

- [ ] **Step 7: Commit**

```bash
git add task07-claude-code-rfp-agent/.claude/commands/rfp-eval.md task07-claude-code-rfp-agent/outputs/.gitignore task07-claude-code-rfp-agent/rfp_eval/README.md
git commit -m "feat(rfp-eval): /rfp-eval command + docs + output gitignore"
```

---

## Self-Review

**Spec coverage:**
- **Task B** ("Migrate RFP to Agent SDK & run as a Swarm Agent") → Task 4 `swarm.py`: coordinator system prompt + specialist `AgentDefinition` workers on `claude-agent-sdk`, producing proposal.docx + risk-assessment.html — the diagram's coordinator→workers→branded output. ✅
- **Task A** "command that spins up parallel evaluation" → Task 8 `/rfp-eval` + Task 7 orchestrator (`asyncio.gather` over three strategies). ✅
- "single agent, agent teams/swarm, dynamic workflows" → Tasks 1 + 4 (`single`, `swarm`, `dynamic`). ✅
- "aggregate results" → Task 7 (metrics.json, quality.json). ✅
- "compare output quality" → Task 5 LLM judge + rubric. ✅
- "compare costs" → Task 3 real cost/tokens from the SDK `ResultMessage` (the reason this is on the Agent SDK, not markdown). ✅
- "fancy index.html with charts" → Task 6 Chart.js dashboard. ✅
- index.md "look closer to Risk Assessment report" → judge reads `risk-assessment.html` first; rubric has a `risk_depth` dimension; swarm's risk worker writes the HTML. ✅

**Placeholder scan:** No TBD/TODO/"handle edge cases"/"similar to Task N". All code steps are complete.

**Type consistency:** `RunResult(key, result_text, raw)`, `RunMetrics` (10 fields), `QualityScore(strategy_key, scores, total, rationale)`, `RUBRIC_DIMS` (5) are used identically across sdk_runner→metrics→judge→report→orchestrator. `build_call` returns `(prompt, ClaudeAgentOptions)` for all three keys (swarm via `swarm.build_swarm_call`). `run_query`/`judge_quality` take a `query_fn`; `run_evaluation` takes a `query_fn` **factory** `(out_dir)->query_fn` plus a `judge_query_fn` — the orchestrator test pins that contract. `usage` token keys match the SDK (`input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`) and metrics reads exactly those. ✅

**Known constraints (not gaps):** (1) dynamic-workflow and agent-swarm are prompt/options-driven, not per-run CLI flags — documented in Global Constraints and kept data-driven. (2) `technical-fit` reuses the `competitive-intel` skill as reference material since the repo has no dedicated technical-fit skill — noted inline in `swarm.py`.
