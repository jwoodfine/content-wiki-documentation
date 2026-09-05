---
schema: foundry-doc-v1
type: topic
content_type: topic
index_group: network-control-and-infrastructure
slug: os-privategit
short_description: "The OS layer hosting the private Git infrastructure underpinning the development workspace, staging-tier commit flow, and canonical repos for PointSav engineering."
title: "Private git OS"
category: systems
language: en
paired_with: os-privategit.es.md
status: stub
last_edited: 2026-08-22
editor: pointsav-engineering
---

`os-privategit` is the operating system layer that runs the platform's sovereign version-control infrastructure — private Git repositories and [[design-system-substrate|design-system]] hosting — on hardware the operator owns, without routing source code through a third-party Git hosting provider. The OS binary itself is a thin license-check gate; the Git-hosting and design-system logic lives in the sibling `app-privategit-*` applications it hosts (`app-privategit-source`, `app-privategit-design`, `app-privategit-marketplace`, `app-privategit-workbench`), following the same OS/app split as the rest of the family. It belongs to the [[os-family-overview|eight-OS family]] and pairs with the [[app-privategit-workbench|browser workbench]] for file authoring and review.

The [[os-workplace|os-workplace]] desktop environment and the [[totebox-os|Totebox]] archive are the primary consumers of the software hosted on `os-privategit`. Source code flows from `os-privategit` into the [[customer-first-ordering|customer-first]] deployment model.

## Current build and deployment status

Unlike a general-purpose "list of apps" summary, each of the four hosted applications has its own
confirmed build state rather than a single, uniform description:

| Application | Version | Status | What it does |
|---|---|---|---|
| `app-privategit-source` | v0.1.0 | Active | Binary release server with Ed25519 license-token verification |
| `app-privategit-marketplace` | v0.1.0 | Active | Software storefront — product catalog, license issuance, payment verification |
| `app-privategit-workbench` | v0.0.1 | Active | The browser-based three-column file editor (tree / viewer / editor) referenced above |
| `app-privategit-design` | v0.3.0 | Unconfirmed | A substantial codebase exists on disk; the crate's own README self-describes it as an early architectural scaffold pending a dedicated engineering cycle — the two signals conflict and are not reconciled here |

`app-privategit-source` and `app-privategit-marketplace` are both deployed and active on the
`vault-privategit-source-1` host today. `app-privategit-workbench` is active as the file-editing
surface described above. `app-privategit-design`'s actual state could not be confirmed one way or
the other from available sources at the time of writing — it is named here rather than silently
omitted, with its status flagged as unconfirmed rather than asserted.

## See also

- [[app-privategit-workbench]] — the browser-based file editor running on os-privategit
- [[os-family-overview]] — the eight-OS family and where os-privategit fits
- [[machine-based-auth]] — the authorization model governing access to private repositories
- [[deployment-patterns]] — how os-privategit appears in canonical fleet configurations
