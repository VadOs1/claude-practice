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
