---
description: Process the sample RFP via the deal-desk-orchestrator, forcing it to delegate to its specialist subagents
---

Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

Produce:
1. A customer-facing proposal response (.docx) covering: executive summary, our
   understanding of the customer's need, why we're the right fit, commercial
   proposal, contract approach, and risks/mitigations.
2. An internal risk assessment (.html) — a self-contained interactive risk vs.
   revenue dashboard, for internal use only.

Use the `deal-desk-orchestrator` agent to run this deal. This requires spinning
up an agent team: the orchestrator acts as coordinator and distributes tasks,
the specialist agents (Pricing Specialist, Legal Reviewer, Technical Fit
Specialist, Competitive Intel Analyst, Risk Assessment Specialist) pick up
their assigned work and proceed independently, and agents can communicate with
each other as needed. The orchestrator must NOT perform the pricing, legal,
technical-fit, competitive, or risk-assessment analysis itself — it must
delegate each of those to its specialist subagents and synthesize their
responses.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

Save both outputs under `outputs/run-3-agent-teams/`.
