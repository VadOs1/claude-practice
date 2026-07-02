# BTS-Synthetic Enterprise Data Platform
## Proposal for Acme Corp — Enterprise Data Platform Modernisation

**Prepared by:** BTS-Synthetic Deal Desk
**Prepared for:** Sarah Chen, VP Procurement | Marcus Webb, Chief Data Officer
**Date:** 2026-05-23
**Response to RFP issued:** 2026-05-12
**Valid until:** 2026-07-23

---

## Executive Summary

Acme Corp is at a pivotal moment: 280 TB of production data spread across a Teradata estate being decommissioned through 2027, 40,000 IoT devices generating up to 80,000 events per second, 600 analysts demanding Power BI-native reporting, and manufacturing operations spanning 18 countries with strict EU data-residency obligations. A patchwork of on-premises systems cannot carry you forward.

BTS-Synthetic's Enterprise Data Platform is purpose-built for exactly this profile — and we have the references to prove it. Initech Sensors (comparable IoT ingest scale, Azure, Power BI, EU data residency) and Globex Manufacturing (280+ TB, Teradata migration, multi-region) are both referenceable and available for a call within two weeks.

**Our proposal delivers:**

- **Full functional fit** on every hard requirement: real-time IoT ingest validated to 3× your peak throughput, certified Power BI DirectQuery integration, EU-region data residency enforced at the storage layer, and a true lakehouse on open Delta/Iceberg/Parquet formats.
- **A 3-year commercial commitment at 28% off Enterprise list pricing**, with CPI-anchored annual adjustment capped at 5%, and a 2-year renewal option priced and locked at signing.
- **A 20-week migration programme** from Teradata to full production — with a 30-day acceptance period before Year 1 fees begin.
- **99.99% uptime SLA** via multi-region active-active configuration, included in our proposed pricing.

We proactively flag five contractual items that require negotiation before we can execute (§5). None are deal-breakers; all have signed precedents in our comparable enterprise contracts.

---

## 1. Technical Proposal

### 1.1 Architecture Overview

We propose deploying BTS-Synthetic's Enterprise Data Platform in a **lakehouse configuration on Azure**, with:

- **Primary region:** Azure West Europe (Amsterdam) — EU data residency anchor
- **Secondary region:** Azure East US 2 — US analytics and disaster recovery
- **Storage layer:** Azure Blob Storage (Acme-owned subscription), Delta Lake format
- **Compute layer:** Decoupled elastic compute in both regions, independently scalable
- **Governance layer:** Unity-style catalog with per-table residency tags pinning EU customer data to West Europe exclusively — enforced at the storage API layer, not just policy

This architecture keeps EU data in the EU, satisfies GDPR Article 46, and integrates natively into Acme's existing Azure tenant.

### 1.2 Workload Coverage

#### Real-Time IoT Ingest (80,000 events/second peak)

BTS-Synthetic's streaming ingest layer is built on Kafka-native consumers with auto-scaling compute. Our validated single-region throughput is **250,000 events/second** — 3× your stated peak. A dual-region active-active configuration provides additional headroom and failover capability without data loss.

Recommended topology:
- Azure Event Hubs (Kafka-compatible, Acme-owned) as the ingest broker
- BTS-Synthetic streaming connectors consume, transform, and land to Delta tables in West Europe
- 800ms–1.5s latency to queryable state for analytical dashboards

> **Transparency note:** Sub-100ms streaming query latency is not our strength — we hit 250ms–1s on streaming queries. For operational alerting requiring sub-100ms, we recommend a companion time-series layer (Azure Data Explorer integrates with our platform). We are happy to architect this hybrid approach at no additional platform cost.

#### Batch ETL (30+ Internal Sources including Teradata)

