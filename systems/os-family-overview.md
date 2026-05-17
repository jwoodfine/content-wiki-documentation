---
schema: foundry-doc-v1
title: "The OS family — eight operating systems, one substrate"
slug: os-family-overview
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: os-family-overview.es.md
short_description: "PointSav builds eight purpose-built operating systems that share a common seL4 + Rust substrate. Each does one job, contains no features it does not need, and communicates through a common Diode-based protocol discipline."
cites: []
---

PointSav builds eight purpose-built operating systems that share a common seL4 microkernel substrate, a common Rust language discipline, and a common Diode-based communication protocol. Each OS does one job and contains no feature it does not need. The family ranges from a human-facing terminal to a sovereign cloud appliance, yet every member compiles from the same kernel and speaks the same protocol. This article covers the eight members of the OS family, the substrate they share, how they compose into deployments, and the Diode discipline that governs command flow across all of them.

## The eight operating systems

| OS | Role | Operated by |
|---|---|---|
| `os-console` | Universal human terminal — the Command Ledger | The operator at the keyboard |
| `os-totebox` | Sovereign vault and service host — the data archive | An entity (person, corporation, property) |
| `os-orchestration` | Fleet aggregator — multi-archive view for commercial operators | Enterprise administrator |
| `os-infrastructure` | Compute substrate that hosts the others | Fleet administrator |
| `os-network-admin` | Network control plane — routing, pairing registry, mesh policy | Network architect |
| `os-mediakit` | Public web appliance — marketing, wiki, compliance newsroom | Reporting Issuer or SMB |
| `os-privategit` | Sovereign source and design hosting | PointSav internal and customer |
| `os-workplace` | Sovereign desktop with native Rust apps | Community and SMB customer |

## Why eight, not one

Conventional operating systems try to be everything: accounting, email, secure browsing, video editing. The result is a large attack surface and constant feature drift. PointSav inverts the model: every OS is small, single-purpose, and replaceable. If a deployment does not need a fleet aggregator, it does not include `os-orchestration`. If it has no public website, it does not include `os-mediakit`. Each OS is a piece of precision plumbing, not a platform.

## The shared substrate

All eight operating systems share the same foundational layer:

| Layer | Component | Purpose |
|---|---|---|
| Kernel | [[sel4-microkernel-substrate|seL4 microkernel]] | Mathematically verified hardware isolation |
| Language | Rust (memory-safe; no garbage collector) | All `system-*`, `service-*`, and `os-*` code; C/C++ banned at L3 and above |
| Drivers | sDDF (seL4 Device Driver Framework) | Direct hardware access without runtime bloat |
| Protocol | PointSav Protocol (PSP) | Capability-based binary protocol; tunnels through TLS and VirtIO at the edge |
| Trust | `service-pairing` | Hardware-bound cryptographic pairings; no usernames, no passwords |
| Audit | Append-only ledger (planned) | Tamper-resistant event record that cannot be disabled by an administrator |
| Transferability | Sovereign Addendum (planned) | The running instance remains the operator's property in any cloud provider |

## How they compose into deployments

The minimum viable deployment is one operator running `os-console`, connected to one `os-totebox` hosted in the cloud. The Console is the keyboard and screen; the Totebox is the vault and the worker.

The largest deployment is hundreds of `os-totebox` instances spread across on-premises, leased, and cloud `os-infrastructure` nodes, governed by one `os-network-admin`, and aggregated through `os-orchestration` for executive review. Both extremes use the same binaries. Scale is a configuration matter, not a code fork.

The six canonical compositions are covered in detail in [[deployment-patterns]].

## The Diode discipline

Across all eight, command flow is unidirectional. `os-console` and `os-orchestration` can issue commands to the others. The others emit telemetry upward — never commands in the reverse direction. This constraint is enforced at the [[diode-standard|Diode]] protocol level, not by policy. A compromised public-facing `os-mediakit` instance cannot reach back into a corporate `os-totebox` because the code to do so is absent from the binary.

## See also

- [[console-os]] — the Command Ledger terminal; human-facing surface
- [[totebox-os]] — the sovereign vault and service host
- [[os-orchestration]] — the fleet aggregator for commercial deployments
- [[sel4-microkernel-substrate]] — the shared seL4 kernel and why PointSav adopted it
- [[diode-standard]] — the Diode protocol that governs unidirectional command flow
- [[deployment-patterns]] — the six canonical deployment configurations
- [[six-tier-sovereignty-matrix]] — how the `os-*` family fits the broader six-tier model
- [[machine-based-auth]] — hardware-bound pairing across all OS members
