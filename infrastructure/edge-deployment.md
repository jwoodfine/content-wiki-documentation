---
schema: foundry-topic-v1
title: "Edge Deployment and Boundary Ingest"
slug: edge-deployment
category: infrastructure
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

The platform moves all external network connections to the outermost boundary of the system before any data reaches the core processing rings. This architecture prevents common network-based attacks from reaching the financial ledgers and structured records held in Ring 2.

## The problem with deep ingest

Standard server configurations process incoming internet traffic — email, HTTP, external API calls — inside the same execution environment that holds core data. A vulnerability in any ingest pathway grants an attacker access to the same memory space as the core records. Isolation cannot be added retroactively once a process has shared-memory access to another.

## Boundary placement

The platform positions all ingest processes at the physical and logical edge of the system. No inbound internet payload crosses into Ring 2 until it has passed through the Ring 1 boundary layer. Ring 1 is implemented as a set of Model Context Protocol (MCP) server processes, one per ingest channel (email, filesystem, people records, external input).

Each Ring 1 process:

1. Accepts the inbound payload from the external source.
2. Sanitizes the payload — removes transport metadata, validates structure, discards malformed input.
3. Passes only the cleaned, structured record inward to Ring 2.

The public internet is never in direct contact with Ring 2 or Ring 3. Ring 2 has no outbound internet path except through service-egress.

## Effect on audit integrity

Because raw payloads are sanitized at the boundary and the cleaned records are what Ring 2 processes, the audit ledger in Ring 2 reflects what the system acted on — not what arrived at the wire. This separation is a precondition of the WORM ledger design: the ledger records clean, validated events, not raw network traffic.

## See also

- [[worm-ledger-architecture]] — the WORM ledger that stores the sanitized records
- [[service-email]] — Ring 1 ingest for email
- [[compounding-substrate]] — the three-ring architecture in context

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
