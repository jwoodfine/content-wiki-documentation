---
schema: foundry-topic-v1
title: "Platform Architecture Overview"
slug: architecture
category: architecture
status: published
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
---

The PointSav platform is designed around two structural properties: distributed cryptographic consistency and sovereign bootability. Both properties are preserved across cloud and offline-vault environments simultaneously.

## Distributed cryptographic state

A single archive can exist across multiple physical environments — an active cloud node and an offline vault — while maintaining a single, unified cryptographic state. The two environments share an identical root Merkle hash at all times.

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

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
