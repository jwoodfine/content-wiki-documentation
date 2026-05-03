---
schema: foundry-doc-v1
title: "Citation Graph as Substrate"
slug: citation-substrate
category: reference
type: topic
quality: published
short_description: How PointSav builds a machine-readable citation graph into every doctrine clause, convention, and published document as a first-class substrate element.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: citation-substrate.es.md
---

A knowledge platform that publishes claims about technology, governance, and business outcomes is only as trustworthy as the sources those claims rest on. The citation substrate makes source traceability a structural property of the platform rather than an editorial afterthought — every document declares its citation dependencies in machine-readable frontmatter, every inline reference resolves against a central registry, and a verification mechanism keeps the registry current as sources change.

## The central registry

A workspace-level citation registry is the canonical resolver for all citations across the platform. It uses CFF-flavored YAML and assigns a stable identifier to each entry. A representative entry carries: the citation type (regulatory instrument, research paper, technical specification, vendor documentation), the authoritative title, a stable URL, the date of last verification, a content hash for drift detection, an evidence class, and any recognized aliases.

The stable identifier — for example, `ni-51-102` for National Instrument 51-102 — is the handle every document uses. Citing the ID rather than a raw URL means the URL can change in the registry without breaking every document that references it.

## Per-document frontmatter

Every doctrine clause, convention, README, and public-facing document declares its citation dependencies:

```yaml
cites:
  - ni-51-102
  - osc-sn-51-721
```

The IDs resolve against the registry. Tooling can validate that every declared ID exists in the registry, auto-generate a References section at the bottom of each document, and build a reverse index showing which documents cite each source.

## Inline reference syntax

Inline references use the citation ID in square brackets: `[ni-51-102]`. Where a specific clause or section is relevant, a section reference appends: `[ni-51-102 §4A.2]`. Tooling renders the bracketed form as a hyperlink to the source URL via the registry. Until the rendering tooling is deployed, the brackets are legible to human readers as registry-resolvable references.

## Three provenance classes

Every assertion in the corpus carries one of three provenance classes:

**Primary.** An original observation — a measurement, an operator interaction, an inbox message at the time of authorship. Primary assertions are immutable: they are never edited, and supersedence happens by addition rather than revision.

**Derived.** Reasoning over primary or other derived assertions — a doctrine clause, a synthesis, a runbook. Derived assertions are versioned: supersedence is tracked through document versioning and commit history.

**Cited.** An external authority — a regulatory instrument, a published paper, a vendor specification. Cited assertions undergo periodic content-hash verification; substantive content changes at the source are logged as material changes.

The `evidence_class` field on registry entries and training corpus records makes the provenance class explicit and machine-filterable.

## Self-healing custodianship

When the platform's local inference capability is operational, it is intended to run nightly knowledge-hygiene passes against the citation graph. The planned pass operations include: verifying each registry URL by fetching and comparing a content hash, flagging mismatches and 404 responses for review; validating that every `cites:` entry across the corpus resolves in the registry; building and persisting a reverse index of what cites what; detecting pairs of documents that cite the same authority but make divergent claims; and surfacing documents whose cited authorities have changed since the document's last update.

These passes are intended to be suggestions, not automated fixes. The inference layer surfaces the finding; a human principal decides whether and how to act.

## The seeding principle

The registry is seeded with references that already exist in current doctrine and conventions. Going forward, every new citation in any document is added to the registry as part of the same commit that introduces the inline reference. The registry grows alongside the prose; the hygiene pass keeps it consistent. A post-commit hook can validate that every new bracketed reference has a corresponding registry entry.

## Connection to the disclosure posture

The citation substrate is the operational form of one element of the BCSC continuous-disclosure posture [ni-51-102]: citations are committed alongside the prose they support, machine-readable, and audit-traceable. A regulator or auditor can follow the citation chain from a published claim to its source without relying on the publishing organization's characterization of what the source says.

## See also

- [[bcsc-disclosure-posture]] — the disclosure discipline this substrate operationalizes
- [[draft-research-trail-discipline]] — how draft-time research feeds the citation registry
- [[cluster-wiki-draft-pipeline]] — the editorial pipeline where citations are resolved at refinement time

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/citation-substrate.md` (ratified 2026-04-26). Self-referential: this TOPIC is itself subject to the citation discipline it describes, and its `cites:` frontmatter demonstrates the practice. Forward-looking statements (nightly hygiene passes, tooling auto-generation) carry intended/planned framing per [ni-51-102].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
