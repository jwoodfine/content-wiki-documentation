---
schema: foundry-doc-v1
title: "Cómo conectarse al pipeline de datos OSM"
slug: connect-osm-data-pipeline
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: connect-osm-data-pipeline.md
---

El sistema de inteligencia de ubicación de la plataforma ingesta datos de puntos de interés (POI) de OpenStreetMap a través de archivos de ingestión JSONL. Conectarse al pipeline de datos OSM significa escribir o adaptar un script de ingestión que consulte la API de Overpass, produciendo un archivo JSONL en el esquema de la plataforma y registrando la ingestión con la configuración de taxonomía. Esta guía cubre una ingestión de cadena única para una nueva categoría minorista o de servicios.

Para la arquitectura del motor GIS, véase [[pointsav-gis-engine]]. Para construir un mapa a partir de datos de clusters ingeridos, véase [[build-a-colocation-map]].

## Requisitos previos

- Acceso al directorio de trabajo `app-orchestration-gis` (los scripts de pipeline)
- Python 3.9+ con `requests` disponible
- Acceso de red a la API de Overpass (`overpass-api.de` o un espejo local)
- Un Q-ID de Wikidata para la cadena o categoría que se está ingestando (búsquelo en `wikidata.org`)

## Paso 1: Identificar el Q-ID de Wikidata

Cada cadena en la taxonomía está anclada a un Q-ID de Wikidata. Esto proporciona un identificador estable e independiente del idioma para la entidad. Busque la cadena en Wikidata y registre el Q-ID (p.ej., Walmart: Q483551, IKEA: Q54078).

Si la categoría no tiene una entrada de Wikidata única, use una consulta basada en nombre (modo `name_query`) en lugar de una búsqueda por Q-ID.

## Paso 2: Escribir el YAML de ingestión

Cree un archivo YAML de ingestión bajo `service-business/` con el nombre `<nombre-cadena>-<código-país>.yaml`:

```yaml
chain: walmart-us
wikidata_id: Q483551
query_mode: wikidata    # o: name_query
name_query: null         # usado solo cuando query_mode: name_query
country_code: US
bbox: [-125.0, 24.4, -66.9, 49.4]   # cuadro delimitador para el país
output: service-business/walmart-us.jsonl
taxonomy_family: ALPHA_HYPERMARKET
taxonomy_tier: 1
```

Para el modo `name_query` (cuando la cobertura de Wikidata es escasa), establezca `query_mode: name_query` y proporcione `name_query: "Walmart"`. El script de ingestión realiza una búsqueda de nombre de texto libre en la API de Overpass.

## Paso 3: Ejecutar el script de ingestión

Ejecute el script de ingestión existente con el nuevo YAML:

```
python3 app-orchestration-gis/ingest-chain.py service-business/walmart-us.yaml
```

El script consulta la API de Overpass, filtra los resultados por el cuadro delimitador y el código de país, y escribe registros JSONL en `service-business/walmart-us.jsonl`. Cada registro contiene: `name`, `lat`, `lon`, `wikidata_id`, `chain`, `country`, `taxonomy_family`, `taxonomy_tier`.

Recuentos de registros típicos: las cadenas urbanas densas producen 500–2.000 registros; las cadenas de hipermercados nacionales producen 100–500; los minoristas especializados producen 50–200.

## Paso 4: Registrar la cadena en la taxonomía

Añada la nueva cadena a la configuración de taxonomía en `app-orchestration-gis/taxonomy.py` bajo el grupo de familia apropiado:

```python
"walmart-us": TaxonomyEntry(
    family="ALPHA_HYPERMARKET",
    tier=1,
    jsonl_path="service-business/walmart-us.jsonl",
    wikidata_id="Q483551",
),
```

## Paso 5: Reconstruir la capa de clusters

Después del registro, reconstruya la capa de clusters para incorporar los nuevos datos POI:

```
python3 app-orchestration-gis/build-geometric-ranking.py
```

La reconstrucción lee todos los archivos JSONL registrados, ejecuta el paso de agrupamiento DBSCAN y regenera `clusters-meta.json`. Verifique que la nueva cadena aparezca en la salida del cluster:

```
python3 -c "import json; d=json.load(open('gateway/www/data/clusters-meta.json')); print(sum(1 for c in d['clusters'] if 'walmart' in str(c)))"
```

## Puntos clave

- Cada cadena requiere un descriptor YAML de ingestión y un archivo de salida JSONL en `service-business/`
- Los Q-IDs de Wikidata son preferibles a las consultas de nombre; recurra a consultas de nombre solo cuando la cobertura de Wikidata esté ausente
- El paso de registro de taxonomía vincula el archivo JSONL con el pipeline de agrupamiento
- Se requiere una reconstrucción completa del cluster después de añadir una nueva cadena — las actualizaciones incrementales no están soportadas en el pipeline actual

## Véase también

- [[pointsav-gis-engine]] — la arquitectura del motor GIS y el pipeline de agrupamiento DBSCAN
- [[build-a-colocation-map]] — cómo mostrar los datos del cluster en una aplicación web MapLibre
- [[location-intelligence-archetypes]] — el modelo de arquetipos PRO/VWH/PKS que alimenta la taxonomía
- [[export-structured-data]] — exportar el GeoJSON resultante para uso externo
