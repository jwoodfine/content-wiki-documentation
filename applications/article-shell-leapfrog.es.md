---
schema: foundry-doc-v1
title: "El avance del shell de artículo"
slug: article-shell-leapfrog.es
category: applications
type: topic
quality: complete
short_description: "Cinco primitivos de shell de artículo que extienden la superficie de lectura de Wikipedia en sus puntos de debilidad estructural: la cinta de autoridad de citas, el bloque de pie de pista de investigación, la cinta de frescura, el interruptor de lenguaje sencillo y el mini-mapa del grafo de citas."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: article-shell-leapfrog.md
cites:
  - ni-51-102
  - osc-sn-51-721
references:
  - id: 1
    text: "Wikipedia Manual of Style — Lead section."
    url: "https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Lead_section"
  - id: 2
    text: "Wikipedia:Verifiability policy."
    url: "https://en.wikipedia.org/wiki/Wikipedia:Verifiability"
  - id: 3
    text: "Wikimedia Foundation Annual Plan 2025-2026 — Product and Technology OKRs."
    url: "https://meta.wikimedia.org/wiki/Wikimedia_Foundation_Annual_Plan/2025-2026/Product_%26_Technology_OKRs"
  - id: 4
    text: "Schema.org TechArticle specification."
    url: "https://schema.org/TechArticle"
---

## Adaptación estratégica

El wiki de documentación de PointSav en `documentation.pointsav.com` hereda su superficie de lectura de artículos de Wikipedia bajo el diseño Vector 2022. Las pestañas de artículo, los lápices de edición, las notas de sombrero, las convenciones de sección inicial, las tablas de contenidos plegables, las convenciones de infobox, las secciones de referencias y las rutas de categoría preservan todos los primitivos estructurales que un lector de Wikipedia reconoce sin pensamiento consciente.[^1] El artículo complementario [[wikipedia-leapfrog-design]] cubre lo que se preserva de forma literal — el contrato de memoria muscular.

Este artículo cubre lo que extiende más allá. Se introducen aquí cinco primitivos de shell de artículo que el modelo de gobernanza voluntaria de Wikipedia ha sido estructuralmente incapaz de implementar en quince años. Tres son de primera clase — el sustrato los implementa en la iteración 1. Dos son de segunda clase — el sustrato define sus superficies de token y motor y los implementa cuando el corpus alcanza la escala donde justifican el costo editorial.

## Por qué se necesita el avance

El shell de artículo de Wikipedia es la superficie de lectura más imitada en la internet pública. Es el estándar de referencia para la profundidad enciclopédica de conocimiento general precisamente porque sus primitivos han sido refinados por veinte años de comunidad editorial. También está estructuralmente limitado en 2026 por diez debilidades específicas que ningún competidor comercial de wikis ha implementado una solución. La Wikimedia Foundation ha nombrado algunas de ellas en sus OKRs de Producto y Tecnología 2025-2026.[^3]

Los primitivos de avance que siguen no son novedades. Cada uno aborda una debilidad nombrada específica con un primitivo nombrado específico. El sustrato implementa la solución porque tiene la superficie de ingeniería y la disciplina editorial para hacerlo.

## Debilidades estructurales del shell de artículo de Wikipedia

Diez categorías de debilidad de la auditoría de 2026:

**(i) La sección de referencias es una lista numérica plana sin semántica de autoridad de fuente.** Un artículo revisado por pares y una entrada de blog personal ocupan registros visuales idénticos.

**(ii) Los infoboxes son semi-estructurados pero no legibles por máquina de forma nativa.** Wikidata es el espejo legible por máquina canónico pero la sincronización es mantenida por voluntarios y es inconsistente.

**(iii) La tabla de contenidos es solo estructural sin tipificación semántica de secciones.** "Antecedentes", "Método", "Controversia" no se pueden distinguir por la maquinaria de la tabla de contenidos.

**(iv) Lo-que-enlaza-aquí devuelve una lista plana paginada, no un grafo.** Para un artículo de concepto la lista puede contener miles de artículos sin vecinos de segundo salto ni agrupación por dominio temático.

**(v) No hay superficie de comentarios en línea en la vista de lectura del artículo.** La discusión editorial está en una página Discusión separada.

**(vi) No hay granularidad de última edición o autoría por sección.** Un artículo de 20 secciones reporta solo "última edición" a nivel de artículo — la ilusión de frescura.

**(vii) No hay tiempo de lectura ni ayuda para hojear.** La orientación sobre el tamaño del artículo es metadatos en `?action=info`, no visible en la vista de lectura.

**(viii) No hay rastro de citas de vuelta al pasaje citado específico.** La nota al pie `[4]` resuelve a una entrada bibliográfica; el lector debe navegar independientemente a la fuente citada.

**(ix) No hay indicador de actualidad de edición en vivo.** Los artículos editados decenas de veces al día no presentan ninguna señal de cambio en sesión.

**(x) La superficie de consumo por IA está desestructurada a granularidad de sección.** El HTML de la superficie de lectura de Wikipedia no proporciona indicaciones semánticas por sección.[^3]

## Los primitivos de avance

### Cinta de autoridad de citas (primera clase)

Un pequeño distintivo inicial en cada entrada de la sección de Referencias de un artículo que indica la categoría de la fuente: académica, regulador, industria, fuente directa, noticias, web-informal. La clase se deriva del tipo de plantilla de cita y opcionalmente de un campo de frontmatter `source_authority`. Se emite como un refinamiento adicional `@type` en las entradas de citas en el bloque JSON-LD `<head>`.[^4]

