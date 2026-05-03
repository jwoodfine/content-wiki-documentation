---
schema: foundry-topic-v1
title: "Telemetry Architecture"
slug: topic-telemetry-architecture
category: infrastructure
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

The platform's telemetry system collects web traffic analytics from production edge nodes and routes them to a local processing environment without passing through a third-party cloud aggregation service. All analysis runs on hardware the operator controls.

This article describes the architecture as of the initial deployment. The routing topology and processing stack are planned to evolve as the fleet expands.

## Four-tier routing path

### Tier 1 — Edge capture

Live Nginx relays on the cloud edge nodes capture JSON payloads from organic web traffic and route them to the local network over designated ports: `10.50.0.2:8081` for the PointSav tenant and `10.50.0.2:8082` for the Woodfine tenant. The relays do not inspect or buffer payloads; they forward them directly to the tunnel endpoint.

### Tier 2 — Encrypted transit

Payloads traverse a WireGuard mesh (`wg0`) between the cloud edge and the local processing node. The tunnel terminates at the local firewall. Payloads are encrypted in transit and do not pass through any intermediate cloud service.

### Tier 3 — Local processing

A Rust telemetry daemon running on the local processing node (`laptop-a`) binds to all interfaces, receives the decrypted payloads, and writes them to per-tenant CSV ledgers. A cross-reference process consults the GeoLite2 City database to resolve IP addresses to geographic regions and produces structured Markdown reports from the ledger data.

### Tier 4 — Analysis extraction

The control node (the operator's workstation) runs a pull script (`pull_sovereign_telemetry.sh`) that physically extracts the compiled reports from the processing node without touching the raw ledger data. Analysis is performed on the extracted reports; the raw CSV ledger remains on the processing node.

## Design rationale

Routing telemetry to a locally controlled node rather than a cloud aggregation service means the operator retains full custody of traffic data. No third party holds or processes the raw analytics. This is a precondition for the tenancy isolation model: each tenant's analytics are isolated at the ledger level and never commingled in a shared cloud table.

## See also

- [[topic-worm-ledger-architecture]] — the WORM ledger design that shares the append-only write model
- [[topic-edge-deployment]] — the boundary ingest architecture for the Ring 1 services
- [[compounding-substrate]] — the broader substrate context for local-first data custody

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
