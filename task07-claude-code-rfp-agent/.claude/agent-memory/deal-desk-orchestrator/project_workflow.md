---
name: project-workflow
description: How RFP runs are structured in this repo (outputs/runs/run-NN-*, specialist roster, no branded docx template)
metadata:
  type: project
---

Runs are organized under `outputs/runs/run-NN-<label>/` (e.g. `run-01-baseline`, `run-02-agent-teams`), each a self-contained set of deliverables for one RFP pass. Don't dump directly into `outputs/` — check for a run-specific subdirectory the requester names.

**Why:** The repo is used to compare different orchestration approaches (baseline single-agent vs. multi-agent teams) side by side, so each run's outputs must stay isolated and reproducible under its own folder.

**How to apply:** When asked to "process an RFP," confirm/create the exact output path requested (e.g. `outputs/runs/run-02-agent-teams/`) rather than defaulting to `outputs/`.

Specialist agent types available via the Agent tool in this repo: `pricing`, `legal`, `technical_fit`, `competitive`, `risk_assessment`. Each has its own skill/playbook (pricing-playbook, legal-checklist, competitive-intel, risk-assessment skills under `.claude/skills/`) and reads `synthetic-data/past-wins.json` + `synthetic-data/product-overview.md` itself when briefed — the orchestrator should read the RFP and reference docs to brief them well, but must delegate the actual domain analysis rather than doing it itself.

No BTS-branded docx reference template exists in `templates/` as of 2026-07 (only `report.html.tmpl` for HTML reports, and a `docx` skill that does a plain pandoc markdown-to-docx conversion with no `--reference-doc`). Use the plain `docx` skill conversion unless a branded template shows up later — check `templates/` and `.claude/skills/docx/SKILL.md` before assuming one exists.

Related: [[specialist-conflict-handling]]
