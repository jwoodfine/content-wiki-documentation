---
schema: foundry-doc-v1
title: "BCSC Continuous-Disclosure Posture"
slug: bcsc-disclosure-posture
category: reference
type: topic
quality: published
short_description: The operating discipline that treats every published artifact as potentially reviewable under Canadian securities continuous-disclosure obligations.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: bcsc-disclosure-posture.es.md
---

Every artifact published to a public repository — documentation, release notes, README files, changelog entries, wiki topics — is treated as potentially reviewable under Canadian securities continuous-disclosure obligations, regardless of whether any affiliated entity is currently a reporting issuer. Operating this discipline at all times means no retrofit is required if reporting status changes.

This TOPIC describes the five operating rules, how they manifest in published content, and why the compliance takes the form of practice rather than declaration.

## Why operate this discipline preemptively

National Instrument 51-102 Continuous Disclosure Obligations [ni-51-102] and OSC Staff Notice 51-721 Forward-Looking Information Disclosure [osc-sn-51-721] define obligations for Canadian reporting issuers. A software platform that publishes substantive claims about future capability, commercial outcomes, and governance arrangements creates a disclosure record whether or not the publishing entity is currently subject to securities law. Building the practice into daily operations is materially cheaper than retrofitting it at the point of a material corporate event.

## The five operating rules

### Rule 1 — Forward-looking information is labelled

Any statement about future capability, planned timeline, intended customer outcome, or governance arrangement carries:

- Identification as forward-looking ("planned", "intended", "may", "expected to", "subject to")
- A stated reasonable basis (research, working prototype, ratified document, signed commit)
- Cautionary language ("actual results may vary", "subject to operational reality", "subject to ratification")
- Named material assumptions on which the statement depends

Per [osc-sn-51-721], forward-looking information must have a reasonable basis, its underlying assumptions must be reasonable, and the preparation and review process should be documented.

### Rule 2 — Third-party governance and equity claims are documented before naming

A party is named as holding a governance position only when that position is documented and current. This rule prevents aspirational claims about future governance relationships from appearing as present-tense facts in published material.

### Rule 3 — Material changes are surfaced through the version record

Significant doctrinal changes, adapter version releases, and any change that could be material to a reporting issuer are committed with date-stamped, signed commits and changelog entries suitable for legal review. The versioning discipline — one changelog line per patch, one section per minor release, one chapter per major release — ensures no information is lost in squashes. A regulator reviewing the commit history can reconstruct what changed, when, and why.

### Rule 4 — Publication to a public repository is public disclosure

Anything pushed to a public repository is treated as published material at the moment of the push. Internal-only state stays in workspace files, local mailboxes, and deployment instances that are not tracked in any public repository.

### Rule 5 — Compliance is the practice, not the declaration

Copy describing the disclosure rule does not belong in READMEs, release notes, or announcement copy. Naming the rule in product copy creates a fresh attestation surface that itself becomes reviewable. The compliance is visible in how artifacts are written, not in assertions about how they are written.

## What correct and incorrect framing looks like

A capability statement claiming that the platform matches a named commercial service's performance on enterprise tasks is non-compliant. A statement that when a named milestone is reached, a capability is planned to be available under a service contract, with actual outcomes subject to corpus volume, training compute, and operational reality, is compliant.

A timeline statement announcing a specific deployment in a named quarter with no qualification is non-compliant. A statement that a deployment is planned for a named version milestone, subject to operator capacity and listed prerequisites, is compliant.

A governance statement naming a third party as providing oversight when that role is not yet formally established is non-compliant. A statement that the third party's role in the planned governance pattern is to be determined and documented prior to activation is compliant.

## Scope of application

The posture applies to all published Markdown files, all commit messages on branches that may be pushed to public repositories, all README files, all TOPIC files in documentation wikis, all deployment runbooks, and any code comments or documentation strings that may be visible at runtime.

## Citations are part of the practice

A sixth element of this posture — introduced alongside a citation substrate convention — requires every doctrine clause, convention, and public-facing document to declare its citation dependencies in structured frontmatter. Inline regulatory references use stable identifiers resolvable against a workspace citation registry. This makes the regulatory grounding of every claim machine-readable and auditable, not just human-readable.

## See also

- [[citation-substrate]] — the citation graph that makes regulatory grounding machine-readable
- [[draft-research-trail-discipline]] — how forward-looking research items are scrubbed at refinement time
- [[cluster-wiki-draft-pipeline]] — the editorial pipeline where this posture is applied uniformly

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/bcsc-disclosure-posture.md` (ratified 2026-04-26). Regulatory basis: [ni-51-102], [osc-sn-51-721]. This TOPIC is itself subject to the disclosure posture it describes.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
