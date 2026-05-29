---
schema: foundry-doc-v1
title: "Liquidación con Service-wallet"
slug: service-wallet-settlement.es
short_description: "Un libro mayor contable interno por tenant que registra y liquida ingresos de flujo inverso del mercado de datos como entradas JSONL firmadas, con opciones de retiro sin custodia a blockchain o moneda fiduciaria y deducciones de tarifa de plataforma aplicadas en tiempo de crédito."
category: services
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: service-wallet-settlement.md
---


`service-wallet` es el libro mayor de contabilidad interna por tenant que registra y liquida todos los ingresos de flujo inverso procedentes del mercado de datos y el intercambio publicitario de la plataforma. El servicio opera en el [[three-ring-architecture|Anillo 2]] de la plataforma y no custodia fondos: registra créditos, débitos y comisiones como entradas firmadas criptográficamente, y el retiro hacia la cartera o cuenta bancaria del operador se gestiona fuera de la plataforma.

## Qué es service-wallet (y qué no es)

`service-wallet` es un **libro mayor de contabilidad**, no un riel de pago ni una cartera custodiada. Esta distinción importa legal y estructuralmente: registra créditos, débitos y comisiones como entradas JSONL firmadas; PointSav no tiene fondos en tránsito; la plataforma nunca tiene las claves privadas del inquilino. Esta arquitectura mantiene a la plataforma estructuralmente fuera del territorio regulado de transmisores de dinero y carteras custodiadas.

## Flujo de liquidación

El flujo va de: evento de ingresos → crédito registrado (con comisión de plataforma deducida) → el saldo neto del inquilino aumenta → el inquilino inicia el retiro (controlado por el inquilino, no automático) → el evento de retiro se registra en el libro mayor, el recibo se ancla a Sigstore Rekor mediante [[fs-anchor-emitter]], y la entrada en el [[worm-ledger-design|libro mayor WORM]] en [[service-fs-architecture|service-fs]] cierra el ciclo contable.

## Rieles de pago para retiros en criptomoneda

Polygon PoS (aproximadamente $0,002/tx; principal) y Solana (aproximadamente $0,0005/tx; secundario). No custodiado: la plataforma almacena solo las direcciones de destino (claves públicas); el retiro lo firma la cartera del inquilino, no la plataforma. Circle Paymaster maneja la abstracción del gas — los inquilinos pagan el gas en USDC; no se requiere token nativo de Polygon/Solana.

## Portabilidad

El historial completo del libro mayor es consultable por el inquilino en cualquier momento. El formato de exportación es JSONL. La portabilidad es incondicional; el libro mayor viaja con el tenant al salir, conforme a la garantía de portabilidad de datos de propiedad del cliente.

## Véase también

- [[reverse-flow-substrate]] — fuentes de ingresos; detalle del riel de pago
- [[customer-owned-graph-ip]] — la exportación del libro mayor es propiedad incondicional del tenant
- [[worm-ledger-architecture]] — service-wallet agrega entradas al libro mayor WORM de service-fs
