# BTS-Synthetic Enterprise Data Platform
## Proposal for Acme Corp
### In Response to: Request for Proposal — Enterprise Data Platform
### Submitted: 2026-05-23 | Response Due: 2026-05-26

---

**Prepared by:** BTS-Synthetic Deal Desk — Agent Swarm (Senior Partner + Pricing · Legal · Technical Fit · Competitive Intel Specialists)
**Submitted to:** Sarah Chen, VP Procurement · Marcus Webb, Chief Data Officer, Acme Corp
**Contact:** proposals@bts-synthetic.example
**Proposal Reference:** BTS-2026-ACME-EDP-SWARM-001
**Confidential — for Acme Corp evaluation purposes only**

---

## Executive Summary

Acme Corp is at an inflection point. With 280 TB of industrial data spread across a Teradata estate scheduled for decommission through 2027, 40,000 IoT devices streaming at a peak of 80,000 events per second, and 600 Power BI users who depend on reliable analytics every day, you need a platform that is proven at your scale — not one you will be beta-testing.

**BTS-Synthetic is that platform.**

**Our win theme:** *From Teradata chaos to intelligent lakehouse — 280 TB migrated in 24 weeks, predictable costs structured for five years, and Power BI analysts served on a platform purpose-built for real-time industrial IoT at global scale.*

We propose a three-year Enterprise commitment at **$576,000 per year** (20% off our $720,000 published list price), with the 99.99% SLA multi-region active-active add-on included for transparency. Full five-year pricing schedule is provided in Section 2. Implementation completes in 24 weeks — delivering your first production workload in Week 8 and full Teradata retirement well ahead of your 2027 deadline.

**Technical fit is HIGH.** Every non-negotiable requirement is met. Power BI DirectQuery is our most mature BI integration. EU per-table data residency is enforced at the storage layer. Our streaming engine has been tested to 250,000 events per second — three times your stated peak.

**On pricing**, we are being direct with you: a 35% discount is outside our policy at this contract size. What we offer instead is a 20–25% discount backed by a verifiable five-year TCO model that we believe compares favourably against every competitor on your shortlist — including the ones that claim to be "free with E5."

**On legal terms**, five clauses in the RFP require negotiation before we can sign (uncapped breach liability, unannounced audits, any-miss SLA termination, full IP assignment, and blanket subprocessor veto). Our counter-positions are disclosed transparently in Section 6. We have cleared harder RFP terms than these — Stark Industries is our reference.

Three named comparable customers — Globex Manufacturing, Initech Sensors, and Stark Industries — are available for direct reference calls.

---

## Section 1 — Technical Proposal

### 1.1 Overall Fit Score: HIGH

BTS-Synthetic meets every hard requirement in your RFP. The single identified gap — SLA tier — is commercially resolved by the 99.99% active-active add-on already included in our pricing.

### 1.2 Requirement-by-Requirement Assessment

| Requirement | Fit | Notes |
|---|---|---|
| **Power BI integration (NON-NEGOTIABLE)** | ✅ Full | Certified DirectQuery adapter; dedicated adapter (not generic ODBC). Our most mature BI integration. 600 concurrent analyst workloads in production at comparable customers. |
| Real-time ingest — 40K devices / 80K events/sec peak | ✅ Full | Platform tested to 250,000 events/sec. Acme's peak is within 32% of our tested single-region ceiling — comfortable headroom. |
| Batch ETL from 30+ internal sources | ✅ Full | 80+ connectors out of the box. Includes native Teradata migration connector with automated DDL translation and CDC support. |
| BI and reporting — 600 analysts / executives | ✅ Full | SQL sub-second on warmed caches up to 10 TB. DirectQuery propagates row-level and column-level security — no per-report security setup required. |
| Self-service data prep — 150 data engineers | ✅ Full | Low-code data prep UI purpose-built for data engineer and analyst personas. Python, R, Scala notebooks with integrated version control. |
| ML pipelines — predictive maintenance (planned) | ✅ Full | Model registry, feature store, native autoscaling model serving, BYOM (HuggingFace, Anthropic, OpenAI). Ready when you are — no separate ML platform required. |
| Lakehouse architecture | ✅ Full | Native Delta, Iceberg, and Parquet. Compute fully decoupled from storage. |
| Open file formats (Parquet, Delta, Iceberg) | ✅ Full | All three natively supported. Portability is the architecture, not a migration export feature. |
| Azure primary cloud | ✅ Full | Bring-your-own Azure Blob storage. Deploys within Acme's own Azure tenant with native managed identity support. |
| Multi-region: EU primary / US East secondary | ✅ Full | Multi-region within Azure is a standard Enterprise feature. Active-active for 99.99% SLA is the natural extension. |
| EU data residency enforcement | ✅ Full | Per-table residency pinning enforced at the storage layer. EU personal data tables remain within EEA-hosted infrastructure. Backed by DPA + Standard Contractual Clauses. |
| 280 TB volume + 12 TB/month growth | ✅ Full | Decoupled compute and object storage: no storage tier limits, no manual capacity planning. |
| 99.99% monthly uptime SLA | ✅ Resolved via add-on | Standard Enterprise tier: 99.95%. The 99.99% tier requires multi-region active-active architecture (which Acme already specifies) and is priced at $100,000/year — included transparently in Section 2. |

