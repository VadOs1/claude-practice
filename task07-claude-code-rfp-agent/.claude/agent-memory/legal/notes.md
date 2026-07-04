# Legal Reviewer — carryforward notes

## Patterns worth remembering (not deal-specific numbers)

- **"Vendor bears all audit costs" + unannounced audits** tend to arrive
  bundled in industrial/manufacturing RFPs alongside uncapped liability.
  Flag the no-notice provision as the blocker driver even when frequency
  and cost-allocation are independently negotiable — don't let the
  negotiable sub-issues dilute the blocker severity of the combined clause.

- **SLA + termination-on-any-failure clauses**: treat as two separate
  issues that get conflated in RFP drafting. The uptime number (99.99%)
  is usually just aspirational language procurement copies from a
  template — it's negotiable. The "any failure, any duration → immediate
  termination + full refund" trigger is the actual blocker (removes our
  cure-period standard entirely). Always split these in the flag so
  Pricing/Orchestrator don't over-index on the number.

- **IP assignment demands**: the Stark Industries precedent (license-back
  of derivative works instead of full assignment) is our strongest
  fallback script and has now worked on a $1.1M/5-year defence/aerospace
  deal — cite it confidently even for industrial/IoT customers (Acme is
  same profile as Initech Sensors, not Stark, but the IP counter-position
  is industry-agnostic).

- **MFN pricing warranties (not in the SKILL.md checklist)**: these show
  up in procurement-led RFPs from large industrials (Acme, ~$1.4B rev).
  They're a legal/operational risk item even when pricing itself is
  Pricing's call, because an undefined "comparable customer" warranty
  creates perpetual audit exposure and a ratchet risk against future
  competitive discounting (e.g. deals like Pied Piper where we walked
  away rather than match a competitor's 40% discount). Recommend: narrow
  scope to same industry/tier/volume band, annual (not continuous)
  attestation, and exclude one-off/promotional pricing. Consider
  proposing this addition to SKILL.md so it's not an ad-hoc call each time.

- **Sequencing**: liability, audit, SLA-termination, IP, and subprocessor
  consent clauses in section 4 usually travel together in industrial
  procurement RFPs as a single "risk-transfer" package. Worth flagging to
  the orchestrator as a package (all-or-nothing negotiation posture is
  common on the customer side) rather than five independent asks.

## Open item for skill maintainers
Suggest adding an explicit MFN entry to `.claude/skills/legal-checklist/SKILL.md`
(section 3.4-style clauses recur and currently require ad-hoc judgment).
