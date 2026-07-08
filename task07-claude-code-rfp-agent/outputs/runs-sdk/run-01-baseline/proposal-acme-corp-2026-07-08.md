# Proposal for Acme Corp Enterprise Data Platform

**Prepared by:** BTS-Synthetic
**Prepared for:** Acme Corp — Sarah Chen, VP Procurement; Marcus Webb, Chief Data Officer
**Date:** 2026-07-08
**In response to:** RFP issued 2026-05-12, response format per Section 7

---

## 1. Executive Summary

Acme Corp is replacing a patchwork of on-premises Teradata warehouses and ad-hoc cloud analytics with a single enterprise data platform capable of supporting 40,000 IoT devices, 600 BI users, 150 data engineers, and a future predictive-maintenance ML program — on Azure, with EU data residency, and without disrupting your 600-seat Power BI estate.

BTS-Synthetic is purpose-built for exactly this profile. We are a lakehouse platform with our most mature BI integration built specifically for Power BI (dedicated DirectQuery adapter), native real-time streaming tested to 3x your peak ingest requirement, per-table EU data residency enforcement, and open file formats (Delta, Iceberg, Parquet) so you are never re-locked into a proprietary format the way you were with Teradata. We have won and delivered this exact profile before — industrial and IoT manufacturers migrating off legacy warehouses onto Azure, defending Power BI as the analyst front end, at scale comparable to yours.

On price, we are proposing a **25% strategic discount off list** ($540,000/year for the Enterprise tier, down from $720,000 list), backed by dedicated VP sign-off given Acme's strategic fit — a target vertical, multi-year commitment, and strong reference potential. This does not reach the 35% ceiling requested in Section 3.3; we explain why below, and why we believe a rigorous 3-year TCO comparison closes that gap more credibly than a headline discount does. On the terms most likely to affect deal risk — liability, IP, audit, SLA, and MFN — we have proposed a small number of counter-positions consistent with how we structure every enterprise SaaS agreement, and we are ready to work through them quickly against your 2026-06-30 award date.

We believe BTS-Synthetic is the lowest-risk, best-value path off Teradata and onto a durable, open, Power-BI-native platform for Acme.

---

## 2. Our Understanding of Acme's Needs

Acme is a $1.4B global industrial IoT/sensor manufacturer (7,200 employees, 18 countries; manufacturing in Mexico, Vietnam, Romania; R&D in Austin and Munich) retiring legacy Teradata warehouses through 2027 in favour of a single enterprise data platform on Azure. In summary, the platform must:

| Requirement | Detail |
|---|---|
| Real-time ingest | ~40,000 IoT devices, peak 80,000 events/second |
| Batch ETL | 30+ internal sources |
| BI & reporting | ~600 analysts/executives, **Power BI non-negotiable** |
| Self-service prep | ~150 data engineers |
| ML | Predictive maintenance pipelines (planned, not yet active) |
| Scale | ~280 TB current, ~12 TB/month growth |
| Architecture | Lakehouse preferred; open formats (Parquet, Delta, Iceberg) |
| Deployment | Multi-region — primary EU, secondary US East |
| Residency | EU customer data must remain in EU |
| Term | 3-year initial + 2-year renewal option; 5-year pricing transparency requested |

We read three priorities behind the RFP's structure and 40% weighting on functional fit and TCO:

1. **Power BI continuity is the line in the sand.** With 600 active users, any platform that disrupts the BI layer creates change-management risk Acme is not willing to take on. This is explicitly called out as non-negotiable.
2. **You are actively de-risking vendor lock-in.** The Teradata decommissioning, the explicit request for open formats, and the multi-vendor RFP process (Databricks, Snowflake, Microsoft Fabric, and a regional vendor are all being evaluated) tell us Acme was burned by proprietary lock-in once and does not intend to repeat it.
3. **This is a cost-governance-led decision as much as a technical one.** A 5-year fixed-price ask, a 35% discount floor, Net 90 payment, and an MFN clause all point to a procurement organisation optimising hard for cost certainty over the full contract horizon — reasonable, but some of these terms (as drafted) go beyond standard SaaS industry practice and are addressed candidly in Section 5.

---

## 3. Why BTS-Synthetic Is the Right Fit

### 3.1 Functional fit: strong across every stated requirement

