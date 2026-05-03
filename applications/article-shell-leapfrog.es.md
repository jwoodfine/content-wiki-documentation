---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
companion: topic-article-shell-leapfrog.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

El wiki de documentación de PointSav en documentation.pointsav.com hereda su superficie de lectura de artículos de Wikipedia bajo el diseño Vector 2022. El TOPIC complementario [[wikipedia-leapfrog-design]] cubre lo que se preserva verbatim — el contrato de memoria muscular. Este TOPIC cubre lo que se extiende más allá.

Cinco primitivas de la capa de artículo que el modelo de gobernanza voluntaria de Wikipedia ha sido estructuralmente incapaz de desarrollar en quince años se describen aquí. Tres son de primera clase — el sustrato las implementa en la iteración 1. Dos son de segunda clase — el sustrato define sus superficies de token y motor y las implementa cuando el corpus alcanza la escala donde compensan el costo editorial.

## Por qué es necesario el salto tecnológico

La capa de artículo de Wikipedia es la superficie de lectura más imitada en internet público. Es el estándar de oro para la profundidad enciclopédica del conocimiento general precisamente porque sus primitivas están perfeccionadas por veinte años de refinamiento de la comunidad editorial. También está estructuralmente limitada en 2026 por diez debilidades específicas que ningún competidor comercial de wikis ha resuelto.

Las debilidades clave incluyen: la sección de referencias es una lista numérica plana sin semántica de autoridad de fuente; las infocajas son semiestructuradas pero no nativamente legibles por máquinas; la tabla de contenidos es sólo estructural sin tipado semántico de secciones; "Lo que enlaza aquí" devuelve una lista plana paginada; no hay superficie de comentarios en línea en la vista de lectura; no hay granularidad de última edición por sección; y la superficie de consumo por IA carece de pistas semánticas a nivel de sección.

## Las primitivas del salto tecnológico

**Cinta de autoridad de cita (primera clase).** Una pequeña insignia en cada entrada de la sección de Referencias indicando la categoría de la fuente — académica, regulatoria, industrial, fuente directa, noticias, informal-web. El lector puede ver de un vistazo si el artículo está respaldado por fuentes académicas y regulatorias o por fuentes informales. Los consumidores de IA obtienen la autoridad de la fuente como campo legible por máquina.

**Bloque de pie de página de rastro de investigación (primera clase).** Un bloque de pie de página plegable debajo de la sección de Referencias, renderizado cuando el frontmatter del artículo declara `research_trail: true`. Tres subsecciones: Investigación realizada, Investigación sugerida, Preguntas abiertas. Plegado por defecto. El rastro se emite como nodos JSON-LD estructurados `potentialAction`. Los consumidores de IA identifican la frontera epistémica del artículo sin leer prosa.

**Cinta de frescura — última revisión de contenido por sección (primera clase).** Una pequeña insignia opcional en cada encabezado de sección mostrando la fecha del último cambio sustantivo de contenido. Escala de tres estados indica fresco / obsoleto / archivado. El sustrato emite propiedades `dateModified` por sección en nodos JSON-LD `WebPageElement`.

**Palanca de lenguaje sencillo respaldada por párrafos redactados y revisados (segunda clase).** Una palanca en la barra de preferencias del lector. Cuando está activa, las secciones del artículo marcadas `plain_language: true` renderizan un párrafo de introducción alternativo escrito en un nivel de lectura más bajo. Los párrafos de lenguaje sencillo son redactados explícitamente por humanos y confirmados en el código fuente del artículo — no son generados en tiempo de solicitud. Posicionada como segunda clase porque la curación cuesta labor editorial que escala linealmente con el tamaño del corpus.

**Minimapa del grafo de citas — vecindad de 3 saltos (segunda clase).** Una sección plegable al pie del artículo que muestra un pequeño grafo SVG: el artículo actual como nodo central, los wikilinks salientes de 1 salto como primer anillo, los enlaces entrantes de 1 salto como segundo anillo. Los mismos datos de enlace se emiten en arrays JSON-LD `relatedLink` y `mentions`. Posicionada como segunda clase porque el grafo de wikilinks debe pre-computarse; vale la pena implementarla cuando el corpus de artículos alcanza ≥200 artículos.

## Lo que el salto tecnológico deliberadamente no cambia

Cada primitiva de salto tecnológico en este TOPIC es aditiva — ninguna modifica el registro del cuerpo del artículo. El estilo de resumen, el sujeto definido en la apertura, el registro NPOV, la disciplina de longitud de párrafo, la densidad de enlaces, el contrato de la sección introductoria — todas estas características se preservan verbatim. Las primitivas son subordinadas al cuerpo del artículo y no interfieren con la experiencia de lectura principal.

## Véase también

- [[wikipedia-leapfrog-design]] — el contrato de memoria muscular
- [[app-mediakit-knowledge]] — el motor que implementa estas primitivas
- [[knowledge-wiki-home-page-design]] — intención de diseño de la página principal
- [[wiki-provider-landscape]] — el panorama competitivo

## Procedencia

Redactado el 2026-04-30 por el cluster project-knowledge, sintetizando investigación paralela de sub-agentes y consulta directa de documentos del espacio de trabajo. Refinado por project-language 2026-04-30. Las declaraciones prospectivas siguen la postura de divulgación continua [ni-51-102] y [osc-sn-51-721].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
