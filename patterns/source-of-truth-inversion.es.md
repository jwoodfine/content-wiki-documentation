---
schema: foundry-doc-v1
title: "Inversión de la fuente de verdad"
slug: source-of-truth-inversion
short_description: "La inversión de origen de verdad designa una capa de almacenamiento como canónica (el registro autorizado, comprometido y firmado), una segunda como una vista derivada (reconstruida determinísticamente bajo demanda), y una tercera como efímera de sesión (estado colaborativo descartado hasta confirmación explícita)."
status: active
category: patterns
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-infrastructure-patterns
language: es
last_edited: 2026-08-24
editor: pointsav-engineering
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
paired_with: source-of-truth-inversion.md
cites:
 - ni-51-102
 - np-51-201
---

## Descripción del patrón

La inversión de la fuente de verdad es un patrón de diseño nombrado de la plataforma. En cada aplicación de PointSav, una capa de almacenamiento se declara canónica — el registro autoritativo que se confirma, se firma, se replica y se divulga. Una segunda capa es una vista derivada: el índice en memoria del proceso en ejecución, la salida renderizada o el resumen computado — reconstruido de forma determinista desde el registro canónico bajo demanda y descartable sin pérdida de información. Una tercera capa, cuando la edición colaborativa está activa, es efímera de sesión: existe durante la duración de una sesión de edición compartida y no escribe de vuelta al canónico hasta que un autor humano realiza un commit deliberado. La capa canónica es típicamente el [[worm-ledger-design|libro mayor WORM]] o un árbol git firmado, según la aplicación.

El patrón se repite en el motor wiki, en la canalización de extracción de Ring 2, y en las aplicaciones planificadas `app-workplace-presentation` y `app-workplace-proforma`. En cada caso, la elección de qué es canónico sigue la misma lógica estructural: la capa con el mayor requisito de durabilidad, la obligación de auditoría más fuerte y la historia de replicación más limpia es la canónica. Todo lo demás es derivado.

**Por qué importa:** un lector nunca tiene que preguntarse cuál copia de un registro es la real — la capa canónica siempre está nombrada, y cualquier otra capa puede eliminarse y reconstruirse sin perder nada que alguna vez haya sido autoritativo.

## Aplicación: motor wiki (instancia ancla)

El tratamiento completo de la inversión de la fuente de verdad en el motor wiki aparece en [[app-mediakit-knowledge]] §2. El resumen aquí: git es canónico, el binario en ejecución es una vista, y la histórica [[collab-via-passthrough-relay|superposición CRDT de relé de paso]] — desde entonces eliminada del motor — fue la capa efímera de sesión mientras existió.

El índice de búsqueda de texto completo Tantivy, el grafo de wikilinks redb (planificado, Fase 4) y todo el HTML renderizado se derivan bajo demanda del árbol de Markdown en disco. Cualquiera de estos artefactos derivados puede descartarse y reconstruirse; ninguno se respalda; ninguno se divulga. El árbol git es lo que se respalda, replica, firma y divulga. El binario no puede acumular estado que el árbol git no tenga.

Este caso fundamenta el patrón con un despliegue en vivo: `https://documentation.pointsav.com` ha servido este sustrato desde el 2026-04-27.

**Por qué importa:** el servidor en ejecución puede fallar, redesplegarse o reemplazarse por completo, y ningún contenido de artículo corre riesgo — todo lo que ve el lector se reconstruye desde el mismo árbol git cada vez.

## Aplicación: service-extraction (canalización de revisión multiautor de Ring 2)

`service-extraction` es el servicio de Ring 2 que ejecuta la canalización de revisión de documentos multiautor. El mapeo de fuente de verdad:

