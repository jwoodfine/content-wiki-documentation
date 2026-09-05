---
schema: foundry-doc-v1
title: "Liquidación de billetera — el diseño"
slug: service-wallet-settlement
short_description: "service-wallet es un libro mayor contable por inquilino planificado para ingresos de flujo inverso del mercado — aún no existe código; el diseño propone un libro firmado sin custodia en lugar de un riel de pago."
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: service-wallet-settlement.md
references:
  - id: 1
    text: "PointSav platform specification: per-tenant accounting ledger design for reverse-flow settlement — structural properties of the service-wallet component."
  - id: 2
    text: "PointSav platform specification: reverse-flow substrate — the revenue-routing mechanism through which data marketplace proceeds reach operator wallets."
  - id: 3
    text: "PointSav platform specification: customer-owned graph intellectual property — the portability and ownership guarantees for operator-generated graph data."
  - id: 4
    text: "PointSav platform specification: Write-Once-Read-Many (WORM) ledger design — the append-only storage substrate underpinning all platform accounting records."
---

`service-wallet` es un libro mayor contable por inquilino planificado para los ingresos del
mercado de datos y el intercambio publicitario de la plataforma — registrando y liquidando lo
que se le debe a un inquilino como entradas firmadas criptográficamente, sin custodiar fondos
nunca. Aún no existe ninguna implementación; este artículo describe el diseño, no un servicio
distribuido. Existe una utilidad real y distinta, ya distribuida, llamada `tool-wallet` en el
mismo monorepo — un vigilante de pagos USDC en Polygon del lado del proveedor, de un solo
inquilino, para compras de licencias — pero es un componente diferente con un propósito
diferente, no este libro mayor planificado bajo otro nombre.

## La distinción central del diseño

El diseño propone que `service-wallet` sea un libro mayor contable, nunca un riel de pago ni
una billetera con custodia — una distinción que importa tanto estructural como legalmente.

- **Libro mayor contable**: registra créditos, débitos y comisiones como entradas firmadas
  denominadas en la unidad de cuenta elegida por el operador; ningún fondo pasa por la
  plataforma.
- **No es un riel de pago**: el dinero se movería directamente entre el comprador y la
  dirección de destino o el contrato inteligente; la comisión de la plataforma se propone
  como una deducción contable en el momento en que se registra un crédito, no como un
  movimiento de dinero separado.
- **No es una billetera con custodia**: la plataforma nunca mantendría las claves privadas
  de un inquilino — el saldo de un inquilino sería una cifra contable que representa un monto
  adeudado, no un fondo bajo control de la plataforma.

## Lo que propone el diseño

Un registro firmado por cada entrada de crédito, débito o comisión, rastreando monto, moneda,
cadena (si aplica), deducción de comisión, y un saldo de inquilino en ejecución. Un flujo de
liquidación donde un evento de ingreso registra un crédito con la comisión de plataforma
deducida en ese paso, el saldo del inquilino se acumula, y el inquilino — no la plataforma —
inicia cualquier retiro, ya sea a una dirección cripto, una cuenta bancaria, o reinvertido
como crédito de cómputo.

Cada recibo de retiro se anclaría al mismo registro de transparencia externo que
[[fs-anchor-emitter]] ya usa para otros registros de la plataforma. El historial completo del
libro sería exportable por el inquilino en cualquier momento, en el mismo formato en que se
escribió — portabilidad incondicional, en línea con los compromisos de datos de propiedad del
cliente en el resto de la plataforma.[^3]

## Lo que esto no es

Aún no existe ninguna implementación — todo lo anterior es diseño, no un servicio distribuido.
Si se construye según lo diseñado, esto mantendría a la plataforma estructuralmente fuera del
territorio regulado de transmisión de dinero y billeteras con custodia; esto es una
descripción del diseño previsto, no asesoría legal, y las propias actividades de pago de un
inquilino siguen siendo responsabilidad de su propio asesor. Los porcentajes de comisión
específicos, las elecciones de cadena, y los mecanismos de abstracción de gas nombrados en
borradores anteriores de este diseño son detalles de implementación que no se han decidido, y
mucho menos construido — no se repiten aquí como si estuvieran resueltos.

## Véase también

- [[reverse-flow-substrate]] — las fuentes de ingresos que este libro registraría
- [[customer-owned-graph-ip]] — el compromiso de portabilidad que sigue el formato de exportación de este diseño
- [[worm-ledger-architecture]] — el patrón de almacenamiento de solo-anexado que este diseño usaría
