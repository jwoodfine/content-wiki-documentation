---
schema: foundry-topic-v1
title: "Visión General de la Arquitectura de la Plataforma"
slug: topic-architecture
category: architecture
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

La plataforma PointSav está diseñada en torno a dos propiedades estructurales: consistencia criptográfica distribuida y capacidad de arranque soberano. Ambas propiedades se mantienen de forma simultánea en entornos en la nube y en bóvedas físicas desconectadas.

## Estado criptográfico distribuido

Un único archivo puede existir en múltiples entornos físicos —un nodo activo en la nube y una bóveda sin conexión— mientras mantiene un estado criptográfico unificado. Ambos entornos comparten en todo momento el mismo hash Merkle raíz. Esto permite que un auditor verifique la integridad de cualquiera de las copias sin necesidad de que ambas estén en línea simultáneamente.

## Colapso y portabilidad del archivo

Cuando un operador emite el comando de colapso, la plataforma comprime el índice federado en la nube y la copia física sin conexión en una única entidad transferible: una imagen de arranque autoejecutada en formato `.ISO` o `.IMG`. Esta operación es explícita e iniciada por el operador; no se ejecuta de forma automática.

## Imagen de arranque soberana

La imagen resultante es un entorno operativo autocontenido. Puede desplegarse en hardware físico o importarse en un entorno de nube comercial. La imagen lleva el estado completo del archivo, lo que permite reconstituir el sistema en hardware nuevo sin necesidad de recuperar datos desde una fuente remota.

Esta propiedad está diseñada para garantizar la continuidad operativa cuando el entorno de despliegue principal no está disponible.

## Véase también

- [[topic-worm-ledger-architecture]] — diseño del registro WORM que sustenta la integridad del archivo
- [[compounding-substrate]] — cómo las propiedades estructurales se acumulan entre despliegues
- [[topic-customer-hostability]] — propiedades de diseño que permiten al cliente alojar la plataforma completa

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
