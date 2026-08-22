---
schema: foundry-doc-v1
title: "Recetas de componentes frente a tokens en bruto"
slug: component-recipes-vs-raw-tokens
short_description: "Qué añade el nivel de componentes del Sistema de Diseño PointSav más allá del valor de un token: el formato recipe.json — variantes, marcado, referencias de tokens, CSS, guía ARIA y objetivos WCAG en un solo artefacto legible por máquina — demostrado contra la receta publicada del componente Button y el estado documental real del registro (53 componentes: 20 con documentación completa, 33 con receta más al menos un documento de uso)."
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
paired_with: component-recipes-vs-raw-tokens.md
cites: []
---

Un token de diseño responde una sola pregunta: ¿cuál es el valor?
`interactive-primary` es un color, `space-5` es una longitud, `speed-2` es
una duración. Los tokens son la unidad más pequeña de decisión de diseño
que el sistema versiona, y todo lo que está por encima se resuelve por
referencia. Pero un elemento de interfaz funcional no es una bolsa de
valores. Un botón es marcado, un conjunto de estilos de estado, un
comportamiento de foco, un contrato de accesibilidad y un puñado de reglas
de uso sobre cuándo es apropiada cada variante — y nada de eso vive en un
token.

La respuesta del Sistema de Diseño PointSav a esa brecha es la receta de
componente: un único artefacto JSON legible por máquina, por componente,
que compone referencias de tokens en un elemento funcional. Este artículo
explica qué añade el nivel de recetas más allá de los valores de tokens en
bruto, usando la receta publicada del componente Button como ejemplo
trabajado, y describe el estado documental real del registro en lugar de
uno idealizado.

## Qué da un token en bruto — y dónde se detiene

Un token del paquete en formato DTCG del sistema porta un valor, un tipo y
una descripción que registra la fundamentación de la decisión. Eso basta
para los problemas que los tokens resuelven: una sola fuente de verdad por
valor, sustitución a nivel de tema y reutilización sin deriva. No basta
para construir. Un desarrollador con `interactive-primary` en la mano
todavía tiene que decidir qué elemento renderizar, qué estados estilizar,
cómo se relacionan hover y presionado con el color base, qué hace el anillo
de foco y qué aspecto tiene el estado deshabilitado. Cada consumidor que
toma esas decisiones por su cuenta reintroduce exactamente la divergencia
que los tokens debían eliminar — un nivel más arriba.

## El formato de receta

La receta del Button demuestra la forma. Es un documento JSON que declara
un esquema, una identidad (`name`, `display_name`, una descripción de una
frase, una categoría, un tipo de registro) y, a continuación, la sustancia:

**Variantes como decisiones con nombre.** Cada variante — primary,
secondary, ghost, critical — porta su propia descripción, su plantilla
HTML, su clase CSS y la lista de tokens que consume. Las descripciones son
reglas de uso, no epígrafes: primary es "la acción más prominente de una
superficie. Una por superficie"; critical es "acción destructiva. Siempre
emparejada con un paso de confirmación". La regla viaja dentro de los
datos, donde un generador de código o un agente revisor la lee, y no solo
en una prosa que un humano quizá no abra.

**Marcado con ranuras.** El campo `html` de cada variante es una plantilla
— un `<button type="button">` nativo con una ranura `{{label}}` — de modo
que los consumidores heredan el elemento y la estructura correctos en lugar
de reconstruirlos.

**Referencias de tokens, no valores.** El arreglo `tokens` de una variante
lista referencias semánticas: `{semantic.interactive-primary}`,
`{semantic.interactive-primary-hover}`, `{semantic.ink-on-interactive}`.
La receta nunca codifica un color en duro. En el CSS estas referencias se
resuelven como propiedades personalizadas con valores de respaldo
(`var(--ps-interactive-primary, #234ed8)`), de modo que el componente
cambia de tema cuando el grafo de tokens cambia de tema.

**El CSS completo.** La receta porta las reglas completas de base más
variantes, incluidos los estados que una vista de solo-valores omite:
hover, activo, deshabilitado y `:focus-visible` con un anillo de 2 píxeles
y un desplazamiento de 2 píxeles.

**El contrato de accesibilidad.** Un campo `aria` enuncia en prosa la guía
para lectores de pantalla — rol de botón nativo, `aria-label` para uso de
solo icono, y la regla de que las acciones destructivas no deben quedar a
un clic de completarse. Un bloque `wcag` estructurado declara el objetivo
(2.2 AA, con AAA donde sea alcanzable), la visibilidad del foco, las cifras
reales de contraste por variante —6,66:1 para la primaria, que aprueba AA
pero no el piso de 7:1 de AAA, y 7,33:1 para la crítica, que alcanza
ambos— y el objetivo táctil mínimo de 44 por 44.

