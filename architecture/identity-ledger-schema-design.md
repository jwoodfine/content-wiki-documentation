---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: identity-ledger-schema-design
short_description: "The Identity Ledger provides a JSONL-based append-only record of canonical person identities using deterministic UUIDv5 derivation from email addresses and WORM discipline. It serves as the unified source for all communication endpoints and temporal role snapshots, enabling deterministic entity resolution without probabilistic inference."
title: "Identity ledger schema design"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: identity-ledger-schema-design.es.md
category: architecture
---



The Identity Ledger provides a JSONL-based, append-only record of canonical person identities within the platform. Following the [[three-ring-architecture|Three-Ring Architecture]]’s boundary-ingest pattern, [[service-people]] publishes this schema to enable deterministic identity resolution across all Ring 2 and Ring 3 knowledge-extraction services. See also [[worm-ledger-design|the WORM ledger design]] and [[machine-based-auth|machine-based authorization]].

## Key Takeaways

- Identity resolution is fully deterministic. The primary identifier (`identity_id`) is a UUIDv5 derived from the user’s primary email address — the same email always produces the same UUID across any node, with no AI or probabilistic matching. This satisfies ADR-07’s requirement that Ring 1 extraction bypass inference.
- Identity records follow [[worm-ledger-architecture|WORM discipline]]. Role changes, new endpoints, and other updates are appended as new records; readers fetch the latest record per `identity_id`. The full append history is preserved as an immutable audit trail of the identity’s progression over time.
- A single identity record is the authoritative source for all communication endpoints: email (RFC 5322), phone (E.164), and typed platform handles (Slack, Teams, Signal). Downstream services resolve endpoints from this record — they do not derive or cache their own.
- Ambiguous or conflicting identities are surfaced to a human operator rather than silently merged. Deterministic extraction at Ring 1; human resolution for exceptions. No probabilistic model makes silent merges at ingest.

## Core Design Principles

### 1. Deterministic Identity via UUIDv5
The primary identifier (`identity_id`) is derived deterministically from the user’s primary email address using a UUIDv5 namespace. This ensures that the same email always produces the identical UUID across any node without requiring AI or probabilistic matching, satisfying the strict requirements of ADR-07.

### 2. Append-Only Integrity
The platform uses a [[worm-ledger-architecture|WORM (Write-Once-Read-Many) discipline]] for identity records. To update an identity—such as a role change or a new communication endpoint—a new record is appended to the ledger. Readers always fetch the latest record per `identity_id`, preserving a full, immutable audit trail of the identity’s history.

### 3. Multi-Channel Communication
Identity records serve as a unified source for all communication endpoints, including:
* **Email:** RFC 5322 compliant, case-insensitive addresses.
* **Phone:** E.164 formatted numbers.
* **Endpoints:** Typed handles for Slack, Teams, Signal, and other integrated platforms.

## Temporal Role Snapshots

Roles are recorded as immutable snapshots within the `roles` array. This allows the system to track an individual's progression (e.g., from contractor to employee) over time. Each role assignment includes:
* A unique `role_id`.
* A categorical `role_type` (Employee, Vendor, Customer, etc.).
* `effective_at` and `expires_at` temporal markers.
* Extensible attributes for department, title, and permissions.

## Entity Resolution Standards

Per ADR-07, identity resolution must be deterministic and bypass AI inference at the Ring 1 layer:
* **Regex Extraction:** Email and phone data are extracted via deterministic patterns.
* **Ambiguity Management:** Unknown or conflicting identities are surfaced to a human operator rather than being silently merged by a probabilistic model.
* **Normalization:** Emails are lowercased and deduplicated prior to UUID derivation.

## MCP Integration

[[service-people]] exposes identity data through the [[mcp-substrate-protocol|Model Context Protocol (MCP)]], providing resources for looking up records by ID or email, and tools for appending new identity claims from Ring 1 inbound services. This architecture ensures that identity remains a stable, verifiable substrate for all downstream automated processing.

## See also

- [[machine-based-auth]]
- [[capability-based-security]]
- [[worm-ledger-design]]
- [[cryptographic-ledgers]]
