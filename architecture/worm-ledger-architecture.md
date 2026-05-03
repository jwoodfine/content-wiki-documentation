---
schema: foundry-doc-v1
type: topic
slug: worm-ledger-architecture
title: WORM Ledger Substrate: Four-Layer Architecture
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: worm-ledger-architecture.es.md
---

# WORM Ledger Substrate: Four-Layer Architecture

Foundry’s `service-fs` provides the per-tenant Write-Once-Read-Many (WORM) immutable ledger that serves as the durable backbone for all Ring 1 boundary-ingest services. By enforcing a strict append-only invariant through cryptographic hash-chaining and structural isolation, Foundry ensures that identity, communications, and document records remain tamper-evident and permanently accessible.

## Architectural Integration

The {{gli|WORM}} ledger sits at the critical boundary between the per-tenant data plane and the multi-tenant knowledge plane. Every ingest service—including `service-people` and `service-email`—writes through this substrate, while Ring 2 services access data via cursor-paged {{gli|MCP}} queries.

*   **Current Posture:** Isolation is achieved through separate daemon processes per tenant `moduleId` and rigorous filesystem permissioning.
*   **Intended Trajectory:** Migration to {{gli|seL4}} microkernel-level capability enforcement is planned to provide formally verified tenant isolation.

## Multi-Tier Protocol Stack

The architecture utilizes a layered design to ensure that individual components remain swappable without disrupting the core durability contract.

### Layer 4: Cryptographic Anchoring
Checkpoints are intended to be anchored monthly to the public Sigstore {{gli|Rekor}} transparency log (per the fundamental physics of 2030 hyperscaler infrastructure). This provides external verifiability without exposing raw tenant data.

### Layer 3: Wire-Level Abstraction
Today, services communicate via axum-based HTTP with mandatory `X-Foundry-Module-ID` headers. Long-term, this is intended to transition to a native {{gli|MCP}}-server interface across both Linux and {{gli|seL4}} targets.

### Layer 2: Core State API
The stable core contract defining methods for `append`, `read_since`, and `checkpoint`. This target-independent layer ensures consistency regardless of the underlying storage engine.

### Layer 1: Storage Primitives
*   **Linux/BSD (Current):** POSIX files using atomic write-then-rename discipline.
*   **seL4 (Intended):** Capability-addressed objects mediated by `moonshot-database`.
*   **Format:** Standardized **{{gli|C2SP}} tlog-tiles** (matching RFC 9162 v2 / {{gli|Rekor}} v2) ensure 100-year readability.

## Regulatory Compliance and Durability

The design is engineered to align with SEC Rule 17a-4(f) {{gli|WORM}} requirements and EU eIDAS qualified preservation standards. By adopting the plain-text {{gli|C2SP}} tile format, Foundry guarantees that a forensic analyst in the year 2126 could decode the storage using only basic Unix utilities and a SHA-256 implementation.

## Cross-Target Synthesis

Foundry’s implementation is unique in its dual-target Rust strategy, allowing the same binary to serve as a Linux daemon today and an {{gli|seL4}} unikernel tomorrow. This ensures that the storage substrate is portable from a virtual machine to a future ToteboxOS hardware appliance without a core rewrite.
