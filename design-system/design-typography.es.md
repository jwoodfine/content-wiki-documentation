---
schema: foundry-doc-v1
title: "Sistema de Diseño — Tipografía"
slug: design-typography
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-typography.md
cites:
  - wcag-22
  - dtcg-spec
## Véase también

- [[design-color]]
- [[design-spacing]]
- [[design-philosophy]]

---

Dos escalas tipográficas — Utility y Display — dividen la carga tipográfica entre el texto funcional de la interfaz y las superficies expresivas.

## Las dos escalas

La escala **Utility** cubre el texto de interfaz: cuerpo, etiquetas, descripciones, celdas de tabla, etiquetas de botones (4 pasos: 12/14/16/16-bold). La escala **Display** cubre la tipografía expresiva: subtítulos, encabezados de sección, títulos de página, hero (4 pasos: 20/24/32/42).

La separación es estructural, no decorativa. El texto Utility utiliza interletrado optimizado para legibilidad en pantalla a tamaños pequeños; el texto Display utiliza interletrado negativo para un ritmo de encabezado más ajustado y confiado. Mezclar escalas rompe la jerarquía visual del sistema.

## Tipografía canónica

El sustrato incluye Inter como tipografía sans-serif canónica, con una cadena de respaldo del sistema operativo. Inter es una tipografía de código abierto (SIL OFL 1.1), optimizada para renderizado de interfaz a tamaños pequeños. La cadena de respaldo garantiza que el sustrato sea completamente funcional incluso si el archivo Inter no está cargado — la degradación es elegante.

Un tema de cliente puede sustituir cualquier familia tipográfica en la capa primitiva. El alojamiento del archivo tipográfico es responsabilidad del cliente; el sustrato referencia la familia por nombre.

## Jerarquía de encabezados

Un salto de nivel de encabezado (h1 → h3 sin h2 entre ellos) rompe la accesibilidad — los lectores de pantalla dependen de la jerarquía para navegar. El sustrato aplica esta regla en el trabajo de auditoría de hitos posteriores.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
