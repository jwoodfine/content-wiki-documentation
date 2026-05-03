---
schema: foundry-doc-v1
title: "Draft Research-Trail Discipline"
slug: draft-research-trail-discipline
category: reference
type: topic
quality: published
short_description: The requirement that every draft entering an editorial or design pipeline carries structured documentation of the research that informed it and the research the next leg should do.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: draft-research-trail-discipline.es.md
---

Publishing a claim without tracing the research behind it produces a document that cannot be audited, improved, or reliably trained on. The draft research-trail discipline requires that every draft entering either the editorial pipeline or the design pipeline carries two forms of research documentation: structured frontmatter fields that machines can parse, and a body section that humans and the refinement gateway can read. Together they create a trail from source material to published claim that persists across every transition in the publication lifecycle.

## Two surfaces, one trail

**Frontmatter fields** carry five required metadata items: the count of research sources the author consulted, the count of research sources the author suggests the gateway consult, the count of open questions the author could not resolve, the provenance category of the research, and a flag indicating whether the trail appears in the body. All five fields are required on every draft; counts of zero are valid for trivial drafts, but the fields themselves are not optional.

**Body section** carries the trail in prose when the body flag is set. It has three subsections: Done (what informed the draft, with one-line findings and their influence on specific parts of the bulk), Suggested (what the gateway should consult, with priority notes), and Open questions (items the author could not resolve, with candidate sources or escalation paths). Subsections may be empty.

## Provenance categories

The `research_provenance` field uses a closed vocabulary: `direct-consultation` (author read primary sources), `sub-agent` (author dispatched a research agent and consumed its result), `citation-registry` (author resolved against the registry only), `mixed`, `tacit` (author judgement without traceable external research, legitimate for drafts that synthesize existing in-context knowledge), or `none` (trivial draft).

Honest declaration of `tacit` is better than fabricated source tokens. The gateway treats tacit drafts with additional refinement scrutiny but does not reject them.

## Source token grammar

A research source in the body section follows a small grammar: a registry citation ID in brackets; a registry ID with a specific clause; a workspace file path; a specific line in a workspace file; a reference to a research agent result file; an external URL not yet in the registry; or an in-session context note. External URL tokens that appear across multiple drafts can be promoted to the citation registry with stable IDs; future drafts then cite by ID rather than URL.

## What the gateway does with the trail

At refinement time, the gateway reads the research-suggested subsection before composing the refinement. It consults named sources where scope allows, records which suggestions it acted on, and notes which remain open. The refined output carries a Provenance footer derived from the trail — citations resolved to registry IDs, workspace references preserved, open questions noting which were resolved and which remain.

Disclosure discipline applies at the Provenance footer stage: forward-looking research items are scrubbed from public-facing Provenance footers; in-session context notes never appear in published output. The footer is a published-substrate property — readers of the documentation wiki see what informed each topic and can follow the citation chain.

## Corpus integration

The apprenticeship corpus that trains the platform's local inference capability gains additional dimensions from the research trail. A `draft-created` event records which sources were consulted and which remain suggested; a `draft-refined` event records which suggested sources the gateway actually consulted during refinement. The model trained on this corpus learns not just the text mapping from raw to refined, but the research practice that underlies good refinement.

## Applies to both pipelines

The discipline applies uniformly to every draft family in both the editorial pipeline (PROSE-*, COMMS-*, LEGAL-*) and the design pipeline (DESIGN-COMPONENT, DESIGN-RESEARCH, DESIGN-TOKEN-CHANGE). Spanish translation drafts inherit their research trail from the English source rather than conducting independent research. The fields are still required; counts of zero are expected and valid.

## Discipline without bureaucracy

The mechanism is designed to be lightweight in practice:

- One-line findings; verbose research goes in a separate research file, referenced once.
- Empty counts are valid and transparent.
- Dispatching a research agent handles the high-research path; most drafts don't need it.
- Open questions that the gateway cannot resolve become outbox asks back to the originating contributor. The trail closes the loop.

## See also

- [[cluster-wiki-draft-pipeline]] — the editorial pipeline that applies this discipline
- [[cluster-design-draft-pipeline]] — the design pipeline that applies this discipline
- [[citation-substrate]] — the registry that recurring external URLs are promoted into
- [[bcsc-disclosure-posture]] — the disclosure rules applied at the Provenance footer stage

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/draft-research-trail-discipline.md` (ratified 2026-04-28). Self-referential: this TOPIC is itself subject to the discipline it describes. Forward-looking statements (corpus training outcomes) carry intended/planned framing per [ni-51-102].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
