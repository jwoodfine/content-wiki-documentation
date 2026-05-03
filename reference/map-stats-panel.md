---
schema: foundry-doc-v1
type: topic
category: reference
slug: map-stats-panel
title: Map Stats Panel
paired_with: map-stats-panel.es.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
---

# Map Stats Panel

The Map Stats Panel is a reactive data-display component that surfaces real-time aggregate statistics based on active map filters. Positioned as a floating overlay, it provides users with constant visibility into key performance indicators such as anchor counts, jurisdictional distribution, and cluster grades.

## Executive Summary

Foundry map surfaces utilize the Map Stats Panel to provide immediate quantitative context to geographic visualizations. As users manipulate country chips or brand-family filters, the panel reactively updates to reflect the current data subset. The component is designed for non-intrusive persistent visibility, typically anchored to the top-right margin to avoid collision with standard map navigation controls.

## Usage Guidelines

### Deployment Scenarios
- **Location Intelligence**: Displays aggregate counts for retail corridors and anchors within the current viewport.
- **Executive Dashboards**: Provides high-level portfolio statistics (e.g., average cluster grade) alongside map views.
- **Comparative Analysis**: Planned for use in federated cluster comparison to show side-by-side aggregate deltas.

### Constraints
The panel is a read-only display. It should not be used for triggering filters or navigation, which are handled by the Country Filter Chips and Map Side Drawer components.

## Technical Specifications

### Anatomy and Composition
- **Data Cells**: A grid-based layout (typically 2x2) containing high-contrast numeric values and compact semantic labels.
- **Container**: A floating card with elevated surface tokens and rounded corners to distinguish it from the map background.
- **Grid Density**: Supports 2 to 6 statistical cells with responsive adjustments for multi-column layouts.

### Interaction Model
- **Reactive Updates**: Values update asynchronously via `aria-live="polite"` announcements when the underlying data filter changes.
- **Positioning**: Floats above the map canvas at a fixed offset (default 16px) from the top and right edges.
- **Visual Feedback**: Transitions between values are intended to utilize a 200ms fade to prevent jarring layout shifts during rapid filtering.

## Accessibility and Compliance
The component is engineered for compliance with WCAG 2.2 AA standards:
- **Live Regions**: Implements `aria-live="polite"` to ensure screen-reader users are notified of data changes without interruption.
- **Semantic Pairing**: Utilizes description list markup (`<dt>` and `<dd>`) to maintain clear value-to-label relationships.
- **Accessible Units**: Numeric values utilize hidden `aria-label` attributes to provide full unit context (e.g., "12 corridors" instead of just "12").

## Design Tokens (DTCG)

| Token | Value | Description |
| :--- | :--- | :--- |
| `ps.map-stats.bg` | surface-elevated | Background for floating panels |
| `ps.map-stats.value.font` | heading-04 | Large numeric value typography |
| `ps.map-stats.label.font` | caption-01 | Compact label typography |
| `ps.map-stats.shadow` | shadow-floating | Depth cue for floating overlays |

## Strategic Roadmap
Future enhancements are intended to include:
- **Inline Sparklines**: Planned support for compact data visualizations below numeric values to show grade distribution.
- **Mobile Auto-Collapse**: Research is ongoing to determine the optimal collapse threshold for mobile viewports to maximize map visibility.
