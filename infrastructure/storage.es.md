---
schema: foundry-doc-v1
title: "Almacenamiento inmutable y respaldo seguro"
slug: storage
short_description: "El registro resistente a manipulaciones de la plataforma se apoya en permisos de sistema de archivos y una cadena de hash criptográfica, no en un bloqueo de escritura a nivel de hardware — un administrador con privilegios aún puede eludirlo, y cualquier elusión es detectable, no impedida."
category: infrastructure
index_group: storage-substrate
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: storage.md
---

La plataforma está diseñada para ofrecer a auditores e inversores un registro resistente a manipulaciones: cualquier cambio retroactivo a datos ya escritos es detectable. "Detectable" es la palabra precisa — la garantía se apoya en permisos de sistema de archivos y criptografía, no en un bloqueo de escritura a nivel de hardware que haría la elusión imposible por completo.

## Puntos clave

- La aplicación de solo adición opera en tres capas, ninguna de ellas hardware: la propia superficie de la API del registro (ningún método elimina ni modifica una entrada), permisos del sistema de archivos (un registro finalizado se marca como solo lectura) y criptografía (una cadena de hash más puntos de control anclados externamente). Un administrador con acceso root aún puede cambiar los permisos del archivo subyacente y editar un registro finalizado — la garantía es que hacerlo rompe la cadena de hash y por tanto es detectable, no que la escritura en sí esté bloqueada.
- No existe una vía de destrucción de clave criptográfica para la eliminación legal, ni un esquema de unidades de respaldo emparejadas criptográficamente. Ninguno de los dos existe hoy en la plataforma.
- La inmutabilidad del almacenamiento es la base del [[worm-ledger-architecture|diseño del registro WORM]]. La especificación del libro mayor formaliza la garantía completa construida sobre este sustrato de sistema de archivos y criptografía.

## Escritura de solo adición aplicada por sistema de archivos y criptografía

El subsistema de almacenamiento de la plataforma marca cada registro finalizado como solo lectura a nivel del sistema de archivos en cuanto se escribe, y encadena el hash de cada registro con el anterior. Revertir una escritura exige o bien recuperar privilegios de root para cambiar los permisos y el contenido del archivo, o aceptar que la cadena de hash — y cualquier punto de control ya anclado en un registro de transparencia público — dejará de coincidir. Ninguna vía está bloqueada por completo; ambas son detectables después del hecho.

## Eliminación legal

La plataforma no cuenta con un mecanismo de destrucción de clave criptográfica para hacer ilegible un registro específico a solicitud. Cualquier obligación de eliminación legal hoy debe cumplirse mediante un proceso externo al registro mismo, no mediante una función incorporada del registro.

## Copias de seguridad

La plataforma no cuenta con un esquema de unidades de respaldo emparejadas criptográficamente que proteja los soportes extraídos de ser leídos fuera del sistema principal. Las copias de seguridad y la restauración, donde existen, no incorporan hoy esa protección específica.

## Véase también

- [[worm-ledger-architecture]] — especificación completa del registro WORM de cuatro capas
- [[worm-ledger-design]] — diseño del sustrato de escritura única y lectura múltiple
- [[edge-deployment]] — cómo entran los datos al sistema antes de llegar al almacenamiento
