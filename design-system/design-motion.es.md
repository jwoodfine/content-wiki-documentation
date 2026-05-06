---
schema: foundry-doc-v1
title: "Sistema de Diseño — Movimiento"
slug: design-motion
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-motion.md
cites:
  - wcag-22
  - dtcg-spec
## Véase también

- [[design-spacing]]
- [[design-color]]
- [[design-philosophy]]

---

El movimiento comunica causalidad. El sustrato incluye cuatro curvas de easing y seis pasos de duración. Se combinan según la clase de interacción.

## Principio de diseño

Las curvas productivas están diseñadas para duraciones cortas (≤200 ms): `ease-utility` para interacciones productivas — botones, inputs, pestañas. Las curvas expresivas funcionan a duraciones más largas (≥320 ms): `ease-display` para interacciones expresivas — toasts, modales, hero.

Los seis pasos de duración cubren desde 70 ms (imperceptible — hover de color) hasta 720 ms (deliberado — animación de hero). Los valores fuera de escala (350 ms, 500 ms) rompen el ritmo.

## Respeto por el movimiento reducido

`prefers-reduced-motion: reduce` se respeta en todas las capas de interacción. Las recetas de componentes incluyen la sobreescritura de media query; los consumidores la heredan. No se omite la sobreescritura — los usuarios sensibles al movimiento han optado explícitamente por no participar.

Este no es un detalle de implementación secundario: es un requisito de accesibilidad estructural. Los sistemas que bypassean `prefers-reduced-motion` crean barreras para usuarios con vestibular sensibilities, epilepsia fotosensible, y otras condiciones.

## Anti-patrones

- Animaciones que bloquean la entrada del usuario. La entrada modal es `speed-5` para lo visual; el foco se mueve de inmediato en duración 0.
- Movimiento decorativo que añade tiempo a una tarea productiva.
- Duraciones fuera de escala. La escala de 6 pasos cubre cada clase de interacción.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
