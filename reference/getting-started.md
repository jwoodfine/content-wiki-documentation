---
schema: foundry-doc-v1
title: "Getting started with the PointSav platform"
slug: getting-started
category: reference
index_group: platform-orientation
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: getting-started.es.md
short_description: "An orientation to the PointSav developer platform: what it is, who it is for, where to start, and how the pieces fit together before the first task."
aliases:
  - quick-start
cites: []
---

The PointSav platform is an independently verifiable, operator-controlled software stack for commercial real estate intelligence, fleet management, and distributed compute. This guide orients new contributors and evaluators to the platform's main surfaces and the documentation structure.

## Where to start

- **Developer Platform** — [[guide-catalog|Developer Guide Catalog]] lists practical how-to guides grouped by task.
- **Architecture** — [[ppn-small-business-compute|PPN Small-Business Compute]] and [[ppn-vm-resource-pool|PPN VM Resource Pool Architecture]] introduce the compute substrate.
- **Authorization model** — [[machine-based-auth|Machine-Based Authorization]] describes pairing-as-permission, the device-identity model used across the platform.
- **Data and GIS** — [[app-orchestration-gis|GIS Orchestration Platform]] covers the location intelligence engine.

## Prerequisites

- Access to a PointSav Private Network (PPN) node via pairing approval. See [[machine-based-auth|Machine-Based Authorization]] for the pairing model.
- Familiarity with command-line tooling. The platform has no graphical installer.

## First steps

For an engineer opening the platform for the first time, a working session depends on four things falling into place: reachable node access over the WireGuard tunnel and fleet controller; familiarity with the three-node compute stack described in [[ppn-small-business-compute|PPN Small-Business Compute]] (fleet controller, per-node agent, tenant proxy); the ability to spawn a VM through the tenant proxy; and the OS Console, the terminal interface used for provisioned VMs and platform management. The runnable, step-by-step version of this path lives in the [[guide-catalog|Developer Guide Catalog]].

This orientation covers where to start and the prerequisites for a first working session; a fuller walkthrough of the platform's surfaces is not yet written.
