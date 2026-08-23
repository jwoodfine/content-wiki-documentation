---
schema: foundry-doc-v1
title: "Sovereign vault and service host"
slug: totebox-os
category: systems
type: concept
content_type: topic
quality: complete
index_group: the-archive-layer
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: totebox-os.es.md
aliases: [os-totebox]
short_description: "os-totebox is the archive layer of the PointSav family — one isolated vault per entity, storing inert flat files with no delete, exposed via the Diode on command. Its production path hosts a Linux guest under the seL4 microkernel; other host forms exist for compatibility and local development."
cites: []
references:
  - id: 1
    text: "NIST. 'Security Guidelines for Storage Infrastructure.' SP 800-209, 2020."
    url: "https://doi.org/10.6028/NIST.SP.800-209"
---

`os-totebox` is the archive layer of the PointSav family: one isolated vault per entity. It stores the records, runs the services that process them, and exposes nothing else. An entity is whatever needs a separate set of books — a person, a corporation, a real property, a project, a household. Each entity has its own `os-totebox`. Toteboxes do not share files, do not share users, and cannot see each other. They communicate only through the [[diode-standard|Diode]], and only on command from [[console-os|os-console]] or [[os-orchestration]]. This article covers the services inside, the WORM discipline, the current host shape, a known persistence limitation, the compute tiers, and the freely transferable design.

## What lives inside

Each `os-totebox` hosts a fixed set of services:

| Service | Function |
|---|---|
| `service-fs` | WORM ledger enforcer; the only service holding the block-device capability that touches raw disk |
| `service-input` | Ingest, migration, and calibration entry point; writes flow through `service-fs` |
| `service-email` | SMTP/IMAP ingest; WORM Maildir; sanitisation of HTML and tracking pixels |
| `service-people` | Identity ledger; the F2 surface; entity claims and the Sovereign-ID graph |
| `service-content` | Reads payloads, applies the editorial synthesis pipeline, generates outputs |
| `service-extraction` | Entity-mass extraction across the archive |
| `service-slm` | Local small language model; operates behind the Doorman audit boundary |

Every service above is a real, currently active crate, not a placeholder. `service-fs` is worth a specific caveat: its own companion integrity-anchoring service has been failing since 2026-08-01, and checkpoint signing is deliberately unset at this baseline — the ledger is running, but not yet fully hardened. Two functions sometimes assumed to be separate `os-totebox` services — a deep archive of immutable records and a financial ledger — are not backed by dedicated services today; the nearest existing artifacts are thin front-end views with no independent service identity behind them.

## The WORM discipline

`service-fs` writes raw payloads directly to append-only block storage. There is no delete operation in the code path. [^1] A compromised service cannot overwrite history because the verb does not exist at the storage interface. This is the architectural enforcement layer for processing integrity and the [[worm-ledger-design|WORM ledger discipline]].

Every institutional record lives as an inert flat file — Markdown, YAML, or CSV — that requires no proprietary runtime to read decades later. A `.yaml` ledger or `.csv` register is universally readable by any text editor, on any hardware, in any decade. Data migration cost falls toward zero: the operator always holds the source in a form no proprietary software can lock. The [[worm-ledger-storage-architecture|WORM storage architecture]] and [[worm-ledger-architecture|ledger architecture]] articles describe the technical implementation.

## The host shape

"`os-totebox`" names three distinct things today, and keeping them apart matters for reading the rest of this section correctly.

