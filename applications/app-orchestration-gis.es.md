---
schema: foundry-doc-v1
title: "Aplicación de orquestación GIS"
slug: app-orchestration-gis
category: applications
type: topic
content_type: topic
quality: complete
index_group: location-intelligence-applications
status: active
audience: public
short_description: "El pipeline de datos en Python que produce las clasificaciones de co-ubicación de Woodfine y el mapa interactivo — geometría de clústeres reconstruida en un ciclo nocturno a partir de los conjuntos de datos de origen, publicada como mosaicos de mapa estáticos."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: app-orchestration-gis.md
cites:
 - pmtiles-spec
 - maplibre-gl-js
---

El pipeline que produce las clasificaciones de co-ubicación de Woodfine y el mapa interactivo en [gis.woodfinegroup.com](https://gis.woodfinegroup.com) es un pipeline de datos en Python, no un servicio permanente — no contiene datos canónicos propios y no produce salida alguna hasta que se ejecuta. Cada reconstrucción nocturna lee los conjuntos de datos actuales de negocios y lugares, reagrupa los clústeres, reasigna el nivel de cada uno y escribe mosaicos de mapa nuevos; los mosaicos que produce son lo que el sitio realmente sirve entre reconstrucciones.

## Asignación de nivel

El pipeline asigna a cada clúster uno de cuatro niveles evaluándolo frente a la
[[retail-co-location-tier-methodology|metodología de niveles de co-localización minorista]]
— composición, rango de población de captación, respaldo cívico y no solapamiento con
vecinos más fuertes. La asignación de nivel es una clasificación de aprobación/rechazo
frente a condiciones fijas, no una puntuación numérica compuesta.

## Generación de mosaicos

El pipeline compila la salida clasificada en activos de mosaicos vectoriales para su entrega al mapa interactivo:

- **Mosaicos vectoriales:** formato PMTiles para renderizado del lado del cliente sin necesidad de un servidor de mosaicos dedicado [pmtiles-spec]
- **Renderizado:** MapLibre GL JS procesa los mosaicos del lado del cliente con alto rendimiento [maplibre-gl-js]
- **Niveles visuales:** la convergencia espacial entre categorías de anclaje (primaria, ferretería, almacén, cívica) se traduce en la clasificación visual de cuatro niveles en la superficie del mapa, según la [[retail-co-location-tier-methodology|metodología de niveles]] anterior

## Ciclo de reconstrucción, no un servicio bajo demanda

El pipeline se ejecuta en un ciclo nocturno, no bajo demanda. Cada reconstrucción reagrupa los datos de origen actuales, regenera las capas de mosaicos y publica el resultado; el sitio, entre reconstrucciones, sirve lo que produjo la última ejecución exitosa. Esto simplifica la recuperación en un sentido concreto: un conjunto de mosaicos perdido o dañado se reemplaza con la siguiente reconstrucción programada, o con una reejecución bajo demanda, sin requerir migración de estado alguna. También significa que el mapa publicado refleja los datos de la última reconstrucción, no el instante actual.

## Véase también

- [[location-intelligence-substrate]] — la capa de renderizado que sirve los mosaicos producidos por este pipeline
- [[retail-co-location-tier-methodology]] — la metodología de niveles implementada por el pipeline
- [[location-intelligence-platform]] — el artículo de plataforma que cubre el despliegue GIS completo
