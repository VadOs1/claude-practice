---
description: Process the sample RFP with no subagent strategy specified (baseline — Claude likely works single-agent + skills)
---

Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

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

Save all outputs under `outputs/runs/run-01-baseline/`, producing exactly
these three files (`<customer>` and `<date>` reflect the customer name and
today's date):

- `outputs/runs/run-01-baseline/proposal-<customer>-<date>.docx`
- `outputs/runs/run-01-baseline/proposal-<customer>-<date>.md`
- `outputs/runs/run-01-baseline/risk-assessment-<customer>-<date>.html`