| Acme requirement | BTS-Synthetic capability | Fit |
|---|---|---|
| Native Power BI | Certified Power BI integration with a **dedicated DirectQuery adapter** — our most mature BI integration of any we offer | **Strong** |
| Real-time ingest, 80K events/sec peak | Native Kafka/Kinesis streaming, tested to 250K events/sec — **~3x headroom** over your stated peak | **Strong** |
| Batch ETL, 30+ sources | 80+ out-of-box connectors (SAP, Salesforce, NetSuite, common databases) | **Strong** |
| Lakehouse, open formats | Native Delta, Iceberg, Parquet; bring-your-own Azure Blob storage; compute decoupled from storage | **Strong** |
| EU data residency | Per-table residency enforcement — EU tables pinned to EU regions, enforced, not just documented | **Strong** |
| Multi-region (EU primary / US East secondary) | Multi-region deployment within Azure, supports active-active design | **Strong** |
| Self-service prep for 150 engineers | Low-code data prep UI purpose-built for analyst/engineer personas | **Strong** |
| Predictive maintenance ML (future) | Model registry, feature store (offline + online), native model serving with autoscaling, bring-your-own-model (HuggingFace, Anthropic, OpenAI) | **Strong — ready when you are** |
| Governance / audit | Unity-style catalog, row/column-level ABAC, full audit logging exportable to your SIEM, built-in PII detection & masking | **Strong** |
| Compliance | SOC 2 Type II, ISO 27001, GDPR-aligned (DPA available) | **Strong** |

**One area we'll flag transparently rather than oversell:** our streaming *query* latency (as opposed to ingest) runs ~250ms–1s, not sub-100ms. Nothing in your RFP requires sub-100ms interactive latency today, but if the predictive-maintenance program later requires sub-100ms inference response times, we'd recommend a short architecture review before that phase begins. We would rather flag this now than have it surface as a surprise in month 18.

### 3.2 Why not Databricks, Snowflake, or Microsoft Fabric

You named three of your four evaluated vendors in the RFP, so we'll address them directly rather than talk around them.

- **Microsoft Fabric** will likely be the most natural incumbent argument, given you're an Azure/Microsoft shop already licensing E5. We take that seriously rather than dismiss it — but Fabric is roughly 18 months into building capabilities we've operated in production for 8 years, and Fabric's "free with E5" framing tends to understate the Microsoft consulting hours required to reach production readiness at your scale. We'd rather show you an honest, fully-loaded TCO comparison than compete on "who owns Power BI" — Microsoft does, and we simply integrate with it exceptionally well.
- **Databricks** has a strong ML/engineering brand, but its total cost of ownership tends to surprise customers once compute spend ramps, and its BI/analyst tooling is less mature than a platform built with 600 analysts in mind. We'd rather run a 3-year TCO projection at your actual workload profile than compete engineer-to-engineer on Spark internals.
- **Snowflake** offers a polished analyst experience but is materially weaker on real-time and semi-structured ingest — a gap that matters directly to your 80,000 events/second IoT requirement — and its ML story is bolted on rather than native, which matters for your predictive-maintenance roadmap.

### 3.3 Comparable customers

Three reference-quality engagements at comparable scale, industry, and stack:

1. **Initech Sensors** (Industrial/IoT) — closest profile to Acme. Won against Microsoft Fabric on real-time ingest performance and governance maturity; Fabric could not match our real-time SLA despite the "free with E5" pitch.
2. **Globex Manufacturing** (Industrial/Manufacturing) — won against Snowflake and Databricks on a 3-year TCO comparison run against their actual (heavy, unstructured) workload profile — the same exercise we're proposing to run with Acme.
3. **Wayne Manufacturing** (Industrial) — started with a 90-day proof-of-concept, credited the PoC fee toward Year 1, and is now a signed reference-customer account. We'd propose the same PoC-first structure to Acme if useful for de-risking the award decision.

Full named-contact references will be made available on request per your Section 7 requirement.

### 3.4 Implementation approach & milestones

Acme's profile — multi-region, multi-source, migrating off Teradata, at 280TB scale — maps to our "very large, multi-region, multi-source" implementation track. Indicative plan against your 2026-06-30 award target:

| Phase | Timeline from kickoff | Milestone |
|---|---|---|
| Foundation | Weeks 1–4 | Landing zone provisioned (EU primary + US East secondary), catalog & governance model, security review, subprocessor disclosure |
| First production workload | Weeks 5–10 | One IoT ingest pipeline and one BI domain (Power BI DirectQuery) live in production — early proof point, not a big-bang cutover |
| Core migration | Weeks 10–20 | Batch ETL sources (30+) onboarded in priority waves; self-service prep environment live for the 150-engineer team |
| Full cutover | Weeks 20–24 | Full 280TB migration complete, Teradata parallel-run and decommission plan executed, all 600 analysts migrated |
| ML readiness (optional, phased with your roadmap) | Post week 24 | Model registry, feature store, and serving environment stood up ahead of the predictive-maintenance program |

