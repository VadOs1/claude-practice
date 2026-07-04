# Proposal to Acme Corp: Enterprise Data Platform

**Prepared for:** Sarah Chen, VP Procurement / Marcus Webb, Chief Data Officer, Acme Corp
**Prepared by:** BTS-Synthetic
**Date:** 2026-05-26
**In response to:** RFP — Enterprise Data Platform, issued 2026-05-12

---

## 1. Executive Summary

Acme Corp is replacing a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics with a single enterprise data platform capable of ingesting 80,000 events/second from 40,000 IoT devices, serving 600 BI users on Power BI, and supporting 150 data engineers today — with predictive-maintenance ML on the roadmap.

BTS-Synthetic proposes our **Enterprise-tier Lakehouse platform**, deployed multi-region (EU primary, US East secondary) on Azure, with native Power BI DirectQuery integration, per-table EU data residency enforcement, and open Delta/Iceberg/Parquet formats so Acme is never locked into a single vendor's file format.

We are a strong functional fit for every workload in Section 2 of the RFP. Our one area requiring a joint architecture decision is the 99.99% uptime target (Section 4.3) — our standard Enterprise SLA is 99.95%; 99.99% is available as an active-active multi-region add-on, which aligns naturally with Acme's own multi-region requirement.

On commercial terms, we want to be direct: several of the RFP's requested terms (a flat 35% discount off list, uncapped breach liability, full IP assignment, and most-favoured-nation pricing) sit outside what we — or, we believe, any vendor with a real insurance and legal function — can respons­ibly commit to. Section 4 below sets out where we align, where we need to negotiate, and why. We would rather be candid about this in writing now than discover it in contract redlining after award.

We have won and delivered against this exact profile before. **Initech Sensors** — an industrial IoT customer of comparable scale, also evaluating Microsoft Fabric — selected us on real-time ingest performance and governance maturity. We believe Acme is an even stronger fit for the same reasons.

---

## 2. Our Understanding of Acme's Needs

Acme Corp is a $1.4B global manufacturer of industrial sensors and IoT devices, operating across 18 countries with manufacturing in Mexico, Vietnam, and Romania and R&D in Austin and Munich. Acme is a Microsoft/Azure shop retiring legacy Teradata warehouses through 2027.

We understand the platform must, at minimum:

| Requirement | Detail |
| --- | --- |
| Real-time ingest | ~40,000 IoT devices, peak 80,000 events/second |
| Batch ETL | 30+ internal source systems |
| BI & reporting | ~600 analysts and executives, **Power BI is non-negotiable** |
| Self-service prep | ~150 data engineers |
| ML | Predictive maintenance pipelines (planned) |
| Scale | ~280 TB current, ~12 TB/month growth |
| Architecture | Lakehouse, open formats (Parquet, Delta, Iceberg) |
| Geography | Multi-region: EU primary, US East secondary; EU customer data must stay in EU |

We also understand this is a competitive procurement — Acme is evaluating Databricks, Snowflake, Microsoft Fabric, and a regional vendor alongside us — and that award is targeted for 2026-06-30, weighted 30% functional fit, 25% commercial terms, 20% five-year TCO, 15% implementation timeline/risk, 10% vendor stability/references.

---

## 3. Why BTS-Synthetic Is the Right Fit

**Workload coverage, proven at your scale.** Our streaming ingest layer is tested to 250,000 events/second on single-region deployments — more than 3x Acme's stated peak of 80,000 events/second, giving substantial headroom for growth. Our 80+ pre-built batch connectors cover the common ERP, CRM, and database sources typical of a 30-source ETL estate.

**Power BI is our most mature BI integration.** We maintain a dedicated Power BI DirectQuery adapter, purpose-built for exactly the "non-negotiable" requirement Acme has flagged. Unlike Databricks or Snowflake, which treat Power BI as one certified connector among several, this is where we invest disproportionately because so many of our industrial customers standardize on it.

**Lakehouse and open formats, no lock-in.** Native support for Delta, Iceberg, and Parquet means Acme's data remains portable even if strategy changes down the road — directly answering the RFP's stated preference.

**Multi-region and EU data residency, natively.** Per-table residency enforcement lets Acme pin EU customer data to EU regions while running US East as a secondary region, satisfying Section 2.3 without bespoke engineering.

**A governance and ML foundation ready for what's next.** Row/column-level attribute-based access control, PII detection and masking, and full audit logging give Acme's 150 data engineers self-service capability without compromising governance. When predictive maintenance ML becomes active, our model registry and feature store (offline + online serving) are ready — no re-platforming required.

