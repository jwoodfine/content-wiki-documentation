---
schema: foundry-doc-v1
title: "Filosofía del sistema de diseño"
slug: design-philosophy
short_description: "El sistema de diseño PointSav es un sustrato auto-alojado propiedad del cliente que se ejecuta en design.pointsav.com y publica investigación de decisiones de diseño junto con valores de tokens en formato DTCG, priorizando interoperabilidad agnóstica respecto a editores y rationale estructurado."
category: design-system
type: reference
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
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

El sustrato responde con tres inversiones estructurales:

1. **Propiedad del cliente** sobre alojamiento en plataforma. El sistema de diseño vive en el repositorio Git del cliente — la migración tiene un costo tendiente a cero.
2. **La investigación como canónica** en lugar de como marketing. El POR QUÉ vive en la misma bóveda que el QUÉ, en el mismo nivel de legibilidad por máquinas, accesible a través del mismo endpoint MCP.
3. **Neutralidad de editor** en lugar de dependencia de editor. El formato DTCG es el denominador común: cualquier editor compatible produce contenido que el sustrato acepta.

En la era de la IA 2026–2030, el sustrato de sistema de diseño de una pyme es un medio: su forma — legibilidad por máquinas, interoperabilidad sin dependencia de editor, auto-alojamiento, investigación consumible por IA — determina cómo la marca de la pyme llega a cada superficie orientada al cliente.

## Diseño móvil primero y fundación Inter

Cada superficie de operador que renderiza el sistema de diseño está especificada con enfoque móvil primero. La maquetación, la navegación y los componentes interactivos se definen a 375 px antes de la mejora progresiva para ventanas más amplias. Los objetivos táctiles cumplen el SC 2.5.8 de las WCAG 2.2 — mínimo 44 px × 44 px — y las interacciones no dependen de estados hover. Se aplica relleno de zona segura (`env(safe-area-inset-*)`) al cromo de la interfaz para pantallas con muesca y dynamic island.

La fundación tipográfica de interfaz es **Inter** (SIL OFL 1.1) — una neo-grotesca mantenida por la comunidad, diseñada específicamente para legibilidad en pantalla, sin asociación de marca corporativa. Inter es el resultado práctico de elegir neutralidad de editor en tipografía: es la tipografía más interoperable, ampliamente disponible y optimizada para pantalla que ninguna plataforma posee. Véase [[wiki-typography-system]] para la pila tipográfica completa de la superficie wiki (Inter + Source Serif 4 + mono del sistema).

## Véase también

- [[design-primitive-vocabulary]] — la capa de vocabulario de tokens: escalas de color numéricas, alias semántico y justificación de nomenclatura original de PointSav
- [[design-system-substrate]] — la arquitectura del sustrato: bóveda rastreada en Git, endpoint MCP y estructura de anulación multitenant
- [[wiki-component-library]] — nueve componentes del wiki construidos sobre este sistema de tokens
- [[app-mediakit-knowledge]] — el motor wiki que renderiza la superficie pública del sistema de diseño