We recommend a short paid PoC (4–6 weeks, fee credited to Year 1 per our standard practice) to validate ingest throughput and Power BI performance against your real data before full commitment — this is exactly the model Wayne Manufacturing used.

---

## 4. Commercial Proposal

### 4.1 Pricing

Your scale places Acme in our Enterprise tier (unlimited ingest, unlimited users, 24/7 support, dedicated CSM).

| Item | List price | Notes |
|---|---|---|
| Enterprise tier (base) | $720,000/year | Unlimited ingest & users, 99.95% monthly uptime SLA, 24/7 support, dedicated CSM |
| Optional: 99.99% SLA add-on | $95,000/year | Bespoke active-active multi-region architecture — a natural fit given your EU-primary/US-East-secondary design |

**Proposed discount: 25% off list**, reflecting Acme's fit as a strategic account (target vertical, multi-year commitment, strong reference potential) and requiring our VP Sales sign-off, which we have already initiated internally in anticipation of this response.

We are aware Section 3.3 asks for a discount no lower than 35%. **We are not proposing 35% today, and we want to be direct about why rather than paper over it:** 25% is the maximum we can offer within standard policy at this deal size even at our top "strategic" tier. Rather than stretch a headline number we can't sustainably deliver, we'd like to win this on the same basis we've won comparable industrial/IoT accounts before (see Section 3.3): a rigorous, workload-specific 3-year TCO comparison against Databricks, Snowflake, and Fabric. In every comparable deal where we've run that exercise, our effective cost position after year 2 has been stronger than a higher headline discount from a less TCO-efficient competitor. We would like the opportunity to run that comparison with your team before final vendor selection.

### 4.2 Five-year pricing transparency (Section 7 requirement)

Per your request for full 5-year pricing transparency. Figures assume the standard 99.95% SLA tier (99.99% add-on priced separately, above, if selected):

| Year | Term | Annual fee | Basis |
|---|---|---|---|
| 1 | Initial (Year 1 of 3) | $540,000 | 25% off list, fixed at signature |
| 2 | Initial (Year 2 of 3) | $540,000 | Fixed at signature — no escalator |
| 3 | Initial (Year 3 of 3) | $540,000 | Fixed at signature — no escalator |
| 4 | Renewal option (Year 1 of 2) | $567,000 (not-to-exceed) | Capped escalator, CPI + 2%, hard cap 5% |
| 5 | Renewal option (Year 2 of 2) | $595,350 (not-to-exceed) | Capped escalator, CPI + 2%, hard cap 5% |
| **5-year total** | | **$2,782,350** | |

**On the "fixed for the full 5 years, no escalators" request:** we can and do fix pricing for the full 3-year initial term at signature — that part of your ask we meet exactly. The 2-year renewal is an *option*, not a committed term, so we price it with a capped escalator (never more than 5%/year, tied to CPI) determined at renewal rather than guessing 2029–2030 costs today. We think this is a more honest number than an artificially flat 5-year figure would be, and the cap protects you from anything beyond modest inflation.

### 4.3 Payment terms

Requested: annual in advance, Net 90. **Our standard is annual in advance, Net 30**, with **Net 60 available for Fortune-500-scale customers with strong credit** — which we'd extend to Acme. Net 90 sits outside what our finance team will approve; we'd like to settle on Net 60.

### 4.4 Most Favoured Nation (Section 3.4)

We are not able to offer a contractual MFN warranty. Pricing across our customer base varies by volume commitment, term length, deployment configuration, and timing — an MFN clause would require us to actively track and true up pricing across every account, which is operationally unworkable and, frankly, a clause we do not offer to any customer regardless of size. In its place, we're glad to commit to the discount structure in Section 4.1 for the life of the contract and to a transparent conversation about our pricing methodology at any renewal.

---

## 5. Contract Approach

We structure enterprise agreements consistently across our customer base, and Acme's draft terms touch several of those standard positions. We'd rather flag these now, with a proposed resolution, than let them slow down negotiation after award.

