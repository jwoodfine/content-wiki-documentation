---
schema: foundry-doc-v1
title: "Libros Contables Criptográficos"
slug: cryptographic-ledgers
category: architecture
type: topic
quality: core
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: cryptographic-ledgers.md
cites: []
---

Los libros contables criptográficos son el patrón de almacenamiento de estado inmutable utilizado en la plataforma PointSav. Aplican inmutabilidad matemática de modo que cualquier alteración a un hecho registrado rompe una cadena de hash criptográfica verificable, en lugar de requerir confianza en controles de acceso administrativos.

## El problema que resuelven

En los sistemas de bases de datos tradicionales, un administrador de sistema con privilegios suficientes puede editar silenciosamente un registro — alterando una entrada financiera o un registro de cumplimiento sin activar ninguna alarma automática. El libro contable criptográfico elimina esta vulnerabilidad suprimiendo el concepto de una ruta mutable con privilegios.

## Cómo funciona

La arquitectura separa cada carga entrante en dos entidades: el activo y su registro de estado.

**El activo** — cuando un usuario envía un archivo al sistema, la capa de almacenamiento lo coloca en una bóveda aislada y elimina todos los permisos de ejecución. Se convierte en un objeto binario inerte.

**El registro de estado** — el sistema genera concurrentemente un registro determinista con metadatos legibles y un checksum SHA-256 del activo original. El registro de estado se añade al libro contable; no puede modificarse después de ser añadido.

## Estructura de árbol Merkle

Cada nueva entrada es hasheada; el hash de la nueva entrada se combina con el hash de la entrada anterior para producir el hash del estado actual del árbol. El checkpoint es firmado por la clave del inquilino y publicado. Si los hashes coinciden y la prueba de inclusión se verifica, el registro está intacto.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
