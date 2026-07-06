# Proposal Response — Acme Corp Enterprise Data Platform

**Prepared for:** Sarah Chen, VP Procurement / Marcus Webb, Chief Data Officer, Acme Corp
**Prepared by:** BTS-Synthetic
**Date:** 2026-07-06
**In response to:** RFP issued 2026-05-12

---

## Executive Summary

- **Strong functional fit, Azure-native delivery.** BTS-Synthetic's lakehouse platform meets Acme's core requirements out of the box — native Power BI with our most mature BI integration (dedicated DirectQuery adapter), open formats (Delta/Iceberg/Parquet), multi-region EU/US deployment with per-table EU data residency, and headroom on real-time ingest (tested to 250K events/sec against your peak of 80,000/sec, single-region validated; we will load-test the multi-region topology during onboarding).
- **Commercially disciplined, TCO-led offer.** We propose a 25–28% discount off list, anchored to 3-year TCO rather than headline discount — the same approach that won us Globex Manufacturing (18% discount, beat Snowflake) and Initech Sensors (15% discount, beat Microsoft Fabric on real-time SLA), both comparable industrial/IoT accounts.
- **Contract terms that protect both sides.** Several of Acme's standard contractual asks (uncapped liability, no-notice audits, absolute IP vesting, unilateral subprocessor veto, a zero-tolerance 99.99% SLA with immediate termination) sit outside any deal we or our insurers can stand behind. We've proposed workable, precedented alternatives below — the same structure that got Stark Industries (Defence/Aerospace, $1.1M/year) across the line.

## Our Understanding of Your Need

Acme is replacing a legacy Teradata-based, on-premises warehouse patchwork with a modern lakehouse to support real-time ingest from ~40,000 IoT devices (peak 80,000 events/sec), batch ETL from 30+ sources, BI/reporting for ~600 analysts on Power BI, self-service prep for ~150 data engineers, and a near-term roadmap into predictive-maintenance ML. You are Azure-first, need EU data residency with a US East secondary region, and are running a competitive process against Databricks, Snowflake, Microsoft Fabric, and a regional vendor, with an award decision targeted for 2026-06-30. Commercial terms matter as much as capability here (25% weight) — you're seeking a 5-year fixed-price horizon, ≥35% discount, Net 90 payment, and an aggressive contractual risk allocation (uncapped liability, unrestricted audit rights, full IP assignment, 99.99% uptime).

## Why We're the Right Fit

**Technical fit: Medium-High, with one flagged risk.** Our Technical Fit assessment confirms full coverage of your core workloads: batch ETL (80+ connectors comfortably covers your 30+ sources), Power BI (our strongest BI integration), lakehouse architecture with native Delta/Iceberg/Parquet, multi-region deployment with per-table EU residency pinning, and the model registry/feature store/serving stack needed for your planned predictive-maintenance pipelines. Peak ingest of 80,000 events/sec is well inside our tested single-region ceiling of 250K events/sec; we will validate sustained throughput across your dual-region (EU primary/US secondary) topology during solution design. Self-service prep for your 150 data engineers may need light supplementary tooling since our low-code prep UI is analyst-oriented — we'll scope this in discovery at no extra commercial impact. The one genuine gap: your 99.99% uptime ask exceeds our standard 99.95% Enterprise SLA; see Risks section below for how we address it. Realistic implementation timeline given active Teradata decommissioning and dual-region, multi-source scope is **16–24 weeks** to full migration (not the 8-week best case, which applies to single-region, clean-source deployments).

**Competitive position: strong, if we lead with the right story.** You're evaluating Microsoft Fabric, Databricks, Snowflake, and a regional vendor. Fabric is the most credible competitor given your Azure/Power BI footprint and E5 bundling economics — but we beat Fabric at Initech Sensors, a comparable industrial IoT account, specifically on real-time ingest performance and governance maturity, and Fabric will struggle to responsibly commit to your SLA terms. Databricks' multi-cloud pitch is largely wasted on an Azure-committed customer, and we out-competed them on 3-year TCO at Globex Manufacturing using the customer's actual workload profile — we'll run the same analysis for Acme. Snowflake's real-time ingest is a known weak spot and we've beaten them twice on TCO and PoC outcomes (Globex, Wayne Manufacturing). Our recommended wedge: real-time ingest performance + governance maturity, backed by a rigorous 5-year TCO model built on your actual 280TB/12TB-per-month growth profile — not a discount race.

## Commercial Proposal