**We've won this exact deal before.** Initech Sensors — industrial IoT, similar scale, also fielding a Microsoft Fabric bid — chose us specifically for real-time ingest performance and governance maturity. We expect the same dynamics to play out here, and Initech will serve as a live reference.

**One honest gap to flag:** we are not best-in-class for sub-100ms streaming query latency (we run 250ms–1s). Nothing in the RFP indicates Acme needs sub-100ms interactive analytics on streaming data, but we want this on the record rather than discovered later.

### How we compare to the other vendors you're evaluating

- **Databricks** will bring a strong ML/open-format story, but total cost of ownership tends to surprise customers as compute spend ramps, and their BI/analyst tooling is a secondary investment for them, not a primary one.
- **Snowflake** offers a polished analyst experience but is materially weaker on real-time/streaming ingest at your event volumes, and its ML story is bolted on rather than native — a gap against your predictive-maintenance roadmap.
- **Microsoft Fabric** will look attractively priced if bundled into an existing E5 license, and it owns Power BI natively. We won't out-compete that ownership claim. What we'd ask you to pressure-test is Fabric's product maturity (broadly ~18 months versus our 8 years in market) and the all-in cost once Microsoft implementation services are included — plus whether Acme wants to concentrate this much of its data estate inside a single cloud vendor's roadmap.

We'd propose a head-to-head 3-year TCO model at your actual workload profile as part of due diligence — this is the comparison that won us Globex Manufacturing against a Snowflake-first mandate, and Initech Sensors against Fabric.

---

## 4. Commercial Proposal

### 4.1 Pricing

Our Enterprise tier (unlimited ingest, unlimited users, 24/7 support, dedicated CSM) is the appropriate tier at Acme's scale, list-priced at **$720,000/year**, plus a **99.99% SLA add-on** discussed in Section 4.3 below (typically $80K–$120K/year, dependent on final architecture).

The RFP requests a minimum 35% discount off list. We want to be transparent about where that sits relative to our pricing governance: our standard enterprise discount bands top out at 20–25%, with a strategic ceiling of 25–30% reserved for multi-year commitments, reference-customer agreements, or flagship logos in target verticals — approved at VP level.

Acme qualifies for our strategic band on the strength of the 3+ year committed term and Acme's profile as a reference-quality industrial IoT account. **We are prepared to offer 28% off list** ($518,400/year base before the SLA add-on), matched to the structure that closed our Stark Industries deal (28% at 5-year horizon) — the largest discount we have extended in this segment, contingent on a signed reference-customer agreement and case study rights.

We recognize this is short of the 35% requested. Rather than meet that number on list price alone (which would come at the expense of the SLA and support commitments below), we'd like to make the case on **5-year total cost of ownership** — factoring in unlimited ingest/user scaling (no true-up fees within a 10% buffer), no migration lock-in penalties from open formats, and the operational cost of the audit/liability terms discussed below. We're glad to build this TCO model jointly and let the numbers, not the headline discount, carry the comparison — this is exactly the approach that won Globex and Initech.

### 4.2 Term and Pricing Fixation

We accept a 3-year initial term with a 2-year renewal option, and can commit to **fixed pricing across the initial 3-year term with no escalator**, consistent with the "no escalators" ask in Section 3.1. Note that this means Acme forgoes our standard multi-year escalator-linked discount uplift (an additional 5%, tied to CPI+2%) — we are not applying it here in order to honor the flat-pricing request. For the 2-year renewal, we propose pricing be re-benchmarked at the prevailing rate card at time of renewal, discounted at no less than the rate secured in the initial term, rather than fixed 5 years in advance for a term that has not yet been committed to.

### 4.3 Service Levels

We propose our standard Enterprise SLA of **99.95% monthly uptime**, with the option to upgrade to **99.99%** via an active-active multi-region deployment add-on. Because Acme already requires EU-primary/US-East-secondary multi-region deployment, the incremental engineering lift for active-active is smaller than usual — we estimate the add-on at the lower end of our typical $80K–$120K/year range, to be firmed up during technical scoping. SLA remedies would follow our standard model: service credits up to 30% of the affected month's fees as the exclusive remedy for a miss, with termination rights reserved for repeated or sustained failures (not a single miss of any duration) — see Section 5 for our reasoning.

### 4.4 Payment Terms

We propose **annual payment in advance at Net 30**, consistent with how the large majority of our enterprise accounts are structured, including deals of comparable or larger size (Stark Industries, Globex, Initech). We recognize Acme requested Net 90 and are open to discussing **Net 60** as a bridge, reflecting Acme's investment-grade profile, but Net 90 is outside what our finance function can extend on an annual-upfront model. We're glad to explore quarterly billing at the same effective annual price if cash-flow timing is the underlying concern.

