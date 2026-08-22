---
schema: foundry-doc-v1
title: "Filosofía del sistema de diseño"
slug: design-philosophy
short_description: "El sistema de diseño PointSav es un sustrato auto-alojado propiedad del cliente que se ejecuta en design.pointsav.com y publica investigación de decisiones de diseño junto con valores de tokens en formato DTCG, priorizando interoperabilidad agnóstica respecto a editores y rationale estructurado."
category: design-system
type: reference
content_type: topic
quality: complete
index_group: philosophy-and-primitive-vocabulary
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: design-philosophy.md
cites:
 - wcag-22
 - dtcg-spec
 - doctrine-38
---

El [[design-system-substrate|sistema de diseño]] de PointSav es un sustrato auto-alojado de propiedad del cliente para gestionar tokens de diseño, componentes e investigación de decisiones de diseño. Responde a cuatro brechas estructurales en el panorama del diseño de 2026 — la ausencia de justificación de diseño legible por máquinas, precios de nivel empresarial que excluyen a las pequeñas y medianas empresas (PyMES), la dependencia de editores específicos y la estructura insuficiente para el consumo por inteligencia artificial — mediante tres inversiones arquitectónicas del modelo de plataforma dominante. El vocabulario de tokens está documentado en [[design-primitive-vocabulary|el vocabulario primitivo del sistema de diseño]]; la superficie wiki construida sobre este sustrato es servida por [[app-mediakit-knowledge]].

El sustrato de sistema de diseño de PointSav existe como respuesta directa a cuatro brechas estructurales en el panorama del diseño de 2026.

Los sistemas de diseño establecidos publican únicamente el QUÉ: valores de tokens y formas de componentes. Ninguno publica la investigación de decisiones de diseño — el POR QUÉ — en un formato que un agente de IA o un desarrollador en una nueva organización pueda leer en tiempo de generación de código. Las plataformas SaaS de gestión de sistemas de diseño cobran precios para empresas de más de 5.000 empleados, dejando a las pymes sin alternativas. Cada editor de diseño construye para retener al cliente dentro de su plataforma. Y el 77% de los sistemas de diseño no están estructurados para el consumo de IA en 2026.

## Qué hace el sustrato

El sustrato lleva cinco elementos por inquilino, en una bóveda rastreada en Git que el cliente posee:

- **`tokens/`** — tokens de diseño en formato DTCG. Capa primitiva (familias de color originales de PointSav, escala tipográfica, espaciado, movimiento, anillo de foco — patrones estructurales alineados con el campo moderno de sistemas de diseño, valores hexadecimales y nombres de familia propios de PointSav), capa semántica (interactive-primary, surface-elevated, ...), capa de componentes.
- **`components/`** — archivos de receta HTML+CSS+ARIA. Agnósticos al framework; el framework elegido por el cliente consume la receta, no al revés.
- **`themes/<marca>/`** — capas de anulación por inquilino que redirigen las referencias semánticas hacia las primitivas.
- **`research/`** — justificación de decisiones de diseño legible por IA, justificaciones de accesibilidad, reglas de voz de marca, antipatrones.
- **`exports/`** — cachés derivados (JSON de Variables de Figma, configuración de Tailwind, variables CSS, builds de Style Dictionary). Recalculables a partir de los cuatro directorios canónicos anteriores.

El motor del sustrato (`app-privategit-design`) lee esta bóveda y la sirve como un showcase público, un paquete DTCG, una superficie de investigación legible por IA y un servidor de Model Context Protocol (MCP). Los agentes de IA consultan el endpoint MCP en tiempo de generación de código; las herramientas de diseño consultan el paquete de tokens exportado para la sincronización con el editor; las personas leen el showcase.

El sustrato responde con tres inversiones estructurales:

1. **Propiedad del cliente** sobre alojamiento en plataforma. El sistema de diseño vive en el repositorio Git del cliente — la migración tiene un costo tendiente a cero.
2. **La investigación como canónica** en lugar de como marketing. El POR QUÉ vive en la misma bóveda que el QUÉ, en el mismo nivel de legibilidad por máquinas, accesible a través del mismo endpoint MCP.
3. **Neutralidad de editor** en lugar de dependencia de editor. El formato DTCG es el denominador común: cualquier editor compatible produce contenido que el sustrato acepta.

En la era de la IA 2026–2030, el sustrato de sistema de diseño de una pyme es un medio: su forma — legibilidad por máquinas, interoperabilidad sin dependencia de editor, auto-alojamiento, investigación consumible por IA — determina cómo la marca de la pyme llega a cada superficie orientada al cliente.

## Diseño móvil primero y fundación Inter

Cada superficie de operador que renderiza el sistema de diseño está especificada con enfoque móvil primero. La maquetación, la navegación y los componentes interactivos se definen a 375 px antes de la mejora progresiva para ventanas más amplias. Los objetivos táctiles cumplen el SC 2.5.8 de las WCAG 2.2 — mínimo 44 px × 44 px — y las interacciones no dependen de estados hover. Se aplica relleno de zona segura (`env(safe-area-inset-*)`) al cromo de la interfaz para pantallas con muesca y dynamic island.

La fundación tipográfica de interfaz es **Inter** (SIL OFL 1.1) — una neo-grotesca mantenida por la comunidad, diseñada específicamente para legibilidad en pantalla, sin asociación de marca corporativa. Inter es el resultado práctico de elegir neutralidad de editor en tipografía: es la tipografía más interoperable, ampliamente disponible y optimizada para pantalla que ninguna plataforma posee. Véase [[wiki-typography-system]] para la pila tipográfica completa de la superficie wiki (Inter + Source Serif 4 + mono del sistema).

## Antipatrones que el sustrato rechaza

- Integración con Storybook (renderizador paralelo; el sustrato es dueño del renderizado).
- Dependencia de SaaS de sistemas de diseño de nivel empresarial.
- Componentes atados a un framework JS (las recetas HTML+CSS+ARIA son la forma canónica).
- Empaquetado en contenedores (según [[zero-container-runtime]]).
- Dependencia de editor (se rechazan las funciones exclusivas de un solo editor).
- Vocabulario de marketing en los archivos de investigación (los archivos de investigación describen justificación estructural, no posicionamiento de producto).

## Véase también

- [[what-is-a-design-token|Qué es un token de diseño]] — comience aquí para una definición introductoria de un token de diseño antes de este argumento arquitectónico
- [[design-primitive-vocabulary]] — la capa de vocabulario de tokens: escalas de color numéricas, alias semántico y justificación de nomenclatura original de PointSav
- [[design-system-substrate]] — la arquitectura del sustrato: bóveda rastreada en Git, endpoint MCP y estructura de anulación multitenant
- [[wiki-component-library]] — nueve componentes del wiki construidos sobre este sistema de tokens
- [[app-mediakit-knowledge]] — el motor wiki que renderiza la superficie pública del sistema de diseño
- [[design-tokens-and-accessibility|Tokens de diseño y conformidad de accesibilidad]] — cómo se aplican estructuralmente como tokens los requisitos de accesibilidad, en lugar de verificarse ad hoc
- [[self-hosting-customer-controlled-design-systems|Autoalojar un sistema de diseño]] — la oferta separada para que otra organización autoaloje este motor de servicio para su propio sistema de diseño

## Referencias

- Formato del W3C Design Tokens Community Group — https://design-tokens.github.io/community-group/format/
- WCAG 2.2 (piso de accesibilidad) — https://www.w3.org/TR/WCAG22/
- Marshall McLuhan, *Understanding Media: The Extensions of Man* (1964), cap. 1 "The Medium is the Message"

