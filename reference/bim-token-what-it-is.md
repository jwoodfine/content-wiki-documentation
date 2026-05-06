---
schema: foundry-doc-v1
title: "What Is a BIM Token"
slug: bim-token-what-it-is
category: reference
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: []
paired_with: bim-token-what-it-is.es.md
---

Building Information Modelling (BIM) produces detailed digital representations of structures — but standard BIM does not prevent violations. A model can be geometrically complete, materially specified, and classified by IFC entity type while still containing elements that fail code compliance, violate climate performance floors, or conflict with jurisdictional regulation. These failures are discovered only when a post-design checker runs. A BIM Token addresses this upstream: it encodes a built-environment element decision as a composable, aliasable specification unit that pre-constrains the design space rather than auditing a completed model. The concept was formalised in 2026 as part of the BIM Token platform (Doctrine claim #40), and the Specification layer is complete at v0.0.1 with Regulation and Climate Zone layers in active development.

## Definition

A BIM Token is a composable built-environment specification unit — the structural counterpart of a Design System Token. Where a Design System Token encodes a design decision (a colour, a spacing unit, a component recipe) as a reusable, aliasable value that all conforming surfaces must honour, a BIM Token encodes a built-environment element decision across three simultaneous axes:

1. **What the element IS** — its IFC entity class, Uniclass 2015 classification, bSDD identity URI, and applicable property set templates.
2. **What it MUST satisfy** — the regulatory requirements imposed by its jurisdiction, expressed as jurisdictional overlays (IDS 1.0 constraint files and IFC geometric exclusion fragments).
3. **How it MUST perform** — the energy, thermal, structural, and acoustic requirements imposed by its climate zone, expressed as tabular performance parameters keyed to ASHRAE and equivalent national standards.

Placing a BIM Token in a model simultaneously places the element, its regulatory envelope, and its climate performance floor. Violations are geometrically impossible by construction rather than discovered in post-design review.

## What a BIM Token Is Not

Precision requires distinguishing the BIM Token from four structures it superficially resembles.

**Not an IFC entity type.** IFC 4.3 (ISO 16739-1:2024) defines `IfcWall`, `IfcSlab`, `IfcBeam`, and approximately 900 other schema classes. An IFC entity type is a schema class — it defines what data shape a wall record must conform to. It carries no constraint values, no jurisdiction-specific requirements, and no performance parameters. A BIM Token uses the IFC entity class as its identity anchor but adds the three constraint layers the schema class cannot hold.

**Not a proprietary BIM Family format.** Proprietary BIM Family formats are geometry parameterised for a specific authoring tool, stored in a vendor-specific binary format, and tool-locked. They carry no normative regulatory data, no jurisdiction mapping, and no climate zone performance specification. They cannot be read by other tooling without export. A BIM Token is plain JSON (W3C DTCG format), tool-neutral, and machine-readable by any conformant consumer.

**Not a COBie spreadsheet.** COBie (Construction Operations Building Information Exchange) is after-the-fact data capture — facility management data extracted from a model after design is complete. It documents what was built. A BIM Token constrains what may be placed.

**Not an IFC Property Set.** An IFC Property Set (`Pset_WallCommon`, etc.) is a template for values without enforcement logic, constraint hierarchy, or jurisdiction mapping. It records properties; it does not enforce them. A BIM Token includes applicable property set definitions but adds the regulatory and climate zone enforcement layers that property sets cannot express.

**Not a BIM model file.** An IFC model is a geometry instance for a specific project. A BIM Token is a reusable specification — a template that generates conformant geometry instances when instantiated. The relationship is analogous to a Design System component recipe to a rendered DOM node.

## The Pre-Constraining Thesis

Two decades of BIM tooling have been built on a validation-first assumption: design freely, then check. Commercial validation platforms run rules against completed models and report violations. Singapore's CORENET X — the most advanced government BIM submission system in production — operates on the same principle: submit a model, receive a compliance report.

The pre-constraining approach inverts this. If the only elements available to a designer are BIM Tokens, and each token already encodes the regulatory and performance constraints applicable to its type in a given jurisdiction and climate zone, then the compliance report is structurally unnecessary. The model cannot be non-compliant because non-compliant configurations cannot be placed.

This is a compositional claim, not a validation claim. The distinction matters because validators generate reports that require human remediation. A composition system that enforces constraints at placement time has no violations to report.

## Three Layers

A BIM Token has three layers. All three are data embedded in the token. Neither Regulation nor Climate Zone is a runtime user-selectable option — they are reference data displayed as static lookup tables, exactly as a technical standard datasheet shows multiple jurisdiction rows simultaneously.

**Layer 1 — Specification.** The IFC entity class (e.g., `IfcWall`), Uniclass 2015 classification reference (e.g., `Ss_20_05_30_75`), bSDD concept URI, plain-language description, and applicable property set templates. This layer is the token's permanent identity.

**Layer 2 — Regulation.** A table of registered jurisdictional overlays. Each row is one overlay: jurisdiction, standard, constraint type, required value, source authority, and IDS 1.0 file path. Where an overlay includes an IFC geometric exclusion fragment, that fragment takes unconditional precedence over any numeric constraint.

**Layer 3 — Climate Zone.** A table of registered climate zone performance requirements. Each row is one registered zone: zone identifier (aligned to ASHRAE 90.1 or national equivalent), performance parameter, required value, unit, and source standard. Where a climate zone row conflicts with a Regulation row for the same parameter, the more restrictive value applies.

**Composition rule:** `effective_value = max(regulation_requirement, climate_zone_requirement)` where both express lower bounds. Geometric exclusion fragments override numeric constraints unconditionally. When a layer has no registered data for a given element type, the token remains valid and serves specification-only.

See [[bim-token-three-layers]] for the full layer specification.

## Implementation Form

BIM Tokens are stored as W3C Design Token Community Group (DTCG) format JSON, extended with BIM-specific token types. The `$type` field is extended beyond the DTCG core set to include `bim-element`, `bim-material`, `bim-assembly`, and related AEC-specific types. The standard DTCG aliasing mechanism (`{token.reference}`) is preserved, enabling BIM tokens to reference each other compositionally — a curtain wall assembly token can alias its glazing unit token, its mullion profile token, and its thermal break token.

The machine-readable format enables:
- Tooling integration: any BIM authoring tool with a DTCG parser can consume BIM Tokens without proprietary plugin development.
- Regulatory versioning: jurisdictional overlays are versioned separately from the specification layer, allowing a jurisdiction to update its constraint rows without breaking the token's identity.
- Offline operation: a complete vault of BIM Tokens is a directory of JSON files, cloneable via git and queryable without network access — a prerequisite for ITAR-restricted, GDPR-sovereign, and construction-site use cases.

## Relationship to the Design System

The BIM Token system parallels the structure of a software design system. Where software design systems provide a token primitive layer (colours, spacing, typography), a component recipe layer, and a surface-specific extension layer, the BIM Token platform provides a token primitive layer (eight DTCG token categories anchored to IFC 4.3), a universal AEC component layer (spatial tree, properties panel, viewport renderer), and surface-specific extensions per built-environment programme type.

The analogy is structural, not metaphorical. Both systems address the same problem: enforcing consistency across independent authoring surfaces by encoding decisions as reusable, aliasable, versionable units with machine-readable constraint specifications. The BIM platform extends the model into a physical constraint domain that software design systems do not address.

## See Also

- [[bim-token-three-layers]]
- [[building-design-system-bim]]
- [[city-code-as-composable-geometry]]
- [[flat-file-bim-leapfrog]]
- [[bim-token-taxonomy]]

## References

- IFC 4.3 (ISO 16739-1:2024) — buildingSMART International
- Uniclass 2015 — NBS / RIBA Enterprises
- buildingSMART Data Dictionary (bSDD) — buildingSMART International
- IDS 1.0 (Information Delivery Specification) — buildingSMART International
- W3C Design Token Community Group (DTCG) format — W3C

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
