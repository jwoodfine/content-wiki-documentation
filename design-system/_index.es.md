---
schema: foundry-doc-v1
title: "Sistema de Diseño"
slug: _index
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: _index.md
---

El sustrato de sistema de diseño de PointSav es un motor de sistema de diseño auto-alojado y de propiedad del cliente. Entrega un vocabulario completo de tokens, una biblioteca de recetas de componentes y una guía de voz editorial en una bóveda versionada en Git que el cliente posee en su totalidad.

El sustrato atiende tres tipos de consumidores desde la misma bóveda: agentes de IA que consultan el endpoint MCP en tiempo de generación de código, herramientas de diseño que sincronizan el paquete de tokens DTCG, y diseñadores humanos que leen la investigación de componentes.

## Elementos de fundación

La capa de fundación define los cinco primitivos sobre los que se construye toda superficie.

- [[design-color]] — modelo de color de tres capas (primitivo, semántico, componente) con cinco familias de color y garantías de contraste WCAG 2.2 AAA.
- [[design-typography]] — escalas tipográficas Utility y Display; Inter como tipografía canónica; cadena de respaldo del sistema.
- [[design-spacing]] — escala de espaciado de 13 pasos sobre base de 16 px.
- [[design-motion]] — cuatro curvas de easing y seis pasos de duración; `prefers-reduced-motion` respetado incondicionalmente.

## Investigación de diseño

- [[design-philosophy]] — por qué existe el sustrato; tres inversiones estructurales del patrón de plataformas enterprise.
- [[design-primitive-vocabulary]] — justificación del vocabulario; qué preservó el sustrato de la convención del campo y qué reemplazó.

## Guías de componentes

Guías de uso para componentes individuales — recetas HTML+CSS+ARIA, referencias de tokens y requisitos de accesibilidad para cada uno.

- [[guide-component-badge]]
- [[guide-component-breadcrumb]]
- [[guide-component-button]]
- [[guide-component-checkbox]]
- [[guide-component-citation-authority-ribbon]]
- [[guide-component-freshness-ribbon]]
- [[guide-component-home-grid]]
- [[guide-component-input-text]]
- [[guide-component-link]]
- [[guide-component-navigation-bar]]
- [[guide-component-notification]]
- [[guide-component-research-trail-footer]]
- [[guide-component-select]]
- [[guide-component-surface]]
- [[guide-component-switch]]
- [[guide-component-tab]]
