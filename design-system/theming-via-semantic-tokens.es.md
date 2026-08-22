---
schema: foundry-doc-v1
title: "Tematización mediante tokens semánticos"
slug: theming-via-semantic-tokens
short_description: "Artículo de contexto sobre los temas claro/oscuro como sustitución de tokens semánticos en lugar de una hoja de estilos paralela, fundamentado en el grupo theme.dark ya publicado del paquete PointSav (28 tokens, conmutador [data-theme=\\"dark\\"]) y situado frente al mismo patrón en Carbon, Material 3 y Radix — una técnica establecida, sin pretensión de novedad."
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
paired_with: theming-via-semantic-tokens.md
cites: []
---

El modo oscuro, en este sistema de diseño, no es una segunda hoja de estilos.
Es una sustitución: los mismos 53 roles semánticos que estilizan cada
superficie clara — `surface-base`, `ink-primary`, `border-subtle`,
`interactive-primary` — se vuelven a vincular a valores optimizados para
oscuridad cuando un único atributo, `data-theme="dark"`, aparece en el
elemento raíz del documento. Los componentes nunca se enteran de que existe
un tema. Referencian roles; el tema decide a qué se resuelven los roles.

Esta es una técnica establecida en la industria, no un invento de PointSav, y
este artículo no reclama novedad alguna para ella. Lo que el artículo sí hace
es mostrar el mecanismo de forma concreta en el paquete de tokens publicado
del sistema de diseño — nombres de token reales, valores reales, ya enviados
y en uso en el wiki de documentación — y situarlo frente a los sistemas que
popularizaron el patrón.

## El mecanismo, tal como se envía

El paquete publicado, `tokens.full.json`, transporta el tema oscuro completo
como un solo grupo: `theme.dark`, 28 tokens junto a los 53 roles del tema
claro en `theme.semantic`. El propio campo de descripción del grupo enuncia
el mecanismo de conmutación — "Dark mode semantic overrides — applied via
`[data-theme='dark']` on the root element" (anulaciones semánticas del modo
oscuro, aplicadas mediante `[data-theme='dark']` en el elemento raíz) — y su
composición cuenta la historia arquitectónica:

- **La mayoría del grupo anula un rol semántico por su nombre.**
  `surface-base`, que en el tema claro se resuelve a blanco, se convierte en
  `#1f2125` (el paso primitivo neutral-90) en oscuro. `ink-primary` pasa de
  casi negro a `#f5f6f8` (neutral-10). `border-subtle`, `focus-ring`,
  `interactive-primary`, los colores de estado de precaución, crítico y
  positivo — cada uno conserva su nombre y cambia su valor.
- **Un conjunto más pequeño existe solo en oscuro.** `surface-code` (un fondo
  de bloque de código casi negro, más oscuro que la página, para preservar
  la profundidad), `ink-on-inverse` y varios colores específicos del wiki —
  enlace, enlace inexistente y roles de resaltado de sintaxis — cubren los
  casos en que el modo oscuro no es un espejo del claro, sino que
  necesita decisiones propias.

Dos detalles del mapa oscuro merecen atención. Primero, la dirección del
hover se invierte: en el tema claro, `interactive-primary` es el azul
primary-60 y su estado hover oscurece hacia primary-70; en oscuro, el
relleno es el primary-50, más claro, y el hover se mueve aún más claro,
hacia primary-40. Un esquema ingenuo de "invertir la paleta" pierde esto; un
mapa de sustitución ajustado a mano lo codifica. Segundo, la accesibilidad
queda registrada en el lugar: el grupo declara WCAG 2.2 AA como mínimo para
todos los pares de texto en las superficies verificadas, y los tokens
individuales llevan sus pares de contraste medidos en sus campos de
descripción (el `ink-primary` oscuro contra el `surface-base` oscuro está
documentado en 14,5:1; el recálculo durante la redacción confirma que los
pares citados alcanzan o superan los pisos AA, con varias razones
registradas de forma conservadora).

Como solo cambia la capa semántica, el costo del modo oscuro no escala con
el número de componentes. Un componente construido sobre tokens semánticos
adquiere soporte oscuro el día en que se escribe, sin selectores oscuros por
componente. El wiki que sirve este artículo ejecuta exactamente este
esquema; el artículo separado [[wiki-dark-mode|sobre el modo oscuro del wiki]] documenta los
detalles de implementación de esa superficie — cómo se establece el
atributo, cómo persiste entre visitas y cómo se aplica antes del primer
renderizado — que este artículo deliberadamente no repite.

## La alternativa que esto reemplaza

El enfoque previo a los tokens para el modo oscuro era una hoja de estilos
paralela: un segundo archivo CSS, o un gran bloque
`@media (prefers-color-scheme: dark)`, que reformulaba cada regla que
menciona un color. La reformulación es el defecto. Cada componente nuevo
añade reglas en dos lugares; cada ajuste de paleta debe hacerse dos veces; y
nada garantiza que las dos copias describan la misma interfaz. La deriva
entre claro y oscuro no es un riesgo en esa arquitectura — es la trayectoria
por defecto.

