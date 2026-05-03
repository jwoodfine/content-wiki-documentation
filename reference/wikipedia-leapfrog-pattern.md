---
schema: foundry-doc-v1
title: "The Wikipedia Leapfrog Pattern"
slug: wikipedia-leapfrog-pattern
category: reference
type: topic
quality: published
short_description: Nine Wikipedia structural patterns and their substrate-enforced equivalents — the leapfrog transformation that replaces volunteer editorial norms with generation-time, commit-time, and training-loop enforcement.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: wikipedia-leapfrog-pattern.es.md
---

Wikipedia's editorial authority rests on twenty years of accumulated structural conventions: article anatomy, disambiguation hatnotes, footnote density standards, navigation primitives, infobox templates, talk-page deliberation, quality grades, summary-style writing, and attributed contribution. These conventions are enforced through volunteer social norms, bot patrol, editorial review, and community governance. They are powerful because they have been iterated for decades; they are also fragile because their enforcement depends on sustained volunteer attention that is uneven across the corpus.

The PointSav documentation wiki draws its structural muscle memory from Wikipedia while replacing volunteer enforcement with substrate enforcement. Where Wikipedia relies on editorial convergence over months, the PointSav substrate enforces equivalent structures at generation time, at commit time, and through a continued-training loop. This document maps nine Wikipedia structural patterns to their substrate equivalents and identifies the leapfrog transformation each enables.

## Article anatomy — inverted pyramid at generation time

Wikipedia's inverted-pyramid article structure is a negotiated convention. The lead section should carry a one-sentence definition, a one-paragraph summary, and a complete overview that a reader can stop at any depth and still have a coherent picture. Achieving this on a new article typically takes months of editorial attention.

The PointSav substrate enforces the inverted-pyramid structure before the draft reaches a creative contributor. The genre template applied at refinement time requires a one-sentence definition as the opening body line, an overview section within the first two hundred words, and a fixed section ordering. Article type — concept, service, application, governance decision, and others — drives per-type lead-paragraph templates that are structurally correct before any human author reads the draft.

Leapfrog: Wikipedia enforces anatomy through volunteer social norms over months. The substrate enforces it at generation time. Creative contributors inherit a structurally complete lead and apply narrative craft on top.

## Disambiguation — canonical term enforcement via glossary

Wikipedia's hatnote system — the disambiguation and cross-reference notes that appear at the top of articles with potential name collisions — is placed by editors and degrades when disambiguation pages accumulate without curation.

The PointSav substrate maintains canonical term values in a per-wiki glossary. The banned-vocabulary grammar applied at refinement time enforces preferred terms at generation time: a draft cannot produce non-canonical synonyms for platform-specific names. Machine-readable front-matter fields carry disambiguation and cross-reference relations that the wiki renderer resolves automatically into equivalent hatnote structures.

Leapfrog: Wikipedia's disambiguation depends on editorial convergence. Term consistency is a substrate property enforced at generation time, not an editorial outcome.

## Footnote density — citation registry resolves URLs at refinement

Wikipedia's citation quality is a function of volunteer attention: high-traffic articles carry dense, verified citations; stub articles carry none. The reliable-sources policy names the standard, but enforcement is per-editor and uneven.

The PointSav citation substrate maintains a registry mapping stable citation identifiers to verified source records. The editorial gateway resolves raw URLs in draft material to registry identifiers at refinement time. Per-document front-matter lists the citations used, and the renderer filters the bibliography to only cited entries. The LEGAL protocol variant disables citation generation entirely and routes factual claims to an explicit verification step rather than allowing the substrate to produce a citation it cannot verify.

Leapfrog: Wikipedia's citation quality is volunteer-dependent. The PointSav substrate can only reference entries that exist in the verified registry, and resolution happens at refinement time on every draft.

## Navigation — map-of-content landings and aliased wikilinks

Wikipedia's navigation is multi-layered but degrades at depth: category trees require per-edit volunteer maintenance, navboxes accumulate inconsistently, and "what links here" produces unfiltered noise at scale.

The PointSav wiki caps URL depth at two levels. Each category carries a curated Map of Content landing page with prose-introduced sub-theme groupings. Alias fields in front-matter allow old slugs to resolve to current articles without creating redirect files. Named-relation fields generate navbox-equivalent navigation automatically from structured metadata. An automatically built "wanted articles" page, derived from unresolved wikilinks sorted by inbound-link count, provides the red-link discovery mechanism without per-article manual maintenance.

