---
name: cross-examination-patterns
description: When a follow-up between two specialists is worth the extra round-trip vs. accepting first replies as-is
metadata:
  type: feedback
---

Genuine cross-examination is worth it when two specialists' *initial* outputs
touch the same clause/number from different angles and could silently ship
inconsistent guidance if left unreconciled — not just whenever two specialists
mention the same topic.

Two real patterns from the Acme run (recurring RFP, industrial IoT profile):

1. **Severity/position conflict on the same clause (MFN).** Legal rated the
   MFN warranty "negotiable" with a narrowed-scope counter; Pricing's own
   playbook rates MFN a hard no / walk-away item. Both are legitimate legal
   *and* commercial reads, but only one can go in the proposal. Follow up
   with whichever specialist owns the clause's primary domain (here:
   Pricing owns commercial-term severity even though Legal drafts the
   counter-language) and ask them to pick a lead position, not to average
   the two. See [[mfn-ownership-precedent]].

2. **A cost/architecture fact one specialist surfaces that another's math
   doesn't yet reflect (SLA add-on premium).** Technical Fit's 99.99% ->
   custom add-on / $80-120K premium finding came back concurrently with
   Pricing's discount recommendation, which had no mechanism for it.
   Rather than assume Pricing would "of course" account for it, sent a
   direct follow-up asking whether the premium compresses the discount
   ceiling or sits as a separate line. This produced a materially better
   answer (two explicit commercial tracks, premium kept non-discounted)
   that would NOT have emerged from the first-pass replies alone.

**How to apply next time:** after collecting the first four replies, scan for
(a) the same clause/number getting different severity/verdicts from two
specialists, or (b) a quantitative fact one specialist introduces that a
peer's recommendation predates and doesn't visibly account for. Those two
conditions are the actual signal for a follow-up — not "these two mentioned
the same word." If neither condition is present for a given tension point
(e.g. this run's SLA-number-vs-termination-trigger split was already
internally consistent between Legal and Technical Fit — both wanted a
cure-period fix, no real disagreement), don't manufacture a follow-up just to
prove the process ran. Fabricated disagreement wastes a round-trip and
muddies the synthesis.
