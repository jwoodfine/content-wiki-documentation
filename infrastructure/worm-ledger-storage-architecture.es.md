---
schema: foundry-doc-v1
type: topic
slug: worm-ledger-storage-architecture
short_description: "La arquitectura de almacenamiento adopta C2SP tlog-tiles como su primitivo fundamental, soportando implementación de objetivo dual desde demonios Linux hasta microkernels seL4 mientras asegura inmutabilidad estructural y legibilidad a largo plazo a través de transparencia de texto plano y durabilidad atómica."
title: Arquitectura de almacenamiento del ledger WORM
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: worm-ledger-storage-architecture.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-05-25
editor: pointsav-engineering
---



La arquitectura de almacenamiento del [[worm-ledger-design|libro de registros WORM]] describe cómo el ledger inmutable de la plataforma persiste datos en disco siguiendo la [[worm-ledger-architecture|arquitectura de cuatro capas]]. La capa de almacenamiento adopta la especificación C2SP tlog-tiles, basándose en la inmutabilidad estructural y garantizando que los archivos de datos sean permanentes y legibles a largo plazo.

## El Motor de Almacenamiento por Teselas (Tiles)

La plataforma utiliza el estándar **C2SP tlog-tiles**, dividiendo el historial de datos en archivos estáticos e inmutables:
- **Transparencia DARP:** Los datos se guardan en formato de texto plano (base64), legibles por cualquier sistema operativo futuro.
- **Integridad Criptográfica:** Cada dato se encadena en un "Árbol de Merkle", permitiendo demostrar que ningún registro ha sido alterado sin necesidad de leer todo el archivo.

## Dualidad de Ejecución

El mismo código está diseñado para funcionar en dos entornos:
1. **Hoy (Linux/BSD):** Como un proceso estándar con seguridad basada en permisos de archivos.
2. **Futuro (seL4):** Como un micro-kernel verificado matemáticamente, donde la seguridad es física y estructural.

## Cumplimiento Global

Este diseño cumple con las normativas SEC (EE. UU.) y eIDAS (UE), devolviendo la soberanía de los datos a la empresa y asegurando que la información sea accesible y válida legalmente durante décadas, independientemente de la evolución del software.

## Véase también

- [[worm-ledger-architecture]] — visión arquitectónica de cuatro capas: almacenamiento por bloques, API WORM, protocolo de red, anclaje
- [[worm-ledger-design]] — mapeo de cumplimiento regulatorio y soberanía de claves del cliente
- [[service-fs-architecture]] — la implementación `service-fs` que aplica esta arquitectura de almacenamiento en producción
- [[cryptographic-ledgers]] — el contexto más amplio del libro de registros criptográfico
