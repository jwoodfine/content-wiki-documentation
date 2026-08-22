---
schema: foundry-doc-v1
title: "Aplicación MediaKit Knowledge"
slug: app-mediakit-knowledge
category: applications
type: topic
content_type: topic
quality: complete
index_group: knowledge-and-editorial-applications
short_description: "Motor wiki Rust de binario único que sirve documentation.pointsav.com — una vista sobre un árbol Markdown donde los commits son canónicos y el binario es descartable."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: app-mediakit-knowledge.md
cites: []
references:
  - id: 1
    text: "CommonMark Specification."
    url: "https://commonmark.org/"
  - id: 2
    text: "comrak — CommonMark-compliant Markdown processor in Rust."
    url: "https://github.com/kivikakk/comrak"
  - id: 3
    text: "Tantivy full-text search engine."
    url: "https://www.tantivy-search.org/"
  - id: 4
    text: "Schema.org TechArticle schema."
    url: "https://schema.org/TechArticle"
  - id: 5
    text: "Atom Syndication Format — RFC 4287."
    url: "https://datatracker.ietf.org/doc/html/rfc4287"
  - id: 7
    text: "llmstxt.org convention for LLM crawlers."
    url: "https://llmstxt.org/"
  - id: 8
    text: "Wikipedia Manual of Style — Layout."
    url: "https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Layout"
---

`app-mediakit-knowledge` es el motor wiki Rust de binario único que sirve la documentación de ingeniería de PointSav en `https://documentation.pointsav.com`. El motor combina un servidor HTTP `axum`, un renderizador CommonMark `comrak`[^1][^2] con extensiones específicas de la plataforma para wikilinks, notas al pie, tabla de contenidos y anclas de sección, un backend de búsqueda de texto completo `tantivy`[^3] y una capa de plantillas `maud`. El motor lee archivos Markdown desde un directorio de contenido que el operador indica al arrancar, los renderiza bajo demanda a HTML y los devuelve con cabeceras de caché ajustadas para un público de documentación técnica.

El motor es una *vista* sobre un árbol de Markdown, no un repositorio de contenido. El árbol de Markdown es canónico; el binario en ejecución es una vista que cualquier número de operadores puede levantar sobre el mismo árbol de contenido, o sobre árboles distintos, sin estado mutable compartido del lado del binario. Esta inversión de la fuente de verdad es la decisión de diseño más importante y se trata en detalle en la siguiente sección.

La primera implementación pública del motor entró en servicio el 2026-04-27 a las 16:25 UTC, sirviendo un árbol de contenido inicial de cuatro archivos en `https://documentation.pointsav.com`.

## Inversión de la fuente de verdad

La decisión de diseño central del sustrato: **git es canónico; el binario en ejecución es una vista**.

Todo artefacto concreto con el que un lector interactúa — la página HTML, la entrada del feed Atom, el bloque JSON-LD, el resultado de búsqueda — se deriva en tiempo de solicitud del árbol de Markdown en disco. El estado del disco es lo que se confirma, revisa, replica y divulga. El HTML es descartable. El índice Tantivy es descartable, reconstruido desde el árbol de Markdown al arrancar.

### Inversión del modelo MediaWiki

Esta inversión revierte el modelo tradicional de MediaWiki, donde la base de datos es canónica y el sistema de archivos es una copia de trabajo derivada. Aquí, el sistema de archivos es canónico y la base de datos (índice de búsqueda) es una copia de trabajo derivada. La motivación es la simplicidad operativa — una copia de seguridad del árbol de contenido es un `git clone`; una réplica es un `git pull`; una auditoría es un `git log` — y una invariante a nivel de sustrato: cada afirmación publicada es un commit git firmado; el registro de divulgación es el historial de git; la postura de divulgación continua BCSC queda impuesta por la estructura, no solo por política.

### Flujos de trabajo que la inversión elimina

De la inversión se derivan otros patrones. La wiki no tiene flujo de vista-previa-y-publicación porque el estado canónico es lo que ya se confirmó — un commit ya es una publicación. La wiki no tiene publicación programada por la misma razón. La wiki no tiene estado de borrador del lado del servidor porque los borradores viven en la copia de trabajo git del colaborador o en el pipeline editorial, no en una base de datos que el motor posea.

## Superficie de rutas

El motor expone un conjunto acotado de rutas HTTP. Cada una es independiente; ninguna depende de estado de sesión ni de una base de datos que el motor posea.

