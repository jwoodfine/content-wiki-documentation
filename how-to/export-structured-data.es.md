---
schema: foundry-doc-v1
title: "Exportar datos estructurados de la plataforma"
slug: export-structured-data
short_description: "Exporta datos de la plataforma por tres rutas reales — registros de entidades del DataGraph a través de herramientas MCP, Markdown wiki leído directamente de git, y entradas de libro mayor paginadas a través de la API HTTP de service-fs."
category: how-to
index_group: records-storage
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: export-structured-data.md
---

## Requisitos previos

- Acceso a las herramientas MCP del DataGraph, para exportaciones de entidades
- Acceso de lectura al repositorio git `media-knowledge-*` correspondiente, para exportaciones wiki
- Acceso de red a `service-fs` y su identificador de módulo, para exportaciones del libro mayor
- Un dispositivo emparejado con el espacio de trabajo (véase [[pair-a-new-device]])

## Propósito

Elija la ruta de exportación correcta para lo que realmente busca obtener de la plataforma — registros de entidades, contenido de artículos o historial del libro mayor con grado de auditoría tienen cada uno un mecanismo real genuinamente distinto.

## Procedimiento

### Ruta 1: Datos de entidades del DataGraph

Use esto para registros estructurados sobre una persona, organización, proyecto o servicio.

1. Llame a `query_datagraph` para identificar la entidad, luego a `get_entity_context` sobre su identificador para obtener el perfil completo — véase [[query-the-datagraph]] para las firmas exactas de las herramientas.
2. El objeto devuelto es el registro de entidad autoritativo. Cópielo o canalícelo a su destino.

No existe una operación de exportación masiva separada para datos de entidades más allá de llamadas repetidas a `get_entity_context` — trátela como una interfaz de búsqueda, no como una herramienta de volcado masivo.

### Ruta 2: Artículos wiki como Markdown

Use esto para contenido de artículos que necesita para publicación, procesamiento o indexación posteriores.

Los artículos wiki son archivos Markdown planos con frontmatter YAML, almacenados directamente en los repositorios git `media-knowledge-*`. Léalos o expórtelos de la misma manera que exportaría cualquier archivo de un repositorio git — clone o actualice el repositorio correspondiente y lea los archivos que necesita directamente. No existe un endpoint HTTP de exportación separado; el propio repositorio git es la superficie de exportación.

### Ruta 3: Entradas del libro mayor para auditoría

Use esto para registros a prueba de manipulación para cumplimiento, descubrimiento legal o auditoría de terceros.

Pagine a través de `GET /v1/entries?since=<cursor>` contra su instancia de `service-fs` hasta que la respuesta esté vacía, luego obtenga `GET /v1/checkpoint` para anclar lo que exportó a un `tree_size`/`root_hash` específico. Véase [[read-the-command-ledger]] para el procedimiento completo y [[verify-worm-ledger]] para confirmar que lo que exportó no ha sido alterado. Tanto las entradas exportadas como el punto de control son JSON plano, verificable con una utilidad SHA-256 estándar — no se requiere ninguna herramienta propietaria.

## Elegir la ruta correcta

| Lo que necesita | Use la ruta |
|---|---|
| Información sobre una entidad nombrada (persona, proyecto, servicio) | 1 — DataGraph |
| Contenido de artículos para publicación o indexación | 2 — Markdown wiki |
| Registros a prueba de manipulación para cumplimiento o auditoría | 3 — Entradas del libro mayor |

> **Nota:** si busca una ruta de exportación espacial/GIS (clústeres de co-ubicación, datos de arquetipos), eso es un sistema separado que esta guía no cubre — consulte la documentación específica de GIS de su despliegue en lugar de asumir que las rutas genéricas anteriores se aplican ahí.

## Resultado esperado

Los datos que necesita, exportados a través de la ruta que realmente coincide con cómo los almacena la plataforma — no un endpoint de exportación unificado fabricado que no existe.

## Verificación

Para datos de entidades, confirme que la actualidad del perfil devuelto coincide con su expectativa (véase [[query-the-datagraph]]). Para contenido wiki, confirme que el bloque de frontmatter se analiza correctamente y que el `slug` coincide con lo que esperaba exportar. Para entradas del libro mayor, verifique que el `tree_size` del punto de control cubre cada cursor que exportó.

## Reversión

Las tres rutas son de solo lectura. Nada que deshacer.

## Próximos pasos

- [[query-the-datagraph]] — el procedimiento completo de búsqueda de entidades
- [[read-the-command-ledger]] — el procedimiento completo de lectura del libro mayor
- [[verify-worm-ledger]] — confirme que las entradas del libro mayor exportadas no han sido alteradas

## Véase también

- [[service-content]] — el servicio que mantiene el DataGraph
- [[service-fs]] — el libro mayor WORM del que provienen estas entradas
