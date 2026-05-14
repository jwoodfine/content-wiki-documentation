---
schema: foundry-doc-v1
title: "The article shell leapfrog"
slug: article-shell-leapfrog
category: applications
type: topic
quality: complete
short_description: "Five article-shell primitives that extend Wikipedia's reading surface at structural weaknesses volunteer-governance cannot address: citation-authority ribbon, research-trail footer, freshness ribbon, plain-language toggle, and citation-graph mini-map."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: article-shell-leapfrog.es.md
cites:
  - ni-51-102
  - osc-sn-51-721
references:
  - id: 1
    text: "Wikipedia Manual of Style — Lead section."
    url: "https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Lead_section"
  - id: 2
    text: "Wikipedia:Verifiability policy."
    url: "https://en.wikipedia.org/wiki/Wikipedia:Verifiability"
  - id: 3
    text: "Wikimedia Foundation Annual Plan 2025-2026 — Product and Technology OKRs."
    url: "https://meta.wikimedia.org/wiki/Wikimedia_Foundation_Annual_Plan/2025-2026/Product_%26_Technology_OKRs"
  - id: 4
    text: "Schema.org TechArticle specification."
    url: "https://schema.org/TechArticle"
---

The PointSav documentation wiki at `documentation.pointsav.com` inherits its article reading surface from Wikipedia under the Vector 2022 design. Article tabs, edit pencils, hatnotes, lead-section conventions, collapsible Tables of Contents, infobox conventions, references sections, and category breadcrumbs all preserve the structural primitives a Wikipedia reader recognises without conscious thought.[^1] The companion article [[wikipedia-leapfrog-design]] covers what is preserved verbatim — the muscle-memory contract.

This article covers what extends beyond. Five article-shell primitives that Wikipedia's volunteer-governance model has been structurally unable to ship in fifteen years are introduced here. Three are first-class — the substrate ships them at iteration 1. Two are second-class — the substrate defines their token and engine surfaces and ships when the corpus reaches the scale where they pay off the editorial cost.

## Why the leapfrog is needed

Wikipedia's article shell is the most-imitated reading surface on the public internet. It is the gold standard for general-knowledge encyclopedic depth precisely because its primitives are honed by twenty years of editorial-community refinement. It is also structurally limited in 2026 by ten specific weaknesses that no commercial wiki competitor has shipped a fix for. The Wikimedia Foundation has named some of them in its 2025-2026 Product and Technology OKRs[^3]; others are visible in academic literature and Wikipedia's own Talk: discussion threads.

The leapfrog primitives below are not novelties. Each addresses a specific named weakness with a specific named primitive. The substrate ships the fix because it has the engineering surface and the editorial discipline to do so. Wikipedia structurally cannot — its codebase is 25 years old, its community-consensus governance has not achieved coalition for substantial article-shell change since 2012, and its labour model rewards new articles over revisions to existing structural infrastructure.

## Where Wikipedia's article shell is structurally weak

Ten weakness categories from the 2026 audit:

**(i) References section is a flat numeric list with no source-authority semantics.** A peer-reviewed paper and a personal blog post occupy identical visual registers. An auditor or analyst who wants to know whether a claim is regulator-backed or industry-press-backed must read each citation in full.

**(ii) Infoboxes are semi-structured but not natively machine-readable.** Wikidata is the canonical machine-readable mirror but synchronisation is volunteer-maintained and inconsistent.

**(iii) Table of Contents is structural-only with no semantic section typing.** "Background", "Method", "Controversy", "Technical implementation" cannot be distinguished by the TOC machinery — readers must read section titles and infer.

**(iv) What-links-here returns a paginated flat list, not a graph.** For a concept article the list may contain thousands of articles, with no second-hop neighbours, no cluster grouping by topic domain, and no machine-readable export at article level.

**(v) No inline-comment surface on the article reading view.** Editorial discussion is on a separate Talk: page; there is no way to see that a particular sentence is contested without leaving the article.

**(vi) No per-section last-edited or authorship granularity.** A 20-section article reports only article-level "last edited" — the freshness illusion.

**(vii) No reading-time or skim-aid.** Article-size guidance is metadata at `?action=info`, not surfaced in the reading view.

**(viii) No citation trail back to the specific cited passage.** Footnote `[4]` resolves to a bibliography entry; the reader must independently navigate to the cited source and locate the relevant passage.

**(ix) No live-edit currency indicator.** Articles edited dozens of times per day present no in-session change signal.

**(x) AI-consumption surface is unstructured at section granularity.** Wikipedia's reading-surface HTML provides no per-section semantic hints. The Wikimedia Foundation's 2025-2026 OKRs explicitly note that 65% of expensive requests come from scraper bots collecting AI training data — the structure provided does not match the structure AI consumers need.[^3]

## The leapfrog primitives

### Citation-authority ribbon (first-class)

A small leading badge on each entry in an article's References section indicating source category — academic, regulator, industry, direct-source, news, web-informal. The class is derived from the citation template type and optionally from a `source_authority` frontmatter field. Emitted as an additional `@type` refinement on citation entries in the JSON-LD `<head>` block.[^4]

A reader can see at a glance whether the article is backed by academic and regulatory sources or by informal ones. An AI consumer pulling structured data gets source authority as a machine-readable field. This addresses weakness (i) directly.

