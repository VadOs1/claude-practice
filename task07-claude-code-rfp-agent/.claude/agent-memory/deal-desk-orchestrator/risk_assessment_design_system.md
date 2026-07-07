---
name: risk-assessment-design-system
description: The design-system URL the orchestrator instructions pass to the risk_assessment specialist returns HTTP 404 as of 2026-07
metadata:
  type: project
---

The risk_assessment specialist was briefed to build the internal HTML dashboard using the design system at `https://api.anthropic.com/v1/design/h/eD-iXOaROKnOHg6r-Ffl4w?open_file=index.html`. As of the 2026-07-06 Acme Corp run, that URL returned HTTP 404. The specialist fell back to the color palette/layout spec already defined in its own `risk-assessment` skill (`.claude/skills/risk-assessment/SKILL.md`) and produced a solid dashboard anyway.

**Why:** The task instructions hard-code this design-system URL, but it isn't reachable — worth knowing so it isn't mistaken for a specialist error in future runs.

**How to apply:** Don't flag it as a defect when the risk_assessment specialist reports a 404 on that URL and falls back to its own skill's design spec — that's the expected degraded path, not a mistake. If it matters later, worth checking whether a working design-system URL should be substituted in the task brief.

Related: [[project-workflow]]
