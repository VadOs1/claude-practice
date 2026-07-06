# BTS-Synthetic — Enterprise Data Platform Proposal for Acme Corp

**Prepared for:** Sarah Chen, VP Procurement / Marcus Webb, Chief Data Officer, Acme Corp
**Prepared by:** BTS-Synthetic Deal Desk
**Date:** 2026-07-05
**In response to:** RFP issued 2026-05-12, response due 2026-05-26

---

## Executive Summary

- BTS-Synthetic's lakehouse platform is a **high-confidence functional fit** for Acme's real-time IoT ingest, BI/analyst, and predictive-maintenance roadmap — including native Power BI, open file formats (Parquet, Delta, Iceberg), and per-table EU data residency.
- We propose a **5-year fixed-price commercial structure** (3-year initial term + 2-year renewal, no escalators) with a **28% discount off list**, backed by directly comparable wins in industrial IoT (Initech Sensors) and multi-region/sovereign deployments (Stark Industries).
- Our contract approach protects both sides: **market-standard liability caps, tiered SLA credits, and licensed (not assigned) IP** — terms that have closed deals of this profile before, and that we're prepared to work through with Acme's legal team on an accelerated timeline.

---

## Our Understanding of Your Need

Acme is consolidating a patchwork of legacy Teradata warehouses and ad-hoc cloud analytics onto a single platform ahead of a 2027 decommission deadline. The platform must handle real-time ingest from ~40,000 IoT devices (peak 80,000 events/sec), batch ETL from 30+ sources, BI/reporting for 600 analysts, self-service prep for 150 data engineers, and a near-term roadmap into predictive-maintenance ML — all on an Azure-first, EU/US multi-region footprint with strict EU data residency and non-negotiable native Power BI integration. You are evaluating us alongside Databricks, Snowflake, and Microsoft Fabric, with award weighted heavily toward functional fit (30%), commercial terms (25%), and 5-year TCO (20%).

## Why BTS-Synthetic Is the Right Fit

**Technical fit: High.** Our lakehouse architecture natively supports Delta, Iceberg, and Parquet, giving you the open-format portability the RFP calls for without a rip-and-replace of your data contracts. Our Power BI integration is our most mature BI adapter — a dedicated DirectQuery connector, not a bolt-on. Batch ETL from 30+ sources, BI for 600 analysts, and self-service prep for 150 engineers are all comfortably within our out-of-the-box capability, and our model registry, feature store, and native model serving mean your predictive-maintenance roadmap has a home on the same platform from day one. Per-table residency pinning satisfies your EU-data-stays-in-EU requirement directly.

We will validate two items with you during technical due diligence rather than overstate them today: streaming throughput at your peak 80,000 events/sec in a true multi-region (EU-primary/US-secondary) topology, and SQL performance characteristics at your full 280TB+ working set. Neither is a gap in our platform; both simply deserve a joint validation exercise before go-live given the scale involved.

**Why not Databricks, Snowflake, or Microsoft Fabric?** Each is a credible operator, and you'll hear a compelling case from all three. Microsoft Fabric will lean hard on "already in your E5 tenant" and Power BI — a fair point, but one that trades a lower sticker price today for a shallower track record at your scale and workload mix, and locks you into Azure with no multi-cloud optionality if your strategy ever changes. Databricks will lean on the same open-format story we're telling you — the difference is proven multi-region production maturity at your scale, not just format compatibility. Snowflake is a safe, mature choice for BI, but real-time ingestion at 80,000 events/sec is not its strength. We'd rather win this on a transparent, itemized 5-year TCO model at your actual workload profile than on a feature checklist — that comparison is where we've won directly comparable deals before (see Commercial Proposal below).

## Commercial Proposal

We propose the following structure, built around your 3-year initial term with a 2-year renewal option and a fully fixed 5-year price at signature — no escalators:

| Term | Our Proposal |
|---|---|
| Discount off published list | **28%**, with a path to 30% as a best-and-final commitment reflecting your full 3-year committed term |
| Term structure | 3-year initial + 2-year renewal option, priced and fixed for the full 5-year horizon at signature, as requested |
| Payment terms | Annual in advance, **Net 60** |
| Escalators | None — fixed pricing for the full 5-year horizon as requested |
| Most Favoured Nation | We propose a narrowed, time-bound version tied to your specific tier and volume commitment rather than an open-ended, perpetual warranty |

This structure mirrors terms we've closed with directly comparable customers: a 28% discount on a 5-year, multi-region deployment for a similarly complex industrial customer, and a win against Microsoft Fabric in the IoT/sensor vertical decided on real-time ingest performance and governance maturity rather than headline discount depth. We are confident a transparent, itemized 5-year TCO comparison — built against your actual workload profile — will show BTS-Synthetic as the most cost-effective option at your scale, and we'd like to build that model jointly with your finance team early in the process.

## Contract Approach

We want this to move quickly, so we're flagging our standard positions on the handful of terms in Section 4 where we'll need to align with your legal team, alongside our proposed counters:

- **Liability & indemnification:** We propose a liability cap set at 24 months of fees paid, with uncapped carve-outs for gross negligence, confidentiality breach, and IP infringement — a structure that keeps both parties' exposure insurable and predictable.
- **Audits:** One scheduled audit per year with 30 days' notice, at our cost; additional audits available at your request, at your cost.
- **Service levels:** We commit to 99.95% monthly uptime as standard, with tiered service credits (up to 30% of monthly fees) as the remedy for shortfalls, and a termination right if performance is chronically below target across a defined window. A 99.99% active-active multi-region tier is available as a priced add-on if your board requires it.
- **Intellectual property:** You own your data outright. Custom configurations and integrations built for Acme are licensed to you on a perpetual, non-exclusive, royalty-free basis — the same model we've used successfully with customers who initially requested full IP assignment.
- **Subprocessors:** We propose a notice-and-object model (30 days' notice, with a substitution or termination right if unresolved) rather than case-by-case pre-approval, to keep operations moving without introducing avoidable delay.
- **Termination:** We're aligned with a for-convenience termination right and no early-termination penalty; we'd like this to be mutual, with 60–90 days' notice to allow for an orderly transition on both sides.

None of these are unusual asks in enterprise data platform agreements, and we've closed on comparable terms with customers of your size and profile before. We're ready to work through redlines with your legal team immediately upon shortlisting.

## Risks and How We Mitigate Them

- **Throughput at scale in a multi-region topology:** we propose a joint technical validation sprint during due diligence, ahead of contract signature, so both sides have confidence in production numbers before go-live.
- **SLA expectations:** rather than commit to a number we can't stand behind, we're offering our proven 99.95% standard tier with strong credit remedies, plus a clearly priced path to 99.99% if that becomes a hard requirement.
- **Migration risk from Teradata:** based on comparable deployments, a program of your scale and multi-source complexity typically runs 16–24 weeks to full migration; we'll propose a phased cutover plan with your legacy warehouses running in parallel until each workload is validated.
- **Commercial alignment:** the gap between your 35% discount ask and our proposed 28–30% is real; we believe an itemized, transparent 5-year TCO comparison — not discount depth alone — is the fastest way to close that gap credibly.

We look forward to discussing this proposal with your team and are prepared to move on your timeline toward the 2026-06-30 award date.

*— BTS-Synthetic Deal Desk*