**The production path is a seL4-isolated Linux guest.** A hand-written, dependency-free seL4 protection domain — real, bare-metal AArch64 code, not a simulation — has booted, performed IPC, and driven genuine VirtIO network I/O to reach the Doorman service over a real TCP handshake. Above that low-level milestone sits the actual hosting design: a Microkit-managed VMM (`libvmm`) boots an ordinary, unmodified Linux guest, and the `os-totebox` binary runs inside it as the guest's own init process. seL4's formally verified capability boundary provides the isolation guarantee at the hypervisor layer; the services inside the guest run unmodified. A real, purpose-built guest root filesystem — Ubuntu 24.04 arm64 ("noble"), assembled via `debootstrap` — backs this path; the glibc base is a deliberate choice, needed for FFI compatibility with the C++ knowledge-graph engine `service-content` depends on. This produces a real, complete boot image (`loader.img`, roughly 113 MB) that has been live-verified: a genuine boot, followed by an end-to-end inference round trip through the Doorman and back. The full target architecture is a seven-domain capability map — a supervisory `watchdog-pd`, and six service domains including `service-fs-pd`, `network-pd`, `service-content-pd`, `service-people-pd`, `service-slm-pd`, and `service-extraction-pd` — with one invariant enforced at build time: only `service-fs-pd` ever receives the block-device capability. Every other domain reaches durable storage only through it.

**A NetBSD 10.1 image also exists as a transitional artifact**, not the production target. It is real and built — a genuine NetBSD cross-toolchain pipeline (`nbmakefs`, `nbinstallboot`) produces a bootable image with a Veriexec binary-signing manifest — but it is a compatibility bridge on the path to the seL4 guest above, not a parallel destination.

**A third, unrelated meaning is the plain single-process bundle that actually runs `os-totebox` locally today.** Its own `main.rs` spawns `service-content` and the Doorman (`slm-doorman-server`) as two threads inside one ordinary Linux process — each service's router and business logic are untouched, this file only launches them together. This is what is deployed as the `local-totebox.service` systemd unit on the development workspace. It is a legitimate, production-intended packaging shape in its own right (the same single-binary-multiple-role pattern used by tools like Vault or Nomad), but it is a different thing from the seL4-hosted guest described above, and the shared name is a real source of confusion worth naming plainly.

## A known limitation — data persistence inside the seL4 guest

The seL4-hosted guest's `virtio-blk` storage device is attached but is never actually mounted by the guest's own init sequence. In practice, this means a reboot of that guest currently wipes all of its data — a direct tension with this article's own "sovereign, persistent data vault" framing, and a limitation stated here plainly rather than left implicit. A related gap compounds it: the QMP-based graceful-shutdown path is documented as non-functional, because the guest declares no ACPI or power-button device for QEMU to signal — so a redeploy today hard-kills the guest with no checkpoint guarantee. Neither gap affects `service-fs`'s own WORM ledger, which is a separate, host-level service (see above); it affects the data a seL4-hosted guest itself accumulates internally. Both are known, open items, not silent defects.

## Compute tiers

`os-totebox` adjusts its behaviour to available hardware, following the [[model-tier-discipline|model-tier discipline]] that governs SLM usage:

| Tier | Profile | Capability |
|---|---|---|
| Zero-Compute Vault | ~$7/month cloud node, ≤1 GB RAM | WORM ledger and cryptographic router only; defers heavy processing to the Yo-Yo Relay |
| Yo-Yo Relay | Operator-provisioned elastic cloud node | Stateful bridge to a temporary compute node; runs batch [[service-extraction|extraction]], then tears down |
| Sovereign Iron | 16 GB+ RAM workstation or bare-metal server | Loads the full local [[service-slm|small language model]] in RAM; no cloud egress |

## Freely transferable

Every `os-totebox` instance is intended to ship as a single, signed boot image. The operator picks it up and moves it between cloud providers, a private server, or bare-metal at their own facility. There is no host operating system underneath that holds the keys. Portability of this kind is a design goal — the running instance stays the operator's property in any environment — rather than a distinct license grant; `os-totebox` itself is FSL-licensed, one of two separate licenses across the OS family (see [[legal-and-ip-structure]]).

## See also

- [[os-family-overview]] — where os-totebox fits in the eight-OS family
- [[console-os]] — the Command Ledger that connects to os-totebox and presents its state
- [[os-orchestration]] — the fleet aggregator that queries many Toteboxes at once
- [[diode-standard]] — the unidirectional protocol through which the Totebox communicates
- [[sel4-microkernel-substrate]] — the kernel underpinning os-totebox's isolation guarantees
- [[machine-based-auth]] — how pairing governs access to a Totebox
- [[worm-ledger-design]] — the append-only storage discipline enforced by os-totebox
