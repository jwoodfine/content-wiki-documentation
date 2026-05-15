---
schema: foundry-doc-v1
title: "bim-and-real-property-surfaces"
slug: bim-and-real-property-surfaces
category: applications
type: concept
quality: complete
short_description: "BIM and real-property surfaces describes how PointSav treats Building Information Modelling as a first-class operational domain, with dedicated design-system tooling, ISO 19650 record-keeping discipline, and Totebox archive patterns."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: bim-and-real-property-surfaces.es.md
references:
 - id: 1
 text: "International Organization for Standardization, ISO 19650-1:2018 — Organization and digitization of information about buildings and civil engineering works, including building information modelling (BIM). Part 1: Concepts and principles."
 url: "https://www.iso.org/standard/68078.html"
 - id: 2
 text: "buildingSMART International, Industry Foundation Classes (IFC) — the open BIM standard for building data exchange."
 url: "https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/"
---

BIM and real-property surfaces describes how the PointSav platform treats Building Information Modelling as a first-class operational domain within a real-estate customer deployment. The platform provides dedicated design-system tooling, ISO 19650 record-keeping conventions[^1], and [[totebox-os|Totebox]] archive patterns for real-property data. BIM components, tokens, and geospatial primitives live in a separate customer-tier design system (`woodfine-design-bim`) distinct from the vendor `pointsav-design-system` — this article summarises the integration points; the detailed BIM content is in `woodfine-design-bim`. By the end of this article, a reader will understand the two-design-system boundary, the ISO 19650 suffix discipline, and the [[archetypes-and-chart-of-accounts|Chart of Accounts]] placement for BIM contributors.

## Two design systems, deliberately separate

The single most important structural clarification: PointSav operates two distinct design systems, not one design system with a BIM sub-section.

| Design system | Repository | Audience | Domain |
|---|---|---|---|
| `pointsav-design-system` | `github.com/pointsav` (vendor) | PointSav contributors and fleet operators | UI and UX substrate for [[console-os\|os-console]], [[os-workplace]], and the full vendor OS family |
| `woodfine-design-bim` | `github.com/woodfine` (customer) | Architects, engineers, real-property operators | BIM tokens, IFC components[^2], geospatial visual primitives, real-property design system |

The two systems share authoring methodology — `foundry-draft-v1` frontmatter, the six-tier sovereignty structure, strict kebab-case naming — but they do not share content. The separation is structural: BIM concerns real property; the vendor design system concerns operating-system surfaces. Content or tokens that are specific to BIM workflows belong in `woodfine-design-bim`, never in `pointsav-design-system`.

The intended public deployment for `woodfine-design-bim` is `bim.woodfinegroup.com`. Full BIM component specifications, token definitions, and geospatial primitives are maintained there.

## ISO 19650 record-keeping suffix discipline

BIM document management operates under ISO 19650[^1], which defines explicit document-state codes for every artefact. The PointSav deployment adopts these codes as filename-suffix conventions so that audit tooling can read document state directly from the filename.

| Suffix | ISO 19650 status | Meaning |
|---|---|---|
| `_JW` | S0 | Work in progress — draft, not yet shared |
| `_FIN` | S4 | Final, shared for approval or coordination |
| `_PUB` | A0 | Published and approved for use |
| `_EXE` | CR | Executed or signed — record or as-constructed state |
| `_MCH` / `_DAT` | (matches parent) | Machine-readable version of the parent document |

Audit tooling reads the suffix and routes accordingly. A `_PUB` file is signed and treated as immutable; a `_JW` file is in flight and does not carry verified status. A `_EXE` file has passed operator confirmation and enters the [[totebox-os|Totebox]] archive as a sealed record.

The suffix discipline applies to every BIM artefact that enters the [[service-content|Gravity Engine]] — whether a drawing, a coordination model, a permit, or a lease record. This makes the record-keeping posture consistent with the broader [[worm-ledger-design|WORM ledger]] discipline across the platform.

## BIM contributors in the Chart of Accounts

In the institutional [[archetypes-and-chart-of-accounts|Chart of Accounts]], BIM-domain contributors occupy a specific structural socket:

| Profile | Domain | Sub-Domain | Anchor archetype |
|---|---|---|---|
| IT Support | Contributors | BIM | The Engineer |

This placement is not aesthetic. It determines how [[service-people]] sockets BIM contributors when their work product enters [[service-content]]. A BIM modeller, a BIM coordinator, and a structural engineer all occupy the Engineer archetype slot under IT Support → Contributors → BIM, which means the platform applies the same evaluator key (`logic_efficiency`) and the same task-routing logic to their output.

BIM contributors sit structurally adjacent to DevOps, Networking, Database, Backend, GIS, and IoT workers — all Engineer-archetype positions under IT Support. This adjacency means BIM work inherits the same computational treatment as other data-and-logic disciplines, rather than being classified under Compliance or Real Estate where a different archetype governs.

## BIM-adjacent operating-system surfaces

Three [[console-os|os-console]] surfaces are planned for BIM-domain work. All three are aspirational and carry appropriate forward-looking language.

| Planned surface | Function |
|---|---|
| `app-console-bim` | High-fidelity BIM viewer and review; intended to read IFC files via an IFC-native Rust library; renders B-rep geometry via a Rust geometry kernel |
| `app-console-bim` GIS variant | Geospatial overlay and analytics via a Rust-native whitebox toolset; intended to replace legacy C++ geospatial tooling |
| `app-console-bim` Maps Console | Spatial visualisation with a map-driven Console layout |

Each planned surface is single-purpose and Rust-native. The substrate design explicitly avoids legacy C++ BIM tooling, which carries decades of accumulated complexity and exceeds the hardware profiles of the lower Totebox tiers.

The [[app-console-input|F12 input gate]] handles BIM document ingestion — an operator drags an IFC or drawing file into F12, selects the Chart-of-Accounts destination, confirms the extracted entities, and the file enters the Totebox archive with an ISO 19650 suffix and a timestamped audit record.

## See also

- `woodfine-design-bim` — the customer-tier BIM design system (maintained separately at `github.com/woodfine`)
- [[archetypes-and-chart-of-accounts]] — the Chart of Accounts and eleven archetypes taxonomy
- [[totebox-os]] — the Totebox operating system that hosts real-property archives
- [[app-console-input]] — the F12 input gate through which BIM documents enter the platform
- [[service-content]] — the Gravity Engine that classifies and routes BIM documents
- [[worm-ledger-design]] — the WORM ledger substrate that seals real-property records
