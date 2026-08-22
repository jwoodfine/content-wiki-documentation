---
schema: foundry-doc-v1
title: "Location intelligence UX design philosophy"
slug: location-intelligence-ux
aliases:
  - location-intelligence-ux
category: patterns
type: topic
content_type: topic
quality: complete
index_group: interface-and-user-experience
short_description: "Conclusion-First interface philosophy rendering ranked tier conclusions rather than individual data points, so defensible commercial nodes surface immediately."
status: active
audience: public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: location-intelligence-ux.es.md
---

The PointSav [[location-intelligence-platform|Location Intelligence]] interface uses a Conclusion-First design philosophy — rendering ranked tier conclusions rather than individual data points — so a user comparing markets at a national zoom level sees the most defensible commercial nodes immediately, and only drills into individual operators when a node has earned the attention. The interface draws inspiration from professional-grade spatial platforms where complex multi-parameter models are rendered as intuitive layered navigation surfaces rather than legend-driven dot maps. The [[app-orchestration-gis|GIS orchestration surface]] delivers this design at production scale.

## Quality Benchmark: The Professional Map

The interface draws inspiration from professional-grade spatial platforms (e.g., meteoblue.com), where complex multi-parameter models are rendered as intuitive, layered navigation surfaces. Key design patterns adopted from this benchmark include:

- **First-Class Layer Toggles:** Analytical layers (Clusters, Catchment, OD Study) are presented as primary navigation controls, not secondary legend items.
- **Decision-Driven Visualization:** The map renders conclusions (e.g., "This node is Tier 5") rather than individual data points, allowing for rapid cross-market comparisons.
- **Scale-Adaptive Legibility:** Visual detail adapts dynamically to zoom level, ensuring a coherent national overview without sacrificing street-level precision.

## Design differentiation: cluster grade as the primary unit

Unlike commercial GIS products that default to individual "dots on a map," the PointSav platform uses **cluster grade** as the primary visual and analytical unit. **A user scanning the national map sees which clusters are worth their attention before they see any individual site.** The map answers the ranking question first, not last. This differentiation reflects three design choices:

1. **Multi-hue tier encoding.** Sites are color-coded across four tiers — Regional, District, Local, and Fringe — using a distinct hue per tier rather than a single gradient. A user distinguishes tiers by color family at a glance, not by judging shade intensity against neighboring markers.
2. **Structural guardrails.** The interface enforces a visual hierarchy where Regional and District nodes dominate the national view, guiding the user toward the most defensible commercial nodes before the lower tiers compete for attention.
3. **Contextual drawer, not a modal.** Clicking a cluster opens a side drawer that provides immediate municipal ranking, operator detail, and institutional support counts without losing map context — the underlying map stays visible and interactive behind the drawer.

## Component architecture

The GIS surface's cluster inspector is a drawer component (internally named "BentoBox") that renders cluster-level metadata in a dense, scannable layout without requiring the user to leave the map view. The four-tier color scheme and the drawer pattern together are what make the cluster-as-primary-unit choice legible to a reader browsing a national-scale map.

## See also

- [[location-intelligence-platform]] — the location intelligence platform these UX patterns serve
- [[app-orchestration-gis]] — the GIS orchestration surface that implements this design
- [[retail-co-location-tier-methodology]] — the tier methodology that produces the tier conclusions displayed