Un lector puede ver de un vistazo si el artículo está respaldado por fuentes académicas y regulatorias o por fuentes informales. Un consumidor de IA que extrae datos estructurados obtiene la autoridad de fuente como un campo legible por máquina. Esto aborda la debilidad (i) directamente.

### Bloque de pie de pista de investigación (primera clase)

Un bloque de pie plegable debajo de la sección de Referencias, renderizado cuando el frontmatter del artículo declara `research_trail: true`. Tres subsecciones: Investigación realizada (fuentes consultadas con estado), Investigación sugerida (tareas abiertas del siguiente tramo), Preguntas abiertas (afirmaciones que requieren verificación). Para editores e investigadores, no para lectores casuales — plegado por defecto.

El rastro se emite como nodos JSON-LD `potentialAction` estructurados. Los consumidores de IA identifican la frontera epistémica del artículo sin leer el texto. Esto aborda las debilidades (viii) y (x) simultáneamente.

La combinación de la cinta de autoridad de citas y el bloque de pie de pista de investigación es lo que hace legible la posición epistemológica del artículo sin leer todas las notas al pie. Un lector de la comunidad financiera, un analista, un regulador — cualquier lector cuya formación profesional involucre la evaluación del tipo de fuente — entiende inmediatamente lo que está leyendo.[^2]

### Cinta de frescura — última revisión de contenido por sección (primera clase)

Un pequeño distintivo opcional en cada encabezado de sección que muestra la fecha del último cambio de contenido sustantivo en esa sección. Una escala de color de tres paradas señala fresco / obsoleto / archivado según umbrales de fecha configurables. Superficia una señal que Wikipedia estructuralmente no tiene — una fecha de revisión a nivel de sección que distingue "Antecedentes sin cambios desde 2019" de "Implementaciones actuales actualizadas ayer".

El sustrato emite propiedades `dateModified` por sección en nodos JSON-LD `WebPageElement`. Esto aborda la debilidad (vi) directamente y también aborda la debilidad (x).

### Interruptor de lenguaje sencillo respaldado por párrafos curados y redactados (segunda clase)

Un interruptor en la barra de herramientas de preferencias del lector. Cuando está activo, las secciones de artículos marcadas con `plain_language: true` en su frontmatter renderizan un párrafo inicial alternativo escrito en un nivel de lectura más bajo. El párrafo en lenguaje sencillo aparece en un bloque visualmente distinto encima del inicio técnico.

Disciplina de diseño crítica: los párrafos en lenguaje sencillo son explícitamente redactados por humanos y confirmados al código fuente del artículo, con la misma disciplina de citas que el cuerpo del artículo. No se generan automáticamente en tiempo de solicitud. Esto preserva el registro de punto de vista neutral y la verificabilidad basada en fuentes mientras extiende el punto de entrada a lectores cuyo nivel de lectura o formación no coincide con el registro técnico.

El sustrato implementa el interruptor y el esquema; el corpus elige para qué artículos redactar párrafos en lenguaje sencillo. Posicionado como segunda clase porque curar el párrafo en lenguaje sencillo en tiempo de edición cuesta labor editorial que escala linealmente con el tamaño del corpus.

### Mini-mapa del grafo de citas — vecindad de 3 saltos (segunda clase)

Una sección plegable al pie del artículo que muestra un pequeño grafo SVG: el artículo actual como nodo central, los wikilinks de salida de 1 salto como un anillo, los enlaces de entrada de 1 salto como un segundo anillo. Nodos etiquetados con títulos de artículos; las aristas llevan direccionalidad. Interactivo — hacer clic navega a ese artículo.

Los mismos datos de enlace se emiten en matrices JSON-LD `relatedLink` y `mentions`. Los consumidores de grafos de conocimiento descendentes recorren sin la capa visual. Posicionado como segunda clase porque el grafo de wikilinks debe ser pre-computado en tiempo de renderizado o servido desde una API. Vale la pena implementarlo cuando el corpus de artículos alcanza un tamaño donde el recorrido del grafo es genuinamente útil (objetivo: ≥200 artículos).

## Lo que el avance deliberadamente no cambia

El registro del cuerpo que hace que el texto de Wikipedia se sienta autoritativo es el producto de una disciplina editorial explícita. Cada primitivo de avance en este artículo es aditivo — ninguno modifica el registro del cuerpo. El estilo de resumen. El sujeto definido en la apertura. El registro de punto de vista neutral. La disciplina de longitud de párrafo. La densidad de enlaces como densidad de navegación. El contrato de sección inicial.

Las seis características se preservan de forma literal. Los primitivos de avance son subordinados al cuerpo — las insignias de autoridad de citas se ubican en un canal de 1.25em que no rompe el ritmo de línea; la pista de investigación está plegada por defecto; las cintas de frescura pueden desactivarse por preferencia del lector; el interruptor de lenguaje sencillo es opcional; el mini-mapa del grafo de citas está plegado debajo del pie de artículo visible. Un lector que llega al shell del artículo y lee solo el cuerpo recibe el contrato de memoria muscular de Wikipedia intacto.

## Véase también

- [[wikipedia-leapfrog-design]] — el contrato de memoria muscular y lo que se preserva de forma literal de Wikipedia
- [[knowledge-wiki-home-page-design]] — la intención de diseño de la página de inicio y el contrato de dos audiencias
- [[app-mediakit-knowledge]] — el motor wiki; la ruta de emisión JSON-LD para metadatos por sección