Our 80+ certified connectors include SAP (ECC and S/4HANA), Teradata (via Debezium-compatible CDC), common RDBMS (SQL Server, Oracle, PostgreSQL), and cloud sources. Acme's Teradata estate can be migrated in **parallel incremental waves** — no big-bang cutover — with automated reconciliation ensuring data parity before each wave is promoted to production. We have executed two comparable Teradata migrations (Globex Manufacturing and an undisclosed industrial customer) on this tooling.

#### BI and Reporting (600 Analysts + Executives)

Power BI is our most mature BI integration. Our **certified DirectQuery adapter** — not a generic JDBC bridge — delivers:
- Sub-second response on warmed query caches for report page loads
- Full semantic model compatibility (composite models, calculation groups, row-level security passthrough)
- No material rework required for existing Power BI reports or datasets

600 concurrent Power BI users is within our tested enterprise configuration. No changes to Acme's Power BI or Azure licensing are required.

#### Self-Service Data Preparation (150 Data Engineers)

Our low-code data prep UI supports analyst and engineer personas with visual pipeline builders, notebook interfaces (Python, SQL, Scala), and Git-backed pipeline versioning integrated with Azure DevOps.

#### Machine Learning Pipelines (Predictive Maintenance — Planned)

Model registry, feature store (offline + online serving), and native model serving with autoscaling are available today. When Acme's ML programme activates, no additional platform migration is required — the capability is already present. We can also integrate Azure ML workspaces if Acme's data science team has existing investments there.

### 1.3 Capability Matrix

| Acme Requirement | BTS-Synthetic Capability | Fit |
|---|---|---|
| Real-time ingest 80K events/s | Validated to 250K events/s | ✅ Full |
| Batch ETL 30+ sources | 80+ connectors incl. Teradata CDC, SAP | ✅ Full |
| Power BI integration (600 users) | Dedicated DirectQuery adapter, certified | ✅ Full |
| Multi-region EU primary / US East secondary | Azure West Europe + East US 2 | ✅ Full |
| EU data residency enforcement | Per-table residency pinned at storage API layer | ✅ Full |
| Lakehouse architecture | Native Delta/Iceberg/Parquet lakehouse | ✅ Full |
| Open file formats (Parquet, Delta, Iceberg) | All three natively supported | ✅ Full |
| ML pipelines (predictive maintenance) | Model registry, feature store, native serving | ✅ Full |
| 99.99% uptime SLA | Multi-region active-active add-on (included in price) | ✅ Full |
| 280 TB + 12 TB/month growth | Unlimited ingest/storage on Enterprise tier | ✅ Full |

### 1.4 Governance and Compliance

- **Data residency:** Per-table enforcement at the storage API layer. EU tables pinned to Azure West Europe. Automated drift detection alerts if policy is bypassed.
- **Security:** Row-level and column-level security with attribute-based access control. Native Azure Entra ID integration.
- **Audit logs:** Every read and write logged with immutable trail retained for 7 years, exportable to Acme's SIEM.
- **PII detection and masking** built-in — relevant for IoT device data containing location or operator identifiers.
- **Certifications:** SOC 2 Type II, ISO 27001, GDPR-aligned (DPA available and ready for signature), HIPAA-eligible.

---

## 2. Commercial Proposal

### 2.1 Proposed Configuration and Pricing

| Component | Annual List | Annual Net (28% discount) |
|---|---|---|
| Enterprise Platform License | $720,000 | $518,400 |
| 99.99% SLA Upgrade (multi-region active-active) | $100,000 | $72,000 |
| **Total** | **$820,000** | **$590,400** |

### 2.2 Five-Year Cost Schedule

| Year | Net Annual Fee | Notes |
|---|---|---|
| Year 1 | $590,400 | Billing starts after 30-day acceptance period |
| Year 2 | $602,208 | CPI + 2%, capped at 5% |
| Year 3 | $614,252 | CPI + 2%, capped at 5% |
| **3-Year Committed Total** | **$1,806,860** | |
| Year 4 (renewal) | $626,537 | Renewal pricing locked at signing |
| Year 5 (renewal) | $639,068 | CPI + 2%, capped at 5% |
| **5-Year Total (illustrative at 2% CPI)** | **$3,072,465** | |

