---
schema: foundry-doc-v1
title: "service-extraction — la canalización de ingesta del DataGraph"
slug: service-extraction
short_description: "service-extraction vigila un directorio en busca de cargas útiles JSON entrantes que llevan entidades clasificadas en el borde, escribe un registro de libro mayor por carga útil para el servicio objetivo, y puede puentear el mismo texto hacia la canalización de ingesta del DataGraph."
category: services
type: topic
content_type: topic
quality: complete
index_group: ring-2-knowledge-and-processing
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: service-extraction.md
cites: []
---

`service-extraction` vigila un directorio en busca de cargas útiles JSON entrantes y convierte cada una en un registro duradero de libro mayor. A diferencia de un componente del Anillo 2 que clasifica los datos por sí mismo, consume entidades que ya han sido clasificadas — su carga útil de entrada lleva un campo `edge_entities`, poblado por inferencia de IA local basada en WASM antes de que la carga útil llegue siquiera a este servicio.

## El ciclo de vigilancia y escritura

Ejecutándose como un vigilante del sistema de archivos, el servicio recoge cada archivo JSON nuevo depositado en su directorio de vigilancia, identificado por un `worm_id` derivado del nombre de archivo. Para cada carga útil:

1. Lee las `edge_entities` ya clasificadas y construye un conjunto de entidades listas para el grafo a partir de ellas.
2. Escribe esas entidades en un registro de libro mayor `CRM_<worm_id>.json`, archivado bajo el servicio objetivo nombrado en la propia carga útil — el objetivo no está fijo a un solo servicio posterior, es lo que la carga útil especifique.
3. Si hay configurada una ruta de emisión de corpus, también escribe un segundo archivo separado, `CORPUS_<worm_id>.json`, con el texto en bruto de la carga útil — un archivo puente que [[service-content]] vigila de forma independiente, alimentando ese texto a su propia canalización escalonada de extracción de entidades para el grafo de conocimiento.

Las dos salidas cumplen propósitos distintos: el libro mayor CRM es el registro de entidades estructuradas para el servicio objetivo propio de la carga útil, y el puente CORPUS es lo que permite que el mismo texto también alimente el grafo de conocimiento general de la plataforma, sin que este servicio necesite saber nada sobre cómo ocurre esa extracción más adelante.

## Lo que no hace

Este servicio no ejecuta su propia clasificación de IA — las `edge_entities` que consume llegan ya etiquetadas. No analiza formatos de documentos binarios (PDF, DOCX, XLSX) — eso es una canalización separada y dedicada. Y no mantiene una matriz de enrutamiento de propósito general por tipo de contenido; cada carga útil simplemente nombra su propio servicio objetivo.

## Véase también

- [[service-content]] — vigila los archivos puente CORPUS que emite este servicio y ejecuta su propia extracción escalonada sobre el texto
- [[service-people]] — un servicio objetivo común para los registros de libro mayor CRM que escribe este servicio
- [[service-email]] — una fuente ascendente típica de las cargas útiles JSON que este servicio vigila
