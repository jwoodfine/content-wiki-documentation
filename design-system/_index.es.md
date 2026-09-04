---
schema: foundry-doc-v1
title: "Diseño y Marca"
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
last_edited: 2026-09-04
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
- [[design-philosophy|Filosofía de diseño]] — El sistema de diseño PointSav es un sustrato auto-alojado propiedad del cliente que se ejecuta en design.pointsav.com y publica investigación de decisiones de diseño junto con valores de tokens en formato DTCG, priorizando interoperabilidad agnóstica respecto a editores y rationale estructurado.
- [[design-primitive-vocabulary|Vocabulario primitivo de diseño]] — Justificación de los patrones de la capa de tokens primitivos — escalas de color numéricas, aliasing semántico y separación tipográfica — con nomenclatura propia de PointSav.
- [[design-system-substrate|Sustrato del sistema de diseño]] — El marco de sustrato: motor de sistema de diseño autoalojado que almacena tokens y componentes en el propio repositorio git del cliente; formato de tokens W3C DTCG; endpoint MCP legible por máquina.
<!-- END AUTO-GENERATED -->

## Conceptos de tokens y herramientas

Artículos de contexto sobre qué son los tokens, cómo componen los componentes, cómo tematizan y cómo llegan a diseñadores, agentes de IA y otras organizaciones.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: token-concepts-and-tooling -->
- [[what-is-a-design-token|Qué es un token de diseño]] — Artículo introductorio que define los tokens de diseño, el Format Module del Design Tokens Community Group del W3C (primera versión estable, octubre de 2025) y la arquitectura de tres niveles primitivo/semántico/componente, fundamentado en el paquete DTCG publicado del Sistema de Diseño PointSav (130 primitivos + 86 de tema, más los pilares separados de papel y escritura).
- [[theming-via-semantic-tokens|Tematización mediante tokens semánticos]] — Los temas claro/oscuro como sustitución de tokens semánticos, fundamentado en el grupo `theme.dark` publicado y el mismo patrón en Carbon, Material 3 y Radix.
- [[component-recipes-vs-raw-tokens|Recetas de componentes frente a tokens en bruto]] — Qué añade el nivel de componentes del Sistema de Diseño PointSav más allá del valor de un token: el formato recipe.json — variantes, marcado, referencias de tokens, CSS, guía ARIA y objetivos WCAG en un solo artefacto legible por máquina — demostrado contra la receta publicada del componente Button y el estado documental real del registro (53 componentes: 20 con documentación completa, 33 con receta más al menos un documento de uso).
- [[design-tokens-and-accessibility|Tokens de diseño y conformidad de accesibilidad]] — Cómo el Sistema de Diseño PointSav expresa los requisitos de accesibilidad — objetivos táctiles mínimos, color del anillo de foco, relaciones de contraste — como tokens de diseño con nombre, de modo que la conformidad WCAG se aplica por la estructura del grafo de tokens en lugar de verificarse ad hoc por componente, demostrado contra la especificación de accesibilidad del componente Button ya publicada.
- [[figma-tokens-studio-integration|Figma y Tokens Studio]] — Explica cómo los diseñadores incorporan a Figma la exportación de tokens DTCG publicada por el Sistema de Diseño PointSav mediante la sincronización por URL del plugin Tokens Studio — una lectura de solo consulta desde el propio JSON alojado por el sistema, sin paso de exportación/importación — y por qué la dirección de solo lectura es una característica de gobernanza, con una comparación honesta con el soporte nativo de tokens de Penpot.
- [[mcp-ai-agent-consumable-design-systems|MCP y sistemas de diseño consumibles por agentes de IA]] — Explica por qué el Sistema de Diseño PointSav expone una superficie legible por máquinas — un punto de conexión Model Context Protocol alojado en la propia infraestructura, una API de búsqueda de tokens y una exportación de tokens DTCG — para que los agentes de codificación de IA consulten datos actuales de tokens y componentes desde el mismo registro que genera la documentación para lectores humanos, sin que ninguna consulta salga de la infraestructura del anfitrión.
- [[registry-driven-releases|Versiones dirigidas por registro]] — Explica la arquitectura dirigida por registro detrás de las versiones del sitio del sistema de diseño: la navegación, las estadísticas de la portada, el punto de acceso de registro legible por máquina, las respuestas MCP y el empaquetado de versiones se resuelven todos contra un único archivo de registro, de modo que no pueden divergir — ilustrado con dos defectos reales de la propia historia del sistema, no con hipótesis.
- [[self-hosting-customer-controlled-design-systems|Autoalojar un sistema de diseño]] — Explica las dos ofertas diferenciadas del Sistema de Diseño PointSav — usar directamente los datos de tokens bajo Apache-2.0, que no requiere nada, y por separado autoalojar el motor de publicación para operar el sistema de diseño propio y distinto de otra organización — incluyendo el procedimiento real de bifurcación en cinco pasos, la superficie de configuración de tres variables, la gobernanza basada en git y los límites precisos de licencia entre datos de tokens, código del servidor y texto del artículo.
<!-- END AUTO-GENERATED -->

## Superficie de marca

Cómo se codifica la identidad de marca como familias de color y pilas tipográficas en las superficies de producto PointSav y Woodfine.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: brand-surface -->
- [[brand-family-swatch|Familias de color de marca]] — Las familias de color de marca asignadas a categorías de anclaje minoristas e institucionales en la superficie GIS de co-ubicación de la plataforma, proporcionando identificadores codificados por color consistentes para visualización de mapas y datos tabulares en modos de visualización accesible y estándar.
- [[brand-typography|Tipografía de marca]] — Las superficies web de PointSav se renderizan en Inter, Source Serif 4 y Playfair Display, alojadas localmente en vez de depender de la pila de fuentes del sistema. Existe una matriz tipográfica OFL de impresión documentada por separado, sin canal de generación aún implementado.
<!-- END AUTO-GENERATED -->

## Diseño de superficie wiki

El vocabulario de componentes, sistema tipográfico y paleta de modo oscuro que componen la superficie de lectura de `documentation.pointsav.com`.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: wiki-surface-design -->
- [[wiki-component-library|Biblioteca de componentes wiki]] — El armazón compartido — encabezado, navegación móvil fuera de lienzo, barra lateral izquierda y pie de página — más las plantillas de página que envuelve, que juntas renderizan cada página de la plataforma de conocimiento de PointSav.
- [[wiki-typography-system|Sistema tipográfico wiki]] — Pila tipográfica Inter y Source Serif 4, escala de encabezados y tokens de espaciado para el wiki de PointSav.
- [[wiki-dark-mode|Modo oscuro wiki]] — Esquemas de color claro y oscuro para el wiki de PointSav, controlados por anulaciones de tokens semánticos sobre un atributo data-theme, con persistencia de tema mediante localStorage.
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

- [Bloques de Construcción](/substrate/) — el marco de sustrato del sistema de diseño junto con los otros sustratos de mecanismos fundacionales
- [Patrones de Diseño](/patterns/) — patrones de diseño nombrados que el sistema de diseño codifica en la capa de interfaz
- [Aplicaciones](/applications/) — aplicaciones orientadas al operador que consumen el sistema de diseño a través de las capas de tokens y componentes
