---
schema: foundry-doc-v1
title: "Postura de derechos de autor canadiense-simple"
slug: canadian-simple-copyright
category: governance
type: topic
content_type: topic
quality: complete
index_group: licensing-and-contribution
short_description: "La propiedad intelectual de la plataforma se concentra en una única sociedad holding matriz canadiense por operación del artículo 13(3) de la Ley de Derechos de Autor canadiense, sin cesión entre empresas, y está diseñada para evolucionar de forma incremental a medida que madura la estructura corporativa."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - ni-51-102
paired_with: canadian-simple-copyright.md
---

La propiedad intelectual de la plataforma se mantiene bajo una postura
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
entidad holding matriz de la trayectoria PointSav.

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
| MCorp | Incorporada (BC); operativa | Operaciones; no genera ingresos derivados de PI usando PI de WCP |
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
 PI es empleado bona fide de WCP Inc. en nómina T4 conforme al [[contributor-model|modelo de contribución]]. Los
 contratistas independientes retienen los derechos de autor
 por defecto bajo la ley canadiense y requerirían cesión
 escrita bajo § 13(4).
- **MCorp permanece no-operativa** respecto
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

Las alternativas de venta de activos a nivel de subsidiaria requieren cronogramas de PI enumerados,
cesiones individuales y consentimientos de cliente. La asimetría se mantiene también hacia adelante
en el tiempo: empujar la PI hacia abajo, a PointSav Digital Systems Inc., en la incorporación mediante
el rollover del § 85, es una transacción de un solo evento. Extraer la PI hacia arriba desde un
tenedor subsidiario más adelante exigiría cesión bajo § 13(4), documentación § 247, posibles
implicaciones de GST/HST y la cristalización del valor de mercado justo.

La postura preserva tanto la opcionalidad de venta de acciones hoy como la ruta de rollover
descendente más limpia en el momento de la incorporación.

## Lo que esta postura no es

No es un estado permanente. Es la estructura mínima viable elegida para el estado actual de la
trayectoria de PointSav, diseñada para evolucionar a medida que el proyecto madura sin deshacer los
acuerdos preexistentes.

No es un sustituto de los acuerdos redactados por asesoría legal a escala. Cada uno de los eventos
disparadores anteriores exige acuerdos redactados por asesoría legal que sustituyan el régimen
estatutario por defecto. La estructura es deliberadamente mínima para que esa sustitución pueda
escalonarse.

No es divulgación continua al estilo BCSC. Las disciplinas descritas aquí rigen cómo se asigna el
derecho de autor y cómo se ve la estructura corporativa; el régimen de
divulgación continua bajo `[ni-51-102]` opera en una superficie distinta y se aplica independientemente de
si la entidad correspondiente es actualmente un emisor reportante.

## Véase también

- [[customer-hostability|Hospedaje por el cliente]] — la postura de soberanía de datos del cliente que esta estructura de derechos de autor habilita
- [[contributor-model|Modelo de contribución]] — quién puede contribuir trabajo creador de PI y bajo qué condiciones
- [[sovereign-replacement-initiative|Iniciativa de reemplazo soberano]] — el programa de independencia de proveedores cuya PI se gobierna aquí

## Referencias

- Ley canadiense de derechos de autor — <https://laws-lois.justice.gc.ca/eng/acts/c-42/>
- BC Business Corporations Act — <https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/02057_00>
- Income Tax Act § 85 (rollover) — <https://laws-lois.justice.gc.ca/eng/acts/i-3.3/section-85.html>
