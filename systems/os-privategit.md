---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-privategit
short_description: "The operating system layer hosting the private Git infrastructure that underpins the development workspace, staging-tier commit flow, and canonical source repositories for all PointSav engineering repos."
title: "Private Git OS"
category: systems
language: en
paired_with: os-privategit.es.md
status: stub
last_edited: 2026-05-25
editor: pointsav-engineering
---

`os-privategit` is the operating system layer that hosts the platform's sovereign version-control infrastructure — private Git repositories and [[design-system-substrate|design-system]] hosting — on hardware the operator owns, without routing source code through a third-party Git hosting provider. It belongs to the [[os-family-overview|eight-OS family]] and pairs with the [[os-privategit-workbench|browser workbench]] for file authoring and review.

The [[os-workplace|os-workplace]] desktop environment and the [[totebox-os|Totebox]] archive are the primary consumers of the software hosted on `os-privategit`. Source code flows from `os-privategit` into the [[customer-first-ordering|customer-first]] deployment model.

## See also

- [[os-privategit-workbench]] — the browser-based file editor running on os-privategit
- [[os-family-overview]] — the eight-OS family and where os-privategit fits
- [[machine-based-auth]] — the authorization model governing access to private repositories
- [[deployment-patterns]] — how os-privategit appears in canonical fleet configurations
