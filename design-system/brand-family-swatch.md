---
schema: foundry-doc-v1
type: topic
content_type: topic
category: design-system
slug: brand-family-swatch
short_description: "The brand color families assigned to retail and institutional anchor categories in the co-location GIS surface, providing consistent color-coded map and table identifiers."
title: "Brand-family swatch"
paired_with: brand-family-swatch.es.md
state: authoritative
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
last_edited: 2026-05-25
---

The brand-family swatch is the visual classification component the [[app-orchestration-gis|platform’s GIS surface]] uses to identify retail anchor categories — Department, Hardware, and Warehouse Club — on maps, filter rows, and detail panels, as part of the [[location-intelligence-platform|location intelligence platform]]. It pairs a color-coded dot with a semantic label so that category membership is legible at a glance without relying on color alone, supporting the [[retail-co-location-tier-methodology|retail co-location tier methodology]]’s tier visualization. The component is designed to be taxonomy-agnostic: family identifiers resolve through a runtime configuration, so operators extend or reclassify anchor categories without code changes.

## Visual representation

The platform’s GIS surface uses the brand-family swatch to standardize how retail anchors appear across map markers, tabular filters, and detail drawers. A color-coded identifier paired with a semantic label ensures accessible data density. The component decouples presentation from the underlying taxonomy, resolving family identifiers through a runtime JSON configuration.

## Usage guidelines

### Deployment scenarios
- **Map Markers**: Functions as the visual foundation for anchor markers, using color-coded dots to signal family affiliation.
- **Data Filtering**: Serves as the interactive primitive within filter rows (typically paired with a checkbox).
- **Detail Overlays**: Provides high-level categorization within side drawers and header chips.
- **Cluster Analysis**: Employs a concentric ring variant to represent family distribution within aggregate map clusters.

### Constraints

The component is reserved for taxonomic classification. It must not be used for binary state indicators, transient system feedback, or non-taxonomic tagging, which are serviced by the Tag and Status Indicator components.

## Technical specifications

### Anatomy and composition
- **Indicator**: A 12px (default) or 24px (marker) circular dot using family-specific color tokens.
- **Label**: A taxonomy-resolved display name (e.g., "Warehouse Club").
- **Accessibility Layer**: An `aria-label` that combines the dot and label semantics, ensuring the visual indicator is hidden from screen readers to prevent redundant announcements.

### Interaction model
The swatch is natively static. Interactivity is inherited from its parent container (e.g., a filter button or map feature). On map surfaces, the component supports a reveal-by-zoom behavior: cluster-centroid rings are intended to render at zoom levels below 8.5, transitioning to individual swatches at higher magnifications.

## Accessibility and compliance
The component is engineered to meet WCAG 2.2 AA standards:
- **Redundant Signaling**: Color is never the sole channel for information; labels provide primary semantic meaning.
- **High-Contrast Support**: In Windows High Contrast Mode or `forced-colors` environments, the dot reverts to system link colors while the label maintains text integrity.
- **Luminance Contrast**: Family color tokens are validated for a minimum 3:1 contrast ratio against both light and dark map basemaps.

## Design tokens (DTCG)

**Correction (2026-08-02):** the dot-size tokens below don't exist. The real recipe (`dtcg-vault/components/brand-family-swatch/recipe.json`) hardcodes dot size as inline CSS (`.ps-swatch__dot { width: 10px; height: 10px }`, not 12px), with no named `ps.swatch.dot.size` token — its actual token references are `{semantic.ink-primary}`, `{semantic.ink-secondary}`, `{primitive.space.05}`, `{primitive.radius.sm}`. The three brand-family color values below are independently confirmed accurate. **Flagged, not resolved.**

| Token | Value | Description |
| :--- | :--- | :--- |
| `ps.swatch.dot.size` | 12px | Default inline dot size |
| `ps.swatch.dot.size.marker` | 24px | Map marker variant size |
| `ps.brand-family.department.color` | `#0B5FFF` | Azure blue |
| `ps.brand-family.hardware.color` | `#FF6B00` | Construction orange |
| `ps.brand-family.warehouse-club.color` | `#00875A` | Warehouse green |

## Planned extensions
Future iterations are intended to include:
- **Pattern Infills**: Planned support for geometric patterns within the dot to enhance distinguishability for users with advanced color vision deficiencies.
- **Dynamic Pie Charts**: Research is underway to transition the cluster-centroid ring into a dynamic donut chart when cluster density exceeds 10 anchors.

## See also

- [[brand-typography]] — the platform's print typography standards that pair with this visual identity system
- [[app-orchestration-gis]] — the GIS analytics engine that produces the cluster data this component visualizes
- [[location-intelligence-platform]] — the location intelligence platform that uses this component on its interactive map surface
- [[retail-co-location-tier-methodology]] — the tier methodology whose tier rankings drive the swatch color assignments
