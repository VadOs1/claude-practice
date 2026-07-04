---
description: Process the sample RFP as an agent team (coordinator + communicating specialist agents)
---

Process the RFP at `synthetic-data/rfp-acme-corp.md` for BTS-Synthetic.

Produce:
1. A customer-facing proposal response (.docx) covering: executive summary, our
   understanding of the customer's need, why we're the right fit, commercial
   proposal, contract approach, and risks/mitigations.
2. An internal risk assessment (.html) — a self-contained interactive risk vs.
   revenue dashboard, for internal use only.

I need to process this RFP as an agent team: spin up `deal-desk-orchestrator` as
the coordinator, which distributes tasks to the specialist agents — Pricing,
Legal, Technical Fit, Competitive Intel, and Risk Assessment. Agents should be
able to communicate with each other (e.g. the coordinator following up with a
specialist) rather than each one just returning a single one-shot answer.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

Save both outputs under `outputs/run-3-agent-teams/`.

After the deal is complete, have the orchestrator persist memory (per its
agent definition's memory-saving step) and remind each specialist it
consulted to save their own memory too.
