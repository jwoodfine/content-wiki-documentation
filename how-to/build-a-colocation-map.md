---
schema: foundry-doc-v1
title: "How to build a co-location map"
slug: build-a-colocation-map
category: how-to
content_type: how-to
type: how-to
status: stable
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: build-a-colocation-map.es.md
---

The PointSav GIS engine exposes a tile API and a clusters endpoint that you can integrate into any MapLibre GL application. This guide covers authenticating against the GIS API, fetching the cluster GeoJSON layer, and rendering tier-coloured cluster markers on a MapLibre map canvas.

For the GIS engine architecture, see [[pointsav-gis-engine]]. For the co-location scoring system that produces the cluster data, see [[topic-co-location-ranking-system|co-location ranking system]].

## Before you begin

You need:

- A GIS API key from the platform administrator
- A web project with MapLibre GL JS v3 or later loaded
- The base URL of your GIS deployment (for example, `https://gis.example.com`)

## Step 1: Exchange your API key for a session token

The clusters endpoint requires a short-lived bearer token. Exchange your API
key at the authentication endpoint:

```shell
curl -X POST https://<your-gis-host>/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"api_key": "<your-api-key>"}' \
  -o token.json

TOKEN=$(jq -r .access_token token.json)
```

Tokens expire after one hour. Refresh by repeating the exchange. If your
application runs in a browser, perform this exchange server-side and proxy
the clusters endpoint to avoid exposing the API key to clients.

## Step 2: Fetch the cluster GeoJSON

Download the cluster layer for the countries you want to display:

```shell
curl -fsSL \
  -H "Authorization: Bearer $TOKEN" \
  "https://<your-gis-host>/api/v1/clusters?country=US" \
  -o clusters.geojson
```

The response is a GeoJSON `FeatureCollection`. Each feature carries a `tier`
property (`T1`, `T2`, or `T3`) and a `cluster_id`. Optional query parameters
include `country` (ISO 3166-1 alpha-2), `min_tier` (`T1` or `T2`), and `bbox`
(`west,south,east,north`).

## Step 3: Initialise the MapLibre map

```javascript
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const map = new maplibregl.Map({
  container: 'map',          // id of the DOM element to mount into
  style: '<your-basemap-style-url>',
  center: [-98.5, 39.5],    // lon, lat
  zoom: 4,
});
```

Replace the `style` value with the basemap URL from your deployment. The map
container element must have an explicit CSS height; an unsized container
renders at zero height.

## Step 4: Add the cluster GeoJSON source

```javascript
map.on('load', () => {
  map.addSource('clusters', {
    type: 'geojson',
    data: clusters,          // the parsed FeatureCollection object
  });
```

If you are serving the GeoJSON directly from the API endpoint in a browser
context, pass the endpoint URL as `data` and supply the bearer token using a
`transformRequest` callback in the `Map` constructor options.

## Step 5: Add the tier-coloured circle layer

```javascript
  map.addLayer({
    id: 'cluster-circles',
    type: 'circle',
    source: 'clusters',
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

T1 clusters (regional hubs, highest anchor composition) render largest in
blue. T2 clusters (district hubs) render in purple. T3 clusters (local pairs)
render smallest in grey. Adjust the colour and radius values to match your
application's visual language.

## See also

- [[pointsav-gis-engine]] — GIS engine architecture and available API surfaces
- [[topic-co-location-methodology|co-location methodology]] — how cluster tiers are scored
- [[topic-od-catchment-methodology|O-D catchment methodology]] — how trade areas are defined
- [[federate-archives-via-content-mounts]] — mount location-intelligence data into a second instance
