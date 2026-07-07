# BTS-Synthetic — Proposal for Acme Corp Enterprise Data Platform

**Prepared for:** Sarah Chen, VP Procurement / Marcus Webb, Chief Data Officer, Acme Corp
**Prepared by:** BTS-Synthetic
**Date:** 2026-07-06
**In response to:** RFP issued 2026-05-12, response due 2026-05-26

---

## Executive Summary

- **Strong technical fit.** BTS-Synthetic's lakehouse platform meets or exceeds every functional requirement in this RFP — real-time ingest at 3x your peak load, native Power BI DirectQuery (our most mature BI integration), EU data residency, and open-format (Delta/Iceberg/Parquet) portability — with one item, uptime SLA, that we address head-on below rather than over-promise.
- **Proven in your exact segment.** We closed a near-identical industrial IoT deployment (Initech Sensors, Nov 2025) against the same competitive field you're running — Microsoft Fabric, Databricks, Snowflake — and won on real-time ingest performance and governance maturity, not on being the cheapest bid.
- **Commercial terms grounded in real deal data, not list-price theater.** We propose a discount, payment, and pricing-structure package calibrated against comparable enterprise wins, and we flag transparently where a small number of your contractual asks (uncapped liability, unannounced audits, full IP vesting, zero-tolerance SLA termination) need a negotiated middle ground before signature — with precedent for how we've resolved each one before.

---

## Our Understanding of Your Need

Acme Corp is consolidating a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics into a single enterprise data platform, ahead of full Teradata decommissioning in 2027. The platform must simultaneously serve:

- Real-time ingest from ~40,000 IoT devices in the field, peaking at 80,000 events/second
- Batch ETL from 30+ internal sources
- BI and reporting for ~600 analysts and executives, standardized on Power BI
- Self-service data preparation for ~150 data engineers
- Future machine learning pipelines for predictive maintenance

All of this at ~280TB current scale, growing ~12TB/month, deployed across a primary EU region and secondary US East region, with EU customer data required to stay in the EU. You are a Microsoft/Azure shop evaluating us alongside Databricks, Snowflake, Microsoft Fabric, and one regional vendor — and you're running a disciplined, TCO-weighted evaluation (functional fit 30%, commercial 25%, TCO 20%, implementation 15%, vendor stability 10%).

We read this as a decision that will ultimately turn on two questions: *can this vendor actually handle our real-time ingest and governance requirements at production scale*, and *can we get commercial terms that don't lock us into open-ended risk for five years*. Our proposal is built to answer both directly.

---

## Why BTS-Synthetic Is the Right Fit

**Technical fit: high, with one item addressed transparently.** Our platform's real-time streaming layer is tested to 250,000 events/second on single-region deployments — more than 3x your 80,000 events/second peak — well within headroom for growth. Batch ETL is covered by 80+ out-of-the-box connectors against your 30+ sources. Power BI is our most mature BI integration, built on a dedicated DirectQuery adapter — this directly satisfies your non-negotiable requirement for your 600 analysts and executives. Self-service prep for your 150 data engineers is covered by our low-code UI. Lakehouse architecture with native Delta, Iceberg, and Parquet support matches your stated architectural preference exactly, and per-table residency pinning lets us guarantee EU data stays in the EU while serving US East as a secondary region. Your planned predictive-maintenance ML workloads are covered today by our model registry, feature store, and native model serving — no rush risk when you're ready to activate them. The one area requiring an honest conversation: our standard Enterprise SLA is 99.95% monthly uptime; 99.99% is available as a bespoke, multi-region active-active add-on. We address the commercial and contractual shape of this in the Risks section below rather than commit to terms we can't stand behind.

**Competitive position: we've won this exact matchup before.** Your Microsoft/Azure footprint makes Microsoft Fabric the most natural incumbent threat, and we expect Fabric to be positioned as "free" or low-cost via your existing E5 licensing. We've seen this play out already: in a near-identical industrial IoT deal (Initech Sensors, closed November 2025), Fabric offered exactly this bundled pricing and lost — because it could not match our real-time ingest SLA or governance maturity at production scale. We expect that pattern to repeat here. Databricks and Snowflake are credible on parts of this deal (Databricks on ML/streaming, Snowflake on SQL), but neither has a native, DirectQuery-grade Power BI integration or our depth of governance tooling (audit-log export, attribute-based access control, PII detection) — both of which matter directly for the audit and compliance posture your contractual requirements demand. We recommend leading with proven real-time performance and governance maturity, backed by reference customers in your exact segment, rather than competing purely on headline discount.

---

## Commercial Proposal

We are proposing a structure calibrated against comparable enterprise wins, not generic list pricing:

- **Discount:** Your RFP specifies a 35% floor off list. Our standard strategic ceiling tops out at 30%, and our closest comparable deal in your segment (Initech Sensors — same industry, similar scale) settled at 15% off an initial 25% ask, winning on real-time performance and governance rather than price. We are prepared to bring a **28-30% discount** to the table, contingent on a 3-year minimum committed term and a signed reference-customer agreement — the strongest offer we can responsibly stand behind without compromising the service levels you actually need. We will not chase the 35% floor with a race-to-the-bottom discount; our own data shows that path leads to under-resourced implementations and margin that can't support your uptime and governance requirements.
- **Term and pricing structure:** We propose pricing fixed for the initial 3-year term, with a pre-agreed volume true-up mechanism (a defined buffer covering your ~12TB/month growth trajectory) rather than an annual escalator — this gives you cost predictability without us silently absorbing five years of unbounded data growth. Full repricing terms for the 2-year renewal option are set at signature, addressing your 5-year horizon requirement, with the true-up as the only variable component.
- **Payment terms:** We propose annual-in-advance billing at **Net 60**, reflecting your credit profile and scale, rather than the requested Net 90. Quarterly billing is available at no price change if that better suits your treasury preferences.
- **Most Favoured Nation clause:** We cannot warrant MFN pricing for the reasons any enterprise vendor cannot — our discount methodology varies by deal shape, term, and volume commitment across our full customer base, and an MFN warranty is commercially unworkable to police or guarantee. In its place, we will provide full transparency into our published discount-band methodology so you can independently verify you're receiving a top-tier enterprise rate.
- **Proactive concessions:** PoC-fee credit toward Year 1 fees, a custom MSA appropriate to a deal of this size, and 30-day acceptance testing — all available now, not held back as negotiation chips.

---

## Contract Approach

Several of your Section 4 requirements are more aggressive than our standard paper, and we want to be direct about where we need a negotiated middle ground rather than silently accepting terms we can't operationally support:

| Clause | Your ask | Our position |
| --- | --- | --- |
| **Liability (4.1)** | Uncapped breach liability, full indemnification incl. regulatory fines and reputational damages | Cap aggregate liability at 24 months' fees, with carve-outs for gross negligence and IP infringement; exclude reputational damages and third-party regulatory fines from indemnity scope |
| **Audit (4.2)** | Unannounced audits, up to 4x/year, vendor bears all costs | One audit/year with 30 days' notice and confidentiality protections; customer bears cost of any additional audits requested beyond the first |
| **SLA (4.3)** | 99.99% uptime; any SLA miss of any duration triggers immediate termination + full monthly refund | 99.95% standard SLA (99.99% available as a paid, multi-region active-active add-on if required); service credits up to 30% of monthly fees as the primary remedy; termination right reserved for chronic breach (3+ misses in 6 months) with a cure period |
| **IP (4.4)** | All custom work product vests in Acme upon creation | We retain underlying platform IP with a full license-back of derivative works to Acme — the same structure we agreed with Stark Industries (a comparable enterprise deal) after they raised an identical request |
| **Subprocessors (4.5)** | Prior written consent for any subprocessor, withholdable at Acme's sole discretion | Published subprocessor list with 30 days' advance notice of changes and a right to object, with substitution or a limited termination right if unresolved |
| **Termination for convenience (3.5)** | 30 days' notice, no fee, terminable at any time | Workable as proposed; we'd prefer 60-90 days but will not hold this point given no early-termination fee is being requested of either side |

None of these are dealbreakers on our side — each has direct precedent for how we've resolved it with comparable enterprise customers — but they need to be worked through before signature rather than assumed away.

---

## Risks and How We Mitigate Them

1. **SLA / termination mismatch (highest priority).** Your Section 4.3 pairs an aggressive uptime target with a zero-tolerance termination trigger. Committing to 99.99% under an "any miss, any duration" termination clause is a risk neither side benefits from — a single transient blip could void the contract. Mitigation: 99.95% standard SLA with service credits as the primary remedy, chronic-breach termination threshold, and 99.99% available as a scoped, priced add-on if your operational requirements truly demand it after we've validated actual performance in a pilot.
2. **Discount gap (35% floor vs. our 28-30% ceiling).** We are not the cheapest bid, and Databricks/Snowflake will likely bid lower. Mitigation: win on 3-year TCO, not sticker price — our real-time performance headroom (250K vs. your 80K events/sec) and native Power BI integration reduce downstream integration and re-platforming costs that a lower headline discount elsewhere won't.
3. **MFN and 5-year fixed pricing.** Both introduce open-ended commercial exposure on our side over a 5-year horizon with 12TB/month uncontrolled growth. Mitigation: discount-methodology transparency in place of an MFN warranty; a defined volume true-up mechanism in place of an escalator, agreed at signature so there are no surprises later.
4. **Contractual liability, audit, and IP terms (Section 4).** As detailed above, uncapped liability, unannounced 4x/year audits, and full IP vesting are outside our standard paper. Mitigation: negotiated positions above, each with direct precedent from comparable enterprise deals (notably Stark Industries on IP), to be resolved during contracting rather than left ambiguous.
5. **Implementation timeline risk.** A deployment at your scale (280TB, multi-region, multi-source) typically takes us up to 24 weeks for full migration. Mitigation: we'll propose a phased plan — first production workload within 8 weeks, full Teradata migration completed well ahead of your 2027 decommissioning deadline — with milestones defined jointly during onboarding.

We're ready to move quickly to finalize these terms and support your evaluation timeline.
