---
schema: foundry-doc-v1
title: "BIM objects — what they are"
slug: bim-objects-what-they-are
short_description: "BIM Objects are composable built-environment specification units that encode element type, regulatory requirements by jurisdiction, and climate zone performance requirements, pre-constraining the design space so non-compliant configurations cannot be placed."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, dtcg-w3c]
paired_with: bim-objects-what-they-are.es.md
---

Building Information Modelling produces detailed digital representations of structures. It does not, in its standard form, prevent violations. A model can be geometrically complete, materially specified, and classified by IFC entity type while still containing elements that fail code compliance, violate climate performance floors, or conflict with jurisdictional regulation — discoveries made only when a post-design checker runs. A BIM Object addresses this upstream. It encodes a built-environment element decision as a composable, aliasable specification unit that pre-constrains the design space rather than auditing a completed model. See also [[bim-objects-substrate|BIM object categories]] and [[building-design-system-bim|the Building Design System]].

## Definition

A BIM Object is a composable built-environment specification unit — the structural counterpart of a [[design-system-substrate|Design System Token]]. Where a Design System Token encodes a design decision (a [[design-color|colour]], a [[design-spacing|spacing unit]], a component recipe) as a reusable, aliasable value that all conforming surfaces must honour, a BIM Object encodes a built-environment element decision across three simultaneous axes:

1. **What the element IS** — its IFC entity class, Uniclass 2015 classification, bSDD identity URI, and applicable property set templates.
2. **What it MUST satisfy** — the regulatory requirements imposed by its jurisdiction, expressed as jurisdictional overlays (IDS 1.0 constraint files and IFC geometric exclusion fragments).
3. **How it MUST perform** — the energy, thermal, structural, and acoustic requirements imposed by its climate zone, expressed as tabular performance parameters keyed to ASHRAE and equivalent national standards.

Placing a BIM Object in a model simultaneously places the element, its regulatory envelope, and its climate performance floor. Violations are geometrically impossible by construction rather than discovered in post-design review.

## What a BIM Object Is Not

Precision requires distinguishing the BIM Object from four structures it superficially resembles.

**Not an IFC entity type.** IFC 4.3 (ISO 16739-1:2024) defines `IfcWall`, `IfcSlab`, `IfcBeam`, and approximately 900 other schema classes. An IFC entity type is a schema class — it defines what data shape a wall record must conform to. It carries no constraint values, no jurisdiction-specific requirements, and no performance parameters. A BIM Object uses the IFC entity class as its identity anchor but adds the three constraint layers the schema class cannot hold.

**Not a Revit Family.** A Revit Family is geometry parameterised for one authoring tool, stored in a proprietary binary format, and vendor-locked. It carries no normative regulatory data, no jurisdiction mapping, and no climate zone performance specification. It cannot be read by non-Revit tooling without export. A BIM Object is plain JSON (W3C DTCG format), tool-neutral, and machine-readable by any conformant consumer.

**Not a COBie spreadsheet.** COBie (Construction Operations Building Information Exchange) is after-the-fact data capture — facility management data extracted from a model after design is complete. It documents what was built. A BIM Object constrains what may be placed.

**Not an IFC Property Set.** An IFC Property Set (`Pset_WallCommon`, etc.) is a template for values without enforcement logic, constraint hierarchy, or jurisdiction mapping. It records properties; it does not enforce them. A BIM Object includes applicable property set definitions but adds the regulatory and climate zone enforcement layers that property sets cannot express.

**Not a BIM model file.** An IFC model is a geometry instance for a specific project. A BIM Object is a reusable specification — a template that generates conformant geometry instances when instantiated. The relationship is analogous to a Design System component recipe to a rendered DOM node.

## The Pre-Constraining Thesis

Two decades of BIM tooling have been built on a validation-first assumption: design freely, then check. Solibri, Archistar, and similar platforms run rules against completed models and report violations. Singapore's CORENET X — the most advanced government BIM submission system in production — operates on the same principle. Submit a model; receive a compliance report.

