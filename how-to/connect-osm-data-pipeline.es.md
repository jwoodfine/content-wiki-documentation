---
schema: foundry-doc-v1
title: "Conectarse al pipeline de datos OSM"
slug: connect-osm-data-pipeline
short_description: "Ingiere una nueva cadena minorista o de servicios desde OpenStreetMap usando el script real ingest-osm.py y los diccionarios CATEGORIES/BRAND_FILL de taxonomy.py, y luego reconstruye los tiles de clúster servibles."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: connect-osm-data-pipeline.md
---

## Requisitos previos

- Acceso al directorio de trabajo `app-orchestration-gis` (los scripts del pipeline)
- Python 3.11+ con las dependencias del pipeline instaladas
- Acceso de red a la API de Overpass
- Un Q-ID de Wikidata para la cadena que está ingiriendo (búsquelo en wikidata.org)

## Propósito

Añada una nueva cadena minorista o de servicios al pipeline de inteligencia de ubicación — desde datos crudos de OpenStreetMap hasta un tile de clúster servible. Un procedimiento genuinamente ya ejecutado antes, no hipotético.

## Procedimiento

1. Busque el Q-ID de Wikidata de la cadena. Este es el identificador estable y neutral en idioma al que se ancla la taxonomía (Walmart: Q483551, IKEA: Q54078). Si la cadena no tiene una entrada limpia en Wikidata, más adelante recurrirá a una consulta basada en nombre.

2. Ejecute el script de ingestión directamente contra el identificador de la cadena — no hay ningún archivo YAML descriptor separado que redactar para una ejecución sencilla:

   ```bash
   python3 ingest-osm.py --chain <id-de-cadena>
   ```

   Esto consulta la API de Overpass y escribe registros JSONL en el directorio de datos de la plataforma. Si la cadena devuelve cero registros, la cobertura de etiquetas de Wikidata puede ser escasa en OpenStreetMap para esa cadena — revise si conviene una consulta de respaldo basada en nombre antes de asumir que la cadena no tiene datos.

3. Registre la categoría de la cadena en `taxonomy.py`, en el diccionario `CATEGORIES`:

   ```python
   "su_categoria_slug": {
       "label": "Nombre de Categoría Legible",
       "naics": "<codigo-naics>",
       "description": "Una línea describiendo qué señala esta categoría.",
   },
   ```

4. Añada la cadena a `BRAND_FILL`, bajo su categoría, indexado por código de país:

   ```python
   "su_categoria_slug": {
       "US": ["su-id-de-cadena"],
       "CA": [],
       # ... cada país mostrado necesita una entrada, incluso si está vacía
   },
   ```

5. Reconstruya la capa de clústeres y sus tiles servibles:

   ```bash
   python3 build-clusters.py       # reconstruye work/clusters.geojson desde todas las cadenas registradas
   python3 build-tiles.py --layer 2  # regenera el archivo PMTiles servido al mapa
   ```

## Resultado esperado

Las ubicaciones de la nueva cadena están presentes en el GeoJSON de clúster reconstruido y reflejadas en el archivo PMTiles regenerado que realmente sirve el mapa.

## Verificación

Verifique que el recuento de registros de la nueva cadena llegó como se esperaba:

```bash
grep -c '"chain":"su-id-de-cadena"' ruta/a/su-id-de-cadena.jsonl
```

Luego confirme que aparece en la salida de clúster reconstruida antes de dar por completa la ingestión. Una cadena registrada en la taxonomía pero nunca realmente ingerida, o una ingestión que se ejecutó pero nunca se incluyó en una reconstrucción, ambas dejan el mapa mostrando datos obsoletos sin ningún error que lo advierta.

## Reversión

Elimine las entradas de la cadena de `CATEGORIES`/`BRAND_FILL` y borre su archivo JSONL, luego vuelva a ejecutar los pasos de reconstrucción para regenerar la salida de clústeres sin ella. No hay un "deshacer" en el lugar para una reconstrucción ya servida — el estado anterior solo es recuperable reconstruyendo de nuevo desde una taxonomía que la excluya.

## Próximos pasos

- [[build-a-colocation-map]] — renderice los tiles de clúster reconstruidos en una aplicación MapLibre

## Véase también

- [[location-intelligence-substrate]] — la arquitectura de archivo plano/PMTiles que alimenta este pipeline
