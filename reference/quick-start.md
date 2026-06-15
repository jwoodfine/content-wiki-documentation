---
schema: foundry-doc-v1
title: "Quick Start — First Session on the PointSav Platform"
slug: quick-start
category: reference
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-15
editor: pointsav-engineering
paired_with: quick-start.es.md
short_description: "A concise first-session guide for engineers and contributors evaluating the PointSav platform."
cites: []
---

This article is a task-oriented orientation for an engineer opening the platform for the first time. It covers the minimum set of steps to reach a working session.

## Prerequisites

- Access to a PointSav Private Network (PPN) node via pairing approval. See [[machine-based-auth|Machine-Based Authorization]] for the pairing model.
- Familiarity with command-line tooling. The platform has no graphical installer.

## First steps

1. **Verify node access.** Confirm the WireGuard tunnel is up and the fleet controller is reachable.
2. **Review the architecture overview.** Read [[ppn-small-business-compute|PPN Small-Business Compute]] for the three-node stack (fleet controller, host agent, tenant proxy).
3. **Create a VM.** Issue a spawn request through the tenant proxy. See the operational guides in the [[guide-catalog|Developer Guide Catalog]].
4. **Access the console surface.** The OS Console provides a terminal interface for provisioned VMs and platform management.

*This article is a stub. Detailed task steps are planned for a future session.*
