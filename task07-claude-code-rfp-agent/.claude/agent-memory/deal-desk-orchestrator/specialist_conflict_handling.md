---
name: specialist-conflict-handling
description: How to handle it when two specialists' recommendations conflict on the same customer-facing point (e.g. SLA commitment)
metadata:
  type: feedback
---

When two specialists give conflicting guidance on the same customer-facing point, resolve it in the synthesis by favoring the more conservative/authoritative domain expert for that specific fact, rather than sending a follow-up round-trip for every minor conflict.

Example encountered: on the Acme Corp RFP, the Competitive Intel Analyst suggested leading with a 99.99% SLA commitment as a differentiator ("competitors will hedge this commitment; we commit it"), while Technical Fit and Legal both flagged 99.99% as a gap/blocker versus our 99.95% standard SLA. Rather than looping back to Competitive Intel, the synthesis kept the "real-time ingest performance + governance maturity" positioning angle (which all specialists agreed on) but dropped the specific 99.99% commitment, framing the SLA instead per Legal's countered position (99.95% + service credits).

**Why:** A follow-up round-trip for every cross-specialist inconsistency slows down a time-boxed deal-desk workflow; the RFP deadline is real. Legal and Technical Fit are the authoritative sources on contractual/capability facts (what we can actually promise), so their view should win over a positioning suggestion from Competitive Intel when they conflict on a specific commitment.

**How to apply:** Only send a specialist a follow-up when the conflict is large enough to change the deal's viability or a core commercial/legal position (per the orchestrator instructions: "only if it matters"). Cosmetic or framing-level conflicts (like which SLA number to headline) can be resolved directly in synthesis by deferring to the more conservative/authoritative specialist.
