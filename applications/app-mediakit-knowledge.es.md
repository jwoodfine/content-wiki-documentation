---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
companion: topic-app-mediakit-knowledge.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

`app-mediakit-knowledge` es el motor wiki que sirve la documentación de ingeniería de PointSav en `https://documentation.pointsav.com`. El motor es un servicio Rust de binario único compuesto por un servidor HTTP `axum`, un renderizador CommonMark `comrak` con extensiones específicas para wikilinks y notas al pie, un backend de búsqueda de texto completo `tantivy`, y una capa de plantillas `maud` que incluye cuatro plantillas de artículo. El motor lee archivos Markdown de un directorio de contenido que el operador designa al arrancar, los renderiza en HTML bajo demanda, y los devuelve con cabeceras de caché adecuadas para una audiencia de documentación.

El motor es una *vista* sobre un árbol de Markdown, no un repositorio de contenido. El árbol de Markdown es canónico; el binario en ejecución es una vista. Esta inversión de la fuente de verdad es la decisión de diseño más importante del sistema.

La primera implementación pública entró en servicio el 2026-04-27 a las 16:25 UTC, sirviendo un árbol de contenido inicial de cuatro archivos en `https://documentation.pointsav.com`. La superficie de rutas completa de las fases de construcción 1, 1.1, 2 y 3 está operativa; las fases 4 a 8 están planificadas pero aún no implementadas.

## La inversión de la fuente de verdad

La decisión de diseño central del sustrato: **git es canónico; el binario en ejecución es una vista; el CRDT, cuando la edición colaborativa está habilitada, es efímero de sesión**.

Todo artefacto concreto con que un lector interactúa — la página HTML, la entrada del feed Atom, el bloque JSON-LD, el resultado de búsqueda — se deriva en tiempo de solicitud del árbol de Markdown en disco. El estado del disco es lo que se confirma, revisa, replica y divulga. El índice Tantivy se reconstruye desde el árbol de contenido al arrancar. El CRDT de colaboración es efímero entre sesiones.

Esta inversión revierte el modelo tradicional de MediaWiki, donde la base de datos es canónica y el sistema de archivos es una copia de trabajo derivada. El motor elige el sistema de archivos como canónico y la base de datos como copia derivada. La motivación es la simplicidad operacional — una copia de seguridad del árbol de contenido es un `git clone`; una replicación es un `git pull`; una auditoría es un `git log` — y también una invariante a nivel de sustrato: cada afirmación publicada es un commit git firmado; el registro de divulgación es el historial de git; la postura de divulgación continua BCSC queda impuesta por la estructura del sustrato, no sólo por política.

## Superficie de rutas

El motor expone un conjunto acotado de rutas HTTP, cada una independiente y sin estado de sesión ni base de datos propia. Las rutas de la Fase 1 cubren el servidor básico y el renderizado de artículos; la Fase 1.1 añade el cromo Wikipedia; la Fase 2 introduce el editor CodeMirror 6 y el relé WebSocket para colaboración; la Fase 3 incluye búsqueda Tantivy, feeds de sindicación Atom y JSON Feed, sitemap, y el endpoint `/git/{slug}` para ingesta de markdown crudo. Las fases 4 a 8 están planificadas.

## Cromo de memoria muscular Wikipedia

El motor incluye un cromo deliberadamente reconocible para los lectores de Wikipedia. Los elementos preservados incluyen pestañas Artículo/Discusión, pestañas Leer/Editar/Ver historial, lápices de edición por sección, ordenación final del artículo (Referencias, Véase también, Categorías), notas hatnote, convención de primera oración en negrita, índice de contenidos plegable en el margen izquierdo, y selector de idioma.

Los añadidos más allá de Wikipedia incluyen insignias de citas junto a referencias `[citation-id]`, un banner de información prospectiva cuando el frontmatter del artículo establece `forward_looking: true`, y una banda de encabezado IVC de verificación (Phase 7 está planificada para añadir la maquinaria de verificación real).

## Inventario de inventos

`INVENTIONS.md` en la raíz del crate cataloga ocho inventos específicos del motor (conteo a la fecha de v0.1.29): inversión de la fuente de verdad, compatibilidad nativa del sustrato (Doctrine claim #29), Autor Constitucionalmente Restringido (CCA, Doctrine claim #31), Cita de Verificabilidad de Información (IVC, planificado Fase 7), Prestaciones Autorizadas por el Sustrato (SAA), esquema de URL `verify://` (planificado Fase 7), el relé WebSocket de paso, y el conjunto de superficie API nativa del sustrato.

## Trayectoria de fases de construcción

A fecha de 2026-04-27, el motor está al final de la Fase 3. Las Fases 1, 1.1, 2 y 3 están implementadas. Las Fases 4 a 8 están *planificadas*; aplica lenguaje cautelar conforme a [ni-51-102] y [osc-sn-51-721]. Los cambios materiales al plan de construcción se registran en los documentos de planificación de fase y en el `CHANGELOG.md` del espacio de trabajo.

## Véase también

- [[source-of-truth-inversion]] — el patrón canónico / vista / efímero generalizado
- [[substrate-native-compatibility]] — la decisión de eliminar el shim de la Action API
- [[collab-via-passthrough-relay]] — la implementación del relé WebSocket
- [[wikipedia-leapfrog-design]] — intención de diseño del cromo y el contrato 95%/5%
- [[documentation-pointsav-com-launch-2026-04-27]] — la narrativa del lanzamiento público v0.1.29

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
