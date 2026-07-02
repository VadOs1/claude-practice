# BTS-Synthetic Enterprise Data Platform
## Proposal for Acme Corp
### Response to RFP — Enterprise Data Platform
**Submitted:** 2026-05-22 | **Valid until:** 2026-07-22
**Primary contact:** deals@bts-synthetic.example

---

## Executive Summary

Acme Corp is at a pivotal moment: decommissioning legacy Teradata warehouses while simultaneously scaling real-time IoT telemetry from 40,000 field devices and empowering 750+ data professionals across 18 countries. A patchwork cannot carry you forward — you need an enterprise-grade, open lakehouse that is built for exactly this profile.

BTS-Synthetic's Enterprise Data Platform is that platform. We are the only vendor in your evaluation capable of delivering:

- **Native 99.99% SLA** with active-active multi-region (EU primary + US East) — addressing your data residency requirements from day one
- **Real-time ingest at 250,000 events/second** tested — your 80K peak is well within our operational envelope
- **Certified Power BI DirectQuery adapter** — your 600 analysts move without retraining or reconfiguration
- **Open file formats natively** (Delta, Iceberg, Parquet) — no proprietary lock-in, full portability
- **16-week Teradata migration path** — proven with comparable industrial customers

Comparable wins: Initech Sensors (industrial IoT, $420K/yr, displaced Microsoft Fabric) and Globex Manufacturing (heavy unstructured manufacturing workloads, $580K/yr, displaced Snowflake). Both are available as references.

**Proposed 3-year committed investment:** $2.05M (Years 1–3), with a 2-year renewal option priced and locked at signing. This represents approximately 25% below Enterprise list pricing, including the 99.99% SLA premium and implementation credits.

---

## 1. Technical Proposal

### 1.1 Architecture Overview

BTS-Synthetic's platform is purpose-built as a **true lakehouse**: compute decoupled from storage, open file formats at the foundation, and multiple specialised engines sharing one logical data layer. For Acme, we propose the following architecture:

| Layer | Component | Notes |
|---|---|---|
| Storage | Azure Blob (customer-owned) | EU region primary; US East secondary |
| File format | Delta + Iceberg | Delta for operational tables; Iceberg for cross-system portability |
| Batch ingest | 80+ built-in connectors | SAP, Oracle, Teradata CDC, flat-file |
| Streaming ingest | Native Kafka consumers | Active-active across EU/US East |
| SQL analytics | ANSI SQL engine | Sub-second on warmed caches up to 10 TB |
| BI | Power BI DirectQuery | Certified adapter; no data copy required |
| Self-service prep | Low-code data prep UI | For your 150 data engineers |
| Governance | Unity-style catalog | Row- and column-level security, ABAC |
| ML / AI | Model registry + feature store | Ready for predictive maintenance phase |

### 1.2 Workload Coverage

**Real-time IoT ingest**
Your requirement: 80,000 events/second peak from ~40,000 field devices. Our tested throughput on single-region deployments: 250,000 events/second. Your peak is ~32% of our ceiling. We propose a dedicated streaming cluster in EU West sized for 120K events/second (50% headroom) with auto-scale burst to 200K. Latency to queryable state: typically 800ms–1.5s (streaming windows). Sub-100ms interactive analytics on streaming data is a known weak point in our stack — we are transparent that we hit ~250ms-1s on streaming queries. For operational alerting at sub-100ms, we recommend a companion time-series store (InfluxDB or Azure Data Explorer); our platform handles the analytical lake tier.

**Batch ETL**
30+ internal sources including Teradata (via Debezium-compatible CDC). Migration path: 16 weeks for full Teradata migration, based on comparable engagements (see Globex Manufacturing). We provide pre-built Teradata connectors and schema-mapping tooling.

**BI and Reporting**
Power BI is your stated non-negotiable requirement. It is our most mature BI integration. Our certified DirectQuery adapter supports live query to the lakehouse with row-level security pushed down, meaning your 600 analysts see only data they're entitled to — without any semantic layer rebuild. Existing Power BI reports and datasets require no material rework.

**Self-service data preparation**
Our low-code data prep UI is designed for the analyst/engineer persona. Your 150 data engineers can build and schedule pipelines without writing Spark — though Spark-equivalent compute is available for those who want it, via Python and Scala notebooks.

**Machine learning pipelines (predictive maintenance)**
ML infrastructure is ready today: model registry, feature store (offline + online serving), and native model serving with autoscaling. When Acme's predictive maintenance initiative activates, no additional platform layer is required. Time to first trained model: 2–4 weeks with existing feature engineering from your IoT streams.

### 1.3 Scale

