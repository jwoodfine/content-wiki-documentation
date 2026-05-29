---
schema: foundry-doc-v1
title: "Sovereign desktop"
slug: os-workplace
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: os-workplace.es.md
short_description: "os-workplace is the free desktop operating system in the PointSav family — a native-Rust sovereign desktop that pairs with a Totebox archive, runs on deliberate reference hardware, and serves as the adoption gateway to the commercial PointSav product line."
cites: []
references:
 - id: 1
 text: "ISO 19005-1:2005 — Document management — Electronic document file format for long-term preservation — Part 1: Use of PDF 1.4 (PDF/A-1)."
 url: "https://www.iso.org/standard/38920.html"
 - id: 2
 text: "W3C. 'WebRTC 1.0: Real-Time Communication Between Browsers.' W3C Recommendation, 2021."
 url: "https://www.w3.org/TR/webrtc/"
---

`os-workplace` is the free desktop operating system in the PointSav family. It provides a clean, secure, native-Rust desktop environment that pairs naturally with a [[totebox-archive|Totebox archive]] and brings the F-key discipline and [[machine-based-auth|security model]] of the platform to a community user installing it for the first time. The strategy is deliberate: `os-workplace` is the adoption gateway. A new user installs it because it is free and fast; once their daily work happens inside the PointSav ecosystem, the commercial [[os-orchestration|`os-orchestration`]] aggregator becomes a logical next step. This article covers the reference hardware, the application suite, the pairing model, and the strategic rationale for a free desktop.

## Reference hardware

`os-workplace` targets a small, deliberate set of devices. Hardware fragmentation is the enemy of stability; the official reference profiles are chosen for first-class driver support under a hardened FreeBSD or seL4 base:

| Tier | Device |
|---|---|
| Flagship | Dell XPS 13 / 14 (Developer Edition) |
| Fleet | HP ProBook 400 series (445/450) |

The kernel evolution mirrors the rest of the family: Phase 1 runs on a hardened FreeBSD desktop profile; Phase 2 (planned) migrates to a native [[sel4-microkernel-substrate|seL4]] microkernel build.

## The application suite

All applications are native Rust binaries. The choice is principled: an SMB customer in 2030 values local-first performance and offline reliability over browser-based subscription tooling. Each app is small, single-purpose, and starts in under 100 milliseconds.

| App | Source approach |
|---|---|
| `app-workplace-pdfs` | Fork of `pdf-rs`; ISO PDF/A fidelity only [^1] |
| `app-workplace-wordprocessor` | Typst engine for document layout |
| `app-workplace-spreadsheet` | IronCalc — deterministic-maths Rust engine |
| `app-workplace-email` | Fork of Himalaya; TUI-first, local-first |
| `app-workplace-browser` | Fork of Servo; telemetry removed |
| `app-workplace-communications` | WebRTC-based peer-to-peer Rust client [^2] |
| `app-workplace-chat` | Real-time secure messaging |
| `app-workplace-file-manager` | Fork of Broot; fuzzy-search, action-triggered |
| `app-workplace-wiki` | Offline-first documentation viewer |
| `app-workplace-gis` (planned) | Fork of Whitebox-tools; pure-Rust geospatial |
| `app-workplace-bim` (planned) | ifc-rs and truck B-rep kernel |

## Pairing with the Totebox

`os-workplace` is the user's local environment. Data lives in the user's [[totebox-os|os-totebox]]. A pairing handshake between the workstation and the archive establishes hardware-bound trust through `service-pairing`. There are no usernames or passwords — the pairing is the permission.

A user can carry `os-workplace` on a USB drive, boot it on a borrowed machine, and have the same secure environment without leaving traces on the host. Closing the session wipes the secure memory. The Totebox remains untouched in the cloud.

## Why a free desktop is strategic

Three reasons make `os-workplace` a structural commitment rather than a marketing gesture:

1. **Adoption funnel.** A free, fast desktop introduces the operator to the F-key discipline of [[console-os|`os-console`]] and the security model of the [[diode-standard|Diode]]. The commercial products feel familiar from day one.
2. **Reference implementation.** Every line of code written for `os-workplace` is reviewable in the public monorepo. Customers can audit the [[compounding-substrate|substrate]] before they buy commercial aggregation against it.
3. **Ecosystem gravity.** A growing community of `os-workplace` users creates an independent constituency of contributors, packagers, and translators that no commercial-only product can replicate. The [[contributor-model|contributor model]] describes the roles and rights for community participation.

## See also

- [[os-family-overview]] — the eight-OS family and where os-workplace fits
- [[totebox-os]] — the data partner; the archive os-workplace pairs with
- [[console-os]] — the alternative TUI-first surface for operators who want keyboard-only control
- [[machine-based-auth]] — the pairing model that replaces usernames and passwords
- [[hardware-reference]] — full CPU and hardware requirements for the PointSav family
