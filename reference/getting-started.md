---
schema: foundry-doc-v1
title: "Getting started with the PointSav platform"
slug: getting-started
category: reference
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-11
editor: pointsav-engineering
paired_with: getting-started.es.md
short_description: "An orientation to the PointSav developer platform: what it is, who it is for, where to start, and how the pieces fit together before the first task."
aliases:
  - quick-start
cites: []
---

The PointSav platform is an independently verifiable, operator-controlled software stack for commercial real estate intelligence, fleet management, and distributed compute (Correction, 2026-08-02: "sovereign" as a bare adjective is on this workspace's own Do-Not-Use list — see `editorial-language-registers.md`'s own vocabulary-retirement table — and this `audience: vendor-public` article violated it). This guide orients new contributors and evaluators to the platform's main surfaces and the documentation structure.

## Where to start

- **Developer Platform** — [[guide-catalog|Developer Guide Catalog]] lists practical how-to guides grouped by task.
- **Architecture** — [[ppn-small-business-compute|PPN Small-Business Compute]] and [[ppn-vm-resource-pool|PPN VM Resource Pool Architecture]] introduce the compute substrate.
- **Authorization model** — [[machine-based-auth|Machine-Based Authorization]] describes pairing-as-permission, the device-identity model used across the platform.
- **Data and GIS** — [[app-orchestration-gis|GIS Orchestration Platform]] covers the location intelligence engine.

## Prerequisites

- Access to a PointSav Private Network (PPN) node via pairing approval. See [[machine-based-auth|Machine-Based Authorization]] for the pairing model.
- Familiarity with command-line tooling. The platform has no graphical installer.

## First steps

A task-oriented path to a working session, for an engineer opening the platform for the first time:

1. **Verify node access.** Confirm the WireGuard tunnel is up and the fleet controller is reachable.
2. **Review the architecture overview.** Read [[ppn-small-business-compute|PPN Small-Business Compute]] for the three-node stack (fleet controller, per-node agent, tenant proxy).
3. **Create a VM.** Issue a spawn request through the tenant proxy. See the operational guides in the [[guide-catalog|Developer Guide Catalog]].
4. **Access the console surface.** The OS Console provides a terminal interface for provisioned VMs and platform management.

*This article is a stub, merged 2026-08-03 with the former `quick-start` article (same onboarding purpose, overlapping content — see `redirects.yaml` and this file's `aliases:`). Full content is planned for a future session.*
