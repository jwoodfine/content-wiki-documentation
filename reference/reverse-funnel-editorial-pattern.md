---
schema: foundry-doc-v1
title: "The Reverse-Funnel Editorial Pattern"
slug: reverse-funnel-editorial-pattern
category: reference
type: topic
quality: published
short_description: The structural inversion of conventional editorial workflow — the substrate generates drafts, an editorial gateway refines them to register, and creative contributors enter at the end of the cycle rather than the beginning.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: reverse-funnel-editorial-pattern.es.md
---

In the standard editorial workflow, a writer synthesises source material into a first draft. Engineers review for technical accuracy. An editor reviews for register and brand voice. Only then does a document reach publication. The synthesis burden falls on the writer, the review burden falls on the engineer, and the overall pace is bounded by the slowest person in the chain.

The Reverse-Funnel Editorial Pattern inverts this sequence. The substrate generates a structurally complete draft as a byproduct of normal engineering work. An editorial gateway refines the draft to the required register. The refined version is published. Creative contributors then enter at the end — editing the published version to add craft, opening narrative, graphics, layout, and brand voice. Their edits become the preference signal that trains the substrate to produce sharper baseline drafts in the next cycle.

This pattern is Foundry Doctrine claim 35.

## The inversion in detail

Engineering work — code commits, runbook drafts, architecture notes — produces raw editorial material as a natural byproduct. Task-layer sessions stage this material as draft TOPIC files in their cluster's drafts-outbound directory.

The project-language editorial gateway sweeps those draft files. The refinement step applies a deterministic editorial floor: banned vocabulary is structurally removed, forward-looking statements are framed with the required cautionary language, citation identifiers are resolved against the registry, Bloomberg-standard register is applied, and bilingual pairs are generated. This floor is enforced mechanically, not by an editor reading each document individually.

The refined version is published to the documentation wiki. At this point, the creative contributor enters. Their job is not synthesis — the draft already contains the technical substance. Their job is craft: opening hooks, narrative arc, metaphor, graphics, layout, brand voice. The edited version replaces the refined version as the published document.

The pair of (refined draft, creative-edited version) becomes a preference training pair in the apprenticeship corpus. When the substrate model is trained on accumulated pairs, its baseline draft quality improves. In the next cycle, the creative contributor's incremental load falls because the baseline is already closer to the craft target.

## Why the inversion matters structurally

The conventional pattern places the heaviest cognitive burden at the beginning: the writer must learn the technical content before producing a draft. This makes the writer a bottleneck when subject matter is complex or when the volume of material to document is large. Hiring more writers does not remove the bottleneck proportionally because each writer's onboarding curve must be traversed independently.

The inverted pattern removes the synthesis burden from the creative contributor entirely. The substrate-generated draft contains the technical depth; the creative contributor inherits a structurally complete document and applies taste and craft without needing to understand WORM ledger internals or capability-based security primitives. This expands the talent pool eligible for the creative role and makes each creative contributor's time substantially more productive.

The editorial floor is deterministic and scales with compute, not with editor hours. Quality control on creative output is correspondingly lighter: the substrate floor has already been verified mechanically, and the human review layer focuses on whether craft additions preserved technical accuracy, whether brand voice aligns with the tenant's style, and whether graphics render correctly across target surfaces.

## The three-tier contributor model

The Reverse-Funnel pattern makes explicit where each contributor tier adds value in a substrate-mediated editorial cycle.

Core contributors — the small number of engineers and operators who build and maintain the substrate — operate throughout the cycle. They produce the raw material, operate the editorial gateway, and ratify corpus-producing milestones.

Paid contributors — the creative specialists — enter at the end of each cycle. Their craft work elevates published content from structurally correct to editorially excellent. They are not tech writers in the conventional sense: they do not synthesise, they elevate. Their per-publication leverage is high because the substrate has already handled the volume work.

Open contributors — the broader audience of readers, remixers, and downstream consumers — receive and cite the published creative-edited output. Their interaction with the wiki feeds the demand signal that guides which topics warrant attention in the next cycle.

## The compounding loop

The cycle closes through the training corpus. Creative edits accumulate as preference pairs. Periodic continued pretraining on the accumulated corpus produces a substrate that generates drafts progressively closer to the creative contributor's craft baseline. After enough cycles, the creative contributor's role shifts from correction to light review and rare exception — the substrate handles the eighty or ninety percent case, and the creative contributor's time is freed for the irreducibly human judgment at the margin.

This loop is intentionally closed per-tenant. A creative contributor editing content for a specific customer's deployment produces preference pairs that train a per-tenant adapter. The next cycle's substrate drafts for that tenant come out already closer to that tenant's voice. Multi-tenant general-purpose deployments cannot replicate this because their editorial regime must average across all tenants simultaneously.

## See also

- [[project-tetrad-discipline]] — The wiki leg of the Tetrad is what generates bulk draft input for this pipeline.
- [[service-slm-operationalization-plan]] — The operational plan for bringing the substrate model into active use as a draft generator.
- [[wikipedia-leapfrog-pattern]] — How Wikipedia's editorial structures map to substrate-enforced equivalents.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