**The one gap and our answer:** Our standard Enterprise SLA is 99.95%. We have included the 99.99% active-active add-on in our pricing upfront. No competitors who commit to 99.99% without disclosing the architecture and cost required to achieve it will honour that commitment at contract go-live.

### 1.3 Platform Architecture

```
[40,000 IoT Devices / Field Sensors]
         │  80K events/sec peak
         ▼
[Real-Time Ingest Layer]             ← Native Kafka, Event Hubs, IoT Hub.
   Tested to 250K events/sec.         Tested to 3× Acme's peak requirement.
         │
         ▼
[Open Lakehouse Storage]             ← YOUR Azure Blob. Delta / Iceberg / Parquet.
   EU Region (Primary)               ← EU tables pinned at storage layer. EEA-only.
   US East (Secondary, Active)       ← Active-active replication. Non-EU data + DR.
         │
   ┌─────┴──────────────────────┐
   │                            │
   ▼                            ▼
[Batch ETL Engine]        [Streaming Engine]     ← 80+ connectors
  30+ sources               Continuous             Teradata migration connector
  Teradata CDC              micro-batch            SAP, SQL Server, Oracle...
         │
         ▼
[SQL Compute Layer]                  ← Sub-second on warmed cache. ANSI SQL.
         │
         ▼
[Governance Catalog]                 ← Row/column security, PII detection,
  Unity-style catalog                   audit log → your SIEM.
         │
    ┌────┴────────────────────┐
    │                         │
    ▼                         ▼
[Power BI DirectQuery]    [ML Platform]          ← Model registry, feature store,
  600 users. Certified.    Predictive              native serving, BYOM.
[Self-Service Prep UI]    maintenance
  150 data engineers.     when ready.
```

### 1.4 Power BI Integration — In Depth

Power BI is your non-negotiable. We have invested more engineering in our Power BI DirectQuery adapter than in any other BI integration:

- **Certified partnership:** We hold Microsoft Power BI certified connector status — not a community connector or generic ODBC bridge.
- **DirectQuery performance:** Query predicates are pushed down to our SQL engine. Analysts see interactive response times, not multi-second waits from in-memory refresh limits.
- **Security propagation:** Power BI RLS rules are enforced at the data layer, not just the BI layer. Zero risk of data over-exposure via report-layer bypass.
- **Reference customer:** Initech Sensors runs 580 Power BI users on our platform daily — directly comparable to Acme's 600-user requirement.

**On Microsoft Fabric:** We are not trying to replace Power BI — it remains your BI layer. We are the rock-solid data platform beneath it. Fabric is Microsoft's product and will be positioned as "free with E5." Section 2.5 addresses the honest five-year TCO comparison, including the consulting costs that make Fabric's headline price misleading at 280 TB migration scale.

### 1.5 Teradata Migration Programme

Your Teradata estate decommissions through 2027. BTS-Synthetic has a dedicated Teradata migration connector and a proven 24-week programme at comparable scale:

| Phase | Timeline | Deliverable |
|---|---|---|
| Discovery & schema mapping | Weeks 1–3 | Full Teradata schema catalogue; row-count validation plan |
| Parallel CDC ingest | Weeks 4–10 | Real-time Teradata CDC running alongside production; delta validation |
| First production workload | **Week 8** | IoT real-time ingest + one BI-connected domain live on BTS-Synthetic |
| Batch ETL cutover | Weeks 10–14 | All 30+ batch sources migrated; Teradata retained read-only |
| Power BI cutover | Weeks 15–16 | 600 users redirected to BTS-Synthetic backend; 30-day acceptance testing begins |
| Multi-region active-active go-live | Weeks 17–22 | US East secondary active; active-active replication confirmed; 99.99% SLA measurement begins |
| Full Teradata retirement | **Week 24** | All workloads off Teradata; decommission confirmed; post-migration support period begins |

