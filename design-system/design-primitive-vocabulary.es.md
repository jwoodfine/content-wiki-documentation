---
schema: foundry-doc-v1
title: "Sistema de diseño — Justificación del vocabulario primitivo"
slug: design-primitive-vocabulary
short_description: "Justificación de los patrones de la capa de tokens primitivos — escalas de color numéricas, aliasing semántico y separación tipográfica — con nomenclatura propia de PointSav."
category: design-system
type: reference
content_type: topic
quality: complete
index_group: philosophy-and-primitive-vocabulary
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: design-primitive-vocabulary.md
cites:
 - wcag-22
 - dtcg-spec
 - doctrine-38
---

La capa de tokens primitivos del [[design-system-substrate|sistema de diseño]] documenta qué patrones estructurales ha consolidado el campo desde 2018, cuáles preserva el sustrato de forma literal y cuáles reemplaza con vocabulario y valores originales de PointSav. La distinción es relevante para los profesionales que llegan de otros sistemas de diseño: los patrones estructurales compartidos generan reconocimiento inmediato; los nombres y valores originales de PointSav evitan cualquier conflicto de propiedad intelectual con los sistemas de los que se tomaron referencias. La justificación arquitectónica del sustrato está en [[design-philosophy|la filosofía del sistema de diseño]].

La capa de tokens primitivos del sustrato preserva cuatro patrones estructurales en los que el campo moderno de sistemas de diseño ha convergido (2018–2026): escalas de color numéricas, capas primitivo → semántico → componente, la división de tipografía productiva vs expresiva, y escalas de espaciado numéricas de ~12–15 pasos.

Estos patrones no son propiedad intelectual de ningún sistema de diseño en particular — son el vocabulario compartido del campo. Re-implementarlos es la elección arquitectónica correcta para cualquier sistema de diseño de 2026 que quiera que los profesionales lo adopten sin necesidad de re-aprender lo básico.

## Lo que el sustrato reemplazó

El sustrato utiliza vocabulario, valores hexadecimales, elecciones tipográficas y contenido originales de PointSav. Concretamente:

| Superficie | Convención habitual del campo | Elección del sustrato | Por qué se reemplazó |
|---|---|---|---|
| Nombres de familias de color | `gray`, `blue`, `red`, `green`, `yellow` | `neutral`, `primary`, `positive`, `caution`, `critical` | Los nombres de PointSav describen el rol, no la familia cromática — los inquilinos que cambian su marca de azul a verde azulado no tienen que renombrar tokens. |
| Valores hexadecimales | Tonos propios del proveedor | Tonos elegidos por PointSav (p. ej., Primary 60 = `#234ed8`) | Evita el entrelazamiento de propiedad intelectual; el sustrato se sostiene con sus propios valores. |
| Nombre del token de espaciado | `spacing-01` a `spacing-13` (con ceros a la izquierda) | `space-1` a `space-13` (sin ceros a la izquierda) | Ligeramente más limpio; misma escala numérica; misma estructura de base de 8px. |
| Nombres de familia de escala tipográfica | `productive-01..N`, `expressive-01..N` | `utility-1..4`, `display-1..4` | Misma división conceptual; nombres originales de PointSav. |
| Nombres de curvas de movimiento | `ease-productive`, `ease-expressive`, `ease-entrance`, `ease-exit` | `ease-utility`, `ease-display`, `ease-enter`, `ease-exit` | Mismo conjunto de cuatro curvas; alineado con el renombrado de la escala tipográfica. |
| Nombres de duración | `fast-01`, `fast-02`, `moderate-01`, `moderate-02`, `slow-01`, `slow-02` | `speed-1` a `speed-6` | Misma escala de seis pasos; nomenclatura más limpia. |
| Nombres de radio de borde | `radius-01`, `radius-02`, `radius-03` | `corner-1`, `corner-2`, `corner-3` | Misma escala de tres pasos; nomenclatura diferenciada. |
| Tipografía por defecto | Una tipografía de código abierto patrocinada por una empresa | Inter (código abierto comunitario, SIL OFL 1.1) + pila de sistema como respaldo | Sin asociación de marca corporativa; Inter es el caballo de batalla moderno de la interfaz; la pila de sistema garantiza una degradación adecuada. |
| Nombres de tema | Etiquetas claro/oscuro propias de una marca | `pointsav-brand` (canónico), variantes por inquilino | PointSav distribuye la marca canónica y los clientes PYME distribuyen la suya propia. |

## Lo que el sustrato preservó literalmente de la convención más amplia

Estos elementos son compartidos por el campo, no propios de un proveedor:

- `$type: "color"`, `$value`, `$description` — sintaxis de la especificación DTCG 2025.10
- Sintaxis de referencia `{path.to.token}` — aliasing DTCG
- Piso de contraste WCAG 2.2 AAA — estándar de accesibilidad
- Consulta `prefers-reduced-motion` — CSS Media Queries Level 5
- Cuadrícula base de 8px para el espaciado — común en todo el campo

Estos son los estándares abiertos que el sustrato hereda como consumidor de estándares abiertos.

## Por qué importa la memoria muscular

Un diseñador o desarrollador que llega de cualquier entorno de sistema de diseño moderno reconoce los patrones estructurales del sustrato en segundos: escala de color numérica, capas DTCG, dos pistas tipográficas. Este reconocimiento es la rampa cognitiva de entrada. Es la mayor ventaja libre del sustrato — un profesional se adapta en días, no en semanas.

## Por qué importa el vocabulario

Un token nombrado por familia cromática con los valores exactos de un proveedor específico pone al sustrato a un litigio de marcas de distancia de un rediseño. Un token nombrado por rol con valores elegidos por PointSav, no.

## Véase también

- [[what-is-a-design-token|Qué es un token de diseño]] — comience aquí para una definición introductoria de un token de diseño antes de este artículo de justificación
- [[design-philosophy]] — las tres inversiones estructurales que motivan las decisiones de diseño del sustrato
- [[wiki-typography-system]] — la pila tipográfica Inter y Source Serif 4 construida sobre estas convenciones de tokens
- [[wiki-component-library]] — el armazón compartido y las plantillas de página del wiki, que consumen las capas de tokens descritas aquí
- [[component-recipes-vs-raw-tokens|Recetas de componentes frente a tokens en bruto]] — cómo el nivel de componentes consume el esquema de nomenclatura descrito aquí
- [[design-tokens-and-accessibility|Tokens de diseño y conformidad de accesibilidad]] — cómo se aplica estructuralmente como tokens el límite de contraste WCAG 2.2 AAA mencionado arriba

## Referencias

- Formato del W3C Design Tokens Community Group — https://design-tokens.github.io/community-group/format/
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
