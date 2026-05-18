---
schema: foundry-doc-v1
title: "BIM Objects — Substrate"
slug: bim-objects-substrate
short_description: "BIM Objects anchor to the IFC 4.3 entity hierarchy, Uniclass 2015 classification, and bSDD URIs, organizing into eight primitive categories that encode spatial, elemental, material, assembly, system, performance, and climate-zone specifications."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, dtcg-w3c]
paired_with: bim-objects-substrate.es.md
---

The Building Design System BIM Object library anchors every object to a node in the IFC 4.3 entity hierarchy, classified by Uniclass 2015, and published as a dereferenceable bSDD URI. This article describes how the three-layer reference system works, what the eight BIM Object primitive categories encode, and how a BIM operator reads and applies them when authoring an IFC file.

## Three Layers of Reference

### Layer 1 — IFC 4.3 entity hierarchy

IFC 4.3 was published as ISO 16739-1:2024 in April 2024. The standard defines a hierarchy of named entity classes — `IfcSite`, `IfcBuilding`, `IfcBuildingStorey`, `IfcSpace`, `IfcWall`, `IfcSlab`, `IfcDoor`, and hundreds more — each with typed Property Sets (Psets) specifying what attributes a compliant implementation must support.

Every Building Design System BIM Object maps to a specific IFC entity class or Pset. The spatial BIM Object `bim.spatial.storey` anchors to `IfcBuildingStorey`; the performance BIM Object `bim.performance.door-fire-exit` anchors to `Pset_DoorCommon.IsFireExit`. When a BIM Object value changes, a validator can trace the change back to the IFC Pset that the BIM Object represents.

### Layer 2 — Uniclass 2015 classification floor

Uniclass 2015 is the unified classification system for the UK construction industry, maintained by the NBS. Building Design System BIM Objects carry a Uniclass 2015 reference in their `$extensions.uniclass` field, establishing a classification floor that maps to the national procurement and specification context.

The classification is non-normative for jurisdictions outside the UK but serves as the consistent structural vocabulary for the object catalogue. Where a North American equivalent exists — OmniClass, UniFormat II, or MasterFormat — the object carries a cross-map annotation in `$extensions.omniclass`.

### Layer 3 — bSDD URIs

buildingSMART's Data Dictionary (bSDD) publishes machine-readable JSON-LD definitions for building properties and classifications, each with a stable dereferenceable URI such as `https://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/prop/IsFireExit`. Building Design System BIM Objects carry these URIs in their `$extensions.bsdd_uri` fields, linking the object to an authoritative definition that a validator or authoring tool can resolve at runtime.

## Eight BIM Object Primitive Categories

The Building Design System groups BIM Objects into eight categories, each mapped to a distinct layer of the IFC entity model.

### 1. Spatial (`bim.spatial.*`)

Site, Building, Storey, and Space — the `IfcSpatialStructureElement` hierarchy. BIM Objects in this category encode floor-to-floor heights, minimum net area per use type, and occupancy limits. These are the objects that drive building massing at the earliest design stage.

Source file: `spatial.dtcg.json`

### 2. Elements (`bim.elements.*`)

Walls, slabs, columns, beams, curtain walls, doors, and windows — `IfcProduct` subclasses. BIM Objects encode structural fire ratings, acoustic performance classes, maximum glazing ratios, and the door-width minima required by ADA 2010 and CSA-B651.

Source file: `elements.dtcg.json`

### 3. Materials (`bim.materials.*`)

Thermal conductivity, density, acoustic absorption coefficients, and compressive strength — `Pset_MaterialCommon` and material-specific Psets. Material BIM Objects encode the properties of the substrate, not the assembly. Assembly-level properties (U-values for a wall assembly) are encoded in the Assemblies category.

Source file: `materials.dtcg.json`

### 4. Assemblies (`bim.assemblies.*`)

