---
schema: foundry-doc-v1
title: "Build a co-location map"
slug: build-a-colocation-map
short_description: "Renders tier-coloured co-location cluster markers in MapLibre GL by loading a PMTiles archive directly — the real flat-file architecture, since no bearer-token REST cluster API exists."
category: how-to
index_group: integration-data
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: build-a-colocation-map.es.md
research_trail:
  sources: [substrate/location-intelligence-substrate.md (the real flat-file/PMTiles/MapLibre/Martin architecture, already fact-checked 2026-08-01)]
  verification_method: "this guide's own prior Correction note had already confirmed the bearer-token REST API was fictional and pointed to location-intelligence-substrate.md as the real architecture; this rewrite is grounded directly in that already-verified article rather than re-deriving the tile-serving mechanism from scratch, and stays deliberately generic on deployment-specific URLs/ports that aren't confirmed anywhere in source"
---

## Prerequisites

- A web project with MapLibre GL JS v3 or later loaded
- The `pmtiles` JS library, for reading the PMTiles tile archive format
- The URL of your deployment's PMTiles archive (or its Martin tile-server endpoint, if your deployment generates tiles dynamically)

## Purpose

Render tier-coloured co-location clusters on a MapLibre map — the real architecture is a flat-file tile archive read directly by the browser, not a live REST API you authenticate against. There's no API key, no token exchange, and no per-request billing to plan around.

## Procedure

1. Register the PMTiles protocol handler with MapLibre before creating your map:

   ```javascript
   import maplibregl from 'maplibre-gl';
   import { Protocol } from 'pmtiles';

   const protocol = new Protocol();
   maplibregl.addProtocol('pmtiles', protocol.tile);
   ```

2. Initialize the map, giving its container element an explicit CSS height — an unsized container renders at zero height:

   ```javascript
   const map = new maplibregl.Map({
     container: 'map',
     style: '<your-basemap-style-url>',
     center: [-98.5, 39.5],
     zoom: 4,
   });
   ```

3. Add the cluster archive as a `pmtiles://` source once the map has loaded:

   ```javascript
   map.on('load', () => {
     map.addSource('clusters', {
       type: 'vector',
       url: 'pmtiles://<your-deployment-pmtiles-url>',
     });
   ```

   If your deployment generates tiles dynamically instead of serving a pre-baked archive, point a `type: 'vector'` source at your Martin tile-server endpoint's `tiles.json` URL instead — the rest of this guide is identical either way.

4. Add the tier-coloured circle layer, referencing the source layer name your archive actually uses:

   ```javascript
     map.addLayer({
       id: 'cluster-circles',
       type: 'circle',
       source: 'clusters',
       'source-layer': '<your-source-layer-name>',
       paint: {
         'circle-color': [
           'match', ['get', 'tier'],
           'T1', '#2563eb',
           'T2', '#7c3aed',
           /* T3 */ '#6b7280',
         ],
         'circle-radius': [
           'match', ['get', 'tier'],
           'T1', 12,
           'T2', 9,
           /* T3 */ 6,
         ],
         'circle-opacity': 0.85,
       },
     });
   });
   ```

## Expected outcome

Cluster markers render on the map, colour- and size-coded by tier — T1 largest and most prominent, T3 smallest — with no authentication step anywhere in the flow.

## Verification

Confirm markers appear at the expected zoom level and that clicking or hovering one shows a `tier` value matching its rendered colour. If nothing renders, check the browser console for a PMTiles fetch error first — a wrong archive URL fails silently on the map canvas but not in the network tab.

## Rollback

Remove the added source and layer, or simply don't mount the map component — nothing about this integration writes to any backend; it's a pure read of a static (or dynamically-tiled) archive.

## Next steps

- [[connect-osm-data-pipeline]] — add a new chain to the data this map renders

## See also

- [[location-intelligence-substrate]] — the full flat-file/PMTiles/MapLibre/Martin architecture behind this integration
