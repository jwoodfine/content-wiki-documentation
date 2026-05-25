---
schema: foundry-doc-v1
title: "Totebox archive"
slug: totebox-archive
short_description: "Un Totebox Archive es una máquina virtual micro auto-contenida y libremente transferible que persiste datos institucionales como archivos planos inmutables."
category: systems
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: topic-totebox-archive.md
cites: []
---


Un Totebox Archive es la unidad fundamental de almacenamiento y soberanía de datos dentro de la plataforma PointSav — una micro máquina virtual autocontenida que persiste registros institucionales como archivos planos inmutables y puede trasladarse físicamente entre proveedores de nube, servidores privados o hardware bare-metal sin perder su integridad criptográfica. Cada archivo está anclado a un libro contable de escritura única y lectura múltiple (WORM, por sus siglas en inglés), creando una pista de auditoría permanente y verificable para cada transacción y cambio de estado.

## Capa de datos inmutable

A diferencia de las bases de datos tradicionales que requieren procesos activos para acceder a los datos, un Totebox Archive persiste la información como archivos planos inmutables — JSONL, GeoParquet y Markdown — de modo que los datos permanecen accesibles y legibles incluso si el motor de software original ya no está en ejecución. No se requiere ningún entorno de ejecución propietario para leer los registros décadas después.

## Diseño libremente transferible

Un Totebox Archive está empaquetado como una imagen de disco arrancable que puede moverse entre servidores físicos, nubes privadas o hardware bare-metal sin perder integridad ni contexto histórico. El operador toma la imagen y la traslada; no existe un sistema operativo subyacente que retenga las claves.

## Especialización de activos

Los Totebox Archives se despliegan habitualmente como contenedores específicos por dominio para activos institucionales diferenciados.

| Tipo de archivo | Contenido |
|---|---|
| Personal | Registros cifrados e identificación |
| Corporativo | Identificación fiscal, documentos de constitución y actas |
| Inmuebles | Títulos de propiedad, registros de zonificación y libros de construcción |

## Véase también

- [[totebox-os]]
- [[totebox-orchestration]]
- [[infrastructure-os]]
- site-ledger-integration
