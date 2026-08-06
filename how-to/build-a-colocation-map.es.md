---
schema: foundry-doc-v1
title: "Construir un mapa de co-ubicación"
slug: build-a-colocation-map
short_description: "Renderiza marcadores de clúster de co-ubicación coloreados por nivel en MapLibre GL cargando un archivo PMTiles directamente — la arquitectura real de archivo plano, ya que no existe ninguna API REST de clústeres con token bearer."
category: how-to
index_group: integration-data
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: build-a-colocation-map.md
---

## Requisitos previos

- Un proyecto web con MapLibre GL JS v3 o posterior cargado
- La biblioteca JS `pmtiles`, para leer el formato de archivo de tiles PMTiles
- La URL del archivo PMTiles de su despliegue (o su endpoint de servidor de tiles Martin, si su despliegue genera tiles dinámicamente)

## Propósito

Renderice clústeres de co-ubicación coloreados por nivel en un mapa MapLibre — la arquitectura real es un archivo de tiles plano leído directamente por el navegador, no una API REST en vivo contra la que se autentica. No hay clave de API, ni intercambio de tokens, ni facturación por solicitud que planificar.

## Procedimiento

1. Registre el manejador de protocolo PMTiles con MapLibre antes de crear su mapa:

   ```javascript
   import maplibregl from 'maplibre-gl';
   import { Protocol } from 'pmtiles';

   const protocol = new Protocol();
   maplibregl.addProtocol('pmtiles', protocol.tile);
   ```

2. Inicialice el mapa, dando a su elemento contenedor una altura CSS explícita — un contenedor sin dimensionar se renderiza con altura cero:

   ```javascript
   const map = new maplibregl.Map({
     container: 'map',
     style: '<url-de-su-estilo-de-mapa-base>',
     center: [-98.5, 39.5],
     zoom: 4,
   });
   ```

3. Añada el archivo de clústeres como una fuente `pmtiles://` una vez que el mapa haya cargado:

   ```javascript
   map.on('load', () => {
     map.addSource('clusters', {
       type: 'vector',
       url: 'pmtiles://<url-pmtiles-de-su-despliegue>',
     });
   ```

   Si su despliegue genera tiles dinámicamente en lugar de servir un archivo pre-generado, apunte una fuente `type: 'vector'` a la URL `tiles.json` del endpoint de su servidor de tiles Martin en su lugar — el resto de esta guía es idéntico de cualquier manera.

4. Añada la capa de círculos coloreados por nivel, referenciando el nombre de la capa fuente que realmente usa su archivo:

   ```javascript
     map.addLayer({
       id: 'cluster-circles',
       type: 'circle',
       source: 'clusters',
       'source-layer': '<nombre-de-su-capa-fuente>',
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

## Resultado esperado

Los marcadores de clúster se renderizan en el mapa, codificados por color y tamaño según el nivel — T1 el más grande y prominente, T3 el más pequeño — sin ningún paso de autenticación en todo el flujo.

## Verificación

Confirme que los marcadores aparecen en el nivel de zoom esperado y que al hacer clic o pasar el cursor sobre uno se muestra un valor `tier` que coincide con su color renderizado. Si nada se renderiza, revise primero la consola del navegador en busca de un error de obtención de PMTiles — una URL de archivo incorrecta falla silenciosamente en el lienzo del mapa pero no en la pestaña de red.

## Reversión

Elimine la fuente y la capa añadidas, o simplemente no monte el componente del mapa — nada en esta integración escribe en ningún backend; es una lectura pura de un archivo estático (o generado dinámicamente en tiles).

## Próximos pasos

- [[connect-osm-data-pipeline]] — añada una nueva cadena a los datos que renderiza este mapa

## Véase también

- [[location-intelligence-substrate]] — la arquitectura completa de archivo plano/PMTiles/MapLibre/Martin detrás de esta integración
