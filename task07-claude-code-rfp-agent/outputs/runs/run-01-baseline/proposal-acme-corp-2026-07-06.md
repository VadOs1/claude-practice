# Proposal: Enterprise Data Platform for Acme Corp

**Prepared for:** Acme Corp, Procurement Office (Sarah Chen, VP Procurement; Marcus Webb, Chief Data Officer)
**Prepared by:** BTS-Synthetic
**Date:** 2026-07-06
**In response to:** RFP issued 2026-05-12

---

## 1. Executive Summary

Acme Corp is replacing a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics with a single enterprise data platform capable of ingesting 80,000 events/second from 40,000 IoT devices, serving 600 BI analysts and executives on Power BI, and supporting 150 data engineers today — with predictive-maintenance ML pipelines on the near-term roadmap.

BTS-Synthetic proposes our Enterprise Data Platform, a lakehouse built on open formats (Delta, Iceberg, Parquet) with native multi-region deployment across EU (primary) and US East (secondary), per-table data residency enforcement, and the most mature Power BI integration in our portfolio — including a dedicated DirectQuery adapter built specifically for high-concurrency analyst workloads like Acme's.

We are well matched to Acme's scale and workload profile: our real-time ingest is tested to 250,000 events/second, more than 3x Acme's peak requirement, and our 80+ connector library covers standard ETL sources out of the box. We have won comparable industrial/IoT deals on this exact combination of real-time performance and governance maturity (see §3, references).

Two areas require open negotiation before signature: **discount depth** and **certain liability/termination terms**, both addressed transparently in §4 and §6. We would rather be direct about where we differ from the RFP's initial terms than paper over gaps that surface later in the relationship.

---

## 2. Our Understanding of Your Need

Acme Corp is a $1.4B global industrial sensor and IoT manufacturer operating across 18 countries, with manufacturing in Mexico, Vietnam, and Romania and R&D in Austin and Munich. You are a Microsoft/Azure shop decommissioning legacy Teradata warehouses through 2027, and you need a platform that can absorb:

- **Real-time ingest** from ~40,000 field IoT devices, peaking at 80,000 events/second
- **Batch ETL** from 30+ internal sources
- **BI and reporting** for ~600 analysts and executives, with Power BI as a non-negotiable, primary interface
- **Self-service data preparation** for ~150 data engineers
- **Predictive maintenance ML pipelines**, planned but not yet active
- **~280 TB** of current data, growing ~12 TB/month
- **Multi-region deployment** (EU primary, US East secondary) with EU customer data required to stay in the EU
- **Lakehouse architecture** on open file formats, to avoid the vendor lock-in your Teradata migration is designed to escape

We also understand you are running a competitive process against Databricks, Snowflake, and Microsoft Fabric, and evaluating primarily on functional fit (30%), commercial terms (25%), 5-year TCO (20%), implementation risk (15%), and vendor stability/references (10%).

---

## 3. Why BTS-Synthetic Is the Right Fit

### 3.1 Technical fit

| Requirement | Our capability | Fit |
| --- | --- | --- |
| Real-time ingest, 80K events/sec peak | Native Kafka/Kinesis streaming, tested to 250K events/sec | Strong |
| Batch ETL, 30+ sources | 80+ out-of-box connectors, CDC via Debezium-compatible connectors | Strong |
| Power BI (non-negotiable) | Certified integration; dedicated DirectQuery adapter — our most mature BI integration | Strong |
| Self-service prep, 150 engineers | Low-code data prep UI for analyst/engineer personas | Strong |
| ML pipelines (predictive maintenance) | Model registry, feature store (offline + online), native autoscaling model serving | Strong |
| Lakehouse, open formats | Native Delta, Iceberg, Parquet support; decoupled compute/storage | Strong |
| Multi-region, EU/US | Multi-cloud, multi-region; per-table residency pinning enforces EU-only tables | Strong |
| 280 TB scale, 12 TB/mo growth | Well within proven deployment scale | Strong |
| 99.99% uptime | Our Enterprise tier ships at 99.95%; 99.99% is available as a custom active-active add-on (see §4) | Partial — addressed commercially |

We are not the best-in-class option for sub-100ms streaming analytics or geospatial/graph workloads — neither of which appears in your stated requirements, so we do not consider this a gap for this engagement.

### 3.2 Positioning against the field

You've named Databricks, Snowflake, and Microsoft Fabric as competing bidders. Briefly, on why we believe we win this specific evaluation:

