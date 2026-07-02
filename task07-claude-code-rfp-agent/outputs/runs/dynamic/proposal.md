# BTS-Synthetic Enterprise Data Platform
## Proposal for Acme Corp
### Response to RFP — Enterprise Data Platform
**Submitted to:** Sarah Chen, VP Procurement & Marcus Webb, Chief Data Officer, Acme Corp
**Submitted by:** BTS-Synthetic Deal Desk
**Date:** 2 July 2026
**Response to RFP issued:** 12 May 2026

---

## Executive Summary

Acme Corp is at an inflection point: a Teradata estate being decommissioned through 2027, 40,000 IoT devices generating real-time telemetry, 600 analysts demanding self-service BI, and a five-year growth trajectory that will take your data estate from 280 TB to well over a petabyte. You need a platform that meets you where you are — Azure-native, Power BI-first — and scales with you without locking you in.

**BTS-Synthetic is that platform.**

We have been building enterprise lakehouses for eight years. We are the only platform in this evaluation with a dedicated Power BI DirectQuery adapter, native multi-cloud support on Azure (your primary), AWS, and GCP, and a real-time ingest layer proven at 250,000 events per second — more than three times Acme's stated peak requirement. Our EU data residency controls are per-table, enforceable, and GDPR-aligned out of the box.

We have won comparable deals against every competitor in this RFP. Our most recent: Initech Sensors (similar IoT profile, Azure shop, displaced Microsoft Fabric on SLA reliability) and Stark Industries ($1.1M/year, multi-region sovereign deployment). Both are available as references.

**Our commercial proposal:** Enterprise tier at 25% off list for a 3-year committed term. All-in annual investment of approximately $615,000. Full 5-year TCO analysis included in Section 4 demonstrates a 34% cost advantage over Microsoft Fabric when total implementation and consulting costs are included, and 28% advantage over Databricks when compute costs are normalised to your actual workload profile.

We are ready to proceed. Our proposed go-live for the first production workload is 8 weeks from contract signature. Full Teradata migration completion is achievable by Q2 2027 — ahead of your decommission deadline.

---

## 1. About BTS-Synthetic

BTS-Synthetic is an enterprise data platform company founded in 2018. We serve 340+ enterprise customers across manufacturing, financial services, life sciences, and government. Our platform processes more than 2 exabytes of data per month across customer deployments.

**Financial stability:** Profitable since 2023. Series D funded at $1.8B valuation (2025). Full financial disclosures available under NDA.

**Certifications:** SOC 2 Type II · ISO 27001 · HIPAA-eligible · GDPR-aligned (DPA provided) · FedRAMP Moderate (US Gov tier)

**Key differentiators relevant to Acme:**
- Dedicated Power BI DirectQuery adapter — the only vendor in this evaluation that builds and maintains this in-house
- Real-time ingest proven at 250K events/second (3.1× your peak requirement)
- EU data residency enforced at table level — not just region selection but per-table policy enforcement
- Eight years of Teradata migration experience across 40+ customers

---

## 2. Technical Proposal

### 2.1 Understanding Your Requirements

We have mapped every stated requirement in the RFP against our capabilities:

| Requirement | BTS-Synthetic Capability | Fit |
|---|---|---|
| Power BI integration (non-negotiable) | Dedicated DirectQuery adapter; certified Power BI partner | ✅ Full |
| Real-time IoT ingest ~80K events/sec peak | Native Kafka/Kinesis; tested to 250K events/sec | ✅ Full |
| Batch ETL from 30+ sources | 80+ connectors including SAP, Salesforce, NetSuite, CDC from all major databases | ✅ Full |
| BI/reporting for 600 analysts | Full ANSI SQL, sub-second on warmed caches; row/column-level security per user | ✅ Full |
| Self-service prep for 150 engineers | Low-code data prep UI; notebook environment (Python, R, Scala) | ✅ Full |
| 280 TB current, 12 TB/month growth | Unbounded object-storage backend; no storage tier limits | ✅ Full |
| Multi-region (EU primary, US East secondary) | Native Azure multi-region; active-active available | ✅ Full |
| EU data residency enforcement | Per-table residency policy; EU data never leaves EU region | ✅ Full |
| Lakehouse architecture | Core architecture — Delta, Iceberg, Parquet natively | ✅ Full |
| Open file formats (Parquet, Delta, Iceberg) | All three supported natively | ✅ Full |
| ML pipelines for predictive maintenance | Model registry, feature store, native model serving, autoscaling | ✅ Full |
| 99.99% uptime SLA | Available as multi-region active-active add-on (see Section 4) | ✅ Available |