---

## 5. Contract Approach

We support Acme's underlying goals — cost predictability, accountability, and control over its own data and vendor relationships. We think we can meet those goals through terms slightly different from what's drafted, without weakening the protection Acme is seeking. A full legal redline will follow contract award; the headline positions are:

| Area | RFP Position | Our Position | Why |
| --- | --- | --- | --- |
| Liability (4.1) | Uncapped for any data breach | Capped at 24 months' fees paid, with uncapped carve-outs for gross negligence, willful misconduct, and IP infringement | Uncapped liability is not insurable at any price on our (or most vendors') cyber policy; a 24-month cap with meaningful carve-outs gives Acme real teeth without voiding our coverage — which is itself part of Acme's protection |
| Audit (4.2) | Unannounced, up to 4x/year, vendor pays all costs | 30 days' notice, up to 2x/year, vendor bears cost of the first audit, Acme bears cost of additional audits | Unannounced audits of a multi-tenant platform create operational and security risk for other customers sharing the infrastructure; scheduled audits achieve the same assurance safely |
| SLA / Termination-for-breach (4.3) | Any SLA miss of any duration → immediate termination + full month's refund | 99.95–99.99% SLA with service credits (up to 30% of monthly fees) as remedy; termination reserved for repeated/material breach after cure | Ties remedy to severity, avoiding a single transient blip triggering full contract termination — protects continuity of a system this central to Acme's operations |
| Termination for convenience (3.5) | Either party, anytime, 30 days' notice, no fee | 90 days' notice for convenience; immediate termination for uncured material breach | Enterprise data platform migrations take months to plan; 90 days protects both parties' ability to transition responsibly. We do not charge early-termination penalties either way |
| IP (4.4) | All work product vests in Acme on creation | Acme owns all its data outright; custom configurations, integrations, and reports we build for Acme are licensed to Acme in perpetuity, royalty-free; we retain ownership of our underlying platform and reusable IP | We've structured this exact model successfully with Stark Industries (license-back of derivative works) — Acme gets full practical use of everything built for it without our platform IP fragmenting across every customer contract |
| Subprocessors (4.5) | Prior written consent for any subprocessor, withholdable at Acme's sole discretion | Published subprocessor list, 30 days' advance notice of additions, right to object with substitution or termination as remedy | A pre-approval veto right is operationally unworkable at platform scale; advance notice plus an objection-and-remedy right gives Acme real control without freezing our ability to operate |
| MFN (3.4) | Pricing warranted no less favorable than any comparable customer, for contract duration | Not offered | MFN clauses require tracking and reconciling pricing across our entire customer base indefinitely, which is not operationally sustainable and is not a term we extend to any customer regardless of deal size |

We recognize this table doesn't hand Acme everything requested. We'd rather show our hand plainly now, alongside a workload-level technical fit that we believe is the strongest of any vendor in this process, than negotiate by omission.

---

## 6. Risks and Mitigations (Customer-Facing Summary)

| Risk | Mitigation |
| --- | --- |
| Migration from legacy Teradata warehouses could disrupt reporting continuity during 2026–2027 decommissioning | Phased migration plan (Section below), with legacy and new platform run in parallel until BI workloads are validated on the new system |
| 99.99% uptime target requires architecture Acme hasn't yet scoped in detail | Joint technical workshop in the first 30 days to finalize active-active design before SLA is contractually locked |
| Predictive maintenance ML is "planned, not active" — requirements may shift | Feature store and model registry are available from day one; no re-platforming needed whenever ML work starts |
| Multi-vendor competitive process means commercial terms may need to flex during negotiation | We've proposed our best strategic-tier position up front and are prepared to jointly build a 3-year TCO model to support final terms |

### Indicative Implementation Timeline

- **Weeks 1–8:** First production workload live (typical for customers with clean source systems); initial Power BI connectivity and governance model in place
- **Weeks 1–16:** Full migration path for Teradata-equivalent legacy warehouse workloads
- **Weeks 1–24:** Full cutover for all 30+ sources, all real-time ingest, multi-region EU/US active-active SLA architecture, and ML platform readiness, given Acme's scale and multi-region footprint

Three references available on request, matched to Acme's profile (industrial/IoT, Power BI, Azure, comparable scale): Initech Sensors, Globex Manufacturing, and Wayne Manufacturing.

---

*This proposal is submitted by BTS-Synthetic in response to the Acme Corp RFP dated 2026-05-12. Commercial terms above are indicative and subject to final contract negotiation and technical scoping.*