*Annual escalation: CPI + 2%, capped at 5%/year, referencing EU HICP index published by Eurostat. All 5-year figures above assume 2% CPI — actual fees will be at or below these figures if inflation remains ≤3%.*

### 2.3 Implementation Services (Fixed-Scope, Fixed-Price)

| Item | Cost |
|---|---|
| 20-week migration programme | $185,000 |
| 30-day PoC (credited toward Year 1) | $0 net |

Professional services are fixed-scope and fixed-price. No T&M exposure for Acme.

### 2.4 Our Position on Acme's Commercial Requirements

| Acme Requirement | Our Position |
|---|---|
| **35% discount** | **Counter: 28%.** Our maximum strategic discount for a deal of this size, term, and profile. We have offered 28% to comparable manufacturing customers. Further reduction is not possible without removing the 99.99% SLA premium. |
| **5-year price lock, no escalators** | **Counter: 3-year lock + CPI+2% escalator (capped 5%).** A 5-year flat price on a $590K/year cloud contract is not commercially sustainable given infrastructure cost inflation. We commit the Year 1 net price for Years 1–3, with a fully transparent and capped escalator. Renewal-year pricing is locked at signing. |
| **Net 90 payment** | **Counter: Net 60.** We accept Net 60 for Fortune 500-equivalent enterprise customers. Our own cloud infrastructure billing cycles make Net 90 a binding constraint we cannot absorb. |
| **Most Favoured Nation (MFN)** | **We cannot accept MFN clauses** — this is a company-wide policy protecting all existing customer agreements. In lieu, we will contractually commit that Acme's pricing will not be increased by more than the stated escalator cap during the contracted term. |

### 2.5 Discount Basis and Reference Agreement

The 28% discount reflects:
1. 3-year committed term (5% uplift over standard)
2. Strategic account designation (manufacturing vertical, logo value for our reference programme)
3. Reference customer agreement — we ask Acme to permit BTS-Synthetic to reference Acme Corp by name and industry in sales materials after the first year of production. No financials disclosed.

---

## 3. Implementation Plan

### 3.1 Phased Migration (20 Weeks to Full Production)

| Phase | Weeks | Milestones |
|---|---|---|
| **Phase 0 — Discovery & Design** | 1–3 | Architecture sign-off, data cataloguing, security design, Azure integration blueprint |
| **Phase 1 — Foundation** | 4–7 | Platform provisioning (EU + US regions), network connectivity, Entra ID integration, governance catalog seeded with Teradata schema |
| **Phase 2 — Priority Workloads** | 8–13 | IoT ingest pipeline live, 3 highest-priority Teradata schemas migrated, Power BI connection validated with pilot (50 users); **first production workload** |
| **Phase 3 — Ramp & Cutover** | 14–19 | Remaining Teradata schemas migrated in waves, all 30+ batch sources connected, full 600-user Power BI rollout |
| **Phase 4 — Acceptance** | 20 + 30 days | Full production cutover, 30-day acceptance period, Year 1 billing begins post-acceptance |

**Buffer to Teradata decommission deadline (end-2027):** 18+ months. No schedule risk.

### 3.2 Migration Risk Controls

- **Parallel run:** Teradata and BTS-Synthetic run in parallel through Phases 2–3. Automated reconciliation checks ensure data parity before each wave is promoted.
- **Wave-based rollback:** Each migration wave is independently reversible. No Teradata schema is decommissioned until Acme's data team provides written sign-off.
- **Dedicated on-site support:** Migration engineer co-located with Acme's Austin R&D team during Phases 1–2.