- **Discount:** We propose **25–28% off published list price** (hard ceiling 30% with executive sign-off), reflecting deal scale (>$1M/year likely at this footprint) and a 3-year committed term. This is above every comparable industrial win in our portfolio (Initech Sensors 15%, Globex 18%, Stark Industries 28%) — we are stretching to be competitive, but 35% is below any margin floor we can sustain and still deliver the SLA and residency architecture this deal requires. We will win this on total cost of ownership across the 5-year horizon, not on headline discount, using the same analysis that won Globex and Stark.
- **Payment terms:** We counter Net 90 with **Net 60, annual in advance** — precedented at Initech Sensors and appropriate given Acme's investment-grade financial profile.
- **Term structure:** We accept the 3-year initial term. On the 5-year price lock: we will fix Years 1–3 firmly at signature, and propose the Year 4–5 renewal be re-priced with a capped escalator (CPI+2%, maximum 5% per year) rather than an open-ended blanket lock — this protects both parties against multi-year cost/inflation risk while still giving you full pricing visibility at signature.
- **Concessions we're prepared to make:** PoC-fee credit-roll into Year 1 (Wayne Manufacturing precedent), 30-day acceptance testing window, volume true-up mechanism rather than rigid tiering.

## Contract Approach

Our legal review flagged several clauses in Sections 3–4 that we cannot accept as drafted, alongside proposed counter-positions we believe will land:

| Clause | Acme's Ask | Severity | Our Counter |
| --- | --- | --- | --- |
| 4.1 Liability | Uncapped, full indemnification incl. reputational damages | Blocker | Cap aggregate liability at 24 months' fees; mutual carve-outs for gross negligence/IP infringement; indemnify direct costs, not unquantifiable reputational damages |
| 4.2 Audit | Unlimited-notice, 4x/year, vendor-funded | Blocker | 1 audit/year, 30 days' notice, customer bears cost beyond the first; no direct subprocessor audits |
| 4.3 SLA | 99.99% uptime; any breach triggers immediate termination + full refund | Blocker | 99.95% uptime (our Enterprise standard) with service credits (up to 30% of monthly fees) as sole remedy; termination only after chronic/repeated failures with a cure period |
| 4.4 IP | Full work-product vesting in Acme | Blocker | BTS retains IP; Acme receives a perpetual license to all custom deliverables and derivative works — the structure Stark Industries accepted |
| 4.5 Subprocessors | Prior consent at Acme's sole discretion | Blocker | 30 days' advance notice with objection right and substitution option, not an absolute veto |
| 3.5 Termination for convenience | 30 days, no fee, unilateral | Negotiable | Extend to 60–90 days, ideally made mutual |
| 3.4 MFN | Unbounded "no less favourable than any comparable customer" | Negotiable | Narrow to similarly-sized customers in the same industry/region, time-boxed |

Sections 3.1 (term), 3.2 (payment structure), EU residency terms, and standard confidentiality provisions are acceptable as drafted or addressed commercially above.

## Risks and How We Mitigate Them

- **SLA mismatch (highest priority):** Your 99.99% ask exceeds our 99.95% Enterprise standard; a bespoke multi-region active-active architecture can close most of the gap but carries a premium and no guarantee of 100% attainment. Combined with a zero-tolerance termination clause, an ordinary transient blip could otherwise void the contract. Mitigation: we commit to 99.95% with meaningful service credits as the sole remedy, and will scope the active-active add-on during solution design if Acme wants to pursue incremental uptime beyond that baseline.
- **Multi-region throughput at scale:** 80,000 events/sec peak ingest is comfortably within our tested 250K/sec ceiling, but that ceiling is proven single-region; we haven't yet load-tested sustained throughput across an active EU+US topology. Mitigation: joint load-testing in solution design before go-live sign-off, with contingency built into the implementation plan.
- **Aggressive contractual risk allocation:** Uncapped liability, unrestricted audits, full IP vesting, and subprocessor veto rights are outside standard and insurable terms. Mitigation: precedented counter-positions above (Stark Industries model for IP; capped liability/audit structure), negotiated collaboratively rather than as take-it-or-leave-it.
- **Price pressure from a four-way competitive process:** Databricks and Snowflake may discount aggressively to win; Fabric has a structural Azure/Power BI advantage. Mitigation: compete on 5-year TCO and real-time ingest/governance maturity — the exact combination that beat Fabric at Initech Sensors and Databricks/Snowflake at Globex — rather than chasing the 35% discount floor, which we believe is unsustainable for any vendor able to deliver this architecture at the required residency and reliability bar.
- **Implementation timeline risk:** Active Teradata decommissioning plus dual-region, multi-source scope points to a realistic 16–24 week migration, not the 8-week best case. Mitigation: phased migration plan with clear milestones (detailed in the full technical proposal), sequencing lower-risk sources first and validating throughput/residency architecture before cutover of core BI workloads.

---

*This document synthesizes input from BTS-Synthetic's Pricing, Legal, Technical Fit, and Competitive Intelligence teams. Full technical proposal, implementation plan, and reference customers to follow as separate attachments per the RFP response format.*
