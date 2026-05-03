---
schema: foundry-doc-v1
title: "service-extraction: Deterministic Parser"
slug: service-extraction
category: services
type: topic
quality: complete
short_description: "service-extraction is the Ring 2 central traffic controller that strips proprietary formatting from raw payloads, constructs structured Entity Bundles, assigns transaction IDs, and routes data to deterministic services or to service-slm for AI-assisted extraction."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: service-extraction.es.md
---

# service-extraction: Deterministic Parser

> service-extraction is the Ring 2 central traffic controller that strips proprietary formatting from raw payloads, constructs structured Entity Bundles, assigns transaction IDs, and routes data to deterministic services or to service-slm for AI-assisted extraction.

**service-extraction** is a Ring 2 knowledge-and-processing service in the PointSav three-ring architecture. It receives raw payloads from Ring 1 ingest services, strips proprietary third-party formatting (JSON, MIME, Base64), and constructs machine-readable Entity Bundles — self-contained directory structures that hold both the text payload and any associated binary attachments. It is the canonical successor to the legacy working name `service-parser`.

## Architectural Baseline

Every message that passes through Ring 1 arrives at service-extraction as an unprocessed, vendor-formatted payload. The service has one responsibility: transform that payload into a clean, traceable Entity Bundle and route it to the correct downstream service. It assigns a transaction ID to each bundle, providing a chain-of-custody reference that persists through every subsequent processing step.

## Ring and Role

service-extraction occupies **Ring 2 — Knowledge and Processing** in the three-ring architecture. Ring 2 is multi-tenant (via `moduleId` namespacing) and deterministic: it processes data without invoking AI inference unless the data shape requires it. When a payload contains unstructured text that cannot be classified by deterministic rules, service-extraction routes that text to Ring 3 (service-slm) for AI-assisted extraction. Structured and semi-structured payloads route entirely within Ring 2.

## Structural Organization of Components

### The Entity Bundle

Each payload is isolated into a Unix directory named by its timestamp and routing ID. The bundle contains:

- **`payload.txt`** — the core text payload reduced to plain-text frontmatter format. This file is the permanent, human-readable record of the communication.
- **Binary attachments** — PDFs, images, and other attached files stored natively alongside the text payload. Binary decoupling eliminates split-brain metadata tracking between the text record and its attachments.

### The Multi-Path Routing Matrix

After constructing the bundle, the service routes it based on the payload's origin tags:

| Route | Destination | Condition |
|---|---|---|
| Immutable ledger | Cold storage via service-fs | Standard assets (most messages) |
| Identity ledger | service-people | Sender identity records for CRM downstream ingestion |
| AI synthesis | service-slm, then purge | Consumable media (newsletters, low-retention items) |

The routing decision is deterministic and tag-driven. No AI inference is required for the routing step itself.

## Configuration

| Parameter | Purpose |
|---|---|
| Queue path | Input path for Ring 1 payloads (e.g., `assets/tmp-maildir/`) |
| Bundle output path | Filesystem location for completed Entity Bundles |
| Routing rules | TOML configuration file mapping origin tags to routing destinations |
| Transaction ID format | Timestamp + routing ID composition format |

## See Also

- [[service-email]]
- [[service-people]]
- [[service-slm]]
- [[service-search]]

## References

-  §XI — Ring 2 knowledge-and-processing architecture
- `pointsav-monorepo/service-extraction/` — implementation crate
- SYS-ADR-07 — structured data never routes through AI (governs the boundary between Ring 2 deterministic routing and Ring 3 AI invocation)
