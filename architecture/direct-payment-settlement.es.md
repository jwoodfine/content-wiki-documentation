---
schema: foundry-doc-v1
title: "Acuerdo de Pago Directo"
slug: direct-payment-settlement.es
category: architecture
type: topic
quality: published
short_description: "El pago por transacciones del mercado está planificado para fluir directamente del comprador al inquilino-cliente; la participación de Foundry es una comisión por transacción en el momento de la liquidación, no una suscripción recurrente."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: direct-payment-settlement.md
---

El **Acuerdo de Pago Directo** es la arquitectura de pago planificada para los flujos de mercado de datos e intercambio de anuncios de Foundry. Bajo este modelo, el pago está previsto para viajar directamente del comprador al inquilino-cliente, con Foundry deduciendo una comisión por transacción transparente en el momento de la liquidación. No está planificado que los fondos fluyan a través de las cuentas de Foundry; no están planificados ciclos de pago; y el acceso del cliente a la plataforma no está condicionado a ninguna suscripción o pago mínimo. Este patrón codifica la reclamación doctrinal #53.

## Por qué el pago directo importa para las pequeñas empresas

Las plataformas de mercado que intermedian el pago crean complicaciones operacionales para las pequeñas empresas que los operadores empresariales absorben rutinariamente. Un ciclo de pago de 30 a 60 días es un problema de gestión de tesorería para una empresa de cinco personas que no tiene función de tesorería. Un intermediario que retiene los fondos del cliente introduce una exposición de contraparte que una pequeña empresa no puede gestionar prácticamente. Y el pago intermediado por la plataforma requiere que el vendedor reconcilie los estados de cuenta de la plataforma con sus propios registros — una carga de cumplimiento que se agrava para los negocios en industrias reguladas.

El pago directo elimina estas complicaciones. El comprador paga al vendedor; Foundry toma su comisión en el momento de la transacción; no existe ningún período de flotación; y la cadena de auditoría es más simple.

## Dos raíles de liquidación planificados

`service-settlement` (servicio del Anillo 2 planificado) está previsto para soportar dos raíles simultáneamente:

**Raíl bancario tradicional.** El patrón previsto conecta la cuenta bancaria empresarial del inquilino en el aprovisionamiento. Cuando un comprador inicia una transacción, el pago se enruta a través de un mecanismo de liquidación de mercado estándar — el comprador es cargado, la comisión de Foundry se deduce, y el resto se transfiere a la cuenta del inquilino. Este raíl gestiona las obligaciones de declaración fiscal para las jurisdicciones aplicables.

**Raíl de criptomoneda directo.** La alternativa prevista conecta una billetera de criptomoneda propiedad del cliente. Cuando un comprador elige este raíl, se construye una transacción dirigiendo los fondos del comprador al inquilino con una salida de comisión para la billetera operativa de Foundry. El comprador difunde la transacción; el inquilino recibe fondos tan pronto como la cadena confirma. La liquidación está prevista para ser más rápida que el raíl bancario y operar transfronterizamente sin complejidad de conversión de divisas. Este raíl está planificado como opt-in.

## El modelo de comisión previsto de Foundry

La comisión prevista de Foundry es un porcentaje del valor de la transacción deducido en la liquidación. La comisión está prevista para ser transparente (visible para el comprador y el inquilino antes de confirmar la transacción), consistente (un porcentaje por transacción en lugar de negociación por inquilino) y no recurrente (sin suscripción, sin mínimo, sin tarifa anual).

El aprovisionamiento del inquilino no está planificado para requerir ningún pago por adelantado a Foundry. Se prevé que Foundry gane solo cuando el inquilino gana. Esto se alinea con el principio [[customer-owned-graph-ip]]: los datos y los adaptadores del cliente son su propiedad; se prevé que Foundry tome una comisión de servicio sobre la actividad de monetización, no una tarifa de licencia por acceso a los propios registros del cliente.

## Composición

El Acuerdo de Pago Directo compone con el [[reverse-flow-substrate]] — cada transacción de mercado e intercambio de anuncios está prevista para desencadenar un evento de liquidación. Compone con [[customer-owned-graph-ip]] — los ingresos de la monetización de la PI del cliente van al titular de la PI. Y compone con [[single-boundary-compute-discipline]] — el tráfico de liquidación está previsto para enrutarse a través del Portero de manera que la misma frontera de auditoría capture la monetización además de la inferencia.

## Véase También

- [[reverse-flow-substrate]] — los flujos planificados de mercado e intercambio de anuncios que generan eventos de liquidación
- [[customer-owned-graph-ip]] — el principio de propiedad que hace que el pago directo al cliente sea el modelo correcto
- [[single-boundary-compute-discipline]] — el Portero como la frontera de auditoría de liquidación prevista

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-direct-payment-settlement.md` (refinado el 30 de abril de 2026). Todas las reclamaciones de liquidación, comisiones y hoja de ruta llevan encuadre "planificado," "previsto" e "intencional" — la implementación de la Fase 5 no ha comenzado. Postura de divulgación continua BCSC aplicada.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