**Canónico**: el registro de eventos de extracción confirmado en el libro mayor WORM inmutable gestionado por `service-fs`. Un evento de extracción queda secuenciado de forma durable en el momento en que se añade al libro mayor; este aplica un orden total sobre todos los eventos. Las entradas del libro mayor no son modificables después del hecho — eso es lo que significa WORM (Write Once Read Many) estructuralmente, no solo operativamente. El libro mayor WORM como almacenamiento canónico sigue la preferencia general del sustrato por registros firmados de solo-adición: en lugar de una base de datos relacional mutable como autoridad para el estado de revisión, el sustrato es un registro firmado de solo-adición.

**Vista**: la cola de revisión mostrada a cada revisor se deriva del conjunto de entradas del libro mayor que aún no han recibido un commit de veredicto. El resumen de veredicto por revisor se deriva de forma similar. Ni la cola ni el resumen se almacenan por separado — ambos se rederivan en cada consulta desde el libro mayor. La derivación es determinista: el mismo libro mayor produce la misma cola y el mismo resumen cada vez que se consulta, porque el libro mayor es inmutable y de orden total.

**Efímero**: las anotaciones de un revisor hechas antes de un commit de veredicto son efímeras de sesión. Las anotaciones de trabajo de un revisor no pueden ver ni corromper las de otro revisor, porque esas anotaciones todavía no se han confirmado en el libro mayor canónico. Los revisores concurrentes trabajan contra su propio estado en proceso; el libro mayor concilia cuando llega un commit de veredicto. La aplicación de orden total del libro mayor es el mecanismo del sustrato que hace segura la revisión concurrente sin bloqueos de coordinación.

**Por qué importa:** dos revisores trabajando la misma cola en el mismo momento nunca pueden producir un registro de revisión corrupto o ambiguo — el orden total del libro mayor resuelve el resultado de forma determinista, sin que ninguno de los dos necesite coordinarse con el otro.

## Aplicación: app-workplace-presentation (colaboración en presentaciones, planificado)

`app-workplace-presentation` es una aplicación planificada para la autoría colaborativa de presentaciones de diapositivas. El mapeo de fuente de verdad previsto sigue el mismo patrón:

**Canónico**: el origen de la presentación, previsto para confirmarse en el repositorio git del cliente — el repositorio git del cliente es la autoridad canónica para el contenido de la presentación, no un servidor de documentos propietario. Un commit al repositorio git de la presentación es el evento de divulgación; el historial git de la presentación es el registro de auditoría.

**Vista**: los cuadros de diapositiva renderizados y servidos a los clientes de navegador, calculados a partir del origen confirmado bajo demanda. Los cuadros renderizados no se almacenan de forma persistente; se reconstruyen desde el origen confirmado en cada solicitud.

**Efímero**: el estado CRDT de colaboración multi-cursor para sesiones de coautoría en tiempo real está planificado como efímero de sesión, sobre el mismo diseño de relé de paso que el motor wiki alguna vez ejecutó — la implementación propia del wiki ha sido eliminada desde entonces, pero el diseño en sí sigue siendo la referencia para esta capa planificada. Ese estado de sesión no persiste entre sesiones sin un commit explícito de un autor humano. Cuando todos los autores abandonan la sesión, el estado efímero se descarta; el registro canónico en git no cambia. La capa de colaboración CRDT para `app-workplace-presentation` está planificada; todavía no está implementada.

**Por qué importa:** se prevé que varios autores puedan coeditar una presentación en tiempo real sin que ninguno de ellos arriesgue la versión confirmada — una sesión de colaboración que termina mal pierde solo las ediciones en curso, nunca el último estado confirmado de la presentación.

## Aplicación: app-workplace-proforma (colaboración en tablas, planificado)

`app-workplace-proforma` es una aplicación planificada para la edición colaborativa de datos estructurados — tablas proforma, calendarios financieros y documentos estructurados usados en contextos de negocio regulados. El mapeo de fuente de verdad:

**Canónico**: la tabla proforma, prevista para confirmarse como datos estructurados (CSV o Markdown estructurado con una declaración de esquema) en el repositorio Git del cliente. La declaración de esquema viaja con los datos, haciendo que el artefacto confirmado sea autodescriptivo.

