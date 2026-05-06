---
schema: foundry-doc-v1
title: "Sistema de Diseño — Espaciado"
slug: design-spacing
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-spacing.md
cites:
  - dtcg-spec
## Véase también

- [[design-color]]
- [[design-typography]]
- [[design-motion]]

---

Una escala de espaciado de 13 pasos sobre una base de 16 px. Numérico — `space-1` hasta `space-13` — proporciona una respuesta canónica para cada decisión de diseño.

## Principio de composición

La escala cubre desde 2 px (separación de borde, `space-1`) hasta 160 px (espaciado exclusivo de hero, `space-13`). Cada medida intermedia tiene un propósito definido: `space-5` (16 px) es la unidad de cuadrícula del cuerpo y el relleno predeterminado del contenedor; `space-6` (24 px) cubre el relleno de tarjeta y el ritmo vertical entre secciones; `space-7` (32 px) define el margen de sección.

La regla de composición es estricta: se compone el espaciado mayor a partir de la escala, nunca se inventan valores fuera de ella. Los valores fuera de escala (5 px, 14 px, 22 px) rompen el ritmo y se acumulan como deriva. La escala de 13 pasos es lo suficientemente densa como para cubrir todas las necesidades de diseño sin recurrir a valores arbitrarios.

## Base de cuadrícula

El sustrato utiliza una cuadrícula de línea base de 16 px (`space-5`). El texto del cuerpo y los encabezados se alinean a múltiplos de 16 px en su cálculo de altura de línea; el relleno del contenedor se alinea a múltiplos de 16 px en el eje en línea. Esto es estructural: garantiza que el ritmo vertical permanezca consistente entre superficies.

Esta disciplina es lo que distingue un sistema de diseño maduro de una colección de estilos: el espaciado no es una decisión casual sino una consecuencia calculada del sistema.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
