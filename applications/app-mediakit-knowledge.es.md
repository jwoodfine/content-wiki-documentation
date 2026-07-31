---
schema: foundry-doc-v1
title: "Aplicación MediaKit Knowledge"
slug: app-mediakit-knowledge
category: applications
type: topic
content_type: topic
quality: complete
short_description: "Motor wiki Rust de binario único que sirve documentation.pointsav.com — una vista sobre un árbol Markdown donde los commits son canónicos y el binario es descartable."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: app-mediakit-knowledge.md
cites:
 - ni-51-102
 - osc-sn-51-721
---

`app-mediakit-knowledge` es el motor wiki Rust de binario único que sirve la documentación de ingeniería de PointSav en `https://documentation.pointsav.com` — una vista sobre un árbol de Markdown, no un repositorio de contenido. Los commits de Markdown son canónicos; cada binario en ejecución es un estado derivado descartable, incluyendo el HTML renderizado, el índice Tantivy y (cuando la edición colaborativa está habilitada) la sala CRDT. El motor combina un servidor HTTP `axum`, un renderizador CommonMark `comrak` con extensiones específicas de la plataforma para wikilinks y notas al pie, un backend de búsqueda de texto completo `tantivy`, y una capa de plantillas `maud` con cuatro plantillas de artículo. La primera implementación pública del motor entró en servicio el 2026-04-27 a las 16:25 UTC.

El motor es una *vista* sobre un árbol de Markdown, no un repositorio de contenido. El árbol de Markdown es canónico; el binario en ejecución es una vista. Esta inversión de la fuente de verdad es la decisión de diseño más importante del sistema.

La primera implementación pública entró en servicio el 2026-04-27 a las 16:25 UTC, sirviendo un árbol de contenido inicial de cuatro archivos en `https://documentation.pointsav.com`. La superficie de rutas completa de las fases de construcción 1, 1.1, 2 y 3 está operativa; las fases 4 a 8 están planificadas pero aún no implementadas.

## La inversión de la fuente de verdad

La decisión de diseño central del sustrato: **git es canónico; el binario en ejecución es una vista; el CRDT, cuando la edición colaborativa está habilitada, es efímero de sesión**.

Todo artefacto concreto con que un lector interactúa — la página HTML, la entrada del feed Atom, el bloque JSON-LD, el resultado de búsqueda — se deriva en tiempo de solicitud del árbol de Markdown en disco. El estado del disco es lo que se confirma, revisa, replica y divulga. El índice Tantivy se reconstruye desde el árbol de contenido al arrancar. El CRDT de colaboración es efímero entre sesiones.

### Inversión del modelo MediaWiki

Esta inversión revierte el modelo tradicional de MediaWiki, donde la base de datos es canónica y el sistema de archivos es una copia de trabajo derivada. El motor elige el sistema de archivos como canónico y la base de datos como copia derivada. La motivación es la simplicidad operacional — una copia de seguridad del árbol de contenido es un `git clone`; una replicación es un `git pull`; una auditoría es un `git log` — y también una invariante a nivel de sustrato: cada afirmación publicada es un commit git firmado; el registro de divulgación es el historial de git; la postura de divulgación continua BCSC queda impuesta por la estructura del sustrato, no sólo por política.

## Superficie de rutas

El motor expone un conjunto acotado de rutas HTTP, cada una independiente y sin estado de sesión ni base de datos propia. Las rutas de la Fase 1 cubren el servidor básico y el renderizado de artículos; la Fase 1.1 añade el cromo Wikipedia; la Fase 2 introduce el editor CodeMirror 6 y el relé WebSocket para colaboración; la Fase 3 incluye búsqueda Tantivy, feeds de sindicación Atom y JSON Feed, sitemap, y el endpoint `/git/{slug}` para ingesta de markdown crudo. Las fases 4 a 8 están planificadas.

## Cromo de memoria muscular Wikipedia

El motor incluye un cromo deliberadamente reconocible para los lectores de Wikipedia. Los elementos preservados incluyen pestañas Artículo/Discusión, pestañas Leer/Editar/Ver historial, lápices de edición por sección, ordenación final del artículo (Referencias, Véase también, Categorías), notas hatnote, convención de primera oración en negrita, índice de contenidos plegable en el margen izquierdo, y selector de idioma.

Los añadidos más allá de Wikipedia incluyen insignias de citas junto a referencias `[citation-id]`, un banner de información prospectiva cuando el frontmatter del artículo establece `forward_looking: true`, y una banda de encabezado IVC de verificación (Phase 7 está planificada para añadir la maquinaria de verificación real).

## Superficie del editor

