---
schema: foundry-doc-v1
title: "Versiones dirigidas por registro: una sola fuente de verdad para tokens, componentes y conteos"
slug: registry-driven-releases
short_description: "Explica la arquitectura dirigida por registro detrás de las versiones del sitio del sistema de diseño: la navegación, las estadísticas de la portada, el punto de acceso de registro legible por máquina, las respuestas MCP y el empaquetado de versiones se resuelven todos contra un único archivo de registro, de modo que no pueden divergir — ilustrado con dos defectos reales de la propia historia del sistema, no con hipótesis."
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
paired_with: registry-driven-releases.md
cites: []
---

El sitio de un sistema de diseño hace pequeñas afirmaciones de hecho por
todas partes: la navegación enumera ocho secciones, la portada dice 146
tokens y 37 componentes, la página de versiones dice que un paquete contiene
lo que contiene, el punto de acceso para máquinas devuelve conteos a
cualquier agente que pregunte. Cada afirmación es fácil de enunciar y fácil
de equivocar, porque cada una suele vivir en un archivo distinto, mantenido
por una mano distinta, en un día distinto.

La arquitectura v3 de design.pointsav.com toma una posición al respecto:
cada una de esas afirmaciones debe resolverse contra un único archivo de
registro. La navegación, las estadísticas de la portada, el punto de acceso
de registro legible por máquina (`/registry.json`), las respuestas de las
herramientas MCP y el empaquetado que corta las descargas de cada versión
leen todos los mismos registros. Un componente que no está registrado no
puede aparecer en la navegación; un conteo en la portada no puede diferir de
lo que contiene una versión, porque hay exactamente un lugar del que sale
cualquiera de esos números. Las versiones dejan de ser artefactos ensamblados
a mano y pasan a ser cortes del registro.

Esa es la tesis. Lo que la hace merecedora de un artículo es que este
sistema ya la ha violado dos veces, de maneras pequeñas e instructivas, en
su propia historia de trabajo — y ambos defectos enseñan más que cualquier
hipótesis.

## El modo de fallo: copias paralelas mantenidas a mano

El patrón general está bien documentado en la práctica de la ingeniería de
software. El movimiento docs-as-code existe porque la documentación
mantenida junto al código, en lugar de dentro de la misma cadena que el
código, deriva de manera fiable: el código cambia continuamente, la
descripción paralela cambia esporádicamente, y la brecha se acumula. El
remedio es estructural, no disciplinario — mantener una sola fuente y
generar el resto, de modo que la copia paralela que podría derivar no
exista.

Las herramientas de diseño llegaron a la misma conclusión para los valores
de los tokens. Todo el modelo de Style Dictionary es una única fuente de
JSON de tokens transformada en salidas por plataforma — propiedades
personalizadas de CSS, formatos de iOS y Android — precisamente para que
ninguna plataforma mantenga su propia copia editada a mano de un color.
Tokens Studio aplica la misma lógica a la frontera entre diseño y código,
usando un repositorio git como la fuente de verdad contra la que se
sincronizan tanto la herramienta de diseño como la cadena de construcción.
La arquitectura de registro descrita aquí extiende ese principio establecido
un nivel hacia arriba: no solo los *valores* de los tokens, sino las
afirmaciones del sitio *sobre* sus tokens y componentes — qué existe, cómo
se llama, cuántos hay, qué se incluye en una versión.

## Un ejemplo práctico de nuestra propia revisión

Durante la revisión del 2026-07-10 de la maqueta de la portada v3, la página
llevaba una respuesta `curl` ilustrativa que mostraba lo que devolvería
`/registry.json` — incluido un arreglo `nav` que enumeraba las secciones del
sitio. La navegación visible de la misma página tenía ocho entradas. El
arreglo `nav` del JSON del registro tenía siete: omitía "Running at
PointSav", una entrada que la navegación renderizada claramente incluía.

En una página cuyo diagrama central sostiene que la navegación y el registro
no pueden discrepar porque ambos leen el mismo archivo, la navegación y el
registro discrepaban. La razón es exactamente el modo de fallo descrito
arriba: en una maqueta estática, tanto la navegación visible como el
"registro" son HTML escrito a mano, de modo que la garantía estructural que
la página describe aún no protegía a la página que la describía. El defecto
se encontró en revisión y se corrigió el mismo día, y se registra aquí
deliberadamente: es una instancia genuina y verificada de lo fácil que es
violar el principio por accidente — una edición aplicada a una copia y no a
la otra — y, por lo tanto, de por qué la garantía tiene que construirse, no
prometerse.