| Metric | Acme requirement | BTS-Synthetic position |
|---|---|---|
| Current data volume | 280 TB | No ceiling on Enterprise tier (object storage) |
| Growth rate | 12 TB / month | Capacity auto-scales; costs are usage-based |
| Peak ingest | 80,000 events/sec | Tested to 250,000 events/sec |
| Analyst users | 600 | Unlimited on Enterprise tier |
| Data engineers | 150 | Unlimited on Enterprise tier |

### 1.4 Multi-region and Data Residency

We deploy active-active across EU West (primary) and US East (secondary). EU data residency is enforced at the table level via per-table pinning — EU customer data tables are tagged at creation and the engine refuses to process them outside the EU region. This is implemented at the storage API layer, not just policy, so it survives configuration drift.

Our GDPR-aligned Data Processing Agreement (DPA) is available for signature and documents this enforcement model. We are SOC 2 Type II and ISO 27001 certified.

### 1.5 Competitive Context

You are evaluating Databricks, Snowflake, and Microsoft Fabric alongside BTS-Synthetic. Here is our honest assessment:

**vs. Microsoft Fabric:** Microsoft is your default vendor because you are an Azure shop with 600 Power BI users. We respect that. Their offer will likely be bundled with your E5 agreement, making the headline price look low or free. What that headline obscures: Fabric is 18 months old as a unified platform; its streaming ingest, governance maturity, and real-time SLA at your scale are not enterprise-tested. We have been doing this for 8 years. For your Teradata migration and IoT ingest workloads specifically, we believe the TCO comparison — including Microsoft consulting hours and integration rework — favours BTS-Synthetic in Year 2 and beyond. We welcome a TCO workshop.

**vs. Databricks:** Databricks will lead with their ML story and Delta Lake pedigree. Both are genuine strengths. Their weakness at Acme's profile: BI and analyst-facing tooling is a second-class citizen in their architecture, and TCO for interactive SQL workloads surprises customers at your scale. We integrate with Power BI natively; they do not prioritise it.

**vs. Snowflake:** Snowflake's analyst experience is best-in-class. Their challenge at your profile: real-time ingest at 80K events/second is expensive on Snowflake's compute model, and their ML story is bolt-on. We ran a comparable workload comparison for Initech Sensors (similar IoT profile) and won on 3-year TCO by 28%.

**Our recommended position:** Lead with Power BI continuity, EU data residency assurance, and real-time ingest performance. Request a joint TCO workshop with Acme's CDO team within two weeks of this submission.

---

## 2. Commercial Proposal

### 2.1 Pricing Basis

All pricing is on BTS-Synthetic's Enterprise tier. List price: $720,000/year base.

We are proposing a **3-year committed term** with a **2-year renewal option**. Pricing for the renewal option is locked at signing per the formula below.

### 2.2 Proposed Pricing

| Year | Base Platform | 99.99% SLA Premium | Annual Fee |
|---|---|---|---|
| Year 1 | $504,000 | $90,000 | **$594,000** |
| Year 2 | $529,200 | $94,500 | **$623,700** |
| Year 3 | $555,660 | $99,225 | **$654,885** |
| **3-Year Total** | | | **$1,872,585** |
| Year 4 (renewal) | $583,443 | $104,186 | **$687,629** |
| Year 5 (renewal) | $612,615 | $109,396 | **$722,011** |
| **5-Year Total** | | | **$3,282,225** |

**Discount from list:** Base platform at Year 1 reflects **30% off list** ($720K list × 0.70 = $504K), reflecting:
- 3-year committed term (+5% vs. standard)
- Strategic account designation (manufacturing vertical, multi-region, logo value)
- Reference customer agreement (see Section 2.5)

**Escalator:** CPI + 2%, capped at 5% per year, applied to both base platform and SLA premium. The 5-year pricing above is computed at the cap (5%) — Acme's actual Year 2–5 fees will be at or below these figures.

> **Note on the 35% discount request:** Our playbook maximum for this deal size and structure is 30% off list. We are at that ceiling. We are not able to offer 35% as this would require us to operate below cost on the SLA premium component. We believe the 5-year TCO at our proposed terms compares favourably to Snowflake and Databricks at their stated discount bands, and we are prepared to demonstrate this in a joint TCO workshop.

### 2.3 Payment Terms

We propose **annual upfront, Net 60** (from invoice date). Invoices issued 30 days before each anniversary.

> **Note on Net 90 request:** Our standard is Net 30. We are offering Net 60 as a concession for Acme's credit profile. We cannot accept Net 90 — this is a binding constraint from our finance covenants.

### 2.4 Implementation Credit

