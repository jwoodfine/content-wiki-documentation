---
schema: foundry-doc-v1
title: "Cluster Design Draft Pipeline"
slug: cluster-design-draft-pipeline
category: reference
type: topic
quality: published
short_description: The workspace pipeline that routes UI component, design research, and token-change drafts through a design-system gateway into the canonical design substrate.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: cluster-design-draft-pipeline.es.md
---

When a development cluster ships a user-facing feature, the UI components that feature introduces need to land in a canonical design substrate — not as one-off local implementations that diverge silently over time. The cluster design draft pipeline is the mechanism that routes those contributions from wherever they originate through a design-system gateway and into the substrate where they become reusable, AI-readable, and consistently maintained.

The pipeline is the structural counterpart of the cluster wiki draft pipeline. The two share the same three input ports and the same frontmatter schema; they differ in the gateway that processes them and the destination substrate they feed.

## Three input ports, one design gateway

Drafts originate from three layers:

- **Cluster-level:** a cluster working on a specific product feature drafts the UI component, design decision, or token change that feature requires.
- **Repository-level:** per-repository design contracts and cross-project patterns originate from the repository layer.
- **Workspace-level:** cross-cluster design-language decisions, brand-voice updates, and governance-driven token changes originate at the workspace level.

All three feed into the design-system gateway, which filters by the `language_protocol` field in the draft's frontmatter. Drafts with PROSE-*, COMMS-*, LEGAL-*, or TRANSLATE-* protocols belong to the editorial pipeline and are ignored here.

## Three draft families

The pipeline handles three categories of design contribution:

**DESIGN-COMPONENT.** A UI component — HTML markup, CSS variables, ARIA roles, keyboard interaction notes. The gateway verifies alignment with the IBM Carbon primitive vocabulary (the substrate's floor layer), performs WCAG 2.2 AA accessibility checks, pairs the component recipe with an AI-readable research file, and triggers an exports rebuild. Components that will be public-facing also generate a wiki TOPIC explainer, which routes through the editorial pipeline for publication.

**DESIGN-RESEARCH.** Design-decision rationale, accessibility justifications, brand-voice rules, AI-consumption hints — contributions that belong in the substrate's research backplane rather than as component code. These accumulate for Creative Designer review and form the machine-readable context AI agents consult at code-generation time.

**DESIGN-TOKEN-CHANGE.** Proposed additions or modifications to the token vocabulary stored in W3C Design Tokens Community Group format. Token changes propagate to every downstream tool — design software exports, CSS variables, style dictionary builds — so they require explicit sign-off before the gateway processes them.

## What the gateway enforces

On every DESIGN-COMPONENT draft, the gateway verifies:

- Carbon-baseline alignment: the component names the IBM Carbon primitive it derives from or extends, or carries explicit divergence rationale.
- WCAG 2.2 AA conformance: focus management, ARIA patterns, keyboard interaction, and motion preference respect.
- Research file pairing: every component lands in the substrate alongside a markdown file with structured metadata that AI agents can consume at code-generation time.
- Exports rebuild trigger: downstream tool formats update when token-dependent component CSS changes.

The gateway refuses drafts that skip accessibility considerations or that omit the required frontmatter. DESIGN-TOKEN-CHANGE drafts that lack an explicit governance sign-off are also refused — brand identity changes affect every downstream surface and require deliberate approval.

## Frontmatter schema

Every DESIGN-* draft carries `foundry-draft-v1` frontmatter, extended with `component_metadata` for component drafts. Required fields include `language_protocol`, `target_repo`, `target_path`, `bcsc_class`, `authored`, and — for DESIGN-COMPONENT — a `component_metadata` block naming the Carbon baseline component, accessibility targets, brand-voice alignment, and a one-line preview HTML snippet.

Research-trail fields are mandatory on every draft: `research_done_count`, `research_suggested_count`, `open_questions_count`, `research_provenance`, and `research_inline`. Empty counts are valid for trivial drafts; the fields themselves are required.

## Apprenticeship corpus

Every transition through the pipeline emits a structured event to the apprenticeship corpus. Three event types accumulate: `draft-created` (when the originating cluster stages the draft), `draft-refined` (when the gateway completes its pass), and `creative-edited` (when a Creative Designer edits the published recipe). The first pair forms a Stage-1 training example: the model learns design-system register, Carbon alignment, and accessibility discipline from the contrast between raw draft and refined output. The second pair forms a Stage-2 example: the model learns Creative Designer craft from the contrast between refined output and the designer's edit.

## When a cluster is required to stage a DESIGN-* draft

The pipeline is opt-in for clusters that produce no user-facing surfaces. A cluster that ships infrastructure, data ingest, or cryptographic services is not required to stage design drafts. However, any cluster that introduces a new visual element, modifies an existing substrate component for its own use, or invents a brand-voice rule or accessibility refinement must stage the appropriate draft type. Shipping a UI feature with a one-off component that never enters the substrate is a form of design drift.

## See also

- [[design-system-substrate]] — the substrate this pipeline feeds
- [[cluster-wiki-draft-pipeline]] — the structural sibling for editorial drafts
- [[draft-research-trail-discipline]] — research-trail requirements that apply to every draft in both pipelines

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/cluster-design-draft-pipeline.md` (ratified 2026-04-28). Forward-looking statements (planned service-design automation, full AI-constrained refinement) carry intended/planned framing per [ni-51-102].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
