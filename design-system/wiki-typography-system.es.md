---
schema: foundry-doc-v1
title: "Sistema Tipográfico del Wiki"
slug: wiki-typography-system
language: es
category: design-system
type: topic
quality: core
status: active
bcsc_class: vendor-public
last_edited: 2026-05-07
editor: pointsav-engineering
paired_with: wiki-typography-system.md
---

El sistema tipográfico del wiki PointSav emplea IBM Plex Sans para texto de prosa e
IBM Plex Mono para código y notación técnica. Ambas tipografías se distribuyen bajo la
Licencia de Fuente Abierta SIL 1.1, que permite uso, modificación y redistribución sin
restricciones. Una pasada de investigación de 24 agentes (2026-05-06) estableció la
escala de encabezados, el tamaño base y la medida de línea; todos los pares de contraste
superan WCAG 2.1 AAA.

## Pila tipográfica

**Prosa:** IBM Plex Sans, serif humanista con alta legibilidad a tamaños de lectura y
diferenciación clara entre glifos frecuentemente confundidos (l, 1, I; O, 0). Pesos
disponibles: 400, 500, 600, 700.

**Código y notación técnica:** IBM Plex Mono, compañero monoespaciado proporcional de
IBM Plex Sans. Se usa en fragmentos de código en línea, bloques de código, ejemplos de
línea de comandos y campos de metadatos.

El wiki aloja las fuentes localmente en `/static/fonts/`, sin solicitudes a CDNs externos.
El subconjunto `latin-ext` incluye caracteres acentuados para el contenido bilingüe.

## Escala tipográfica

| Nivel | Token | rem | px (base 17px) | Uso |
|---|---|---|---|---|
| H1 | `--ps-wiki-text-h1` | 2,25rem | 38px | Título de artículo |
| H2 | `--ps-wiki-text-h2` | 1,75rem | 29,75px | Sección principal |
| H3 | `--ps-wiki-text-h3` | 1,375rem | 23,375px | Subsección |
| H4 | `--ps-wiki-text-h4` | 1,125rem | 19,125px | Encabezado menor |
| Cuerpo | `--ps-wiki-font-size-base` | 1,0625rem | 17px | Prosa continua |

La base de 17px (106,25% de la raíz) produce la longitud de línea correcta a la medida
de 65 caracteres en escritorio. La interlineación de 1,6 a 17px da 27,2px de leading,
equiparando el ritmo de espaciado del texto cuerpo de Wikipedia.

## Véase también

- [[wiki-dark-mode]]
- [[wiki-component-library]]
- [[design-typography]]
