---
schema: foundry-doc-v1
title: "Ontological governance"
slug: ontological-governance
category: governance
type: topic
content_type: topic
quality: complete
short_description: "Ontological governance describes the four self-healing control ledgers that govern how service-content classifies and accumulates knowledge, and the human-verification loop that keeps extracted identity data accurate before it is permanently committed."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-19
editor: pointsav-engineering
cites: []
paired_with: ontological-governance.es.md
---


Automated classification systems drift over time — categories multiply, vocabulary fractures, and extracted data accumulates errors faster than they can be corrected. **Ontological governance** prevents this through two structural mechanisms: four throttled control ledgers that define classification vocabulary at intentionally slow update rates, and a human-verification loop that forces extracted identity fragments through human review before they are permanently written into the verified ledger. These two mechanisms are structurally separate but serve the same goal: preventing accumulated classification drift from undermining the integrity of long-lived institutional data. For a regulated operator, this means the platform's knowledge graph remains auditable and its identity records remain accurate without continuous manual curation.

## The three-stage extraction pipeline

Data extraction across the platform is mechanically isolated into
three services:

1. **[[service-email]] (ingestion).** Processes MIME payloads and
 deposits raw text and CSV files into the spool. No
 classification is applied at this stage.
2. **[[service-people]] (identity resolution).** Scans the spool
 for human identity clusters and routes them to the verification
 surveyor before committing to the verified ledger.
3. **[[service-content]] (linguistic classification).** Scans the
 spool for narrative knowledge and cross-references text against
 the four control ledgers.

## The four control ledgers

`service-content` is governed by four CSV ledgers that update at
heavily throttled rates to preserve longitudinal data stability:

| Ledger | Minimum update interval | Governs |
|---|---|---|
| [[archetypes-and-chart-of-accounts|Archetypes]] | More than 24 months | The psychological and functional identity of the firm (for example, "The Fiduciary") |
| [[archetypes-and-chart-of-accounts|Chart of Accounts]] | 18–24 months; requires executive override | The structural and financial geometry of the operation (for example, "Compliance", "IT Support") |
| Domains | More than 12 months | Bilingual glossaries defining the macro-categories: Corporate (Finance), Projects (Real Estate), Documentation (Technology) |
| Themes | 3–8 months | The active frontline narratives (for example, "Co-Location Expansion") |

Update rates are intentionally asymmetric. The slowest ledgers
(Archetypes, Chart of Accounts) capture what the firm fundamentally
is; the fastest (Themes) capture what it is currently working on.
Premature updates to the slower ledgers corrupt the longitudinal
coherence of the data corpus.

## The verification loop

`service-people` uses a human-in-the-loop verification step to prevent automated extraction errors from entering the verified ledger. The process is described in detail at [[verification-surveyor|Verification Surveyor]]. In brief: the system isolates unverified identity fragments for operator review; the operator verifies each entity using their own personal browser and off-network lookup; the verified result is then committed to the ledger. The daily throughput limit ensures that operator attention remains high-fidelity rather than habitual.

## Why asymmetric update rates matter for regulated operators

The asymmetric ledger structure produces a property that matters in regulated contexts: the base of the knowledge graph is stable enough to audit. A procurement evaluator or compliance reviewer reading data extracted two years ago and data extracted last week will find them classified against the same Archetypes and Chart of Accounts taxonomy — the categories have not drifted. Only the Themes layer, which updates most frequently, reflects the current operational focus.

For financial disclosure purposes, this means that the platform's knowledge graph does not introduce spurious variation into the record. Consistent classification over time is not a side effect of discipline; it is a structural property enforced by the update-rate ledger. An auditor querying "what has this firm classified as Compliance over the past three years" receives a meaningful answer because the category boundaries have not shifted underneath the data.

## See also

- [[verification-surveyor|Verification Surveyor]] — the human-in-the-loop agent that verifies identity fragments before they enter the ledger
- [[archetypes-and-chart-of-accounts]] — the two slowest-updating control ledgers that define firm identity and financial geometry
- [[message-courier|Message Courier Service]] — the routing substrate that delivers inbound communications to service-email
- [[moonshot-initiatives|Moonshot Initiatives]] — engineering program to replace quarantined dependencies that ontological governance depends on
- [[worm-ledger-design]] — the append-only storage substrate that makes the verified ledger authoritative
