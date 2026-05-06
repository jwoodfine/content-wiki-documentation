---
schema: foundry-doc-v1
type: topic
slug: bim-token-taxonomy
title: BIM Token Taxonomy
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: bim-token-taxonomy.es.md
## See Also

- [[bim-design-philosophy]]
- [[bim-aec-muscle-memory]]
- [[flat-file-bim-leapfrog]]
- [[design-color]]

---


Foundry’s BIM Token Taxonomy organizes the Building Design System into eight primitive categories anchored to the IFC 4.3 (ISO 16739-1:2024) entity hierarchy. This alignment ensures that design-system tokens correspond directly to canonical AEC classification conventions, facilitating seamless data exchange across the openBIM ecosystem.

## Eight Primitive Token Categories

| Primitive | IFC Anchor | Description |
| :--- | :--- | :--- |
| **SPATIAL** | `IfcSpatialElement` | Hierarchy of Site, Building, Storey, and Space. |
| **ELEMENTS** | `IfcBuiltElement` | Physical components: walls, slabs, doors, windows, etc. |
| **SYSTEMS** | `IfcDistributionElement` | MEP components: pipes, ducts, and distribution networks. |
| **MATERIALS** | `IfcMaterial` | Material definitions, layer sets, and constituent sets. |
| **ASSEMBLIES** | `IfcElementAssembly` | Hierarchical compositions and furnishings. |
| **PERFORMANCE** | `IfcPropertySet` | Property templates (Pset_*) and quantities (Qto_*). |
| **IDENTITY+CODES** | `IfcClassificationRef` | Taxonomy references (Uniclass) and jurisdictional constraints. |
| **RELATIONSHIPS** | `IfcRel*` | Connectivity, containment, and semantic associations. |

## Classification Floor: Uniclass 2015

Foundry adopts **Uniclass 2015** as its universal classification floor. Published by the NBS and recognized globally in the openBIM community, Uniclass provides the baseline semantic tagging for every element in the system. While deployment-specific taxonomies (e.g., OmniClass or MasterFormat) can be layered on top, Uniclass 2015 serves as the mandatory default, ensuring consistent data structures from day one.

## Component Architecture

The Building Design System defines 18 core components across three categories:

1.  **Universal AEC (10):** `SpatialTree`, `PropertiesPanel`, `Viewport3D`, `ViewNavigator`, `Toolbar`, `StatusBar`, `SelectionFilter`, `TypeBrowser`, `SectionPlane`, `AnnotationLayer`.
2.  **Console-Unique (4):** `BimGuidSearch`, `BimAuditLog`, `BimDashboard`, `BimExportPanel`.
3.  **Workplace-Unique (4):** `MaterialsBrowser`, `TypeEditor`, `ClashDetector`, `VersionHistory`.

### The Component-Recipe Pattern
Each component follows a standardized recipe structure to ensure framework independence:
*   `recipe.html`: Semantic, framework-agnostic markup.
*   `recipe.css`: Namespaced BEM CSS.
*   `aria.md`: The accessibility and interaction contract.

Host frameworks (e.g., Yew, Leptos, or vanilla TypeScript) integrate by mounting the recipe markup and attaching the required logic while strictly adhering to the ARIA contract.

## Release Roadmap

*   **v0.0.1 (Current):** `SpatialTree`, `PropertiesPanel`, and `Viewport3D` are released as foundational components.
*   **v0.0.2 (Planned):** Console-unique and workplace-unique components will ship alongside the building element index and BIM authoring features.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
