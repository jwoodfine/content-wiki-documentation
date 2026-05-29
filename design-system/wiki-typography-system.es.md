---
schema: foundry-doc-v1
title: "Sistema tipográfico del wiki"
slug: wiki-typography-system
short_description: "Pila tipográfica IBM Plex Sans e IBM Plex Mono, escala de encabezados y tokens de espaciado para el wiki de PointSav."
category: design-system
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wiki-typography-system.md
---

# Sistema tipográfico del wiki

El sistema tipográfico del [[app-mediakit-knowledge|wiki de PointSav]] usa IBM Plex Sans para la prosa principal e IBM Plex Mono para el código y la notación técnica, construido sobre [[design-system-substrate|el sistema de tokens de la plataforma]] conforme a las [[design-primitive-vocabulary|convenciones del vocabulario primitivo]]. Este artículo explica la elección tipográfica, la escala de encabezados, los tokens de espaciado y cómo el sistema logra una cobertura lingüística amplia para el contenido bilingüe (inglés/español).

---

## Pila tipográfica

**Prosa principal:** IBM Plex Sans (pesos 400, 500, 600, 700). IBM Plex Sans es la tipografía de código abierto de IBM, publicada bajo la SIL Open Font License 1.1 (SIL OFL 1.1), que permite su uso, modificación y redistribución sin restricciones. Es una sans-serif humanista con alta legibilidad a tamaños de lectura y diferenciación clara entre glifos frecuentemente confundidos (l, 1, I; O, 0).

**Código y notación técnica:** IBM Plex Mono (pesos 400, 500). Tipografía monoespaciada diseñada como complemento de IBM Plex Sans. Se usa para `código` en línea, bloques de código, ejemplos de línea de comandos y campos de metadatos (fechas, identificadores).

**Pila de respaldo:** -apple-system, BlinkMacSystemFont, Segoe UI, Roboto (cadena sans-serif del sistema) para el cuerpo; SFMono-Regular, Consolas, Liberation Mono para el código.

---

## Distribución

IBM Plex Sans e IBM Plex Mono están disponibles a través de Google Fonts, el paquete npm `@ibm/plex` y descarga directa desde el repositorio de IBM Plex en GitHub.

IBM Plex Sans incluye un archivo de fuente variable (`IBM-Plex-Sans-Variable.woff2`) que cubre el eje completo de pesos (100–700). Un único archivo de fuente variable reemplaza a cuatro archivos WOFF2 de peso estático, con un tamaño aproximado de 60–80 KB para el subconjunto latino.

**El alojamiento propio** desde el directorio `/static/fonts/` del despliegue es el método preferido. No se realizan solicitudes a redes de distribución de contenido externas, lo que protege la privacidad de los lectores. El subconjunto latino es el mínimo; el subconjunto latin-ext, necesario para el contenido bilingüe en español, añade aproximadamente un 10–20% al tamaño del archivo.

**`font-display: swap`** evita el texto invisible durante la carga de la fuente. La fuente del sistema de respaldo se renderiza de inmediato; IBM Plex reemplaza cuando finaliza la descarga.

---

## Escala tipográfica

| Nivel | Token | rem | px (base 17 px) | Uso |
|---|---|---|---|---|
| H1 | `--ps-wiki-text-h1` | 2,25 rem | 38 px | Título del artículo |
| H2 | `--ps-wiki-text-h2` | 1,75 rem | 29,75 px | Sección principal |
| H3 | `--ps-wiki-text-h3` | 1,375 rem | 23,375 px | Subsección |
| H4 | `--ps-wiki-text-h4` | 1,125 rem | 19,125 px | Encabezado menor |
| Cuerpo | `--ps-wiki-font-size-base` | 1,0625 rem | 17 px | Prosa corrida |

**Base:** 106,25% de tamaño de fuente raíz (17 px) — ligeramente mayor que el valor predeterminado del navegador de 16 px, para mejorar la legibilidad en una medida de 65 caracteres en escritorio.

---

## Medida de lectura y altura de línea

| Propiedad | Valor | Token |
|---|---|---|
| Medida (max-width) | 65 ch | `--ps-wiki-measure` |
| Altura de línea (cuerpo) | 1,6 | `--ps-wiki-line-height-body` |

65 caracteres por línea es el óptimo tipográfico para lectura sostenida. Una altura de línea de 1,6 a 17 px de base produce 27,2 px de interlineado, igualando el ritmo de espaciado del cuerpo de texto de Wikipedia.

---

## Tokens CSS

Todos los valores son propiedades personalizadas CSS definidas en `:root` dentro de `dist/tokens.css`:

```css
--ps-wiki-font-body: 'IBM Plex Sans', -apple-system, …;
--ps-wiki-font-mono: 'IBM Plex Mono', 'SFMono-Regular', …;
--ps-wiki-font-size-base:   1.0625rem;
--ps-wiki-line-height-body: 1.6;
--ps-wiki-measure:          65ch;
--ps-wiki-text-h1: 2.25rem;
--ps-wiki-text-h2: 1.75rem;
--ps-wiki-text-h3: 1.375rem;
--ps-wiki-text-h4: 1.125rem;
```

---

## Véase también

- [[wiki-component-library]] — los nueve componentes que utilizan esta pila tipográfica
- [[wiki-dark-mode]] — el sistema de esquemas de color que se combina con estos tokens tipográficos
- [[design-system-substrate]] — la bóveda de tokens donde se definen las variables de pila tipográfica y escala