- **vs. Microsoft Fabric:** Fabric will look attractively priced if bundled with your existing E5 licensing, and it has native Azure/Power BI advantages we won't dispute. But Fabric is an 18-month-old product still maturing core capabilities, and its all-in Azure model works against the multi-cloud optionality your Teradata exit is designed to preserve. Our real-time ingest performance and governance maturity are proven at your scale — we closed a directly comparable industrial IoT account against Fabric on exactly this basis.
- **vs. Databricks:** Databricks is strong on ML/AI breadth and large-scale engineering workloads, and we won't out-engineer them on Spark internals. But 600 of your 750 platform users are analysts and executives, not engineers — our BI-first tooling and predictable total cost of ownership matter more to that population than Databricks' engineering-centric strengths.
- **vs. Snowflake:** Snowflake's analyst experience is excellent, but it is weaker on real-time and semi-structured ingest — exactly the workload your 40,000-device IoT fleet generates. We also offer a more native ML story for your planned predictive-maintenance pipelines.

### 3.3 References

Three comparable accounts, available for reference calls:

1. **Initech Sensors** (Industrial/IoT) — closed 2025-11-22. Directly comparable profile to Acme: won on real-time ingest performance and governance maturity, against Microsoft Fabric's "free with E5" pitch.
2. **Globex Manufacturing** (Industrial/Manufacturing) — closed 2025-09-14. Won on a 3-year TCO comparison run at their actual (heavy-unstructured) workload profile against a Snowflake-leaning shortlist.
3. **Wayne Manufacturing** (Industrial) — closed 2026-03-05. Started as a 90-day PoC with fee credited into Year 1; signed a reference customer agreement, and can speak to implementation experience.

---

## 4. Commercial Proposal

Per your request for full 5-year pricing transparency:

### 4.1 List pricing

| Component | Annual list |
| --- | --- |
| Enterprise tier (unlimited ingest/users, 24/7 support, 99.95% SLA, dedicated CSM) | $720,000 |
| 99.99% uptime add-on (custom active-active architecture) | $100,000 |
| **Total annual list** | **$820,000** |

### 4.2 Proposed discount

Your RFP requires a minimum 35% discount from list. We want to be transparent rather than nominally agree and revisit later: **our standard discount governance caps out at 25% for a deal in this size band, even at our top "strategic" tier** (which requires VP Sales sign-off and is reserved for multi-year commitments and reference-customer relationships — both of which Acme qualifies for).

We are proposing **25% off list** ($615,000/year) as our strategic offer, contingent on:
- A committed 3-year initial term (not just an option), and
- A signed reference customer agreement (as Wayne Manufacturing and others have done)

This is 10 points short of your 35% floor. Rather than either walking away or agreeing to unsustainable pricing, we'd like to make the case on 5-year TCO: our transparent, all-in pricing (no per-connector fees, no compute-consumption surprises) has repeatedly beaten nominally cheaper competitors once real usage is modeled — this is exactly how we won the Globex and Initech accounts referenced above. We are happy to build a workload-specific TCO model against Databricks and Snowflake pricing if that would help your evaluation committee compare like-for-like on the 20%-weighted TCO criterion.

### 4.3 Five-year view

| Year | Annual fee | Notes |
| --- | --- | --- |
| 1–3 | $615,000/year, fixed | Initial committed term |
| 4–5 (renewal option) | $615,000/year, fixed | We propose holding renewal pricing flat at the Year 3 rate rather than applying our standard escalator, given your no-escalator requirement — this needs pricing committee sign-off but we intend to seek it given the deal's size and reference value |
| **5-year total** | **$3,075,000** | Fully fixed, no escalators, subject to committee approval of the renewal-year waiver |

### 4.4 Payment terms

Your RFP requests Net 90 billed annually in advance. Net 90 falls outside terms we can commit to broadly. Given Acme's scale and credit profile, we can offer **Net 60** — our maximum standard concession, normally reserved for large, strong-credit accounts. We propose annual billing in advance with Net 60 payment.

### 4.5 Most Favoured Nation clause

We are not able to offer an MFN warranty (pricing no less favourable than any comparable customer). This is a clause we decline on all deals, including this one — our discount structure already reflects deal-specific factors (size, term, reference value) that make cross-customer pricing comparisons unworkable in practice. We're glad to discuss alternative assurances, such as most-favoured pricing among your specific named competitor set, if useful.

---

## 5. Contract Approach