El editor de la wiki es una instancia de CodeMirror 6 empaquetada en el binario, servida en `/edit/{slug}`. Admite resaltado de sintaxis Markdown con numeración de línea, ajuste de línea configurable e historial de deshacer/rehacer, con escritura atómica en disco a través de `POST /edit/{slug}`.

### Funciones de edición conscientes del sustrato

Tres funciones distinguen la implementación:

**Linter en tiempo real (Fase 2, Paso 4).** Siete reglas deterministas señalan problemas editoriales mientras se escribe, cada una con una autoridad citada en una tarjeta emergente. Las reglas cubren vocabulario prohibido, formulaciones prospectivas sin el banner cautelar correspondiente, verificaciones de disciplina BCSC y verificaciones de registro institucional. Las reglas son deterministas en el momento de edición; se prevé que la decodificación restringida estructurada en tiempo de inferencia endurezca estas reglas hasta convertirlas en garantías equivalentes a tiempo de compilación una vez que el Doorman de service-slm incorpore la integración de restricciones gramaticales.

**Autocompletado de citas (Fase 2, Paso 5).** Al pulsar `[` se activa un autocompletado que consulta el registro de citas del espacio de trabajo. El colaborador escribe `[ni-51` y la lista se reduce a `ni-51-102` (divulgación continua BCSC) más cualquier otra coincidencia. Seleccionar una entrada inserta la forma canónica `[citation-id]` y añade la cita a la lista `cites:` del frontmatter del artículo automáticamente.

**Escalera de tres teclas para el Doorman (Fase 2, Paso 6 — stubs).** Tab abre una escalera de funciones "preguntar al Doorman" en la posición del cursor — buscar una cita, sugerir un objetivo de hatnote, generar un enlace de desambiguación, proponer un encabezado de sección. Estas devuelven stubs 501 en el binario v0.1.29; la Fase 4 está planificada para conectarlas al Doorman de service-slm.

### Semántica de escritura atómica

La semántica de escritura atómica del editor es conservadora: el motor escribe el contenido nuevo del archivo en una ruta temporal dentro del mismo directorio, ejecuta fsync y renombra sobre el destino. Una escritura fallida es visible para el colaborador y deja el contenido canónico intacto. Las ediciones concurrentes desde dos sesiones no colaborativas compiten en el paso de renombrado; la convención documentada es que gana la última escritura.

## Búsqueda, feeds e ingesta

El motor indexa el árbol de contenido al arrancar y de forma incremental en cada edición. El índice es Tantivy en disco (BM25 por defecto) en `<state-dir>/search/`, reconstruido desde el árbol de contenido si falta. El `IndexWriter` de Tantivy se mantiene en un `Arc<Mutex<>>` siguiendo el patrón habitual del crate, y se libera antes de recargar el lector para evitar la condición de carrera de recarga asíncrona.

### Sindicación y descubrimiento por rastreadores

Tres formatos de sindicación presentan el corpus a los rastreadores:

- **`/feed.atom`** — sindicación Atom RFC 4287. Cada artículo es una entrada del feed con `title`, `summary`, `published`, `updated` y la lista `cites:` del artículo resuelta contra el registro.
- **`/feed.json`** — sindicación JSON Feed 1.1. Mismo contenido que el feed Atom; solo difiere el formato.
- **`/sitemap.xml`** — conforme a sitemaps.org. Enumera cada URL de artículo con su fecha de última modificación.

Dos archivos de descubrimiento para rastreadores completan la superficie: **`/robots.txt`** y **`/llms.txt`**. La ruta `/git/{slug}` sirve el código fuente Markdown crudo. Un rastreador o un futuro par de federación puede ingerir el árbol de contenido siguiendo `/llms.txt` para descubrir la lista de artículos y luego consultando `/git/{slug}` para cada fuente de artículo. La ruta acepta un sufijo `.md` opcional para las herramientas que esperan que las URL de Markdown terminen en `.md`.

## Colaboración en tiempo real

El motor admite opcionalmente la edición colaborativa en tiempo real mediante el CRDT Yjs. La función está desactivada por defecto tras el indicador de línea de comandos `--enable-collab`; el despliegue de producción en v0.1.29 no la activa.

### Relé de paso, no un servidor Yjs

La implementación sigue la inversión de la fuente de verdad: **el servidor es un relé WebSocket de paso, no un servidor Yjs**. El estado del documento Yjs nunca reside en el servidor. El relé es una sala `tokio::sync::broadcast` ligera por slug con un búfer de rezago de 256 mensajes; los clientes envían paquetes de actualización Yjs, el servidor los reenvía a los demás clientes de la sala, y la persistencia fluye a través de la ruta de guardado existente `POST /edit/{slug}` en un guardado deliberado. Cuando todos los clientes abandonan la sala, esta se cierra y cualquier estado CRDT sin guardar se descarta.

