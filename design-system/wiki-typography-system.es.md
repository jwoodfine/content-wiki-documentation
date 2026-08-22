---
schema: foundry-doc-v1
title: "Sistema tipográfico del wiki"
slug: wiki-typography-system
short_description: "Pila tipográfica Inter y Source Serif 4, escala de encabezados y tokens de espaciado para el wiki de PointSav."
category: design-system
type: topic
content_type: topic
index_group: wiki-surface-design
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-01
editor: pointsav-engineering
paired_with: wiki-typography-system.md
---

El sistema tipográfico del [[app-mediakit-knowledge|wiki de PointSav]] usa Source Serif 4 para el título del artículo y los encabezados de sección, Inter para la prosa de lectura continua, y una pila monoespaciada del sistema para el código y la notación técnica, construido sobre [[design-system-substrate|el sistema de tokens de la plataforma]] conforme a las [[design-primitive-vocabulary|convenciones del vocabulario primitivo]]. Este artículo explica las elecciones tipográficas, la escala de encabezados, los tokens de espaciado y cómo el sistema logra una cobertura lingüística amplia para el contenido bilingüe (inglés/español).

---

## Pila tipográfica

**Título del artículo y encabezados de sección:** Source Serif 4 (fuente variable). Source Serif 4 es la tipografía de texto de código abierto de Adobe, publicada bajo la SIL Open Font License 1.1 (SIL OFL 1.1), que permite su uso, modificación y redistribución sin restricciones. Su contraste de trazo ligeramente superior al de una sans-serif le da al título y a los encabezados un registro distinto del texto corrido que los acompaña.

**Prosa de lectura continua:** Inter (fuente variable). Inter es una tipografía de código abierto comunitario diseñada por Rasmus Andersson, publicada bajo SIL OFL 1.1. Es una neo-grotesca diseñada específicamente para la legibilidad en pantalla, con alta claridad a tamaños reducidos y diferenciación explícita entre glifos frecuentemente confundidos (l, 1, I; O, 0). No tiene asociación de marca corporativa y es la tipografía de interfaz de referencia en el campo de los sistemas de diseño actuales.

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

| Nivel | Token | rem | px | Uso |
|---|---|---|---|---|
| H1 | `--k-title-fs` | 2,125 rem | 34 px | Título del artículo |
| H2 | `--k-h2-fs` | 1,5 rem | 24 px | Sección principal |
| H3 | `--k-h3-fs` | 1,2 rem | 19 px | Subsección |
| H4 | (sin nombre, fijado directamente) | 1,05 rem | 16,8 px | Encabezado menor |
| Cuerpo | `--k-prose-fs` | 1 rem | 16 px | Prosa corrida |

El tamaño base del cuerpo es el predeterminado de 16 px del navegador. Los encabezados se renderizan en Source Serif 4 (`--k-title-font`); la prosa del cuerpo se renderiza en Inter (`--k-prose-font`).

---

## Medida de lectura y altura de línea

| Propiedad | Valor | Token |
|---|---|---|
| Medida (max-width) | 44 rem (~72 car.) | `--k-prose-measure` |
| Altura de línea (cuerpo) | 1,6 | `--k-prose-leading` |

Una medida amplia mantiene la columna de lectura a todo el ancho en la maquetación estilo Wikipedia, en vez de angostarla artificialmente. Una altura de línea de 1,6 a 16 px de base produce 25,6 px de interlineado.

---

## Tokens CSS

Todos los valores son propiedades personalizadas CSS definidas en la hoja de tokens del motor:

```css
--k-font-sans:  'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
--k-font-serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
--k-font-mono:  ui-monospace, 'SFMono-Regular', 'Menlo', 'Consolas', monospace;

--k-prose-font:  var(--k-font-sans);
--k-title-font:  var(--k-font-serif);
--k-code-font:   var(--k-font-mono);

--k-prose-fs:      1rem;      /* 16px cuerpo */
--k-title-fs:      2.125rem;  /* 34px h1 */
--k-h2-fs:         1.5rem;    /* 24px */
--k-h3-fs:         1.2rem;    /* 19px */
--k-prose-leading: 1.6;
--k-prose-measure: 44rem;     /* ~72 car. */
```

---

## Véase también

- [[wiki-component-library]] — los nueve componentes del wiki que utilizan esta pila tipográfica
- [[wiki-dark-mode]] — el sistema de esquemas de color que se combina con estos tokens tipográficos
- [[design-system-substrate]] — la bóveda de tokens donde se definen las variables de pila tipográfica y escala
