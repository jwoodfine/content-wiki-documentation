---
schema: foundry-doc-v1
type: topic
category: reference
slug: brand-family-swatch
title: Brand-Family Swatch
paired_with: brand-family-swatch.es.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
---

# Brand-Family Swatch

The Brand-Family Swatch is the primary taxonomic primitive for retail anchor classification within the Foundry GIS ecosystem. It encodes the tripartite operator-ratified taxonomy—Department, Hardware, and Warehouse Club—while maintaining a data-agnostic architecture that supports customer-driven extensions via sovereign data layers.

## Executive Summary

Foundry’s geographic information systems utilize the Brand-Family Swatch to standardize the visual representation of retail anchors. By combining a color-coded identifier with a semantic label, the component ensures accessible data density across map surfaces, tabular filters, and detail drawers. The architecture is intentionally decoupled from the specific taxonomy; it resolves family identifiers through a runtime JSON configuration, permitting operators to modify or extend classification categories without code changes.

## Usage Guidelines

### Deployment Scenarios
- **Map Markers**: Functions as the visual foundation for anchor markers, utilizing color-coded dots to signal family affiliation.
- **Data Filtering**: Serves as the interactive primitive within filter rows (typically paired with a checkbox).
- **Detail Overlays**: Provides high-level categorization within side drawers and header chips.
- **Cluster Analysis**: Employs a concentric ring variant to represent family distribution within aggregate map clusters.

### Constraints
The component is reserved for taxonomic classification. It must not be used for binary state indicators, transient system feedback, or non-taxonomic tagging, which are serviced by the Tag and Status Indicator components.

## Technical Specifications

### Anatomy and Composition
- **Indicator**: A 12px (default) or 24px (marker) circular dot utilizing family-specific color tokens.
- **Label**: A taxonomy-resolved display name (e.g., "Warehouse Club").
- **Accessibility Layer**: An `aria-label` that combines the dot and label semantics, ensuring the visual indicator is hidden from screen readers to prevent redundant announcements.

### Interaction Model
The swatch is natively static. Interactivity is inherited from its parent container (e.g., a filter button or map feature). On map surfaces, the component supports a reveal-by-zoom behavior: cluster-centroid rings are intended to render at zoom levels below 8.5, transitioning to individual swatches at higher magnifications.

## Accessibility and Compliance
The component is engineered to meet WCAG 2.2 AA standards:
- **Redundant Signaling**: Color is never the sole channel for information; labels provide primary semantic meaning.
- **High-Contrast Support**: In Windows High Contrast Mode or `forced-colors` environments, the dot reverts to system link colors while the label maintains text integrity.
- **Luminance Contrast**: Family color tokens are validated for a minimum 3:1 contrast ratio against both light and dark map basemaps.

## Design Tokens (DTCG)

| Token | Value | Description |
| :--- | :--- | :--- |
| `ps.swatch.dot.size` | 12px | Default inline dot size |
| `ps.swatch.dot.size.marker` | 24px | Map marker variant size |
| `ps.brand-family.department.color` | `#0B5FFF` | Azure blue |
| `ps.brand-family.hardware.color` | `#FF6B00` | Construction orange |
| `ps.brand-family.warehouse-club.color` | `#00875A` | Warehouse green |

## Strategic Roadmap
Future iterations are intended to include:
- **Pattern Infills**: Planned support for geometric patterns within the dot to enhance distinguishability for users with advanced color vision deficiencies.
- **Dynamic Pie Charts**: Research is underway to transition the cluster-centroid ring into a dynamic donut chart when cluster density exceeds 10 anchors.