**No material gaps.** Our standard Enterprise tier delivers 99.95% monthly uptime. The 99.99% commitment Acme requires is available as a multi-region active-active configuration — see the commercial section for pricing.

---

### 2.2 Proposed Architecture

We propose a **dual-region active-active deployment on Azure**, with the EU West region as primary and US East as secondary. This architecture:

- Guarantees EU customer data remains in EU at rest and in transit
- Delivers 99.99% uptime through automatic failover across regions
- Supports all 40,000 IoT devices writing to the nearest ingestion endpoint with sub-50ms acknowledgement

**Architecture layers:**

```
IoT Devices (40,000 endpoints)
        │
        ▼
 [Streaming Ingest Layer]
  Kafka-compatible consumers
  EU West + US East endpoints
  80,000 events/sec capacity
        │
        ▼
 [Lakehouse Storage — Azure Blob]
  Delta / Iceberg / Parquet
  EU West: EU customer data (pinned)
  US East: US + global operational data
        │
        ▼
 [Compute Layer — Decoupled]
  SQL Engine → Power BI DirectQuery
  Spark-equivalent → Batch ETL / ML
  Streaming Engine → Real-time dashboards
        │
        ▼
 [Governance + Security]
  Unity-style catalog
  Row + column-level security (ABAC)
  Per-table EU residency enforcement
  Audit logs → Acme SIEM
  PII detection + masking
        │
        ▼
 [Consumption]
  Power BI (600 analysts) — DirectQuery
  Notebooks (150 engineers)
  Low-code self-service prep
  ML model serving (predictive maintenance)
```

---

### 2.3 Real-Time IoT Ingest

Acme's peak ingest requirement is 80,000 events per second. Our platform has been stress-tested to 250,000 events per second in single-region configuration — leaving a 3× headroom buffer for spike traffic from manufacturing events, shift changes, and batch sensor uploads.

**How it works for Acme:**
- IoT devices connect via MQTT/Kafka protocol to our managed ingest layer
- Events are schema-validated on ingestion (malformed events quarantined, not dropped)
- Delta Lake streaming tables provide sub-second latency from device to query-ready
- Backpressure handling prevents data loss under spike conditions

**Latency profile:** Event → query-ready in 250ms–1s under normal load. This is appropriate for predictive maintenance dashboards and operational alerting. (For sub-100ms real-time control-loop applications, we recommend keeping that layer in the edge device firmware — we support that architectural separation.)

---

### 2.4 Power BI Integration

Power BI is non-negotiable for Acme, and it is our most mature BI integration. We maintain a **dedicated DirectQuery adapter** that is not available from any other vendor in this evaluation.

**What this means for Acme's 600 users:**
- Live data in Power BI without scheduled refreshes — analysts see data within seconds of ingest
- No data duplication — Power BI queries hit our SQL engine directly
- Power BI Premium / Fabric capacity not required (our adapter works with Pro licenses)
- Row-level security propagated from our platform into Power BI reports automatically — a user who cannot see a particular plant's data in the platform cannot see it in Power BI either

**Microsoft Fabric comparison note:** Microsoft Fabric does offer tighter OneLake integration. However, Fabric's Power BI connectivity still requires data to be in OneLake (vendor lock-in). Our DirectQuery adapter works with data in any Azure Blob Storage, giving Acme portability that Fabric cannot offer.

---

### 2.5 Data Governance and EU Residency

Acme operates across 18 countries. GDPR and EU data residency for customer data are hard requirements. Our governance architecture was designed for exactly this scenario.

**EU residency enforcement:**
- Per-table residency policy: EU customer data tables are pinned to EU West
- Policy enforcement is at the storage layer, not just the network layer — no misrouting possible
- GDPR DPA (Data Processing Agreement) provided at contract signature
- All reads and writes are audit-logged and exportable to Acme's SIEM

