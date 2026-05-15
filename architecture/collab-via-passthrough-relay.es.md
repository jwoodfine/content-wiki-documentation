---
schema: foundry-doc-v1
title: "Colaboración en tiempo real mediante relé de paso"
slug: collab-via-passthrough-relay.es
category: architecture
type: topic
quality: complete
short_description: "El patrón de relé de paso para la edición colaborativa en tiempo real: el servidor no conserva ningún estado de documento, git permanece como único registro canónico, y el estado CRDT es efímero de sesión por construcción."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: collab-via-passthrough-relay.md
references:
 - id: 1
 text: "Yjs — Biblioteca de tipos de datos replicados sin conflictos para aplicaciones colaborativas."
 url: "https://github.com/yjs/yjs"
 - id: 2
 text: "y-codemirror.next — Enlace de Yjs para CodeMirror 6."
 url: "https://codemirror.net/"
 - id: 3
 text: "tokio::sync::broadcast — Documentación del canal multi-productor multi-consumidor de Tokio."
 url: "https://docs.rs/tokio/latest/tokio/sync/broadcast/"
---

## Adaptación estratégica

El patrón de relé de paso invierte la suposición habitual sobre dónde reside la autoridad en un sistema de edición colaborativa: el servidor de relé no conserva ningún estado de documento, por lo que el árbol git canónico sigue siendo el único registro autoritativo del contenido de cada artículo en todo momento. Los editores concurrentes se conectan mediante WebSocket a un canal `tokio::sync::broadcast` identificado por slug — una sala de difusión por documento — y la única responsabilidad del servidor es reenviar mensajes de actualización del protocolo CRDT de Yjs entre esos clientes.[^1] El único límite de persistencia en todo el sistema es la ruta de escritura atómica `POST /edit/{slug}`: cuando un editor guarda, el cliente serializa su documento Yjs local a Markdown, lo envía por HTTP y el servidor mueve atómicamente el nuevo archivo a su lugar en disco.

## Por qué un relé de paso en lugar de un servidor CRDT

Herramientas como Etherpad y HackMD operan bajo un modelo de documento autoritativo en el servidor: el servidor de edición colaborativa mantiene un objeto de documento vivo y mutable, y ese objeto es el registro principal del contenido actual. Una exportación a git es una instantánea tomada de ese registro del servidor, no al revés. La consecuencia es un segundo estado autoritativo permanente: dos lugares en el sistema contienen una respuesta a la pregunta "¿cuál es el texto actual de este documento?", y pueden divergir si el mecanismo de exportación falla o el registro CRDT difiere del historial de git.

El diseño de relé de paso elimina ese segundo registro por completo. El servidor es un conducto de mensajes, no un almacén. Cuando un cliente Yjs envía un mensaje de actualización binario a `GET /ws/collab/{slug}`, el manejador Rust recibe los bytes en bruto y los difunde a todos los demás clientes de la misma sala de slug mediante `tokio::sync::broadcast`.[^3] El servidor nunca deserializa el protocolo Yjs; nunca construye un Y.Doc; nunca escribe nada en disco como efecto secundario de una operación de relé.

Esto importa para la postura de divulgación. El registro de divulgación canónico en este sistema es el árbol git. Bajo el diseño de relé de paso, no existe ningún registro paralelo: el estado CRDT en curso no es parte del registro de divulgación por construcción, porque nunca se escribe en ningún lugar. El registro se cierra en el momento de `POST /edit`, no antes.

## Implementación en app-mediakit-knowledge

El relé de colaboración se implementó en el commit `05f1dab` como `src/collab.rs`, completamente restringido por el indicador CLI `--enable-collab`. Cuando el indicador está ausente — configuración predeterminada y postura de producción actual en v0.1.29 — la ruta WebSocket no se registra en el enrutador axum, la variable de plantilla `window.WIKI_COLLAB_ENABLED` se establece en `false`, y el paquete JavaScript del lado del cliente nunca se carga.

El relé del lado del servidor se implementa mediante `tokio::sync::broadcast`. Cada slug obtiene su propio canal de difusión con una capacidad de búfer de 256 mensajes, creado en la primera conexión y almacenado en un `DashMap<String, broadcast::Sender<Bytes>>` en `AppState`.[^3] Cuando un cliente WebSocket envía un mensaje de actualización de Yjs, el manejador lee los bytes en bruto y llama a `sender.send(bytes)` — una sola línea que distribuye el mensaje a todos los demás receptores de ese canal. No hay dependencia del crate `yrs`: el servidor reenvía mensajes binarios del protocolo Yjs sin deserializarlos, por lo que el servidor no porta ningún estado de documento en ningún momento.

