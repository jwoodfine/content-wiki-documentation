---
schema: foundry-doc-v1
title: "Sustrato de bóveda de datos para contabilidad"
slug: data-vault-bookkeeping-substrate
category: infrastructure
index_group: storage-substrate
type: topic
content_type: topic
quality: complete
short_description: Una arquitectura de contabilidad para PYMEs construida sobre una bóveda de fuente inmutable, un diario de solo adición y separación estructural entre el registro contable y cualquier herramienta de contabilidad.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
 - ni-51-102
paired_with: data-vault-bookkeeping-substrate.md
---


## Resumen estratégico

El sustrato de bóveda de datos para contabilidad es una arquitectura planeada, pensada para abordar el bloqueo estructural en el software de contabilidad para PYMEs separando el registro canónico de cada herramienta que lo consume, sobre la misma disciplina del [[worm-ledger-design|libro mayor WORM]] usada en los [[three-ring-architecture|servicios del Anillo 1]] en otras partes de la plataforma. **Hoy, la única superficie construida es un panel de interfaz provisional** (`app-console-bookkeeper`, un cartucho de `os-console`) que muestra una cifra estática de "esperando sincronización" — nada de la bóveda, el libro mayor o la lógica contable descrita abajo existe todavía.

## Tres inversiones estructurales (planeadas)

**La bóveda sería la única capa canónica.** Los documentos fuente llegarían en cualquier formato compatible y se almacenarían inmutablemente en el libro mayor de solo adición de la plataforma. El documento original, los campos semánticos analizados y un compromiso criptográfico se almacenarían juntos.

**Contabilidad y cuentas serían preocupaciones separadas.** Una aplicación de contabilidad sería una superficie de lectura: navegar, auditar y exportar desde la bóveda. Una aplicación de cuentas sería una superficie productiva: generar balances de comprobación, estados financieros y documentos de cumplimiento fiscal. El contador del cliente podría usar cualquier herramienta contra la exportación de la bóveda.

**Ninguna lógica contable viviría dentro de la bóveda.** La bóveda almacenaría hechos; los consumidores calcularían vistas derivadas.

## Tres capas planeadas

Ninguna existe en código todavía. Una capa de bóveda organizaría los datos de facturas analizadas en tres directorios: `/source` (documentos originales, inmutables), `/ledger` (diario de doble entrada, solo adición, firmado criptográficamente por fila), y `/asset` (vistas materializadas derivadas, reconstruibles desde el libro mayor). Una capa de contabilidad proporcionaría la superficie de consulta principalmente de lectura. Una capa de cuentas proporcionaría la superficie productiva.

## Auditoría y garantía (planeada)

La estructura del sustrato está diseñada para satisfacer, una vez construida, los requisitos de cadena de custodia de ISAE 3402 Tipo II y SOC 2 Integridad de Procesamiento por construcción. La intención es que un informe de attestation trimestral cite estas propiedades explícitamente, verificable de forma independiente por un auditor con herramientas públicas. Nada de esto existe hoy; no puede producirse un informe de attestation contra una bóveda sin construir.

## Véase también

- [[worm-ledger-design]] — el diseño del libro mayor WORM que proporciona la disciplina de inmutabilidad estructural
- [[three-ring-architecture]] — el límite del Anillo 1 donde opera el sustrato de la bóveda
- [[compounding-substrate]] — el contexto arquitectónico más amplio del sustrato
- [[service-fs]] — la implementación `service-fs` del libro mayor WORM en producción