| Ruta | Propósito |
|---|---|
| `/healthz`, `/health` | Verificación de disponibilidad |
| `/` | Página de índice (lista todos los artículos del árbol de contenido servido) |
| `/wiki/{slug}` | HTML del artículo renderizado |
| `/es/wiki/{slug}` | HTML del par en español renderizado |
| `/category/{name}` | Página de categoría |
| `/history/{slug}` | Historial de revisiones por artículo, leído directamente del log de git y mostrando el diff de cada revisión |
| `/special/all-pages` | Índice completo de artículos |
| `/special/recent-changes` | Artículos editados recientemente |
| `/search?q=` | Resultados de búsqueda de texto completo (Tantivy) |
| `/sitemap.xml` | Sitemap conforme a sitemaps.org |
| `/robots.txt` | Descubrimiento para rastreadores |
| `/feed.atom` | Feed de sindicación Atom RFC 4287[^5] |
| `/llms.txt` | Convención llmstxt.org para rastreadores de LLM[^7] |
| `/static/{*path}` | Activos estáticos (CSS, JS, fuentes) |

No existe editor en el navegador ni ruta de escritura — cada artículo se edita en su repositorio git de origen y se recoge en el siguiente renderizado, no a través del propio motor.

### Esquema JSON-LD del artículo

El motor emite esquema JSON-LD `TechArticle`[^4] y `DefinedTerm` en el bloque `<head>` de cada artículo renderizado, para comprensión de motores de búsqueda y rastreadores. Los datos estructurados se generan a partir del frontmatter del artículo, no se redactan a mano por página; el esquema tiene la misma forma en todo el corpus.

## Cromo de memoria muscular de Wikipedia

El motor incluye un cromo deliberadamente reconocible para cualquier lector de Wikipedia. Un lector de cualquier artículo de Wikipedia navegará el motor sin instrucciones previas, y un lector no familiarizado con Wikipedia adoptará el patrón rápidamente porque son convenciones bien documentadas.[^8]

### Convenciones conservadas de Wikipedia

- Pestañas Artículo/Discusión en la parte superior de la página
- Una pestaña Ver historial junto al par Artículo/Discusión, leída directamente del log de git del artículo
- Orden de cierre del artículo: Referencias, Véase también, Categorías, con una banda de pie que nombra la licencia del artículo y el sustrato
- Banda hatnote en la parte superior del artículo para desambiguación y referencias cruzadas
- Convención de primera oración del lead (sujeto en negrita más cópula más definición)
- Eslogan directamente bajo el título del artículo
- Tabla de contenidos plegable en el margen izquierdo (construida desde encabezados H2 y H3)
- Selector de idioma (actualmente inglés / español)

### Añadidos más allá de Wikipedia

- Insignias de cita junto a referencias `[citation-id]` en línea, con tarjeta emergente que muestra la entrada del registro
- Banner cautelar de Información Prospectiva cuando el frontmatter de un artículo establece `forward_looking: true`
- Campo `disclosure_class` de BCSC expresado en los datos estructurados JSON-LD de cada artículo renderizado
- Selector de densidad de lectura (compacto / cómodo; la preferencia persiste del lado del cliente)

## Modelo de edición

No existe editor en el navegador, ni API de escritura, ni modelo de sesión colaborativa o de bloqueo — el motor es de solo lectura desde la perspectiva de un visitante. Un artículo se edita en su repositorio git de origen, mediante el flujo editorial normal que produce el commit, y el cambio aparece en el siguiente renderizado sin reinicio del servicio. El historial de revisiones que un lector ve en `/history/{slug}` es ese mismo log de git, leído directamente en lugar de duplicado en una base de datos aparte.

## Búsqueda y sindicación

El motor indexa el árbol de contenido al arrancar. El índice es Tantivy en disco en `<state-dir>/search/`, reconstruido desde el árbol de contenido si falta.

### Sindicación y descubrimiento para rastreadores

- **`/feed.atom`** — feed de sindicación Atom RFC 4287 del corpus.
- **`/sitemap.xml`** — conforme a sitemaps.org. Enumera cada URL de artículo con su fecha de última modificación.
- **`/robots.txt`** y **`/llms.txt`** — archivos de descubrimiento para rastreadores y rastreadores de LLM[^7].

## Superficie de compatibilidad nativa del sustrato

El motor es una wiki nativa del sustrato, no un shim de MediaWiki. Esto refleja decisiones arquitectónicas tomadas durante el desarrollo temprano de la plataforma.

### Superficies de MediaWiki conservadas y descartadas

Lo que se conservó: la **ruta de importación `xml-dump`** para migración de corpus única; las **convenciones de URL** (`/wiki/{slug}`); la **sintaxis de wikilink** (`[[slug]]` y `[[slug|texto]]`); la **sintaxis de nota al pie** (`[^1]`).

