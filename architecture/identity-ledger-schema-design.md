---
schema: foundry-doc-v1
type: topic
slug: identity-ledger-schema-design
title: Identity Ledger Schema Design
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: identity-ledger-schema-design.es.md
---


The Identity Ledger provides a JSONL-based, append-only record of canonical person identities within the Foundry ecosystem. Following the Three-Ring Architecture’s boundary-ingest pattern, `service-people` publishes this schema to enable deterministic identity resolution across all Ring 2 and Ring 3 knowledge-extraction services.

## Core Design Principles

### 1. Deterministic Identity via UUIDv5
The primary identifier (`identity_id`) is derived deterministically from the user’s primary email address using a UUIDv5 namespace. This ensures that the same email always produces the identical UUID across any node without requiring AI or probabilistic matching, satisfying the strict requirements of ADR-07.

### 2. Append-Only Integrity
Foundry utilizes a WORM (Write-Once-Read-Many) discipline for identity records. To update an identity—such as a role change or a new communication endpoint—a new record is appended to the ledger. Readers always fetch the latest record per `identity_id`, preserving a full, immutable audit trail of the identity’s history.

### 3. Multi-Channel Communication
Identity records serve as a unified source for all communication endpoints, including:
*   **Email:** RFC 5322 compliant, case-insensitive addresses.
*   **Phone:** E.164 formatted numbers.
*   **Endpoints:** Typed handles for Slack, Teams, Signal, and other integrated platforms.

## Temporal Role Snapshots

Roles are recorded as immutable snapshots within the `roles` array. This allows the system to track an individual's progression (e.g., from contractor to employee) over time. Each role assignment includes:
*   A unique `role_id`.
*   A categorical `role_type` (Employee, Vendor, Customer, etc.).
*   `effective_at` and `expires_at` temporal markers.
*   Extensible attributes for department, title, and permissions.

## Entity Resolution Standards

Per ADR-07, identity resolution must be deterministic and bypass AI inference at the Ring 1 layer:
*   **Regex Extraction:** Email and phone data are extracted via deterministic patterns.
*   **Ambiguity Management:** Unknown or conflicting identities are surfaced to a human operator rather than being silently merged by a probabilistic model.
*   **Normalization:** Emails are lowercased and deduplicated prior to UUID derivation.

## MCP Integration

`service-people` exposes identity data through the Model Context Protocol (MCP), providing resources for looking up records by ID or email, and tools for appending new identity claims from Ring 1 inbound services. This architecture ensures that identity remains a stable, verifiable sustrato for all downstream automated processing.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
