# BTS-Synthetic Enterprise Data Platform
## Proposal in Response to Acme Corp RFP — Enterprise Data Platform

**Prepared for:** Sarah Chen, VP Procurement; Marcus Webb, Chief Data Officer
**Prepared by:** BTS-Synthetic Deal Desk
**Date:** 2026-05-26
**RFP reference:** Acme Corp Enterprise Data Platform RFP, issued 2026-05-12

---

## 1. Executive Summary

Acme Corp is replacing a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics with a single enterprise data platform capable of real-time IoT ingest, governed BI at scale, and a foundation for predictive-maintenance ML. BTS-Synthetic proposes our Enterprise Data Platform — a multi-cloud lakehouse built on open formats (Delta, Iceberg, Parquet) — as that platform.

Three points define our response:

- **Technical fit is high.** Every workload in your RFP — 40,000-device real-time ingest, 30+ source batch ETL, BI for 600 analysts with native Power BI, self-service prep for 150 engineers, and a future predictive-maintenance ML path — maps to a proven, production capability. The two items requiring closer scoping during due diligence are multi-region streaming throughput validation and your 99.99% uptime target, both addressed in Sections 3 and 5.
- **We win on total cost of ownership, not headline discount.** Acme is also evaluating Databricks, Snowflake, and Microsoft Fabric. We will not chase the lowest sticker price — we will show you the 5-year cost of running this workload on each platform, including the compute-cost ramp that catches Databricks customers by surprise and the consulting overhead Fabric deployments typically carry.
- **We propose a fair, workable contract — not your starting draft, but not a rubber stamp of the status quo either.** Several terms in Section 3 and 4 of your RFP (uncapped liability, no-notice audits, immediate termination on any SLA miss, full IP assignment, subprocessor veto, and the MFN warranty) fall outside terms we can respond "yes" to. Section 6 sets out counter-positions we believe are fair to both sides and workable in the 14-day window ahead of your evaluation.

We are ready to move quickly toward a signed reference-customer relationship and a production-grade platform ahead of your 2026-06-30 award date.

---

## 2. Our Understanding of Your Need

Acme Corp is a $1.4B global industrial manufacturer of sensors and IoT devices, operating across 18 countries with manufacturing in Mexico, Vietnam, and Romania and R&D in Austin and Munich. You are a Microsoft/Azure shop decommissioning legacy Teradata warehouses through 2027, and you need a single platform to replace that patchwork.

Specifically, we understand you need to support:

- **Real-time ingest** from ~40,000 field IoT devices, peaking at 80,000 events/second
- **Batch ETL** from 30+ internal sources
- **BI and reporting** for ~600 analysts and executives, with Power BI as the primary (non-negotiable) interface
- **Self-service data preparation** for ~150 data engineers
- **A future ML pipeline** for predictive maintenance (planned, not yet active)
- **~280TB** of current data, growing ~12TB/month
- **Multi-region deployment** — EU primary, US East secondary — with EU customer data required to stay in the EU
- **A lakehouse architecture on open formats** (Parquet, Delta, Iceberg) to preserve portability and avoid lock-in

Commercially, you're seeking a 3-year initial term with a 2-year renewal option, fixed 5-year pricing, an aggressive discount off list, and contractual terms that place maximum risk and audit leverage on the vendor side — consistent with a sophisticated, procurement-led evaluation running four vendors in parallel.

---

## 3. Why We're the Right Fit

### 3.1 Functional and technical fit: High

| Requirement | Our capability |
| --- | --- |
| Real-time ingest, 80K events/sec peak | Tested to 250K events/sec single-region — 3x headroom even before accounting for regional distribution of your EU/US traffic |
| Batch ETL, 30+ sources | 80+ out-of-box connectors (Salesforce, SAP, NetSuite, common databases) plus Debezium-compatible CDC |
| Native Power BI, 600 users | Power BI is our most mature BI integration, with a dedicated DirectQuery adapter — this is a strength, not a checkbox |
| Self-service prep, 150 data engineers | Low-code prep UI for analyst personas plus full Python/R/Scala notebook environments for engineering personas |
| Lakehouse, open formats | Native Delta, Iceberg, and Parquet support; compute fully decoupled from storage |
| Multi-region, EU residency | Multi-cloud (AWS/Azure/GCP), multi-region within cloud, with per-table residency pinning for EU data |
| Future ML for predictive maintenance | Model registry, feature store (offline + online), autoscaling model serving, and bring-your-own-model support (HuggingFace, Anthropic, OpenAI) — the platform is ready when your ML program is |

Two items we will validate jointly with your team during technical due diligence rather than assert unconditionally today:

- **Multi-region streaming throughput.** Our 250K events/sec figure is benchmarked single-region. We are confident 80K events/sec split or replicated across EU/US is comfortably within capacity, and we will confirm this with a joint architecture review before contract signature.
- **150 concurrent data-engineer scale on self-service tooling.** Functionally supported; we will size the environment together during implementation planning rather than quote a number we haven't tested at your specific concurrency.

### 3.2 The competitive landscape

We expect Databricks, Microsoft Fabric, and Snowflake to be your closest alternatives (alongside the unnamed regional vendor). Each is a credible platform — and each carries a trade-off worth surfacing plainly:

- **Microsoft Fabric** will look attractive on headline price if bundled into an existing E5 agreement, and it has the shortest path to "already in your tenant." But it is a young platform (in market roughly 18 months against our multi-year track record) and is Azure-only — which cuts against your own stated preference for open formats and portability. We integrate deeply with Power BI; we do not require you to give up multi-cloud optionality to get that integration.
- **Databricks** is a genuine lakehouse peer with a strong ML story and native Delta support. Where customers are typically surprised is the compute-cost ramp as usage scales, and Spark-based query latency for the kind of interactive, analyst-facing BI your 600 Power BI users need daily.
- **Snowflake** offers a polished analyst experience but is comparatively weaker on real-time, high-throughput ingest — precisely your core 80,000 events/second requirement — and its ML/AI capability is a more recent addition to the platform rather than native architecture.

Our recommendation is that you evaluate all vendors on **5-year total cost of ownership at your actual workload profile**, not on published list price. We will provide a detailed TCO model as part of technical due diligence, and we are glad to have that model reviewed by your finance team directly.

---

## 4. Commercial Proposal

We want to be direct about where our commercial proposal aligns with your RFP and where we believe an adjustment serves both parties better.

| Term | Your RFP | Our proposal |
| --- | --- | --- |
| List price basis | — | Enterprise tier (unlimited ingest/users, 24/7 support, dedicated CSM) — the only tier appropriate at your scale |
| Discount off list | ≥35% | We propose an opening position in the low-to-mid 20s%, moving toward our strategic ceiling (reserved for multi-year, reference-customer commitments) as the structure below is agreed. We are not able to commit to 35% off list as a standing position — see Section 6 for why, and for the value levers we'd rather use to close that gap than a straight price cut. |
| Term | 3-year initial + 2-year renewal option | Accepted as proposed |
| Full 5-year pricing fixed at signature, no escalators | Required | We propose fixing pricing for the 3-year initial term in full. For the 2-year renewal, we propose a modest, capped adjustment (CPI plus a small margin, capped at 5% annually) rather than a blanket 5-year freeze — this is standard practice for any 5-year infrastructure commitment and protects you from a worse outcome (a full re-negotiation) if the renewal is not exercised on schedule. |
| Payment terms | Annual in advance, Net 90 | We propose annual in advance, **Net 60** — consistent with terms we extend to comparable investment-grade industrial customers of your scale and credit profile |
| Most Favoured Nation warranty | Required | We are not able to offer an MFN warranty (see Section 6) |

We will provide full 5-year pricing transparency in our written commercial exhibit, itemizing list price, discount, and total contract value year by year, as requested in your response format.

**Value levers beyond headline discount** that we believe close the gap between your 35% target and a sustainable commercial structure without eroding either side's position:
- A committed 3-year term (rather than annual renewal risk) supports a stronger discount than a shorter commitment would
- A signed reference-customer agreement (case study, reference calls) — which, given your profile, is one we would value highly — supports movement toward our strategic discount ceiling
- Volume true-up terms with a buffer, so you aren't paying for headroom you don't use
- A PoC/acceptance period, with any pilot fees credited toward Year 1, reducing switching risk on your side

---

## 5. Contract Approach

We approach contracting as a partnership, not a template fight — but a small number of terms in your draft would put BTS-Synthetic in a position no vendor could respectably accept and stay in business (uncapped liability without an insurable ceiling, for example, isn't a negotiating stance — it's a term our insurer would refuse to underwrite). Below is our position on each item that needs to move, and why.

