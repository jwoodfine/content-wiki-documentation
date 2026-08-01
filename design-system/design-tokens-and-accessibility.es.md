---
schema: foundry-doc-v1
title: "Tokens de diseño y conformidad de accesibilidad"
slug: design-tokens-and-accessibility
short_description: "Cómo el Sistema de Diseño PointSav expresa los requisitos de accesibilidad — objetivos táctiles mínimos, color del anillo de foco, relaciones de contraste — como tokens de diseño con nombre, de modo que la conformidad WCAG se aplica por la estructura del grafo de tokens en lugar de verificarse ad hoc por componente, demostrado contra la especificación de accesibilidad del componente Button ya publicada."
category: design-system
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: design-tokens-and-accessibility.md
cites: []
---

La mayor parte del trabajo de accesibilidad es retroactivo: se construye la
interfaz y después se audita. Un verificador recorre la página, señala un
anillo de foco que desapareció o un objetivo táctil que se encogió, y
alguien rastrea el defecto por el CSS hasta el componente que lo introdujo.
La auditoría encuentra el fallo después de publicado, página por página, y
vuelve a encontrarlo la próxima vez que el mismo error se comete en otro
lugar.

El Sistema de Diseño PointSav sostiene que los valores de los que depende la
conformidad de accesibilidad — un objetivo táctil mínimo, el color de un
anillo de foco, la relación de contraste entre dos colores — son tokens de
diseño como cualquier otro, y pertenecen al mismo grafo de tokens versionado
que el color, el espaciado y la tipografía. Cuando el requisito es un token,
todo componente que referencia el token satisface el requisito de forma
estructural. La pregunta de auditoría cambia de "¿resulta que todos los
botones de todas las páginas son suficientemente grandes?" a "¿referencia la
receta del botón el token de tamaño de objetivo?" — una pregunta con una
sola respuesta, verificada en un solo lugar.

## Los valores de accesibilidad son tokens

Dos tokens anclan el patrón. `a11y-target-min` es un token primitivo cuyo
valor es 44 píxeles — la dimensión mínima de objetivo definida por el
Criterio de Éxito 2.5.5 de las WCAG, Tamaño del Objetivo (Mejorado), un
criterio de nivel AAA que exige objetivos de puntero de al menos 44 por 44
píxeles CSS. `cds-focus` es un token semántico que nombra el color del
anillo de foco; se resuelve contra un primitivo de la escala de azules en
lugar de portar un valor hexadecimal propio, de modo que un cambio de tema
se propaga a todos los anillos de foco a la vez.

Vale la pena enunciar con precisión los requisitos externos que estos
tokens codifican, porque los niveles difieren. Las WCAG 2.2, publicadas
como Recomendación del W3C en octubre de 2023, añadieron el SC 2.5.8
Tamaño del Objetivo (Mínimo) en nivel AA — 24 por 24 píxeles CSS, con
excepciones por separación y objetivos en línea. El SC 2.5.5 preexistente,
de nivel AAA, exige 44 por 44 sin excepción por separación. Este sistema de
diseño tokeniza el valor AAA, el más estricto. Los indicadores de foco se
rigen por dos criterios que operan juntos: el SC 2.4.7 Foco Visible (nivel
AA) exige que exista un indicador visible, y el SC 1.4.11 Contraste No
Textual (nivel AA) exige que el indicador — como toda información visual
que identifica el estado de un componente — mantenga al menos 3:1 de
contraste frente a los colores adyacentes.

## La cadena de niveles porta el requisito

Los tokens del sistema se resuelven en tres niveles — primitivo, semántico,
componente — y un requisito de accesibilidad desciende por la cadena igual
que lo hace un color de marca:

```
a11y-target-min (primitivo, 44px, WCAG 2.5.5 AAA)
  → cds-focus (semántico, color del anillo de foco)
    → btn-min-height (componente: {a11y-target-min}, aplicado a todo botón)
```

El nivel de componente nunca repite el número. `btn-min-height` es una
referencia, `{a11y-target-min}`, no una segunda copia de "44px" que podría
derivar cuando la primera cambie. Si la organización adoptara alguna vez
otra política de tamaño de objetivo, el cambio se haría una sola vez, en el
primitivo, y todos los componentes que consumen la cadena lo seguirían —
exactamente la propiedad de mantenimiento que motiva los tokens de color,
aplicada a un valor de conformidad.

## Los pares de contraste se computan desde el grafo

Como los tokens de color son datos, las relaciones de contraste entre ellos
son computables en lugar de meramente afirmables. La referencia de
fundamentos del sistema presenta pares de accesibilidad — un token de
primer plano contra un token de fondo — con razones computadas directamente
desde los valores hexadecimales de los tokens mediante la fórmula de
luminancia relativa de las WCAG: el texto primario sobre el fondo
predeterminado en torno a 19,2:1 (AAA), el texto secundario en torno a
8,2:1 (AAA), el color de enlace primario en torno a 6,7:1 (AA).

