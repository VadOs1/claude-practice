# Proposal: Enterprise Data Platform for Acme Corp

**Prepared by:** BTS-Synthetic
**Prepared for:** Acme Corp Procurement Office — Sarah Chen (VP Procurement), Marcus Webb (Chief Data Officer)
**Date:** 2026-07-06
**In response to:** RFP issued 2026-05-12, Enterprise Data Platform

---

## Executive Summary

- **Strong functional fit.** BTS-Synthetic's lakehouse platform natively covers Acme's full workload mix — 40,000-device real-time IoT ingest, 30+ source batch ETL, self-service prep, and BI/reporting — with Power BI as our most mature, purpose-built integration (dedicated DirectQuery adapter), matching your single non-negotiable requirement.
- **A platform built to retire Teradata cleanly**, not a bet on unproven architecture: EU/US multi-region deployment with per-table EU data residency enforcement, open formats (Parquet, Delta, Iceberg) for long-term portability, and a phased migration that puts your first production workload live in 8 weeks.
- **A commercial and contractual position designed for a multi-year partnership**, not a single transaction — we propose meaningful, TCO-justified pricing, and counter-positions on liability, audit, and SLA terms that keep this agreement bankable for both sides over the full 5-year horizon.

---

## Our Understanding of Your Needs

Acme Corp is retiring a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics in favor of a single enterprise data platform, to be substantially complete by 2027. As a global industrial IoT/sensor manufacturer (~$1.4B revenue, 7,200 employees, manufacturing in Mexico, Vietnam, and Romania, R&D in Austin and Munich), your platform must simultaneously serve:

- **Real-time ingest** from ~40,000 fielded IoT devices, peaking at 80,000 events/second
- **Batch ETL** from 30+ internal systems
- **BI and reporting** for ~600 analysts and executives, built around Power BI
- **Self-service data preparation** for ~150 data engineers
- **Predictive-maintenance ML pipelines**, planned but not yet active

At ~280TB today and growing ~12TB/month, this is an enterprise-scale, multi-region program with a hard EU data-residency constraint and a lakehouse/open-format architecture preference. We understand the platform decision will be evaluated on functional fit (30%), commercial terms (25%), 5-year TCO (20%), implementation timeline/risk (15%), and vendor stability/references (10%) — and that Databricks, Snowflake, and Microsoft Fabric are also under evaluation.

---

## Why BTS-Synthetic Is the Right Fit

**Fully met today, with no gaps:**

- Lakehouse architecture with native Delta, Iceberg, and Parquet support — a direct match for your portability requirement
- Batch ETL: 80+ pre-built connectors, well beyond your 30+ source count
- **Power BI**: our most mature BI integration, with a dedicated DirectQuery adapter — this is the capability advantage neither Databricks nor Snowflake can match natively, and where even Microsoft Fabric's home-turf advantage is really an incumbency story, not a technical one
- EU data residency via per-table residency pinning, and multi-region deployment (EU primary, US East secondary) — both natively supported, not custom work
- BI/reporting scale for 600 analysts, and self-service prep for 150 data engineers via our low-code UI plus Python/R/Scala notebooks
- ML foundation for predictive maintenance (model registry, feature store, native model serving) already in place ahead of your planned rollout

**Two areas we want to be transparent about, and how we address them:**

1. **Peak real-time ingest at multi-region scale.** We are proven well past your 80,000 events/second peak (tested to 250K events/sec), but that benchmark is on a single-region deployment. Given your EU-residency constraint applied at ingest across a globally distributed device fleet, we propose a joint architecture validation exercise during onboarding to confirm multi-region ingest performance against your actual device topology before go-live, rather than asking you to take it on faith.
2. **99.99% uptime.** Our standard Enterprise tier is 99.95%. We can meet 99.99% through our multi-region active-active add-on, and we address the commercial mechanics of this directly in the Commercial Proposal and Risks sections below — we would rather be upfront about this now than have it surface as a surprise during contracting.

