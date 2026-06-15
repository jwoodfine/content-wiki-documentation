---
schema: foundry-doc-v1
title: "Cómo exportar datos estructurados de la plataforma"
slug: export-structured-data
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: export-structured-data.md
---

La plataforma almacena datos en múltiples capas — tiles del libro mayor en bruto, registros de entidades en el DataGraph, contenido wiki y conjuntos de datos de inteligencia de ubicación. Exportar esos datos significa elegir la capa correcta para su caso de uso y el formato de exportación apropiado. Esta guía cubre las cuatro rutas principales de exportación y cuándo usar cada una.

Para el modelo de datos por capas, véase [[service-content]]. Para el almacenamiento del libro mayor subyacente, véase [[service-fs-architecture]].

## Requisitos previos

- Un dispositivo emparejado con acceso de nivel apropiado (INPUT para el libro mayor; USER para exportaciones de solo lectura)
- Una sesión Totebox activa (véase [[open-first-totebox-session]])
- Conocimiento de qué capa de datos está consultando

## Ruta de exportación 1: Datos de entidad del DataGraph

Use esta ruta cuando necesite registros estructurados sobre personas, organizaciones, proyectos o servicios.

Llame a `query_datagraph` para identificar la entidad, luego llame a `get_entity_context` para recuperar el perfil completo. El objeto JSON devuelto es el registro de entidad autorizado. Cópielo o envíelo a su sistema de destino.

Para exportaciones masivas, la API de `service-fs` proporciona una operación `read_since` que devuelve registros vinculados a entidades del libro mayor en orden cronológico.

## Ruta de exportación 2: Artículos wiki como Markdown

Use esta ruta cuando necesite contenido de artículos para publicación posterior, procesamiento o indexación.

Los artículos wiki son archivos Markdown planos con frontmatter YAML, almacenados en los repositorios git `media-knowledge-*`. Expórtelos leyendo los archivos directamente, o usando el endpoint de exportación de la instancia de conocimiento si está configurado:

```
GET /export/<categoría>/<slug>
Accept: text/markdown
```

La respuesta es el archivo Markdown crudo incluyendo frontmatter. No se requiere autenticación para contenido marcado como `audience: vendor-public`.

## Ruta de exportación 3: Conjuntos de datos de inteligencia de ubicación como GeoJSON

Use esta ruta cuando necesite datos espaciales de clusters o arquetipos para aplicaciones GIS.

La puerta de enlace GIS sirve archivos GeoJSON preconstruidos en:

```
GET /data/archetype-<nombre>.geojson
```

Donde `<nombre>` es uno de: `vwh` (Almacén Vertical), `pks` (Estructuras de Estacionamiento), o el archivo principal de clusters. Estos archivos incluyen clasificaciones de nivel, campos de señal de co-localización y atributos de enriquecimiento.

Para el esquema de datos y definiciones de campos, véase [[pointsav-gis-engine]].

## Ruta de exportación 4: Tiles del libro mayor para auditoría

Use esta ruta cuando necesite registros con evidencia de manipulación para cumplimiento, descubrimiento legal o auditoría por terceros.

Use la CLI `service-fs verify` o la API `read_since` para exportar C2SP tlog-tiles:

```
service-fs export --from <checkpoint-id> --format tlog-tiles --out <archivo-salida>
```

El archivo resultante es texto plano, verificable con una utilidad SHA-256 y legible sin herramientas de PointSav. Véase [[verify-worm-ledger]] para el procedimiento de verificación.

## Elegir la ruta correcta

| Lo que necesita | Use la ruta de exportación |
|---|---|
| Información sobre una entidad nombrada (persona, proyecto, servicio) | 1 — DataGraph |
| Contenido de artículo para publicación o indexación | 2 — Markdown wiki |
| Datos espaciales de clusters para una aplicación de mapa | 3 — GeoJSON |
| Registros con evidencia de manipulación para cumplimiento o auditoría | 4 — Tiles del libro mayor |

## Puntos clave

- El DataGraph es la ruta correcta para datos de entidades nombradas — contiene registros verificados y actuales
- Las exportaciones de Markdown wiki incluyen frontmatter; elimínelo o procéselo antes de enviarlo a consumidores de destino que esperan prosa plana
- Los archivos GeoJSON están preconstruidos y se sirven estáticamente; se actualizan cuando se ejecuta la reconstrucción nocturna
- Las exportaciones de tiles del libro mayor son autoverificables con una utilidad SHA-256; no se necesita servicio activo después de la exportación

## Véase también

- [[service-content]] — el Motor de Gravedad y el modelo de datos de cinco capas
- [[service-fs-architecture]] — el libro mayor WORM que almacena la capa de registros en bruto
- [[verify-worm-ledger]] — cómo verificar la integridad de un tile del libro mayor exportado
- [[pointsav-gis-engine]] — el motor GIS y su esquema de datos
- [[query-the-datagraph]] — cómo buscar datos de entidades antes de exportar
