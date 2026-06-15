---
schema: foundry-doc-v1
title: "Platform architecture overview"
slug: architecture
short_description: "The platform is designed around distributed cryptographic consistency and sovereign bootability, with the capability to collapse a federated archive into a self-contained bootable image transferable across environments."
category: architecture
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: architecture.es.md
---

The [[pointsav-overview|PointSav]] platform is designed around two structural properties: distributed [[cryptographic-ledgers|cryptographic consistency]] and sovereign bootability. Both properties are preserved across cloud and offline-vault environments simultaneously.

## Key Takeaways

- The platform maintains a single, unified cryptographic state across multiple physical environments simultaneously. An active cloud node and an offline vault share an identical [[merkle-proofs-as-substrate-primitive|Merkle root]] at all times — an auditor can verify either copy without requiring both to be online.
- Sovereign bootability means any deployment can collapse into a self-contained bootable image (`.ISO` or `.IMG`) and reconstitute on new hardware without fetching data from a remote source. The system carries its own state.
- The archive collapse operation is explicit and operator-initiated. It does not run on a schedule or trigger automatically. This is a deliberate design constraint: portability is a capability an operator invokes, not a background process.
- These two properties — cryptographic consistency and sovereign bootability — are structural, not add-ons. They are preserved simultaneously, not traded against each other when moving between cloud and offline-vault environments.

## Distributed cryptographic state

A single archive can exist across multiple physical environments — an active cloud node and an offline vault — while maintaining a single, unified cryptographic state. The two environments share an identical root [[merkle-proofs-as-substrate-primitive|Merkle hash]] at all times.

- **Active cloud node** — the live, networked copy of the archive.
- **Offline vault** — a physically isolated copy that mirrors the cloud node's Merkle root without a persistent network connection.

This shared-root property means an auditor can verify the integrity of either copy against the same hash without needing both to be online simultaneously.

## Archive collapse and portability

When an operator issues the collapse command, the platform compresses the federated cloud index and the offline physical copy into a single transferable entity. The result is a self-executing bootable image (`.ISO` or `.IMG` format).

The collapse operation is explicit and operator-initiated. It is not automatic and does not run on a schedule.

## Sovereign bootable image

The resulting image is a self-contained operating environment. It can be deployed on bare-metal hardware or imported into a commercial cloud environment. The image carries the full archive state, making it possible to reconstitute the system on new hardware without reconstructing data from a remote source.

This property is intended to guarantee operational continuity when a primary deployment environment becomes unavailable.

## See also

- [[worm-ledger-architecture]] — WORM ledger design that underpins archive integrity
- [[compounding-substrate]] — how structural properties compound across deployments
- [[customer-hostability]] — the design properties that allow a customer to host the full stack