El paquete cliente `cm-collab.bundle.js` (aproximadamente 302 KB tal como fue entregado) está construido a partir de tres paquetes npm: `yjs`, `y-codemirror.next`[^2] e `y-websocket`, todos incluidos como artefacto precompilado en `static/vendor/`. El script de inicialización `static/saa-init.js` verifica `window.WIKI_COLLAB_ENABLED` en tiempo de carga; si el indicador es `false`, la importación del paquete de colaboración nunca se ejecuta. El editor CodeMirror se carga completamente en cualquier caso — la colaboración es aditiva a la superficie de edición, no un requisito previo.

La cobertura de pruebas en el commit `05f1dab` agregó 7 pruebas (3 unitarias, 4 de integración) para elevar el total de 90 a 97. Las pruebas unitarias cubren la aceptación de conexiones WebSocket cuando se establece `--enable-collab`, la multiplexación correcta entre dos clientes en el mismo slug, el vaciado del búfer de 256 mensajes sin pánico, y la carga del paquete cliente solo cuando se establece el indicador. La cobertura no incluye la propiedad visual de presencia del cursor, que requiere un proceso de verificación manual con dos navegadores.

## Límites deliberados del servidor

A efectos de evaluación de seguridad y arquitectura, lo que el relé deliberadamente omite:

**Sin crate `yrs` ni estado de documento en el servidor.** El servidor reenvía mensajes binarios del protocolo Yjs sin deserializarlos. La semántica del documento Yjs reside íntegramente en el lado del cliente.

**Sin persistencia de estado CRDT en ningún punto de la ruta de relé.** El único escrito en disco en toda la ruta de colaboración es el `POST /edit/{slug}` iniciado por el cliente.

**Sin identidad portadora de autenticación que dure más que la vida útil del WebSocket.** Los identificadores de color de cursor visibles en la interfaz de usuario de colaboración se generan del lado del cliente y no se almacenan.

**Sin historial de edición accesible desde el servidor.** El único historial de edición que existe es el registro de commits git producido por los guardados sucesivos de `POST /edit`.

## Lo que esto significa para la postura de divulgación

El estado CRDT en curso — la secuencia de mensajes de actualización de Yjs intercambiados entre clientes durante una sesión de colaboración — no forma parte del registro de divulgación y no puede serlo, por construcción. Dado que el relé nunca persiste esos mensajes, no existe ningún artefacto del lado del servidor que pudiera producirse posteriormente en respuesta a una obligación de divulgación.

Las ediciones guardadas ingresan al registro de divulgación a través de la misma ruta que todas las demás ediciones: `POST /edit/{slug}` envía el texto Markdown completo del documento, el servidor realiza un renombrado atómico del archivo, y el siguiente commit git captura esa instantánea. Desde la perspectiva de git, un guardado editado en colaboración es idéntico a un guardado de un solo autor. La unidad de divulgación es el estado del documento confirmado, no la descomposición de autoría de cómo se alcanzó ese estado.

La ruta de reversión del indicador `--enable-collab` no es destructiva en ninguna capa, precisamente debido a este diseño. La superposición CRDT de colaboración es efímera por construcción; su eliminación al reiniciar el servicio no es un evento de pérdida de datos. Cualquier contenido guardado antes del reinicio existe en el árbol git y es completamente recuperable.

## Generalización más allá del wiki

El relé de paso es un patrón de sustrato, no una característica específica del wiki. Cualquier servicio que desee semánticas de edición concurrente enfrenta la misma pregunta arquitectónica: ¿necesita la infraestructura de colaboración mantener el estado del documento en el servidor, o puede ese estado residir completamente en los clientes y en el almacenamiento canónico?

**Revisión multiautor en la canalización de extracción.** El almacenamiento canónico para los resultados de extracción son los registros estructurados producidos por combinadores de análisis deterministas. Si el servidor CRDT materializa correcciones parciales no confirmadas de vuelta al almacén estructurado, el patrón de relé de paso no aplicaría directamente sin una capa adaptadora. El patrón aplica en su forma más simple solo cuando el tipo de documento CRDT se corresponde limpiamente con el tipo de almacenamiento canónico.

**Colaboración en presentaciones.** El patrón de relé de paso aplica si y solo si el archivo de presentación en disco es el registro canónico y la superposición CRDT se trata como efímera de sesión sobre él.

**Colaboración en tablas de proforma.** Si el almacenamiento canónico del proforma son datos confirmados en git y la superposición CRDT es efímera de sesión, el patrón aplica con la misma lógica que el caso del wiki. La diferencia es que el paso de serialización en el guardado debe producir datos estructurados válidos, añadiendo un requisito de validación en el momento del guardado.

## Véase también

- [[app-mediakit-knowledge]] — el motor wiki; implementación de colaboración en la sección de fases de construcción
- [[source-of-truth-inversion]] — el patrón canónico / vista / efímero del que depende este diseño
- [[substrate-native-compatibility]] — la postura nativa del sustrato en términos más amplios
