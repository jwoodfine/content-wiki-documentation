---
schema: foundry-doc-v1
title: "The Building Design System for the Built Environment"
slug: building-design-system-bim
category: architecture
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, dtcg-w3c]
paired_with: building-design-system-bim.es.md
---

Major software design systems solve a coordination problem at scale: when independent teams author UI surfaces in parallel, consistency breaks down unless design decisions are encoded in a shared layer of tokens, component recipes, and interaction patterns. No equivalent system exists for the built environment. Building Information Modelling production is coordinated through shared standards (IFC, Uniclass, bSDD) and shared authoring tools, but there is no common token layer — no canonical, machine-readable library of built-environment element specifications that authoring surfaces consume by reference. Research commissioned in April 2026 surveyed the available prior art and found the space empty. The Building Design System for the built environment is intended to fill that space.

## Why the Space Is Empty

The absence of a built-environment design system is not accidental. Three structural factors kept the space empty.

**Proprietary authoring tool dominance.** The dominant BIM authoring tools have historically stored element specifications in proprietary object formats. These formats carry geometry, parametric behaviour, and some metadata — but they are format-locked, not interoperable across tools, and not designed to carry normative regulatory data. They serve as the element library for a single tool, not as a shared cross-tool specification layer.

**IFC as exchange format, not specification format.** IFC 4.3 (ISO 16739-1:2024) is a neutral exchange format — it expresses what a model contains, not what a token specification requires. The IFC Property Set mechanism (`Pset_WallCommon`, `Pset_SlabCommon`) provides templates for property values but carries no enforcement logic, constraint hierarchy, or jurisdiction mapping. IFC is an excellent exchange substrate but was not designed to be a design system.

**Standards fragmentation.** The built-environment standards stack — IFC, Uniclass, Omniclass, MasterFormat, CoClass, NBS, bSDD — evolved in parallel across jurisdictions. Each solves part of the identification and classification problem. None provides a composable specification layer analogous to DTCG.

The Building Design System uses each of these standards in its proper role: IFC as the entity type hierarchy, Uniclass 2015 as the classification floor, bSDD as semantic identity, and IDS 1.0 as constraint expression. DTCG provides the container format and aliasing mechanism.

## The Eight Token Primitive Categories

The token layer of the Building Design System is organised into eight primitive categories, each corresponding to a cluster of IFC 4.3 entity types. This structure mirrors the organisation of software design system token primitives but is anchored to the IFC entity hierarchy rather than to visual design properties.

**1. Spatial** — `IfcSpatialElement` hierarchy: site, building, building storey (level), space, zone. Spatial tokens define the organisational units that contain elements.

**2. Elements** — `IfcBuiltElement` hierarchy: walls, slabs, beams, columns, doors, windows, stairs, ramps, and related structural and envelope components. Element tokens carry the full three-layer specification (Specification / Regulation / Climate Zone) because built elements are the primary objects of regulatory constraint.

**3. Systems** — `IfcDistributionElement` hierarchy: mechanical, electrical, plumbing, fire protection, and HVAC distribution elements. System tokens connect to climate zone performance requirements (heating/cooling loads, ventilation rates) more directly than structural elements.

**4. Materials** — `IfcMaterial` and `IfcMaterialLayer` specifications. Material tokens encode thermal conductivity, structural grade, fire classification, embodied carbon (where data is available), and applicable bSDD material URIs. A material token is referenced (aliased) by element tokens that specify its composition.

**5. Assemblies** — `IfcElementAssembly` compositions. Assembly tokens are composed references: a curtain wall assembly aliases its glazing unit token, mullion profile token, and thermal break material token. The assembly's performance parameters are derived from the aliased component tokens using the most-restrictive-wins composition rule.

**6. Performance** — `IfcPropertySet` templates for performance specifications not covered by entity-specific property sets. This category holds cross-cutting performance definitions: thermal bridges, air permeability, acoustic isolation ratings.

**7. Identity + Codes** — `IfcClassificationReference` and `IfcExternalReferenceRelationship` specifications. This category holds the mapping tables that relate BIM Token identifiers to external classification systems: Uniclass 2015, Omniclass Table 23, NBS Section references, Masterformat 2018.

**8. Climate Zones** — Performance parameter tables keyed to climate zone identifiers (ASHRAE 90.1 zones 1A through 8, Canadian NBC climate zones, and European EN ISO 52000 zones). Each row is one climate zone × one element type × one performance parameter. See [[bim-token-three-layers]] for the full Climate Zone layer specification.

