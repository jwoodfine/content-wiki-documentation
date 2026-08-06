---
schema: foundry-doc-v1
title: "Sovereign desktop"
slug: os-workplace
category: systems
type: concept
content_type: topic
quality: complete
index_group: operator-surfaces
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: os-workplace.es.md
short_description: "os-workplace is the planned free desktop tier in the PointSav family — today a growing set of independent Rust and Tauri apps an operator runs on their own computer, joining the network as a station-* WireGuard peer; the intended adoption gateway to the commercial line."
cites: []
references:
  - id: 1
    text: "ISO 19005-1:2005 — Document management — Electronic document file format for long-term preservation — Part 1: Use of PDF 1.4 (PDF/A-1)."
    url: "https://www.iso.org/standard/38920.html"
---

**Correction, 2026-08-02, resolved 2026-08-06.** The original app-suite table named 11 apps; 8
did not exist in any form (`app-workplace-{wordprocessor,spreadsheet,email,browser,
communications,chat,file-manager,wiki}`), and the 3 that did exist (`app-workplace-pdf`, `-gis`,
`-bim`) were misdescribed. This correction replaces the table with the real nine-crate
`app-workplace-*` family, each row checked directly against its own source tree. It also corrects
two further claims found while re-verifying. First: the apps are Tauri applications — a Rust
backend paired with an HTML/JS/CSS WebView, targeting macOS 10.13 and later — not the "native Rust
binaries" the article previously claimed. Second: the "Reference hardware" section's Dell XPS/HP
ProBook/hardened-FreeBSD-or-seL4 framing has been removed. It contradicted every app's own stated
macOS target and does not appear anywhere in the ratified architecture
(`BRIEF-os-product-family.md` §D); `os-workplace` itself remains a one-line architectural
placeholder (`"SYSTEM EVENT: os-workplace scaffold verified."`, no other logic), not built
infrastructure behind a custom kernel. That section has been replaced with the real, ratified
deployment model below. The rest of the article is hedged to planned/intended language
accordingly.

`os-workplace` is planned as the free desktop tier in the PointSav family. What exists today is a
family of independent Rust and Tauri desktop applications — the workplace apps — that an operator
downloads and runs directly on their own computer. The `os-workplace` crate that would bind them
into one unified, branded environment is still a one-line placeholder, not built infrastructure.
The strategy behind the free tier is deliberate: an operator installs the workplace apps because
they are fast and cost nothing; once daily work happens inside the PointSav ecosystem, the
commercial [[os-orchestration|`os-orchestration`]] aggregator becomes a logical next step. This
article covers the real applications that exist today, the ratified plan for how a workplace
machine joins the network, and the strategic rationale for a free desktop tier.

## The workplace apps

The apps are Tauri desktop applications — a Rust backend paired with an HTML/JS/CSS WebView,
targeting macOS 10.13 High Sierra and later. Two of the nine crates below are pure Rust with no
WebView. Each app is independent: an operator can install one without the others, and none
require the unified `os-workplace` shell to run.

| App | State | What it does |
|---|---|---|
| `app-workplace-memo` | Active | Document editor; produces a self-contained `.html` file with fonts embedded, printing to a flawless PDF via the OS print dialogue [^1] |
| `app-workplace-presentation` | Active | Slide editor, built on the same offline-first, no-cloud design as Memo |
| `app-workplace-workbench` | Active | A thin WebView window onto the locally running `app-privategit-workbench` HTTP server; it does not itself start, stop, or manage that server |
| `app-workplace-proforma` | Active | Spreadsheet for institutional financial analysis; produces a self-contained `.json` file carrying formulas, formatting, and an audit chain |
| `app-workplace-pdf` | Scaffold-coded | PDF viewer and print tool using the `pdfium-render` crate (Google PDFium, Apache-2.0) |
| `app-workplace-gis` | Scaffold-coded | Desktop viewer for location-intelligence data; loads a MapLibre GL tile viewer against `gis.woodfinegroup.com` or a local tile server over the PPN |
| `app-workplace-bim` | Reserved-folder | Planned BIM authoring editor (Revit/AutoCAD muscle memory); a research document only today — no `Cargo.toml` or source exists yet |
| `app-workplace-aibridge` | Built, not yet registry-tracked | The AI section-edit bridge core — lets an operator hand one section of a document to an external AI session and apply only that section's result; enforces [[machine-based-auth|SYS-ADR-07]] by refusing structured schemas (proforma, GIS, BIM data) at every entry point |
| `app-workplace-http-prototype` | Built, not yet registry-tracked | An axum server exposing the workplace apps over the WireGuard PPN while native Tauri builds await a macOS build host; the Memo editor is the only surface it currently serves, the rest are listed pending |

## Deployment: joining the network

**Ratified 2026-05-23** (`DOCTRINE.md §IV.f`); implementation pending. `os-workplace` runs on the
operator's own personal computer — today, a MacBook — and is planned to deliver
`app-workplace-desktop`, the unified operator desktop surface that would bind the apps above into
one environment. It hosts [[console-os|`os-console`]] as a co-resident application, not through
Type 2 virtualization — the two are independent layers sharing the same machine. The machine joins
the [[ppn-architecture-overview|PointSav Private Network]] as a direct WireGuard peer in the
`10.42.20.0/24` range; the `node-*` instance of `os-console` it hosts inherits that membership
rather than getting a separate address. Deployment instances use the `station-*` prefix. The first
two planned are `station-workplace-jennifer-1` and `station-workplace-mathew-1`, both awaiting the
WireGuard network rollout and the `app-workplace-desktop` build. `os-workplace` does not connect
to [[totebox-orchestration|the orchestration gateway]] directly — only indirectly, through the
`os-console` instance it hosts.

## Pairing with the Totebox

`os-workplace` is the operator's local environment. Data lives in the operator's
[[totebox-os|os-totebox]]. Machine-based pairing establishes hardware-bound trust between the
workstation and the archive — see [[machine-based-auth]] for the mechanism. There are no
usernames or passwords; the pairing is the permission.

## Why a free desktop is strategic

Three reasons make `os-workplace` a structural commitment rather than a marketing gesture:

1. **Adoption funnel.** A free, fast set of desktop apps is intended to introduce the operator to
   the F-key discipline of [[console-os|`os-console`]] and the security model of the
   [[diode-standard|Diode]], so the commercial products feel familiar from day one.
2. **Reference implementation.** Every line of code written for the workplace apps is reviewable
   in the public monorepo. Customers can audit the [[compounding-substrate|substrate]] before they
   buy commercial aggregation against it.
3. **Ecosystem gravity.** A growing community of workplace-app users is intended to create an
   independent constituency of contributors, packagers, and translators that no commercial-only
   product can replicate. The [[contributor-model|contributor model]] describes the roles and
   rights for community participation.

## See also

- [[os-family-overview]] — the eight-OS family and where os-workplace fits
- [[totebox-os]] — the data partner; the archive os-workplace pairs with
- [[console-os]] — the co-resident TUI-first surface that carries os-workplace's network
  connection
- [[machine-based-auth]] — the pairing model that replaces usernames and passwords
- [[ppn-architecture-overview]] — the WireGuard network that station-* deployments join
