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

When the orchestrator delegates to the first four specialists (and later to
Risk Assessment), it must get two independent settings right:

- CONCURRENCY comes from batching: issue all four `Agent` calls as separate
  tool-use blocks in the SAME message. The harness runs them at the same
  time regardless of `run_in_background`.
- RETURN PATH comes from foreground vs. background: omit `run_in_background`
  (or set it to `false`) on every specialist call. Never set
  `run_in_background: true`. Foreground means each specialist's result lands
  back directly in the orchestrator's own conversation once ready.
  Background detaches the call — the orchestrator's turn ends immediately,
  and since the orchestrator is itself a spawned subagent, the completion
  notification does not come back to it directly; it surfaces to whatever
  session invoked the orchestrator, which then has to relay it second-hand.
  That relay is exactly what stalls the workflow (a dropped or delayed
  relay leaves the orchestrator waiting on a specialist that already
  finished).

So: same message (parallel), foreground (direct result, no relay). The
orchestrator must not end its turn while a specialist call is still
pending.

Use `synthetic-data/past-wins.json` and `synthetic-data/product-overview.md` as
reference material where relevant.

Save both outputs under `outputs/runs/run-02-agent-teams/`.