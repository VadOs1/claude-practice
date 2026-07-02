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
