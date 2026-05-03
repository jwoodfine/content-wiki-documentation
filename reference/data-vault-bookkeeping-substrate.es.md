---
schema: foundry-doc-v1
title: "Sustrato de bóveda de datos para contabilidad"
slug: data-vault-bookkeeping-substrate.es
category: reference
type: topic
quality: published
short_description: Una arquitectura de contabilidad para PYMEs construida sobre una bóveda de fuente inmutable, un diario de solo adición y separación estructural entre el registro contable y cualquier herramienta de contabilidad.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: data-vault-bookkeeping-substrate.md
---

## Resumen estratégico

El sustrato de bóveda de datos para contabilidad aborda el bloqueo estructural en el software de contabilidad para PYMEs separando el registro canónico de cada herramienta que lo consume. La bóveda almacena hechos; los consumidores calculan vistas derivadas. La migración desde cualquier herramienta de contabilidad es estructuralmente sin costo: la bóveda permanece intacta, la nueva herramienta reproduce el diario, y las vistas derivadas se reconstruyen desde la misma fuente canónica.

## Tres inversiones estructurales

**La bóveda es la única capa canónica.** Los documentos fuente llegan en cualquier formato compatible y se almacenan inmutablemente en el libro mayor de solo adición de la plataforma. El documento original, los campos semánticos analizados y un compromiso criptográfico se almacenan juntos. Nada se sobrescribe nunca.

**Contabilidad y cuentas son preocupaciones separadas.** La aplicación de contabilidad es una superficie de lectura: permite navegar, auditar y exportar desde la bóveda. La aplicación de cuentas es una superficie productiva: genera balances de comprobación, estados financieros y documentos de cumplimiento fiscal. El contador del cliente puede usar cualquier herramienta contra la exportación de la bóveda.

**Sin lógica contable dentro de la bóveda.** La bóveda almacena hechos; los consumidores calculan vistas derivadas.

## Tres capas

La capa de bóveda organiza los datos de facturas analizadas en tres directorios: `/source` (documentos originales, inmutables), `/ledger` (diario de doble entrada, solo adición, firmado criptográficamente por fila), y `/asset` (vistas materializadas derivadas, reconstruibles desde el libro mayor). La capa de contabilidad proporciona la superficie de consulta principalmente de lectura. La capa de cuentas proporciona la superficie productiva.

## Auditoría y garantía

La estructura del sustrato satisface los requisitos de cadena de custodia de ISAE 3402 Tipo II y SOC 2 Integridad de Procesamiento por construcción. Un informe de attestation trimestral cita estas propiedades explícitamente. Un auditor puede verificar el attestation de forma independiente usando herramientas de verificación disponibles públicamente, sin depender de la caracterización del proveedor de sus propios controles.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