| Area | Acme's request | Our proposed approach |
|---|---|---|
| **Liability** | Uncapped for any data breach, full indemnification incl. regulatory fines and reputational damages | Liability capped at 24 months of fees paid, with carve-outs for gross negligence, willful misconduct, and IP infringement (i.e., no cap on those). Backed by $5M cyber liability, $5M E&O, $10M general liability insurance — certificates available on request. Uncapped liability isn't something our insurance will support at any price. |
| **Audit** | Unannounced, up to 4x/year, vendor pays | One comprehensive audit per year with 30 days' notice, at no cost to Acme. Additional audits (up to your requested 4/year) available with reasonable notice; Acme covers audit costs beyond the first. Mutual confidentiality applies. |
| **SLA** | 99.99% uptime; any SLA miss triggers immediate termination + full monthly refund | 99.95% standard, with 99.99% available as a paid add-on (Section 4.1) — genuinely achievable given the active-active multi-region design your architecture already calls for. We propose service credits (up to 30% of monthly fees) as the standard remedy, with a termination right preserved for sustained failure (e.g., three consecutive months of breach) rather than any single miss of any duration. |
| **IP** | All work product (custom development, configurations, integrations) vests in Acme | Acme's data is and remains Acme's data, without qualification. Custom configurations and integrations we build for you are licensed to Acme on a perpetual, royalty-free, worldwide basis — full practical ownership of the use, while we retain the underlying IP we reuse across the platform. This is the same structure we agreed with a comparable industrial customer that initially asked for full assignment. |
| **Subprocessors** | Prior written consent required for every subprocessor, at Acme's sole discretion | Public subprocessor list maintained, 30 days' advance notice before any new subprocessor, right to object; if unresolved, Acme may terminate the specific affected service without penalty. |
| **Termination** | Any time, with or without cause, 30 days' notice, no fees | We propose termination for convenience on 90 days' notice (protecting both sides' planning horizon on a 3–5 year platform migration), termination for material breach with a 30-day cure period, and pro-rated refunds with no penalty fees in either case. We're open to negotiating notice period down toward 60 days if that better fits your governance cycle. |

We see all of the above as standard, resolvable negotiation points — not blockers to award — and we're ready to work through them on your timeline.

---

## 6. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| **Migration complexity** — 280TB, 30+ sources, live Teradata decommission through 2027 | Phased migration (Section 3.4) with a dedicated migration engineering pod, parallel-run periods before cutover, and an early first-production-workload milestone (week 5–10) to prove the pattern before scaling it. |
| **Analyst change management** — 600 Power BI users cannot experience disruption | Power BI DirectQuery adapter preserves existing report/dashboard investment; phased, domain-by-domain BI cutover rather than a big-bang switch; dedicated CSM through go-live. |
| **Real-time ingest validated at your actual peak, not just on paper** | We're tested to 250K events/sec, ~3x your 80K peak, but we recommend proving this on your real device telemetry during the PoC phase rather than taking headroom on faith. |
| **Query performance at full 280TB scale** | Sub-second SQL is proven on warmed caches up to 10TB; at 280TB total volume, performance depends on tiering the working set correctly. We recommend validating a hot/warm/cold storage design against your actual query patterns during the PoC. |
| **Predictive-maintenance latency requirements are not yet defined** | Our streaming query latency (250ms–1s) is not best-in-class for sub-100ms use cases. Since ML pipelines are "planned, not active," we recommend a short architecture review once latency requirements are known, well ahead of that program's start. |
| **Contractual terms as drafted (liability, IP, MFN, SLA-termination, audit, payment) diverge from what either side can execute against** | Addressed point-by-point in Section 5 with proposed resolutions. We recommend a focused contract working session in the first two weeks of negotiation so these don't become late-stage blockers against your 2026-06-30 award date. |
| **Discount gap versus your 35% floor** | Addressed in Section 4.1. We propose resolving this via a joint TCO exercise rather than a further headline discount, consistent with how we've closed this exact gap with comparable industrial customers. |

---

## 7. Next Steps

1. Joint working session to scope the 4–6 week PoC (real-time ingest + one Power BI domain) — fee credited to Year 1 if you proceed.
2. Contract working session covering Section 5 items, targeted for completion within two weeks of kickoff.
3. Reference calls with Initech Sensors and/or Globex Manufacturing, on request.
4. Finalize 3-year TCO comparison model using your actual workload figures (280TB, 12TB/month growth, 80K events/sec peak) to validate the commercial position in Section 4.

We appreciate the opportunity to respond and are ready to move at the pace your 2026-06-30 award timeline requires.

**Contact:** BTS-Synthetic Deal Desk, in response to procurement@acme-synthetic.example
