---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
companion: topic-wikipedia-leapfrog-design.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

La narrativa de diseño detrás del cromo de `app-mediakit-knowledge`: qué se mantuvo de Wikipedia, qué se añadió más allá de Wikipedia, la divergencia deliberada de identidad visual, y qué significa el 5% de espacio de maniobra del salto tecnológico para lectores e ingenieros.

## El contrato de memoria muscular

Wikipedia tiene aproximadamente dos mil millones de lectores mensuales. Esos lectores han desarrollado reflejos de navegación durante dos décadas de exposición a un cromo específico. El sustrato elige adoptar ese cromo de manera principista — no superficial. La adopción principista identifica el conjunto exacto de patrones que llevan la memoria muscular y los mantiene inviolables.

`UX-DESIGN.md §3` nombra la asignación estructural: el 95% del cromo es el inventario de memoria muscular de Wikipedia, mantenido inviolable en todas las fases; el 5% es el espacio de maniobra del salto tecnológico — adiciones que ningún lector de Wikipedia ha encontrado, implementadas como añadidos en lugar de reemplazos.

**Lo que se mantuvo en la Fase 1** cubre la convención de notas al pie, la capacidad de infocaja en el carril derecho, los colores de enlace (azul no visitado / violeta visitado / rojo objetivo faltante), la tipografía del cuerpo (pila serif, cuerpo mínimo 17px, interlineado 1.5 o mayor, longitud de línea de 45–75 caracteres), el marcador de posición de búsqueda en el centro superior, y el cromo para móviles.

**La Fase 1.1 (aditiva sobre la Fase 1)** añade los elementos del cromo que requieren adiciones estructurales a la capa de plantilla: par de pestañas Artículo / Discusión, pestañas Leer / Editar / Ver historial, lápices `[editar]` por sección, ordenación al final del artículo, nota hatnote, convención de primera oración del encabezado, colofón "De PointSav Knowledge", tabla de contenidos plegable en el carril izquierdo, selector de idioma, y convención de pie de página.

## Lo que se añadió más allá de Wikipedia

Cinco adiciones se implementan más allá del inventario de Wikipedia. Cada una es aditiva.

**Insignias de cita.** Junto a cada referencia `[citation-id]` en línea, el cromo muestra una pequeña insignia en la convención del glifo "CR" de C2PA. El color predeterminado es gris neutro — la decisión de diseño crítica tomada directamente de la lección del candado TLS. La calibración: gris neutro para todo verificado, ámbar para deriva de fuente, rojo para una cita faltante o sin coincidencia de hash, azul para información prospectiva.

**Patrón de banner FLI.** Los artículos cuyo frontmatter establece `forward_looking: true` renderizan un banner cautelar en la vista de lectura. El banner es la expresión en la superficie de lectura del requisito de la postura de divulgación continua BCSC.

**Campo `disclosure_class` BCSC.** Los artículos llevan un campo `disclosure_class` en el frontmatter con tres valores: `narrative`, `financial`, `governance`. En la fase actual este campo es invisible para los lectores — se expresa en datos estructurados JSON-LD en el bloque `<head>` de cada artículo renderizado.

**Banda de encabezado del marcador de posición IVC.** Una sola franja horizontal en la parte superior de cada artículo. En la Fase 1.1 esta banda muestra texto de marcador de posición. La Fase 7 está planificada para llenar la banda con una línea de resumen de verificación en vivo.

**Palanca de densidad del lector.** Una preferencia con tres estados: Desactivado, Solo excepciones (predeterminado), Todo. El predeterminado es Solo excepciones — la puesta en práctica de la lección del candado TLS: la experiencia de lectura de referencia suprime la señal positiva, mostrando solo las desviaciones del estado verificado esperado.

## La divergencia deliberada de identidad visual

La adopción del cromo de Wikipedia por parte del sustrato es principista, no imitativa. Se hereda el sustrato ergonómico de la memoria muscular — la ubicación de pestañas, el índice de contenidos, cómo caen los encabezados, cómo se numeran las notas al pie — y se diverge visualmente donde la divergencia no cuesta familiaridad ergonómica.

El sustrato rastrea la disciplina tipográfica de Vector 2022 porque es ergonómica, no de marca: texto del cuerpo mínimo 17px, interlineado 1.5 o mayor, longitud de línea de 45 a 75 caracteres. La paleta de colores de la casa PointSav se aplica a todos los elementos del cromo: fondo de la barra de pestañas, color de subrayado del enlace, color del encabezado de sección. Sin logotipo de Wikimedia. Sin marca de Wikipedia.

## Por qué ambas audiencias se sienten en casa

El **lector de la comunidad financiera** llega a un artículo específico. Navega sin fricción porque ha navegado esta estructura miles de veces en Wikipedia. El **lector de ingeniería** tiene la misma experiencia de navegación y también nota la presencia de `<script type="application/ld+json">` con un perfil `TechArticle` de Schema.org, la URL del artículo que corresponde a un nombre de archivo Markdown en un repositorio Git, y el endpoint `/feed.atom` anunciado en la cabecera de la página. Ambos lectores están en casa. Ninguno tuvo que aprender un nuevo paradigma.

## Véase también

- [[topic-app-mediakit-knowledge]] — la arquitectura del motor; inventario del cromo
- [[topic-source-of-truth-inversion]] — el patrón canónico / vista / efímero
- [[topic-substrate-native-compatibility]] — la justificación de la eliminación de la Action API
- [[topic-article-shell-leapfrog]] — las cinco primitivas de la capa de artículo más allá de Wikipedia
- [[topic-knowledge-wiki-home-page-design]] — la intención de diseño de la página de inicio

## Procedencia

Redactado el 2026-04-28 por el cluster project-knowledge basándose en `UX-DESIGN.md` y `ARCHITECTURE.md`. Refinado por project-language 2026-04-30. Las declaraciones prospectivas sobre las fases planificadas siguen [ni-51-102] y [osc-sn-51-721].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
