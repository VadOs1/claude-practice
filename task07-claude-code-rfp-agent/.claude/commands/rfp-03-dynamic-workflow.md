---
description: Process the ACME Corp RFP using Dynamic Workflow orchestration
---

Use a workflow to process the RFP at `synthetic-data/rfp-acme-corp.md`.

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

Save all outputs under `outputs/runs/run-03-dynamic-workflow/`, producing
exactly these three files (`<customer>` and `<date>` reflect the customer
name and today's date):

- `outputs/runs/run-03-dynamic-workflow/proposal-<customer>-<date>.docx`
- `outputs/runs/run-03-dynamic-workflow/proposal-<customer>-<date>.md`
- `outputs/runs/run-03-dynamic-workflow/risk-assessment-<customer>-<date>.html`

Use ultracode.