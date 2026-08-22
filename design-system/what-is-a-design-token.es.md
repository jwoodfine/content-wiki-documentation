---
schema: foundry-doc-v1
title: "Qué es un token de diseño"
slug: what-is-a-design-token
short_description: "Artículo introductorio que define los tokens de diseño, el Format Module del Design Tokens Community Group del W3C (primera versión estable, octubre de 2025) y la arquitectura de tres niveles primitivo/semántico/componente, fundamentado en el paquete DTCG publicado del Sistema de Diseño PointSav (130 primitivos + 86 de tema, más los pilares separados de papel y escritura)."
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
paired_with: what-is-a-design-token.md
cites: []
---

Un token de diseño es una decisión de diseño registrada como datos: un
nombre, un valor y — en un sistema maduro — un tipo y una descripción que
explica cuándo usarlo. La decisión "nuestro color interactivo primario es
este azul específico" se convierte en una entrada de un archivo JSON, en
lugar de un código hexadecimal repetido por las hojas de estilos. Todo lo que
está aguas abajo — CSS, bibliotecas de componentes, sitios de documentación,
plataformas nativas — consume la entrada por su nombre, de modo que la
decisión se toma una vez y se referencia en todas partes.

El Sistema de Diseño PointSav publica sus tokens como un único paquete
legible por máquina, `tokens.full.json`. El paquete ha crecido más allá de
su forma original de dos grupos: ahora reúne cuatro pilares de nivel
superior — `primitive` (130 tokens hoja), `theme` (86, repartidos en 53
roles semánticos del tema claro, 28 entradas del modo oscuro y 5
anulaciones específicas de accesibilidad) y dos pilares que el alcance
original de este artículo no cubría, `paper` (383, tokens de impresión/
documentos) y `writing` (37, tokens de contenido editorial). Los recuentos
siguientes describen los pilares `primitive` y `theme`, que son de lo que
trata realmente este artículo; como cualquier paquete vivo, el recuento
exacto de tokens se mueve conforme crece el sistema de diseño, y el
archivo mismo —no una cifra fija en este artículo— es la fuente
autorizada.

## Una decisión con nombre

La forma más simple de ver qué aporta un token es comparar las dos maneras de
escribir el mismo botón. Sin tokens, una hoja de estilos dice
`background: #234ed8` — un valor sin historia y sin significado. Si el color
de marca cambia, hay que localizar y editar cada aparición, y nada distingue
las apariciones que significaban "acción primaria" de las que usaban el mismo
azul por una razón sin relación.

Con tokens, la hoja de estilos referencia un nombre, y el nombre porta la
intención. En el paquete PointSav publicado, `#234ed8` existe en exactamente
un lugar: el token primitivo `primitive.color.primary-60`. Un token
semántico, `theme.semantic.interactive-primary`, lo señala por alias —
`{color.primary-60}` — y los botones consumen el nombre semántico. Se cambia
el primitivo una vez y toda superficie que significa "interactivo primario"
lo sigue; las superficies que significaban otra cosa quedan intactas porque
referencian otro nombre.

Los tokens también llevan la documentación consigo. El token de duración
`speed-2` del paquete no es solo `120ms`; su campo de descripción dice
"Quick — button press, focus ring fade" (rápido — pulsación de botón,
desvanecimiento del anillo de foco). El token de espaciado `space-3` registra
"8px @ 16px base — paragraph rhythm floor" (piso del ritmo de párrafo). La
regla de uso viaja con los datos, donde una herramienta de compilación, un
linter o un agente de IA que lea el archivo en el momento de la generación
puede verla — no en una guía de estilo que deriva por separado.

## Un formato para todas las herramientas: el DTCG Format Module

Durante la mayor parte de la última década, cada herramienta de tokens usó su
propia forma de archivo. Eso terminó cuando el Design Tokens Community Group,
un grupo comunitario del W3C, publicó la primera versión estable de su Format
Module — la versión 2025.10 —, anunciada el 28 de octubre de 2025. La
especificación define un formato JSON neutral respecto de los proveedores:
los tokens declaran `$value`, `$type` y `$description`; los grupos se anidan;
los alias usan referencias entre llaves como `{color.primary-60}`; y la
versión estable añadió soporte para espacios de color modernos y para la
tematización y la herencia multi-marca. Las herramientas de diseño y las
cadenas de tokens de ambos lados — diseño e ingeniería — soportan el formato,
que es lo que convierte un archivo de tokens en un artefacto de intercambio
portátil y no en una convención privada.

El paquete PointSav está escrito conforme a esta especificación y la declara
explícitamente: ambos grupos de nivel superior llevan
`"$schema": "https://schemas.designtokens.org/2025-10-01/draft.json"`. El
paquete usa los mecanismos centrales de la especificación — grupos tipados,
campos de descripción y alias entre llaves — y todavía no usa la función más
nueva de herencia de grupos `$extends`; esa evaluación está pendiente, y se
registra en las preguntas abiertas de este artículo en lugar de pasarse por
alto.

## Tres niveles: primitivo, semántico, componente

La arquitectura en la que el campo ha convergido — y la que este sistema de
diseño enseña en su página de fundamentos — organiza los tokens en tres
niveles, cada uno de los cuales responde una pregunta distinta.

