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
last_edited: 2026-05-06
editor: pointsav-engineering
cites:
 - ni-51-102
paired_with: data-vault-bookkeeping-substrate.md
---

El patrón dominante en el software de contabilidad para PYMEs coloca el libro mayor general, el plan de cuentas y el historial de transacciones dentro de una base de datos propietaria operada por el proveedor del software. Migrar entre plataformas exige reimportar los asientos del diario, conciliar cada período y volver a vincular manualmente los documentos fuente — un proceso que habitualmente cuesta miles de dólares en tiempo de contador. El sustrato de bóveda de datos para contabilidad es una arquitectura planeada, pensada para abordar este bloqueo estructural separando el registro canónico de cada herramienta que lo consume, aplicando la misma [[worm-ledger-design|disciplina de libro mayor WORM]] usada en los [[three-ring-architecture|servicios de límite del Anillo 1]] en otras partes de la plataforma. **Hoy, la única superficie construida es un panel de interfaz provisional de un solo panel** (`app-console-bookkeeper`, un cartucho de `os-console`) que muestra una cifra estática de "esperando sincronización" — nada de la bóveda, el libro mayor o la lógica contable descrita abajo está construido todavía.

## Tres inversiones estructurales (planeadas)

El sustrato está diseñado alrededor de tres decisiones arquitectónicas. Juntas, están pensadas para invertir el patrón de los hiperescaladores:

**La bóveda sería la única capa canónica.** Los documentos fuente — facturas, recibos, órdenes de compra — llegarían en cualquier formato compatible y se almacenarían inmutablemente en el libro mayor de solo adición de la plataforma. Los campos semánticos analizados, el documento original y un compromiso criptográfico se almacenarían juntos, con el original conservado junto a cada representación derivada de él.

**Contabilidad y cuentas serían preocupaciones separadas.** Una aplicación de contabilidad sería una superficie de lectura: navegar, auditar, buscar y exportar desde la bóveda. Una aplicación de cuentas sería una superficie productiva: generar balances de comprobación, estados financieros y documentos de cumplimiento fiscal. El contador del cliente podría usar cualquier herramienta — incluidas herramientas con las que el proveedor no tiene ninguna relación — contra la exportación de la bóveda. La intención es que el proveedor sea dueño de la plataforma de la bóveda, no de los datos que contiene.

**Ninguna lógica contable viviría dentro de la bóveda.** La bóveda almacenaría hechos; los consumidores calcularían vistas derivadas. Migrar fuera de la herramienta de contabilidad está pensado para ser estructuralmente gratuito: la bóveda permanece intacta, la nueva herramienta reproduce el libro mayor, y las vistas derivadas se reconstruyen desde la misma fuente canónica.

## Tres capas planeadas

El diseño del sustrato contempla tres capas arquitectónicas, ninguna de las cuales existe en código todavía:

**Una capa de bóveda** organizaría los datos de facturas analizadas en una estructura de archivos planos con tres directorios: `/source` (los documentos originales, inmutables, con hash SHA-256), `/ledger` (el diario de doble entrada, de solo adición, firmado criptográficamente por fila), y `/asset` (vistas materializadas derivadas de los saldos de cuentas, reconstruibles desde el libro mayor por repetición y nunca la fuente de verdad). Las correcciones a los asientos del diario serían asientos compensatorios, nunca ediciones de fila.

**Una capa de contabilidad** proporcionaría la superficie de consulta, principalmente de lectura: navegar diarios por fecha, cuenta, proveedor o monto; ver documentos fuente en línea; ejecutar búsquedas de texto completo; exportar a CSV conservando las referencias a los documentos fuente.

**Una capa de cuentas** proporcionaría la superficie productiva para la generación de balances de comprobación, la preparación de estados financieros y el trabajo de cumplimiento fiscal, leyendo desde la exportación de la bóveda y produciendo documentos con la herramienta contable que el cliente elija.

## Soporte nativo de facturación electrónica (planeado)

Los mandatos regulatorios europeos están haciendo obligatorios, en un calendario escalonado de 2025 a 2028, los formatos estructurados de factura electrónica — XML conforme a EN 16931 en las especificaciones Peppol y ZUGFeRD — para las transacciones entre empresas. El sustrato está pensado para ingerir estos formatos de forma nativa junto con las facturas en PDF, una vez construido. Estados Unidos no cuenta con un mandato federal comparable a partir de 2026; el PDF sigue siendo dominante, aunque la red de pagos instantáneos FedNow transporta datos de remesa ISO 20022 que el sustrato podría llegar a admitir.

## Auditoría y garantía (planeada)

La estructura del sustrato está diseñada para satisfacer, por construcción y una vez construida, los requisitos de cadena de custodia de ISAE 3402 Tipo II y SOC 2 Integridad de Procesamiento. Se aplicarían cuatro propiedades:

- Documentos fuente originales conservados de forma inmutable junto a sus representaciones analizadas.
- Asientos del diario que referencian sus documentos fuente y están firmados criptográficamente por una identidad autorizada.
- Una propiedad de libro mayor de solo adición que hace estructuralmente imposible la modificación retroactiva sin detección.
- Anclaje mensual a un registro público de transparencia, que produce evidencia verificable de forma independiente de que el estado del libro mayor en cada punto de control no ha sido alterado.

La intención es que un informe de atestación trimestral cite estas propiedades explícitamente, verificable de forma independiente por un auditor usando herramientas públicas en lugar de depender de la caracterización que el proveedor hace de sus propios controles — una propiedad categóricamente distinta de un informe SOC 2 del proveedor, que da fe de los controles del proveedor sobre la infraestructura del proveedor y no sobre la integridad de los datos del cliente. Nada de esto existe hoy; no puede producirse un informe de atestación contra una bóveda sin construir.

## Por qué el bloqueo estructural no puede replicarse a escala de nube empresarial

Las plataformas de contabilidad en la nube empresarial no pueden ofrecer estructuralmente bóvedas inmutables por inquilino con identidades de firma por inquilino, porque su modelo de negocio depende de una fidelización del cliente que la portabilidad de la bóveda por inquilino eliminaría. La separación arquitectónica entre la bóveda y la contabilidad destruye el costo de cambio que constituye el foso defensivo; ninguna plataforma que dependa de ese foso puede ofrecer esa separación de forma voluntaria.

## Patrón de trabajo: aprendizaje junto a un experto de dominio

Se pretende que la especificación de comportamiento del sustrato de contabilidad surja de operaciones reales realizadas por un experto de dominio real — capturando el conocimiento procedimental de cómo se hace el trabajo contable antes de escribir software para automatizarlo. Esto invierte el patrón habitual de construir software a partir de una hipótesis de producto. El software resultante heredaría su especificación de comportamiento de operaciones observadas, no de suposiciones sobre cómo lucen esas operaciones. Esto está planeado para la fase inicial de desarrollo; los resultados reales dependen del alcance y la cadencia de esas sesiones operativas [ni-51-102].

## Véase también

- [[compounding-substrate]] — el patrón de soberanía de sustrato que esta arquitectura extiende
- [[worm-ledger-design]] — el sustrato de libro mayor WORM del que depende esta capa de contabilidad para las pistas de auditoría inmutables
- [[design-system-substrate]] — un sustrato paralelo con el mismo patrón de bóveda-como-canónica, consumidor-como-intercambiable
