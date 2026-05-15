---
schema: foundry-doc-v1
title: "Sistema de Diseño — Tipografía"
slug: design-typography
category: design-system
type: reference
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: design-typography.md
cites:
 - wcag-22
 - dtcg-spec
---

El sistema de diseño PointSav organiza cada familia tipográfica del producto en seis familias funcionales y dos activos de marca, dividiendo la carga tipográfica entre dos escalas de renderizado — Utility para texto funcional de interfaz y Display para superficies expresivas. Cada familia se distribuye como un binario autohospedado; ninguna superficie realiza llamadas a servicios tipográficos externos. La fidelidad pantalla-impresión es un requisito regulatorio, no una preferencia estética: un documento firmado debe renderizarse de forma idéntica en 2026 y en 2030. Este artículo cubre las dos escalas, las seis familias, el modelo de empaquetado y el requisito de fidelidad que los sustenta.

## Dos sistemas de diseño, no uno

PointSav opera dos sistemas de diseño. La distinción es estructural:

| Sistema de diseño | Repositorio | Propósito | Audiencia |
|---|---|---|---|
| `pointsav-design-system` | Organización de proveedor `pointsav` | Sustrato de UI/UX para el Libro Mayor de Comandos y toda la familia de sistemas operativos PointSav | Contribuyentes de PointSav y operadores de flota |
| `woodfine-design-bim` | Organización de cliente `woodfine` | Tokens y componentes de Modelado de Información de Construcción para superficies de activos inmobiliarios | Arquitectos, ingenieros y operadores de activos inmobiliarios |

Los dos sistemas comparten metodología — el [[six-tier-sovereignty-matrix|modelo de soberanía de seis niveles]] y la regla estricta de kebab-case — pero no comparten contenido. Un token de diseño BIM no pertenece al sustrato de UI de PointSav; un token de interfaz de consola no pertenece a la biblioteca BIM. Este artículo cubre el primer sistema.

## Las dos escalas

| Escala | Uso | Pasos |
|---|---|---|
| **Utility** | Texto de interfaz — cuerpo, etiquetas, descripciones, celdas de tabla, botones | 4 (12/14/16/16-negrita) |
| **Display** | Tipografía expresiva — subtítulos, encabezados de sección, títulos de página, hero | 4 (20/24/32/42) |

La separación es estructural, no decorativa. El texto Utility utiliza interletrado optimizado para legibilidad en pantalla a tamaños pequeños; el texto Display utiliza interletrado negativo para un ritmo de encabezado más ajustado. Mezclar escalas rompe la jerarquía visual del sistema.

## Las seis familias tipográficas

El sistema de diseño organiza cada tipografía en cinco familias funcionales más dos activos de marca:

| Familia | Función | Implementación de referencia | Utilizada por |
|---|---|---|---|
| `font-ui-variable` | Sans de peso variable para toda la interfaz; un solo archivo reemplaza pesos separados para escritorio y móvil | Inter Variable o Roboto Flex | Escritorio `os-workplace`, cromo del Libro Mayor de Comandos |
| `font-mono-code` | Monoespaciada con parches Nerd Font; ligaduras de código; cero con barra; `1 l I` distinguibles | Mono personalizada con parches NF | Texto del cuerpo del Libro Mayor de Comandos, el Forge |
| `font-document-serif` | Serif transicional optimizada para pantalla e impresión | Noto Serif o Literata | Wiki de documentación, lectura de forma larga, salida PDF-A |
| `font-tabular-nums` | Subconjunto numérico especializado con alineación vertical perfecta | Variante de la sans de UI con figuras tabulares | [[service-bookkeeper\|service-bookkeeper]], IronCalc, tablas financieras |
| `font-iconography` | Conjunto de símbolos vectoriales SVG-en-OTF | Propiedad de PointSav | Todos los iconos de UI de `os-*` |

| Activo de marca | Función |
|---|---|
| `asset-brand-pointsav` | La marca del proveedor — marketing, presentaciones públicas, la marca del proveedor en sí. Nunca se usa para texto de interfaz. |
| `asset-brand-wcp` | La submarca de Woodfine Capital Projects — legalmente distinta de PointSav para mantener la jerarquía corporativa. |

