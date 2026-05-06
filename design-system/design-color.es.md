---
schema: foundry-doc-v1
title: "Sistema de Diseño — Color"
slug: design-color
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-color.md
cites:
  - wcag-22
  - dtcg-spec
## Véase también

- [[design-typography]]
- [[design-spacing]]
- [[design-philosophy]]

---

El sistema de color del sustrato tiene tres capas: primitiva, semántica y de componente. La marca de cada cliente vive en la capa semántica; los primitivos son estables entre clientes; los componentes referencian semánticas, nunca primitivos directamente.

## Modelo de tres capas

Un cliente que quiere que su acción principal sea verde azulado en lugar de azul sobreescribe únicamente la capa semántica:

```json
"interactive-primary": { "$value": "{color.brand-teal-60}" }
```

Los componentes no cambian. Los primitivos no cambian. La sobreescritura se propaga a través de cada consumidor de `interactive-primary`.

## Familias primitivas

El sustrato incluye cinco familias de color en la capa primitiva. Los nombres son genéricos — describen el rol, no el significado de negocio:

- **Neutral** — Fondos, bordes, tinta, divisores
- **Primary** — El color interactivo más prominente del cliente
- **Positive** — Estado exitoso, retroalimentación positiva
- **Caution** — Problemas reversibles, estados próximos a expirar
- **Critical** — Fallos, acciones destructivas, errores

Los números indican luminosidad: `10` es el más claro, `90`/`100` es el más oscuro.

## Garantías de contraste WCAG

Las elecciones de primitivos del sustrato garantizan contraste AAA de WCAG 2.2 (7:1) para los pares texto-sobre-superficie canónicos. Un tema de cliente que sobreescriba los primitivos por debajo del nivel AA de WCAG 2.2 falla el endpoint de auditoría (hito posterior). El sustrato aplica el nivel mínimo; el cliente elige todo lo que está por encima de él.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
