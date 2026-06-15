---
schema: foundry-doc-v1
title: "Cómo construir un mapa de co-ubicación"
slug: build-a-colocation-map
category: how-to
content_type: how-to
type: how-to
status: stable
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: build-a-colocation-map.md
---

El motor GIS de PointSav expone una API de tiles y un punto de conexión de clústeres que puedes integrar en cualquier aplicación MapLibre GL. Esta guía cubre la autenticación con la API GIS, la obtención de la capa GeoJSON de clústeres y la renderización de marcadores de clústeres con color por nivel en un lienzo MapLibre.

Para la arquitectura del motor GIS, consulta [[pointsav-gis-engine]]. Para el sistema de puntuación de co-ubicación que produce los datos de clústeres, consulta [[topic-co-location-ranking-system|sistema de clasificación de co-ubicación]].

## Antes de empezar

Necesitas:

- Una clave de API GIS proporcionada por el administrador de la plataforma
- Un proyecto web con MapLibre GL JS v3 o posterior cargado
- La URL base de tu despliegue GIS (por ejemplo, `https://gis.example.com`)

## Paso 1: Intercambia tu clave de API por un token de sesión

El punto de conexión de clústeres requiere un token bearer de corta duración.
Intercambia tu clave de API en el punto de autenticación:

```shell
curl -X POST https://<tu-host-gis>/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"api_key": "<tu-clave-de-api>"}' \
  -o token.json

TOKEN=$(jq -r .access_token token.json)
```

Los tokens vencen después de una hora. Para renovar, repite el intercambio.
Si tu aplicación corre en un navegador, realiza este intercambio en el lado
del servidor y actúa como proxy del punto de conexión de clústeres para evitar
exponer la clave de API a los clientes.

## Paso 2: Obtén el GeoJSON de clústeres

Descarga la capa de clústeres para los países que deseas mostrar:

```shell
curl -fsSL \
  -H "Authorization: Bearer $TOKEN" \
  "https://<tu-host-gis>/api/v1/clusters?country=US" \
  -o clusters.geojson
```

La respuesta es un `FeatureCollection` GeoJSON. Cada característica tiene una
propiedad `tier` (`T1`, `T2` o `T3`) y un `cluster_id`. Los parámetros de
consulta opcionales son `country` (ISO 3166-1 alpha-2), `min_tier` (`T1` o
`T2`) y `bbox` (`oeste,sur,este,norte`).

## Paso 3: Inicializa el mapa MapLibre

```javascript
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const map = new maplibregl.Map({
  container: 'map',            // id del elemento DOM donde montar el mapa
  style: '<url-del-estilo-base>',
  center: [-98.5, 39.5],      // lon, lat
  zoom: 4,
});
```

Reemplaza `style` con la URL del mapa base de tu despliegue. El elemento
contenedor del mapa debe tener una altura CSS explícita; un contenedor sin
dimensiones se renderiza con altura cero.

## Paso 4: Agrega la fuente GeoJSON de clústeres

```javascript
map.on('load', () => {
  map.addSource('clusters', {
    type: 'geojson',
    data: clusters,          // el objeto FeatureCollection ya analizado
  });
```

Si sirves el GeoJSON directamente desde el punto de conexión de la API en un
contexto de navegador, pasa la URL del punto de conexión como `data` y
proporciona el token bearer mediante una función de retorno de llamada
`transformRequest` en las opciones del constructor `Map`.

## Paso 5: Agrega la capa de círculos con color por nivel

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

Los clústeres T1 (centros regionales, mayor composición de anclas) se
renderizan más grandes y en azul. Los clústeres T2 (centros de distrito) en
púrpura. Los clústeres T3 (pares locales) en gris y con el tamaño más
pequeño. Ajusta los colores y radios para que coincidan con el lenguaje visual
de tu aplicación.

## Véase también

- [[pointsav-gis-engine]] — arquitectura del motor GIS y superficies de API disponibles
- [[topic-co-location-methodology|metodología de co-ubicación]] — cómo se puntúan los niveles de los clústeres
- [[topic-od-catchment-methodology|metodología de captación O-D]] — cómo se definen las áreas comerciales
- [[federate-archives-via-content-mounts]] — monta datos de inteligencia de ubicación en una segunda instancia
