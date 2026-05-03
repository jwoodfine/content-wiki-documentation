---
schema: foundry-doc-v1
title: "Cluster Wiki Draft Pipeline"
slug: cluster-wiki-draft-pipeline
category: reference
type: topic
quality: published
short_description: The workspace pipeline that routes editorial drafts from all contributor layers through an editorial gateway into published documentation, wiki topics, deployment runbooks, and governance documents.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: cluster-wiki-draft-pipeline.es.md
---

A software platform that publishes continuously — to a documentation wiki, to deployment runbooks, to governance documents, to contributor identity pages — cannot treat each publication as an ad hoc authoring event. The cluster wiki draft pipeline is the structured mechanism that collects editorial drafts from across the platform, applies a consistent editorial pass, and routes the refined output to the appropriate published surface.

The pipeline operationalizes the Reverse-Funnel Editorial Pattern: the substrate generates structural drafts; an editorial gateway refines them to register; Creative Contributors edit the published version at the end of the cycle, and those edits become new training material for the platform's local inference capability.

## Three input ports

Editorial drafts originate from three layers of the contributor model:

**Cluster-level drafts** are the highest-velocity input. A development cluster working on a specific feature or milestone produces drafts explaining what it built, how to operate the resulting deployment, and what the architectural decisions were. These drafts reflect detailed technical knowledge but may not conform to the publication register.

**Repository-level drafts** come from contributors working at the repository layer — per-repository README updates, architecture topics that span multiple projects within a single codebase, documentation that describes the repository's own conventions.

**Workspace-level drafts** originate at the platform's governance layer and cover cross-cluster topics, governance documents, license text, contributor identity pages, and workspace conventions. These are lower velocity but higher governance weight.

All three ports feed into the same editorial gateway. The gateway cares about the draft's frontmatter — specifically the `language_protocol` field, the `audience` field, and the `bcsc_class` field — not about which layer produced it.

## What the editorial gateway applies

The editorial gateway applies four disciplines to every draft:

**Register discipline.** The raw draft may be technically accurate but conversationally written, repetitive, or heavy with jargon. The gateway produces output in Bloomberg-grade register — precise, economical, readable by a financially literate non-specialist. A list of prohibited vocabulary is applied during refinement; banned terms cannot appear in published output.

**Disclosure discipline.** The draft's `bcsc_class` field determines which disclosure rules apply. Drafts marked as `forward-looking` receive planned/intended/may language, cautionary framing, a stated reasonable basis, and named material assumptions before publication. Drafts marked `current-fact` require stable tense and verified citations.

**Citation resolution.** Inline URL references in the raw draft are resolved to stable citation IDs from the registry. The refined output carries `cites:` frontmatter and bracketed inline references rather than raw URLs.

**Bilingual generation.** Published wiki topics and README files are produced as bilingual pairs. The Spanish version follows a strategic-adaptation pattern: it provides an overview that reflects the document's strategic intent rather than a word-for-word translation.

## Editorial surfaces and their velocity

The pipeline serves multiple publication surfaces at different cadences:

- Documentation wiki topics are the highest-velocity surface, swept at every editorial session.
- Deployment runbooks are produced when a deployment reaches a stable operational state.
- Per-project README files are produced when a project is activated or reaches a significant state change.
- Repository README files are produced at major version milestones or quarterly.
- Contributor identity pages are produced at quarterly intervals or at public-launch milestones.
- Governance documents — license text, contributor license agreements, policy documents — are produced when governance decisions are made.

## Frontmatter schema

Every draft carries `foundry-draft-v1` frontmatter with fields for: state (pending, in-refinement, refined, archived), originating cluster, target repository and path, audience, disclosure class, language protocol, authoring metadata, and notes for the editorial gateway. Research-trail fields are also mandatory: `research_done_count`, `research_suggested_count`, `open_questions_count`, `research_provenance`, and `research_inline`. The gateway reads the research trail before composing the refinement, consults suggested sources where scope allows, and preserves the trail as a Provenance footer in the refined output.

## Apprenticeship corpus

Every editorial transition emits a structured event to the apprenticeship corpus. A `draft-created` event records the raw bulk draft; a `draft-refined` event records the (raw, refined) pair as a preference learning example; a `creative-edited` event records the (refined, creative-edited) pair as a Stage-2 craft preference example. These pairs accumulate as training material for the platform's local inference capability — the model learns to produce publication-register output from technical bulk input, and then learns to produce Creative-voice output from the refined baseline.

## Layer discipline

Each layer writes drafts only within its own scope. The gateway reads drafts from all three input ports — reading across layers is unrestricted. The destination repository commits the refined output — that commit is made at the repository layer. No layer writes to another layer's scope directly; the pipeline uses the passive outbox mechanism for cross-repo handoffs.

## See also

- [[cluster-design-draft-pipeline]] — the structural counterpart for design-system contributions
- [[draft-research-trail-discipline]] — research-trail requirements that apply to every draft
- [[bcsc-disclosure-posture]] — the disclosure rules the gateway applies at refinement time
- [[citation-substrate]] — the citation registry the gateway resolves against

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/cluster-wiki-draft-pipeline.md` (ratified 2026-04-27). Forward-looking statements (grammar-constrained AI refinement at scale, automated bilingual generation) carry intended/planned framing per [ni-51-102].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
