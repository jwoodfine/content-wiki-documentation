---
schema: foundry-doc-v1
title: "Sistema de diseño"
slug: _index
short_description: "El sistema de diseño PointSav como componente de plataforma — su vocabulario fundacional, filosofía de diseño y contexto de superficie de marca. Las guías de implementación de componentes, especificaciones de tokens y documentación de accesibilidad se encuentran en design.pointsav.com."
category: design-system
type: reference
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.md
short_description: "El sistema de diseño de PointSav como componente de la plataforma — estructuración arquitectónica, primitivos de diseño y contexto de identidad de marca."
---

La categoría de sistema de diseño abarca el sistema de diseño de PointSav como componente de la plataforma — su vocabulario fundamental, filosofía de diseño, contexto de superficie de marca y las familias de tokens de la capa de fundación que heredan las superficies orientadas al operador. Trata el sistema de diseño como concepto dentro de la plataforma: por qué existe, cómo está estructurado, qué identidad de marca porta y dónde se alinea el vocabulario de tokens fundacionales con la convención del campo. Las guías de implementación de componentes, las especificaciones de accesibilidad y la superficie de trabajo se encuentran en el repositorio del sistema de diseño en `design.pointsav.com`; esta categoría aporta el marco arquitectónico.

El sistema de diseño es en sí mismo uno de los sustratos portantes de la plataforma — véase [[design-system-substrate|sustrato del sistema de diseño]] para el marco de sustrato — y hereda las mismas disciplinas de propiedad del cliente, legibilidad por máquina e interoperabilidad agnóstica al editor que el resto de la plataforma aplica a sus capas de datos. Cada superficie que renderiza el sistema de diseño está especificada con enfoque móvil primero; **Inter** es la tipografía de interfaz de usuario y encabezados, elegida por su legibilidad en pantalla y la ausencia de propiedad corporativa.

## Filosofía y vocabulario primitivo

Las decisiones fundacionales: por qué existe el sustrato, qué preservó de la convención, qué reemplazó.

- [[design-philosophy|Filosofía de diseño]] — Por qué existe el sustrato; tres inversiones estructurales del patrón de plataformas enterprise; publicación de tokens autoalojada, de propiedad del cliente y agnóstica al editor.
- [[design-primitive-vocabulary|Vocabulario primitivo de diseño]] — Justificación del vocabulario: escalas numéricas de color, aliasing semántico por capas, separación entre tipografía productiva y expresiva, y escalas numéricas de espaciado alineadas con la convención del campo de 2018 a 2026.
- [[design-system-substrate|Sustrato del sistema de diseño]] — El marco de sustrato: motor de sistema de diseño autoalojado que almacena tokens y componentes en el propio repositorio git del cliente; formato de tokens W3C DTCG; endpoint MCP legible por máquina.

## Tokens de fundación

Las cuatro familias de tokens de la capa de fundación: color, tipografía, espaciado y movimiento. Especificaciones completas mantenidas en `pointsav-design-system` y publicadas en `design.pointsav.com/foundations/`.

- [[design-color|Color]] — Fundaciones de tokens de color: paleta primitiva, alias semánticos y pares de modo oscuro en formato DTCG.
- [[design-typography|Tipografía]] — Fundaciones de tokens tipográficos: escala tipográfica, pilas de fuentes, variables de tipografía fluida y tokens de ritmo de lectura.
- [[design-spacing|Espaciado]] — Fundaciones de tokens de espaciado: unidad base, escala geométrica, tokens de separación de componentes y tokens de margen de diseño.
- [[design-motion|Movimiento]] — Fundaciones de tokens de movimiento: escala de duración, curvas de aceleración y variantes de movimiento reducido.

## Superficie de marca

Cómo se codifica la identidad de marca como familias de color y pilas tipográficas en las superficies de producto PointSav y Woodfine.

- [[brand-family-swatch|Familias de color de marca]] — Las familias de colores de la marca asignadas a categorías minoristas e institucionales en la superficie GIS de co-localización; identificadores codificados por color consistentes para visualización en mapa y datos tabulares.
- [[brand-typography|Tipografía de marca]] — La separación tipográfica entre fuentes del sistema para interfaz web y tipografía institucional para impresión; tipos serif de licencia abierta reservados para generación de PDF y divulgaciones formales.

## Diseño de superficie wiki

El vocabulario de componentes, sistema tipográfico y paleta de modo oscuro que componen la superficie de lectura de `documentation.pointsav.com`.

- [[wiki-component-library|Biblioteca de componentes wiki]] — Nueve componentes de interfaz reutilizables que componen una página completa de artículo wiki; convenciones de diseño de Wikipedia, estándares de accesibilidad actuales, sistema de tokens PointSav.
- [[wiki-typography-system|Sistema tipográfico wiki]] — Pila tipográfica Inter y Source Serif 4, escala de encabezados y tokens de espaciado para el wiki; cobertura lingüística amplia para contenido bilingüe.
- [[wiki-dark-mode|Modo oscuro wiki]] — Esquemas de color claro y oscuro para el wiki: paletas verificadas por WCAG y persistencia del tema mediante localStorage.

## Fundaciones relacionadas

Los artículos arquitectónicos y de sustrato que enmarcan el sistema de diseño dentro de la plataforma más amplia.

- [[building-design-system-bim|Sistema de diseño para BIM]] — Herramientas del sistema de diseño adaptadas para flujos de trabajo de BIM y propiedad inmobiliaria, emparejadas con la disciplina de mantenimiento de registros ISO 19650.
- [[aec-interface-conventions|Convenciones de interfaz AEC]] — Convenciones de interfaz para superficies AEC que el sistema de diseño hereda y extiende.
- [[knowledge-wiki-leapfrog-architecture|Arquitectura de salto del wiki de conocimiento]] — Cómo el motor wiki consume los tokens y componentes del sistema de diseño para renderizar cromo con forma de Wikipedia sobre Markdown plano.

## Véase también

- [Sustrato](/substrate/) — el marco de sustrato del sistema de diseño junto con los otros sustratos de mecanismos fundacionales
- [Patrones](/patterns/) — patrones de diseño nombrados que el sistema de diseño codifica en la capa de interfaz
- [Aplicaciones](/applications/) — aplicaciones orientadas al operador que consumen el sistema de diseño a través de las capas de tokens y componentes
