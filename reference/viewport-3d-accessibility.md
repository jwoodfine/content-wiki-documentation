---
schema: foundry-doc-v1
type: topic
slug: viewport-3d-accessibility
title: 3D Viewport Accessibility
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: viewport-3d-accessibility.es.md
## See Also

- [[spatial-tree-accessibility]]
- [[properties-panel-accessibility]]
- [[neurodiversity-typography-standards]]

---


The `bim-viewport-3d` component is the primary visualization layer for building models. While 3D canvas content is inherently graphical, the component is designed to remain operational and informative for all users through selection synchronization and robust keyboard navigation.

## Structural Role and Interface

*   **Container:** A `<section aria-label="3D viewport">` element.
*   **Canvas:** A `<canvas aria-label="3D model canvas">`. As canvas content is not directly inspectable, all selection states are mirrored in the accessible `SpatialTree` and `PropertiesPanel`.
*   **Viewport Toolbar:** A `<div role="toolbar">` containing accessible buttons for view control.
*   **Navigation Cube:** The NavCube is presentational only (`aria-hidden="true"`); its functionality is fully duplicated by standardized keyboard shortcuts.

## Selection Synchronization

Interaction between the 3D view and accessible text-based components is bidirectional:
*   Selecting an element in the canvas triggers an announcement in the `PropertiesPanel` live region.
*   Selecting or focusing an item in the `SpatialTree` highlights the corresponding geometry in the viewport and adjusts the camera as necessary.

## Keyboard Parity for Navigation

The viewport implements industry-standard AEC shortcuts to ensure full control without a mouse:

| Key | Action |
| :--- | :--- |
| **1 – 6** | Snap camera to ±X, ±Y, or ±Z axes (Top, Bottom, Front, Back, etc.). |
| **F** | Fit selection to view (or fit entire model if no selection). |
| **Arrows** | Pan the camera (Shift + Arrows) or Orbit. |
| **+ / -** | Zoom in and out. |
| **S** | Toggle the active section plane. |
| **B** | Capture a BCF viewpoint (Workplace mode only). |
| **Tab** | Move focus to the viewport toolbar. |

## Mode-Specific Behavior

*   **Console Mode:** The viewport may degrade to high-fidelity static SVG plan thumbnails. This preserves the EUPL-1.2 license boundary by avoiding 3D engine overhead in read-only surfaces.
*   **Workplace Mode:** Enables full interactive 3D rendering (xeokit-based) for authoring and coordination. Large model data is loaded via Tauri’s `asset:` protocol to prevent IPC bottlenecks.

## Implementation Guardrails

*   **Zero IPC for Geometry:** Do not pipe raw IFC or geometry bytes over the IPC boundary. Use localized asset protocols to load visualization caches (e.g., XKT files) directly into the GPU.
*   **Decoupled CSS:** Viewport-specific 3D engine CSS should remain decoupled from the Building Design System’s core styles to allow for runtime-specific engine updates.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
