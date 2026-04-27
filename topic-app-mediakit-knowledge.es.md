---
schema: foundry-doc-v1
document_version: 0.1.0
title: "app-mediakit-knowledge — el motor de wiki (resumen)"
slug: topic-app-mediakit-knowledge
category: applications
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
lang: es
paired_with: topic-app-mediakit-knowledge.md
cites:
  - ni-51-102
  - osc-sn-51-721
  - constitutional-ai-2212-08073
  - mcp-spec
  - mediawiki-action-api
  - mediawiki-xml-dump
---

## Visión general

`app-mediakit-knowledge` es el motor de wiki que sirve la documentación técnica de PointSav en `https://documentation.pointsav.com`. Se trata de un servicio de un único binario escrito en Rust que combina un servidor HTTP, un renderizador CommonMark, un índice de búsqueda de texto completo y una capa de plantillas. El sistema entró en producción el 27 de abril de 2026.

## Inversión de la fuente de verdad

El principio central del diseño es que **git es la fuente de verdad; el binario en ejecución es una vista; el CRDT colaborativo es efímero por sesión**.

Todo lo que un lector ve —la página HTML, las entradas del feed Atom, los bloques JSON-LD, los resultados de búsqueda— se genera en el momento de la solicitud a partir del árbol de archivos markdown en disco. Esos archivos son los que se confirman (*commit*), se revisan, se replican y se divulgan. El HTML es desechable.

Este enfoque invierte el modelo tradicional de MediaWiki, donde la base de datos es canónica y el sistema de archivos es una copia derivada. Aquí el sistema de archivos es canónico: una copia de seguridad es un `git clone`; una réplica es un `git pull`; una auditoría es un `git log`. La postura de divulgación continua que exige la normativa canadiense de valores `[ni-51-102]` queda reforzada por la estructura del substrato, no solo por política interna.

## Compatibilidad con el ecosistema existente

El motor conserva las convenciones de URL de MediaWiki (`/wiki/{slug}`), la sintaxis de wikilinks (`[[slug]]`) y la posibilidad de importar volcados XML de MediaWiki para migraciones puntuales. Lo que no se reproduce es la Action API de MediaWiki `[mediawiki-action-api]`, las plantillas del parser ni el ecosistema de bots de pywikibot. En su lugar, el motor ofrece una superficie de API propia y coherente con el substrato: HTML de artículo, JSON-LD, feeds Atom y JSON, mapa del sitio, descubrimiento para rastreadores de LLM y fuente markdown sin procesar.

## Chrome reconocible (Wikipedia)

El motor incorpora deliberadamente los patrones visuales de Wikipedia —pestañas de Artículo / Discusión, pestañas de Leer / Editar / Historial, lápices de edición por sección, tabla de contenidos colapsable en la barra lateral, convención de primera oración en negrita, cambio de idioma (actualmente inglés / español)— para que cualquier lector familiarizado con Wikipedia pueda navegar el motor sin instrucciones adicionales.

Se añaden elementos propios del substrato: distintivos de citas junto a cada referencia `[citation-id]`, un banner de información prospectiva cuando el artículo lo requiere, y un campo de clase de divulgación visible en el JSON-LD.

## Superficie del editor y linting

El editor en navegador usa CodeMirror 6. Incluye siete reglas de linting deterministas que señalan problemas editoriales en tiempo de escritura: vocabulario prohibido, afirmaciones prospectivas sin el encuadre cautelar exigido `[ni-51-102]` `[osc-sn-51-721]`, y verificaciones de la postura de divulgación del substrato. La integración con el Doorman de service-slm —que endurecería estas reglas en restricciones equivalentes a tiempo de compilación `[constitutional-ai-2212-08073]`— está prevista para fases posteriores.

## Trayectoria de construcción

Las fases 1, 1.1, 2 y 3 están operativas. Las fases 4 a 8 son trabajo planificado; se aplica el encuadre cautelar correspondiente `[ni-51-102]` `[osc-sn-51-721]`. La Fase 4 añadirá historial de ediciones, gráfico de backlinks, servidor MCP `[mcp-spec]` para clientes de agentes, y un remoto Git de solo lectura sobre HTTP. Las Fases 5 a 8 cubren imágenes, adaptación multicliente, federación con direccionamiento por contenido y el linter de clases de divulgación que se pretende formalice las invariantes del substrato.

El catálogo de invenciones del proyecto enumera ocho diseños distintivos, desde la inversión de la fuente de verdad hasta la superficie de API nativa del substrato. La documentación detallada en inglés está disponible en el artículo principal.