La sustitución de tokens elimina la segunda copia. Hay un solo conjunto de
estilos de componente, escrito una vez contra nombres semánticos, y un mapa
compacto por tema que dice qué significan los nombres allí. El mapa del tema
son datos, así que puede validarse — verificarse su completitud contra el
listado semántico, verificarse contra los pisos de contraste — de una manera
en que una hoja de estilos paralela no puede.

## El mismo patrón en otros sistemas: Carbon, Material 3, Radix

Tres sistemas de uso extendido implementan la misma idea, lo que vale la pena
ver a la vez como antecedente y como confirmación de que el patrón soporta
carga a escala.

**IBM Carbon** estructura sus temas como intercambios de valores sobre un
vocabulario fijo de roles: cada tema comparte las mismas variables y roles, y
solo el valor cambia por tema. La documentación de color de Carbon es
explícita en que el cambio de modo solo es posible porque los tokens de color
se usan en todas partes — los valores codificados a mano simplemente no
responden cuando el tema cambia. Los productos eligen un tema claro y uno
oscuro del mismo conjunto de roles.

**Material Design 3** expresa su esquema como roles de color — las ranuras
con nombre a las que se adhieren los componentes —, y el sistema genera
valores de esquema claro y oscuro para cada rol, incluso a partir del color
de origen dinámico (derivado del fondo de pantalla) en Android. La capa de
roles es lo que permanece estable; los valores resueltos por esquema son lo
que cambia.

**Radix Colors** vincula las variables CSS de cada escala de color dos veces:
las escalas claras a `:root` y a una clase `.light`, las escalas oscuras a
una clase `.dark`. Los nombres de las variables son idénticos en ambas, de
modo que la misma regla de estilo se renderiza correctamente bajo cualquiera
de las dos clases — cambiar de tema es aplicar una clase a un contenedor, el
mismo gesto que el atributo `data-theme` de este sistema de diseño.

Las diferencias entre los cuatro (incluido PointSav) son superficiales —
selectores de atributo frente a clases, mapas ajustados a mano frente a
esquemas generados — y la invariante es la misma en todos: los componentes
consumen nombres de rol estables; los temas vuelven a vincular valores;
ningún componente se reescribe para ganar un tema.

## Qué significa esto para los inquilinos

El mismo mecanismo de sustitución que transporta el modo oscuro transporta la
tematización de marca. El grupo `theme` del paquete se describe a sí mismo
como la anulación de capa semántica de la marca PointSav y señala que los
clientes lo bifurcan como su propio archivo de tema, re-apuntando los mismos
roles semánticos hacia sus propios valores primitivos. El modo oscuro y el
recambio de marca de un inquilino son la misma operación a escalas
distintas: un mapa de nombres de rol estables a valores diferentes. Ese es el
argumento práctico para mantener disciplinado el nivel semántico — cada rol
que un componente consume es una ranura que un tema puede re-vincular, y
cada valor codificado a mano es un lugar donde la tematización falla en
silencio.

## Licencias: los datos y este artículo tienen licencias distintas

Como en todos los artículos de esta serie que citan el paquete de tokens:
los datos de tokens en sí — el JSON en formato DTCG del repositorio
`pointsav-design-system`, incluido el grupo `theme.dark` aquí descrito — se
licencian bajo Apache-2.0. El texto de este artículo, como parte del wiki de
documentación, se licencia bajo CC BY 4.0. Las dos licencias cubren dos
artefactos distintos; citar aquí nombres y valores de tokens no coloca este
texto bajo Apache-2.0, y reutilizar esta explicación no licencia el archivo
de tokens.

## Alcance y límites

Dicho con claridad: el mapa oscuro enviado está verificado, según sus propios
campos de descripción, en las superficies del wiki — extender la misma
verificación de contraste a otras superficies es trabajo abierto, no una
afirmación completada. Las anulaciones oscuras llevan valores hexadecimales
literales anotados con el paso primitivo al que corresponden, en lugar de
alias vivos hacia la capa primitiva; esa es una consideración de
mantenimiento (un cambio en un primitivo no se propaga automáticamente al
mapa oscuro) registrada como pregunta abierta, no ocultada. Y la sección
comparativa anterior describe Carbon, Material 3 y Radix como antecedentes a
partir de su documentación pública; afirma similitud de patrón, no
equivalencia de alcance o calidad entre esos sistemas y este.

---

*Este artículo es material de contexto sobre el mecanismo de tematización
del Sistema de Diseño PointSav. Para qué es un token y la arquitectura de
tres niveles, véase [[what-is-a-design-token|Qué es un token de diseño]].
Para la implementación del modo oscuro en la superficie del wiki —
conmutador, persistencia, manejo del primer renderizado — véase
[[wiki-dark-mode|el artículo sobre el modo oscuro del wiki]].*
