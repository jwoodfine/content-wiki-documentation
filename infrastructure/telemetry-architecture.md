---
schema: foundry-doc-v1
title: "Telemetry architecture"
slug: telemetry-architecture
short_description: "The platform collects web traffic analytics from production edge nodes, routing them to a locally controlled environment via an encrypted path, no third-party cloud."
category: infrastructure
index_group: network-and-telemetry
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-28
editor: pointsav-engineering
paired_with: telemetry-architecture.es.md
---

The platform's telemetry system collects web traffic analytics from production [[edge-deployment|edge nodes]] and routes them to a local processing environment over the [[sovereign-mesh|WireGuard mesh]] without passing through a third-party cloud aggregation service. All analysis runs on hardware the operator controls, consistent with [[customer-hostability|customer-rooted data custody]].

This article describes the architecture as of the initial deployment. The routing topology and processing stack are planned to evolve as the fleet expands.

## Key Takeaways

- Telemetry routes through four tiers: edge capture → WireGuard encrypted transit → local processing node → control workstation pull. No payload passes through a third-party cloud aggregation service at any step.
- All traffic is written to a single shared ledger on the local processing node (`assets/ledger_telemetry.csv`) — there is no per-tenant ledger separation today.
- The control workstation pulls only compiled Markdown reports from the processing node's `outbox/` directory over rsync — not the raw CSV ledger, which stays on the processing node. This limits the blast radius of a workstation compromise to summary data, not the full traffic record.
- Local-first telemetry is a precondition of the tenancy isolation model and the [[customer-hostability|customer-rooted data custody]] property. The operator holds full custody of traffic analytics; no third party holds or processes the raw data.

## Four-tier routing path

### Tier 1 — Edge capture

Live Nginx relays on the cloud edge nodes capture JSON payloads from organic web traffic and route them to the local network over designated ports: `10.50.0.2:8081` for the PointSav tenant and `10.50.0.2:8082` for the Woodfine tenant. The relays do not inspect or buffer payloads; they forward them directly to the tunnel endpoint.

### Tier 2 — Encrypted transit

Payloads traverse a WireGuard mesh (`wg0`) between the cloud edge and the local processing node. The tunnel terminates at the local firewall. Payloads are encrypted in transit and do not pass through any intermediate cloud service.

### Tier 3 — Local processing

A Rust telemetry daemon running on the local processing node binds to all interfaces, receives the decrypted payloads, and appends them to a single shared CSV ledger. A separate reporting binary reads that ledger, consults a local GeoLite2 City database to resolve each recorded IP address to a geographic region, and writes a structured Markdown report to the outbox directory.

### Tier 4 — Analysis extraction

The control node (the operator's workstation) runs a pull script that extracts the compiled reports from the processing node without touching the raw ledger data. Analysis is performed on the extracted reports; the raw CSV ledger remains on the processing node.

## Design rationale

Routing telemetry to a locally controlled node rather than a cloud aggregation service means the operator retains full custody of traffic data. No third party holds or processes the raw analytics.

## See also

- [[sovereign-telemetry]] — the client-side beacon payload that this article's server-side routing carries
- [[worm-ledger-architecture]] — the WORM ledger design that shares the append-only write model
- [[edge-deployment]] — the boundary ingest architecture for the Ring 1 services
- [[compounding-substrate]] — the broader substrate context for local-first data custody
