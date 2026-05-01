---
schema: foundry-topic-v1
title: "Colaboración en tiempo real mediante relé de paso — un patrón de sustrato"
status: published
category: architecture
last_edited: 2026-04-30
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
companion: architecture/collab-via-passthrough-relay.md
cites:
  - doctrine-claim-29
  - doctrine-claim-16
---

## El patrón en un párrafo

El patrón de relé de paso invierte la suposición habitual sobre dónde reside la autoridad en un sistema de edición colaborativa: el servidor de relé no conserva ningún estado de documento, por lo que el árbol git canónico sigue siendo el único registro autoritativo del contenido de cada tema en todo momento. Los editores concurrentes se conectan mediante WebSocket a un canal `tokio::sync::broadcast` identificado por slug — una sala de difusión por documento — y la única responsabilidad del servidor es reenviar mensajes de actualización del protocolo CRDT de Yjs entre esos clientes. El servidor nunca decodifica ni almacena el estado del documento que esos mensajes codifican. El único límite de persistencia en todo el sistema es la ruta de escritura atómica `POST /edit/{slug}`: cuando un editor guarda, el cliente serializa su documento Yjs local a Markdown, lo envía por HTTP, y el servidor mueve atómicamente el nuevo archivo a su lugar en disco — la misma operación que un guardado de un solo autor.

## Por qué un relé de paso, no un servidor CRDT

Herramientas como Etherpad y HackMD operan bajo un modelo de documento autoritativo en el servidor: el servidor de edición colaborativa mantiene un objeto de documento vivo y mutable, y ese objeto es el registro principal del contenido actual. Una exportación a git es una instantánea tomada de ese registro del servidor, no al revés. La consecuencia es un segundo estado autoritativo permanente: dos lugares en el sistema contienen la respuesta a la pregunta "¿cuál es el texto actual de este documento?", y pueden divergir si el mecanismo de exportación falla o el registro CRDT del servidor difiere del historial de git.

El diseño de relé de paso elimina ese segundo registro por completo. El servidor es un conducto de mensajes, no un almacén. Cuando un cliente Yjs envía un mensaje de actualización binario, el manejador Rust recibe los bytes en bruto del WebSocket y los difunde a todos los demás clientes de la misma sala mediante `tokio::sync::broadcast`. El servidor nunca deserializa el protocolo Yjs; nunca construye un Y.Doc; nunca escribe nada en disco como efecto secundario de una operación de relé.

Esto importa para la postura de divulgación descrita en la reclamación #29 de Doctrine (Sustitución de Sustrato). El registro de divulgación canónico es el árbol git. Bajo el diseño de relé de paso, no existe ningún registro paralelo: el estado CRDT en curso no forma parte del registro de divulgación por construcción, porque nunca se escribe en ningún lugar. El registro se cierra en el momento de `POST /edit`, no antes.

## Implementación en `app-mediakit-knowledge`

El relé de colaboración se implementó como `src/collab.rs`, restringido por el indicador CLI `--enable-collab`. Cuando el indicador está ausente — la configuración predeterminada y la postura de producción actual en v0.1.29 — la ruta WebSocket `GET /ws/collab/{slug}` no se registra en el enrutador axum, y el paquete JavaScript del lado del cliente nunca se carga. Ninguna ruta de código de colaboración se ejecuta en la configuración desactivada por defecto.

El relé del lado del servidor usa `tokio::sync::broadcast`. Cada slug obtiene su propio canal de difusión con capacidad de 256 mensajes. Cuando un cliente WebSocket envía un mensaje de actualización de Yjs, el manejador lee los bytes en bruto y llama a `sender.send(bytes)` — una sola línea que distribuye el mensaje a todos los demás receptores del canal. No hay dependencia del crate `yrs`: el servidor reenvía mensajes binarios sin deserializarlos, por lo que no porta ningún estado de documento en ningún momento.

El paquete cliente `cm-collab.bundle.js` está construido a partir de tres paquetes npm: `yjs`, `y-codemirror.next` e `y-websocket`. El paquete se confirma como un artefacto precompilado, por lo que no se requiere ninguna cadena de herramientas npm en tiempo de ejecución.

## Lo que esto significa para la divulgación

El estado CRDT en curso — la secuencia de mensajes de actualización de Yjs intercambiados entre clientes durante una sesión de colaboración — no forma parte del registro de divulgación y no puede serlo, por construcción. Dado que el relé nunca persiste esos mensajes, no existe ningún artefacto del lado del servidor que pudiera producirse en respuesta a una obligación de divulgación. La sesión de colaboración no deja ningún estado en el servidor.

Las ediciones guardadas ingresan al registro de divulgación a través de la misma ruta que todas las demás ediciones: `POST /edit/{slug}` envía el texto Markdown completo del documento, el servidor realiza un renombrado atómico del archivo, y el siguiente commit git captura esa instantánea. Desde la perspectiva de git, un guardado editado en colaboración es idéntico a un guardado de un solo autor.

## El patrón más allá del wiki

El relé de paso es un patrón de sustrato, no una característica específica del wiki. Cualquier servicio que desee semánticas de edición concurrente enfrenta la misma pregunta arquitectónica: ¿necesita la infraestructura de colaboración mantener el estado del documento en el servidor, o puede ese estado residir completamente en los clientes y en el almacenamiento canónico?

El patrón aplica directamente cuando el tipo de documento CRDT se mapea con claridad al tipo de almacenamiento canónico. Para `service-extraction` (registros estructurados) y las aplicaciones `app-workplace-presentation` y `app-workplace-proforma` (planificadas), el mismo principio guía la decisión de diseño: si un servidor CRDT con estado competiría con el almacén canónico por la autoridad, el relé de paso es la respuesta preferida.

## Véase también

- [[topic-source-of-truth-inversion]] — La taxonomía de tres capas (canónica / vista / efímera) que este patrón instancia.
- [[topic-app-mediakit-knowledge]] — Arquitectura del motor wiki que implementa este patrón.
- [[topic-substrate-native-compatibility]] — Por qué el motor wiki no imita interfaces existentes.
- [[topic-disclosure-substrate]] — La convención de postura de divulgación que este diseño satisface.

## Procedencia

Versión en español elaborada por project-language el 2026-04-30, basada en el borrador de project-knowledge (sesión 619abe3eff24497e, 2026-04-28). Vista general estratégica por DOCTRINE.md §XII — no es una traducción literal del inglés canónico.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
