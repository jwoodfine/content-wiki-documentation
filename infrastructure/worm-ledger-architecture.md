---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: worm-ledger-architecture
short_description: "The WORM ledger is an immutable, append-only substrate using cryptographic hash-chaining and structural isolation to provide a durable backbone for boundary-ingest services while maintaining tamper-evident records suitable for regulatory compliance."
title: "WORM ledger substrate: four-layer architecture"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: worm-ledger-architecture.es.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-05-25
editor: pointsav-engineering
---



[[service-fs-architecture|`service-fs`]] provides the per-tenant Write-Once-Read-Many (WORM) immutable ledger that serves as the durable backbone for all [[three-ring-architecture|Ring 1]] boundary-ingest services, including [[service-people]] and [[service-email]]. By enforcing a strict append-only invariant through cryptographic hash-chaining and structural isolation per the [[worm-ledger-design|WORM ledger design]], the platform ensures that identity, communications, and document records remain tamper-evident and permanently accessible.

## Architectural integration

The WORM ledger sits at the critical boundary between the per-tenant data plane and the multi-tenant knowledge plane. Every ingest service—including `service-people` and `service-email`—writes through this substrate, while Ring 2 services access data via cursor-paged MCP queries.

* **Current Posture:** Isolation is achieved through separate daemon processes per tenant `moduleId` and rigorous filesystem permissioning.
* **Intended Trajectory:** Migration to seL4 microkernel-level capability enforcement is planned to provide formally verified tenant isolation.

## Multi-tier protocol stack

The architecture uses a layered design to ensure that individual components remain swappable without disrupting the core durability contract.

### Layer 4: Cryptographic Anchoring
Checkpoints are intended to be anchored monthly to the public Sigstore Rekor transparency log (per the fundamental physics of 2030 hyperscaler infrastructure). This provides external verifiability without exposing raw tenant data.

### Layer 3: Wire-Level Abstraction
Today, services communicate via axum-based HTTP with mandatory `X-Module-ID` headers. Long-term, this is intended to transition to a native MCP-server interface across both Linux and seL4 targets.

### Layer 2: Core State API
The stable core contract defining methods for `append`, `read_since`, and `checkpoint`. This target-independent layer ensures consistency regardless of the underlying storage engine.

### Layer 1: Storage Primitives
* **Linux/BSD (Current):** POSIX files using atomic write-then-rename discipline.
* **seL4 (Intended):** Capability-addressed objects mediated by `moonshot-database`.
* **Format:** Standardized **C2SP tlog-tiles** (matching RFC 9162 v2 / Rekor v2) ensure 100-year readability.

## Regulatory compliance and durability

The design is engineered to align with SEC Rule 17a-4(f) WORM requirements and EU eIDAS qualified preservation standards. By adopting the plain-text C2SP tile format, the platform guarantees that a forensic analyst in the year 2126 could decode the storage using only basic Unix utilities and a SHA-256 implementation.

## Cross-target synthesis

The platform’s implementation is unique in its dual-target Rust strategy, allowing the same binary to serve as a Linux daemon today and an seL4 unikernel tomorrow. This ensures that the storage substrate is portable from a virtual machine to a future ToteboxOS hardware appliance without a core rewrite.

## See also

- [[worm-ledger-design]] — regulatory compliance mapping and the structural immutability argument
- [[worm-ledger-storage-architecture]] — storage-layer detail: tile format, atomic durability, and dual-target envelopes
- [[cryptographic-ledgers]] — the broader cryptographic ledger context
- [[sel4-microkernel-substrate]] — the intended seL4 capability-enforcement trajectory for tenant isolation
