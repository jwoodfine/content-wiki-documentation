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
short_description: "The PRO, VWH, and PKS archetypes classify retail anchor compositions by functional role within a co-location cluster, providing the taxonomy that drives GIS analysis and map integration. PRO denotes Retail Centres, VWH denotes Urban Fringe, and PKS denotes Commuter locations."
cites: []
---

Location intelligence archetypes are the classification labels assigned to anchor tenants within a co-location cluster based on their functional role in the retail ecosystem. The three primary archetypes — PRO (Retail Centres), VWH (Urban Fringe), and PKS (Commuter) — describe the dominant commercial draw pattern of each anchor and determine how the cluster is scored in the location intelligence strategy.

## PRO — Retail Centres

The PRO archetype identifies retail-centre anchors whose primary draw is concentrated consumer retail: shopping centres, high-street parades, and town-centre destinations. PRO anchors generate foot traffic peaks that correlate with retail trading hours and tend to cluster in higher-density urban locations.

## VWH — Urban Fringe

The VWH archetype identifies large-format anchors on the urban fringe that operate on a warehouse-club or big-box model: hypermarkets, hardware chains, and wholesale clubs. VWH anchors generate the high-volume, recurring consumer traffic that forms the foundation of the co-location clustering model.

## PKS — Commuter

The PKS archetype identifies commuter-oriented anchors positioned around transit corridors and park-and-ride catchments, where draw is driven by journey-to-work flows rather than destination retail. PKS clusters exhibit different lease and traffic patterns than open-pad co-location clusters.

## Taxonomy and pipeline

Each anchor in the source POI dataset is classified into one of these three archetypes during the nightly pipeline run. The resulting per-cluster archetype composition determines cluster tier (T1, T2, T3) and feeds the spatial tile layers served by the GIS surface.

## See also

- Location Intelligence Strategy — the strategic framework that uses the archetype taxonomy
- [[ppn-small-business-compute|PPN Small-Business Compute]] — the compute layer that hosts the GIS analysis pipeline

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™, and Capability Geometry™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
