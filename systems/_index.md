---
schema: foundry-doc-v1
title: "Systems"
slug: _index
category: systems
type: topic
content_type: topic
quality: complete
short_description: "The purpose-built operating systems that share a common seL4 and Rust substrate — Totebox, Console, Workplace, Orchestration, Infrastructure, Network Admin, MediaKit, and PrivateGit — each doing one job, holding no features it does not need, and communicating through a common Diode-based protocol discipline."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.es.md
---

PointSav builds a family of purpose-built operating systems that share a common seL4 and Rust substrate. Each does one job, contains no features it does not need, and communicates through a common Diode-based protocol discipline. The result is a family that can be audited component by component, upgraded independently, and deployed in any configuration without unexpected coupling between systems.

[[os-family-overview]] is the entry point for readers new to the family — it explains the common substrate, the [[capability-based-security]] model that every OS inherits, the [[diode-standard]] that governs how they communicate, and the [[sel4-microkernel-substrate]] that anchors them all to a mathematically formally verified L1 kernel.

## The archive layer

The core record-keeping systems at the foundation of every deployment — where the canonical record lives and how it is coordinated across a fleet.

- [[totebox-os]] — The archive layer: one isolated, kernel-level vault per entity, storing records as inert flat files with no delete operation, exposed only through the Diode on command from os-console or os-orchestration.
- [[totebox-archive]] — A self-contained, freely transferable micro-virtual machine that persists institutional data as immutable flat files.
- [[totebox-orchestration]] — The coordination layer that manages multiple Totebox data-archive containers, keeping software execution engines isolated from passive corporate ledgers across deployments.

## Operator surfaces

The systems through which a human operator interacts with the platform — keyboard-driven, F-key-structured, and built around muscle memory rather than discoverability.

- [[console-os]] — The human-facing surface: a Command Ledger that connects to a Totebox and renders its state through a keyboard-driven, F-key-structured interface.
- [[os-console-platform]] — The Rust binary that implements os-console: cartridge architecture, F-key-navigated modules, keyboard-native access to Totebox Archive workflows.
- [[input-machine]] — The mandatory document ingest gate in os-console, bound permanently to F12 and backed by `service-input` on the Totebox Archive.
- [[os-workplace]] — The free desktop operating system: a native-Rust sovereign desktop that pairs with a Totebox archive and serves as the adoption gateway to the commercial product line.
- [[os-orchestration]] — The Fleet Aggregator for multi-entity portfolios: one operator sees, queries, and commands many Totebox archives at once.

## Network control and infrastructure

The systems that manage the network fabric, the bootstrap path, and the underlying compute substrate.

- [[infrastructure-os]] — The compute substrate that hosts PointSav operating systems across on-premises, leased, and cloud hardware; bootstraps isolated fleets through the Genesis Protocol.
- [[os-network-admin]] — The control plane for a fleet: manages the pairing registry, Diode rules, and mesh routing policy; commands broadcast as 16-byte binary packets across the WireGuard mesh.
- [[os-privategit]] — Private Git hosting for sovereign version control within a fleet.
- [[os-privategit-workbench]] — The browser-based file editor included in os-privategit: a three-column interface for working with archive files without a terminal session.

## Publishing and media

The public-facing OS that hosts the company's marketing surface, internal wiki, and compliance newsroom on a single sovereign appliance.

- [[mediakit-os]] — The public-facing OS: hosts a company's marketing website, internal wiki, and compliance newsroom on a single sovereign appliance the company owns outright.

## See also

- [Architecture](/architecture/) — cross-cutting platform architecture and the three-ring model
- [Services](/services/) — the autonomous services that run within and across operating systems
- [Infrastructure](/infrastructure/) — fleet deployment topology and cloud operational runtime
- [Substrate](/substrate/) — the substrate disciplines and microkernel primitives the OS family inherits
