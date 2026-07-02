# BTS-Synthetic — Proposal for Acme Corp Enterprise Data Platform

**Prepared for:** Acme Corp — Sarah Chen (VP Procurement), Marcus Webb (Chief Data Officer)
**Prepared by:** BTS-Synthetic Deal Desk
**Date:** 2026-07-01
**RFP reference:** Acme Corp Enterprise Data Platform (issued 2026-05-12)

---

## 1. Executive Summary

- **We fit your core requirements today.** A lakehouse built on open formats (Delta, Iceberg, Parquet), a dedicated Power BI DirectQuery adapter for your 600 analysts, native real-time streaming that comfortably clears your 80,000 events/second peak, and per-table EU data residency — all available now on Azure, multi-region.
- **We win on total cost of ownership, not headline price.** Against Databricks, Snowflake, and Microsoft Fabric, our differentiator is predictable, fixed spend at your actual 280 TB / 12 TB-per-month profile — not compute that ramps unpredictably. We propose a firm 3-year price with transparent 5-year visibility.
- **A few of your contractual terms exceed what any responsible vendor can accept as written** (uncapped breach liability, MFN, full IP assignment, terminate-on-any-SLA-miss). We flag these honestly below with workable counter-positions, rather than agree and re-trade later.

## 2. Our Understanding of Your Need

Acme Corp is replacing a patchwork of on-premises Teradata warehouses (decommissioning through 2027) and ad-hoc cloud analytics with a single enterprise data platform. The platform must serve five distinct workloads on one architecture:

- **Real-time ingest** from ~40,000 field IoT devices, peaking at 80,000 events/second.
- **Batch ETL** from 30+ internal sources.
- **BI and reporting** for ~600 analysts and executives — with **native Power BI integration as a stated non-negotiable**.
- **Self-service data preparation** for ~150 data engineers.
- **Machine-learning pipelines** for predictive maintenance (planned, not yet active).

The environment is Microsoft-centric and Azure-first, at ~280 TB today growing ~12 TB/month, with a hard requirement that **EU customer data remain in the EU** (primary EU region, secondary US East), a **lakehouse architecture** on **open file formats** for portability, and a **99.99% uptime** commitment.

We read this as a migration-and-consolidation deal where the winning vendor must prove real-time performance, first-class Power BI experience, EU residency, and — above all — a defensible multi-year total cost of ownership.

## 3. Why We're the Right Fit

### 3.1 Technical fit against your requirements

| Requirement | BTS-Synthetic capability | Fit |
|---|---|---|
| Lakehouse, open formats (Parquet/Delta/Iceberg) | Native lakehouse with Delta, Iceberg, Parquet; compute decoupled from storage | Full |
| Native Power BI (600 users, non-negotiable) | Certified Power BI integration with a **dedicated DirectQuery adapter** — our most mature BI integration | Full |
| Real-time ingest, 80K events/sec peak | Native Kafka/Kinesis streaming, tested to **250K events/sec** single-region | Full (3x headroom) |
| Batch ETL from 30+ sources | 80+ out-of-the-box connectors, CDC for Teradata migration | Full |
| Self-service prep for 150 engineers | Low-code data-prep UI plus Python/R/Scala notebooks | Full |
| ML for predictive maintenance | Model registry, feature store, autoscaling serving; bring-your-own-model | Full |
| Multi-region (primary EU, secondary US East) | Multi-cloud, multi-region on Azure | Full |
| EU data residency | Per-table residency enforcement — EU tables pinned to EU regions | Full |
| Governance & audit | Unity-style catalog, row/column ABAC, PII detection/masking, exportable audit logs to your SIEM | Full |
| **99.99% uptime** | Standard Enterprise SLA is **99.95%**; **99.99% available as an add-on** requiring multi-region active-active | Partial — addressed in §4 |

**Honest note on latency:** for sub-100 ms interactive streaming we are not best-in-class (we operate in the ~250 ms–1 s range). Your stated workloads — real-time ingest, BI, predictive maintenance — do not require sub-100 ms query latency, so this is not a gap for your use case, but we flag it transparently.

### 3.2 Competitive positioning

Your RFP names Databricks, Snowflake, and Microsoft Fabric. Here is how we position for **this** deal:

- **vs. Microsoft Fabric** — Fabric will look "free with E5." We ask you to weigh the honest TCO including Microsoft consulting hours, the Azure-only lock-in against your open-format portability goal, and platform maturity (we have eight years in production; Fabric's core is roughly eighteen months old). We integrate deeply with Power BI; we do not need to own your BI layer to do so.
- **vs. Databricks** — genuinely strong at large-scale engineering, but customers are repeatedly surprised by compute spend that ramps with usage. We lead with predictable, fixed spend and faster time-to-insight for your 600 analysts, who are not Spark engineers.
- **vs. Snowflake** — excellent analyst experience, but expensive at your scale and weaker on real-time and semi-structured IoT data. Our real-time and ML-native architecture covers all five of your workloads on one platform.

**Our best opening move:** a 3-year TCO comparison run at Acme's actual workload profile (280 TB, 12 TB/month growth, 80K events/sec), which is precisely how we displaced Snowflake at Globex Manufacturing and beat Microsoft on real-time SLA at Initech Sensors — both directly comparable industrial/IoT accounts.

### 3.3 Comparable references

- **Initech Sensors** (Industrial/IoT) — real-time ingest + governance maturity; beat Microsoft on real-time SLA.
- **Globex Manufacturing** (Industrial) — won on 3-year TCO vs. Snowflake at a heavy real workload.
- **Wayne Manufacturing** (Industrial) — proven via a 90-day PoC that converted to a production reference.

All three match your profile on scale, Power BI, and Azure and are available as references.

## 4. Commercial Proposal

All pricing is transparent and expressed against published list. Recommended tier: **Enterprise** (unlimited ingest, unlimited users, 24/7 support, dedicated CSM). List base: **$720,000 / year**.

| Item | List | Proposed | Notes |
|---|---|---|---|
| Enterprise platform (annual) | $720,000 | **$540,000** | 25% strategic discount (see below) |
| 99.99% uptime add-on (annual) | — | **~$100,000** | Multi-region active-active architecture required to honour 99.99% |
| **Total annual** | | **~$640,000** | Firm for the 3-year initial term |
| 3-year initial term (total) | | **~$1.92M** | |
| 5-year horizon (incl. 2-year renewal) | | **~$3.2M** | Renewal priced per §4.3 |

### 4.1 Discount position

Your RFP asks for **no less than 35%** off list. Our maximum authorised discount in this deal band ($500K–$1M annual) is **20% standard / 25% strategic**. We are prepared to extend the **full 25% strategic discount**, justified by your 3-year committed term and reference-customer potential (VP Sales sign-off). We cannot reach 35% without eroding the service levels this platform is built to deliver; our value case is 3-year TCO, not the headline number, and that is where we expect to win.

### 4.2 Payment terms

Your RFP requests **Net 90**. Our standard is annual-upfront **Net 30**. Given Acme's financial strength, we can offer **Net 60** as a concession. Net 90 is outside policy.

### 4.3 Term and price protection

We will hold the annual price **firm for the full 3-year initial term with no escalators**. For the 2-year renewal, we propose a modest CPI-linked adjustment **capped at 5%** rather than a fixed 5-year freeze; a genuinely fixed 5-year price normally requires an escalator to underwrite, so the cap is our compromise that still gives you full budget visibility.

### 4.4 Concessions we will make

- PoC/pilot fees credited toward Year 1.
- Acceptance-testing period up to 30 days.
- Year-end volume true-up with a 10% buffer above committed volume.
- Custom MSA (deal is above $500K), with legal sign-off.

## 5. Contract Approach

We have reviewed your contractual terms against our standard positions. We flag the following, with counter-positions, in the spirit of surfacing everything now rather than re-trading later. Items marked **BLOCKER** are terms we cannot accept as written under our insurance and corporate policy.

| # | Your term | Severity | Our counter-position |
|---|---|---|---|
| 4.1 | Uncapped liability for data breach | **BLOCKER** | Liability capped at **24 months of fees**, with mutual carve-outs for IP infringement and gross negligence. Uncapped liability voids our cyber-insurance ceiling. |
| 4.1 | Uncapped indemnity for regulatory fines & reputational damages | **BLOCKER** | Indemnity capped at **24 months of fees** with defined carve-outs; reputational damages excluded as uninsurable. |
| 3.4 | Most-Favoured-Nation pricing | **BLOCKER (redlined)** | Removed entirely. MFN is incompatible with SaaS list pricing; we decline rather than agree and breach later. |
| 4.4 | All work product vests in Acme on creation | **BLOCKER** | We retain IP in our underlying service; any Acme-specific custom work is **licensed back to Acme** (the model Stark Industries accepted). Your data remains yours. |
| 4.3 | Immediate termination on any SLA miss + full monthly refund | **BLOCKER** | Service credits up to 30% of monthly fees as sole remedy; termination for material breach with a **30-day cure period**. |
| 4.5 | Prior written consent for every subprocessor (sole discretion) | HIGH | Public subprocessor list; **30-day advance notice** of new subprocessors; right to object with substitute-or-terminate. Per-subprocessor veto is operationally unworkable. |
| 4.2 | Unannounced audits, up to 4×/year, vendor pays | HIGH | **One audit per year with 30 days' notice**, under confidentiality; Acme pays for audits beyond the first. |
| 4.3 | 99.99% uptime demanded | MEDIUM | Deliverable **only via the multi-region active-active add-on** (§4). Standard Enterprise SLA is 99.95%. |
| 3.5 | Termination for convenience on 30 days' notice | MEDIUM | Acceptable in principle; we ask for **60 days'** notice. Refunds pro-rated; no penalty fees either way. |
| 3.1 | 5-year fixed price, no escalators | (commercial) | Firm for the 3-year initial term; CPI-capped adjustment on renewal (§4.3). |
| 2.3 | Multi-region processing (EU + US East) | ACCEPTABLE | Supported via per-table residency; flagged for DPA review. |

## 6. Risks and How We Mitigate Them

- **Contractual blockers (liability, MFN, IP, terminate-on-SLA-miss).** These are the main risk to a signable deal. Mitigation: table our counter-positions early, route to VP-level approval, and negotiate as a package — each has a well-precedented compromise (see comparable deals).
- **99.99% SLA gap.** Our standard is 99.95%. Mitigation: the multi-region active-active add-on, which also satisfies your EU-primary / US-secondary topology, so the architecture does double duty.
- **Aggressive price expectation (35% ask).** Mitigation: reframe the evaluation onto 3-year TCO at Acme's real workload — the ground on which we beat Snowflake (Globex) and Microsoft (Initech).
- **Migration complexity (Teradata decommission, 30+ sources, multi-region).** Typical timeline for a migration of this size is ~16–24 weeks. Mitigation: phased plan — first production workload in ~8 weeks on clean sources, CDC-based Teradata migration in parallel, full cutover by ~24 weeks.
- **Payment terms (Net 90 ask).** Mitigation: offer Net 60 as the concession; hold the line on Net 90.

---

*This proposal is commercial-in-confidence. Pricing reflects proposed positions subject to final contract and internal approvals.*