We offer a **complimentary 90-day Proof of Concept**, credit-rolled into Year 1 (no separate fee). The PoC scope: one production IoT data stream, one Power BI dashboard, EU data residency validation. This eliminates deployment risk before financial commitment and has been Acme's requested starting point in analogous engagements.

### 2.5 Reference Customer Agreement

In exchange for the strategic discount, we ask Acme to sign a reference customer agreement permitting BTS-Synthetic to reference Acme Corp as a customer (name and industry only, no financials) in sales materials following the first year of production operation.

### 2.6 Positions We Cannot Accept

In the spirit of transparency, we flag the following RFP commercial requirements that require negotiation before we can execute a contract:

| RFP Clause | Our Position | Severity |
|---|---|---|
| §3.3 — 35% discount | Maximum 30% at this deal structure | Negotiable |
| §3.2 — Net 90 payment | Maximum Net 60 | Negotiable |
| §3.4 — MFN / Most Favoured Nation | We cannot offer MFN to any customer | **Not negotiable** |
| §3.1 — Zero price escalators | Escalator capped at 5%/year (CPI+2%) is required | Negotiable within cap |

---

## 3. Contractual Positions

The following RFP contractual clauses require negotiation. We flag them proactively to avoid surprises during redlining.

### 3.1 Liability — Section 4.1 (BLOCKER)
**RFP says:** "Vendor liability for any data breach is uncapped. Vendor must indemnify Acme for all costs, including notification costs, regulatory fines, and reputational damages."
**Our position:** Aggregate liability capped at 24 months of fees paid (~$1.25M at Year 1 rates), with mutual carve-outs for gross negligence and wilful misconduct. We carry $5M cyber liability insurance — uncapped indemnification voids our coverage.
**Counter:** "Vendor aggregate liability for any data breach capped at 24 months of fees paid as of the date of the breach. Carve-outs for gross negligence and wilful misconduct. Vendor will maintain cyber liability insurance of not less than $5M and provide certificates on request."

### 3.2 Audit Rights — Section 4.2 (BLOCKER)
**RFP says:** "Audit without prior notice, up to four times per calendar year. Costs borne by vendor."
**Our position:** We accept up to 2 audits per year with 30 days' written notice. We pay costs for the first audit; customer pays for any additional. "Without notice" audit rights are a blocker — our SOC 2 program requires scheduled audit windows.
**Counter:** "Customer may conduct 2 audits per year with 30 days' notice. Vendor bears cost of first audit per year. Additional audits at customer's cost. Audit subject to confidentiality agreement."

### 3.3 Service Levels — Section 4.3 (BLOCKER on remedy)
**RFP says:** "99.99% monthly uptime. Any SLA failure entitles Acme to terminate with full refund."
**Our position:** 99.99% uptime is achievable as a premium add-on (included in our pricing above). However, termination for a single SLA miss is a blocker — SLA credits (up to 30% of monthly fees) are the appropriate remedy. Instant termination on first miss with full refund is operationally incompatible with any SLA-backed product.
**Counter:** "99.99% monthly uptime commitment. SLA failure: service credits of 10% of monthly fee per 0.01% shortfall, capped at 30% of monthly fees. Right to terminate for convenience with 90 days' notice if SLA is missed in 3 or more consecutive months."

### 3.4 Intellectual Property — Section 4.4 (BLOCKER)
**RFP says:** "All work product shall vest in Acme Corp upon creation."
**Our position:** We retain IP in all platform components, base code, and methodologies. Customer-specific deliverables (custom reports, configurations, integration scripts) are licensed to Acme on a perpetual, royalty-free basis — not assigned. We cannot assign IP in work product that shares code with our core platform.
**Counter:** "Vendor retains ownership of all pre-existing IP and platform components. Customer-specific deliverables are licensed to customer on a perpetual, royalty-free, non-exclusive basis. Customer data is, at all times, the property of customer."

### 3.5 Subprocessors — Section 4.5 (BLOCKER)
**RFP says:** "Vendor shall obtain Acme's prior written consent before engaging any subprocessor. Consent may be withheld at Acme's sole discretion."
**Our position:** Pre-approval of every subprocessor is operationally impossible for a cloud SaaS provider. We maintain a public subprocessor list and provide 30 days' written notice before adding any new subprocessor. Customer may object; we will substitute or, if substitution is impossible, allow termination for cause.
**Counter:** "Vendor maintains a current subprocessor list available at [URL]. Vendor will notify customer 30 days before engaging any new subprocessor. Customer may object within 14 days; vendor will use reasonable efforts to accommodate. If vendor cannot substitute and customer objects, customer may terminate the affected services with 30 days' notice."

