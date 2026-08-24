---
schema: foundry-doc-v1
title: "Three-layer stack"
slug: 3-layer-stack
category: architecture
index_group: platform-structure
type: topic
content_type: topic
quality: stub
short_description: "The Three-Layer Stack is the infrastructure decomposition pattern across PointSav deployments, separating raw compute, isolated platform execution, and secure operator access."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites: []
paired_with: 3-layer-stack.es.md
---


> Not to be confused with [[three-layer-architecture|three-layer architecture]], a
> different three-layer model describing how PointSav deliverables move from vendor to
> customer to operator. This article is about the runtime decomposition of a single
> deployment; that one is about the software supply chain.

> The Three-Layer Stack is the infrastructure decomposition pattern used across PointSav deployments, separating raw computing capability, isolated platform execution, and secure operator access into three distinct layers.

**The Three-Layer Stack** is the foundational infrastructure pattern that decouples operational logic from physical hardware across [[pointsav-overview|PointSav]] deployments. The infrastructure layer provides raw computing capability — bare metal, cloud instances, or customer hardware. The platform layer runs [[totebox-os|the archive service]] and the rest of the Ring 1/Ring 2 service set; [[sel4-microkernel-substrate|microkernel isolation]] is the design target for this layer and has a real, working proof for the archive service specifically, but most services running today do so as ordinary processes, not yet under kernel-enforced isolation. The delivery layer provides secure terminal access so operators interact with the system without touching the underlying infrastructure directly. Each layer is independently replaceable, which means a customer can migrate from a cloud infrastructure layer to on-premises hardware without changing how the platform layer operates.

## Key Takeaways

- Three distinct layers: Infrastructure (raw compute — bare metal, cloud, or customer hardware), Platform (service execution with capability-scoped access, kernel-level isolation proven for one service and the design target for the rest), Delivery (terminal and console interfaces operators interact with directly).
- Independent replaceability at each layer. Migrating from a cloud infrastructure to on-premises hardware does not require changes to the platform layer. The layers are decoupled by design, not by convention.
- No component at the platform layer is intended to exceed its explicitly granted capabilities. [[sel4-microkernel-substrate|Kernel-level isolation]] enforcing that boundary is proven for the archive service's boot path; most other services run today without it.
- The delivery layer is the only layer operators touch directly. It forwards requests into the platform and returns results upward; operators never have direct access to infrastructure-layer primitives such as raw disk or network interfaces.

## Overview

The three layers map directly to the operational concerns of a regulated SMB deployment:

- **Infrastructure layer** — the physical or virtual computing substrate: bare-metal servers, GCE instances, customer iMac hardware, or any combination. This layer supplies CPU time and memory. It makes no security guarantees above what the hardware provides.
- **Platform layer** — the operating system and service execution environment: [[totebox-os|the archive service]] and the [[three-ring-architecture|Ring 1/Ring 2]] service processes. Kernel-enforced isolation between components is the design target, proven for the archive service's own boot path; most services today run as ordinary processes without that isolation guarantee. Capability-scoped access — no component exceeding what it's explicitly granted — is the intended boundary regardless of which isolation mechanism enforces it.
- **Delivery layer** — the terminal and console interfaces operators use: [[os-console|ConsoleOS]] terminals, the proofreader interface, and any browser-based access surface. The delivery layer is the only layer operators interact with directly; it forwards requests down into the platform and returns results upward.

## See also

- [[three-layer-architecture]] — a different three-layer model: the vendor/customer/operator software supply chain, not this article's runtime decomposition
- [[compounding-substrate]]
- [[capability-based-security]]
- [[sel4-microkernel-substrate]]
- [[sovereign-ai-routing]]
- [[worm-ledger-architecture]]
