---
schema: foundry-doc-v1
title: "Sistema de Diseño — Justificación del Vocabulario Primitivo"
slug: design-primitive-vocabulary
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-primitive-vocabulary.md
cites:
  - wcag-22
  - dtcg-spec
  - doctrine-38
## Véase también

- [[design-philosophy]]
- [[design-color]]
- [[design-typography]]

---

La capa de tokens primitivos del sustrato preserva cuatro patrones estructurales en los que el campo moderno de sistemas de diseño ha convergido (2018–2026): escalas de color numéricas, capas primitivo → semántico → componente, la división de tipografía productiva vs expresiva, y escalas de espaciado numéricas de ~12–15 pasos.

Estos patrones no son propiedad intelectual de ningún sistema de diseño en particular — son el vocabulario compartido del campo. Re-implementarlos es la elección arquitectónica correcta para cualquier sistema de diseño de 2026 que quiera que los profesionales lo adopten sin necesidad de re-aprender lo básico.

## Lo que el sustrato reemplazó

El sustrato utiliza vocabulario, valores hexadecimales, elecciones tipográficas y contenido originales de PointSav. Los nombres de las familias de color describen el rol en lugar de la familia cromática — los clientes que cambian su marca de azul a verde azulado no tienen que renombrar los tokens. Los valores hexadecimales son propios de PointSav, evitando entrelazamiento de IP. La tipografía canónica es Inter (código abierto, SIL OFL 1.1) en lugar de una tipografía asociada a una empresa específica — sin asociación de marca corporativa.

## Por qué importa la memoria muscular

Un diseñador o desarrollador que llega de cualquier entorno de sistema de diseño moderno reconoce los patrones estructurales del sustrato en segundos: escala de color numérica, capas DTCG, dos pistas tipográficas. Este reconocimiento es la rampa cognitiva de entrada. Es la mayor ventaja libre del sustrato — un profesional se adapta en días, no en semanas.

## Por qué importa el vocabulario

Un token nombrado por familia cromática con los valores exactos de un proveedor específico pone al sustrato a un litigio de marcas de distancia de un rediseño. Un token nombrado por rol con valores elegidos por PointSav, no.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