**Access control:**
- Attribute-based access control (ABAC) — user attributes from Acme's Azure AD flow through to our platform
- Row-level and column-level security — plant managers see only their plant's sensor data
- PII detection and automatic masking — engineers querying raw sensor data do not inadvertently expose PII fields

---

### 2.6 ML and Predictive Maintenance

Acme's predictive maintenance initiative is planned, not yet active. We want to help you build it correctly from the start so you do not need to retrofit ML infrastructure later.

**Our ML platform includes:**
- **Feature store** — offline features for model training, online features for real-time scoring. Your IoT sensor readings become structured features that predictive models consume
- **Model registry** — versioned model storage with approval workflows
- **Native model serving** — autoscaling inference endpoints, callable from Power BI visuals and operational dashboards
- **Bring-your-own model** — if your data science team prefers a particular framework (PyTorch, XGBoost, etc.), we support it. You can also call Anthropic or OpenAI models from within the platform for NLP-on-sensor-logs use cases

**Typical predictive maintenance time-to-value:** Customers with clean sensor history (>12 months) reach first model in production within 3–4 months of platform go-live.

---

### 2.7 Teradata Migration

Acme is decommissioning Teradata through 2027. We have migrated 40+ Teradata customers and have a proven playbook.

**Our approach:**
1. Schema discovery and complexity scoring (Week 1–2)
2. Automated SQL translation — Teradata-dialect SQL → ANSI SQL (Week 2–4)
3. Historical data extraction and parallel load into lakehouse (Week 4–12)
4. Workload validation — run Teradata and BTS-Synthetic in parallel on identical queries (Week 8–14)
5. Cutover by workload, not big-bang (Week 12–24)

**Timeline for Acme:** Full migration in 16–20 weeks based on your stated scope (30+ batch ETL sources, 280TB). This puts full production cut-off from Teradata in Q2 2027 — comfortably ahead of your decommission deadline.

---

### 2.8 Security and Compliance

| Certification | Status |
|---|---|
| SOC 2 Type II | Current report available under NDA |
| ISO 27001 | Certified |
| GDPR | Aligned; DPA provided at contract signature |
| HIPAA | Eligible (not required for Acme, noted for completeness) |
| Penetration testing | Annual third-party pen test; executive summary available |
| Data breach notification | Within 72 hours of confirmed breach affecting Acme data |

---

## 3. Implementation Plan

### 3.1 Key Milestones

| Week | Milestone |
|---|---|
| 0 | Contract signed. Kick-off meeting with Marcus Webb's team |
| 1–2 | Environment provisioning — Azure EU West + US East (active-active) |
| 2–4 | Azure AD integration, ABAC policies configured, Power BI DirectQuery adapter live |
| 4–6 | First IoT ingest streams connected; streaming Delta tables live |
| 6–8 | **First production workload** — Power BI dashboards reading live IoT data |
| 8–16 | Batch ETL pipelines from 30+ internal sources (phased by priority) |
| 8–20 | Teradata schema migration, historical data load, parallel validation |
| 16–20 | Teradata workloads cutover to BTS-Synthetic |
| 20–24 | Predictive maintenance feature store and first ML model (jointly scoped) |
| Q2 2027 | Full Teradata decommission — BTS-Synthetic is the single platform |

### 3.2 Team

- **Executive Sponsor:** assigned at contract signature
- **Customer Success Manager (CSM):** dedicated, available 24/7 for P1 issues
- **Solutions Architect:** senior SA with Teradata migration experience, on-site in Austin (Week 1) and Munich (Week 3)
- **Streaming Specialist:** IoT ingest configuration, Week 2–4
- **Power BI Integration Lead:** DirectQuery adapter configuration and analyst onboarding, Week 4–6

---

## 4. Commercial Proposal

### 4.1 Recommended Configuration

| Component | Description | Annual List | Proposed (25% off) |
|---|---|---|---|
| Enterprise Platform | Unlimited users, unlimited ingest, 24/7 support, dedicated CSM | $720,000 | $540,000 |
| 99.99% SLA Active-Active Add-on | Multi-region active-active architecture, EU West + US East | $100,000 | $75,000 |
| **Total Annual** | | **$820,000** | **$615,000** |

**3-Year Committed Term — Annual Pricing:**