| Area | Your RFP | Our position |
| --- | --- | --- |
| **Liability for data breach** (§4.1) | Uncapped, including regulatory fines and reputational damages | Cap aggregate liability at 24 months of fees paid, with uncapped carve-outs for gross negligence and IP infringement. This is a higher cap than our standard (12 months) in recognition of your scale, but an uncapped commitment falls outside any commercially available cyber-insurance policy and would leave the relationship uninsured in the event of a genuine incident — not a protection to you, in practice. |
| **Audit rights** (§4.2) | Unannounced, up to 4x/year, vendor pays all costs | One audit per year with 30 days' written notice and confidentiality terms; up to two additional audits per year available at your cost. No-notice audits of production infrastructure create operational risk for every customer on shared infrastructure, not just Acme. |
| **Service levels** (§4.3) | 99.99% monthly uptime; any SLA miss triggers immediate termination and full-month refund | 99.95% monthly uptime as our standard Enterprise commitment, with service credits (up to 30% of monthly fees) as the remedy for a miss. If a true 99.99% commitment is required, we can scope a bespoke multi-region active-active architecture as a priced option — happy to walk your technical team through what that involves and costs. Either way, we propose termination rights apply only after a sustained pattern of misses (e.g., three consecutive months), not a single incident — this protects you from chronic underperformance while giving both sides a chance to remediate a one-off issue. |
| **Intellectual property** (§4.4) | All custom work vests in Acme upon creation | Configurations, integrations, and custom work built specifically for Acme are licensed to Acme on a perpetual, royalty-free basis for your internal use; BTS-Synthetic retains ownership of the underlying platform and any component that is broadly reusable across our customer base. This is the same structure we've used successfully with other customers who required strong IP protections, including in defense/aerospace engagements — we're glad to share how that structure worked in practice. |
| **Subprocessors** (§4.5) | Prior written consent for any subprocessor, withholdable at sole discretion | 30 days' advance notice via a public subprocessor list; if you object to a new subprocessor, we will offer a substitute or, if none is workable, allow termination of the affected service without penalty. A blanket pre-approval right is operationally difficult to sustain across our customer base but we want to give you real recourse, which this structure does. |
| **Termination for convenience** (§3.5) | Either party, 30 days' notice, no cause required, no fees | We accept "no cause, no fees." We propose extending the notice period to 90 days (or a negotiated minimum of 60) so both sides have a realistic transition runway — a 30-day cutover on an enterprise data platform risks an operationally difficult handoff for your own teams. |
| **Most Favoured Nation** (§3.4) | Pricing warranted no less favourable than any comparable customer, for contract duration | We are not able to offer an MFN warranty. Enterprise pricing is customized to term length, volume, and deal-specific concessions across our customer base, and an MFN clause would require ongoing cross-customer pricing audits that aren't operationally workable. We believe the discount and value levers in Section 4 deliver you a highly competitive position without this clause. |

We recognize this is a longer list of proposed changes than a "sign as-is" response, and we're presenting it now — ahead of your evaluation — deliberately: we would rather be transparent about our real position in week one than agree to terms in the RFP response and re-open them during contracting, which costs you time against your 2026-06-30 award date.

---

## 6. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Gap between your 35% discount floor and our standing commercial structure | We've proposed a path (Section 4) using term, reference, and volume commitments to move toward our strongest available position; we'd like to discuss this directly with Sarah Chen's team early in the process rather than let it become a late-stage blocker |
| 99.99% uptime target exceeds our standard Enterprise SLA | Standard 99.95% commitment with credits, or a priced active-active architecture option for a true 99.99% commitment — either path is available; we recommend a technical working session to size this properly before contract signature |
| Multi-region real-time throughput at your specific split | Joint architecture review during due diligence to validate ingest performance across EU/US before go-live, ahead of any production commitment |
| Legacy Teradata decommission timeline (through 2027) runs alongside your new-platform rollout | Phased migration plan (Section 7 detail available on request) sequences highest-value workloads first, so Teradata decommissioning and platform adoption can run in parallel without a forced big-bang cutover |
| Multiple vendors under evaluation in parallel | We're proposing a proof-of-concept phase against your actual workload profile (not a generic demo) so the evaluation is decided on real performance and real TCO, not headline claims |

---

## 7. Implementation Plan (Summary)

- **Weeks 1-4:** Architecture validation (including multi-region throughput testing), environment provisioning, connector setup for priority source systems
- **Weeks 5-8:** First production workload live (batch ETL + BI for a priority business unit) — consistent with our typical 8-week time-to-first-production-workload for customers with clean source systems
- **Weeks 9-16:** Real-time IoT ingest pipeline at full scale, remaining source system onboarding, Power BI rollout to full 600-user base
- **Weeks 17-24:** Full Teradata workload migration, self-service enablement for the 150-engineer population, governance/audit configuration finalized
- **Ongoing:** Predictive-maintenance ML pipeline scoping begins once core platform is stable, timed to your program's readiness

Three reference customers of comparable scale, Azure footprint, and Power BI usage will be provided separately per your response format request.

---

*This proposal is submitted in response to the Acme Corp RFP dated 2026-05-12, for consideration ahead of the 2026-05-26 response deadline. All commercial terms are subject to final contract negotiation and mutual execution of a definitive agreement.*