`font-ui-variable` incluye una cadena de respaldo del sistema para que cada superficie siga siendo funcional si el binario de fuente variable no está cargado:

```
'Inter Variable', 'Roboto Flex', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
```

Un tema de cliente puede sustituir cualquier familia tipográfica en la capa primitiva. El autohospedaje del binario tipográfico es responsabilidad del cliente.

## Paquetes tipográficos

La tipografía se divide en un almacén de binarios y un motor:

| Paquete | Contenidos | Justificación |
|---|---|---|
| `package-fonts` | Almacenamiento puro de activos — binarios `.woff2`, `.ttf`, `.otf` | Aislar los binarios evita que los paquetes de lógica hereden la sobrecarga del sistema de archivos |
| `package-typography` | Lógica nativa en Rust para control de respaldo, conformación de texto, interpolación de fuentes variables | La calidad de ingeniería pertenece al motor, no a los activos |

## La escala tipográfica

### Utility

| Token | Tamaño / Línea / Peso | Uso |
|---|---|---|
| `typography.utility-1` | 12 / 16 / 400 | Descripción, etiqueta, celda de tabla |
| `typography.utility-2` | 14 / 20 / 400 | Cuerpo secundario, texto de ayuda |
| `typography.utility-3` | 16 / 24 / 400 | Piso del cuerpo principal |
| `typography.utility-4` | 16 / 24 / 600 | Encabezado de interfaz, etiqueta de botón |

### Display

| Token | Tamaño / Línea / Peso | Uso |
|---|---|---|
| `typography.display-1` | 20 / 28 / 500 | Subtítulo |
| `typography.display-2` | 24 / 32 / 500 | Encabezado de sección |
| `typography.display-3` | 32 / 40 / 400 | Título de página |
| `typography.display-4` | 42 / 50 / 300 | Hero / portada |

## Jerarquía de encabezados

| HTML | Token |
|---|---|
| `<h1>` | `display-3` |
| `<h2>` | `display-2` |
| `<h3>` | `display-1` |
| `<h4>` | `utility-4` |
| Cuerpo `<p>` | `utility-3` |
| `<small>`, ayuda, descripción | `utility-2` |

Un salto de nivel — `h1` seguido de `h3` sin `h2` entre ellos — rompe la accesibilidad; los lectores de pantalla dependen de la jerarquía para navegar.

## Tipografía como ley

El requisito tipográfico más estricto es la fidelidad pantalla-impresión. Un PDF generado a partir de un registro Totebox en 2030 debe renderizarse de forma idéntica a la versión en pantalla que firmó el auditor en 2026. Esto es lo que exigen las obligaciones de [[compliance-and-continuous-disclosure|divulgación continua]]; lo que presuponen los sufijos de estado de documento ISO 19650 (`_JW`, `_FIN`, `_PUB`, `_EXE`, `_MCH`/`_DAT`); y lo que demanda el estándar de Paquete de Resolución de Activos Digitales cuando un registro es separado del proveedor y devuelto a su propietario legal.

La fidelidad tipográfica es cumplimiento regulatorio, no preferencia estética.

## Kebab-case estricto

Todos los nombres de directorios, paquetes, repositorios y binarios son en minúsculas con guiones. Las mayúsculas están prohibidas en todo el sistema de diseño. La regla se aplica en registros Docker (que rechazan mayúsculas), sistemas de archivos Linux (sensibles a mayúsculas), macOS (insensible a mayúsculas) y subdominios DNS. Una excepción en cualquier parte del sistema genera desviación de infraestructura permanente; aplicar la regla cuesta una sola regla.

## Voz de marca

Las reglas de voz del sustrato viven en el bloque `voice` del tema activo. Marca PointSav:

- **Confiada** — sin titubeos, sin disculpas
- **Directa** — verbos de acción primero, oraciones de una sola cláusula donde sea posible
- **Profesional** — registro preciso, sin vocabulario de marketing

El vocabulario prohibido se aplica a todo el texto del cuerpo y los encabezados.

## Véase también

- [[design-color]]
- [[design-spacing]]
- [[design-philosophy]]
- [[six-tier-sovereignty-matrix]] — el modelo de soberanía compartido por ambos sistemas de diseño
- [[compliance-and-continuous-disclosure]] — el marco regulatorio subyacente a la fidelidad tipográfica
