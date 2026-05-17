---
schema: foundry-doc-v1
title: "The six-tier sovereignty matrix"
slug: six-tier-sovereignty-matrix
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: six-tier-sovereignty-matrix.es.md
short_description: "The six-tier sovereignty matrix organises every directory in the PointSav monorepo by purpose, not by language or compile format — six fixed prefixes (app-, asset-, moonshot-, os-, service-, system-) that make the repository self-documenting and enforce dependency hygiene by convention."
cites: []
---

The PointSav monorepo organises every directory by purpose, not by programming language or compile format. Each directory at the repository root belongs to one of six tiers — `app-`, `asset-`, `moonshot-`, `os-`, `service-`, or `system-` — identified by a fixed prefix. A contributor reading the prefix knows immediately what layer a directory operates at without opening a file. This article covers the six tiers, the decision rule for classifying new directories, the kebab-case constraint that makes the taxonomy portable across operating systems and container registries, and the legacy names the taxonomy supersedes.

## The six tiers

Every directory at the monorepo root falls into one of the following tiers:

| Tier | Prefix | Purpose | Example components |
|---|---|---|---|
| 1 — Application | `app-` | User-facing surfaces — the personality cartridges that define how a job looks and feels | `app-console-input`, `app-mediakit-marketing`, `app-orchestration-command` |
| 2 — Asset | `asset-` | Non-code resources — fonts, icons, 3D models, design tokens, brand assets | `asset-brand-pointsav`, `asset-brand-wcp` |
| 3 — Moonshot | `moonshot-` | Research and development experiments not yet promoted to production | `moonshot-gpu` |
| 4 — OS | `os-` | Operating-system compositions — the runtime containers that load other components | `os-console`, `os-totebox`, `os-orchestration` |
| 5 — Service | `service-` | Background business-logic daemons | `service-slm`, `service-content`, `service-email`, `service-people` |
| 6 — System | `system-` | Foundational technology — drivers, networking, foundation utilities | `system-foundation`, `system-driver-network`, `system-audit` |

The word "library" is explicitly retired as a category label. It describes how code is compiled, not what it does.

## The rule of purpose

A new directory is classified by its purpose, not its format. The decision is short:

| Question | Tier |
|---|---|
| Does it talk to the computer — date parsing, networking, math, filesystem? | `system-*` |
| Does it talk to the user's life — contacts, email, photos, accounting? | `service-*` |
| Does it define the look and feel for a specific job? | `app-*` |
| Is it a non-code resource — a font, an icon, a design token? | `asset-*` |
| Is it speculative research not yet committed to production? | `moonshot-*` |
| Does it compose other components into a runtime container? | `os-*` |

## Why the prefix discipline scales

Three structural advantages emerge from the taxonomy:

| Advantage | Effect |
|---|---|
| Discoverability | A new contributor reading a directory name knows immediately what layer it operates at without opening a file |
| Dependency hygiene | `app-*` may depend on `service-*` and `system-*`; `service-*` may depend on `system-*`; `system-*` has no upward dependencies — cyclic dependencies are mechanically impossible |
| Composition over inheritance | An operating system is an `os-*` composition that loads `app-*` cartridges and connects to `service-*` daemons; the OS contains no feature-specific code |

This is the filesystem-level expression of composition over inheritance: the OS is a generic engine; the application is the personality.

## Strict kebab-case

All six tiers use lowercase ASCII with hyphens. Capital letters are not permitted. The constraint holds across Docker registries, case-sensitive Linux filesystems, case-insensitive macOS filesystems, and DNS subdomains.

| Form | Status | Reason |
|---|---|---|
| `os-totebox` | Canonical | Lowercase kebab-case |
| `Totebox-OS` | Not permitted | Mixed case creates phantom drift across operating systems |
| `Totebox_OS` | Not permitted | Underscores are not standard in repository or container names |
| `toteboxos` | Not permitted | Loses readability without a delimiter |

Uppercase is preserved only for a small set of root-level operational files — `README`, `LICENSE`, `CLAUDE.md`, `AGENT.md` — where the convention predates the kebab-case rule.

## Name supersession

The taxonomy took several generations to settle. Earlier names appear throughout the source archive and are normalised when content is migrated:

| Earlier name | Current canonical |
|---|---|
| `lib-pointsav-*` | `package-*` (shared libraries) |
| `software-pdfs`, `software-wordprocessing` | `app-workplace-pdfs`, `app-workplace-wordprocessor` |
| `console-people`, `node-console-people` | `app-console-people` |
| `sys-marketing`, `sys-knowledge`, `sys-distro` | `app-mediakit-marketing`, `app-mediakit-knowledge`, `app-mediakit-distribution` |
| `fleet-infrastructure-*`, `gateway-interface-*`, `route-network-admin` | `app-infrastructure-onprem` / `-leased` / `-cloud`, `app-orchestration-command`, `app-network-admin` |

## See also

- [[os-family-overview]] — the eight operating systems composed using the `os-*` tier
- [[three-layer-architecture]] — the three-layer arrangement of vendor, customer, and operator that the monorepo sits within
- [[five-stage-supply-chain]] — how the monorepo's verified commits reach production deployments
