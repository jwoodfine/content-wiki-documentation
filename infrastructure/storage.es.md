---
schema: foundry-doc-v1
title: "Almacenamiento inmutable y respaldo seguro"
slug: storage.es
short_description: "La plataforma ejecuta escrituras de solo anexar a nivel de hardware para proporcionar un registro inalterable y a prueba de manipulaciones, respaldando la eliminación legal a través de destrucción de claves criptográficas y protección de copias de seguridad mediante unidades secundarias emparejadas criptográficamente."
category: infrastructure
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: storage.md
---

La plataforma está diseñada para ofrecer a auditores e inversores un registro resistente a manipulaciones: una vez que los datos se escriben, no pueden sobrescribirse ni eliminarse en secreto. Esta propiedad se aplica a nivel de hardware a través del [[worm-ledger-design|sustrato del libro mayor WORM]], no solo mediante políticas de software.

## Puntos clave

- La aplicación de solo adición opera a nivel del controlador de la unidad, no de política de software. Un administrador del sistema con credenciales completas no puede sobrescribir ni eliminar bloques existentes — el controlador de hardware rechaza la escritura. Esto hace que la garantía de resistencia a manipulaciones no pueda ser eludida por actores internos con privilegios elevados.
- La eliminación legal funciona mediante la destrucción criptográfica de la clave, no la modificación del registro. El texto cifrado del registro permanece en el disco tras destruir la clave, lo que prueba que el registro existió en el momento de la escritura, mientras que queda permanentemente ilegible. Las obligaciones de revocación de acceso se cumplen sin comprometer la integridad estructural del registro de adición única.
- Las unidades de respaldo se emparejan criptográficamente con las claves de identidad del sistema principal en el momento de aprovisionamiento. Una unidad extraída físicamente del sistema produce texto cifrado ilegible — protegiendo contra el robo físico de soportes de respaldo sin necesidad de una capa de cifrado adicional.
- La inmutabilidad del almacenamiento es la base física del [[worm-ledger-architecture|diseño del registro WORM]]. La especificación del libro mayor formaliza la garantía de cuatro capas construida sobre este sustrato de hardware.

## Escritura exclusivamente de adición, aplicada por hardware

El hardware de almacenamiento estándar permite a un administrador con privilegios suficientes sobrescribir o eliminar cualquier archivo. El subsistema de almacenamiento de la plataforma utiliza unidades configuradas en modo de solo adición, aplicado por el controlador de hardware. La unidad acepta nuevas escrituras, pero rechaza la modificación de bloques existentes. Esto produce un historial inalterable de cada registro añadido al sistema.

## Eliminación legal sin modificar el registro

Algunos marcos legales exigen que determinados registros queden inaccesibles a solicitud. La plataforma cumple estos requisitos sin modificar el registro en sí: la clave de cifrado del registro se destruye de forma criptográfica, el texto cifrado permanece en la unidad como prueba de existencia y el registro queda permanentemente ilegible sin la clave.

## Unidades de respaldo emparejadas

Cuando el disco principal alcanza su capacidad, se realizan copias de seguridad en un disco secundario emparejado criptográficamente con el sistema principal. Un disco de respaldo extraído del sistema produce texto cifrado ilegible, lo que protege frente al robo físico del soporte. La restauración desde una copia de seguridad requiere acceso a las claves de identidad del sistema principal.

## Véase también

- [[worm-ledger-architecture]] — especificación completa del registro WORM de cuatro capas
- [[worm-ledger-design]] — diseño del sustrato de escritura única y lectura múltiple
- [[edge-deployment]] — cómo entran los datos al sistema antes de llegar al almacenamiento
