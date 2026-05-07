---
schema: foundry-doc-v1
title: "Arquitectura Leapfrog del Wiki de Conocimiento"
slug: knowledge-wiki-leapfrog-architecture.es
category: architecture
type: topic
quality: core
status: active
language: es
bcsc_class: public-disclosure-safe
last_edited: 2026-05-07
editor: pointsav-engineering
cites: []
paired_with: knowledge-wiki-leapfrog-architecture.md
---

## Resumen estratégico

`app-mediakit-knowledge` es el motor del wiki de conocimiento de PointSav: un binario Rust que sirve tres instancias wiki — `documentation.pointsav.com`, `projects.woodfinegroup.com` y `corporate.woodfinegroup.com` — desde archivos Markdown almacenados en repositorios git. El motor renderiza contenido con la interfaz visual de Wikipedia: tabla de contenidos adherente, resolución de wikilinks con señalización de enlaces rojos, páginas de categoría, historial de edición y búsqueda de texto completo.

En mayo de 2026, el motor implementa aproximadamente el 78 % de la experiencia visual y funcional de Wikipedia. Una hoja de ruta de varios sprints prevé llevar esa cifra a aproximadamente el 95 %, tras lo cual se añade una capa diferenciadora de Leapfrog 2030 que va más allá de lo que ofrece Wikipedia.

## Por qué no se porta MediaWiki

MediaWiki fue diseñado en 2003 para un stack PHP y MySQL. Su parser — el componente que convierte el formato wikitext en HTML — fue descrito por su autor original como "un gran montón de expresiones regulares." El proyecto Parsoid, el intento de MediaWiki de reemplazar ese parser con un convertidor bidireccional HTML↔wikitext, tardó diez años en desplegarse y aún completaba su adopción en 2025.

El sistema de plantillas de MediaWiki acopla el parser a la base de datos, complica el caching y hace difícil operar el sistema sin MySQL. El objetivo arquitectónico de `app-mediakit-knowledge` es lograr la misma experiencia lectora mediante una pila radicalmente diferente: Markdown con frontmatter YAML en lugar de wikitext; git como registro de versiones; Tantivy (embebido, sin carga operativa) en lugar de Elasticsearch; y tipos de bloque nativos en lugar de expansión de macros recursiva.

## Tipos de bloque nativos

En lugar de implementar un motor de expansión de macros wikitext, `app-mediakit-knowledge` está diseñado para usar bloques de código cercados que el AST de comrak reconoce y convierte a HTML estructurado. Los principales tipos previstos son:

- **Infobox** — tabla resumen de columna derecha (el elemento más reconocible de Wikipedia) definida como bloque YAML cercado que el motor convierte en `<table class="infobox">`.
- **Navbox** — tabla de navegación colapsable en la parte inferior del artículo, que agrupa enlaces a artículos relacionados bajo un título común.
- **Citas con tooltip** — la sintaxis de notas al pie de comrak (`[^id]`) ya parsea correctamente; el trabajo pendiente es el CSS de estilo `[1][2][3]` y el tooltip JavaScript de vista previa en hover.

La implementación de los tipos infobox y navbox requiere, como paso planificado, actualizar comrak de la versión 0.29 a la 0.52, que incorpora la extensión `block_directive`.

## Capa Leapfrog 2030

Una vez alcanzada la paridad con Wikipedia, se prevé añadir tres primitivas de diferenciación planificadas:

**Cinta de autoridad de citas** — indicador visual planificado del estado de verificación de las fuentes citadas, por artículo y eventualmente por afirmación. Las citas resueltas contra `citations.yaml` están previstas para mostrar una cinta de color: verde para verificadas, ámbar para no verificadas, rojo para impugnadas. Wikipedia trata todas las citas como igualmente fiables sin distinción.

**Pie de trayectoria de investigación** — cada artículo declara cinco campos de frontmatter (método, profundidad, confianza, fecha, limitaciones) previstos para renderizarse como una sección plegable que hace visible la procedencia de cada afirmación, apoyando las obligaciones de divulgación continua bajo NI 51-102.

**Editor con integración de IA** — el editor CodeMirror 6 incluye un acceso directo de tres teclas planificado para llamar a `app-orchestration-command` vía el proxy Doorman. Actualmente son endpoints 501 en espera de la operacionalización de service-slm.

## Véase también

- [[app-mediakit-knowledge]] — descripción de la aplicación, configuración de despliegue y hoja de ruta por fases
- [[leapfrog-2030-architecture]] — doctrina Leapfrog 2030 y ocho inventos del marco
- [[wikipedia-structure]] — investigación sobre la anatomía de los artículos de Wikipedia: 16 elementos y esquemas de infobox
- [[compounding-substrate]] — el patrón de compounding que implementa el pilar wiki
