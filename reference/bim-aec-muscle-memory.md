---
schema: foundry-doc-v1
type: topic
slug: bim-aec-muscle-memory
title: AEC Muscle Memory and Interface Conventions
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: bim-aec-muscle-memory.es.md
---

# AEC Muscle Memory and Interface Conventions

The Building Design System adopts established interface vocabularies from industry-standard tools (Revit, ArchiCAD, BricsCAD, and Bonsai) to ensure a zero-learning curve for AEC practitioners. By mirroring universal navigation and layout conventions, Foundry allows users to focus on strategic innovations—such as the flat-file vault and code-as-composable-geometry—rather than basic tool interaction.

## Universal AEC Interface Conventions

Foundry implements the following industry-standard layout patterns:

| Convention | Standard Location | Building Design System Component |
| :--- | :--- | :--- |
| **Spatial Tree** | Left Rail | `SpatialTree` |
| **Properties Panel** | Right Rail | `PropertiesPanel` |
| **Toolbar** | Top | `Toolbar` |
| **Status Bar** | Bottom | `StatusBar` |
| **NavCube** | Top-Right Viewport | `Viewport3D__navcube` |

### Key Navigation Standards
*   **Storey-Level Expansion:** The `SpatialTree` defaults to storey-level nodes. Expanding directly to individual spaces is avoided to minimize visual noise and align with professional mental models.
*   **Non-Modal Properties:** The `PropertiesPanel` operates as a selection-sensitive sidebar that updates in real-time, avoiding disruptive popup modals.
*   **Semantic Grouping:** Property sets (Pset_*) and quantities (Qto_*) are grouped into named, collapsible sections for rapid data retrieval.

## Strategic Divergence from Generic Modeling

While Foundry respects professional conventions, it deliberately avoids artifacts of general-purpose 3D modeling software (e.g., Blender-host artifacts in Bonsai):

1.  **Dedicated Spatial Tree:** Foundry utilizes a purpose-built `SpatialTree` widget rather than a generic scene-graph outliner, enabling features like search-by-space-name and floor-plan thumbnails.
2.  **Standardized Keymaps:** Navigation uses the standard 1–6 number row for view switching (top, bottom, front, back, left, right), accommodating the lack of numpads on modern laptops.
3.  **Removal of Modal Editing:** Foundry eliminates complex "mode-switching" (e.g., Object vs. Edit mode) common in general 3D software, providing a streamlined authoring experience.

## Addressing the FM Operator Persona

Existing BIM tools predominantly target designers. The Building Design System is engineered to address the Facility Management (FM) and Property Manager personas through three intended unique workflows:

*   **Work-Order Linking:** Attaching maintenance status directly to IFC elements via YAML sidecars.
*   **Lease Integration:** Linking `IfcSpace` entities to lease records in the bookkeeping vault.
*   **Sensor Overlays:** Displaying real-time MQTT-backed sensor readings directly in the `Viewport3D`.

These capabilities are planned for the v0.0.2 release and represent the convergence of spatial and operational data.