Composite element constructions — wall assemblies, floor-ceiling assemblies, roof assemblies — where the performance property belongs to the layered system, not any single material. Thermal transmittance (U-value) and sound reduction index (Rw) live here, anchored to ISO 10077 and ISO 717-1 respectively.

Source file: `assemblies.dtcg.json`

### 5. Systems (`bim.systems.*`)

HVAC zones, electrical circuits, and plumbing networks — `IfcSystem` and `IfcDistributionSystem`. The central BIM Object in this category is the climate-zone-autonomy principle: one Tile equals one HVAC zone. The BIM Object `bim.systems.tile-climate-autonomy` encodes this invariant so any downstream validator can confirm a proposed floor-plate composition satisfies it.

Source file: `systems.dtcg.json`

### 6. Performance (`bim.performance.*`)

Energy, daylight, accessibility, and fire-safety thresholds — regulatory minima drawn from EN 12464-1 (workplace daylight), EN 17037 (daylight in buildings), ADA 2010, IBC 2021, and ASHRAE 90.1. Performance BIM Objects are the regulatory floor that the spatial and element objects must satisfy.

The most architecturally consequential performance BIM Object is `bim.performance.max-workstation-to-window`, set at 6.0 metres from EN 12464-1:2021. This single value drives the Zone 1 Habitat depth in every professional office floor plate.

Source file: `performance.dtcg.json`

### 7. Climate zones (`bim.climate-zones.*`)

ASHRAE 90.1 climate zones 1 through 8, encoding the heating-degree-day and cooling-degree-day thresholds that govern mechanical-system sizing across North American jurisdictions. These BIM Objects are consumed by service-codes when a building site is assigned to an ASHRAE zone and the energy model is validated.

Source file: `climate-zones.dtcg.json`

### 8. Identity codes (`bim.identity-codes.*`)

Use-type codes (FFE series: M1, M2, B1, L1, A1, C1), tile codes (Tile A through Tile H), and key-plan index ranges. These are the opaque identifiers that planning documents use when describing floor-plate compositions. The BIM Object library is the lexicon that maps each code to its geometric and programme meaning.

Source file: `identity-codes.dtcg.json`

## How BIM Objects Are Delivered

The BIM Object library is distributed as a set of DTCG-format JSON files. DTCG (W3C Design Token Community Group format) is a JSON structure where each BIM Object carries a `$value`, `$type`, and `$description`, with optional `$extensions` for standards references and provenance.

A BIM authoring tool or validator reads the DTCG files at startup and constructs an in-memory BIM Object index. Any dimension, threshold, or classification referenced in a design session resolves to a BIM Object value rather than a hard-coded number. When a BIM Object changes — because a code amendment raises the minimum corridor width, or a new Uniclass edition replaces a classification code — the consuming tool receives the update via a library version bump, not a manual re-entry of values across hundreds of model elements.

## Relationship to the IFC File

The DTCG BIM Object library does not modify IFC files directly. It is an authoring-time reference — the source of truth for what values to write into an IFC Pset when a model element is created or modified. A BIM operator who follows the Building Design System writes the IFC file with the BIM Object values; IDS 1.0 contracts then validate that the IFC file conforms to the published thresholds.

The BIM Object-to-IFC pipeline is therefore:

```
BIM Object value (bim.performance.max-workstation-to-window = 6.0 m)
        ↓ applied at authoring time
IFC Pset_SpaceOccupancy attribute in IfcSpace
        ↓ validated at delivery time
IDS 1.0 rule: IfcSpace.MaxWorkstationToWindow ≤ 6000 mm
```

This separation — author with BIM Objects, validate with IDS — is the substrate that makes [[city-code-as-composable-geometry]] possible at the next layer.

## Open Questions

Whether DTCG W3C CG format will be superseded by a formal W3C Recommendation before the object library ships a v1.0 release. The v0.0.x object files use the community-group schema; a format migration at v1.0 may be needed.
