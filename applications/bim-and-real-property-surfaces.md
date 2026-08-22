---
schema: foundry-doc-v1
title: "BIM and real property surfaces"
slug: bim-and-real-property-surfaces
category: applications
type: concept
content_type: topic
quality: complete
index_group: domain-applications
short_description: "How PointSav treats Building Information Modelling as a distinct operational domain — a separate customer-tier design system, a real Chart of Accounts placement, and BIM-specific console surfaces still at the research stage."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
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

BIM and real-property surfaces describes how the PointSav platform treats Building Information Modelling as a distinct operational domain within a real-estate customer deployment. BIM components, tokens, and geospatial primitives live in a separate customer-tier design system (`woodfine-bim-library`) distinct from the vendor `pointsav-design-system` — this article summarises the integration points; the detailed BIM content is in `woodfine-bim-library`. By the end of this article, a reader will understand the two-design-system boundary, the platform's real Chart of Accounts placement for BIM contributors, and the current (research-stage) state of BIM-specific console surfaces.

## Two design systems, deliberately separate

The single most important structural clarification: PointSav operates two distinct design systems, not one design system with a BIM sub-section.

| Design system | Repository | Audience | Domain |
|---|---|---|---|
| `pointsav-design-system` | `github.com/pointsav` (vendor) | PointSav contributors and fleet operators | UI and UX substrate for [[os-console]], [[os-workplace]], and the full vendor OS family as described in the [[design-philosophy|design philosophy]] |
| `woodfine-bim-library` | `github.com/woodfine` (customer) | Architects, engineers, real-property operators | BIM tokens, IFC components[^2], geospatial visual primitives, real-property design system |

The two systems share authoring methodology — a common structured-metadata schema, the [[six-tier-sovereignty-matrix|six-tier sovereignty structure]], strict lowercase-hyphenated naming — but they do not share content. The separation is structural: BIM concerns real property; the vendor design system concerns operating-system surfaces. Content or tokens that are specific to BIM workflows belong in `woodfine-bim-library`, never in `pointsav-design-system`.

The intended public deployment for `woodfine-bim-library` is `bim.woodfinegroup.com`. Full BIM component specifications, token definitions, and geospatial primitives are maintained there.

## Document-status filename suffixes

Real-property source documents in the platform's working corpus carry filename suffixes such
as `_FIN` (final, shared for approval or coordination) and `_JW`/`_EXE` (draft and
executed/signed states), an informal convention that predates any platform tooling. Formalising
this as an ISO 19650[^1]-mapped, machine-read status system — with `service-bim` inspecting the
suffix and routing the document automatically — is a design intent for the BIM ingestion
pipeline, not a built capability today: `service-bim` exists only as research and design notes,
with no shipped ingestion, validation, or audit-routing code.

## BIM contributors in the Chart of Accounts

The institutional [[archetypes-and-chart-of-accounts|Chart of Accounts]] carries a real entry
for BIM work: category **IT Support**, type **BIM** (reference `6010`), matched by keywords
including `bim`, `building information modeling`, `digital twin`, `revit`, and `ifc`. BIM
contributors sit in the same category as other technical-execution roles rather than under
Compliance or Real Estate, where different categories apply.

## BIM-adjacent operating-system surfaces

BIM-domain work on [[os-console]] is at the research stage — a design document exists
(`app-console-bim`), no code has shipped. The intended shape, per that research: a single
routing-and-coordination terminal (`app-console-bim`) distinct from an authoring surface
(`app-workplace-bim`) — the split matches the platform's console/workplace distinction
elsewhere, view-and-link versus create-and-edit. `app-console-bim` would query elements, link
work orders, and create issues; it would not edit BIM geometry. For portfolios spanning
multiple properties, a stateless aggregation layer (`app-orchestration-bim`) is intended to
federate queries across property archives rather than store data itself. The research
document's current technical direction favors browser-based IFC rendering (evaluating
`xeokit-sdk` and `@thatopen/components`) over a native Rust geometry kernel — none of this is
committed or built, and the direction may change before implementation starts.

## See also

- `woodfine-bim-library` — the customer-tier BIM design system (maintained separately at `github.com/woodfine`)
- [[archetypes-and-chart-of-accounts]] — the Chart of Accounts and eleven archetypes taxonomy
- [[totebox-os]] — the Totebox operating system real-property archives run on
- [[app-console-input]] — the platform's general document-ingestion gate
- [[service-content]] — the platform's document classification and taxonomy service
- [[worm-ledger-design]] — the platform's immutable-record ledger design
