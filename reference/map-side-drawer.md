---
schema: foundry-doc-v1
type: topic
category: reference
slug: map-side-drawer
title: Map Side Drawer
paired_with: map-side-drawer.es.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
---

# Map Side Drawer

The Map Side Drawer is a persistent overlay pattern designed for detailed feature inspection without loss of geographic context. It replaces transient popups with a fixed-width panel that slides from the right edge, providing a dedicated space for complex metadata, cluster context, and regulatory disclosures.

## Executive Summary

Foundry’s GIS interface utilizes the Map Side Drawer to centralize attribute data for selected map features. Unlike traditional tooltips or popups that obscure the map canvas, the drawer maintains a 340px fixed-width footprint on the right margin, allowing the map to remain interactive and visible. The component is engineered for rapid data parsing, utilizing a structured facts grid and optional disclosure banners to meet both operational and regulatory transparency requirements.

## Usage Guidelines

### Deployment Scenarios
- **Retail Anchor Details**: Serves as the primary display for retail metadata, including address, NAICS codes, and opening dates.
- **Cluster Contextualization**: Provides aggregate data for selected map clusters (e.g., corridor membership, anchor density).
- **Building Analysis**: Planned for use in BIM integrations to display building-envelope and mobility composition details.

### Constraints
The drawer is intended for deep-dive information retrieval. It should not be used for transient confirmation messages or system alerts, which are serviced by Toast or Snackbar components.

## Technical Specifications

### Anatomy and Composition
- **Header Block**: Contains the feature title and a brand-family badge for rapid taxonomic identification.
- **Facts Grid**: Utilizes a definition list (`<dl>`) to present key-value pairs of metadata.
- **Disclosure Zone**: A dedicated area at the top or bottom for BCSC-mandated forward-looking statements.

### Interaction Model
- **Transition**: Slides from the right edge over 250ms using a `cubic-bezier(0.16, 1, 0.3, 1)` ease.
- **Dismissal**: Can be closed via a dedicated icon-button, the ESC key, or by clicking an empty area of the map canvas.
- **Modality**: Operates as a non-modal complementary landmark (`aria-modal="false"`), allowing users to pan and zoom the map behind the drawer.

## Accessibility and Compliance
The component is engineered for full keyboard and screen-reader compatibility:
- **Focus Management**: On opening, focus is trapped within the drawer to facilitate rapid keyboard navigation. Dismissal returns focus to the previously active map element.
- **Semantic Roles**: Utilizes `role="complementary"` with a descriptive `aria-label`.
- **Motion Control**: Respects `prefers-reduced-motion`, collapsing the slide animation into an instant opacity fade.

## Design Tokens (DTCG)

| Token | Value | Description |
| :--- | :--- | :--- |
| `ps.map-drawer.width` | 340px | Fixed width for map overlays |
| `ps.map-drawer.bg` | surface-elevated | Background for elevated surfaces |
| `ps.map-drawer.transition.duration` | 250ms | Standard slide-in duration |
| `ps.map-drawer.shadow` | shadow-side-panel | Inset shadow on leading edge |

## Strategic Roadmap
Future developments are intended to include:
- **Comparison View**: A planned split-drawer variant to support federated cluster comparison (Doctrine Invention #9).
- **Adaptive Width**: Research is ongoing to determine if a full-width expansion is required for mobile viewports while preserving minimal map context.