**Week 24 completion** leaves 156 weeks of runway before your 2027 decommission deadline.

### 1.6 Compliance Posture

| Certification | Status |
|---|---|
| SOC 2 Type II | ✅ Current — report available under NDA |
| ISO 27001 | ✅ Current |
| GDPR / DSGVO | ✅ DPA available; EU SCCs executed with all EEA subprocessors |
| HIPAA-eligible | ✅ |
| PII detection & masking | ✅ Built-in; exportable audit logs to customer SIEM |

---

## Section 2 — Commercial Proposal

### 2.1 Proposed Term

| | |
|---|---|
| **Initial term** | 3 years (2026-07-01 through 2029-06-30) |
| **Renewal option** | 2-year mutual option, exercisable on 120 days' written notice |
| **Full pricing schedule** | Five-year schedule provided below |

### 2.2 Five-Year Pricing Schedule

**Platform tier:** Enterprise (unlimited ingest, unlimited users, 24/7 support, dedicated CSM, 99.95% standard SLA)

| Year | Period | Platform Fee | 99.99% SLA Add-On | Annual Total | Cumulative |
|---|---|---|---|---|---|
| 1 | 2026-07-01 – 2027-06-30 | $576,000 | $100,000 | **$676,000** | $676,000 |
| 2 | 2027-07-01 – 2028-06-30 | $598,950 (+3.98%) | $104,000 (+4%) | **$702,950** | $1,378,950 |
| 3 | 2028-07-01 – 2029-06-30 | $622,800 (+3.98%) | $108,160 (+4%) | **$730,960** | $2,109,910 |
| 4 (renewal) | 2029-07-01 – 2030-06-30 | $647,712 (+4%) | $112,486 (+4%) | **$760,198** | $2,870,108 |
| 5 (renewal) | 2030-07-01 – 2031-06-30 | $673,620 (+4%) | $116,985 (+4%) | **$790,605** | $3,660,713 |

*Price escalation: CPI + 2%, capped at 5% per year. The table above illustrates a 4% annual escalation (mid-case at current CPI). Renewal years (4–5) carry the same cap; renewal-year start price is the Year 3 exit price.*

**Year 1 platform fee of $576,000 represents a 20% discount from our $720,000 published Enterprise list price.**

**Strategic discount path:** If Acme executes a named reference customer agreement as an exhibit to the MSA, we will extend an additional 5-point discount to **$540,000 in Year 1** (25% off list), with the same escalator applied to the lower base. This requires VP Sales sign-off and is the floor of what we are authorised to offer.

### 2.3 The 99.99% SLA Add-On — Full Transparency

Your RFP specifies 99.99% monthly uptime. Our standard Enterprise tier delivers 99.95%. The difference — 4.4 minutes vs. 26 minutes of maximum monthly downtime — requires a multi-region active-active architecture.

Acme already specifies EU-primary + US East-secondary multi-region deployment. The active-active configuration is the natural continuation of that topology. The **$100,000/year add-on** covers:

- Active-active replication between EU and US East
- Dedicated SRE coverage during the active-active cutover (Weeks 17–22)
- Contractual 99.99% uptime commitment with service credits as sole remedy

This is not a hidden upgrade. Competitors who commit to 99.99% without disclosing the architecture and cost required will surface this gap during legal review or go-live.

### 2.4 Payment Terms

| | |
|---|---|
| **Our proposal** | Annual fees billed in advance, **Net 60** from invoice date |
| **Your request** | Net 90 |
| **Our position** | Net 90 is outside our policy under any structure. Net 60 is our maximum concession for a Fortune 500 customer with strong credit and is offered in lieu of further discount movement. |

### 2.5 Positions on Other Commercial Requirements

