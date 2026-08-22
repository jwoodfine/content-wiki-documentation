---
schema: foundry-doc-v1
title: "Platform architecture overview"
slug: architecture
short_description: "The platform's cryptographic consistency rests on a real Merkle-chained ledger; sovereign bootability — collapsing a deployment into one portable image — is a design goal, not yet a shipped feature."
category: architecture
index_group: platform-structure
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: architecture.es.md
---

The [[pointsav-overview|PointSav]] platform is designed around two structural properties: cryptographic consistency, backed by a real [[merkle-proofs-as-substrate-primitive|Merkle-chained ledger]] primitive, and sovereign bootability, a planned capability. Neither an operator-triggered archive-collapse-to-bootable-image feature nor a live dual-environment (cloud-plus-offline-vault) shared-root sync exists in the platform today — both are the intended shape this article describes, not shipped mechanisms.

## Key Takeaways

- Cryptographic consistency rests on a real primitive: a [[merkle-proofs-as-substrate-primitive|Merkle-chained ledger]] with inclusion and consistency proofs, already used by several platform services for tamper-evident append-only records.
- The specific dual-environment guarantee this article describes — an active cloud node and an offline vault sharing an identical Merkle root, verifiable independently — is a design goal, not a built feature. No cross-environment sync mechanism was found in the current codebase.
- Sovereign bootability — collapsing a deployment into a self-contained bootable image and reconstituting it on new hardware without a remote source — is also a design goal. Real bootable-image tooling exists for several individual platform products; an operator-triggered "collapse this archive's current state" command spanning cloud and offline copies does not.
- Both properties are intended to be structural once built, not add-ons — but stating them as already operating would overclaim what's shipped today.

## The cryptographic ledger primitive

The real building block behind the consistency claim is the platform's [[merkle-proofs-as-substrate-primitive|Merkle-chained ledger]]: an append-only structure with cryptographic checkpoints and inclusion/consistency proofs, already in use by several services for tamper-evident records. What is not built is the specific dual-environment property described below — a live cloud node and an offline vault continuously sharing one verified root.

## Planned: dual-environment shared state

The intended design: a single archive would exist across two physical environments — an active cloud node and a physically isolated offline vault — sharing an identical Merkle root at all times, so an auditor could verify either copy independently without both being online. This is forward-looking; no synchronization mechanism implementing it exists in the platform today.

## Planned: archive collapse and portability

The intended design: an operator-issued command would compress a deployment's state into a single self-executing bootable image. Real bootable-image build tooling exists for individual platform products today (compiling a specific product into a `.img` for its own deployment target), but a general "collapse this live archive, including its offline-vault counterpart, into one portable image" operator command does not exist. The design intent is for this operation to be explicit and operator-initiated, never automatic or scheduled.

## See also

- [[worm-ledger-architecture]] — WORM ledger design that underpins archive integrity
- [[compounding-substrate]] — how structural properties compound across deployments
- [[customer-hostability]] — the design properties that allow a customer to host the full stack