We propose a Master Services Agreement with an order form referencing this proposal, plus a Data Processing Agreement (DPA) covering EU residency commitments. Key terms we propose, alongside where we differ from your draft requirements (full detail in §6):

- **Term:** 3-year initial term, 2-year renewal option, pricing fixed as described in §4.3
- **Data residency:** EU customer data pinned to EU-region tables; US-secondary data in US East — this matches our standard architecture and requires no exception
- **Acceptance testing:** up to 30 days post-implementation, standard offer
- **Volume true-up:** annual true-up with 10% buffer above committed volume before overage charges apply
- **Governing law:** England & Wales for this engagement, given your EU operations footprint — open to discussing Delaware if preferred for the US-entity contracting party

---

## 6. Risks and Mitigations

We would rather flag contractual gaps now than have them resurface during legal review. Each item below cites our standard position and a proposed counter.

| # | RFP term | Our standard | Severity | Proposed counter |
| --- | --- | --- | --- | --- |
| 1 | Liability for data breach is uncapped, with full indemnification for regulatory fines and reputational damages | Aggregate liability capped at 12 months of fees; higher caps require insurance review | **Blocker** | Cap liability at 24 months of fees paid, with uncapped carve-outs for gross negligence and IP infringement |
| 2 | Audit without prior notice, up to 4x/year, vendor bears all costs | Customer may audit once/year with 30 days' notice; customer bears cost of audits beyond the first | **Blocker** (no-notice) / **Negotiable** (frequency, cost) | 30 days' notice for all audits; up to 2 audits/year included, additional audits at customer's cost |
| 3 | Any SLA failure of any duration entitles immediate termination + full month's refund | 99.95% monthly uptime; service credits up to 30% of monthly fees as sole remedy | **Blocker** | Service credits (up to 30%) as primary remedy; termination right reserved for repeated failures (3+ consecutive months) via standard material-breach/cure process |
| 4 | All work product (custom development, configurations, integrations) vests in Acme upon creation | We retain platform IP; customer-specific configurations/integrations are licensed, not assigned | **Blocker** | Perpetual, royalty-free license to Acme for all custom configurations/integrations built for this engagement; underlying platform IP remains ours |
| 5 | Prior written consent required for any subprocessor, withholdable at Acme's sole discretion | Public subprocessor list; 30 days' advance notice of new subprocessors; customer may object | **Blocker** | 30-day advance notice with objection right; we substitute the subprocessor or allow termination of the affected service component |
| 6 | Termination for any reason (or none) on 30 days' notice, no fees | Termination for convenience on 90 days' notice | **Negotiable** | 60 days' notice minimum, given the operational lead time our implementation requires |
| 7 | MFN pricing warranty | Never offered | **Blocker** | Declined; alternative narrower assurance available (see §4.5) |
| 8 | Payment Net 90, annual in advance | Net 30 default; Net 60 max concession | **Negotiable** | Net 60 (already reflected in §4.4) |
| 9 | 35% minimum discount from list | Discount bands cap at 25–30% depending on deal size/strategic status | **Negotiable, material gap** | 25% strategic offer (§4.2); TCO-based justification for the gap |
| 10 | 99.99% uptime requirement | Enterprise tier ships at 99.95%; 99.99% is a paid add-on requiring active-active architecture | **Negotiable** | Offered as a priced add-on (§4.1); flag that "any failure = termination" (item 3) is decoupled from the uptime target itself |
| 11 | 3-year term + fixed 5-year pricing with no escalator | Standard 3-year discount requires a CPI+2% escalator (capped 5%) | **Negotiable** | Proposed waiver of escalator for Years 4–5, pending pricing committee approval (§4.3) |
| 12 | EU data residency, multi-region EU/US | Matches our standard per-table residency architecture | **Acceptable** | No exception needed |

**Net assessment:** Items 1, 2, 3, 4, 5, and 7 are hard blockers under our current insurance, IP, and governance posture and cannot be accepted as drafted — they are common negotiation points, though, and we have closed comparable deals (e.g., Stark Industries on IP; Initech Sensors on discount) by reaching acceptable middle ground on each. Items 8–11 are commercial gaps we can close partially but likely not fully to Acme's opening position. We recommend Acme's evaluation committee weigh this proposal on the strength of technical fit and 5-year TCO (55% of stated evaluation weight) against the commercial and legal gaps identified above, which we believe are resolvable in negotiation but should be surfaced now rather than at contract signature.