**Vista**: la interfaz de tabla renderizada con campos calculados — totales, referencias entre filas, formato condicional — derivados de los datos estructurados canónicos en cada renderizado. Los campos calculados no se almacenan en el registro canónico; se rederivan. Esto importa en contextos proforma donde un cambio de fórmula debe producir valores derivados consistentes en todos los lugares donde se referencia la fórmula, sin que sea posible ningún valor obsoleto en caché porque la caché no es canónica.

**Efímero**: el estado CRDT de colaboración a nivel de celda durante sesiones de edición compartida está planificado como efímero de sesión, siguiendo el mismo modelo de persistencia condicionada por commit que `app-workplace-presentation`. Nada persiste al registro canónico hasta un commit explícito. La cifra autoritativa es la que está confirmada y firmada en git — no el valor renderizado en una pestaña de navegador que puede reflejar ediciones de sesión sin guardar. El patrón hace cumplir esa distinción de forma estructural: la única forma de cambiar el registro canónico es un commit. Nota: la capa de colaboración CRDT para `app-workplace-proforma` está planificada; todavía no está implementada a partir de 2026-04-27.

**Por qué importa:** en un contexto regulado de modelado financiero, "qué cifra realmente usamos" siempre tiene una sola respuesta inequívoca — la cifra confirmada y firmada en git, nunca un valor sin guardar que un colaborador estuviera viendo en ese momento.

## Por qué este patrón importa

**Postura de divulgación continua BCSC.** En cada aplicación, lo canónico es el estado divulgado. Conforme a los requisitos de divulgación continua de [ni-51-102], el registro que se divulga es el que está firmado, confirmado y replicado — no la vista renderizada, no el índice de búsqueda, no el búfer CRDT efímero de sesión. La inversión de la fuente de verdad hace cumplir esto por construcción: el sustrato no puede divulgar accidentalmente un artefacto de capa de vista como autoritativo, porque la vista no es el registro por definición. La trazabilidad de auditoría para cualquier afirmación divulgada es un `git log`; la afirmación vive en un commit firmado. Esta propiedad no se logra por política — es una consecuencia estructural de la designación de la capa de almacenamiento.

**Almacenamiento canónico agnóstico al kernel.** El diseño de dos sustratos de la plataforma requiere que los mismos binarios `os-*` se ejecuten en ambos fondos del sustrato (seL4 nativo y NetBSD de compatibilidad) mediante un shim delgado. La consecuencia a nivel de aplicación es que el almacenamiento canónico debe ser agnóstico al kernel: un árbol git firmado y una entrada de libro mayor WORM firmada son registros válidos independientemente de qué kernel del sistema operativo ejecute el proceso de vista. La inversión de la fuente de verdad logra esto — al mantener el registro canónico como datos estructurados firmados (commits de git, entradas de libro mayor) y la vista como un proceso derivado, los binarios del sustrato pueden moverse entre fondos sin que el registro canónico cambie de identidad. El diseño más profundo de seL4/NetBSD se trata en [[substrate-native-compatibility]]; la conexión aquí es solo la afirmación del almacenamiento canónico agnóstico al kernel.

El patrón no es específico de una aplicación. Se repite porque la misma lógica estructural aplica dondequiera que un sustrato necesite un registro de auditoría claro, una historia de replicación limpia y colaboración que no corrompa el estado canónico. Las cuatro aplicaciones anteriores son cuatro instancias de un patrón, no cuatro decisiones de diseño independientes.

## Véase también

- [[app-mediakit-knowledge]] — instancia base del patrón (git como canónico)
- [[collab-via-passthrough-relay]] — la capa efímera de sesión en detalle
- [[worm-ledger-design]] — el sustrato del libro mayor WORM utilizado como almacenamiento canónico en la canalización de Ring 2
- [[substrate-native-compatibility]] — almacenamiento canónico agnóstico al kernel en el contexto del sustrato soberano
- [[disclosure-substrate]] — la convención de postura de divulgación que este patrón satisface

