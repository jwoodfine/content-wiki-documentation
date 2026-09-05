---
schema: foundry-doc-v1
title: "Operating Systems"
slug: systems-index
category: systems
type: topic
content_type: topic
quality: complete
short_description: "The purpose-built operating systems that share a common seL4 and Rust substrate — Totebox, Console, Workplace, Orchestration, Infrastructure, Network Admin, MediaKit, and PrivateGit — each doing one job, holding no features it does not need, and communicating through a common Diode-based protocol discipline."
index_type: thematic
index_scope: systems
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.es.md
---

PointSav builds a family of purpose-built operating systems that share a common seL4 and Rust substrate. Each does one job, contains no features it does not need, and communicates through a common Diode-based protocol discipline. The result is a family that can be audited component by component, upgraded independently, and deployed in any configuration without unexpected coupling between systems.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[os-family-overview]] — the entry point for readers new to the family; it explains the common substrate, the [[capability-based-security]] model every OS inherits, the [[diode-standard]] that governs how they communicate, and the [[sel4-microkernel-substrate]] that anchors them all.

<!-- END-START-HERE-HIGHLIGHT -->

## The archive layer

The core record-keeping systems at the foundation of every deployment — where the canonical record lives and how it is coordinated across a fleet.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: the-archive-layer -->
- [[totebox-os]] — os-totebox is the archive layer of the PointSav family — one isolated vault per entity, storing inert flat files with no delete, exposed via the Diode on command. Its production path hosts a Linux guest under the seL4 microkernel; other host forms exist for compatibility and local development.
- [[totebox-orchestration]] — Totebox Orchestration is the coordination layer managing multiple Totebox data-archive containers, keeping execution engines isolated from passive corporate ledgers.
- [[vm-architecture]] — The PointSav platform organises runtime deployments under five named VM types — Totebox, MediaKit, Orchestration, PrivateGit, Infrastructure — each mapping to one os-* binary.
- [[scaling-coordinated-development-totebox-archives]] — Coordination bottlenecks past twenty archives — publication serialization, message relay latency, operator load, and the path to per-archive process isolation.
- [[os-totebox-sovereign-archive]] — os-totebox is designed to become a Type I bare-metal OS built on a formally verified seL4 microkernel, with a WORM data vault enforced by a compiled capability graph — the intended end state, not the software running today.
- [[os-totebox-service-pd-model]] — How os-totebox is designed to map Rust service binaries to seL4 Protection Domains: the planned seven-PD stack, capability confinement, startup ordering, and the two-bottom development path — Phase H1 roadmap work, not the binary running today.
<!-- END AUTO-GENERATED -->

## Operator surfaces

The systems through which a human operator interacts with the platform — keyboard-driven, F-key-structured, and built around muscle memory rather than discoverability.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: operator-surfaces -->
- [[os-console]] — os-console is the human-facing surface of the PointSav platform — a single-binary, keyboard-native Command Ledger that connects to a Totebox and hosts independent TUI cartridges through a unified chassis.
- [[os-console-totebox-browser]] — os-console-totebox-browser has been folded into os-console's own 'Why this design: the browser analogy' section — this article is now a short pointer, not a separate deep dive.
- [[input-machine]] — The Input Machine is the mandatory document ingest gate in os-console, bound permanently to F12 and backed by service-input on the Totebox Archive.
- [[os-workplace]] — os-workplace is the planned free desktop tier in the PointSav family — today a growing set of independent Rust and Tauri apps an operator runs on their own computer, joining the network as a station-* WireGuard peer; the intended adoption gateway to the commercial line.
- [[os-orchestration]] — os-orchestration is the commercial-tier OS letting a single operator see, query, and command many Totebox archives at once — the Fleet Aggregator for enterprise deployments.
<!-- END AUTO-GENERATED -->

## Network control and infrastructure

The systems that manage the network fabric, the bootstrap path, and the underlying compute substrate.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: network-control-and-infrastructure -->
- [[os-network-admin]] — os-network-admin is the control plane for a PPN: WireGuard mesh routing, the node-join ceremony surface, and Diode-standard enforcement, without archive-tier authority.
- [[os-privategit]] — The OS layer hosting the private Git infrastructure underpinning the development workspace, staging-tier commit flow, and canonical repos for PointSav engineering.
- [[os-infrastructure-ppn-node]] — os-infrastructure is the OS layer for PPN nodes — its sole purpose is to set up and maintain a node: WireGuard tunnels, guest VMs, and the operator control plane.
<!-- END AUTO-GENERATED -->

## Publishing and media

The public-facing OS that hosts the company's marketing surface, internal wiki, and compliance newsroom on a single sovereign appliance.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: publishing-and-media -->
- [[os-mediakit]] — The public-web tier of the PointSav OS family — os-mediakit owns TLS, systemd lifecycle, and gateway-mediated data access; app-mediakit-knowledge/marketing/distribution own domain logic. Ubuntu 24.04 today; the planned end state is one seL4 VM per deployment instance, not a single combined appliance.
<!-- END AUTO-GENERATED -->

## See also

- [How It's Built](/architecture/) — cross-cutting platform architecture and the three-ring model
- [Platform Services](/services/) — the autonomous services that run within and across operating systems
- [Where It Runs](/infrastructure/) — fleet deployment topology and cloud operational runtime
- [Building Blocks](/substrate/) — the substrate disciplines and microkernel primitives the OS family inherits
