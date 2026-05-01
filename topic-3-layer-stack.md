---
schema: foundry-doc-v1
title: "Three-Layer Stack"
slug: topic-3-layer-stack
category: architecture
type: topic
quality: stub
short_description: "The Three-Layer Stack is the infrastructure decomposition pattern used across PointSav deployments, separating raw computing capability, isolated platform execution, and secure operator access into three distinct layers."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-3-layer-stack.es.md
---

# Three-Layer Stack

> The Three-Layer Stack is the infrastructure decomposition pattern used across PointSav deployments, separating raw computing capability, isolated platform execution, and secure operator access into three distinct layers.

**The Three-Layer Stack** is the foundational infrastructure pattern that decouples operational logic from physical hardware across PointSav deployments. The infrastructure layer provides raw computing capability — bare metal, cloud instances, or customer hardware. The platform layer runs isolated micro-kernels and services, applying capability-based security boundaries between components. The delivery layer provides secure terminal access so operators interact with the system without touching the underlying infrastructure directly. Each layer is independently replaceable, which means a customer can migrate from a cloud infrastructure layer to on-premises hardware without changing how the platform layer operates.

<!-- EXPAND: lead needs 200+ words -->

## Overview

The three layers map directly to the operational concerns of a regulated SMB deployment:

- **Infrastructure layer** — the physical or virtual computing substrate: bare-metal servers, GCE instances, customer iMac hardware, or any combination. This layer supplies CPU time and memory. It makes no security guarantees above what the hardware provides.
- **Platform layer** — the operating system and service execution environment: ToteboxOS, capability managers, and the Ring 1/Ring 2 service processes. Isolation between components is enforced at this layer. No component at the platform layer can exceed the capabilities explicitly granted to it.
- **Delivery layer** — the terminal and console interfaces operators use: ConsoleOS terminals, the proofreader interface, and any browser-based access surface. The delivery layer is the only layer operators interact with directly; it forwards requests down into the platform and returns results upward.

## See Also

- [[compounding-substrate]]
- [[capability-based-security]]
- [[sel4-foundation]]
- [[sovereign-ai-routing]]
- [[worm-ledger-architecture]]

## References

- `conventions/three-ring-architecture.md` — the Ring 1 / Ring 2 / Ring 3 service model that sits inside the platform layer
- `DOCTRINE.md §IV` — workspace topology and deployment pattern
- `IT_SUPPORT_Nomenclature_Matrix_V8.md §3` — canonical OS and service names

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.