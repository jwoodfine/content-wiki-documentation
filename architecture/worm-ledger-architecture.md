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

## Strategic Position

The WORM ledger sits at the critical boundary between the per-tenant data plane and the multi-tenant knowledge plane. Every ingest service—including `service-people` and `service-email`—writes through this substrate, while Ring 2 services access data via cursor-paged MCP queries.

*   **Current Posture:** Isolation is achieved through separate daemon processes per tenant `moduleId` and rigorous filesystem permissioning.
*   **Intended Trajectory:** Migration to seL4 microkernel-level capability enforcement is planned to provide formally verified tenant isolation.

## The Four-Layer Stack

The architecture utilizes a layered design to ensure that individual components remain swappable without disrupting the core durability contract.

### L4: Anchoring (Workspace-Tier)
Checkpoints are intended to be anchored monthly to the public Sigstore Rekor transparency log (per Doctrine Invention #7). This provides external verifiability without exposing raw tenant data.

### L3: Wire Protocol
Today, services communicate via axum-based HTTP with mandatory `X-Foundry-Module-ID` headers. Long-term, this is intended to transition to a native MCP-server interface across both Linux and seL4 targets.

### L2: WORM Ledger API (Rust Trait)
The stable core contract defining methods for `append`, `read_since`, and `checkpoint`. This target-independent layer ensures consistency regardless of the underlying storage engine.

### L1: Tile Storage Primitive (Envelope-Specific)
*   **Linux/BSD (Current):** POSIX files using atomic write-then-rename discipline.
*   **seL4 (Intended):** Capability-addressed objects mediated by `moonshot-database`.
*   **Format:** Standardized **C2SP tlog-tiles** (matching RFC 9162 v2 / Rekor v2) ensure 100-year readability.

## Compliance and Durability

The design is engineered to align with SEC Rule 17a-4(f) WORM requirements and EU eIDAS qualified preservation standards. By adopting the plain-text C2SP tile format, Foundry guarantees that a forensic analyst in the year 2126 could decode the storage using only basic Unix utilities and a SHA-256 implementation.

## Innovation and Synthesis

Foundry’s implementation is unique in its dual-target Rust strategy, allowing the same binary to serve as a Linux daemon today and an seL4 unikernel tomorrow. This ensures that the storage substrate is portable from a virtual machine to a future ToteboxOS hardware appliance without a core rewrite.
