---
schema: foundry-doc-v1
title: "Ontological governance"
slug: ontological-governance
category: governance
type: topic
content_type: topic
quality: complete
index_group: platform-disciplines
short_description: "Four reference vocabulary ledgers kept deliberately narrow, plus a human-verification loop that reviews extracted identity fragments before they enter the verified ledger."
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
paired_with: ontological-governance.es.md
---


Automated classification systems drift over time — categories multiply, vocabulary fractures, and extracted data accumulates errors faster than they can be corrected. **Ontological governance** is this platform's answer: a small set of reference vocabulary ledgers, kept deliberately narrow, plus a human-verification loop that forces extracted identity fragments through human review before they are permanently written into the verified ledger. For a regulated operator, this means the platform's identity records stay accurate without continuous automated re-classification.

## The four vocabulary ledgers

[[service-content]] serves four CSV reference ledgers over a config HTTP endpoint (`/v1/config/*`):

| Ledger | Governs |
|---|---|
| [[archetypes-and-chart-of-accounts|Archetypes]] | Named functional roles a firm can occupy (for example, "The Fiduciary", "The Guardian") |
| [[archetypes-and-chart-of-accounts|Chart of Accounts]] | The firm's personnel-role taxonomy (for example, "Compliance", "IT Support") |
| Domains | Bilingual glossaries defining the platform's three subject-matter macro-categories: Corporate (Finance), Projects (Real Estate), Documentation (Technology) |
| Themes | Named active initiatives (for example, "Co-Location Mandate Expansion") |

These are reference vocabulary, not an automated classifier — no code cross-references incoming content against the ledgers' keywords to assign a category. The one confirmed consumer is [[verification-surveyor|Verification Surveyor]], where an operator manually tags an entity against the Archetypes/Chart of Accounts vocabulary during human review. Keeping the vocabulary small and infrequently revised is an editorial practice, not a rate-limited or code-enforced property of the ledgers themselves.

## The verification loop

[[service-people]] uses a human-in-the-loop verification step to prevent automated extraction errors from entering the verified ledger. The process is described in detail at [[verification-surveyor|Verification Surveyor]]. In brief: the system isolates unverified identity fragments for operator review; the operator verifies each entity using their own personal browser and off-network lookup; the verified result is then committed to the ledger. The daily throughput limit ensures that operator attention remains high-fidelity rather than habitual.

## Why a stable vocabulary matters for regulated operators

A small, infrequently-revised vocabulary produces a property that matters in regulated contexts: the base of the knowledge graph stays legible to audit. A procurement evaluator or compliance reviewer reading data classified against the Archetypes and Chart of Accounts vocabulary a year apart finds the same category names in use — the taxonomy has not fragmented underneath the data.

For financial disclosure purposes, this means that the platform's identity records do not introduce spurious variation into the record. An auditor querying "what has this firm classified as Compliance over the past three years" receives a meaningful answer because the category names have not shifted underneath the data.

## See also

- [[verification-surveyor|Verification Surveyor]] — the human-in-the-loop agent that verifies identity fragments before they enter the ledger, and the one confirmed consumer of the Archetypes/Chart of Accounts vocabulary
- [[archetypes-and-chart-of-accounts]] — the two ledgers that define firm identity and personnel-role taxonomy
- [[worm-ledger-design]] — the append-only storage that makes the verified ledger authoritative
