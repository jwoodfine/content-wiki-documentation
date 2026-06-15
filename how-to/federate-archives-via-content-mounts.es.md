---
schema: foundry-doc-v1
title: "Cómo federar archivos mediante montajes de contenido"
slug: federate-archives-via-content-mounts
category: how-to
content_type: how-to
type: how-to
status: stub
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: federate-archives-via-content-mounts.md
---

Los montajes de contenido permiten que una instancia de conocimiento lea el contenido de artículos de la ruta local de una segunda instancia sin copiar archivos. La instancia lectora renderiza el contenido montado como si fuera nativo, con los wikilinks resolviéndose dentro de su gráfico de origen. Esta guía cubre la declaración de un montaje secundario en `knowledge.toml`, la verificación de que el montaje está activo y el acceso a artículos desde la fuente federada.

Para la arquitectura de federación, consulta [[federation-via-content-mounts]]. Para el motor de conocimiento que procesa las declaraciones de montaje, consulta [[app-mediakit-knowledge]].

## Véase también

- [[federation-via-content-mounts]] — la arquitectura de federación declarativa y el modelo de montaje
- [[app-mediakit-knowledge]] — el motor wiki que procesa las declaraciones de montaje de `knowledge.toml`
- [[build-a-colocation-map]] — consume datos de inteligencia de ubicación expuestos a través de un montaje
- [[self-host-a-deployment]] — provisiona la instancia que servirá el contenido federado
