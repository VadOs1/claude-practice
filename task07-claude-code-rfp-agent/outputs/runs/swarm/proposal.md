# BTS-Synthetic — Enterprise Data Platform Proposal
## Response to: Acme Corp RFP — Enterprise Data Platform
**Prepared for:** Sarah Chen, VP Procurement & Marcus Webb, Chief Data Officer, Acme Corp
**Prepared by:** BTS-Synthetic Deal Desk
**Date:** 2026-07-02
**Proposal Reference:** BTS-2026-ACME-EDP-001

---

# Executive Summary

Acme Corp is replacing a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics with a unified Enterprise Data Platform. You require real-time IoT ingest at 80,000 events per second, a 280 TB+ lakehouse growing at 12 TB per month, native Power BI integration for 600 analysts, EU data residency, and multi-region deployment — all delivered on your existing Azure infrastructure.

**BTS-Synthetic meets every one of your functional requirements.** Our platform delivers a proven, production-hardened lakehouse architecture that has handled workloads at this scale and complexity in regulated EU manufacturing environments. We are not pitching a roadmap — we are describing what is in production today.

**Three reasons to choose BTS-Synthetic:**

1. **Proven scale and stability.** We have years of production experience with 200 TB+ enterprise lakehouses in regulated manufacturing environments. Competing platforms at the cutting edge of this market are 12–24 months old at this scale. We are not.

2. **True multi-cloud optionality, no lock-in.** Azure is your primary cloud today. You also have R&D in the US and manufacturing in three regions. Our platform is multi-cloud native — you retain your data in your own Azure Blob storage (Bring Your Own Storage), and you are never trapped on a single cloud. Every competitor in this RFP locks you in tighter than we do.

3. **Power BI partnership, not an afterthought.** Power BI integration is your non-negotiable requirement. We hold a certified Power BI partnership with a dedicated DirectQuery adapter and native connector. We do not bolt on Power BI — we build for it.

Our commercial proposal opens at **$561,600 per year** (22% off list) for a 3-year committed term, with a 2-year renewal option at a capped escalator. Implementation begins within 60 days of contract signature, with production go-live in 16 weeks.

---

# 1. Technical Proposal

## 1.1 Architecture Overview

The BTS-Synthetic platform delivers a **cloud-native lakehouse architecture** aligned to your stated preferences:

- **Open file formats throughout:** Delta Lake, Apache Iceberg, and Parquet are natively supported. Your data is stored in open formats in your own Azure Blob Storage account — you own your data, and it is portable to any future platform.
- **Unified batch and streaming:** A single architectural tier handles your real-time IoT ingest (tested and certified to 250,000 events per second — more than 3x your stated 80,000 peak) and your 30+ batch ETL sources, with no architectural seam between them.
- **Separation of storage and compute:** Compute scales independently of storage, eliminating the capacity planning overhead that plagues legacy warehouses (including your outgoing Teradata estate).

## 1.2 Workload Coverage

### Real-Time IoT Ingest
- **Native streaming ingest** via built-in connectors for MQTT, Kafka, Azure Event Hubs, and IoT Hub
- Certified throughput: **250,000 events/second** — more than 3× your stated 80,000 peak
- Micro-batch delivery to Delta tables with sub-second latency SLA (standard tier)
- Schema evolution handled automatically; no pipeline restarts required on device firmware updates

### Batch ETL
- **80+ pre-built connectors** including Teradata (direct migration path from your legacy estate), SAP, SQL Server, Oracle, and all major Azure data services
- Visual low-code pipeline designer; Python/Scala/R notebooks for data engineers
- Full incremental load support; CDC (Change Data Capture) from Teradata requires no custom development

### BI and Reporting (600 Analysts)
- **Certified Power BI DirectQuery adapter** — your analysts work in Power BI today and continue to do so after cutover, with no retraining
- Native semantic layer (business-friendly metric definitions, centrally governed) eliminates report proliferation from siloed analyst SQL
- Row-level and column-level security enforced at the platform layer — analyst access is governed without per-report security setup

### Self-Service Data Preparation (150 Data Engineers)
- Notebooks in Python, R, and Scala with integrated version control (Azure DevOps / GitHub)
- Low-code data prep UI for non-engineering analysts
- Shared compute pools with resource isolation between teams

### Machine Learning (Predictive Maintenance — Planned)
- **Full MLOps stack in-platform:** feature store, model registry, A/B deployment, native serving
- Pre-built accelerators for IoT sensor anomaly detection and predictive maintenance use cases
- No separate ML platform required; models train against the same Delta tables used by your BI tier

