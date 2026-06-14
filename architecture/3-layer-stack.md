---
schema: foundry-doc-v1
title: "Three-layer stack"
slug: 3-layer-stack
category: architecture
type: topic
content_type: topic
quality: stub
short_description: "The Three-Layer Stack is the infrastructure decomposition pattern used across PointSav deployments, separating raw computing capability, isolated platform execution, and secure operator access into three distinct layers."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: 3-layer-stack.es.md
---


> The Three-Layer Stack is the infrastructure decomposition pattern used across PointSav deployments, separating raw computing capability, isolated platform execution, and secure operator access into three distinct layers.

**The Three-Layer Stack** is the foundational infrastructure pattern that decouples operational logic from physical hardware across [[pointsav-overview|PointSav]] deployments. The infrastructure layer provides raw computing capability — bare metal, cloud instances, or customer hardware. The platform layer runs isolated [[sel4-microkernel-substrate|micro-kernels]] and services, applying [[capability-based-security|capability-based security]] boundaries between components. The delivery layer provides secure terminal access so operators interact with the system without touching the underlying infrastructure directly. Each layer is independently replaceable, which means a customer can migrate from a cloud infrastructure layer to on-premises hardware without changing how the platform layer operates.

<!-- EXPAND: lead needs 200+ words -->

## Overview

The three layers map directly to the operational concerns of a regulated SMB deployment:

- **Infrastructure layer** — the physical or virtual computing substrate: bare-metal servers, GCE instances, customer iMac hardware, or any combination. This layer supplies CPU time and memory. It makes no security guarantees above what the hardware provides.
- **Platform layer** — the operating system and service execution environment: [[totebox-os|ToteboxOS]], capability managers, and the [[three-ring-architecture|Ring 1/Ring 2]] service processes. Isolation between components is enforced at this layer. No component at the platform layer can exceed the capabilities explicitly granted to it.
- **Delivery layer** — the terminal and console interfaces operators use: [[console-os|ConsoleOS]] terminals, the proofreader interface, and any browser-based access surface. The delivery layer is the only layer operators interact with directly; it forwards requests down into the platform and returns results upward.

## See also

- [[compounding-substrate]]
- [[capability-based-security]]
- [[sel4-microkernel-substrate]]
- [[sovereign-ai-routing]]
- [[worm-ledger-architecture]]