Un documento Yjs de larga duración en el servidor crearía un registro canónico paralelo que se desviaría de git, complicaría la auditoría y entraría en conflicto con la postura de divulgación BCSC. El relé de paso mantiene a git como canónico y al CRDT como efímero de sesión.

### Paquete de cliente de carga diferida

El cliente carga de forma diferida `cm-collab.bundle.js` (302 KB) solo cuando la plantilla establece el indicador `window.WIKI_COLLAB_ENABLED` desde el servidor, de modo que los despliegues de producción sin `--enable-collab` nunca cargan JavaScript de Yjs. Una prueba manual de humo con dos clientes (dos navegadores editando el mismo artículo, viendo los cursores del otro) es la vía de homologación actual para la experiencia visual de renderizado de cursores — una propiedad incómoda de verificar mediante programación.

## Federación de contenido

El motor está planificado para servir contenido desde múltiples repositorios git a través de una única superficie renderizada, mediante un manifiesto declarativo de montaje (`knowledge.toml`) que el operador coloca en la raíz del directorio de contenido. Cada entrada de montaje nombra un repositorio fuente, una ruta de montaje local y un plano — el esquema que determina cómo se validan, enrutan y enlazan los archivos en ese montaje. Esta capacidad está planificada; la arquitectura descrita aquí es el diseño previsto, y el modelo de repositorio único es la forma actualmente desplegada.

### Montajes y esquemas de plano

Los montajes son subárboles de directorio derivados de repositorios git nombrados. Los planos son esquemas nombrados que restringen el contenido que puede contener un montaje y determinan el patrón de URL que ocupa. Dos planos son integrados: `topic` (el artículo wiki estándar) y `guide` (documentos operacionales, renderizados con un cromo diferenciado y excluidos del índice de artículos principal). Los operadores podrán registrar planos adicionales — `regional-market`, `adr`, `changelog` y esquemas especializados similares — como complementos cuando la Fase 6 esté disponible.

### Aislamiento por instancia y procedencia

Cada instancia wiki lee sólo los montajes que declara su propio `knowledge.toml`. La configuración de montaje es por instancia, no estado de registro global. Cada artículo renderizado desde un montaje declarativo lleva metadatos de procedencia que identifican el repositorio fuente y la ruta, con enrutamiento de edición de vuelta al repositorio fuente canónico — manteniendo intacta la inversión de la fuente de verdad en toda la superficie federada.

La Fase 6 está planificada para entregar la especificación del esquema `knowledge.toml` y la API de plugin de planos. La Fase 7 está planificada para la recuperación con direccionamiento por contenido y la federación anclada en `blake3`. Véase [[federation-via-content-mounts]] para el patrón en profundidad.

## Inventario de inventos

`INVENTIONS.md` en la raíz del crate cataloga ocho inventos específicos del motor (conteo a la fecha de v0.1.29): inversión de la fuente de verdad, compatibilidad nativa del sustrato, Autor Constitucionalmente Restringido (CCA), Cita de Verificabilidad de Información (IVC, planificado Fase 7), Prestaciones Autorizadas por el Sustrato (SAA), esquema de URL `verify://` (planificado Fase 7), el relé WebSocket de paso, y el conjunto de superficie API nativa del sustrato.

## Trayectoria de fases de construcción

A fecha de 2026-04-27, el motor está al final de la Fase 3. Las Fases 1, 1.1, 2 y 3 están implementadas. Las Fases 4 a 8 están *planificadas*; aplica lenguaje cautelar conforme a [ni-51-102] y [osc-sn-51-721]. Los cambios materiales al plan de construcción se registran en los documentos de planificación de fase y en el `CHANGELOG.md` del espacio de trabajo.

## Véase también

- [[source-of-truth-inversion]] — el patrón canónico / vista / efímero generalizado
- [[substrate-native-compatibility]] — la decisión de eliminar el shim de la Action API
- [[collab-via-passthrough-relay]] — la implementación del relé WebSocket
- [[wikipedia-leapfrog-design]] — la filosofía de diseño de memoria muscular y margen leapfrog del 95%/5%
- [[knowledge-wiki-home-page-design]] — la intención de diseño de la página de inicio y la estructura de espacios
- [[deploy-knowledge-instance]] — guía paso a paso: compilar e iniciar app-mediakit-knowledge apuntando a un repositorio de contenido local
- [[use-knowledge-mounts]] — guía paso a paso: añadir un repositorio de contenido secundario mediante montajes declarativos en knowledge.toml