## 1.3 Scale

| Metric | Acme Requirement | BTS-Synthetic Capacity |
|--------|-----------------|----------------------|
| Current data volume | 280 TB | Unlimited (object storage) |
| Monthly growth | 12 TB/month | Scales automatically |
| Peak ingest | 80,000 events/sec | 250,000 events/sec (certified) |
| BI users (Power BI) | 600 analysts | Governed multi-tenancy, no per-seat compute limit |

## 1.4 Capabilities Matrix

| Capability | Status | Notes |
|-----------|--------|-------|
| Native Power BI integration | ✅ Full | Certified DirectQuery adapter; most mature BI integration in our portfolio |
| Multi-region deployment (EU primary, US East secondary) | ✅ Full | Active-active multi-region on Azure supported |
| EU data residency enforcement | ✅ Full | Per-table residency pinning; EU customer data never leaves EU region |
| Lakehouse architecture | ✅ Full | Native; not a bolt-on |
| Open file formats (Parquet, Delta, Iceberg) | ✅ Full | All three natively read/write |
| GDPR compliance | ✅ Full | DPA available; ISO 27001 + SOC 2 Type II certified |
| Azure deployment | ✅ Full | Azure Blob backend; deployable in Acme's own Azure tenant |
| Real-time ingest at scale | ✅ Full | 3× headroom above stated peak |
| Batch ETL (30+ sources incl. Teradata) | ✅ Full | 80+ connectors; Teradata migration tooling included |
| ML/MLOps pipelines | ✅ Full | Full stack: feature store, registry, serving |
| 99.99% monthly uptime | ⚠️ Add-on | Standard Enterprise tier: 99.95%. 99.99% available as Multi-Region Active-Active add-on ($95,000/year); see §3 Commercial |

## 1.5 Teradata Migration Path

Your legacy Teradata estate is being decommissioned through 2027. BTS-Synthetic provides:
- **Automated schema translation** from Teradata DDL to Delta tables
- **SQL dialect conversion** for Teradata-specific SQL (BTEQ, TDMS) to ANSI SQL
- **Parallel running support** — dual-feed for critical workloads during cutover
- **Migration assessment workshop** (complimentary, week 2 of the implementation): we map every Teradata table and pipeline to its equivalent on BTS-Synthetic before any cutover begins

---

# 2. Commercial Proposal

## 2.1 Pricing Summary — 5-Year Horizon

| Year | Annual Fee | Notes |
|------|-----------|-------|
| Year 1 | $561,600 | 22% off $720,000 list; Enterprise tier |
| Year 2 | $561,600 | Fixed (same as Year 1) |
| Year 3 | $561,600 | Fixed (same as Year 1) |
| Year 4 | $584,064 | Renewal year; CPI+2% escalator, capped at 5% |
| Year 5 | $607,426 | Renewal year; CPI+2% escalator, capped at 5% |
| **5-Year Total** | **$2,876,290** | Base platform |
| Multi-Region Active-Active Add-On (optional) | +$95,000/year | Required for 99.99% SLA commitment |

**Enterprise Tier base includes:**
- Full platform access (streaming, batch, BI, ML, data prep)
- Multi-region deployment (EU primary + US East secondary)
- EU data residency enforcement
- Dedicated Customer Success Manager
- 99.95% monthly uptime SLA (standard Enterprise)
- SOC 2 Type II + ISO 27001 audit reports on request
- 80+ connectors including Teradata migration tooling

## 2.2 Term and Renewal

- **Initial term:** 3 years from contract effective date
- **Renewal option:** 2-year renewal at Acme's election; written notice required 90 days prior to expiry
- **Renewal pricing:** Year 1–3 price + CPI+2% escalator, capped at 5% per year for renewal years (Years 4–5)

## 2.3 Payment Terms

- Annual fees billed in advance
- Payment due **Net 60** from invoice date (subject to credit verification)
- Alternative: **Quarterly billing** available at no additional charge — reduces each payment to approximately $140,400 per quarter, with Net 30 payment terms per quarter

## 2.4 Our Position on Key Commercial Terms

