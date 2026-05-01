---
schema: foundry-topic-v1
title: "Panorama de proveedores de wiki — cómo se ve el campo en 2026"
status: published
category: reference
last_edited: 2026-04-30
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
companion: reference/topic-wiki-provider-landscape.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

El wiki de documentación de PointSav en `documentation.pointsav.com` es uno de los participantes en un campo donde veinticinco proveedores distinguibles ofrecen alguna variación de "superficie de conocimiento con forma de wiki" en 2026. La mayoría no son plataformas de conocimiento enciclopédico; son herramientas de productividad para equipos privados, generadores de sitios de documentación para desarrolladores, o sistemas de pensamiento personal en red. Ninguno ha reemplazado a Wikipedia para el conocimiento enciclopédico de profundidad general. Esta TOPIC documenta el campo, nombra las razones estructurales por las que ningún proveedor ha cerrado la brecha, e identifica las ventajas genuinas que cada proveedor tiene sobre Wikipedia.

La auditoría es estructural, no promocional. Cada proveedor se describe factualmente con su posicionamiento publicado más sólido y la limitación estructural que le impide llenar la brecha del conocimiento enciclopédico.

## Los cuatro grupos

Veinticinco proveedores en cuatro grupos por su caso de uso objetivo:

- **Grupo A — Bases de conocimiento colaborativas**: Notion, Confluence, Coda, ClickUp Docs. Construidas para la gestión de conocimiento organizacional privado. Venden licencias de usuario a TI empresarial.
- **Grupo B — Motores wiki de acceso público**: Wiki.js, BookStack, Outline, MediaWiki, Fandom, Wikidot, DokuWiki, TiddlyWiki. Los más cercanos en forma a una plataforma de clase Wikipedia.
- **Grupo C — Generadores de sitios de documentación para desarrolladores**: Docusaurus, MkDocs Material, VitePress, Nextra, Fumadocs, Astro Starlight, GitBook, Read the Docs. Generan sitios de documentación; primero estático, edición colaborativa en segundo lugar o ninguna.
- **Grupo D — Herramientas personales y de pensamiento en red**: Obsidian Publish, Roam Research, Logseq, Capacities, Quartz v4. Principalmente gestión de conocimiento personal de un solo autor.

## Modos de falla transversales

Las ocho razones estructurales por las que ningún proveedor ha reemplazado a Wikipedia:

**(i) Desajuste de audiencia.** Los Grupos A y C fueron construidos para diferentes públicos — gestión de conocimiento organizacional privado y documentación de proyectos de software, respectivamente. La publicación enciclopédica pública requiere lo opuesto: editores anónimos, fuentes verificables, navegación orientada al lector.

**(ii) Sin constitución editorial.** La NPOV, Notabilidad, Fuentes Fiables, Sin Investigación Original y Manual de Estilo de Wikipedia constituyen una constitución editorial refinada durante décadas. Ningún proveedor en esta auditoría ofrece equivalente.

**(iii) Piso de densidad de información.** Los generadores de sitios de documentación optimizan para elegancia de prosa y estética de desarrollador. Los artículos de Wikipedia son deliberadamente densos — infocajas, hatnotes, referencias con 100+ notas al pie, navboxes, etiquetas de esbozo, páginas de desambiguación.

**(iv) Primitivas de navegación ausentes.** La pila de navegación de Wikipedia — `[[wikilink]]` con señalización de enlace rojo, Special:Random, Special:WhatLinksHere, grafo de categorías — existe completa en MediaWiki y en dos miembros más como máximo en otros lugares.

**(v) Las citas son decorativas, no constitutivas.** El sistema de notas al pie de Wikipedia hace las afirmaciones verificables a nivel de declaración. En los proveedores de los Grupos A, C y D, las citas están ausentes por completo o implementadas como hipervínculos en línea sin estructura formal.

**(vi) Sin sustrato de páginas de Discusión.** Cada artículo de Wikipedia tiene una página Discusión: que es el registro público del debate editorial. Las herramientas de los Grupos A y D tienen comentarios en línea — no debate editorial público archivado.

**(vii) Fragilidad estructural.** El formato de bloques de Notion, la estructura de packs de Coda y los documentos embebidos de ClickUp son formatos de serialización propietarios con riesgo de vendor lock-in.

**(viii) Homogeneización de plantillas.** Cada sitio de Docusaurus, Starlight, VitePress y MkDocs se ve estructuralmente idéntico — que es la estética de documentación que el lector de Wikipedia no asocia con autoridad enciclopédica.

## Por qué existe la brecha del estándar de oro en 2026

La brecha tiene cinco causas estructurales reforzadas mutuamente:

**Desalineación de incentivos comerciales.** Notion, Confluence, GitBook, Coda y ClickUp ganan dinero vendiendo licencias de usuario a organizaciones. Sus hojas de ruta están impulsadas por compradores de TI empresarial — invertir en aplicación de NPOV, infraestructura de páginas de Discusión o descubrimiento de enlaces rojos no se convierte en ingresos por licencias empresariales.

**El problema del trabajo editorial no puede automatizarse.** La autoridad estructural de Wikipedia son veinte años de trabajo editorial acumulado. El contenido generado por IA no puede replicar el proceso editorial transparente, los estándares de verificación de fuentes o la gobernanza comunitaria que hacen que Wikipedia sea confiable.

**Costo de coordinación de código abierto.** La base de código de MediaWiki tiene 25 años, lleva una enorme superficie de compatibilidad heredada y requiere recursos de la Fundación Wikimedia para su mantenimiento. Ningún proyecto de código abierto independiente ha enviado un "MediaWiki v2 con UX moderno".

**Expansión del alcance por un lado, alcance estrecho por el otro.** Los proveedores del Grupo A se expandieron hacia "plataformas de todo"; los del Grupo C son generadores de sitios estáticos deliberadamente mínimos.

**La brecha de memoria muscular de Wikipedia.** Ningún competidor ha invertido en replicar la UX de navegación del lector que miles de millones de usuarios de Wikipedia conocen por reflejo.

## Lo que esto significa para documentation.pointsav.com

El motor wiki `app-mediakit-knowledge` se convierte en la demostración instalable por el cliente de ese sustrato. El argumento estructural para la afirmación de salto generacional es lo que esta TOPIC documenta: la brecha existe por las cinco causas estructurales anteriores; cerrarla requiere las condiciones previas descritas en la convención del sustrato compuesto y la postura de soberanía del sustrato de PointSav.

## Véase también

- [[topic-knowledge-wiki-home-page-design]] — La intención de diseño de la página de inicio y el encuadre competitivo de premios.
- [[topic-article-shell-leapfrog]] — Las primitivas de salto generacional del shell de artículo.
- [[topic-wikipedia-leapfrog-design]] — La narrativa de diseño detrás del contrato de memoria muscular 95%/5%.
- [[topic-substrate-native-compatibility]] — Por qué el sustrato envía su propia superficie en lugar de adaptar un proveedor existente.

## Procedencia

Vista general estratégica en español elaborada por project-language el 2026-04-30. Basada en el borrador de project-knowledge (síntesis Opus desde informe Sonnet sub-agente C, 2026-04-30). La investigación primaria se realizó mediante web-fetch en los 25 proveedores y búsqueda web con términos de revisión y comparación. Por DOCTRINE.md §XII, esta vista general no es una traducción literal — adapta el análisis del campo para lectores en español. Las afirmaciones prospectivas siguen [ni-51-102] y [osc-sn-51-721].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
