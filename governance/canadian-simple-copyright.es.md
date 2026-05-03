---
schema: foundry-doc-v1
title: "Canadian-Simple Copyright Posture"
slug: canadian-simple-copyright.es
category: governance
type: topic
quality: core
short_description: "Foundry's intellectual property vests in a single Canadian parent holding company by operation of Canadian Copyright Act § 13(3), without inter-company assignment, and is designed to be evolved incrementally as the corporate structure matures."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: canadian-simple-copyright.md
---
# Postura de derechos de autor canadiense-simple (resumen)

La propiedad intelectual de Foundry se mantiene bajo una postura
corporativa deliberadamente mínima, elegida para preservar
flexibilidad mientras el proyecto madura. Los derechos de autor
se asignan a una sola entidad canadiense holding por operación
del estatuto, no por cesión inter-empresa. Este artículo describe
la postura, nombra los estatutos que la hacen funcionar y lista
los eventos disparadores que requieren revisarla.

**No es asesoramiento legal.** Es apropiada la revisión por
asesor jurídico antes de cualquier evento disparador.

## El titular

Los derechos de autor son del **Woodfine Capital Projects Inc.**
("WCP Inc."), una corporación de Columbia Británica que es la
entidad holding matriz de la trayectoria Foundry.

## Base estatutaria — Ley canadiense de derechos de autor § 13(3)

§ 13(3) hace al empleador el **primer dueño** de los derechos
de autor en obras hechas por un empleado en el curso de empleo
bajo un contrato de servicio. § 13(3) crea primer-titularidad,
no cesión. No requiere instrumento escrito separado para que
el derecho se asigne. La titularidad resultante no está sujeta
al interés reversivo del § 14(1) que se aplica a las cesiones
del § 13(4).

## Estructura corporativa

| Entidad | Estado | Rol |
|---|---|---|
| Woodfine Capital Projects Inc. | Incorporada (BC); matriz holding | Titular de derechos de autor y marca para todo el software, documentación, contenido y marca |
| Woodfine Management Corp. | Incorporada (BC); operativa | Operaciones; no genera ingresos derivados de PI usando PI de WCP |
| PointSav Digital Systems | Aún no incorporada | Nombre comercial de WCP Inc. pre-incorporación |

## Por qué funciona sin acuerdos inter-empresa de PI

No hay flujo de PI inter-empresa mientras opere así. § 13(3)
es suficiente para la asignación; los requisitos de
documentación de precios de transferencia § 247 de la CRA, que
se aplican al uso inter-empresa de PI, no se aplican cuando no
hay uso inter-empresa que documentar.

## Disciplinas operativas

La postura depende de:

- **Solo contribuyentes empleados.** Cada contribuyente que crea
  PI es empleado bona fide de WCP Inc. en nómina T4. Los
  contratistas independientes retienen los derechos de autor
  por defecto bajo la ley canadiense y requerirían cesión
  escrita bajo § 13(4).
- **Woodfine Management Corp. permanece no-operativa** respecto
  a la PI de WCP.
- **"PointSav Digital Systems" es nombre comercial de WCP**
  bajo la Partnership Act de BC hasta su incorporación.
- **Brecha de derechos morales reconocida.** Los derechos
  morales § 14.1 no pueden cederse, solo renunciarse por
  escrito. § 13(3) no los renuncia; la postura admite esta
  brecha residual sin papelearla.

## Eventos disparadores

La postura se actualiza cuando ocurre cualquiera de los
siguientes: primer empleado no-fundador / no-oficial; primera
contribución de contratista al trabajo en alcance; primer
ingreso externo usando PI de WCP; estado de emisor reportante
bajo BCSC NI 51-102; incorporación de PointSav Digital Systems
Inc. (manejada al rollover, Ley del Impuesto sobre la Renta
§ 85); cualquier uso inter-empresa de PI entre WCP y una
subsidiaria operativa.

## Por qué preserva valor patrimonial

Mantener la PI en la matriz habilita transacciones de
**venta-de-acciones**: vender el patrimonio de WCP transfiere
el patrimonio completo de PI en una transacción. Sin cesiones
por activo, sin disparadores de Bulk Sales Act, sin
consentimientos de cliente. Empujar PI hacia abajo a PointSav
Digital Systems Inc. en la incorporación vía rollover § 85 es
también una transacción de un solo evento.

## Véase también

- [Documento canónico en inglés](topic-canadian-simple-copyright.md)
- El complemento operativo en
  `factory-release-engineering/README.md` §6
- [Hospedaje por el cliente](topic-customer-hostability.md)
