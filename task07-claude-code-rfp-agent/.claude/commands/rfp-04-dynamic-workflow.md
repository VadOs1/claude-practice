---
description: Process the sample RFP using a Dynamic Workflow strategy
---

Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

Produce:
1. A customer-facing proposal response (.docx) covering: executive summary, our
   understanding of the customer's need, why we're the right fit, commercial
   proposal, contract approach, and risks/mitigations.
2. An internal risk assessment (.html) — a self-contained interactive risk vs.
   revenue dashboard, for internal use only.

Run this using a Dynamic Workflow: use the `deal-desk-orchestrator` agent and
let it dynamically plan and adjust which specialist agents (Pricing, Legal,
Technical Fit, Competitive Intel, Risk Assessment) to invoke, in what order,
based on what it discovers in the RFP — rather than a fixed, predetermined
delegation sequence.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

Save both outputs under `outputs/run-4-dynamic-workflow/`.
