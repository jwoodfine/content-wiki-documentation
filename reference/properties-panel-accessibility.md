---
schema: foundry-doc-v1
type: topic
slug: properties-panel-accessibility
title: Properties Panel Accessibility
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: properties-panel-accessibility.es.md
## See Also

- [[viewport-3d-accessibility]]
- [[spatial-tree-accessibility]]
- [[neurodiversity-typography-standards]]

---


The `bim-properties-panel` displays semantic and performance data for selected building elements. It is designed to provide high-density technical information while maintaining full accessibility for screen readers and keyboard users.

## Structural Role and Hierarchy

*   **Container:** An `<aside aria-label="Element properties">` element.
*   **Organization:** Each IFC Property Set (Pset) or Quantity Set (Qto) is contained within a `<section>` marked by an `<h4>` heading.
*   **Data Representation:** Properties are rendered as `<dt>` (description term) and `<dd>` (description details) pairs within a `<dl>` (description list).
*   **Subject Context:** The elemental class and GlobalID (GUID) are displayed as a sub-header to provide persistent context.

## Live Regions and Selection Feedback

To ensure that changes in selection are communicated to users of assistive technology, the panel uses an `aria-live="polite"` region. When a user selects a new element in the `Viewport3D` or `SpatialTree`, the framework announces the new subject to the screen reader without interrupting current tasks.

## Mode-Specific Interactions

The panel’s behavior adapts based on the `data-mode` property:
*   **Console Mode:** A read-only presentation of `<dt>` and `<dd>` pairs.
*   **Workplace Mode:** The `<dd>` elements are replaced with appropriate form controls (`<input>`, `<select>`) to allow data entry.

### Keyboard Parity (Workplace Mode)
| Key | Action |
| :--- | :--- |
| **Tab / Shift-Tab** | Move focus between editable property fields. |
| **Enter** | Commit the edit and save the change to the sidecar. |
| **Escape** | Cancel the current edit and revert to the persisted state. |

## Implementation Guardrails

*   **GlobalID Portability:** Always provide a "copy-to-clipboard" affordance for GlobalIDs. IFC GUIDs are critical for audit trails but impossible to transcribe manually.
*   **Namespace Discipline:** Do not author custom Property Set names without a registered namespace. All non-standard properties must follow the custom Pset prefix conventions to remain IFC-compliant.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
