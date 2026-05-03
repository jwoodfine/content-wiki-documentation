---
schema: foundry-doc-v1
type: topic
slug: spatial-tree-accessibility
title: Spatial Tree Accessibility
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: spatial-tree-accessibility.es.md
---

# Spatial Tree Accessibility

The `bim-spatial-tree` component provides a navigable hierarchy of a building’s spatial elements. It is designed to follow WAI-ARIA best practices for tree widgets, ensuring that complex architectural structures remain accessible to users relying on assistive technologies (AT).

## Structural Role and ARIA Mapping

The component utilizes a semantic tree structure to reflect the building’s containment hierarchy:
*   **Container:** An `<aside aria-label="Spatial hierarchy">` element.
*   **Tree Root:** A `<ul role="tree">` list.
*   **Spatial Items:** Each node is a `<li role="treeitem">` with an `aria-expanded` attribute.
*   **Child Groups:** Nested levels are contained within `<ul role="group">`.

Following AEC industry conventions, storey-level nodes default to `aria-expanded="true"`, while deeper spatial elements remain collapsed by default to reduce initial cognitive load.

## Selection and Multi-Select

Selection state is tracked via the `aria-selected` attribute:
*   **Console Mode:** Single-select only (`aria-selected="true"` on one item).
*   **Workplace Mode:** Supports multi-selection via `Ctrl/Cmd-click` or `Shift-click` patterns.

## Keyboard Interaction

The `bim-spatial-tree` supports full keyboard parity for navigation:

| Key | Action |
| :--- | :--- |
| **Up / Down Arrows** | Focus previous or next visible item. |
| **Right Arrow** | Expand focused item or move focus to first child. |
| **Left Arrow** | Collapse focused item or move focus to parent. |
| **Enter / Space** | Select the focused item. |
| **Home / End** | Focus first or last visible item in the tree. |
| **Forward Slash (/)** | Move focus directly to the spatial search input. |

## Search and Filtering

The tree includes a search interface (`<input type="search">`) that filters nodes by their `IfcSpace` name or long-name. Matches are performed via case-insensitive substring comparison. When a match is found, the tree automatically expands the path to the matching node and focuses it, while non-matching branches are visually hidden or collapsed.

## Implementation Guardrails

*   **Avoid Generic Scene-Graphs:** Do not utilize generic "outliner" widgets. The `SpatialTree` is a purpose-built AEC tool with specific expansion and search logic.
*   **Storey-First Expansion:** Adhere to the storey-default expansion rule to match professional AEC mental models.