**Positioning against the field:** Databricks is a strong technical competitor for compute-heavy ML workloads, but its Spark-based compute model tends to produce TCO surprises at your data volume and growth rate, and it has no native Power BI integration. Microsoft Fabric has the incumbency advantage of your existing Azure/E5 relationship and native Power BI support, but it is a young platform (in market ~18 months) for a workload this business-critical, and real-time ingest at your peak scale is not its demonstrated strength. Snowflake is the most mature analyst experience of the three, but it is fundamentally batch-oriented, treats ML as a bolt-on, and is typically the most expensive option at your scale. We recommend Acme evaluate all vendors on a single basis: **a 5-year total cost of ownership model run against your actual workload profile**, not list-price or single-capability comparisons — this is where we believe we differentiate most clearly.

---

## Commercial Proposal

**Pricing.** Based on your scale (280TB, 40K devices, 600 BI users, 150 engineers) and unlimited-ingest needs, this places Acme in our Enterprise tier at **$720,000/year list price**.

We propose an **initial discount of 20% off list ($576,000/year)**, fixed and flat across the full 5-year horizon (3-year initial term + 2-year renewal) with **no escalators**, as requested — total 5-year contract value of **$2.88M**. In recognition of the scale and strategic nature of this partnership, we can extend to **25% off list ($540,000/year, $2.70M over 5 years)** in exchange for a customer-reference and case-study agreement, consistent with how we've structured comparable industrial/IoT engagements at similar scale.

We are not in a position to commit to a 35% discount floor as a contractual precondition. Rather than compete on headline discount alone, we ask Acme to evaluate this proposal on a like-for-like 5-year TCO basis: our experience in comparable industrial IoT engagements is that platforms with higher advertised discounts have consistently cost more once compute overrun, storage growth, and migration risk are priced in over a multi-year term. We are glad to build that TCO model jointly with your team as part of evaluation.

**Term and payment.** We accept the 3-year initial term with 2-year renewal option, and will hold full 5-year pricing fixed at signature as requested. On payment terms, we propose **Net 60** (rather than Net 90), annual in advance — or, if the underlying need is cash-flow smoothing rather than the specific term, we're open to quarterly billing at the same effective annual pricing.

**On the Most Favoured Nation clause:** we are not able to offer an ongoing warranty that pricing will never be more favorable elsewhere — this is not a term we extend to any customer, as it constrains our ability to price flexibly across our full customer base over a multi-year term. In its place, we offer the fixed, non-escalating discount commitment above as Acme's pricing guarantee for the life of the contract.

**What we're offering in addition:**
- A custom Master Services Agreement reflecting the terms below
- A 30-day acceptance testing period following go-live of each production workload
- Year-end volume true-up with a 10% buffer, reflecting your ~12TB/month growth trajectory (note: Enterprise tier ingest is not volume-capped, so this is a capacity-planning term rather than a pricing lever)
- Pro-rated refund on termination for convenience (see Contract Approach)

---

## Contract Approach

We reviewed the RFP's contractual terms (Section 4) against our standard positions. Most of the RFP's requirements are ones we meet as-is or can accept directly — data residency and multi-region terms match our standard exactly. On a handful of clauses, we're proposing counter-positions rather than silent acceptance, because they fall outside terms we can respons­ibly insure or operationalize:

| Area | Your Request | Our Proposed Position |
| --- | --- | --- |
| **Liability & indemnification** | Uncapped liability; full indemnification incl. reputational damages | Cap at 24 months of fees paid, with uncapped carve-outs for gross negligence and IP infringement; indemnification for direct breach-notification costs and regulatory fines |
| **Audit rights** | No-notice audits, up to 4x/year, vendor bears all costs | Annual audit with 30 days' written notice; additional audits (up to 2/year) available at Acme's cost; findings kept confidential |
| **SLA target & remedy** | 99.99% uptime; any SLA miss triggers immediate termination + full month refund | 99.95% standard (99.99% available via active-active add-on, see Risks); service credits as primary remedy, capped at 30% of monthly fees; termination right after sustained failure (3 consecutive months) with cure period |
| **IP ownership** | All custom work product vests in Acme on creation | Customer-specific configurations/integrations licensed to Acme perpetually, royalty-free, for internal use; underlying platform IP remains ours — protects reusable components while giving you full usage rights |
| **Subprocessors** | Prior written consent required for every subprocessor, at Acme's sole discretion | Published subprocessor list with 30 days' advance notice of additions; Acme may object on reasonable grounds, with substitution or termination if unresolved |
| **Termination for convenience** | 30 days' notice, no fees | Accepted, with the clarification that refunds on early termination are pro-rated for services already rendered |
| **MFN pricing warranty** | Pricing must be no less favorable than any comparable customer | Declined as an ongoing warranty (see Commercial Proposal); replaced with our fixed 5-year discount commitment |