The pre-constraining approach inverts this. If the only elements available to a designer are BIM Objects, and each BIM Object already encodes the regulatory and performance constraints applicable to its type in a given jurisdiction and climate zone, then the compliance report is structurally unnecessary. The model cannot be non-compliant because non-compliant configurations cannot be placed.

This is a compositional claim, not a validation claim. The distinction matters because validators generate reports that require human remediation. A composition system that enforces constraints at placement time has no violations to report.

## Three Layers

A BIM Object has [[bim-objects-three-layers|three layers]]. All three are data embedded in the object. Neither Regulation nor Climate Zone is a runtime user-selectable option — they are reference data displayed as static lookup tables, exactly as a technical standard datasheet shows multiple jurisdiction rows simultaneously.

**Layer 1 — Specification.** The IFC entity class (e.g., `IfcWall`), Uniclass 2015 classification reference (e.g., `Ss_20_05_30_75`), bSDD concept URI, plain-language description, and applicable property set templates. This layer is the BIM Object's permanent identity.

**Layer 2 — Regulation.** A table of registered jurisdictional overlays. Each row is one overlay: jurisdiction, standard, constraint type, required value, source authority, and IDS 1.0 file path. Where an overlay includes an IFC geometric exclusion fragment (a solid geometry encoded as IFC that the element must not occupy), that fragment takes unconditional precedence over any numeric constraint.

**Layer 3 — Climate Zone.** A table of registered climate zone performance requirements. Each row is one registered zone: zone identifier (aligned to ASHRAE 90.1 or national equivalent), performance parameter, required value, unit, and source standard. Where a climate zone row conflicts with a Regulation row for the same parameter, the more restrictive value applies.

**Composition rule:** `effective_value = max(regulation_requirement, climate_zone_requirement)` where both express lower bounds. Geometric exclusion fragments override numeric constraints unconditionally. When a layer has no registered data for a given element type, the BIM Object remains valid and serves specification-only.

## Implementation Form

BIM Objects are stored as W3C Design Token Community Group (DTCG) format JSON, extended with BIM-specific object types. The `$type` field is extended beyond the DTCG core set to include `bim-element`, `bim-material`, `bim-assembly`, and related AEC-specific types. The standard DTCG aliasing mechanism (`{token.reference}`) is preserved, enabling BIM Objects to reference each other compositionally — a curtain wall assembly BIM Object can alias its glazing unit BIM Object, its mullion profile BIM Object, and its thermal break BIM Object.

The machine-readable format enables:
- Tooling integration: any BIM authoring tool with a DTCG parser can consume BIM Objects without proprietary plugin development.
- Regulatory versioning: jurisdictional overlays are versioned separately from the specification layer, allowing a jurisdiction to update its constraint rows without breaking the object's identity.
- Offline operation: a complete vault of BIM Objects is a directory of JSON files, cloneable via git and queryable without network access — a prerequisite for ITAR-restricted, GDPR-sovereign, and construction-site use cases.

## Relationship to the Design System

The BIM Object system parallels the structure of a software [[design-system-substrate|design system]]. Where IBM Carbon or a similar system provides a token primitive layer ([[design-color|colours]], [[design-spacing|spacing]], [[design-typography|typography]]), a component recipe layer (button, card, navigation), and a surface-specific extension layer (mobile, web, print), the BIM Object platform provides an object primitive layer (the 8 DTCG object categories anchored to IFC 4.3), a universal [[aec-interface-conventions|AEC component layer]] (spatial tree, properties panel, viewport renderer), and surface-specific extensions per built-environment programme type.

The analogy is structural, not metaphorical. Both systems address the same problem: enforcing consistency across independent authoring surfaces by encoding decisions as reusable, aliasable, versionable units with machine-readable constraint specifications. The BIM platform extends the model into a physical constraint domain that software design systems do not address.

## See also

- [[bim-objects-three-layers]] — how the three composition layers (Specification, Regulation, Climate Zone) are structured
- [[bim-objects-substrate]] — the eight BIM Object primitive categories and their IFC entity anchors
- [[building-design-system-bim]] — the broader Building Design System for the built environment
- [[flat-file-bim-leapfrog]] — the flat-file substrate that makes pre-constraining composition possible
