---
schema: foundry-doc-v1
title: "Gravity engine"
slug: service-content
category: services
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: service-content.es.md
short_description: "service-content is the synthesis engine of the PointSav family — the Gravity Engine that reads raw payloads from a Totebox, runs them against an institutional taxonomy, and generates the structured documents an organisation publishes."
cites: []
references:
 - id: 1
 text: "Aho, A. V. & Corasick, M. J. 'Efficient String Matching: An Aid to Bibliographic Search.' Communications of the ACM, 18(6):333–340, 1975."
 url: "https://dl.acm.org/doi/10.1145/360825.360855"
 - id: 2
 text: "ILO. 'ISCO-08: International Standard Classification of Occupations.' International Labour Organization, 2012."
 url: "https://www.ilo.org/public/english/bureau/stat/isco/isco08/"
---

`service-content` is the synthesis engine of the PointSav family. It reads raw payloads from inside a Totebox, runs them against an institutional taxonomy, produces dense Gravity Vectors, and ultimately generates the documents an organisation publishes — wikis, news releases, due-diligence ledgers, internal memos. It is the difference between a file store and an active intelligence engine. This article covers the Four-Pillar Seed Vault, the Gravity Engine pipeline, the Stratified Ontology, and the human-in-the-loop boundary that governs what the engine can write autonomously.

## The Four-Pillar Seed Vault

Every Totebox is provisioned with four JSON ledgers that form the institutional grammar of the system — the Seed Vault. The Seed Vault is built once, locked, and adjusted only by operators, not by AI:

| Pillar | What it captures | Example |
|---|---|---|
| Entities | The "who" — every individual, organisation, email, and phone number extracted from payloads | A Sovereign-ID keyed to a specific contact's email hash |
| Archetypes | The "logos" — eleven functional personas (Executive, Guardian, Fiduciary, Architect, Engineer, Artisan, Constructor, Catalyst, Envoy, Steward, Sage) | A façade consultant maps to "The Engineer" |
| Chart of Accounts | The "where" — the rigid hierarchical structure of the organisation (Profile → Domain → Sub-Domain) | Construction → Collaborators → Façade Consultants |
| Domains | The "what" — the localised vocabulary and glossary terms in use | "Direct-Hold Solution" |

A fifth pillar, Themes, captures the multidimensional undercurrents emerging from the corpus — recurring topics and institutional concerns that are flagged and proposed to operators for approval.

## The Gravity Engine pipeline

When a payload arrives (an email, a PDF, a DOCX), the engine performs a tight, deterministic sequence:

1. **Ingest.** `service-email` (or the [[app-console-input|Input Machine]]) writes the raw payload to the Totebox's WORM vault. Nothing is mutated yet.
2. **Entity extraction.** `service-extraction` runs Aho-Corasick over the raw text and pulls out every name, email, phone number, and organisation. [^1] Each gets a deterministic Sovereign-ID and begins in `Discovery` status.
3. **Gravity calculation.** `service-content` loads the four pillars, fuses them into a single search automaton, and extracts only sentences containing structural keywords. A 5 MB payload becomes a 50-word Gravity Vector.
4. **Verification.** The vector and the entity bundle pass to `service-slm`, which evaluates whether the payload aligns with the institution's taxonomy. The output is a single token — `VALID` or `REJECT`.
5. **Routing.** Verified payloads go to deep storage; rejected payloads go to quarantine. Verified entities have their `Discovery` status upgraded and are socketed to the Chart of Accounts.

## The Stratified Ontology

`service-content` organises information in a five-layer stack, with three derivative engines on top:

| Layer | What it holds |
|---|---|
| L0 — Base Geometry | Raw files (`/source`, `/assets`, `/ledger`) — immutable, local |
| L1/L2 — Raw Graph | Blind 100% extraction into a JSONL knowledge graph |
| L3 — Global Anchors | Universal standards (IFRS/GAAP for finance, O*NET/ISCO for personnel) [^2] |
| L4 — Sovereign Taxonomy | The institution's bespoke operational reality — Domains, Glossaries, Topics |
| L5 — Verification Crust | The human-in-the-loop truth ledger; outputs from operator-verified content only |

| Derivative | What it produces |
|---|---|
| D1 — Thematic Quant | Foresight: monitors graph inflow and surfaces emerging themes for operator review |
| D2 — Linguistic Protocols | Behavioural constraints — TRANSLATE, MEMO, COMMS, TEXT, LEGAL protocols |
| D3 — Content Creation | Final artefacts: HTML wikis, PDF ledgers, news releases — generated from L5 truth |

## Self-healing

The Gravity Engine is self-healing in a specific, narrow sense: its own outputs feed back into its inputs. A successfully synthesised memo becomes new content the engine indexes the next time it runs. Over months, the Domain glossaries grow, the Themes track real institutional concerns, and the engine's syntheses converge on the institution's actual voice. This is not autonomous model fine-tuning — the improvement is corpus-level: the engine has more verified material to draw from.

## The human-in-the-loop boundary

`service-content` does not publish to verified ledgers autonomously. Every L5 entry must transit a human-in-the-loop verification step — either through the [[app-console-input|Input Machine]] (F12) or through the content review surface — before it can be written to a verified ledger. This satisfies [[architecture-decisions|SYS-ADR-07]] (no structured data through AI) and [[architecture-decisions|SYS-ADR-19]] (no automated AI publishing to verified ledgers).

## See also

- [[service-slm]] — the local small language model that produces `VALID`/`REJECT` decisions
- [[service-people]] — the identity ledger that receives socketed entities from the Gravity Engine
- [[archetypes-and-chart-of-accounts]] — the institutional taxonomy that forms the Seed Vault's structure
- [[app-console-input]] — the F12 Input Machine; the human-gated ingest surface
- [[totebox-os]] — the Totebox that hosts service-content and its WORM storage
