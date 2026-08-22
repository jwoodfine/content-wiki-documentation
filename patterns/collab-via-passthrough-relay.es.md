---
schema: foundry-doc-v1
title: "Colaboración mediante relé de paso — un patrón de sustrato retirado"
slug: collab-via-passthrough-relay
aliases:
  - collab-via-passthrough-relay
short_description: "Un diseño de edición colaborativa en tiempo real que no conservaba estado de documento en el servidor, reenviando actualizaciones CRDT directamente entre clientes — implementado en el motor wiki y luego retirado."
status: active
category: patterns
type: topic
content_type: topic
quality: complete
index_group: collaboration-and-editorial-workflow
last_edited: 2026-08-22
editor: pointsav-engineering
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
paired_with: collab-via-passthrough-relay.md
cites:
 - doctrine-claim-29
 - doctrine-claim-16
---

## El patrón en un párrafo

El patrón de relé de paso fue un diseño de edición colaborativa en tiempo real implementado en el motor wiki y retirado posteriormente. Invertía la suposición habitual sobre dónde reside la autoridad en un sistema de edición colaborativa. El servidor de relé no conservaba ningún estado de documento; el árbol git canónico seguía siendo el único registro autoritativo del contenido de cada artículo en todo momento. Los editores concurrentes se conectaban mediante WebSocket a un canal de difusión por documento, y la única responsabilidad del servidor era reenviar mensajes de actualización CRDT entre esos clientes — nunca decodificaba ni almacenaba el estado que esos mensajes codificaban. El diseño se documenta aquí porque el razonamiento detrás de él sigue siendo útil aunque la implementación ya no exista.

## Por qué un relé de paso, no un servidor CRDT

Herramientas como Etherpad y HackMD operan bajo un modelo de documento autoritativo en el servidor: el servidor de edición colaborativa mantiene un objeto de documento vivo y mutable, y ese objeto es el registro principal del contenido actual. Una exportación a git es una instantánea tomada de ese registro del servidor, no al revés. La consecuencia es un segundo estado autoritativo permanente que puede divergir si el mecanismo de exportación falla o el servidor se detiene antes de guardar.

El diseño de relé de paso elimina ese segundo registro por completo. El servidor actúa como un conducto de mensajes, no un almacén — reenvía mensajes de actualización entre clientes sin nunca deserializar ni conservar el estado del documento que transportan.

**Un lector que guarda un artículo nunca depende de que el servidor de colaboración haya hecho algo correctamente.** Toda edición que llega al registro canónico lo hace por la misma ruta de guardado que usaría una edición de un solo autor.

## Lo que esto significaba para la divulgación

Esto era relevante para la postura de divulgación del motor wiki. El registro de divulgación canónico es el árbol git: el historial de contenido de cada artículo es una secuencia de commits firmados, y esa secuencia es lo que produciría una auditoría. Bajo el diseño de relé de paso no existía ningún registro paralelo — el estado CRDT en curso nunca se escribía en ningún lugar, por lo que nunca formó parte del registro de divulgación. El registro se cerraba en el momento de guardar, no antes.

## Estado actual

La función de colaboración que describe este patrón ha sido eliminada del motor wiki. Se lanzó restringida detrás de un indicador de activación explícita, nunca estuvo habilitada por defecto, y posteriormente fue eliminada por completo en lugar de quedar inactiva — el motor actual no tiene ninguna ruta de código de edición colaborativa. Este artículo documenta el diseño como registro histórico de un patrón que se construyó, funcionó según lo previsto, y fue retirado después; no describe el comportamiento actual del motor wiki.

## Más allá del wiki

El relé de paso es un patrón de sustrato, no una característica específica del wiki, y la pregunta de diseño subyacente sobrevive a esta implementación en particular. Cualquier servicio que desee semánticas de edición concurrente enfrenta la misma pregunta: ¿necesita la infraestructura de colaboración mantener el estado del documento en el servidor, o puede ese estado residir completamente en los clientes y en el almacenamiento canónico? La respuesta de paso se aplica con claridad cuando el tipo de documento colaborativo se corresponde directamente con el tipo de almacenamiento canónico.

## Véase también

- [[source-of-truth-inversion]] — la taxonomía de tres capas (canónica / vista / efímera) que este patrón instanciaba
- [[app-mediakit-knowledge]] — arquitectura del motor wiki en el que se implementó este patrón y del que después se eliminó
- [[worm-ledger-design]] — el sustrato del libro mayor WORM que cierra el registro de divulgación en el momento de guardar
- [[substrate-native-compatibility]] — por qué el motor wiki no imita interfaces existentes
- [[disclosure-substrate]] — la convención de postura de divulgación que este diseño satisfacía

## Procedencia

Versión en español elaborada por project-language, adaptación estratégica del artículo canónico en inglés — no es una traducción literal. Vista general estratégica por DOCTRINE.md §XII.
