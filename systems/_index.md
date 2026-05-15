---
schema: foundry-doc-v1
title: "Systems"
slug: _index
category: systems
type: topic
quality: complete
short_description: "Eight purpose-built operating systems that share a common seL4 and Rust substrate — each does one job, contains no features it does not need, and communicates through a common Diode-based protocol discipline."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.es.md
---

PointSav builds eight purpose-built operating systems that share a common seL4 and Rust substrate. Each does one job, contains no features it does not need, and communicates through a common Diode-based protocol discipline. The result is a family that can be audited component by component, upgraded independently, and deployed in any configuration without unexpected coupling between systems.

[[os-family-overview]] is the entry point for readers new to the family. It explains the common substrate, the capability model that every OS inherits, and the Diode rule that governs how they communicate.

## The archive layer

The core record-keeping systems at the foundation of every deployment.

- [[totebox-os]] — The archive layer: one isolated, kernel-level vault per entity, storing records as inert flat files with no delete operation, exposed only through the Diode on command from os-console or os-orchestration.
- [[totebox-archive]] — A self-contained, freely transferable micro-virtual machine that persists institutional data as immutable flat files.
- [[totebox-orchestration]] — How Totebox instances are coordinated across a fleet deployment; scheduling, isolation boundaries, and upgrade paths.

## Operator surfaces

The systems through which a human operator interacts with the platform.

- [[console-os]] — The human-facing surface: a Command Ledger that connects to a Totebox and renders its state through a keyboard-driven, F-key-structured interface.
- [[os-workplace]] — The free desktop operating system: a native-Rust sovereign desktop that pairs with a Totebox archive and serves as the adoption gateway to the commercial product line.
- [[os-orchestration]] — The Fleet Aggregator for multi-entity portfolios: one operator sees, queries, and commands many Totebox archives at once.

## Network control and infrastructure

The systems that manage the network fabric and underlying compute.

- [[infrastructure-os]] — The compute substrate that hosts PointSav operating systems across on-premises, leased, and cloud hardware; bootstraps isolated fleets through the Genesis Protocol.
- [[os-network-admin]] — The control plane for a PointSav fleet: manages the pairing registry, Diode rules, and mesh routing policy; commands broadcast as 16-byte binary packets across the WireGuard mesh.
- [[os-privategit]] — Private Git hosting for sovereign version control within a fleet.

## Publishing and media

- [[mediakit-os]] — The public-facing OS: hosts a company's marketing website, internal wiki, and compliance newsroom on a single sovereign appliance the company owns outright.

## See also

- [Architecture](/architecture/) — cross-cutting platform architecture and the three-ring model
- [Services](/services/) — the autonomous services that run within and across operating systems
- [Infrastructure](/infrastructure/) — fleet deployment topology and cloud operational runtime
