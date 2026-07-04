---
description: Process the sample RFP via the deal-desk-orchestrator using an agent team
---

Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

Produce:
1. A customer-facing proposal response (.docx) covering: executive summary, our
   understanding of the customer's need, why we're the right fit, commercial
   proposal, contract approach, and risks/mitigations.
2. An internal risk assessment (.html) — a self-contained interactive risk vs.
   revenue dashboard, for internal use only.

Use the `deal-desk-orchestrator` agent to run this deal via agent team. The
orchestrator spawns five specialist teammates (Pricing Specialist, Legal
Reviewer, Technical Fit Specialist, Competitive Intel Analyst, Risk Assessment
Specialist), assigns each their scope, and synthesizes their findings. The
orchestrator must NOT perform the pricing, legal, technical-fit, competitive,
or risk-assessment analysis itself — delegate each to its specialist and
integrate their responses into the proposal and dashboard.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

Save both outputs under `outputs/run-2-agent-teams/`.