| RFP Requirement | BTS-Synthetic Position |
|----------------|----------------------|
| 35% discount off list | We offer **22% off list** at opening ($561,600/year). Maximum concession to 25% ($540,000/year) requires VP Sales sign-off. The RFP's 35% demand exceeds the maximum our enterprise discount band permits at this contract value. |
| Net 90 payment | **Net 60** maximum (subject to credit verification). Quarterly billing available as an alternative to ease cash flow. |
| 5-year fully fixed pricing | **Years 1–3 fixed.** Years 4–5 renewal carry a CPI+2% escalator capped at 5% per year. A fully frozen 5-year price is not available at this discount level. |
| Most Favoured Nation clause | **Not accepted.** We offer a **Price Stability Commitment**: your contracted rate will not increase during the initial 3-year term, and the renewal escalator is capped. We do not extend MFN clauses to any customer as they create contractual obligations across our entire customer base. |
| Termination for convenience, 30-day notice | We accept termination for convenience. **Notice period: 90 days** (industry standard for enterprise infrastructure with data migration implications). Upon termination, prepaid fees are refunded on a pro-rata basis for the remainder of the terminated contract year. No termination penalty. |

## 2.5 Deal Sweeteners (Included in Proposal)

- **30-day acceptance testing period** before Year 1 billing commences
- **PoC fee credit:** if Acme runs a pre-signature proof of concept, 100% of PoC fees credited to Year 1 invoice
- **Teradata migration tooling** included at no additional charge (estimated $45,000–$80,000 market value for equivalent professional services)
- **Dedicated CSM** included in Enterprise tier (no additional charge)
- **Year-end volume true-up** with 10% buffer — minor overages in Year 1 absorbed without additional billing

---

# 3. Contractual Positions

Acme's RFP contains several contractual requirements that differ from our standard terms. We address each directly below. These positions are our opening negotiation stance; we are prepared to engage legal counsel on all items.

