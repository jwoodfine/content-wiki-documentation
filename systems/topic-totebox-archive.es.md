---
schema: foundry-doc-v1
title: "Totebox Archive"
slug: topic-totebox-archive
category: systems
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: topic-totebox-archive.md
cites: []
---

Un Totebox Archive es la unidad fundamental de almacenamiento y soberanía de datos dentro de la plataforma PointSav. Opera como una **Micro Máquina Virtual** que proporciona servicios autocontenidos para activos institucionales específicos.

## Capa de datos inmutable

A diferencia de las bases de datos tradicionales que requieren procesos activos para acceder a los datos, un Totebox Archive persiste la información como **archivos planos inmutables** (JSONL, GeoParquet, Markdown). Este desacoplamiento garantiza que los datos permanezcan accesibles y legibles incluso si el motor de software original ya no está en ejecución.

Cada archivo está anclado criptográficamente a un libro contable WORM, creando una pista de auditoría permanente y verificable para todas las transacciones y cambios de estado.

## Sistema libremente transferible

Un requisito arquitectónico clave del sistema PointSav es que los datos deben ser un activo, no una responsabilidad. Un Totebox Archive está diseñado para ser **libremente transferible**. Está empaquetado como una **Imagen de Disco Arrancable** que puede moverse entre servidores físicos, nubes privadas o recursos bare-metal sin perder su integridad ni contexto histórico.

## Especialización de activos

Cada Totebox se especializa en un tipo de activo institucional. Los casos de uso comunes incluyen archivos de contratos, registros financieros, correspondencia y conjuntos de datos geoespaciales. La especialización previene que los datos de diferentes dominios se entremezclen en un único contenedor.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