## The AEC Interface Component Layer

Above the token primitive layer, the Building Design System defines a set of universal AEC interface components — UI patterns common to any BIM-capable authoring surface regardless of the specific programme type.

Research identified ten universal components that appear in every BIM authoring context:

1. **BIM Spatial Tree** — Hierarchical display of `IfcSite → IfcBuilding → IfcBuildingStorey → IfcSpace`. The canonical navigation tree for spatial containment.
2. **BIM Properties Panel** — Structured display of element properties: IFC type, applicable property sets, current property values, Uniclass reference, bSDD URI link, and regulatory overlay summary.
3. **BIM Viewport 3D** — Double-precision WebGL renderer for IFC geometry. Uses xeokit-sdk for double-precision rendering (required for large-site coordinate accuracy).
4. **BIM View Navigator** — Orthographic view controls: plan, section, elevation. Section plane control and viewport synchronisation for multi-view layouts.
5. **BIM GUID Search** — IFC GlobalId lookup surface.
6. **BIM Audit Log** — Chronological record of model changes against token specification conformance.
7. **BIM Regulation Navigator** — Jurisdiction and standard browser. Displays registered regulatory overlays with filter by jurisdiction, element type, and effective date.
8. **BIM Token Catalog Card** — The grid card for a token category on the catalog index page.
9. **BIM Token Detail Tab** — The tabbed detail view for a single token category: Specification tab, Regulation tab, Climate Zone tab.
10. **BIM Code Overlay Card** — Display unit for a single registered regulatory overlay: jurisdiction name, standard identifier, constraint summary, IDS file link, effective date.

Three of these components (Spatial Tree, Properties Panel, Viewport 3D) are implemented at v0.0.1. The remaining seven are intended for v0.0.2 and v0.0.3.

## Surface-Specific Extensions

Beyond universal components, each built-environment programme type has a distinct set of interface requirements. Three programme types are in scope at v0.0.1:

**app-orchestration-bim** — The BIM Token Catalog web surface. Displays the full catalog, regulatory overlays, and standards reference. Read-only; serves designers, regulators, and machine consumers.

**app-workplace-bim** — The BIM authoring workbench. Tauri 2.x desktop application embedding xeokit for 3D rendering and IfcOpenShell (via sidecar) for IFC parsing. Licensed AGPL-3.0 due to xeokit component licensing.

**app-console-bim** — The administrative console for BIM token vault management. Web-only Axum application. Read surface for token browsing; write surface (intended for v0.1.x) for token authoring via the four-zone CMS model.

## Uniclass 2015 as Classification Floor

All BIM Tokens use Uniclass 2015 as the classification floor. Uniclass 2015 is the UK-maintained open classification standard that provides a structured reference for elements, systems, products, and activities in the built environment. It is maintained by NBS and published under open licence terms.

Uniclass 2015 was selected over comparable open classification systems because it is the most consistently maintained, maps well to IFC 4.3 entity types at the appropriate level of detail for token specification, and is jurisdiction-neutral despite its UK origin.

The token vault includes the full Uniclass 2015 table as a separate DTCG file (`identity-codes.dtcg.json`), enabling tokens to reference classification codes by alias rather than duplicating the classification text.

## The Sovereign Vault Model

The Building Design System is not a hosted service. It is a set of JSON files in a git repository — the BIM token vault. Organisations operating the platform clone the vault repository, extend it with their own regulatory overlays and climate zone data, and configure their deployed `app-orchestration-bim` instance to read from their local copy.

The vendor-tier `pointsav-design-system` maintains the universal token primitives, component recipes, and research files. Customer-tier vaults extend the vendor layer with jurisdiction-specific and programme-specific additions. Deployment instances read from the customer vault. No data flows upward: vendor → customer → deployment only.

## See Also

- [[bim-token-what-it-is]]
- [[bim-token-three-layers]]
- [[design-system-substrate]]
- [[flat-file-bim-leapfrog]]
- [[bim-token-taxonomy]]

## References

- IFC 4.3 (ISO 16739-1:2024) — buildingSMART International
- Uniclass 2015 — NBS / RIBA Enterprises
- buildingSMART Data Dictionary (bSDD) — buildingSMART International
- IDS 1.0 (Information Delivery Specification) — buildingSMART International
- W3C Design Token Community Group (DTCG) format — W3C
- W3C ARIA 1.2 — W3C Web Accessibility Initiative

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
