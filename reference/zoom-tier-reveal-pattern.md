---
schema: foundry-doc-v1
type: topic
category: reference
slug: zoom-tier-reveal-pattern
title: Zoom-Tier Reveal Pattern
paired_with: zoom-tier-reveal-pattern.es.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-RESEARCH
authored: 2026-04-30
---

# Zoom-Tier Reveal Pattern

The Zoom-Tier Reveal Pattern is a foundational geographic visualization strategy that preserves data semantics across varying scales of magnification. By transitioning between aggregate cluster representations and individual feature markers at defined zoom thresholds, the pattern ensures that high-level density signals remain as informative as granular per-anchor details.

## Executive Summary

Foundry’s GIS surfaces employ the Zoom-Tier Reveal Pattern to resolve the conflict between data density and legibility. Standard map clustering typically collapses multiple points into a generic numeric count, sacrificing qualitative data for performance. In contrast, the Zoom-Tier Reveal Pattern utilizes a transition band—currently set between zoom levels 8.0 and 8.5—to crossfade between aggregate cluster-centroid rings (showing brand-family distribution) and individual anchor markers. This ensures that the retail taxonomy remains visible and actionable at every scale.

## Implementation Strategy

### Threshold Calibration
The transition threshold is calibrated based on three primary factors:
1.  **Spatial Separation**: The zoom level at which individual anchors occupy sufficient screen real estate to be visually distinct.
2.  **Semantic Priority**: The point at which a regional density signal (e.g., "this corridor is Hardware-dominant") becomes less valuable than specific asset identification.
3.  **Crossfade Logic**: A 0.5-stop zoom interval (8.0 to 8.5) is utilized to interpolate opacity between layers, preventing the jarring "snap" associated with hard-threshold toggling.

### Layer Composition
- **Low Magnification (< 8.0)**: Only cluster-centroid rings are intended to render. These rings utilize concentric or pie-chart geometry to represent the brand-family mix within a co-location cluster.
- **Transition Band (8.0 - 8.5)**: Both layers render with inverse opacity interpolations, facilitating a smooth visual handover.
- **High Magnification (> 8.5)**: Individual anchor swatches and markers are rendered, while the aggregate centroid is fully suppressed.

## Technical Specifications (MapLibre Integration)

The pattern is implemented through declarative paint expressions within the MapLibre GL JS engine. By binding layer opacity to the map's zoom state via linear interpolation, the system maintains high performance without manual event listeners.

```javascript
// Example: Interpolated Opacity for Cluster Centroids
'circle-opacity': [
  'interpolate', ['linear'], ['zoom'],
  8.0, 1.0,  // Fully opaque below threshold
  8.5, 0.0   // Fully transparent above threshold
]
```

## Accessibility and Compliance
- **Motion Sensitivity**: For users with `prefers-reduced-motion: reduce` enabled, the 500ms crossfade is intended to collapse into an instant layer swap to minimize vestibular triggers.
- **Keyboard Navigation**: The Tab order is dynamically updated as zoom levels cross the threshold, ensuring only visible markers are reachable by keyboard.
- **Semantic Continuity**: Cluster centroids are treated as first-class data entities (`role="graphics-symbol"`), ensuring screen-readers announce the aggregate density as a meaningful summary rather than an optimization artifact.

## Strategic Roadmap
Future research is intended to investigate:
- **Multi-Tier Reveal**: A planned three-tier system (Regional → Cluster → Individual) for ultra-high-density urban environments.
- **Adaptive Thresholds**: Intended development of dynamic thresholds that adjust based on local data density, ensuring consistent visual clarity in both rural and metropolitan datasets.
- **Click-to-Zoom Pathing**: Research is ongoing to determine if clicking a cluster centroid should fly to the exact reveal threshold or to a predefined higher-magnification detail view (e.g., zoom 13).