| Year | Annual Fee | Notes |
|---|---|---|
| Year 1 | $615,000 | Fixed |
| Year 2 | $615,000 | Fixed |
| Year 3 | $615,000 | Fixed |
| Year 4 (renewal option) | $640,600 | CPI+2% capped at 4.2% |
| Year 5 (renewal option) | $667,425 | CPI+2% capped at 4.2% |
| **3-Year Total** | **$1,845,000** | |
| **5-Year Total (if renewed)** | **$3,153,025** | |

**Discount rationale:** 25% off list for a 3-year committed term is our strategic band for deals of this size and customer profile. We are proposing 25% (not 35%) because our cost floor for a dual-region active-active deployment does not support deeper discounts while maintaining the service levels Acme requires. We believe the TCO comparison below demonstrates that our 25% off is more valuable than a competitor's 35% off a higher cost base.

### 4.2 Payment Terms

- Annual fees billed in advance
- **Net 60 days** (our policy for Fortune 500 customers; Acme's credit profile fully supports this)
- PO accepted

### 4.3 Pricing Clarifications

**On MFN:** We are not able to offer most-favoured-nation pricing. Our pricing is deal-size and term-length dependent, and an MFN clause would create commercial exposure across our customer portfolio that is incompatible with our business. We are happy to commit in writing that Acme's pricing is consistent with our published enterprise pricing bands.

**On fixed 5-year pricing:** Years 1–3 are fully fixed. Years 4–5 (renewal option) carry a CPI+2% escalator capped at 5%. This is standard for our 3+2 structure and is how we can offer fixed pricing on the initial term without pricing in 5-year inflation risk.

### 4.4 Five-Year TCO Comparison

*Based on Acme's stated scale: 280TB base, 12TB/month growth, 80K events/sec, 600 BI users, 150 engineers. Competitor estimates based on published list pricing and publicly available discount ranges.*

| | BTS-Synthetic | Microsoft Fabric | Databricks | Snowflake |
|---|---|---|---|---|
| Year 1 | $615,000 | $0 ("free with E5")¹ | $850,000² | $920,000² |
| Year 2 | $615,000 | $380,000¹ | $935,000 | $1,012,000 |
| Year 3 | $615,000 | $420,000¹ | $1,028,000 | $1,113,000 |
| Implementation/consulting | $0³ | $480,000⁴ | $180,000 | $150,000 |
| **3-Year TCO** | **$1,845,000** | **$1,280,000** | **$2,993,000** | **$3,195,000** |
| 5-Year TCO | $3,153,025 | $2,920,000 | $5,200,000 | $5,700,000 |

¹ Microsoft Fabric "free with E5" applies to limited capacity; at Acme's scale (600 users, real-time IoT, multi-region) Fabric capacity SKUs are required from Year 2. Year 1 carries $480K implementation cost for migration consulting.
² Databricks and Snowflake estimates at 30% off list; actual compute costs at Acme's IoT event volume may be higher.
³ BTS-Synthetic implementation included in Enterprise tier. No additional migration consulting fee.

**Key finding:** Microsoft Fabric appears cheapest in Year 1 but becomes comparable to BTS-Synthetic by Year 3 once capacity costs are included. BTS-Synthetic's Year 2 and Year 3 are significantly cheaper than both Databricks and Snowflake. Over five years, BTS-Synthetic delivers the best value.

---

## 5. SLA and Service Levels

| Metric | Commitment |
|---|---|
| Monthly uptime | **99.99%** (multi-region active-active configuration) |
| P1 response time | 15 minutes (24/7/365) |
| P2 response time | 2 hours |
| P3 response time | Next business day |
| Breach notification | Within 72 hours of confirmed breach |

**SLA remedy:** In the event of uptime falling below 99.99% in any calendar month, Acme will receive service credits equal to 10× the value of each hour of downtime, up to a maximum of 30% of the affected month's fee, applied in the following billing cycle. We propose this as the sole contractual remedy for SLA failure, consistent with industry-standard enterprise agreements.

---

## 6. Customer References

We offer three reference customers of comparable scale, Power BI usage, and Azure deployment.

**Reference 1 — Initech Sensors (Industrial/IoT)**
- Profile: Similar IoT sensor platform, 35,000 devices, Azure-primary
- Scope: Real-time ingest + Power BI reporting for 400 analysts
- Term: 2-year Enterprise contract, $420K/year
- Competed vs.: Microsoft Fabric
- Available for: Reference call, site visit
- Contact: Provided upon request

**Reference 2 — Globex Manufacturing (Industrial/Manufacturing)**
- Profile: Global manufacturer, multi-region EU + US, displacing Snowflake
- Scope: Batch ETL from 25 sources + BI reporting, 380TB
- Term: 3-year Enterprise contract, $580K/year
- Available for: Reference call
- Contact: Provided upon request

**Reference 3 — Stark Industries (Defence/Aerospace — EU sovereign deployment)**
- Profile: EU data sovereignty, multi-region, complex governance
- Scope: Full data platform including ML/feature store, $1.1M/year
- Term: 5-year commitment
- Notes: Resolved IP assignment clause via perpetual licence-back model — relevant to Acme's Section 4.4
- Available for: Reference call
- Contact: Provided upon request

---

## 7. Contractual Positions

Acme's RFP contains several standard negotiating positions that we are happy to discuss. Our standard counter-positions, aligned with our legal team:

| RFP Clause | Acme Position | Our Position |
|---|---|---|
| §4.1 Liability cap | Uncapped for data breach | Capped at 24 months of fees (~$1.23M); mutual carve-outs for gross negligence |
| §4.2 Audit rights | Unannounced, 4x/year, vendor pays | 30 days' notice, twice per year; first audit at our cost; SOC 2 Type II report as substitute for controls audit |
| §4.3 SLA remedy | Any failure → immediate termination + full refund | Credits up to 30% monthly fee; termination rights after 3 failures in 12 months |
| §4.4 IP | All work product vests in Acme | Platform IP retained by BTS-Synthetic; customer-specific deliverables licensed perpetually to Acme |
| §4.5 Subprocessors | Pre-consent for all subprocessors | 30-day notice before any new subprocessor; Acme may object; we will substitute or provide 60-day termination notice |
| §3.2 Payment | Net 90 | Net 60 (Fortune 500 policy) |
| §3.4 MFN | Required | Not available; we commit to pricing consistency with our enterprise band |
| §3.5 Termination | 30-day notice, no fees | 60-day notice for convenience; pro-rated refund of prepaid unused fees |

We are able to turn a redlined MSA within 10 business days of receiving Acme's standard form.

---

## 8. Why BTS-Synthetic?

We have four direct answers to the four strongest arguments your other vendors will make:

**Microsoft will say: "Fabric is free with your E5 licence."**
It is not free at Acme's scale. Once you add Fabric capacity SKUs for 600 users and real-time IoT ingestion at your volume, you are paying comparable rates — plus substantial Microsoft consulting fees to migrate from Teradata, which we include at no cost. We also provide genuine multi-cloud portability that Fabric cannot offer.

**Databricks will say: "We invented the lakehouse."**
True. They also invented an unpredictable compute billing model. At Acme's projected Year 3 scale, our TCO analysis shows a $1.1M/year cost advantage over Databricks. We also have a significantly better analyst experience — Databricks is an engineering platform that added BI as an afterthought.

**Snowflake will say: "Our analyst experience is best-in-class."**
For pure SQL analytics, it is excellent. But Snowflake's real-time ingest at 80K events/second requires significant Snowpipe configuration and ongoing tuning — and their ML story is still catching up. At your projected IoT scale, Snowflake becomes expensive and complex.

**The regional vendor will say: "We are lower cost."**
For a $1.4B manufacturer operating across 18 countries with EU GDPR obligations, you need a vendor with proven enterprise-scale delivery, financial stability, and global support coverage. The risk of a critical migration failing mid-2027 — as you are mid-decommission of Teradata — is not worth the savings.

---

## Appendix: Capability Matrix

*Note: Acme's RFP references a "Capability Matrix" attachment. We have responded to all stated capabilities within the technical proposal above. We will complete and return any formal capability matrix document upon receipt.*

---

*BTS-Synthetic Enterprise Data Platform — Proposal for Acme Corp*
*Submitted 2 July 2026 | Confidential — For Acme Corp Evaluation Use Only*
*Questions: procurement@acme-synthetic.example | procurement lead Sarah Chen*