El cuarto par publicado es el honesto: `cds-positive-text` sobre
`cds-positive-bg` computa en torno a 4,3:1, por debajo del umbral AA de
4,5:1 para texto normal con los valores actuales, y se muestra señalado en
lugar de ajustado en silencio. Un registro que computa la conformidad desde
sus propios datos hace aflorar las regresiones igual que hace aflorar todo
lo demás. Dos salvedades acompañan a estas cifras, enunciadas en la propia
página de referencia y repetidas aquí: las razones ilustran el patrón y no
sustituyen a una herramienta de auditoría en vivo, y el par señalado es un
asunto abierto, no resuelto.

## Un componente hereda su conformidad

La especificación de accesibilidad ya publicada del componente Button
muestra lo que el enfoque de tokens produce en el nivel de componente. Su
objetivo de conformidad es WCAG 2.2 AAA, y su tabla de conformidad se
resuelve, criterio por criterio, en hechos derivados de tokens: contraste
de texto de 7,4:1 contra el fondo de la variante primaria (superando el
SC 1.4.6 Contraste Mejorado, AAA); un anillo de foco de 2 píxeles con un
desplazamiento de 2 píxeles que mantiene el mínimo de 3:1 del SC 1.4.11; y
el tamaño de objetivo cumplido por aritmética — el botón se renderiza con
40 píxeles de altura, y el anillo de foco más su desplazamiento añaden 2
píxeles por lado, llevando el área activable a los 44 píxeles que exige el
SC 2.5.5.

La misma especificación muestra requisitos conductuales, más que numéricos,
portados por tokens allí donde un token puede portarlos: el valor de
duración de transición del CSS se resuelve a cero cuando
`prefers-reduced-motion: reduce` aplica, de modo que los consumidores
obtienen soporte de movimiento reducido sin escribir código alguno. Y
registra las reglas que ningún token puede imponer — ningún estado
comunicado solo por color, elementos `<button>` nativos en lugar de
`role="button"` sobre un `<div>`, ningún anillo de foco eliminado sin
sustituto — como antipatrones con nombre dentro de la especificación, junto
a las referencias de tokens y no en un documento separado que deriva.

La línea de cierre de la propia especificación pone la nota justa de
franqueza: un punto de acceso de auditoría WCAG por componente es trabajo
futuro, y hasta que exista, la especificación escrita es la declaración
canónica de conformidad.

## Lo que la aplicación estructural no sustituye

Dicho con claridad. Las afirmaciones de conformidad anteriores son
autodeclaradas por los mantenedores del sistema de diseño contra los
criterios citados; no se ha realizado una auditoría de accesibilidad por
terceros. Los tokens imponen los valores de los que depende un criterio,
no el criterio en sí — un componente puede referenciar `a11y-target-min` y
aun así fallar a los usuarios de teclado por un marcado roto, y ningún
token expresa los criterios que dependen del juicio sobre contenido,
etiquetas y contexto. Las pruebas con tecnología de asistencia y lectores
de pantalla reales siguen siendo manuales. La afirmación estructural es más
estrecha y, por eso mismo, defendible: valores que antes se redecidían por
componente ahora se deciden una vez, en datos, donde verificarlos es
barato.

## Antecedentes y licenciamiento

La arquitectura de tokens en tres niveles sobre la que cabalga este patrón
está bien establecida y no es una invención de PointSav: Carbon, de IBM,
documenta niveles de tokens globales, alias y de componente, y Material
Design 3, de Google, documenta clases de tokens de referencia, de sistema y
de componente. Ambos sistemas publican guías de accesibilidad junto a sus
tokens. Lo que este artículo describe es la aplicación de esa estructura de
niveles compartida a los valores de conformidad en concreto — el tamaño de
objetivo y el color de foco como tokens de primera clase, con el criterio
WCAG registrado en el propio campo de descripción del token.

En cuanto al licenciamiento, la precisión importa porque hay dos licencias
distintas en juego. Los datos de tokens en sí — `a11y-target-min`,
`cds-focus`, los archivos de tokens DTCG y las recetas de componentes que
los referencian — se publican en el repositorio `pointsav-design-system`
bajo la licencia Apache-2.0. El texto de este artículo se publica en el
wiki de documentación bajo CC BY 4.0. Reutilizar los tokens implica cumplir
Apache-2.0; reutilizar la prosa de este artículo implica cumplir CC BY 4.0.
Ninguna de las dos licencias rige el otro artefacto.

---

*Este artículo es material de contexto para lectores de la documentación
del Sistema de Diseño PointSav, previo a las especificaciones de
accesibilidad por componente y a la referencia de tokens de fundamentos.
Véase también: el artículo de vocabulario primitivo para el esquema
completo de nomenclatura de tokens, y el artículo de filosofía de diseño
para la capa de fundamentación que registra por qué se tomó cada decisión
de accesibilidad.*
