---
name: tooling-notes
description: SendMessage tool is not enabled in this environment; use the Agent tool with the same name to follow up with a previously spawned specialist
metadata:
  type: project
---

The instructions reference a `SendMessage` tool (`to: <agentId or name>`) for
resuming a named background agent. In this environment that tool is **not
enabled** — calling it returns "No such tool available: SendMessage."

**Working approach:** call the `Agent` tool again with the same `name` used
for the original spawn (e.g. `pricing-acme`, `legal-acme`) and a
`subagent_type` matching the original. This produces a *new* agentId each
time (confirmed via the tool's own response), so it is not a true stateful
resume — it behaves like a fresh agent under the same name. Because of this:

- Always write the follow-up prompt as fully self-contained (restate the
  other specialist's finding you want reacted to, don't assume the agent
  remembers its own first answer).
- Do not rely on implicit shared context between the first call and the
  follow-up call just because the `name` matches.

**Why this matters:** if a future run has SendMessage enabled, this workaround
is unnecessary — check tool availability first before assuming the
self-contained-prompt workaround is required.
