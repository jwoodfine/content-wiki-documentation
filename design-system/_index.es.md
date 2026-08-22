---
schema: foundry-doc-v1
title: "Sistema de diseño"
slug: design-system-index
short_description: "El sistema de diseño PointSav como componente de plataforma — su vocabulario fundacional, filosofía de diseño y contexto de superficie de marca. Las guías de implementación de componentes, especificaciones de tokens y documentación de accesibilidad se encuentran en design.pointsav.com."
category: design-system
type: reference
content_type: topic
quality: complete
index_type: thematic
index_scope: design-system
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: _index.md
---

La categoría de sistema de diseño abarca el sistema de diseño de PointSav como componente de la plataforma — su vocabulario fundamental, filosofía de diseño, contexto de superficie de marca y las familias de tokens de la capa de fundación que heredan las superficies orientadas al operador. Trata el sistema de diseño como concepto dentro de la plataforma: por qué existe, cómo está estructurado, qué identidad de marca porta y dónde se alinea el vocabulario de tokens fundacionales con la convención del campo. Las guías de implementación de componentes, las especificaciones de accesibilidad y la superficie de trabajo se encuentran en el repositorio del sistema de diseño en `design.pointsav.com`; esta categoría aporta el marco arquitectónico.

El sistema de diseño es en sí mismo uno de los sustratos portantes de la plataforma — véase [[design-system-substrate|sustrato del sistema de diseño]] para el marco de sustrato — y hereda las mismas disciplinas de propiedad del cliente, legibilidad por máquina e interoperabilidad agnóstica al editor que el resto de la plataforma aplica a sus capas de datos. Cada superficie que renderiza el sistema de diseño está especificada con enfoque móvil primero; **Inter** es la tipografía de interfaz de usuario y encabezados, elegida por su legibilidad en pantalla y la ausencia de propiedad corporativa.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[design-philosophy|Filosofía de diseño]] — por qué existe el sustrato, y las tres inversiones estructurales del patrón de plataformas enterprise sobre las que se construye todo lo demás en esta categoría.

<!-- END-START-HERE-HIGHLIGHT -->

## Filosofía y vocabulario primitivo

Las decisiones fundacionales: por qué existe el sustrato, qué preservó de la convención, qué reemplazó.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: philosophy-and-primitive-vocabulary -->
- [[design-philosophy|Filosofía de diseño]] — Por qué existe el sustrato; tres inversiones estructurales del patrón de plataformas enterprise; publicación de tokens autoalojada, de propiedad del cliente y agnóstica al editor.
- [[design-primitive-vocabulary|Vocabulario primitivo de diseño]] — Justificación del vocabulario: escalas numéricas de color, aliasing semántico por capas, separación entre tipografía productiva y expresiva, y escalas numéricas de espaciado alineadas con la convención del campo de 2018 a 2026.
- [[design-system-substrate|Sustrato del sistema de diseño]] — El marco de sustrato: motor de sistema de diseño autoalojado que almacena tokens y componentes en el propio repositorio git del cliente; formato de tokens W3C DTCG; endpoint MCP legible por máquina.
<!-- END AUTO-GENERATED -->

## Conceptos de tokens y herramientas

Artículos de contexto sobre qué son los tokens, cómo componen los componentes, cómo tematizan y cómo llegan a diseñadores, agentes de IA y otras organizaciones.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: token-concepts-and-tooling -->
- [[what-is-a-design-token|Qué es un token de diseño]] — Un token de diseño como decisión de diseño registrada como datos; el Format Module DTCG del W3C; el modelo de niveles primitivo/semántico/componente.
- [[theming-via-semantic-tokens|Tematización mediante tokens semánticos]] — Los temas claro/oscuro como sustitución de tokens semánticos, fundamentado en el grupo `theme.dark` publicado y el mismo patrón en Carbon, Material 3 y Radix.
- [[component-recipes-vs-raw-tokens|Recetas de componentes frente a tokens en bruto]] — Qué añade el nivel de componentes más allá del valor de un token: el formato `recipe.json` y el estado documental de dos niveles del registro.
- [[design-tokens-and-accessibility|Tokens de diseño y conformidad de accesibilidad]] — Cómo los requisitos de accesibilidad — objetivos táctiles, color del anillo de foco, contraste — se expresan como tokens en lugar de verificarse ad hoc.
- [[figma-tokens-studio-integration|Figma y Tokens Studio]] — Cómo llevar la exportación de tokens publicada a Figma mediante la sincronización de solo lectura por URL del plugin Tokens Studio.
- [[mcp-ai-agent-consumable-design-systems|MCP y sistemas de diseño consumibles por agentes de IA]] — Por qué el sistema de diseño expone un endpoint MCP legible por máquina y una API de búsqueda de tokens para agentes de codificación de IA.
- [[registry-driven-releases|Versiones dirigidas por registro]] — La arquitectura dirigida por registro que evita que la navegación, las estadísticas de la página de inicio y el empaquetado de versiones se desalineen.
- [[self-hosting-customer-controlled-design-systems|Autoalojar un sistema de diseño]] — Las dos ofertas diferenciadas: usar directamente los tokens publicados y autoalojar el motor de servicio para el propio sistema de diseño de otra organización.
<!-- END AUTO-GENERATED -->

