---
schema: foundry-doc-v1
title: "The Citation Substrate"
slug: topic-citation-substrate
category: architecture
status: pre-build
last_edited: 2026-04-28
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - cff-spec
  - cff-github
  - turing-way-cff
  - knowledge-commons-wiki
  - opentimestamps
---

Every doctrine clause, convention, and public-facing document in
the Foundry workspace declares its citation dependencies in YAML
frontmatter. Those IDs resolve against a single workspace-wide
registry at `~/Foundry/citations.yaml`. The discipline is not
a bibliography tool — it is a machine-readable provenance graph
that runs from a regulatory instrument through a doctrine clause
through a public article, auditable at each step.

## Definition

The Citation Substrate is the workspace mechanism that connects
every written artifact to the external authorities it depends on.
Three components work together:

1. **The registry** (`~/Foundry/citations.yaml`). A CFF-flavored
   YAML file `[cff-spec]` `[cff-github]` `[turing-way-cff]` that
   holds one entry per citation ID. Each entry carries the
   citation's type, jurisdiction (for regulatory items),
   authoritative title, stable URL, date of most recent
   verification, a content-hash field for drift detection, an
   evidence class, and any aliases that might appear in prose. As
   of 2026-04-27 the registry holds 62 entries covering regulatory
   instruments, research papers, technical specifications, vendor
   documents, and open standards.

2. **Per-document frontmatter**. A `cites:` field in the YAML
   frontmatter of every doctrine clause, convention, and article:

   ```yaml
   ---
   schema: foundry-doc-v1
   document_version: 0.0.2
   cites:
     - ni-51-102
     - osc-sn-51-721
   ---
   ```

   The IDs in `cites:` are resolvable against the registry.
   Tooling can validate that every declared ID exists, auto-generate
   a References section, and build a `cited_by:` reverse index.

3. **Inline reference syntax**. Body prose references a citation
   with its ID in square brackets: `[ni-51-102]`. Clause-specific
   references append the section: `[ni-51-102 §4A.2]`. Until
   rendering tooling is wired into `app-mediakit-knowledge`, the
   brackets are human-readable cues that a registry-resolvable
   reference is present.

## How the registry works

The registry entry schema makes provenance explicit at each step.
A regulatory citation for `[ni-51-102]` carries
`evidence_class: regulatory-primary` — a machine-filterable signal
that this entry is primary authority, not secondary commentary.
A research paper carries `evidence_class: technical-primary` or
`research-derived` depending on whether it is an original
contribution or a synthesis. A vendor document carries
`evidence_class: cited-secondary`.

The `content_hash` field is the self-healing mechanism. When
service-SLM runs its nightly hygiene pass, it fetches each URL,
computes a SHA-256 of the page content, and compares against the
stored hash. A match updates the `last_verified` date. A mismatch
is flagged as a material change candidate and surfaced to the
Master inbox with the diff. A 404 is flagged as link rot alongside
candidate-replacement search results.

Until service-SLM is operational, Master Claude performs a manual
review of the registry monthly.

Adding a new citation follows the seeding principle: the registry
entry and the inline reference land in the same commit. An
orphaned inline reference — one whose ID does not resolve in the
registry — is a defect, not a convention.

## Why per-claim citation discipline matters

Three reasons drive the discipline, not one.

**Regulatory traceability.** Per `[ni-51-102]` and `[osc-sn-51-721]`,
forward-looking information in public-facing content must carry
cautionary language, a stated basis, and material assumptions.
The citation graph makes "stated basis" machine-auditable: a
reviewer can walk from a public-facing claim back through the
doctrine clause that asserts it to the regulatory instrument or
research paper that grounds it. Without per-claim citations, the
walk is manual and incomplete.

**Drift prevention.** The corpus grows across sessions, contributors,
and years. Two documents citing the same authority can make
divergent claims about what it says — the Knowledge Provenance
Pillar (Doctrine claim #27) identifies this as the primary failure
mode of large knowledge corpuses. The nightly SLM hygiene pass's
drift-detection step finds exactly these divergent-claim pairs and
surfaces them as review items before they propagate into training
data or public publication.

**Public-knowledge compounding.** Per `[knowledge-commons-wiki]`,
the content-wiki repos are the public leg of the Compounding
Substrate. Cited content carries its provenance into any export,
mirror, or derivative corpus. A reader or machine consumer does
not need to trust the platform's own claims — they can follow the
citation to the primary source.

## Why hyperscaler-managed AI cannot replicate this

Three structural reasons.

**1. The graph must be local.** A citation registry that supports
content-hash drift detection, `cited_by:` reverse indexing, and
nightly hygiene passes operates on private workspace content —
draft documents, internal doctrine, session outbox messages — that
has not yet been published. Hyperscaler-managed AI operates only
on what is submitted to its API in a request; it has no persistent,
version-controlled view of the workspace corpus across sessions.
A registry that only sees published content cannot catch drift
before it publishes.

**2. The registry must grow with the corpus.** Every new citation
must land in the registry in the same commit that introduces the
inline reference. This is a workspace-level Git discipline, not a
web-search query. A hyperscaler API call can retrieve a citation's
current content but cannot maintain the registry entry, update
`last_verified`, or enforce that the inline reference and registry
entry land atomically. The workspace's commit hook (planned,
`v0.1.0+`) enforces this constraint at the Git layer.

**3. The audit trail must survive the provider.** Per the WORM
ledger design (`conventions/worm-ledger-design.md`), anchoring
citation-graph snapshots via `[opentimestamps]` or a similar
timestamp authority creates a tamper-evident record of what the
corpus said, and what it cited, at a point in time. This satisfies
the continuous-disclosure posture `[ni-51-102]` requirement that
material changes be surfaced in signed, date-stamped form. A
hyperscaler manages neither the anchor nor the date stamp — the
audit trail lives in the hyperscaler's infrastructure, not the
customer's.

## Forward-looking — pending substrate work

Per `[ni-51-102]` continuous-disclosure language, the trajectory
below is planned and intended:

- A workspace-tier post-commit hook that validates every new
  `[id]` inline reference resolves in the registry. Implementation
  targeted at `v0.1.0`.
- Auto-generation of a References section at the bottom of each
  article from the `cites:` frontmatter plus the registry — to be
  wired into `app-mediakit-knowledge` as a renderer stage.
- A `cited_by:` reverse index persisted as
  `~/Foundry/data/citation-graph.json` (local-only, rebuilt on
  demand by the SLM hygiene pass).
- Nightly hygiene passes by service-SLM covering citation
  verification, forward-citation validation, reverse index build,
  drift detection, stale-topic surfacing, and citation suggestions
  — all as suggestions to Master, not automated fixes.
- Export of citation graph data as part of the
  `[knowledge-commons-wiki]` public-knowledge publication pattern.

These items are planned infrastructure. Until each lands, the
manual discipline — registry entry and inline reference in the
same commit, monthly Master review — is the operational form.

## See also

- [The Compounding Substrate](topic-compounding-substrate.md)
- [The Language-Protocol Substrate](topic-language-protocol-substrate.md)
- [Decode-Time Constraints](topic-decode-time-constraints.md)
- The convention this article reflects:
  `~/Foundry/conventions/citation-substrate.md`
- The registry: `~/Foundry/citations.yaml`
- The BCSC disclosure posture that motivates the discipline:
  `~/Foundry/conventions/bcsc-disclosure-posture.md`
