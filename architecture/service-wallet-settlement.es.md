---
title: "Liquidación con Service-Wallet"
slug: service-wallet-settlement.es
category: architecture
status: stable
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
---

`service-wallet` (Anillo 2) es el libro mayor de contabilidad interna por inquilino que registra y liquida todos los ingresos de flujo inverso procedentes del mercado de datos y el intercambio publicitario.

Esta es la reclamación de Doctrina #53.

## Qué es service-wallet (y qué no es)

`service-wallet` es un **libro mayor de contabilidad**, no un riel de pago ni una cartera custodiada. Esta distinción importa legal y estructuralmente: registra créditos, débitos y comisiones como entradas JSONL firmadas; Foundry no tiene fondos en tránsito; Foundry nunca tiene las claves privadas del inquilino. Esta arquitectura mantiene a Foundry estructuralmente fuera del territorio regulado de transmisores de dinero y carteras custodiadas.

## Flujo de liquidación

El flujo va de: evento de ingresos → crédito registrado (con comisión de plataforma deducida) → el saldo neto del inquilino aumenta → el inquilino inicia el retiro (controlado por el inquilino, no automático) → el evento de retiro se registra en el libro mayor, el recibo se ancla a Sigstore Rekor, y la entrada en el libro mayor WORM en service-fs cierra el ciclo contable.

## Rieles de pago para retiros en criptomoneda

Polygon PoS (aproximadamente $0,002/tx; principal) y Solana (aproximadamente $0,0005/tx; secundario). No custodiado: la plataforma almacena solo las direcciones de destino (claves públicas); el retiro lo firma la cartera del inquilino, no Foundry. Circle Paymaster maneja la abstracción del gas — los inquilinos pagan el gas en USDC; no se requiere token nativo de Polygon/Solana.

## Portabilidad

El historial completo del libro mayor es consultable por el inquilino en cualquier momento. El formato de exportación es JSONL. La portabilidad es incondicional; el libro mayor viaja con el inquilino al salir (reclamación #48).

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ y Foundry™ son marcas no registradas de Woodfine Capital Projects Inc.
