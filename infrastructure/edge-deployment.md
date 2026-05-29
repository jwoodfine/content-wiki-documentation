---
schema: foundry-doc-v1
title: "Edge deployment and boundary ingest"
slug: edge-deployment
short_description: "The platform routes all external network connections through Ring 1 boundary-ingest services at the system edge, sanitizing incoming payloads before they reach core processing rings and recording clean, validated events to the audit ledger rather than raw network traffic."
category: infrastructure
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: edge-deployment.es.md
---

The platform moves all external network connections to the outermost boundary of the [[three-ring-architecture|three-ring architecture]] before any data reaches the core processing rings. This architecture prevents common network-based attacks from reaching the financial ledgers and structured records held in Ring 2, with sanitized records written to the [[worm-ledger-design|WORM ledger]].

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

- [[worm-ledger-architecture]] — the WORM ledger that stores the sanitized records produced at the boundary
- [[three-ring-architecture]] — the three-ring architecture that defines the Ring 1 boundary placement
- [[service-email]] — Ring 1 ingest for email traffic
- [[compounding-substrate]] — the substrate-sovereignty context for boundary-first ingest design