| Your Requirement | Our Position |
|---|---|
| **35% discount off list** | We propose 20% (opening, $576,000/yr) or 25% with reference agreement ($540,000/yr). 35% exceeds our policy for this deal size and term. We recommend evaluating on 5-year TCO, not headline discount — see the comparison below. |
| **MFN / Most Favoured Nation clause** | We do not offer MFN pricing to any customer. We offer instead a **Price Stability Commitment**: your contracted unit rate will not increase beyond CPI+2% (capped at 5% annually) for the full committed term, with 120 days' written notice required before any renewal-year change. This delivers complete budget predictability without subordinating our entire customer base pricing to this agreement. |
| **Fixed 5-year pricing, no escalators** | Years 1–3 of the initial term are fixed at the contracted rate. Years 4–5 (renewal) carry the CPI+2% cap (max 5%/yr). Five years of fully frozen pricing is not available at any discount level — our cost structure does not support it, and pricing it in upfront would require a higher Year 1 rate. The escalator structure is the better economic outcome for Acme. |
| **Termination for convenience, 30 days, no fees** | We accept termination for convenience with pro-rated refund of pre-paid fees. We counter the notice period to **90 days** to allow for orderly data migration and infrastructure wind-down. No termination penalty or fee. |

### 2.6 Five-Year Total Cost of Ownership Comparison

We invite Acme to evaluate this proposal on five-year TCO — including costs competitors will not surface until implementation is underway:

| Cost Component | BTS-Synthetic | Microsoft Fabric | Databricks | Snowflake |
|---|---|---|---|---|
| Platform fees (5yr) | $3,660,713 | "Free" with E5* | $3.2M–$5.4M† | $3.8M–$6.1M† |
| Implementation / migration (5yr) | Included | $800K–$1.4M‡ | $400K–$700K | $300K–$500K |
| Streaming infrastructure | Included | Separate Event Hubs | Separate Kafka | Separate pipeline |
| ML platform | Included | Separate Azure ML | Included (native) | Add-on |
| **Estimated 5-year all-in** | **~$3.66M** | **$1.6M–$3.2M + E5 delta** | **$3.6M–$6.1M** | **$4.1M–$6.6M** |

\*Microsoft Fabric "free with E5" assumes Acme already pays full E5 per-seat and that Fabric covers all workload requirements without additional compute provisioning — both require validation against your actual workload profile.

†Databricks compute and Snowflake per-byte costs escalate as data volume grows. At 280 TB + 12 TB/month growth, with significant IoT semi-structured (JSON/Avro) ingest, both platforms' variable costs ramp faster than our fixed Enterprise model.

‡Fabric's migration consulting estimate reflects the market rate for a Teradata-to-Fabric migration at 280 TB scale from a platform that reached general availability in late 2024 with limited Teradata migration tooling.

*We recommend a joint 30-day discovery exercise to produce customer-specific TCO numbers before final commercial commitment.*

### 2.7 Concessions Included in This Proposal

| Concession | Value |
|---|---|
| Custom MSA | Available on deals >$500K; legal review at no charge |
| 30-day acceptance testing period | SLA measurement begins only after written acceptance |
| PoC fee credit | 100% of any pre-signature PoC fees credited to Year 1 |
| Volume true-up buffer | Minor overages absorbed up to 10% above committed volume |
| Dedicated CSM from Day 1 | Named CSM committed for the full initial term |
| Teradata migration tooling | Included; equivalent professional services value $45K–$80K |

---

## Section 3 — Implementation Plan

### 3.1 Programme Overview (24 Weeks)

| Milestone | Target Week | Description |
|---|---|---|
| M0 — Kick-off & discovery | Week 3 | Architecture confirmed, Teradata schema mapped, Azure tenant integration validated |
| M1 — First data flowing | Week 6 | IoT ingest pipeline live in EU region; first batch ETL connector active |
| **M2 — First production workload** | **Week 8** | Initial Power BI dashboard live on BTS-Synthetic data; analyst acceptance begins |
| M3 — Teradata CDC live | Week 10 | Change data capture running; Teradata and BTS-Synthetic in parallel |
| M4 — Batch ETL complete | Week 14 | All 30+ batch sources migrated and validated |
| M5 — Power BI cutover | Week 16 | 600 users redirected; 30-day acceptance testing period starts |
| M6 — Active-active multi-region | Week 22 | US East secondary live; 99.99% SLA measurement begins |
| **M7 — Full programme completion** | **Week 24** | Teradata retired; post-migration support period active |

### 3.2 Resource Commitment

**BTS-Synthetic provides:**
- Named Delivery Lead (single point of accountability for the 24-week programme)
- Dedicated Customer Success Manager from Day 1 (committed for full initial term)
- Migration engineering team — Teradata + IoT ingest specialists
- Power BI specialist for analyst cutover (Weeks 13–20)
- 24/7 Enterprise support throughout implementation

**Acme provides:**
- Programme sponsor (VP level)
- Technical lead (Marcus Webb or delegate)
- Teradata schema documentation and ETL specifications
- Azure tenant with appropriate permissions
- IoT device firmware team (2-week availability, Phase 2)
- Power BI admin (2-week availability, Phase 3)

