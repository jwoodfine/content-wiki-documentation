---
schema: foundry-doc-v1
title: "BIM Object specification"
slug: bim-object-specification
language: en
category: substrate
index_group: core-named-substrates
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "The platform's reusable building-element specification unit: a fixed set of primitive categories anchored to open standards (IFC, Uniclass, bSDD), each carrying three layers of information at once — what it is, what its jurisdiction requires, and what its climate requires."
cites: [ifc-4-3, uniclass-2015, bsdd-v1]
paired_with: bim-object-specification.es.md
---

Building Information Modelling produces detailed digital representations of a structure, but a standard BIM model does not by itself prevent code violations — a model can be geometrically complete and still fail a jurisdiction's requirements, discovered only when a compliance check runs after the fact. A **BIM Object** is the platform's term for a building-element specification designed to carry its applicable code and performance requirements with it from the moment it's placed, so a violation is caught in the design itself rather than at a later inspection.

**Why it matters:** the substrate exists to make a class of defect structurally impossible to place, not merely easier to catch — the difference between a specification unit and a checklist.

## What distinguishes a BIM Object

A BIM Object differs from the building blocks it might be mistaken for. It is not a raw IFC entity type (which defines a data shape but carries no jurisdiction-specific requirements). It is not a proprietary, vendor-locked model-authoring format. It is not after-the-fact facility-management data captured once a model is complete. It combines three things at once: what the element is, what regulatory requirements it must satisfy in its jurisdiction, and what performance requirements it must meet for its climate zone — bundled into one reusable specification unit rather than checked separately after design.

## Primitive categories — the substrate

Every BIM Object belongs to one of a small, fixed set of primitive categories — spatial elements such as sites and storeys, physical elements such as walls and doors, materials, assemblies, building systems, performance thresholds, climate-zone requirements, and identity codes. Grouping objects this way means a category tells a practitioner what kind of thing an object describes before they open its full specification.

Each category anchors to the same open standards already used across the AEC industry: the IFC entity hierarchy for what an element is, Uniclass 2015 for how it is classified, and buildingSMART's Data Dictionary (bSDD) for a stable, tool-independent definition.

**Why it matters:** anchoring to open standards rather than a proprietary schema means an object's meaning does not depend on any one BIM authoring tool remaining in business — the specification stays legible and verifiable however long the building stands, and however many software vendors come and go over its life.

## Three composition layers

A BIM Object carries three layers of information at once: Specification, Regulation, and Climate Zone. None of the three is a choice a designer makes at design time. A building element has a fixed type, sits in a fixed jurisdiction, and performs in a fixed climate, so the object reflects all three as facts about its physical context rather than as user preferences.

| Layer | What it carries |
|---|---|
| Specification | The object's permanent identity — what kind of element it is, independent of where it is built |
| Regulation | The jurisdiction-specific legal requirements that apply where the building actually sits |
| Climate Zone | The performance requirements that follow from the building's physical climate, sourced from the applicable energy code |

Regulation and Climate Zone are each authored as a growing table of every registered requirement rather than a single value, because a jurisdiction or a climate zone is a fact about the site, not a setting a user selects. Regulatory requirements vary by jurisdiction and change as codes are updated; climate performance requirements vary by zone and change as energy codes are revised. Keeping these as separate layers, rather than folding them into a single number, means each concern can be tracked, sourced, and updated independently without disturbing the other two.

**Why it matters — the composition rule:** where a regulatory requirement and a climate-zone requirement both constrain the same property, the stricter of the two governs. Both layers express performance minimums, so the binding requirement is always whichever minimum is higher — a straightforward most-restrictive-wins rule, not a negotiated tradeoff.

## Where the specification lives

The full field-level schema, jurisdiction overlay structure, delivery format, and current implementation status behind this substrate are maintained directly at [bim.woodfinegroup.com](https://bim.woodfinegroup.com).

## See also

- [[building-design-system]] — the coordination layer this substrate is one of two layers of
- [[aec-interface-conventions]] — the shared interface vocabulary a BIM-capable surface exposes this substrate through
- [[asset-anchored-bim-vault]] — the archive that stores each BIM Object as a hash-addressed object
- [[flat-file-bim-leapfrog]] — the architectural constraints the whole BIM substrate is built on
