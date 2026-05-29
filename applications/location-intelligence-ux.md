---
schema: foundry-doc-v1
title: "Location intelligence UX design philosophy"
slug: location-intelligence-ux
category: applications
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-19
editor: pointsav-engineering
short_description: "The PointSav Location Intelligence interface is engineered for decision-maker clarity, using a Conclusion-First design philosophy that communicates site-selection confidence through visual hierarchy and structural grading rather than raw data volume."
paired_with: location-intelligence-ux.es.md
---

The [[location-intelligence-platform]] interface is engineered to prioritize decision-maker clarity over raw data volume. By using a Conclusion-First design philosophy, the platform communicates site-selection confidence through visual hierarchy and structural grading, applying the [[co-location-methodology|co-location scoring methodology]] as the primary analytical unit.

## Quality benchmark: the professional map

The interface draws inspiration from professional-grade spatial platforms, where complex multi-parameter models are rendered as intuitive, layered navigation surfaces. Key design patterns adopted from this benchmark include:

- **First-class layer toggles:** Analytical layers (Clusters, Catchment, OD Study) are presented as primary navigation controls, not secondary legend items.
- **Decision-driven visualization:** The map renders conclusions (for example, "This node is Tier 5") rather than individual data points, allowing for rapid cross-market comparisons.
- **Scale-adaptive legibility:** Visual detail adapts dynamically to zoom level, ensuring a coherent national overview without sacrificing street-level precision.

## Design differentiation: cluster grade as primary unit

Unlike commercial GIS products that default to individual points on a map, the PointSav platform uses **Cluster Grade** as the primary visual and analytical unit. This differentiation represents a core design principle:

1. **Confidence ramp:** Sites are encoded using a single-hue color ramp (pale to deep amber). Darker, larger markers indicate higher levels of capital-validated convergence.
2. **Structural guardrails:** The interface enforces a strict visual hierarchy where Tier 5 and Tier 4 nodes dominate the national view, guiding the user toward the most defensible commercial nodes.
3. **Contextual index cards:** Clicking a cluster activates a side drawer — not a modal — that provides immediate municipal ranking, operator chips, and institutional support counts without losing map context.

## Component architecture

The GIS surface uses a standardized component set built on [[app-orchestration-gis]] (the analytics engine) and [[pointsav-gis-engine]] (the rendering layer), designed for rapid re-provisioning across deployments.

## See also

- [[location-intelligence-platform]] — the full platform article covering data foundations and sovereign architecture
- [[app-orchestration-gis]] — the analytics engine that produces the cluster grades displayed in the interface
- [[pointsav-gis-engine]] — the rendering layer that serves vector tiles to the map surface
- [[co-location-methodology]] — the scoring and ranking methodology visualised by the interface
