---
schema: foundry-doc-v1
title: "Deterministic parser"
slug: service-extraction
category: services
type: topic
content_type: topic
quality: complete
short_description: "service-extraction is the Ring 2 central traffic controller that strips proprietary formatting from raw payloads, constructs structured Entity Bundles, assigns transaction IDs, and routes data to deterministic services or to service-slm for AI-assisted extraction."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-08
editor: pointsav-engineering
cites: []
paired_with: service-extraction.es.md
---

Every payload that crosses the platform boundary lands at **service-extraction**, the [[three-ring-architecture|Ring 2]] traffic controller that strips proprietary formatting (JSON, MIME, Base64), constructs a machine-readable Entity Bundle, and assigns the transaction identifier that follows the bundle through every downstream step. Structured payloads route entirely within Ring 2; unstructured text routes onward to [[service-slm]] for AI-assisted extraction. service-extraction is the canonical successor to the legacy working name `service-parser`.

## Architectural Baseline

Every message that passes through Ring 1 arrives at service-extraction as an unprocessed, vendor-formatted payload. The first Ring 1 service to produce such payloads is typically [[service-email]] or [[service-input]]. The service has one responsibility: transform that payload into a clean, traceable Entity Bundle and route it to the correct downstream service. It assigns a transaction ID to each bundle, providing a chain-of-custody reference that persists through every subsequent processing step.

## Ring and Role

service-extraction occupies **Ring 2 — Knowledge and Processing** in the [[three-ring-architecture]]. Ring 2 is multi-tenant (via `moduleId` namespacing) and deterministic: it processes data without invoking AI inference unless the data shape requires it. When a payload contains unstructured text that cannot be classified by deterministic rules, service-extraction routes that text to Ring 3 ([[service-slm]]) for AI-assisted extraction. Structured and semi-structured payloads route entirely within Ring 2. Entity identifiers produced here are consumed by the [[archetypes-and-chart-of-accounts|Chart of Accounts socket-assignment]] logic in [[service-people]].

## Structural Organization of Components

### The Entity Bundle

Each payload is isolated into a Unix directory named by its timestamp and routing ID. The bundle is eventually stored as an immutable record in [[service-fs-architecture|`service-fs`]]. The bundle contains:

- **`payload.txt`** — the core text payload reduced to plain-text frontmatter format. This file is the permanent, human-readable record of the communication.
- **Binary attachments** — PDFs, images, and other attached files stored natively alongside the text payload. Binary decoupling eliminates split-brain metadata tracking between the text record and its attachments.

### The Multi-Path Routing Matrix

After constructing the bundle, the service routes it based on the payload's origin tags:

| Route | Destination | Condition |
|---|---|---|
| Immutable ledger | Cold storage via service-fs | Standard assets (most messages) |
| Identity ledger | [[service-people]] | Sender identity records for CRM downstream ingestion |
| AI synthesis | [[service-slm]], then purge | Consumable media (newsletters, low-retention items) |

The routing decision is deterministic and tag-driven. No AI inference is required for the routing step itself.

## Configuration

| Parameter | Purpose |
|---|---|
| Queue path | Input path for Ring 1 payloads (e.g., `assets/tmp-maildir/`) |
| Bundle output path | Filesystem location for completed Entity Bundles |
| Routing rules | TOML configuration file mapping origin tags to routing destinations |
| Transaction ID format | Timestamp + routing ID composition format |

## See also

- [[service-email]]
- [[service-people]]
- [[service-slm]]
- [[service-search]]