### 3.3 Key Risks and Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Teradata schema complexity (18-country data, 30+ sources) | Medium | Schema-mapping workshop in Week 2; dedicated Teradata specialist |
| IoT device protocol heterogeneity | Medium | Pre-built adapters for top 5 industrial protocols; custom adapters scoped in Phase 0 |
| Power BI report rework (complex DAX) | Low | DirectQuery adapter preserves existing DAX; regression testing in Phase 3 |
| EU data residency audit failure | Low | Per-table enforcement at storage API layer, validated in PoC |

### 3.4 BTS-Synthetic Staffing Commitment

| Role | Commitment |
|---|---|
| Dedicated Customer Success Manager | Full-time, Year 1 onward |
| Lead Solutions Architect | Full-time, Weeks 1–20 |
| Teradata Migration Engineer | 50%, Weeks 8–20 |
| Streaming Infrastructure Engineer | 50%, Weeks 8–19 |
| Power BI Integration Specialist | 50%, Weeks 14–20 |

---

## 4. Competitive Context

Acme is evaluating Databricks, Snowflake, and Microsoft Fabric (§6 of the RFP). Our honest assessment:

### vs. Microsoft Fabric
Microsoft will pitch Fabric as "included with your E5 licences." The headline is compelling; the total cost is not free. Fabric has been generally available as a unified platform for approximately 18 months. At Acme's scale — 40,000 IoT devices, 280 TB, 18-country multi-region — you are taking on enterprise-scale operational risk on a maturing platform. We have been doing this for eight years. Our Power BI DirectQuery adapter has been in production at enterprise scale for five years; Fabric's native experience is tighter but the operational maturity is not comparable. We recommend a joint 3-year TCO workshop that includes Microsoft's consulting and integration cost estimates.

*Do not compete on Power BI integration feature parity — both platforms connect. Compete on operational maturity and TCO.*

