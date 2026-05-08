---
schema: foundry-doc-v1
title: "Location Intelligence UX Design Philosophy"
slug: location-intelligence-ux
category: architecture
type: topic
quality: complete
short_description: "The Location Intelligence interface uses a Conclusion-First design philosophy — rendering ranked tier conclusions rather than individual data points — so a user comparing markets at a national zoom level sees the most defensible commercial nodes immediately, and only drills into individual operators when a node has earned the attention."
status: active
audience: public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: location-intelligence-ux.es.md
---

The PointSav Location Intelligence interface uses a Conclusion-First design philosophy — rendering ranked tier conclusions rather than individual data points — so a user comparing markets at a national zoom level sees the most defensible commercial nodes immediately, and only drills into individual operators when a node has earned the attention. The interface draws inspiration from professional-grade spatial platforms where complex multi-parameter models are rendered as intuitive layered navigation surfaces rather than legend-driven dot maps.

## Quality Benchmark: The Professional Map

The interface draws inspiration from professional-grade spatial platforms (e.g., meteoblue.com), where complex multi-parameter models are rendered as intuitive, layered navigation surfaces. Key design patterns adopted from this benchmark include:

-   **First-Class Layer Toggles:** Analytical layers (Clusters, Catchment, OD Study) are presented as primary navigation controls, not secondary legend items.
-   **Decision-Driven Visualization:** The map renders conclusions (e.g., "This node is Tier 5") rather than individual data points, allowing for rapid cross-market comparisons.
-   **Scale-Adaptive Legibility:** Visual detail adapts dynamically to zoom level, ensuring a coherent national overview without sacrificing street-level precision.

## Design Differentiation: Cluster-Grade-as-Primary-Unit

Unlike commercial GIS products that default to individual "dots on a map," the PointSav platform utilizes **Cluster Grade** as the primary visual and analytical unit. This differentiation represents a core Leapfrog 2030 design principle:

1.  **Confidence Ramp:** Sites are encoded using a single-hue color ramp (pale to deep amber). Darker, larger markers indicate higher levels of capital-validated convergence.
2.  **Structural Guardrails:** The interface enforces a strict visual hierarchy where Tier 5 and Tier 4 nodes dominate the national view, guiding the user toward the most defensible commercial nodes.
3.  **Contextual index-cards:** Clicking a cluster activates a side-drawer (not a modal) that provides immediate municipal ranking, operator chips, and institutional support counts without losing map context.

## Component Architecture

The GIS surface utilizes a standardized component set designed for rapid re-provisioning:
-   **cluster-grade-marker:** A five-state vector symbol with built-in accessibility labeling (D1-D5).
-   **location-index-card:** A responsive, data-dense drawer for cluster-level metadata.
-   **map-layer-controls:** A consistent UI panel for managing the three-layer architecture.
