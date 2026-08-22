---
schema: foundry-doc-v1
title: "Visión general de la arquitectura de la plataforma"
slug: architecture
short_description: "La consistencia criptográfica de la plataforma se apoya en un registro real encadenado por Merkle; la capacidad de arranque soberana — colapsar un despliegue en una sola imagen portátil — es un objetivo de diseño, aún no una función publicada."
category: architecture
index_group: platform-structure
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: architecture.md
---

La plataforma [[pointsav-overview|PointSav]] está diseñada en torno a dos propiedades estructurales: consistencia criptográfica, respaldada por un [[merkle-proofs-as-substrate-primitive|registro real encadenado por Merkle]], y capacidad de arranque soberana, una función planificada. Ni un comando de colapso-a-imagen-arrancable iniciado por el operador ni una sincronización en vivo entre entornos (nube más bóveda sin conexión) existen hoy en la plataforma — ambas son la forma prevista que describe este artículo, no mecanismos ya publicados.

## Puntos clave

- La consistencia criptográfica se apoya en una primitiva real: un [[merkle-proofs-as-substrate-primitive|registro encadenado por Merkle]] con pruebas de inclusión y consistencia, ya usado por varios servicios de la plataforma para registros de solo-anexar a prueba de manipulación.
- La garantía específica entre dos entornos que describe este artículo — un nodo activo en la nube y una bóveda sin conexión que comparten un mismo hash raíz, verificable de forma independiente — es un objetivo de diseño, no una función construida. No se encontró ningún mecanismo de sincronización entre entornos en el código actual.
- La capacidad de arranque soberana — colapsar un despliegue en una imagen de arranque autocontenida y reconstituirlo en hardware nuevo sin una fuente remota — también es un objetivo de diseño. Existen herramientas reales de construcción de imágenes arrancables para varios productos individuales de la plataforma; no existe un comando de operador que "colapse el estado actual de este archivo", abarcando las copias en la nube y sin conexión.
- Ambas propiedades están pensadas para ser estructurales una vez construidas, no complementos añadidos — pero afirmar que ya operan sería exagerar lo que hoy está publicado.

## La primitiva del registro criptográfico

El bloque real detrás de la afirmación de consistencia es el [[merkle-proofs-as-substrate-primitive|registro encadenado por Merkle]] de la plataforma: una estructura de solo-anexar con puntos de control criptográficos y pruebas de inclusión/consistencia, ya en uso por varios servicios para registros a prueba de manipulación. Lo que no está construido es la propiedad específica entre dos entornos descrita abajo — un nodo activo en la nube y una bóveda sin conexión que comparten continuamente un mismo hash raíz verificado.

## Planificado: estado compartido entre dos entornos

El diseño previsto: un único archivo existiría en dos entornos físicos — un nodo activo en la nube y una bóveda físicamente aislada sin conexión — compartiendo en todo momento el mismo hash raíz Merkle. Un auditor podría entonces verificar cualquiera de las copias de forma independiente, sin que ambas estuvieran en línea. Esto es prospectivo; no existe hoy ningún mecanismo de sincronización que lo implemente.

## Planificado: colapso y portabilidad del archivo

El diseño previsto: un comando emitido por el operador comprimiría el estado de un despliegue en una única imagen de arranque autoejecutable. Existen hoy herramientas reales para construir imágenes arrancables de productos individuales — compilar un producto específico en una imagen `.img` para su propio destino de despliegue. No existe un comando general que "colapse este archivo en vivo, incluida su bóveda sin conexión, en una sola imagen portátil". La intención de diseño es que esa operación sea explícita e iniciada por el operador, nunca automática ni programada.

## Véase también

- [[worm-ledger-architecture]] — diseño del registro WORM que sustenta la integridad del archivo
- [[compounding-substrate]] — cómo las propiedades estructurales se acumulan entre despliegues
- [[customer-hostability]] — propiedades de diseño que permiten al cliente alojar la plataforma completa