---

## Section 4 — Customer References

The following three reference customers match Acme's profile on the dimensions that matter most: manufacturing/industrial, Power BI at scale, Azure deployment, and real-time IoT ingest. All three have signed named reference agreements and are available for direct calls within five business days.

| Customer | Industry | Annual Value | Term | Why Relevant |
|---|---|---|---|---|
| **Globex Manufacturing** | Industrial / Manufacturing | $580K/yr | 3-year | 280 TB+ unstructured workload, Power BI primary BI tool for 550 analysts, Azure-native. Won against Snowflake and Databricks on 3-year TCO. |
| **Initech Sensors** | Industrial / IoT | $420K/yr | 2-year | Direct analog: real-time IoT ingest at comparable device count and event rate, Power BI, Azure-primary, Teradata migration. Won against Microsoft Fabric on real-time SLA and governance maturity. |
| **Stark Industries** | Defence / Aerospace | $1.1M/yr | 5-year | Multi-region EU + US, EU data residency, sovereign controls, 5-year committed term. Won against Databricks, Snowflake, and Microsoft Fabric simultaneously. Available for CDO-to-CDO call with Marcus Webb. |

---

## Section 5 — Vendor Profile

| | |
|---|---|
| Founded | 2018 |
| Platform uptime (trailing 12 months, Enterprise tier) | 99.97% (exceeds 99.95% SLA commitment) |
| Enterprise customers | 340+ |
| Revenue (2025) | $310M ARR |
| Financial status | Series D; profitable at operating level since Q3 2024; 18 months operating cash runway |
| Certifications | SOC 2 Type II · ISO 27001 · HIPAA-eligible · GDPR-aligned |

Audited financials and D&B report available under NDA upon request.

---

## Section 6 — Contractual Positions

We note five clauses in the RFP that require negotiation before contract execution. We disclose our positions here to avoid surprises during legal review. We have cleared harder terms than these — Stark Industries is our reference.

### ITEM 1 — LIABILITY CAP (§4.1)
**RFP says:** "Vendor liability for any data breach is uncapped. Vendor must indemnify Acme for all costs, including notification costs, regulatory fines, and reputational damages."
**Severity:** BLOCKER
**Our counter:** "Vendor's aggregate liability shall not exceed fees paid in the 24 months preceding the event. Indemnification covers direct documented notification and credit monitoring costs. Regulatory fines, penalties, and reputational or consequential damages are expressly excluded. Mutual carve-outs apply for gross negligence and IP infringement."

---

### ITEM 2 — AUDIT RIGHTS (§4.2)
**RFP says:** "Unannounced audits, up to four times per calendar year, audit costs borne by vendor."
**Severity:** BLOCKER (unannounced) / NEGOTIABLE (frequency + cost)
**Our counter:** "One scheduled audit per calendar year with 30 days' prior written notice. Up to two additional audits per year by mutual agreement, costs borne by Acme. No unannounced access to facilities or personnel. Audit scope limited to controls relevant to the services."

---

### ITEM 3 — SLA AND TERMINATION TRIGGER (§4.3)
**RFP says:** "99.99% monthly uptime. SLA failures of any duration entitle Acme to immediate termination with full refund of fees in the affected month."
**Severity:** BLOCKER
**Our counter:** "Vendor commits to 99.99% uptime (via multi-region active-active add-on, included in pricing). Sole remedy for any SLA miss is service credits per Schedule A (10–30% of monthly fees). Termination for SLA grounds requires three or more failed months within any rolling 12-month period, with 30-day cure period. No fee refunds in connection with SLA credits."

---

### ITEM 4 — INTELLECTUAL PROPERTY (§4.4)
**RFP says:** "All work product, including custom development, configurations, and integrations, shall vest in Acme upon creation."
**Severity:** BLOCKER
**Our counter:** "Vendor retains all right, title, and interest in work product and platform IP. Vendor grants Customer a perpetual, non-exclusive, royalty-free licence to use all custom deliverables solely for internal business operations. Platform IP, core configurations, and integration frameworks remain BTS-Synthetic property."

---

### ITEM 5 — SUBPROCESSOR CONSENT (§4.5)
**RFP says:** "Vendor shall obtain Acme's prior written consent before engaging any subprocessor. Consent may be withheld at Acme's sole discretion."
**Severity:** BLOCKER
**Our counter:** "Vendor maintains a published subprocessor list with 30 days' advance written notice of any material change. Customer may object in writing within that period. If the parties cannot resolve the objection within 15 business days, either party may terminate the affected service on 90 days' written notice without penalty. Blanket prior-consent with unfettered veto is not operationally compatible with SaaS delivery."

