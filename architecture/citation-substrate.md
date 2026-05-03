---
schema: foundry-doc-v1
title: "The Citation Substrate"
slug: citation-substrate
category: architecture
type: topic
quality: complete
short_description: "The Citation Substrate is the Foundry mechanism that connects every written artifact to the external authorities it depends on through a workspace-wide YAML registry, per-document frontmatter cites fields, and inline reference syntax that makes provenance machine-auditable."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - cff-spec
  - cff-github
  - turing-way-cff
  - knowledge-commons-wiki
  - opentimestamps
paired_with: citation-substrate.es.md
---

# The Citation Substrate

> The Citation Substrate is the Foundry mechanism that connects every written artifact to the external authorities it depends on through a workspace-wide YAML registry, per-document frontmatter cites fields, and inline reference syntax that makes provenance machine-auditable.

Every doctrine clause, convention, and public-facing document in the Foundry workspace declares its citation dependencies in YAML frontmatter. Those IDs resolve against a single workspace-wide registry at `~/Foundry/citations.yaml`. **The Citation Substrate** is not a bibliography tool — it is a machine-readable provenance graph that runs from a regulatory instrument through a doctrine clause through a public article, auditable at each step. The discipline supports the BCSC continuous-disclosure posture: citations are part of the substrate, machine-readable, and audit-traceable.

## Overview

Three components work together to constitute the Citation Substrate:

1. **The registry** (`~/Foundry/citations.yaml`). A CFF-flavored YAML file `[cff-spec]` `[cff-github]` `[turing-way-cff]` that holds one entry per citation ID. Each entry carries the citation's type, jurisdiction (for regulatory items), authoritative title, stable URL, date of most recent verification, a content-hash field for drift detection, an evidence class, and any aliases that might appear in prose. As of 2026-04-27 the registry holds 62 entries covering regulatory instruments, research papers, technical specifications, vendor documents, and open standards.

2. **Per-document frontmatter**. A `cites:` field in the YAML frontmatter of every doctrine clause, convention, and article:

   ```yaml
   ---
   schema: foundry-doc-v1
   document_version: 0.0.2
   cites:
     - ni-51-102
     - osc-sn-51-721
   ---
   ```

   The IDs in `cites:` are resolvable against the registry. Tooling can validate that every declared ID exists, auto-generate a References section, and build a `cited_by:` reverse index.

3. **Inline reference syntax**. Body prose references a citation with its ID in square brackets: `[ni-51-102]`. Clause-specific references append the section: `[ni-51-102 §4A.2]`. Until rendering tooling is wired into `app-mediakit-knowledge`, the brackets are human-readable cues that a registry-resolvable reference is present.

## Ring and Role

The Citation Substrate has no ring-layer assignment — it operates at the workspace documentation layer, above and across all three rings. Every document produced by any session at any layer that makes an externally-grounded claim must carry the appropriate `cites:` frontmatter. The nightly hygiene pass that monitors registry health runs as a service-slm (Ring 3) job; the registry itself is a workspace-layer file.

## Architecture

### How the registry works

The registry entry schema makes provenance explicit at each step. A regulatory citation for `[ni-51-102]` carries `evidence_class: regulatory-primary` — a machine-filterable signal that this entry is primary authority, not secondary commentary. A research paper carries `evidence_class: technical-primary` or `research-derived` depending on whether it is an original contribution or a synthesis. A vendor document carries `evidence_class: cited-secondary`.

The `content_hash` field is the self-healing mechanism. When service-slm runs its nightly hygiene pass, it fetches each URL, computes a SHA-256 of the page content, and compares against the stored hash. A match updates the `last_verified` date. A mismatch is flagged as a material change candidate and surfaced to the Master inbox with the diff. A 404 is flagged as link rot alongside candidate-replacement search results.

Until service-slm is operational, Master Claude performs a manual review of the registry monthly.

Adding a new citation follows the seeding principle: the registry entry and the inline reference land in the same commit. An orphaned inline reference — one whose ID does not resolve in the registry — is a defect, not a convention.

### Why per-claim citation discipline matters

Three reasons drive the discipline, not one.

**Regulatory traceability.** Per `[ni-51-102]` and `[osc-sn-51-721]`, forward-looking information in public-facing content must carry cautionary language, a stated basis, and material assumptions. The citation graph makes "stated basis" machine-auditable: a reviewer can walk from a public-facing claim back through the doctrine clause that asserts it to the regulatory instrument or research paper that grounds it. Without per-claim citations, the walk is manual and incomplete.

**Drift prevention.** The corpus grows across sessions, contributors, and years. Two documents citing the same authority can make divergent claims about what it says — the Knowledge Provenance Pillar (Doctrine claim #27) identifies this as the primary failure mode of large knowledge corpora. The nightly SLM hygiene pass's drift-detection step finds exactly these divergent-claim pairs and surfaces them as review items before they propagate into training data or public publication.

**Public-knowledge compounding.** Per `[knowledge-commons-wiki]`, the content-wiki repos are the public leg of the Compounding Substrate. Cited content carries its provenance into any export, mirror, or derivative corpus. A reader or machine consumer does not need to trust the platform's own claims — they can follow the citation to the primary source.

## Configuration

The Citation Substrate currently requires manual discipline — registry entry and inline reference in the same commit, monthly Master review. Per `[ni-51-102]` continuous-disclosure language, the following items are planned infrastructure:

- A workspace-tier post-commit hook that validates every new `[id]` inline reference resolves in the registry. Implementation targeted at `v0.1.0`.
- Auto-generation of a References section at the bottom of each article from the `cites:` frontmatter plus the registry — to be wired into `app-mediakit-knowledge` as a renderer stage.
- A `cited_by:` reverse index persisted as `~/Foundry/data/citation-graph.json` (local-only, rebuilt on demand by the SLM hygiene pass).
- Nightly hygiene passes by service-slm covering citation verification, forward-citation validation, reverse index build, drift detection, stale-topic surfacing, and citation suggestions — all as suggestions to Master, not automated fixes.
- Export of citation graph data as part of the `[knowledge-commons-wiki]` public-knowledge publication pattern.

Until each lands, the manual discipline is the operational form.

## See Also

- [[compounding-substrate]]
- [[language-protocol-substrate]]
- [[decode-time-constraints]]
- [[disclosure-substrate]]

## References

- `~/Foundry/conventions/citation-substrate.md` — the convention this article reflects
- `~/Foundry/citations.yaml` — the registry
- `~/Foundry/conventions/bcsc-disclosure-posture.md` — the BCSC disclosure posture that motivates this discipline
- DOCTRINE.md Claim #25 — Citation Substrate
- `[cff-spec]` — Citation File Format specification
- `[cff-github]` — GitHub CFF support
- `[turing-way-cff]` — The Turing Way on citation practice
- `[knowledge-commons-wiki]` — Knowledge commons and public-knowledge compounding
- `[opentimestamps]` — OpenTimestamps anchoring (planned integration)
- `[ni-51-102]` — NI 51-102 Continuous Disclosure Obligations
- `[osc-sn-51-721]` — OSC Staff Notice 51-721 Forward-Looking Information Disclosure
