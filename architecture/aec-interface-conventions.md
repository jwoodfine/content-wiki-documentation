---
schema: foundry-doc-v1
title: "AEC interface conventions"
slug: aec-interface-conventions
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3]
paired_with: aec-interface-conventions.es.md
---

Every major BIM authoring platform ships with four interface conventions that an architect or engineer learns once and carries across products: a hierarchy tree for the spatial structure, a properties panel for element attributes, a 3D viewport, and a saved-view navigator. These conventions exist because the underlying data model (the IFC entity hierarchy) is the same regardless of which tool authors it. The Building Design System's universal interface components are built on this shared vocabulary.

## The Four Universal Conventions

### Spatial tree

Every BIM authoring tool displays the spatial structure of a building as a hierarchical tree: Site contains Building, Building contains Storey, Storey contains Space, Space contains Elements. This corresponds directly to the `IfcSpatialStructureElement` hierarchy in IFC 4.3. The Building Design System `SpatialTree` component renders this hierarchy with consistent expand/collapse behaviour, selection propagation to the Viewport3D, and IFC GUID display on hover. An operator who has used any of the major authoring tools can navigate a `SpatialTree` without reading documentation.

### Properties panel

When an element is selected, a properties panel shows the element's IFC class name, its globally unique identifier (IFC GUID), and all attached Property Set values. The Building Design System `PropertiesPanel` component renders the same data with a mode-prop variant: the `view` mode shows all Pset values flat; the `edit` mode shows only the values the current role is authorised to modify. A BIM operator finds their familiar Pset vocabulary — `Pset_WallCommon.FireRating`, `Pset_SpaceOccupancy.OccupancyNumber`, `Pset_DoorCommon.IsFireExit` — in the same position as in their authoring tool.

### 3D viewport

The principal interface surface of every BIM tool is a perspective or orthographic 3D viewport. Camera controls (orbit, pan, zoom) use industry-standard mouse bindings: middle-button orbit, scroll zoom, shift-scroll pan. Section cuts are applied as clipping planes. The Building Design System `Viewport3D` component embeds the xeokit-sdk or @thatopen/web-ifc viewer — both open-source — with these standard camera controls. An IFC file loaded into the viewport renders correctly because both viewers implement the IFC 4.3 geometry pipeline natively, without round-tripping through a proprietary format.

### View navigator

Named saved views — floor-plan views, section cuts, elevation views, 3D perspectives framed on a specific storey — are how BIM operators communicate intent without sending full model files. The Building Design System `ViewNavigator` component renders saved views as labelled tabs. Selecting a tab loads the camera state and, optionally, the IFC storey-filter for that view.

## Ten Universal Interface Components

The Building Design System defines ten interface components that appear on every surface — whether the field client, the facility management console, or any future surface that consumes the Building Design System.

| Component | Role |
|---|---|
| `SpatialTree` | Spatial hierarchy navigation (Site → Building → Storey → Space) |
| `PropertiesPanel` | IFC Pset viewer and editor (mode-prop variant) |
| `Viewport3D` | 3D model viewport (xeokit / @thatopen embed) |
| `ViewNavigator` | Named saved views as labelled tabs |
| `IssueTracker` | BCF 3.0 topic list with status and assignee filters |
| `ElementSearch` | IFC GUID or Pset-value search across the loaded model |
| `ClashReview` | Clash detection result list with viewport highlight |
| `HistoryTimeline` | Git commit history rendered as model-state timeline |
| `ExportPanel` | COBie export, IDS validation run, BCF ZIP download |
| `StatusBar` | Model load progress, validation counts, last-sync timestamp |

The four surface-unique components — `GuidSearch` and `AuditLog` for the facility management console, and two field-client components — extend the universal set without replacing it. An operator who learns the ten universal components has a working mental model of every PointSav BIM surface before opening it.

## Why Shared Vocabulary Matters

BIM project teams frequently work across multiple authoring tools in a single project. The structural engineer's model, the architect's model, and the MEP engineer's model all export IFC-SPF. Coordination happens in a common viewer where no one is in their native authoring environment.

A shared interface vocabulary means that the coordination viewer does not introduce a new learning surface on top of the authoring tools. An architect opening a building model in the Building Design System viewer finds the same tree, the same properties panel, and the same viewport controls they use in their authoring tool. The tool is invisible; the model is visible.

## Relationship to the Design System Substrate

The Building Design System is a BIM-semantic extension of the Carbon Design System baseline. Carbon provides the foundational UI primitives — buttons, inputs, data tables, colour tokens, typography scale. The Building Design System adds the AEC-semantic layer on top: the ten universal interface components and the eight BIM Object primitive categories.

A designer who contributes to the Carbon-based platform design surface uses the same token and component authoring workflow to contribute a new BIM component to the BIM Object catalog. The substrate is the same; the semantic domain is different.
