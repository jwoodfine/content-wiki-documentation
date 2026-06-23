---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: worm-ledger-storage-architecture
short_description: "La arquitectura de almacenamiento especifica C2SP tlog-tiles como primitivo objetivo; la implementación actual de service-fs conserva un registro JSON de solo adición por inquilino pendiente del backend de bloques, con inmutabilidad estructural y legibilidad a largo plazo como diseño previsto."
title: Arquitectura de almacenamiento del ledger WORM
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: worm-ledger-storage-architecture.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-06-23
editor: pointsav-engineering
---



La arquitectura de almacenamiento del [[worm-ledger-design|libro de registros WORM]] describe cómo el ledger inmutable de la plataforma persiste datos en disco siguiendo la [[worm-ledger-architecture|arquitectura de cuatro capas]]. La capa de almacenamiento **especifica** la especificación C2SP tlog-tiles como primitivo objetivo. La implementación actual de `service-fs` conserva los registros como un registro JSON de solo adición por inquilino (`log.jsonl`) con resúmenes SHA-256 por carga, pendiente del backend de bloques.

## El Motor de Almacenamiento por Teselas (Tiles)

La arquitectura de almacenamiento **especifica** el estándar **C2SP tlog-tiles** como primitivo de almacenamiento objetivo, dividiendo el historial de datos en archivos estáticos e inmutables. El backend de bloques está planificado y aún no implementado.
- **Durabilidad Atómica (actual):** Los registros se escriben en un archivo temporal, se sincronizan con `fsync` y se renombran atómicamente a la ruta canónica.
- **Transparencia de Texto Plano (planificado):** Bajo el formato de bloques objetivo, los bloques se almacenan como texto base64 delimitado por saltos de línea, inspeccionable con utilidades Unix estándar.
- **Integridad Basada en Merkle (planificado):** El diseño encadena cada entrada en una estructura Merkle para permitir pruebas de inclusión y consistencia. **Este es el modelo previsto — la compilación actual de `service-fs` registra resúmenes por carga y aún no construye un árbol Merkle ni sirve pruebas.**

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
