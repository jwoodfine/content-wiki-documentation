---
schema: foundry-doc-v1
title: "service-search — Índice Invertido"
slug: service-search
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: service-search.md
cites: []
---

`service-search` es el servicio de búsqueda de texto completo del Anillo 2, construido sobre la biblioteca Rust Tantivy. Proporciona recuperación en microsegundos en millones de archivos a través de un índice invertido binario estático que no requiere ningún proceso de base de datos activo.

## Línea de base arquitectónica

Un índice invertido funciona construyendo un mapa comprimido de cada palabra del corpus a la lista de documentos que la contienen — análogo al índice al final de un libro de referencia. En el momento de la consulta, el servicio busca los términos de consulta en este mapa y devuelve los documentos coincidentes en microsegundos, independientemente del tamaño del corpus.

## Anillo y función

`service-search` ocupa el **Anillo 2 — Conocimiento y Procesamiento** en la arquitectura de tres anillos. El Anillo 2 es multiinquilino a través del espacio de nombres `moduleId` y opera deterministamente sin inferencia de IA. La función de `service-search` dentro del Anillo 2 es la recuperación: responde consultas contra el corpus indexado y devuelve referencias de documentos clasificadas.

## Propiedades arquitectónicas clave

- **Sin proceso activo requerido para consultas.** El índice está mapeado en memoria en el momento de la consulta; no hay ningún demonio de base de datos que gestionar.
- **Portátil.** El archivo de índice puede copiarse a almacenamiento USB o una máquina diferente y consultarse inmediatamente.
- **Comprimido.** El formato de índice de Tantivy usa codificación block-maximal para datos de frecuencia de términos.
- **Actualizable.** Los nuevos documentos se añaden al índice a través de un proceso de indexación en segundo plano que fusiona nuevos segmentos.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