**Los tokens primitivos responden "¿qué valores existen?"** Son la paleta en
bruto: opciones, no decisiones de uso. El ejemplo didáctico del sitio de
documentación es `ps-blue-600: #234ed8` — un azul con una posición en la
escala y sin opinión sobre dónde aparece. En el paquete publicado este nivel
es el grupo `primitive`: 60 colores en familias con nombre de rol
(`primary`, `neutral`, `positive`, `caution`, `critical`, cada una en una
escala numérica 10–100, más negro y blanco), una escala de espaciado de 13
pasos, 14 estilos tipográficos, 6 duraciones, 4 curvas de aceleración, 5
dimensiones de borde, 3 puntos de quiebre de viewport, un compuesto de
anillo de foco, y un conjunto de subgrupos de superficie, elevación y
elementos de sitio (surface, elevation, brand-accent, category-tile,
footer) añadidos desde el alcance original de este artículo — 130 tokens
en total.

**Los tokens semánticos responden "¿qué significa este valor aquí?"** Toman
un primitivo por alias y le adjuntan un rol. El ejemplo didáctico es
`cds-interactive: {ps-blue-600}` — "todo aquello sobre lo que una persona
puede actuar". La contraparte del paquete es
`theme.semantic.interactive-primary: {color.primary-60}`, uno de 53 roles
semánticos que cubren superficies (`surface-base`, `surface-elevated`),
texto ("ink", tinta, en el vocabulario de este sistema: `ink-primary`,
`ink-secondary`), bordes, foco, estados interactivos con sus variantes de
hover y presionado, y colores de estado. El nivel semántico es donde vive un
tema: un inquilino re-apunta los alias hacia sus propios primitivos sin
tocar ningún componente. El artículo complementario sobre tematización cubre
este mecanismo en detalle.

**Los tokens de componente responden "¿qué usa esta parte específica?"** El
ejemplo didáctico es `btn-primary-bg: {cds-interactive}` — este botón, esta
superficie, nada más. Acotar un nombre más a un componente cuesta una línea
y compra precisión: si alguna vez solo los botones primarios necesitan
divergir, se re-apunta un alias y nada más se mueve. Una salvedad honesta,
dicha con claridad: el paquete exportado envía actualmente los niveles
primitivo y semántico; el nivel de componente existe como la convención de
nomenclatura documentada que consumen las recetas de componentes, no como un
tercer grupo dentro de `tokens.full.json`. La cadena
`ps-blue-600 → cds-interactive → btn-primary-bg` es la manera en que el
sitio enseña la arquitectura; los dos primeros eslabones soportan carga en
los datos publicados hoy, y formalizar el tercero en la exportación es una
decisión abierta.

La dirección de las referencias es la disciplina que mantiene coherente el
grafo: los componentes apuntan a los semánticos, los semánticos apuntan a
los primitivos, y nada apunta en sentido contrario. Un componente nunca pasa
por encima del nivel semántico para tomar `primary-60` directamente, porque
hacerlo vuelve a incrustar el valor en bruto que el sistema de tokens existe
para centralizar.

## Por qué esta estructura se gana su lugar

La estructura de tres niveles no es un invento de PointSav, y este sistema de
diseño no afirma lo contrario: las escalas primitivas numéricas, los alias
semánticos y el acotamiento por componente son el vocabulario compartido del
campo moderno de los sistemas de diseño, formalizado por el modelo de alias
de la especificación DTCG. Lo que la estructura compra a cualquier adoptante
es lo mismo: decisiones tomadas una sola vez; intención legible en el nombre;
temas expresados como sustitución en lugar de duplicación; y un archivo que
las herramientas y los agentes pueden consumir sin que un humano interprete
una guía de estilo. El artículo de vocabulario primitivo del sistema de
diseño documenta por separado qué patrones estructurales se conservaron del
campo y qué nombres y valores son originales de PointSav, de modo que quien
llegue desde otros sistemas sepa qué le resultará familiar y por qué.

## Licencias: los datos y este artículo tienen licencias distintas

Aquí hay dos artefactos en juego, bajo dos licencias distintas, y la
precisión sobre cuál es cuál importa. Los datos de tokens en sí — el paquete
JSON en formato DTCG del repositorio `pointsav-design-system` — se publican
bajo Apache-2.0, siguiendo la convención de los sistemas de diseño de código
abierto. El texto de este artículo, como el resto del wiki de documentación
al que pertenece, se licencia bajo CC BY 4.0. Ninguna de las dos licencias se
extiende al otro artefacto: reutilizar el archivo de tokens es una cuestión
de Apache-2.0; reutilizar o adaptar esta explicación es una cuestión de
CC BY 4.0.

## Alcance y límites

Dicho con claridad: los recuentos y valores de tokens citados aquí describen
el paquete PointSav publicado al momento de escribir, y fueron recalculados
desde el archivo durante la redacción; derivarán a medida que el paquete
evolucione, y el archivo — no este artículo — es la fuente autorizada. El
nivel de componente es una convención documentada y no un grupo enviado en la
exportación. Y el paquete ejercita el núcleo del DTCG 2025.10, no el conjunto
completo de funciones de la especificación. Cada uno de estos puntos es un
estado, no un defecto, y este sistema de diseño prefiere publicar los estados
a la vista.

---

*Este artículo es material introductorio para quien llega por primera vez a
los tokens de diseño, previo al material de referencia del sistema de
diseño. Para entender por qué el vocabulario primitivo es como es, véase el
artículo de fundamentos del vocabulario primitivo; para el funcionamiento de
los temas, véase "Tematización mediante tokens semánticos".*