| Clause | Acme RFP Position | BTS-Synthetic Counter-Position |
|--------|------------------|-------------------------------|
| §4.1 Liability | Uncapped liability for all data breach costs including regulatory fines and reputational damages | Aggregate liability capped at 24 months of fees. Notification costs and directly attributable regulatory fines are within-cap. Reputational damages excluded. Gross negligence / wilful misconduct carve-outs apply. |
| §4.2 Audit | Unannounced audits, up to 4x/year, at vendor cost | 1 scheduled audit per year (30 days' notice); up to 2 additional audits per year at customer cost. No unannounced audits. Scope limited to controls relevant to the services. |
| §4.3 SLA | 99.99% uptime; any failure entitles immediate termination with full month fee refund | Standard tier: **99.95% uptime**. 99.99% available via Multi-Region Active-Active add-on. SLA remedy: service credits (10–30% of monthly fee). Termination for persistent failure only (3 consecutive months below 99.0%), with 30-day cure period. |
| §4.4 IP | All work product vests in Acme on creation | Acme-specific custom deliverables licensed exclusively to Acme (perpetual, royalty-free). Platform IP, generic configurations, and integration frameworks remain BTS-Synthetic property; Acme receives a broad irrevocable licence for internal use. |
| §4.5 Subprocessors | Prior written consent for every subprocessor; consent withheld at sole discretion | BTS-Synthetic maintains a public subprocessor register. 30-day notice before adding/replacing material subprocessors. Acme may object; if unresolved, Acme may exit on 30-day notice without penalty. No blanket prior consent requirement. |
| §3.4 MFN | Full-term MFN on pricing vs. any comparable customer | Not accepted. Price Stability Commitment offered instead (see §2.4). |
| §3.5 Termination for convenience | 30-day notice, no fees | Accepted in principle. Notice period: 90 days preferred; minimum 60 days. No termination fee or penalty. |

---

# 4. Implementation Plan

## 4.1 Phased Delivery

| Phase | Duration | Key Milestones |
|-------|----------|---------------|
| **Phase 0: Foundation** | Weeks 1–4 | Contract signature; environment provisioning on Azure; network connectivity; Teradata migration assessment workshop; security & compliance review |
| **Phase 1: Core Lakehouse** | Weeks 5–10 | EU data residency configuration; multi-region active-active (if purchased); initial batch ETL from top 10 Teradata tables; first Power BI semantic layer connection |
| **Phase 2: Real-Time + Full ETL** | Weeks 11–16 | IoT device onboarding (40,000 devices); 80,000 events/sec streaming pipeline; remaining 30+ batch ETL sources; data engineer self-service environment |
| **Phase 3: BI Rollout** | Weeks 17–20 | Power BI migration for 600 analysts; executive dashboards; governance policies and row/column security |
| **Phase 4: ML Foundation** | Weeks 21–24 | Feature store setup; predictive maintenance starter models; ML pipeline infrastructure |
| **Production Go-Live** | **Week 16** (core platform) | Streaming, batch ETL, and BI operational for production workloads |
| **Full Cutover** | **Week 20** | Complete Teradata decommission for migrated workloads |

## 4.2 Resource Commitment

**BTS-Synthetic provides:**
- Dedicated Implementation Lead (50% capacity, Weeks 1–24)
- Senior Data Engineer × 2 (full-time, Weeks 1–16)
- Solutions Architect (full-time, Weeks 1–8; advisory Weeks 9–24)
- Customer Success Manager (dedicated, ongoing post-go-live)
- Power BI specialist (full-time, Weeks 13–20)

**Acme Corp to provide:**
- Technical lead (Marcus Webb's team): architecture decisions and Teradata access
- Azure infrastructure access: Blob Storage account, Azure AD tenant, networking
- IoT device firmware team: 2-week availability for streaming connector testing (Phase 2)
- Power BI admin: 2-week availability for BI migration (Phase 3)

---

# 5. Customer References

We offer three customer references at comparable scale, Power BI integration depth, and Azure deployment:

| Customer | Profile | Highlights |
|----------|---------|-----------|
| **Globex Manufacturing** | $1.2B global manufacturer, 180 TB lakehouse, Azure-native, Power BI for 550 analysts | 3-year contract; live in 18 weeks; zero Teradata-to-BTS migration issues reported |
| **Initech Industrial Sensors** | IoT scale: 35,000 field devices, 65,000 events/second peak, EU data residency required | Real-time streaming operational in 10 weeks; GDPR audit passed within 3 months of go-live |
| **Stark Industries (Manufacturing Ops)** | $2.4B manufacturer, 5-year contract, multi-region EU+US, 600+ BI users | Reference available for joint call with Marcus Webb's team; CSO available for technical deep-dive |

Full reference contact details and permission to contact provided upon request, subject to NDA.

---

# 6. Why BTS-Synthetic Wins This Deal

## Against Microsoft Fabric
Fabric is already in your E5 tenant — we know that. But licensing cost is not total cost. Fabric's lakehouse and OneLake are 18 months old; you are being asked to migrate a critical 280 TB enterprise data estate to a platform with limited production track record at your scale. We have run this exact workload — 200 TB+, EU multi-region, 80K+ events/second — in regulated manufacturing environments for years. We also offer something Fabric cannot: **true multi-cloud portability**. Your data lives in your own Azure Blob buckets in open formats. The day your cloud strategy changes, you are not trapped.

## Against Databricks
Databricks is technically excellent for data scientists building ML pipelines. But Acme's evaluation gives 30% weight to functional fit and 20% to TCO — not to raw engineering sophistication. Databricks' consumption pricing at 280 TB scale and 80,000 events/second is unpredictable. Their Power BI story is "bring your own BI" — ours is "Power BI is native." We will deliver a 3-year TCO model comparing our all-inclusive Enterprise pricing against Databricks' compute ramp; the numbers speak for themselves.

## Against Snowflake
Snowflake is the safe, familiar choice for SQL-native analytics. It is not built for real-time IoT ingest at 80,000 events/second — their architecture is batch-first and they know it. Their answer is "Kafka → Snowflake," which is two moving parts you have to own and operate. Ours is a single, unified platform with native streaming. On cost, Snowflake's scale pricing is well-documented; at 280 TB+ active queries, you will discover this during POC.

---

# 7. Next Steps

We propose the following engagement to proceed to contract:

1. **Technical deep-dive** (2 hours): BTS-Synthetic solutions architect with Marcus Webb's team — IoT ingest architecture, Teradata migration approach, Power BI semantic layer design
2. **Commercial alignment call** (1 hour): BTS-Synthetic Account Executive with Sarah Chen — address contractual term gaps (§4.1–§4.5), align on payment terms
3. **Proof of Concept** (optional, 3 weeks): Demonstrate real-time IoT ingest at 80K events/second against a sample of Acme's actual device data, with Power BI dashboard connected — at no charge against any eventual Year 1 contract
4. **Reference calls**: Arrange joint calls with Globex Manufacturing and Initech Industrial Sensors (your best comparables — similar scale, Azure, Power BI, EU)

**Response submitted to:** procurement@acme-synthetic.example
**BTS-Synthetic primary contact:** Deal Desk, BTS-Synthetic Enterprise Sales
**Proposal valid for:** 60 days from date of submission

---

*BTS-Synthetic — Turning data complexity into competitive advantage.*
