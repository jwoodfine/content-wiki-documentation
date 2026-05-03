---
title: "Three-Ring Architecture"
slug: topic-three-ring-architecture
category: architecture
status: stable
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
references:
  - id: 1
    text: "Foundry Doctrine claim #16 — Three-Ring Architecture"
  - id: 2
    text: "Model Context Protocol specification, 2025-11-25. https://modelcontextprotocol.io"
---

The durable architectural pattern for PointSav's service composition: three rings with one-way dependencies, where the AI ring is structurally optional. The pattern enables parallel development, customer-tier-by-composition productization, and natural decoupling as services mature.

This is Doctrine claim #16.[^1]

## The three rings

```
         ┌──────────────────────────────────────────────────┐
         │     Ring 3 — Optional Intelligence                │
         │     service-slm + Yo-Yo                           │
         │     (queries Ring 2; never required)              │
         └────────────────────────┬─────────────────────────┘
                                  │ queries (read-only)
                                  ↓
         ┌──────────────────────────────────────────────────┐
         │     Ring 2 — Knowledge & Processing               │
         │     service-content + service-extraction          │
         │     + service-search + service-egress             │
         │     (the deterministic core)                      │
         └─────────┬───────────────────────┬────────────────┘
                   ↑                       │ writes/reads
                   │ feeds                 │
                   │                       ↓
  ┌────────────────┴───────────────────────────────────────┐
  │     Ring 1 — Boundary Ingest (per-tenant)               │
  │     service-people + service-email + service-input      │
  │     + service-fs (WORM Immutable Ledger)                │
  │     (data flows in; per-tenant; MCP servers)            │
  └────────────────────────────────────────────────────────┘
```

**Directional dependencies (one-way only)**:
- Ring 1 produces raw data; depends on nothing else
- Ring 2 reads from Ring 1, writes structured graph; depends only on Ring 1
- Ring 3 reads from Ring 2; depends only on Ring 2; never required for Rings 1+2 to function

## The Optional Intelligence Layer principle

The deterministic data pipeline (Rings 1+2) is fully functional without AI.

What this enables:
- **Community tier** ships Rings 1+2 only — full data platform with no AI compute required
- **SMB Customer tier** ships Rings 1+2+3 — adds the Doorman and cloud burst
- **Customers can later add or remove Ring 3 without touching Rings 1+2** — same data platform, AI is additive value

## Service taxonomy

| Ring | Service | Purpose | Per-tenant or shared |
|---|---|---|---|
| 1 | service-fs | Immutable Ledger (WORM, Read/Append-Only) | Per-tenant |
| 1 | service-people | Identity Ledger | Per-tenant |
| 1 | service-email | Communications Ledger | Per-tenant |
| 1 | service-input | Generic document ingestion | Per-tenant |
| 2 | service-extraction | Deterministic Parser (zero AI per SYS-ADR-07) | Multi-tenant via moduleId |
| 2 | service-content | Knowledge graph (LadybugDB) + editorial schemas | Multi-tenant via moduleId |
| 2 | service-search | Search Index (Tantivy) | Multi-tenant via moduleId |
| 2 | service-egress | Physical Release Valve | Per-tenant |
| 3 | service-slm | AI Gateway / Doorman | Single-instance, multi-tenant |

## moduleId discipline

`moduleId` is the multi-tenant primitive. Every call carries a `moduleId`; routing logic isolates tenants at every ring:

- Ring 1: per-tenant service instance (security boundary)
- Ring 2: multi-tenant via moduleId (one process, many graphs/indexes)
- Ring 3: single-instance `service-slm` with per-moduleId LoRA loading

## MCP boundary at Ring 1

Each Ring 1 service implements an MCP server interface[^2] — the 2026 enterprise standard for AI-data boundary. Ring 2 talks to Ring 1 services as MCP clients. Customer extensions plug in as additional MCP servers without modifying service-extraction code.

## How services break apart cleanly

Each service is its own Cargo crate; communication is wire-only (HTTP/MCP/Tantivy file format/LadybugDB driver). Each service exposes a stable wire protocol, not a Rust API. No service requires another service to be running for its tests to pass.

## See Also

- [[topic-compounding-substrate]] — the meta-pattern this ring architecture serves
- [[topic-mcp-substrate-protocol]] — MCP as the Ring 1 boundary protocol (claim #46)
- [[topic-substrate-without-inference-base-case]] — Rings 1+2 operational without Ring 3 (claim #54)

## References

[^1]: Foundry Doctrine claim #16 — Three-Ring Architecture
[^2]: Model Context Protocol specification, 2025-11-25. https://modelcontextprotocol.io

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.
