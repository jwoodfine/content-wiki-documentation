---
schema: foundry-doc-v1
title: "Sistema tipográfico del wiki"
slug: wiki-typography-system
short_description: "Pila tipográfica Inter y Source Serif 4, escala de encabezados y tokens de espaciado para el wiki de PointSav."
category: design-system
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-01
editor: pointsav-engineering
paired_with: wiki-typography-system.md
---

# Sistema tipográfico del wiki

El sistema tipográfico del [[app-mediakit-knowledge|wiki de PointSav]] usa Inter para los elementos de interfaz de usuario y la navegación, Source Serif 4 para la prosa de lectura continua, y una pila monoespaciada del sistema para el código y la notación técnica, construido sobre [[design-system-substrate|el sistema de tokens de la plataforma]] conforme a las [[design-primitive-vocabulary|convenciones del vocabulario primitivo]]. Este artículo explica las elecciones tipográficas, la escala de encabezados, los tokens de espaciado y cómo el sistema logra una cobertura lingüística amplia para el contenido bilingüe (inglés/español).

---

## Pila tipográfica

**Interfaz de usuario y encabezados:** Inter (fuente variable, eje de peso 100–900). Inter es una tipografía de código abierto comunitario diseñada por Rasmus Andersson, publicada bajo la SIL Open Font License 1.1 (SIL OFL 1.1), que permite su uso, modificación y redistribución sin restricciones. Inter es una neo-grotesca diseñada específicamente para la legibilidad en pantalla, con alta claridad a tamaños reducidos y diferenciación explícita entre glifos frecuentemente confundidos (l, 1, I; O, 0). No tiene asociación de marca corporativa y es la tipografía de interfaz de referencia en el campo de los sistemas de diseño actuales.

**Prosa de lectura continua:** Source Serif 4 (fuente variable, eje de peso 200–900). Source Serif 4 es la tipografía de texto de código abierto de Adobe, publicada bajo la SIL Open Font License 1.1. Proporciona una lectura cómoda a una medida de 68 caracteres, con un contraste de trazo ligeramente superior al de Inter que facilita el seguimiento visual a lo largo de líneas de prosa extensa.

**Código y notación técnica:** Pila monoespaciada del sistema — `ui-monospace`, `SFMono-Regular`, `Cascadia Code`, `Consolas`, `Liberation Mono`. No se carga ningún archivo de fuente personalizado para el código. La pila del sistema cubre todas las plataformas principales sin ningún ciclo de red adicional. Se usa para `código` en línea, bloques de código, ejemplos de línea de comandos y campos de metadatos (fechas, identificadores).

**Cadenas de respaldo:** -apple-system, BlinkMacSystemFont, Segoe UI, Roboto (sans-serif del sistema) para contextos de interfaz antes de que Inter cargue; Georgia, Times New Roman (serif del sistema) para contextos de prosa antes de que Source Serif 4 cargue.

---

## Distribución

Inter y Source Serif 4 están disponibles a través de Google Fonts y descarga directa desde sus repositorios respectivos. Ambas tipografías incluyen archivos de fuente variable que cubren el eje de peso completo — un único archivo variable reemplaza a varios archivos de peso estático, reduciendo la carga total.

- **Inter variable** (`inter-var.woff2`) — subconjunto latino aproximadamente 100–130 KB; el subconjunto latin-ext, necesario para el contenido bilingüe en español, añade aproximadamente un 15–20%.
- **Source Serif 4 variable** (`SourceSerif4Variable-Roman.woff2`) — subconjunto latino aproximadamente 80–100 KB; latin-ext añade aproximadamente un 10–20%.

**El alojamiento propio** desde el directorio `/static/fonts/` del despliegue es el método preferido. No se realizan solicitudes a redes de distribución de contenido externas, lo que protege la privacidad de los lectores.

**`font-display: swap`** evita el texto invisible durante la carga de la fuente. La fuente del sistema de respaldo se renderiza de inmediato; Inter y Source Serif 4 reemplazan cuando finalizan sus descargas. Para un wiki con abundante texto, la legibilidad inmediata tiene prioridad sobre el desplazamiento de maquetación por el intercambio de fuentes.

---

## Escala tipográfica

| Nivel | Token | rem | px (base 17 px) | Uso |
|---|---|---|---|---|
| H1 | `--ps-wiki-text-h1` | 2,25 rem | 38 px | Título del artículo |
| H2 | `--ps-wiki-text-h2` | 1,75 rem | 29,75 px | Sección principal |
| H3 | `--ps-wiki-text-h3` | 1,375 rem | 23,375 px | Subsección |
| H4 | `--ps-wiki-text-h4` | 1,125 rem | 19,125 px | Encabezado menor |
| Cuerpo | `--ps-wiki-font-size-base` | 1,0625 rem | 17 px | Prosa corrida |

**Base:** 106,25% de tamaño de fuente raíz (17 px) — ligeramente mayor que el valor predeterminado del navegador de 16 px, para mejorar la legibilidad en una medida de 68 caracteres en escritorio. Los encabezados y etiquetas de navegación se renderizan en Inter; la prosa del cuerpo se renderiza en Source Serif 4.

---

## Medida de lectura y altura de línea

| Propiedad | Valor | Token |
|---|---|---|
| Medida (max-width) | 68 ch | `--ps-wiki-measure` |
| Altura de línea (cuerpo) | 1,6 | `--ps-wiki-line-height-body` |

68 caracteres por línea es el óptimo tipográfico para la lectura sostenida con una tipografía con serifa de peso texto. Una altura de línea de 1,6 a 17 px de base produce 27,2 px de interlineado, igualando el ritmo de espaciado del cuerpo de texto de Wikipedia.

---

## Tokens CSS

Todos los valores son propiedades personalizadas CSS definidas en `:root` dentro de `dist/tokens.css`:

```css
--ps-wiki-font-ui:    'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--ps-wiki-font-prose: 'Source Serif 4', 'Georgia', 'Times New Roman', serif;
--ps-wiki-font-mono:  ui-monospace, 'SFMono-Regular', 'Cascadia Code', 'Consolas',
                      'Liberation Mono', monospace;
--ps-wiki-font-size-base:   1.0625rem;
--ps-wiki-line-height-body: 1.6;
--ps-wiki-measure:          68ch;
--ps-wiki-text-h1: 2.25rem;
--ps-wiki-text-h2: 1.75rem;
--ps-wiki-text-h3: 1.375rem;
--ps-wiki-text-h4: 1.125rem;
```

---

## Véase también

- [[wiki-component-library]] — los nueve componentes del wiki que utilizan esta pila tipográfica
- [[wiki-dark-mode]] — el sistema de esquemas de color que se combina con estos tokens tipográficos
- [[design-system-substrate]] — la bóveda de tokens donde se definen las variables de pila tipográfica y escala
