---
schema: foundry-doc-v1
title: "Sovereign compliance appliance"
slug: mediakit-os
category: systems
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: mediakit-os.es.md
short_description: "os-mediakit is the public-facing operating system in the PointSav family, hosting a company's marketing website, internal wiki, and compliance newsroom on a single sovereign appliance the company owns outright."
cites: []
---

`os-mediakit` is the public-facing operating system in the PointSav family. It hosts a company's marketing website, its internal wiki, and its compliance newsroom — three workloads that typically live on rented third-party platforms and that disappear the moment a subscription ends. The target operator is a [[compliance-and-continuous-disclosure|Reporting Issuer]]: a company with statutory disclosure obligations that needs mathematical proof of what it disclosed and exactly when. `os-mediakit` is built on a hardened FreeBSD base and ships three application surfaces as isolated workloads. This article covers the three surfaces, the FreeBSD licensing rationale, the [[worm-ledger-design|Compliance Ledger]], the [[diode-standard|Diode]] adapter, and the two deployment postures.

## The three application surfaces

`os-mediakit` hosts three surfaces on a single appliance. Each workload runs as an isolated instance so that a heavy database query on the wiki cannot induce latency on the landing page:

| Surface | Engine | Role |
|---|---|---|
| `app-mediakit-marketing` | Stripped static site engine with a Rust cache layer | Public landing pages and investor-relations pages |
| `app-mediakit-knowledge` | Markdown wiki engine with content-contract-conforming storage | Corporate wiki, project wiki, documentation wiki |
| `app-mediakit-distribution` | Push-based compliance feed engine | Press releases, regulatory filings, executive commentary |

## Why FreeBSD

The choice of base OS is deliberate. FreeBSD's BSD licence allows PointSav to take the code, modify it, close the modifications, and ship a proprietary distribution without obligation to open-source those modifications. The result is a legally clean path to a proprietary compliance appliance.

The intended roadmap for the substrate is a four-phase metamorphosis:

| Phase | Form | Status |
|---|---|---|
| 1 | Hardened FreeBSD host with the three apps running in jails | Initial |
| 2 | NanoBSD — a stripped, read-only variant | Planned |
| 3 | Custom kernel with interpreted-language rendering replaced by Rust | Planned |
| 4 | Unikernel — OS and application fused into a single binary | Planned |

## The Compliance Ledger

The distinguishing capability is `app-mediakit-distribution`. Conventional investor-relations platforms pull wire-service data after the fact and serve it as a static page. `os-mediakit` inverts the flow:

1. A press release is drafted inside `os-totebox` and cryptographically signed.
2. `os-totebox` pushes the signed payload to `os-mediakit-distribution` at the moment of release.
3. `os-mediakit` archives the signed content, the timestamp, and the cryptographic signature before publishing.
4. The website updates at the moment of release. The signed record remains in `os-mediakit` permanently.

The result is mathematical proof of what was disclosed and exactly when. The company does not lose its archive when a subscription ends — the company owns the appliance.

## The Diode connection

`os-mediakit` faces the public internet. `os-totebox` does not. The two connect only through a unidirectional adapter (`service-pointsav-link`, planned) that permits commands and content to flow from the internal Totebox to the public MediaKit, but never the reverse. A compromised plugin on the marketing surface cannot reach back into the corporate Totebox, because the code to do so is absent from the adapter.

The adapter is a separately installed package. Operators who do not need fleet management can run `os-mediakit` with no adapter at all; the OS has no capability to phone home.

## Standalone or federated

`os-mediakit` deploys in two postures:

| Posture | Use case | Interface |
|---|---|---|
| Standalone | A freelancer or SMB hosting one or two public sites | Local TUI accessed by SSH |
| Federated | A commercial operator managing many sites from a central fleet | The local TUI becomes a status monitor; control passes to `os-orchestration` |

Both postures use the same `os-mediakit` binary. The transition is one command: install the adapter package, perform a one-time [[machine-based-auth|pairing handshake]], and the MediaKit instance joins the [[sovereign-mesh|fleet mesh]].

## See also

- [[os-family-overview]] — the eight-OS family and how os-mediakit fits
- [[totebox-os]] — the internal vault that pushes signed content to os-mediakit
- [[diode-standard]] — the unidirectional adapter that separates the public surface from the private vault
- [[app-mediakit-knowledge]] — the documentation wiki surface
- [[compliance-and-continuous-disclosure]] — continuous-disclosure obligations and regulatory posture
- [[deployment-patterns]] — how os-mediakit appears in each canonical deployment configuration
