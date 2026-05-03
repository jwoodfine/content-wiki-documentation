---
schema: foundry-topic-v1
title: "Almacenamiento Inmutable y Respaldo Seguro"
slug: storage.es
category: infrastructure
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

La plataforma está diseñada para ofrecer a auditores e inversores un registro resistente a manipulaciones: una vez que los datos se escriben, no pueden sobrescribirse ni eliminarse en secreto. Esta propiedad se aplica a nivel de hardware, no solo mediante políticas de software.

## Escritura exclusivamente de adición, aplicada por hardware

El hardware de almacenamiento estándar permite a un administrador con privilegios suficientes sobrescribir o eliminar cualquier archivo. El subsistema de almacenamiento de la plataforma utiliza unidades configuradas en modo de solo adición, aplicado por el controlador de hardware. La unidad acepta nuevas escrituras, pero rechaza la modificación de bloques existentes. Esto produce un historial inalterable de cada registro añadido al sistema.

## Eliminación legal sin modificar el registro

Algunos marcos legales exigen que determinados registros queden inaccesibles a solicitud. La plataforma cumple estos requisitos sin modificar el registro en sí: la clave de cifrado del registro se destruye de forma criptográfica, el texto cifrado permanece en la unidad como prueba de existencia y el registro queda permanentemente ilegible sin la clave.

## Unidades de respaldo emparejadas

Cuando el disco principal alcanza su capacidad, se realizan copias de seguridad en un disco secundario emparejado criptográficamente con el sistema principal. Un disco de respaldo extraído del sistema produce texto cifrado ilegible, lo que protege frente al robo físico del soporte. La restauración desde una copia de seguridad requiere acceso a las claves de identidad del sistema principal.

## Véase también

- [[worm-ledger-architecture]] — especificación completa del registro WORM
- [[architecture]] — portabilidad del archivo y arranque soberano
- [[edge-deployment]] — cómo entran los datos al sistema antes de llegar al almacenamiento

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