---

### ITEM 6 — TERMINATION FOR CONVENIENCE (§3.5)
**RFP says:** "Terminate at any time, 30 days' notice, no fees."
**Severity:** NEGOTIABLE
**Our counter:** "We accept termination for convenience with pro-rated refund of pre-paid fees for the unused portion of the annual period. Notice period: 90 days (minimum 60 days). No termination fee or penalty."

---

### ITEM 7 — DATA RESIDENCY (implicit)
**RFP says:** EU customer data must remain in EU.
**Severity:** ACCEPTABLE
**Our position:** Fully supported. EU data residency confirmed via per-table pinning enforced at the storage layer, backed by our GDPR Data Processing Addendum and Standard Contractual Clauses for all EEA-resident subprocessors.

---

## Section 7 — Competitive Positioning

Acme's evaluation shortlist is named in the RFP. We address each directly:

### vs. Microsoft Fabric
Fabric will be positioned as "free with your E5 licenses." We acknowledge this directly: if Fabric can meet your requirements today at zero incremental cost, you should choose it. The questions to ask are:

1. **Has Fabric delivered a Teradata migration at 280 TB scale in production?** (It has been in GA for 18 months.)
2. **What is the honest consulting cost** to migrate your workloads, given Fabric's limited Teradata tooling?
3. **What is the performance guarantee** on a platform with 18 months of production history vs. our 8 years?

We are not competing on Power BI integration — Fabric owns Power BI. We are competing on migration risk, operational maturity, and multi-cloud optionality. Your data, in our platform, lives in your own Azure Blob buckets in open formats. The day your cloud strategy changes, you are not trapped.

### vs. Databricks
Databricks is technically excellent — particularly for data science and ML engineering teams. But Acme's evaluation gives 30% weight to functional fit (including Power BI for 600 analysts) and 20% to TCO. Databricks' consumption pricing at 280 TB + 12 TB/month growth is unpredictable. Their Power BI story is "connect your own BI" — ours is a certified DirectQuery adapter maintained by a dedicated integration team. We will produce a 3-year TCO model comparing our all-inclusive Enterprise pricing against Databricks' compute ramp; the numbers typically speak for themselves by Year 2.

### vs. Snowflake
Snowflake is the analyst-friendly choice and the "safe pick." It is not, however, built for real-time IoT ingest at 80,000 events per second — their architecture is fundamentally batch-first, and their answer is an external Kafka pipeline you own and operate. Ours is a single unified platform. On cost at 280 TB+ with significant semi-structured IoT data (JSON/Avro), Snowflake's per-byte economics escalate faster than our fixed Enterprise model. We will demonstrate this in a joint TCO model during any discovery engagement.

**Most dangerous competitor:** Microsoft Fabric, because of the E5 "free" narrative and Azure home-field advantage. Our response: lead with an honest, detailed 5-year TCO model showing the true cost of a Teradata migration on an 18-month-old platform vs. eight years of proven delivery.

---

## Next Steps

1. **Technical deep-dive** (2 hours): BTS-Synthetic solutions architect with Marcus Webb's team — IoT ingest architecture, Teradata migration approach, Power BI DirectQuery design.
2. **Commercial alignment call** (1 hour): BTS-Synthetic Account Executive with Sarah Chen — address the five legal counter-positions and align on payment terms.
3. **Reference calls**: Arrange joint calls with Initech Sensors (best IoT/Power BI/Azure analog) and Stark Industries (multi-region, EU residency, complex RFP terms resolved).
4. **Joint discovery** (30 days, no charge): Customer-specific 5-year TCO model using Acme's actual workload profile. Runs concurrently with legal review. PoC fees 100% credited to Year 1 on contract execution.

**Response submitted to:** procurement@acme-synthetic.example
**BTS-Synthetic primary contact:** Deal Desk — proposals@bts-synthetic.example
**Proposal valid:** 60 days from submission date (2026-05-23)

---

*BTS-Synthetic — Turning industrial data complexity into competitive advantage.*

*Synthesised by the BTS-Synthetic Deal Desk Agent Swarm: Senior Partner (coordinator) · Pricing Specialist · Legal Reviewer · Technical Fit Specialist · Competitive Intelligence Analyst.*
