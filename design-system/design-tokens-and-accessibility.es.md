---
schema: foundry-doc-v1
title: "Tokens de diseño y conformidad de accesibilidad"
slug: design-tokens-and-accessibility
short_description: "Cómo el Sistema de Diseño PointSav expresa los requisitos de accesibilidad — objetivos táctiles mínimos, color del anillo de foco, relaciones de contraste — como tokens de diseño con nombre, de modo que la conformidad WCAG se aplica por la estructura del grafo de tokens y no ad hoc por componente, demostrado contra la especificación de accesibilidad de Button ya publicada."
category: design-system
type: topic
content_type: topic
quality: complete
index_group: token-concepts-and-tooling
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

El anillo de foco ancla el patrón. `focus.ring` es un token primitivo —
no un simple color, sino un token compuesto que agrupa el color del
anillo (`{color.primary-60}`), el grosor, el estilo y un desplazamiento de
2px — de modo que un cambio en el color primario se propaga a todos los
anillos de foco a la vez. El tamaño del objetivo no es un token
independiente de la misma forma; se cumple aritméticamente en el nivel de
componente — el botón, más abajo, muestra exactamente cómo.

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
componente — y el requisito del anillo de foco desciende por la cadena
igual que lo hace un color de marca:

```
focus.ring (primitivo: color {color.primary-60}, grosor, estilo, offset 2px)
  → toda receta de componente que necesita un indicador de foco lo referencia directamente
```

El anillo de foco de un componente es una referencia a `{focus.ring}`, no
una segunda copia de los valores de color y grosor que podría derivar
cuando el primitivo cambie. Si el color del anillo cambiara alguna vez, el
cambio se haría una sola vez, en el primitivo, y todos los componentes que
lo consumen lo seguirían — la misma propiedad de mantenimiento que motiva
los tokens de color, aplicada a un valor de conformidad.

## Los pares de contraste se computan desde el grafo

Como los tokens de color son datos, las relaciones de contraste entre ellos
son computables en lugar de meramente afirmables. La referencia de color
del sistema publica los pares que más importan — un token de primer plano
contra un token de fondo — con razones computadas directamente desde los
valores hexadecimales mediante la fórmula de luminancia relativa de las
WCAG: `ink-primary` sobre la superficie predeterminada en 14,7:1 (AAA),
`ink-secondary` sobre la superficie predeterminada en 8,9:1 (AAA), y el
texto de botón (`ink-on-interactive`) sobre el fondo interactivo primario
en 7,4:1 (AAA).

No todos los pares alcanzan el mismo nivel — el componente Button, más
abajo, muestra un caso real donde una variante específica queda en AA en
vez de AAA, y la especificación de accesibilidad del propio componente lo
declara con claridad en vez de redondear hacia arriba. Un registro que
computa la conformidad desde sus propios datos hace aflorar precisamente
este tipo de brecha en vez de afirmar un estándar uniforme entre todos los
pares de color.

## Un componente hereda su conformidad

La especificación de accesibilidad ya publicada del componente Button
muestra lo que el enfoque de tokens produce en el nivel de componente,
incluidas las partes que no alcanzan el nivel más estricto. Su objetivo de
conformidad es WCAG 2.2 AA, con AAA donde sea alcanzable — no una
afirmación general de AAA — y la especificación es explícita sobre qué
variante alcanza qué nivel: el contraste de texto de la variante primaria
es de 6,66:1, que aprueba AA (SC 1.4.3) pero no llega al piso de 7:1 de
AAA (SC 1.4.6); la variante crítica alcanza ambos en 7,33:1. El anillo de
foco mantiene el mínimo de 3:1 del SC 1.4.11 en todas las variantes. El
tamaño de objetivo se cumple por aritmética — el botón se renderiza con 40
píxeles de altura, y el anillo de foco más su desplazamiento añaden 2
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
no el criterio en sí — un componente puede referenciar `{focus.ring}` y
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
distintas en juego. Los datos de tokens en sí — `focus.ring`, los
archivos de tokens DTCG y las recetas de componentes que
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