## Superficie de marca

Cómo se codifica la identidad de marca como familias de color y pilas tipográficas en las superficies de producto PointSav y Woodfine.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: brand-surface -->
- [[brand-family-swatch|Familias de color de marca]] — Las familias de colores de la marca asignadas a categorías minoristas e institucionales en la superficie GIS de co-localización; identificadores codificados por color consistentes para visualización en mapa y datos tabulares.
- [[brand-typography|Tipografía de marca]] — La separación tipográfica entre fuentes del sistema para interfaz web y tipografía institucional para impresión; tipos serif de licencia abierta reservados para generación de PDF y divulgaciones formales.
<!-- END AUTO-GENERATED -->

## Diseño de superficie wiki

El vocabulario de componentes, sistema tipográfico y paleta de modo oscuro que componen la superficie de lectura de `documentation.pointsav.com`.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: wiki-surface-design -->
- [[wiki-component-library|Biblioteca de componentes wiki]] — El armazón compartido del wiki (encabezado, navegación móvil fuera de lienzo, barra lateral, pie de página) y las plantillas de página que envuelve, en un vocabulario de tokens `k-*` compartido.
- [[wiki-typography-system|Sistema tipográfico wiki]] — Pila tipográfica Inter y Source Serif 4, escala de encabezados y tokens de espaciado para el wiki; cobertura lingüística amplia para contenido bilingüe.
- [[wiki-dark-mode|Modo oscuro wiki]] — Esquemas de color claro y oscuro para el wiki: anulaciones de tokens semánticos sobre un atributo `data-theme`, con persistencia del tema mediante localStorage.
<!-- END AUTO-GENERATED -->

## Fundaciones relacionadas

Los artículos arquitectónicos y de sustrato que enmarcan el sistema de diseño dentro de la plataforma más amplia.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: related-foundations -->
- [[knowledge-wiki-leapfrog-architecture|Arquitectura de salto del wiki de conocimiento]] — Cómo el motor wiki consume los tokens y componentes del sistema de diseño para renderizar cromo con forma de Wikipedia sobre Markdown plano.
<!-- END AUTO-GENERATED -->

Artículos adicionales planificados — herramientas del sistema de diseño para BIM y convenciones de interfaz AEC — aún no están escritos.

## Tokens de fundación

Las cuatro familias de tokens de la capa de fundación: color, tipografía, espaciado y movimiento. Las especificaciones completas se mantienen en `pointsav-design-system` y se publican en el sitio propio del sistema de diseño — son enlaces externos, no artículos de la wiki.

- [Tokens de color](https://design.pointsav.com/elements/color/overview) — paleta primitiva, alias semánticos y pares de modo oscuro en formato DTCG.
- [Tokens de tipografía](https://design.pointsav.com/elements/typography/overview) — escala tipográfica, pilas de fuentes, variables de tipografía fluida y tokens de ritmo de lectura.
- [Tokens de espaciado](https://design.pointsav.com/elements/spacing/overview) — unidad base, escala geométrica, tokens de separación de componentes y tokens de margen de diseño.
- [Tokens de movimiento](https://design.pointsav.com/elements/motion/overview) — escala de duración, curvas de aceleración y variantes de movimiento reducido.

## Véase también

- [Sustrato](/substrate/) — el marco de sustrato del sistema de diseño junto con los otros sustratos de mecanismos fundacionales
- [Patrones](/patterns/) — patrones de diseño nombrados que el sistema de diseño codifica en la capa de interfaz
- [Aplicaciones](/applications/) — aplicaciones orientadas al operador que consumen el sistema de diseño a través de las capas de tokens y componentes