### vs. Databricks
Databricks has a strong lakehouse and ML story — both are genuine. Our differentiation: BI and analyst-facing tooling (Power BI is first-class on our platform, second-class on Databricks), and predictable TCO (Databricks customers at Acme's scale frequently report compute cost surprises in Year 2 when interactive SQL workloads scale up). We will produce a 3-year TCO comparison at Acme's exact workload profile on request.

### vs. Snowflake
Snowflake's analyst SQL experience is best-in-class. At Acme's real-time IoT scale (80K events/second, Kafka ingest), Snowflake's architecture is a less natural fit — their streaming ingest carries meaningful additional compute cost at this volume. We ran a comparable workload comparison for Initech Sensors and won on 3-year TCO.

---

## 5. Contractual Positions

We proactively flag five items that require negotiation. All have signed precedents in our enterprise contracts.

### Item 1 — Liability Cap (§4.1) — **BLOCKER**
**RFP says:** Uncapped liability for data breach, including regulatory fines and reputational damages.
**Why it is a blocker:** Our cyber liability insurance (which covers Acme as a beneficiary) caps at 24 months of fees. Uncapped indemnification voids our coverage, leaving Acme with an uncollectable promise.
**Our counter:** Aggregate liability for data breach capped at 24 months of fees paid (~$1.18M at Year 1 rates), with mutual carve-outs for gross negligence and wilful misconduct. We will maintain $5M cyber liability insurance and provide certificates on request.

### Item 2 — Intellectual Property (§4.4) — **BLOCKER**
**RFP says:** All work product vests in Acme upon creation.
**Why it is a blocker:** Custom configurations and integrations share code with our core platform. Full assignment creates conflicting IP chains that threaten the platform for all customers.
**Our counter:** BTS-Synthetic retains all IP in the platform and pre-existing components. Customer-specific deliverables (configurations, custom integrations) are licensed to Acme on a **perpetual, royalty-free, exclusive basis** for Acme's use. Upon termination, Acme retains this licence. *(Precedent: Stark Industries contract, executed February 2026.)*

### Item 3 — Audit Rights (§4.2) — **BLOCKER on "without notice"**
**RFP says:** Audit without prior notice, up to four times per calendar year, at vendor cost.
**Our counter:** We accept up to two audits per calendar year with **30 days' written notice**. We bear cost of the first audit per year; customer bears cost of any additional. "Without notice" audit rights are incompatible with our SOC 2 programme. We will provide SOC 2 Type II and ISO 27001 reports in lieu of on-site audit for scope covered by those certifications.

### Item 4 — Service Levels (§4.3) — **BLOCKER on immediate-termination remedy**
**RFP says:** 99.99% monthly uptime; any SLA failure entitles Acme to terminate immediately with full fee refund.
**Our position on the 99.99% SLA target:** We can commit to 99.99% on the multi-region active-active configuration included in our pricing.
**Our counter on remedy:** SLA failures entitle Acme to **service credits up to 30% of the affected monthly fee**. Right to terminate for convenience arises after three consecutive months of SLA breach at >0.1% downtime. Immediate termination with full refund on a single outage is not commercially viable for any cloud provider — it creates a perverse incentive to over-report availability.

### Item 5 — Subprocessors (§4.5) — **BLOCKER**
**RFP says:** Prior written consent required for every new subprocessor; consent at Acme's sole discretion.
**Our counter:** We maintain a public subprocessor list (updated quarterly). We will notify Acme **30 days before** adding any new subprocessor that processes Acme data. Acme may raise objections within 14 days; we will either substitute or, if substitution is not feasible, offer Acme the right to terminate with 90 days' notice and pro-rated refund. Pre-approval at sole discretion is operationally unworkable for a cloud SaaS provider with 15+ infrastructure subprocessors.

### Items We Accept Without Negotiation

| Clause | Our Position |
|---|---|
| Termination for convenience (§3.5) | Accept with modification: 90 days' notice (vs. 30) to allow data export and offboarding. No early termination fees. Pro-rated refund of prepaid fees. |
| EU data residency | Accepted and built into the platform architecture. |
| GDPR DPA | We will execute Acme's DPA or provide our standard DPA for review. |

---

## 6. Customer References

| Customer | Industry | Annual Value | Won Against | Why Relevant |
|---|---|---|---|---|
| **Initech Sensors** | Industrial / IoT | $420K | Microsoft Fabric | Closest analogue — IoT ingest at scale, Power BI, EU residency, Azure |
| **Globex Manufacturing** | Industrial / Manufacturing | $580K | Snowflake, Databricks | 300+ TB, Teradata migration, multi-region, multi-source |
| **Stark Industries** | Industrial / Aerospace | $1.1M | Databricks, Snowflake, Fabric | Complex multi-region, IP licensing precedent, largest comparable deal |

All three are Enterprise-tier, Azure-primary, Power BI-dependent customers. Contact details available on request following NDA execution.

---

## 7. Why BTS-Synthetic

| Evaluation Criterion (per RFP §5) | Our Position |
|---|---|
| **Functional fit (30%)** | Full coverage on all hard requirements. Transparent disclosure on sub-100ms streaming latency. |
| **Commercial terms (25%)** | 28% off list, Net 60, CPI-capped escalator, 5-year pricing locked at signing, no MFN. |
| **Total cost of ownership (20%)** | Predictable spend; no per-query compute surprise; volume true-up buffer at 10%. We will produce a 3-year TCO comparison at your exact workload profile. |
| **Implementation timeline (15%)** | 20 weeks to full migration; 8 weeks to first production workload. Dedicated team. Fixed-price programme. |
| **Financial stability + references (10%)** | 8 years in market, SOC 2 Type II, ISO 27001, GDPR-aligned. Three referenceable comparable customers. |

We look forward to presenting this proposal to Sarah Chen and Marcus Webb and are available for a technical deep-dive or TCO workshop at Acme's convenience.

**BTS-Synthetic Deal Desk**
deals@bts-synthetic.example

---

*This proposal is confidential and intended solely for Acme Corp's evaluation committee.*
*All pricing is valid until 2026-07-23.*
