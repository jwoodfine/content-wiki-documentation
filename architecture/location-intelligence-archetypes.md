---
schema: foundry-doc-v1
title: "Location Intelligence Archetypes"
slug: location-intelligence-archetypes
category: architecture
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: location-intelligence-archetypes.es.md
short_description: "The PRO, VWH, and PKS archetypes classify retail anchor compositions by functional role within a co-location cluster, providing the taxonomy that drives GIS analysis and map integration."
cites: []
---

Location intelligence archetypes are the classification labels assigned to anchor tenants within a co-location cluster based on their functional role in the retail ecosystem. The three primary archetypes — PRO (Professional), VWH (Warehouse), and PKS (Park-style) — describe the dominant commercial draw pattern of each anchor and determine how the cluster is scored in the [[location-intelligence-strategy|location intelligence strategy]].

## PRO — Professional

The PRO archetype identifies anchors whose primary draw is professional services rather than retail consumption: banks, clinics, government offices, and professional-services franchises. PRO anchors generate foot traffic peaks that correlate with business hours and tend to cluster in higher-density urban locations.

## VWH — Warehouse

The VWH archetype identifies large-format anchors that operate on a warehouse-club or big-box model: hypermarkets, hardware chains, and wholesale clubs. VWH anchors generate the high-volume, recurring consumer traffic that forms the foundation of the co-location clustering model.

## PKS — Park-style

The PKS archetype identifies anchors within enclosed mall or commercial park configurations, where a single landlord controls the co-tenancy relationship among anchors. PKS clusters exhibit different lease and traffic patterns than open-pad co-location clusters.

## Taxonomy and pipeline

Each anchor in the source POI dataset is classified into one of these three archetypes during the nightly pipeline run. The resulting per-cluster archetype composition determines cluster tier (T1, T2, T3) and feeds the spatial tile layers served by the GIS surface.

## See also

- [[location-intelligence-strategy|Location Intelligence Strategy]] — the strategic framework that uses the archetype taxonomy
- [[ppn-small-business-compute|PPN Small-Business Compute]] — the compute layer that hosts the GIS analysis pipeline

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™, and Capability Geometry™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