### 3.6 Termination — Section 3.5 (Negotiable)
**RFP says:** "Terminate at any time, with or without cause, on 30 days' written notice. No early termination fees."
**Our position:** We accept termination for convenience with **90 days'** written notice (not 30). Pro-rated refund of prepaid fees for the unused portion of the period. No early termination fees.
**Counter:** "Either party may terminate for convenience on 90 days' written notice. Upon termination, vendor will refund pro-rated prepaid fees for the unused committed period."

---

## 4. Implementation Plan

### 4.1 Timeline

| Milestone | Target | Duration |
|---|---|---|
| Contract signature | Week 0 | — |
| Kickoff + environment provisioning | Week 1–2 | 2 weeks |
| **PoC: one IoT stream + Power BI dashboard** | Week 6 | 4 weeks |
| PoC acceptance + Year 1 invoice | Week 10 | — |
| Teradata migration (Phase 1: schema + historical) | Week 10–20 | 10 weeks |
| Batch ETL — top 10 sources | Week 12–18 | 6 weeks |
| Streaming ingest — all 40K devices | Week 16–22 | 6 weeks |
| **First production workload** | Week 12 | 8 weeks from PoC start |
| Power BI migration (all 600 users) | Week 18–24 | 6 weeks |
| Teradata decommission readiness | Week 26 | — |
| **Full platform live** | Week 26 | ~24 weeks total |
| ML infrastructure ready | Week 20 | Available when needed |

### 4.2 Staffing (BTS-Synthetic side)

| Role | Commitment |
|---|---|
| Dedicated Customer Success Manager | Full-time, Year 1 |
| Lead Solutions Architect | Full-time, Weeks 1–26 |
| Data Migration Engineer (Teradata specialist) | 50%, Weeks 8–22 |
| Streaming Infrastructure Engineer | 50%, Weeks 12–22 |
| Power BI Integration Specialist | 50%, Weeks 16–24 |

### 4.3 Customer prerequisites

- Azure Blob Storage containers provisioned (EU West + US East) before Week 2
- Network connectivity (ExpressRoute or VPN) from manufacturing facilities to EU West region
- Teradata export access (read-only service account + connectivity)
- Power BI admin access for connector deployment

### 4.4 Key risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Teradata schema complexity (18-country data) | Medium | Dedicated migration engineer; schema-mapping workshop in Week 2 |
| IoT device connectivity heterogeneity | Medium | Pre-built adapters for top 5 industrial protocols; custom adapters for others in PoC scope |
| Power BI report rework (complex DAX) | Low | DirectQuery adapter preserves existing DAX in most cases; regression testing in Week 22 |
| EU data residency audit failure | Low | Per-table enforcement at storage API layer; tested in PoC |
| Teradata decommission schedule (2027) | Low | Platform ready by Week 26; 12+ months buffer |

---

## 5. Customer References

The following customers have agreed to serve as references for Acme. All are similar in scale, Power BI deployment, and Azure infrastructure.

| Customer | Industry | Annual Value | Won Against | Contact (available on request) |
|---|---|---|---|---|
| **Initech Sensors** | Industrial / IoT | $420K | Microsoft Fabric | CDO, available by phone |
| **Globex Manufacturing** | Industrial / Manufacturing | $580K | Snowflake, Databricks | VP Data, available by phone or site visit |
| **Stark Industries** | Industrial / Aerospace | $1.1M | Databricks, Snowflake, Fabric | CIO, available by video call |

All three are multi-year customers, Azure-primary, with Power BI as their primary BI layer. Initech Sensors is the closest profile to Acme (IoT, similar event volumes, EU data residency requirement). We recommend starting there.

---

## 6. Why BTS-Synthetic

| Criterion | Our position |
|---|---|
| **Functional fit** | Full coverage on Power BI, real-time ingest, multi-region, data residency, lakehouse, open formats. Partial on sub-100ms streaming analytics (transparent disclosure). |
| **Commercial** | 30% off Enterprise list, Net 60 payment, 5-year pricing locked at signing with ≤5%/year escalator. |
| **TCO** | Predictable spend model; no per-query compute surprise at scale. Volume true-up at year-end with 10% buffer. |
| **Implementation** | 8 weeks to first production workload; 26 weeks to full migration. Dedicated CSM + architect through Year 1. |
| **References** | Three comparable industrial customers, all Azure + Power BI, all available. |
| **Financial stability** | 8 years in market, SOC 2 Type II, ISO 27001, GDPR-aligned DPA. |

We look forward to presenting this proposal to Sarah Chen and Marcus Webb. We are available for a technical deep-dive or TCO workshop at Acme's convenience.

**BTS-Synthetic Deal Desk**
deals@bts-synthetic.example

---

*This proposal is confidential and intended solely for Acme Corp's evaluation committee.*
*All pricing is valid until 2026-07-22.*