We believe every counter-position above is standard commercial practice and does not reduce the substance of what you're asking for — it makes the agreement one both sides can actually operate and insure over a 5-year term. We're glad to walk through the rationale for any of these live with your legal team.

---

## Implementation Plan

Given Acme's scale (multi-region, multi-source, full Teradata retirement), we propose a phased migration:

| Phase | Timeline | Milestone |
| --- | --- | --- |
| Phase 1 | Weeks 1–8 | First production workload live (highest-value BI/reporting use case) |
| Phase 2 | Weeks 9–16 | Core Teradata migration substantially complete; batch ETL from primary sources cut over |
| Phase 3 | Weeks 17–24 | Full multi-region rollout complete: remaining sources, real-time IoT ingest at full scale, self-service prep rollout to all 150 engineers |
| Ongoing | Month 6+ | Predictive-maintenance ML pipeline enablement (aligned to your "planned, not active" timeline) |

A joint multi-region ingest architecture validation (see Fit section) is scheduled early in Phase 1, before any go-live commitment on real-time SLA.

---

## Customer References

The following reference customers reflect comparable scale, industry, and/or platform profile to Acme's engagement:

1. **Globex Manufacturing** — Industrial/Manufacturing, Enterprise tier, 3-year term. Selected us over Databricks/Snowflake on a 3-year TCO comparison run against their actual (heavy unstructured) workload profile.
2. **Initech Sensors** — Industrial/IoT, Enterprise tier. The closest comparable to Acme's profile: won against Microsoft Fabric on real-time ingest performance and governance maturity.
3. **Wayne Manufacturing** — Industrial, Enterprise tier, began with a 90-day proof-of-concept and has since signed a formal reference-customer agreement.

Full reference contacts available on request.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| **Multi-region real-time ingest at peak scale is unvalidated** for your specific EU/US topology, though we are proven well past your throughput requirement in single-region deployments | Could affect go-live confidence for the real-time IoT workload | Joint architecture validation exercise in Phase 1, before any SLA commitment on the real-time path |
| **99.99% uptime exceeds our standard tier (99.95%)** | Gap between your ask and our out-of-box SLA | Multi-region active-active add-on available to close the gap; alternatively, we propose a 99.95% target with credit-based remedies (see Contract Approach) rather than an unattainable guarantee paired with a zero-tolerance termination trigger |
| **5-year fixed pricing with no escalator, against rising infrastructure costs and ~12TB/month volume growth** | Long-term margin pressure on our side; if unmanaged, risk of service-quality trade-offs over the contract life | We've sized this into our proposed discount band rather than asking for a mid-term repricing right — no action needed from Acme, but it's why we can't also stack a further discount on top of the fixed-pricing ask |
| **Aggressive default contractual terms** (uncapped liability, no-notice audits, immediate-termination SLA, full IP vesting, MFN) as issued in the RFP | If accepted as-is, these terms are not ones we — or likely any vendor — could respons­ibly sign and still deliver a stable, adequately-resourced engagement over 5 years | Counter-positions proposed in Contract Approach, each designed to preserve your substantive protections while keeping the agreement operable and insurable |
| **Competitive field is price-aggressive** (multiple vendors bidding, one likely willing to discount steeply) | Risk that evaluation defaults to headline discount rather than TCO | We're proposing a joint 5-year TCO model as part of evaluation, so the comparison reflects delivered cost, not list-price optics |

---

*This proposal is submitted in response to Acme Corp's RFP dated 2026-05-12. We look forward to discussing next steps with your team.*
