---
schema: foundry-doc-v1
title: "The citation substrate"
slug: citation-substrate
category: substrate
type: topic
quality: complete
short_description: "The citation system connects every published article to the external authorities it depends on — regulatory instruments, research papers, technical specifications — through a platform-wide YAML registry with drift detection and per-document frontmatter declarations that make provenance machine-auditable from regulatory instrument to published claim."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
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

Every article in this documentation that makes an externally-grounded claim carries a `cites:` declaration in its front-matter listing the regulatory instruments, research papers, or technical specifications the claim depends on. Those IDs resolve against a single platform-wide YAML registry. The result is a provenance graph rather than a bibliography — a structure that runs from a published claim back to its primary source, traversable by a machine or a reviewer without access to internal systems.

As of 2026-04-27, the registry holds 62 entries covering regulatory instruments (NI 51-102, SEC Rule 17a-4(f), eIDAS), research papers, technical specifications, vendor documents, and open standards. Every `[ni-51-102]` reference in a published article traces to the same canonical registry entry, with type, jurisdiction, stable URL, and a SHA-256 content hash for drift detection.

Three components work together: a central registry holding one entry per citation ID; per-document `cites:` front-matter that makes dependencies machine-readable; and inline `[id]` syntax in body prose that marks each reference with its registry-resolvable ID. A nightly automated pass fetches each registered URL, verifies the content hash, and surfaces material changes or link rot for human review before they propagate into published content or training data.

For regulated buyers, this means every claim about compliance properties — record immutability, AI audit trails, data residency — carries a traceable stated basis. A compliance officer auditing documentation about SEC Rule 17a-4(f) can follow the citation to the primary regulatory instrument without accessing internal systems. This satisfies the "stated basis" requirement under `[ni-51-102]` and `[osc-sn-51-721]` for forward-looking information in public-facing content.

## Overview

Three components constitute the Citation Substrate:

1. **The registry** (`citations.yaml`). A CFF-flavored YAML file `[cff-spec]` `[cff-github]` `[turing-way-cff]` that holds one entry per citation ID. Each entry carries the citation's type, jurisdiction (for regulatory items), authoritative title, stable URL, date of most recent verification, a content-hash field for drift detection, an evidence class, and any aliases that might appear in prose. As of 2026-04-27 the registry holds 62 entries covering regulatory instruments, research papers, technical specifications, vendor documents, and open standards.

2. **Per-document frontmatter**. A `cites:` field in the YAML frontmatter of every published article and specification document:

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

The Citation Substrate has no ring-layer assignment — it operates at the documentation layer, independent of the platform's three service rings. Every published document that makes an externally-grounded claim must carry the appropriate `cites:` frontmatter. The nightly hygiene pass that monitors registry health runs as a [[service-slm]] (Ring 3) job; the registry itself is a documentation-layer file.

## Architecture

### How the registry works

The registry entry schema makes provenance explicit at each step. A regulatory citation for `[ni-51-102]` carries `evidence_class: regulatory-primary` — a machine-filterable signal that this entry is primary authority, not secondary commentary. A research paper carries `evidence_class: technical-primary` or `research-derived` depending on whether it is an original contribution or a synthesis. A vendor document carries `evidence_class: cited-secondary`.

The `content_hash` field is the self-healing mechanism. When service-slm runs its nightly hygiene pass, it fetches each URL, computes a SHA-256 of the page content, and compares against the stored hash. A match updates the `last_verified` date. A mismatch is flagged as a material change candidate and surfaced for human review with the diff. A 404 is flagged as link rot alongside candidate-replacement search results.

Until [[service-slm]] is operational, the platform maintainer performs a manual review of the registry monthly.

Adding a new citation follows the seeding principle: the registry entry and the inline reference land in the same commit. An orphaned inline reference — one whose ID does not resolve in the registry — is a defect.

### Why per-claim citation discipline matters

Three reasons drive the discipline, not one.

**Regulatory traceability.** Per `[ni-51-102]` and `[osc-sn-51-721]`, forward-looking information in public-facing content must carry cautionary language, a stated basis, and material assumptions. The citation graph makes "stated basis" machine-auditable: a reviewer can walk from a public-facing claim back to the regulatory instrument or research paper that grounds it. Without per-claim citations, the walk is manual and incomplete.

**Drift prevention.** The corpus grows across sessions, contributors, and years. Two documents citing the same authority can make divergent claims about what it says — divergent-claim pairs on primary sources are the primary failure mode of large knowledge corpora. The nightly hygiene pass's drift-detection step finds exactly these pairs and surfaces them as review items before they propagate into training data or public publication.

**Public-knowledge compounding.** Per `[knowledge-commons-wiki]`, the content-wiki repos are the public leg of the [[compounding-substrate]]. Cited content carries its provenance into any export, mirror, or derivative corpus. A reader or machine consumer does not need to trust the platform's own claims — they can follow the citation to the primary source.

## Configuration

The Citation Substrate currently requires manual discipline — registry entry and inline reference in the same commit, monthly maintainer review. Per `[ni-51-102]` continuous-disclosure language, the following items are planned infrastructure:

- A post-commit hook that validates every new `[id]` inline reference resolves in the registry. Implementation targeted at `v0.1.0`.
- Auto-generation of a References section at the bottom of each article from the `cites:` frontmatter plus the registry — to be wired into `app-mediakit-knowledge` as a renderer stage.
- A `cited_by:` reverse index persisted as a local data file (rebuilt on demand by the SLM hygiene pass).
- Nightly hygiene passes by [[service-slm]] covering citation verification, forward-citation validation, reverse index build, drift detection, stale-topic surfacing, and citation suggestions — all as suggestions to the platform maintainer, not automated fixes.
- Export of citation graph data as part of the `[knowledge-commons-wiki]` public-knowledge publication pattern.

Until each lands, the manual discipline is the operational form.

## See also

- [[compounding-substrate]]
- [[language-protocol-substrate]]
- [[decode-time-constraints]]
- [[disclosure-substrate]]