Leapfrog: Wikipedia's navigation requires per-article curation and bot-assisted redirect management. The PointSav wiki derives navigation from machine-readable front-matter, and most navigation artefacts are computed rather than authored.

## Article type templates — type-driven genre selection

Wikipedia's infoboxes are type-specific structured metadata blocks selected and filled manually by editors. Template documentation lags implementation; required fields are frequently omitted.

A closed article-type enumeration in the front-matter schema selects the appropriate genre template at refinement time. A service article cannot be generated without an operations section; a governance decision article cannot be generated without a decision statement and rationale. Per-type structure is applied as prompt scaffolding at generation time, before the draft reaches any human reviewer.

Leapfrog: Wikipedia's infobox templates are selected and filled manually. Article type drives template selection automatically; Creative contributors inherit a structurally typed article.

## Talk-page deliberation — structured audit trail

Wikipedia's talk pages are the deliberation record for each article: proposed edits, content disputes, consensus built through threaded discussion. The pattern degrades at volume: threads are chronological, no formal decision format exists, and an editor returning after months cannot reconstruct the editorial history without reading the full thread.

The PointSav framework maintains three structured audit mechanisms. A cleanup log per repository carries rolling dated entries with open and closed states for in-flight decisions. A passive outbox tracks cross-repository file moves as a structured state machine with defined transitions rather than as ad hoc actions. Every editorial decision that reaches a commit becomes an SSH-signed entry in the version-control history, and when the editorial pipeline is operational, it also becomes a preference training pair in the apprenticeship corpus.

Leapfrog: Wikipedia's talk pages are unstructured, unqueryable, and feed no model. The PointSav audit trail is structured, cryptographically signed, and feeds continued training. The editorial governance surface is simultaneously a training-signal generator.

## Quality grades — threshold-triggered status transitions

Wikipedia's quality grades range from Stub to Featured Article. Grade assessments happen on talk pages; the Featured Article pipeline requires formal nomination and volunteer review. Articles frequently remain at intermediate grades indefinitely because the promotion pipeline is volunteer-bottlenecked.

The `status` field in the PointSav front-matter schema has a defined lifecycle: pre-build, draft, stable. Status transitions are triggered by substrate-enforced criteria rather than volunteer nomination. An article moves from draft to stable when the editorial gateway pass clears the banned-vocabulary grammar, the forward-looking disclosure validator, and the citation registry resolver. A creative contributor revert drops the article one status level.

Leapfrog: Wikipedia's quality grades depend on volunteer nomination. PointSav article status is updated by substrate-enforced criteria; quality is a substrate property with volunteer craft assessment entering only at the creative contributor stage.

## Summary-style writing — map-of-content alignment via the editorial gateway

Wikipedia's summary-style guideline requires broad articles to summarise sub-topics and each sub-topic to have its own deeper article. Parent and child articles drift out of sync when the child article evolves past what the parent summary describes, and synchronisation is manual.

The PointSav Map-of-Content landing for each category is the structural equivalent of a summary-style parent article. When a child article in a category is updated, the editorial pipeline can generate a refreshed category-landing entry using the same genre template and per-tenant adapter that refined the child article, keeping parent and child in register and voice alignment even when authored in different sessions.

Leapfrog: Wikipedia's summary-style synchronisation is manual and periodic. Category-landing alignment is a pipeline property, not a scheduling problem.

## Attribution — tier-stratified signed contribution

Wikipedia's attribution is open-anonymous: any reader can edit, and edits are attributed to a username or IP address. The model produces a flat attribution signal where high-quality and low-quality contributions are structurally indistinguishable at commit time. Quality is recovered post hoc through bot patrol and volunteer review.

The PointSav three-tier contributor model makes attribution structurally distinct at each tier. Core contributors' commits are cryptographically signed against a verified identity at commit time, with attribution verifiable at any point in the version-control history. Paid creative contributors' edits enter at the end of the editorial cycle as signed commits, and each edit is simultaneously a publication record and a training-signal provenance record. Open-tier consumers attribute by citing the article's stable identifier, publication date, and tenant namespace.

Leapfrog: Wikipedia's attribution is open-anonymous. PointSav attribution is tier-stratified, cryptographically signed, and simultaneously a training-signal provenance record.

## See also

- [[reverse-funnel-editorial-pattern]] — The editorial cycle that produces the training-signal provenance records described in the attribution section.
- [[wiki-provider-landscape]] — A structural audit of twenty-five wiki and knowledge-base providers in 2026, with the gap analysis that contextualises these leapfrog claims.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