### Research-trail footer block (first-class)

A collapsible footer block below the References section, rendered when the article frontmatter declares `research_trail: true`. Three subsections: Research done (sources consulted with status), Suggested research (next-leg open tasks), Open questions (claims requiring verification). For editors and researchers, not casual readers — collapsed by default.

The trail is emitted as structured JSON-LD `potentialAction` nodes — `SearchAction` for suggested research, `Question` for open questions. AI consumers identify the article's epistemic frontier without reading prose. This addresses weaknesses (viii) and (x) above simultaneously: a reader gets a one-glance summary of what the editor knows is open; an AI consumer gets a typed semantic frontier.

The combination of citation-authority ribbon and research-trail footer is what makes the article's epistemological position legible without reading all the footnotes. A financial-community reader, an analyst, a regulator — any reader whose professional training involves source-type assessment — immediately understands what they are looking at.[^2]

### Freshness ribbon — per-section last-content-review (first-class)

An optional small badge on each section heading (right-end of the heading row, after the `[edit]` pencil) showing the date of the last substantive content change to that section. Three-stop colour scale signals fresh / stale / archived per configurable date thresholds. Surfaces a signal Wikipedia structurally does not — a section-level review date that distinguishes "Background unchanged since 2019" from "Current implementations updated yesterday" — without modifying the article body register.

The substrate emits per-section `dateModified` properties on `WebPageElement` JSON-LD nodes. This addresses weakness (vi) directly and also addresses weakness (x): AI consumers get cheap section-level freshness signals rather than expensive full-article scrapes.

### Plain-language toggle backed by curated authored paragraphs (second-class)

A toggle in the reader-preference toolbar. When active, article sections flagged `plain_language: true` in their frontmatter render an alternative lead paragraph written at a lower reading level. The plain-language paragraph appears in a visually distinct block above the technical lead.

Critical design discipline: plain-language paragraphs are explicitly authored by humans and committed to the article source, with the same citation discipline as the article body. They are not generated automatically at request time. This preserves the neutral-point-of-view register and source-based verifiability while extending the entry-point to readers whose reading level or background does not match the technical register.

The substrate ships the toggle and the schema; the corpus chooses which articles to author plain-language paragraphs for. Positioned as second-class because curating the plain-language paragraph at edit time costs editorial labour that scales linearly with corpus size.

### Citation-graph mini-map — 3-hop neighbourhood (second-class)

A collapsible section at the article foot showing a small SVG graph: the current article as centre node, 1-hop outbound wikilinks as one ring, 1-hop inbound links as a second ring. Nodes labelled with article titles; edges carry directionality. Interactive — clicking navigates to that article. Sized to a fixed aspect-ratio box; only top-N nodes by link weight shown with an "expand" affordance.

The same link data is emitted in JSON-LD `relatedLink` and `mentions` arrays. Downstream knowledge-graph consumers traverse without the visual layer. Positioned as second-class because the wikilink graph must be pre-computed at render time or served from an API. Worth shipping when the article corpus reaches a size where graph traversal is genuinely useful (target: ≥200 articles).

## What the leapfrog deliberately does not change

The body register that makes Wikipedia's prose feel authoritative is the product of explicit editorial discipline. Every leapfrog primitive in this article is additive — none modify the body register. The summary style (every section opens with its most important information). The defined subject at the open (bolded subject, copula, definitional clause). The neutral-point-of-view register (institutional voice; attributing claims rather than asserting). The paragraph length discipline (3–6 sentences typical; visual whitespace separating; scannable rhythm). The link density as navigation density (first-occurrence-only blue links; no decorative links). The lead-section contract (the lead is a summary, not a teaser).

All six characteristics are preserved verbatim. The leapfrog primitives are subordinate to the body — the citation-authority badges sit in a 1.25em gutter that does not break line-rhythm; the research-trail is collapsed by default; the freshness ribbons can be toggled off by reader preference; the plain-language toggle is opt-in; the citation-graph mini-map is collapsed below the visible article footer. A reader who arrives at the article shell and reads only the body receives the Wikipedia muscle-memory contract intact.

## What this article shell is planned to be competitive for

The substrate is *planned* to be structurally competitive in recognised design and editorial-publishing evaluation contexts — site design awards, the Webby Award in the Reference category (where Wikipedia itself has won), Information is Beautiful Awards in the Interactive and Tools categories, and editorial coverage in technology-journalism annual surveys. The article-shell-specific differentiator is the citation-authority ribbon combined with the research-trail footer — the article's epistemological position made legible at the reading surface, in a way that no other public knowledge platform ships in 2026.

Whether any specific recognition follows depends on factors outside the substrate's control — submission timing, competitive entries, editorial coverage. The substrate's structural position is what is described here; recognition is a downstream consequence, not a premise. Cautionary language applies per [ni-51-102] and [osc-sn-51-721].

## See also

- [[wikipedia-leapfrog-design]] — the muscle-memory contract and what is preserved verbatim from Wikipedia
- [[knowledge-wiki-home-page-design]] — the home page design intent and the two-audience contract
- [[app-mediakit-knowledge]] — the wiki engine; the JSON-LD emission path for per-section metadata
