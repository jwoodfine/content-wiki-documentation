---
schema: foundry-doc-v1
title: "Archetypes and chart of accounts"
slug: archetypes-and-chart-of-accounts
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-2-knowledge-and-processing
short_description: "The Chart of Accounts and eleven archetypes are two reference taxonomies service-content loads into the knowledge graph, giving every classified entity a structural category and a functional signature."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: archetypes-and-chart-of-accounts.es.md
references:
  - id: 1
    text: "IFRS Foundation, IAS 1 — Presentation of Financial Statements, §54–76: Statement of Financial Position — line-item and sub-classification requirements for accounts."
    url: "https://www.ifrs.org/issued-standards/list-of-standards/ias-1-presentation-of-financial-statements/"
  - id: 2
    text: "International Labour Organization, International Standard Classification of Occupations 2008 (ISCO-08): Conceptual Framework and Methodology. ILO, Geneva, 2012."
    url: "https://www.ilo.org/public/english/bureau/stat/isco/docs/publication08.pdf"
---

The Chart of Accounts and the eleven archetypes are two reference taxonomies [[service-content]] maintains as CSV files and loads into the knowledge graph as static entities. Together they give every classified document or entity two independent labels: where it sits in an institutional structure, and what functional role it plays. A reader who only needs the vocabulary can stop after the two tables below; a reader who wants to see how the platform actually uses them should continue to the Verification Surveyor section.

## Two reference tables, two dimensions

| Table | Real shape | What it captures |
|---|---|---|
| Chart of Accounts | `reference_number`, `category`, `type`, `gravity_keywords` — a flat, two-level list, not a deep hierarchy | Structural position: which institutional category (Personal, Compliance, Real Estate, Construction, and others) and which specific type within it |
| Eleven Archetypes | `id`, `name`, `signature`, `healing_trigger`, `gravity_keywords` — one row per archetype | Functional role: what a person or entity does, independent of job title |

A small sample of the real Chart of Accounts:

| Reference | Category | Type |
|---|---|---|
| 1001 | Personal | Director |
| 2001 | Compliance | Counsel |
| 2002 | Compliance | Accounting |
| 3003 | Real Estate | Office Leasing |

The Chart is flat by design — a category and a type, nothing deeper. There is no separate "Domain" or "Sub-Domain" layer; the type field carries that level of specificity directly.

## The eleven archetypes

Each archetype row carries a name and a short signature. It also carries a "healing trigger" — the failure mode the archetype is defined against:

| Archetype | Signature | Healing trigger |
|---|---|---|
| The Executive | Strategic Direction | Stagnation |
| The Guardian | Risk & Compliance | Breach |
| The Fiduciary | Resource Integrity | Leakage |
| The Architect | System Design | Complexity |
| The Engineer | Technical Execution | Friction |
| The Artisan | Creative Precision | Homogeneity |
| The Constructor | Physical Realization | Structural Gap |
| The Catalyst | Growth & Momentum | Inertia |
| The Envoy | External Synergy | Friction |
| The Steward | Asset Preservation | Degradation |
| The Sage | Knowledge & Vision | Ignorance |

Both tables also carry a `gravity_keywords` column — a pipe-separated list of terms associated with the row (a Guardian's keywords include "compliance," "counsel," "audit," "legal"). This column exists in the data today as reference vocabulary; no classification code currently matches incoming text against it automatically.

## How the taxonomy reaches the knowledge graph

[[service-content]] exposes a small admin API that reads each CSV file and loads its rows into the graph as static entities. The eleven archetype rows load as `classification: "archetype"`, the Chart of Accounts rows as `classification: "coa-profile"`, both tagged with a dedicated `__taxonomy__` module so they're distinguishable from entities extracted from real documents. Reloading either file replaces the prior set of rows rather than appending to it.

## Where the archetype label is actually applied

The archetype taxonomy's one confirmed point of use today is the [[verification-surveyor|Verification Surveyor]] tool. When an operator manually verifies an extracted entity's identity, the tool prompts them to pick one of the eleven archetypes from the ontology file and records that choice as a claim on the entity, alongside the verification timestamp and source URL. This is a human decision made once per entity during review — not an automated inference, and not a mechanism that evaluates or scores a person's ongoing behaviour against their archetype. The Chart of Accounts categories are not part of this workflow; only the archetype selection is.

## See also

- [[service-content]] — the service that owns both CSV files and loads them into the knowledge graph
- [[verification-surveyor]] — the tool where an operator applies an archetype label to a verified entity
- [[service-extraction]] — the extraction engine that produces the entities a Verification Surveyor session reviews
