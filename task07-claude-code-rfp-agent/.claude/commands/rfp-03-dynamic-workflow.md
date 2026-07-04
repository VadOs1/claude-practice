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

Save outputs to `runs/run-3-dynamic-workflow/`.

Use ultracode.