Lo que se descartó: el **shim de la Action API de MediaWiki** — el shim se limitó en v0.1.10 y se retiró en v0.1.14, porque el mantenimiento escala con la velocidad de MediaWiki y la auditoría de cumplimiento escala con la superficie de la API. La superficie nativa del sustrato (HTML de artículo, JSON-LD, Atom, sitemap, llms.txt, búsqueda vía `/search?q=`) cubre los mismos casos de uso sin una interfaz autoritativa paralela que exija mantenimiento aparte. Las **plantillas y funciones de parser de MediaWiki** se descartaron porque la ruta de renderizado del motor es CommonMark con extensiones propias de PointSav, no un parser de MediaWiki. El **ecosistema pywikibot** se descartó porque la ruta de automatización del sustrato es el conjunto de herramientas del espacio de trabajo ya existente, no el framework pywikibot.

### Superficie más estrecha, postura coherente

El compromiso es una superficie de compatibilidad más estrecha a cambio de una postura coherente con el sustrato. Un lector que migra desde un despliegue de MediaWiki pierde plantillas y la Action API; gana inversión de la fuente de verdad, renderizado determinista, postura de divulgación fundamentada en BCSC y una superficie de ataque menor.

Un artículo hermano aparte ([[substrate-native-compatibility]]) cubre la justificación completa.

## Federación de contenido

El motor está pensado para servir contenido desde múltiples repositorios git a través de una única superficie renderizada, mediante un manifiesto de montaje declarativo (`knowledge.toml`) que el operador coloca en la raíz del directorio de contenido. Cada entrada de montaje nombra un repositorio de origen, una ruta de montaje local y un plano — el esquema que determina cómo se validan, enrutan y enlazan los archivos de ese montaje. Esta capacidad está planificada; la arquitectura aquí descrita es el diseño previsto, y el modelo de un solo repositorio es la forma actualmente desplegada.

### Montajes y esquemas de plano

Un montaje de contenido es un subárbol de directorio derivado de un repositorio git nombrado. Los planos son esquemas nombrados que restringen el contenido que un montaje puede contener y determinan el patrón de URL que ocupa. Dos planos vienen integrados: `topic` (el artículo wiki estándar) y `guide` (documentos operativos, renderizados con un cromo distinto y excluidos del índice de artículos principal). Los operadores podrán registrar planos adicionales — `regional-market`, `adr`, `changelog` y esquemas específicos de dominio similares — como complementos cuando la Fase 6 esté disponible.

### Aislamiento por instancia

Cada instancia wiki lee solo los montajes declarados en su propio `knowledge.toml`. Un despliegue de `documentation.pointsav.com` y uno de `projects.woodfinegroup.com` pueden tomar de repositorios superpuestos pero presentar superficies de artículo completamente independientes — las definiciones de montaje son configuración por instancia, no estado de registro global.

### Procedencia

Cada artículo renderizado desde un montaje declarativo lleva frontmatter de procedencia que identifica el repositorio de origen y la ruta. Puesto que el motor no tiene superficie de escritura propia, esto mantiene intacta la inversión de la fuente de verdad en toda una superficie federada por construcción: ninguna instancia wiki puede escribir a un repositorio del que no es originaria, porque ninguna instancia wiki escribe a ningún repositorio.

La Fase 6 está planificada para entregar la especificación del esquema `knowledge.toml`, la API de complementos de plano y el manejo del frontmatter de procedencia. La Fase 7 está planificada para entregar recuperación con direccionamiento por contenido y federación anclada en `blake3`. Véase [[federation-via-content-mounts]] para el patrón en profundidad.

## Estado de construcción

El motor está desplegado y sirviendo `documentation.pointsav.com` hoy: el renderizado, los wikilinks, las páginas de categoría, el historial por artículo, la búsqueda y la superficie de sindicación/rastreadores anterior están todos en producción. No existe editor, ni API de escritura, ni superficie de edición colaborativa — el único camino de un artículo hacia la publicación es un commit a su repositorio git de origen, leído por el motor en el siguiente renderizado.

## Véase también

- [[source-of-truth-inversion]] — el patrón canónico / vista / efímero generalizado en el sustrato
- [[substrate-native-compatibility]] — la justificación de retirar la Action API y el conjunto de superficie nativa del sustrato
- [[wikipedia-leapfrog-design]] — la filosofía de diseño de memoria muscular y margen leapfrog del 95%/5%
- [[knowledge-wiki-home-page-design]] — la intención de diseño de la página de inicio y la estructura de espacios
- [[deploy-knowledge-instance]] — guía paso a paso: compilar e iniciar app-mediakit-knowledge apuntando a un repositorio de contenido local
- [[use-knowledge-mounts]] — guía paso a paso: añadir un repositorio de contenido secundario mediante montajes declarativos en knowledge.toml
