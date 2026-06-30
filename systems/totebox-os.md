---
schema: foundry-doc-v1
title: "Sovereign vault and service host"
slug: totebox-os
category: systems
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: totebox-os.es.md
aliases: [os-totebox]
short_description: "os-totebox is the archive layer of the PointSav family — one isolated, kernel-level vault per entity, storing records as inert flat files with no delete operation and exposing them only through the Diode on command from os-console or os-orchestration."
cites: []
references:
  - id: 1
    text: "NIST. 'Security Guidelines for Storage Infrastructure.' SP 800-209, 2020."
    url: "https://doi.org/10.6028/NIST.SP.800-209"
  - id: 2
    text: "Madhavapeddy, A. et al. 'Unikernels: Library Operating Systems for the Cloud.' ACM ASPLOS, 2013."
    url: "https://dl.acm.org/doi/10.1145/2451116.2451167"
---

`os-totebox` is the archive layer of the PointSav family: one isolated, kernel-level vault per entity. It stores the records, runs the services that process them, and exposes nothing else. An entity is whatever needs a separate set of books — a person, a corporation, a real property, a project, a household. Each entity has its own `os-totebox`. Toteboxes do not share files, do not share users, and cannot see each other. They communicate only through the [[diode-standard|Diode]], and only on command from [[console-os|os-console]] or [[os-orchestration]]. This article covers the services inside, the WORM discipline, the host shape evolution, the compute tiers, and the freely transferable design.

## What lives inside

Each `os-totebox` hosts a fixed set of services:

| Service | Function |
|---|---|
| `service-email` | SMTP/IMAP ingest; WORM Maildir; sanitisation of HTML and tracking pixels |
| `service-people` | Identity ledger; the F2 surface; entity claims and the Sovereign-ID graph |
| `service-content` | Reads payloads, applies the editorial synthesis pipeline, generates outputs |
| `service-extraction` | Entity-mass extraction across the archive |
| `service-slm` | Local small language model; operates behind the Doorman audit boundary |
| `service-minutebook` | Deep record archive — immutable PDFs, DOCX, XLSX, with cryptographic checksums |
| `service-bookkeeper` | Financial ledger |
| `service-fs` (planned) | Unikernel file-system service — the only service that touches raw disk |
| `service-audit` (planned) | Append-only ledger at the microkernel level |
| `service-resolution` (planned) | Asset-resolution packager — the self-executing parachute on vendor failure |

## The WORM discipline

`os-totebox` writes raw payloads directly to append-only block storage. There is no delete operation in the code path. [^1] A compromised service cannot overwrite history because the verb does not exist at the storage interface. This is the architectural enforcement layer for processing integrity and the [[worm-ledger-design|WORM ledger discipline]].

Every institutional record lives as an inert flat file — Markdown, YAML, or CSV — that requires no proprietary runtime to read decades later. A `.yaml` ledger or `.csv` register is universally readable by any text editor, on any hardware, in any decade. Data migration cost falls toward zero: the operator always holds the source in a form no proprietary software can lock. The [[worm-ledger-storage-architecture|WORM storage architecture]] and [[worm-ledger-architecture|ledger architecture]] articles describe the technical implementation.

## The host shape

`os-totebox` is designed to evolve across four phases as the seL4 substrate matures:

| Phase | Form | Use case |
|---|---|---|
| 1 | LXC / FreeBSD jail | Active development; iterates quickly |
| 2 | Hardened FreeBSD instance | First customer deployments (planned) |
| 3 | seL4 + Rust monolith | Production hardening (planned) |
| 4 | Unikernel — single binary, ~15 MB, <50 ms boot | End-state (planned) |

The unikernel target is the design goal. [^2] The end-state has no SSH, no shell, no Bash, no Python interpreter — only one compiled binary fused to hardware drivers. An operator recompiles the vendor source in the monorepo and reboots the cloud node with the new image; there is no shell to log into.

## Compute tiers

`os-totebox` adjusts its behaviour to available hardware, following the [[model-tier-discipline|model-tier discipline]] that governs SLM usage:

| Tier | Profile | Capability |
|---|---|---|
| Zero-Compute Vault | ~$7/month cloud node, ≤1 GB RAM | WORM ledger and cryptographic router only; defers heavy processing to the Yo-Yo Relay |
| Yo-Yo Relay | Operator-provisioned elastic cloud node | Stateful bridge to a temporary compute node; runs batch [[service-extraction|extraction]], then tears down |
| Sovereign Iron | 16 GB+ RAM workstation or bare-metal server | Loads the full local [[service-slm|small language model]] in RAM; no cloud egress |

## Freely transferable

Every `os-totebox` instance is intended to ship as a single disk image (`.img` or `.vmdk`). The operator picks it up and moves it between cloud providers, a private server, or bare-metal at their own facility. There is no host operating system underneath that holds the keys. This is the Sovereign Addendum's intended commitment in physical form: the running instance remains the operator's property in any environment.

## See also

- [[os-family-overview]] — where os-totebox fits in the eight-OS family
- [[console-os]] — the Command Ledger that connects to os-totebox and presents its state
- [[os-orchestration]] — the fleet aggregator that queries many Toteboxes at once
- [[diode-standard]] — the unidirectional protocol through which the Totebox communicates
- [[sel4-microkernel-substrate]] — the kernel underpinning os-totebox's isolation guarantees
- [[machine-based-auth]] — how pairing governs access to a Totebox
- [[worm-ledger-design]] — the append-only storage discipline enforced by os-totebox