## Un segundo ejemplo: dos paquetes de tokens

La misma semana aportó una instancia mayor. El repositorio del sistema de
diseño llevaba dos archivos llamados `dtcg-bundle.json` — uno en la raíz
`tokens/` del repositorio, otro dentro del vault — con contenido solapado y
sin relación declarada. Un diff completo de reconciliación, que resolvía
cada alias de token hasta su valor literal final en ambos lados en lugar de
comparar cadenas crudas, encontró 107 rutas de token presentes en ambos
archivos. Cuarenta de los cincuenta conflictos de valor aparentes eran
falsas alarmas — un lado referenciaba un alias donde el otro escribía el
literal al que ese alias resuelve — pero diez eran conflictos reales, y
cinco colores primitivos existían solo en la copia que ya no se mantenía.

Dos detalles hacen útil este ejemplo. Primero, ninguna de las dos copias
alimentaba realmente el sitio: los tokens que sirve design.pointsav.com se
resuelven a través de una sola cadena — los archivos fuente del vault
compilados en una única exportación resuelta
(`dtcg-vault/exports/tokens.full.json`, 146 tokens hoja) — de modo que la
divergencia era invisible en producción mientras seguía siendo un riesgo
vivo para cualquier herramienta que eligiera el archivo equivocado. Segundo,
la resolución tuvo forma de registro: declarar canónica una copia, plegar en
ella los cinco valores genuinamente nuevos, y reemplazar la otra con un
talón de obsolescencia que apunta al archivo canónico. No una limpieza de
dos copias hacia dos copias mejores — la eliminación de la segunda copia
como cosa que puede derivar.

## Qué dirige el registro

En la arquitectura v3, el archivo de registro es la fuente única para cinco
consumidores: la navegación; las estadísticas de la portada; el punto de
acceso `/registry.json`, que devuelve los mismos registros a las máquinas;
las [[design-system-substrate|herramientas MCP]] que responden consultas de agentes sobre tokens y
componentes; y el empaquetado de versiones, donde una descarga versionada —
paquete de tokens, archivo de activos, manifiesto — se corta a partir de las
entradas registradas, de modo que nada se distribuye sin estar registrado y
nada registrado puede omitirse en silencio de lo que se distribuye. La
propiedad que se compra no es orden. Es que las afirmaciones de hecho del
sitio se vuelven verificables contra un archivo, por cualquiera, incluida la
propia construcción del sitio.

## Qué licencia aplica a qué

Hay tres licencias en juego, y no se sustituyen entre sí. El registro
describe **datos** de tokens y componentes, que son Apache-2.0. El
**servidor** que sirve `/registry.json` y el punto de acceso MCP
(`app-privategit-design` en el monorepo de PointSav) es AGPL-3.0-or-later.
**Este artículo** es CC BY 4.0, la licencia del wiki de documentación en el
que se publica. Una descarga de versión construida a partir del registro
lleva la licencia de los datos, Apache-2.0, no la del servidor.

## Alcance y límites

Dicho con claridad: al momento de escribir, el sitio dirigido por registro
es una maqueta de diseño en revisión, no el sitio de producción en vivo, y
el JSON del registro de la maqueta se mantiene, él mismo, a mano — que es
precisamente cómo fue posible el defecto de navegación descrito arriba. La
afirmación de que la deriva es imposible es una propiedad de la arquitectura
objetivo, en la que el registro se genera desde el vault y cada consumidor
lo lee en tiempo de construcción o de solicitud; todavía no es una propiedad
que la maqueta pueda hacer cumplir, y una comprobación de consistencia en
tiempo de construcción que falle cuando las afirmaciones renderizadas
difieran del registro está diseñada pero no implementada. Los dos ejemplos
prácticos de este artículo son reales y se verificaron contra la propia
historia del repositorio antes de su publicación; no se afirman casos de
estudio externos ni cifras de adopción, porque aún no existen.

---

*Este artículo es material de contexto para los lectores de la documentación
del Sistema de Diseño PointSav, previo a la página de versiones y a la
referencia de la superficie para máquinas. Explica por qué los conteos, la
navegación, los puntos de acceso y las descargas del sitio están diseñados
para resolverse contra un único archivo de registro, usando como evidencia
los defectos registrados del propio sistema en lugar de hipótesis.*
