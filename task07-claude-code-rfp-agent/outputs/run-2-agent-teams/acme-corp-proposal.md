# BTS-Synthetic — Proposal for Acme Corp Enterprise Data Platform

**Prepared for:** Sarah Chen, VP Procurement / Marcus Webb, Chief Data Officer, Acme Corp
**Prepared by:** BTS-Synthetic
**Date:** 2026-07-04
**In response to:** RFP issued 2026-05-12, response due 2026-05-26

---

## Executive Summary

- **Strong technical fit, low risk:** BTS-Synthetic's lakehouse platform natively meets Acme's core requirements — 80,000 events/second peak ingest (we're proven to 250,000 events/sec), native Power BI DirectQuery integration for your 600 analysts, and per-table EU data residency across a multi-region EU/US topology.
- **Proven in your exact vertical:** We won a near-identical industrial IoT deal (Initech Sensors) against Microsoft Fabric on real-time ingest performance and governance maturity — the same battleground Acme is evaluating on.
- **Commercial terms grounded in real deal data, not list-price theatre:** We propose an 18-20% discount off list, anchored to a 3-year TCO model at your actual workload profile — the same approach that won Globex Manufacturing away from Snowflake and Databricks.

## Our Understanding of Your Need

Acme is replacing a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics with a single enterprise data platform, ahead of full Teradata decommission by 2027. The platform must handle real-time ingest from 40,000 IoT devices (peak 80,000 events/sec), batch ETL from 30+ sources, BI/reporting for 600 users, self-service prep for 150 data engineers, and eventually ML pipelines for predictive maintenance — all at ~280TB and growing 12TB/month. As an Azure-native, Power BI-first organization with EU and US operations, you need native Power BI integration (non-negotiable), EU data residency, open lakehouse formats (Parquet/Delta/Iceberg), and a platform that will still be portable and cost-predictable five years from now. You are also evaluating Databricks, Snowflake, and Microsoft Fabric, and are pricing this as a 5-year, fixed-cost decision.

## Why We're the Right Fit

**Technical fit: HIGH.** Against the full requirements list, our gaps are narrow and non-blocking:

- **Ingest at scale:** Native Kafka/Kinesis streaming tested to 250K events/sec single-region — 3x headroom over your 80K events/sec peak. 40,000 devices and 30+ batch sources are fully covered by our 80+ connector library.
- **Power BI:** Our most mature BI integration, with a dedicated DirectQuery adapter — built for exactly the scale of your 600-user analyst and executive base.
- **Multi-region EU/US + residency:** Native multi-region deployment on Azure with per-table residency pinning keeps EU data in EU regions while US East serves as your secondary — matching your requested topology exactly.
- **Open formats:** Full native support for Parquet, Delta, and Iceberg, so you retain portability and are never locked into a single vendor's proprietary format.
- **ML readiness:** Model registry, offline/online feature store, and native model serving are in place and ready for your predictive maintenance roadmap when it activates.
- **One honest flag:** Your 99.99% uptime ask (RFP §4.3) sits above our standard Enterprise SLA of 99.95%. We can deliver 99.99% via a multi-region active-active architecture — priced transparently as a add-on rather than silently absorbed (see Commercial Proposal).

**Why we win against the field:** Microsoft Fabric will lead with E5 bundling and native Power BI — but in our closest analog (Initech Sensors, same industrial IoT profile), Fabric could not match the real-time ingest SLA your 80,000 events/sec workload demands. Databricks and Snowflake will contest openness and lakehouse credentials; we beat both of them at Globex Manufacturing not on list price but on a 3-year TCO comparison run against the customer's actual workload — the same analysis we're prepared to run for Acme. We win this deal on proven real-time performance plus governance maturity, not a race to the bottom on discount.

## Commercial Proposal

We propose commercial terms informed directly by comparable enterprise wins of similar scale and vertical (Globex Manufacturing, Initech Sensors, Stark Industries):

- **Discount:** 18-20% off published list pricing for the 3-year initial term (floor 17%). This is a meaningfully deeper discount than our Initech Sensors close (15%, smaller deal) in recognition of Acme's scale, and reflects real economics rather than the unsustainable 35%+ levels that have cost competitors margin and, in at least one case we've observed in the market, the entire deal.
- **Term & pricing structure:** 3-year initial term with 2-year renewal option. We will fix Year 1-3 pricing at signature; for the renewal years we propose a capped escalator (CPI or 3%, whichever is lower) rather than a fully open-ended 5-year zero-escalator commitment, which is not commercially sustainable given infrastructure cost trends.
- **Payment terms:** Annual in advance, Net 45 — a concession from our Net 30 standard, in exchange for firming up the discount band.
- **SLA:** 99.95% uptime included in the base offer (service credits, up to 30% of monthly fees, as sole remedy for misses). 99.99% uptime available as a priced add-on (multi-region active-active architecture, indicative $80K-120K/year) for workloads that require it.
- **MFN clause:** We will warrant most-favoured pricing scoped to comparable industrial IoT customers of similar size and term — not an unscoped, unlimited warranty across our full customer base.
- **Termination:** We accept termination for convenience; we propose 60-90 days' notice (vs. the requested 30) given the operational lead time required to wind down a platform of this scale, with no early termination fee.
- **Indicative deal size:** ~$650K-800K/year at list, ~$530K-650K/year at the proposed discount band — approximately $1.6M-2M across the initial 3-year term.

## Contract Approach

Several clauses in the RFP's draft terms are outside our standard risk posture and require negotiation before signature. We flag severity and our counter-position on each:

| Clause | Severity | Our Counter-Position |
| --- | --- | --- |
| Uncapped breach liability (§4.1) | Blocker | Cap liability at 24 months' fees, with carve-outs for gross negligence and IP infringement |
| Unannounced audits, 4x/year, vendor-funded (§4.2) | Blocker | One audit/year, 30 days' notice, confidentiality terms; additional audits at Acme's cost |
| 99.99% SLA with immediate termination on any miss (§4.3) | Blocker | 99.95% standard SLA with service credits as sole remedy; 99.99% available as a paid add-on |
| Full IP assignment of all work product (§4.4) | Blocker | BTS retains underlying platform IP; Acme receives a perpetual licence to derivative/custom work — the same structure Stark Industries (a comparable enterprise account) accepted in lieu of full assignment |
| Subprocessor consent at Acme's sole discretion (§4.5) | Blocker | Published subprocessor list with 30 days' advance notice of changes; Acme may object, with substitution or termination rights for the affected service |
| Termination for convenience, 30 days, no fee (§3.5) | Negotiable | Extend notice period to 60-90 days; no early termination fee accepted |
| MFN warranty (§3.4) | Negotiable | Scope to comparable industrial IoT accounts of similar size/term |
| Net 90 payment (§3.2) | Negotiable | Counter at Net 45 |

None of these positions are unprecedented: we have resolved the IP question on these exact terms with Stark Industries, a comparable enterprise account, and resolved discount/payment tension with Initech Sensors, an almost identical industrial IoT profile. We read this RFP's draft terms as an aggressive opening position typical of enterprise procurement, not a walk-away signal.

## Risks and Mitigations

- **SLA/termination stacking (§4.3):** The combination of a 99.99% uptime demand with immediate-termination-on-any-miss is the single largest deal risk. *Mitigation:* offer 99.95% standard with credits as sole remedy, and price 99.99% transparently as an add-on rather than accepting the compounded penalty risk into the base contract.
- **Five-year fixed pricing with no escalators:** Exposes us to infrastructure cost inflation over the renewal period. *Mitigation:* fix pricing for the initial 3-year term; cap (not eliminate) escalators for the 2-year renewal.
- **Unscoped MFN warranty:** Could constrain our pricing flexibility across our entire book for years. *Mitigation:* scope the warranty to comparable industrial IoT accounts only.
- **Price-anchoring risk:** The RFP's 35% discount floor mirrors a pattern we've seen competitors chase to their own detriment in commodity-perceived deals. *Mitigation:* lead commercial conversations with 3-year TCO analysis at Acme's actual workload (per the Globex Manufacturing playbook), not a discount-percentage negotiation.
- **Competitive displacement by Microsoft Fabric on price/bundling:** Fabric may undercut via E5 bundling. *Mitigation:* keep the conversation anchored on proven real-time SLA performance (Initech Sensors precedent), where Fabric has a demonstrated gap.
- **Uncapped liability and unrestricted audit rights:** Both create open-ended operational and financial exposure. *Mitigation:* negotiated caps and scoped audit rights as detailed in the Contract Approach section above, prior to signature.

We are ready to move quickly — our standard implementation timeline for a customer of Acme's scale and complexity (multi-region, multi-source, legacy migration) is 24 weeks to full production, with first production workload achievable in 8 weeks. We look forward to discussing this proposal with Sarah Chen and Marcus Webb's team.
