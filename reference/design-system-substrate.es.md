---
schema: foundry-doc-v1
title: "Sustrato del sistema de diseño"
slug: design-system-substrate.es
category: reference
type: topic
quality: published
short_description: Una arquitectura de sistema de diseño autoalojada, propiedad del cliente y legible por IA que las PYMEs ejecutan en su propia infraestructura, con propiedad Git por tenant y un plano de respaldo de investigación legible por máquinas.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: design-system-substrate.md
---

## Resumen estratégico

El sustrato del sistema de diseño invierte el patrón de los grandes proveedores de tecnología: en lugar de que el sistema de diseño viva dentro de la infraestructura del proveedor, cada cliente posee su sistema de diseño como repositorio Git en su propia infraestructura. El costo de migración cae hacia cero porque el cliente siempre tiene la fuente.

## Tres inversiones estructurales

**Propiedad por tenant.** Cada cliente posee su sistema de diseño con firma criptográfica de commits vinculada a la identidad del cliente. La arquitectura de tres capas (bóveda, motor, showcase) significa que un cliente puede llevar la bóveda a cualquier infraestructura que pueda ejecutar el binario del motor.

**Plano de respaldo de investigación legible por IA.** Cada decisión de diseño vive como archivo markdown estructurado junto a las definiciones de tokens y recetas de componentes. Los agentes de IA consultan esta interfaz en tiempo de generación de código, leen el porqué detrás de las decisiones existentes y generan UI que ya refleja la intención de la marca.

**Agnóstico de editor mediante formato de tokens abierto.** Los tokens se almacenan en formato W3C Design Tokens Community Group. Las herramientas de diseño que admiten este formato pueden consumir la misma fuente de tokens; las herramientas posteriores leen desde el mismo bundle DTCG. El sustrato permanece neutral sobre qué herramienta de diseño usa el cliente.

## Arquitectura de tres capas

La **bóveda** es el almacén de contenido canónico: definiciones de tokens, recetas HTML y CSS de componentes, especificaciones ARIA, temas y un directorio de investigación legible por IA. El **motor del sustrato** es un servicio sin estado que lee la bóveda y expone la superficie de investigación a los agentes de IA. El **showcase** es la aplicación web que sirve el sistema de diseño en un dominio. El showcase propio del proveedor usa el mismo código base y arquitectura que cualquier instancia del cliente.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
