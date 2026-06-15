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

## What WORM guarantees — and what it does not

Understanding the ledger's integrity properties requires clarity on what the append-only invariant covers and where it stops.

**The WORM guarantee covers:**
- **Immutability after write.** A record written to the ledger cannot be modified or deleted by any actor — including the platform itself. This is structural, not policy.
- **Tamper evidence.** Any post-write alteration is detectable by computing the hash chain. An auditor with the C2SP tile files and a SHA-256 implementation can verify integrity without a live service.
- **External verifiability.** Monthly Sigstore Rekor anchoring creates a public timestamp chain that persists independently of the platform instance.
- **Readability across decades.** The plain-text C2SP tlog-tiles format requires only basic Unix utilities to decode. No proprietary tooling is needed.

**The WORM guarantee does not cover:**
- **Correctness of what was written.** WORM cannot detect or prevent an incorrect record from entering the ledger. Correctness is the responsibility of the [[app-console-input|human-in-the-loop verification gate]] at F12, not the storage layer.
- **Availability.** WORM guarantees durability; it does not guarantee that the ledger is always reachable. Uptime is an infrastructure concern.
- **Search or query access.** The ledger stores records; it does not index them. Full-text search and entity queries are provided by [[service-search|`service-search`]] and [[service-content|`service-content`]].
- **Cross-tenant isolation above the storage layer.** The WORM invariant is per-tenant. Cross-tenant access control is enforced by the wire protocol (`X-Module-ID` boundaries) and intended to be enforced by seL4 capability mediation in Envelope B.

## Key takeaways

- The WORM ledger is a structural guarantee: append-only is enforced at the API layer (`append`, `read_since`, `checkpoint` only), not by convention.
- Immutability protects the audit trail after a record lands; the [[app-console-input|F12 Input Machine]] is the quality gate before it lands.
- The C2SP tlog-tiles format and Sigstore anchoring make the ledger verifiable by a third party without access to the live service.
- The four-layer architecture allows the storage engine (Envelope A: POSIX; Envelope B: seL4 capability) to change without altering the API contract or the wire protocol.

## See also

- [[worm-ledger-design]] — regulatory compliance mapping and the structural immutability argument
- [[worm-ledger-storage-architecture]] — storage-layer detail: tile format, atomic durability, and dual-target envelopes
- [[service-fs-architecture]] — the service that implements this architecture as a per-tenant deployed ledger
- [[app-console-input]] — the F12 human-in-the-loop gate that is the quality control upstream of the ledger
- [[sel4-microkernel-substrate]] — the intended seL4 capability-enforcement trajectory for tenant isolation