**Enlaces de procedencia.** `research_links` apunta a los documentos de
fundamentación de diseño detrás del componente, y `registry_dependencies`
declara qué otras entradas del registro necesita el componente — para
Button, ninguna.

La distinción frente a un token en bruto queda ahora concreta: el nivel de
tokens dice qué es `interactive-primary`; el nivel de recetas dice qué *es*
un botón — y todo lo que dice se resuelve de vuelta hacia tokens por
referencia, de modo que los dos niveles no pueden discrepar sobre un valor.

## Dos niveles documentales, un registro

El registro contiene actualmente 53 componentes, y no están documentados de
manera uniforme. Veinte portan el juego completo de cinco archivos — la
receta más cuatro documentos de cara humana que cubren uso, estilo, código
y accesibilidad. Tampoco el resto son puro dato: 30 portan la receta más un
documento de uso, y 3 portan la receta más un par de uso bilingüe — todo
componente del registro distribuye al menos un documento en prosa junto a
su receta, no solo el artefacto legible por máquina. La referencia de
componentes presenta esto como tres niveles etiquetados, en lugar de
fingir 53 entradas uniformemente terminadas.

El estado escalonado es un hecho de secuenciación, y el papel de la receta
en él es la clave: la receta es el piso. Todo componente ya es consumible
por máquina en el mínimo — su marcado, sus tokens, su CSS y su bloque WCAG
existen — mientras la documentación de estilo y código restante sigue
pendiente para 33 de los 53. El estado inverso (documentación en prosa sin
artefacto de datos) no es un
estado que el registro permita.

## Antecedentes: el nivel de componentes está bien establecido

Nombrar un nivel de componentes por encima de los tokens semánticos es
práctica estándar en los grandes sistemas de diseño publicados, y este
artículo no reclama novedad alguna al respecto. Material Design 3, de
Google, documenta tres clases de tokens — de referencia, de sistema y de
componente — donde un token de componente como `md.comp.fab.container.color`
se resuelve contra un token de sistema como `md.sys.color.primary-container`.
Carbon, de IBM, documenta la estructura equivalente de global/alias/
componente y restringe los tokens de componente a su propio componente. El
patrón es la herencia compartida de los sistemas de diseño de los grandes
proveedores, no una idea de PointSav.

Lo que el formato de receta hace con ese nivel establecido es empaquetar
más del contrato del componente en el único artefacto de datos: donde un
token de componente sigue siendo una asignación de valor, una receta porta
además el marcado, el CSS completo, la guía ARIA y los objetivos WCAG. Es
una elección de integración — un artefacto en lugar de varios — y su mérito
es práctico, no conceptual: un consumidor, humano o máquina, obtiene el
componente construible completo en una sola descarga.

## Licenciamiento: dos artefactos, dos licencias

Aquí se exige precisión porque la receta y este artículo están licenciados
de manera distinta. Los datos de recetas — button/recipe.json y todas las
demás recetas y archivos de tokens DTCG del repositorio
`pointsav-design-system` — se licencian bajo Apache-2.0, la misma
convención que usan IBM Carbon y Adobe Spectrum para el código y los datos
de sus sistemas de diseño. El texto de este artículo se publica en el wiki
de documentación bajo CC BY 4.0. Copiar una receta a un registro propio es
un asunto de Apache-2.0; republicar la prosa de este artículo es un asunto
de CC BY 4.0. Una frase sobre "la licencia" del sistema de diseño debe
decir a cuál de las dos se refiere; esta lo ha hecho.

## Alcance y límites honestos

El ejemplo trabajado es un solo componente, y el censo del registro es una
instantánea fechada al momento de redactar este artículo — la división por
niveles cambiará a medida que los componentes obtengan la documentación
que les falta. Un borrador anterior de este artículo señaló una discrepancia entre la
descripción y el arreglo de variantes en la receta publicada del Button (la
descripción nombraba una quinta variante "link" ausente del arreglo
`variants`); esa discrepancia ya se corrigió en la fuente, que ahora
describe cuatro variantes y explica el conteo erróneo anterior — no queda
ninguna inconsistencia abierta.
El esquema de recetas está versionado (`component-recipe-v1`), y nada en
este artículo debe leerse como una promesa de compatibilidad para versiones
futuras del esquema.

---

*Este artículo es material de contexto para lectores de la documentación
del Sistema de Diseño PointSav, previo a las páginas de referencia por
componente. Véase también: el artículo de vocabulario primitivo para el
esquema de nomenclatura de tokens contra el que se resuelven las recetas, y
el artículo de la biblioteca de componentes del wiki para ver cómo un
conjunto de estos componentes compone una página completa.*
