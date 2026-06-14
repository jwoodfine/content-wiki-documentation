---
schema: foundry-doc-v1
title: "Reconstrucción nocturna del grafo de datos"
slug: nightly-datagraph-rebuild.es
category: substrate
type: concept
content_type: topic
status: stub
short_description: "El proceso programado que reconstruye el grafo de conocimiento de la plataforma a partir de fuentes canónicas de archivos planos cada noche, produciendo un substrato consultable desde entradas deterministas sin intervención de inteligencia artificial."
bcsc_class: public-disclosure-safe
lang: es
last_edited: 2026-05-18
editor: pointsav-engineering
paired_with: nightly-datagraph-rebuild.md
---

La reconstrucción nocturna del grafo de datos es el proceso programado que reconstruye el [[knowledge-graph-grounded-apprenticeship|grafo de conocimiento]] completo de la plataforma a partir de sus fuentes canónicas de archivos planos. Todas las relaciones consultables en el grafo — enlaces de entidades, [[service-extraction|resultados de extracción]], [[worm-ledger-architecture|entradas del libro de registros]] e índices de [[location-intelligence-substrate|inteligencia de ubicación]] — se derivan de las mismas entradas deterministas en cada ciclo.

## Propósito

El patrón de reconstrucción garantiza que el substrato consultable refleje el estado comprometido del registro canónico, no la deriva acumulada en memoria. Cualquier ejecución individual puede replicarse a partir de los archivos planos archivados.

El proceso se ejecuta sin inferencia de inteligencia artificial. Las relaciones se calculan mediante reglas de extracción deterministas y uniones basadas en esquemas, no mediante clasificación probabilística.

## Posición en la pila de substratos

La reconstrucción nocturna se sitúa entre el [[worm-ledger-design|libro de registros WORM]] (que acumula escrituras de solo adición durante el día) y el nivel de consulta (que lee el grafo completado más recientemente). Los consumidores del grafo de conocimiento siempre leen una instantánea estable, no un grafo parcialmente construido.

## Véase también

- [[compounding-substrate]] — el mecanismo por el cual cada ciclo de reconstrucción acumula el conocimiento anterior
- [[worm-ledger-design]] — el libro de registros de solo adición que alimenta el proceso de reconstrucción
- [[service-extraction]] — el servicio de extracción que produce los registros de entidades consumidos por la reconstrucción
