---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
cites:
  - ni-51-102
  - osc-sn-51-721
references:
  - clones/project-knowledge/.claude/drafts-outbound/research-wikipedia-leapfrog-2030.draft.md
  - external:en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Lead_section
  - external:en.wikipedia.org/wiki/Wikipedia:Verifiability
  - external:en.wikipedia.org/wiki/Wikipedia:Citing_sources
  - external:meta.wikimedia.org/wiki/Wikimedia_Foundation_Annual_Plan/2025-2026/Product_%26_Technology_OKRs
  - external:schema.org/TechArticle
---

The PointSav documentation wiki at documentation.pointsav.com inherits its article reading surface from Wikipedia under the Vector 2022 design. Article tabs, edit pencils, hatnotes, lead-section conventions, collapsible tables of contents, infobox conventions, references sections, and category breadcrumbs all preserve the structural primitives a Wikipedia reader recognises without conscious thought. The companion TOPIC [[wikipedia-leapfrog-design]] covers what is preserved verbatim — the muscle-memory contract.

This TOPIC covers what extends beyond. Five article-shell primitives that Wikipedia's volunteer-governance model has been structurally unable to ship in fifteen years are described here. Three are first-class — the substrate ships them at iteration 1. Two are second-class — the substrate defines their token and engine surfaces and ships them when the corpus reaches the scale where they pay off the editorial cost.

## Why the leapfrog is needed

Wikipedia's article shell is the most-imitated reading surface on the public internet. It is the gold standard for general-knowledge encyclopedic depth precisely because its primitives are honed by twenty years of editorial-community refinement. It is also structurally limited in 2026 by ten specific weaknesses that no commercial wiki competitor has addressed.

The leapfrog primitives in this TOPIC are not novelties. Each addresses a specific named weakness with a specific named primitive. The substrate ships the fix because it has the engineering surface (Rust + axum + maud + comrak + git2 + Tantivy under `app-mediakit-knowledge`) and the editorial discipline (the project-language gateway with the draft-research-trail-discipline mandate per Doctrine claim #39) to do so. Wikipedia structurally cannot — its codebase is 25 years old, its community-consensus governance has not achieved coalition for substantial article-shell change since 2012, and its labour model rewards new articles over revisions to existing structural infrastructure.

## Where Wikipedia's article shell is structurally weak

Ten weakness categories from the 2026 audit:

**(i) References section is a flat numeric list with no source-authority semantics.** A peer-reviewed Nature paper and a personal blog post occupy identical visual registers. An auditor or analyst who wants to know whether a claim is regulator-backed or industry-press-backed must read each citation in full.

**(ii) Infoboxes are semi-structured but not natively machine-readable.** Wikimedia Enterprise's Structured Contents API parses them, but the API is paywall-gated and external to the reading surface. Wikidata is the canonical machine-readable mirror but synchronisation is volunteer-maintained and inconsistent.

**(iii) Table of contents is structural-only with no semantic section typing.** "Background", "Method", "Controversy", "Technical implementation" cannot be distinguished by the table of contents machinery — readers must infer from section titles.

**(iv) What-links-here returns a paginated flat list, not a graph.** For a concept article the list may contain thousands of articles. No second-hop neighbours, no cluster grouping by topic domain, no machine-readable export at article level.

**(v) No inline-comment surface on the article reading view.** Editorial discussion is on a separate Talk: page; there is no way to see that a particular sentence is contested without leaving the article.

**(vi) No per-section last-edited or authorship granularity.** A 20-section article reports only article-level "last edited" — the freshness illusion.

**(vii) No reading-time or skim-aid.** Article-size guidance is metadata at `?action=info`, not surfaced in the reading view.

**(viii) No citation trail back to the specific cited passage.** Footnote `[4]` resolves to a bibliography entry; the reader must independently navigate to the cited source and locate the relevant passage within it.

**(ix) No live-edit currency indicator.** Articles edited dozens of times per day present no in-session change signal.

**(x) AI-consumption surface is unstructured at section granularity.** Wikipedia's reading-surface HTML provides no per-section semantic hints. The Wikimedia Foundation's 2025-2026 OKRs note that 65% of expensive requests come from scraper bots collecting AI training data — the structure provided does not match the structure AI consumers need.

## The leapfrog primitives

### Citation-authority ribbon (first-class)

A small leading badge on each entry in an article's References section indicating source category — academic, regulator, industry, direct-source, news, web-informal. The class is derived from the citation template type and optionally from a `source_authority` frontmatter field. Emitted as an additional `@type` refinement on `citation` entries in the JSON-LD `<head>` block.

A reader can see at a glance whether the article is backed by academic and regulatory sources or by informal ones. An AI consumer pulling structured data gets source authority as a machine-readable field. This primitive addresses weakness (i) directly.

### Research-trail footer block (first-class)

A collapsible footer block below the References section, rendered when the article frontmatter declares `research_trail: true`. Three subsections per the draft-research-trail-discipline (Doctrine claim #39): Research done (sources consulted with status), Suggested research (next-leg open tasks), Open questions (claims requiring verification). Collapsed by default.

The trail is emitted as structured JSON-LD `potentialAction` nodes — `SearchAction` for suggested research, `Question` for open questions. LLM consumers identify the article's epistemic frontier without reading prose. This addresses weaknesses (viii) and (x) simultaneously.

The combination of citation-authority ribbon and research-trail footer makes the article's epistemological position legible without reading all the footnotes. A financial-community reader, an analyst, or a regulator — any reader whose professional training involves source-type assessment — immediately understands what they are looking at.

### Freshness ribbon — per-section last-content-review (first-class)

An optional small badge on each section heading showing the date of the last substantive content change. Three-stop colour scale signals fresh / stale / archived per configurable date thresholds. This surface signals what Wikipedia structurally does not — a section-level review date that distinguishes "Background unchanged since 2019" from "Current implementations updated yesterday" — without modifying the article body register.

The substrate emits per-section `dateModified` properties on `WebPageElement` JSON-LD nodes. This addresses weakness (vi) directly and also addresses weakness (x): AI consumers get cheap section-level freshness signals rather than expensive full-article scrapes.

### Plain-language toggle backed by curated authored paragraphs (second-class)

A toggle in the reader-preference toolbar. When active, article sections flagged `plain_language: true` render an alternative lead paragraph written at a lower reading level. The plain-language paragraph appears in a visually distinct block above the technical lead.

Critical design discipline: plain-language paragraphs are explicitly authored by humans and committed to the article source, with the same citation discipline as the article body. They are not generated at request time. This preserves NPOV register and source-based verifiability while extending the entry-point to readers whose background does not match the technical register.

The substrate ships the toggle and the schema; the corpus chooses which articles to author plain-language paragraphs for. Positioned as second-class because curating the plain-language paragraph at edit time costs editorial labour that scales linearly with corpus size.

### Citation-graph mini-map — 3-hop neighbourhood (second-class)

A collapsible section at the article foot showing a small SVG graph: the current article as centre node, 1-hop outbound wikilinks as one ring, 1-hop inbound links as a second ring. Nodes labelled with article titles; edges carry directionality. Interactive — clicking navigates to that article.

The same link data is emitted in JSON-LD `relatedLink` and `mentions` arrays. Downstream knowledge-graph consumers traverse without the visual layer. Positioned as second-class because the wikilink graph must be pre-computed at render time or served from an API. Worth shipping when the article corpus reaches a size where graph traversal is genuinely useful (target: ≥200 articles).

## What the leapfrog deliberately does not change

The body register that makes Wikipedia's prose feel authoritative is the product of explicit editorial discipline codified in its Manual of Style. Every leapfrog primitive in this TOPIC is additive — none modify the body register.

The summary style (every section opens with its most important information). The defined subject at the open (bolded subject plus copula plus definitional clause). The NPOV register (institutional voice; attributing claims rather than asserting). The paragraph length discipline (3–6 sentences typical). The link density as navigation density (first-occurrence-only blue links). The lead-section contract (the lead is a summary, not a teaser). Register consistency across section types.

All seven characteristics are preserved verbatim. The leapfrog primitives are subordinate to the body — the citation-authority badges sit in a 1.25em gutter that does not break line-rhythm; the research-trail is collapsed by default; the freshness ribbons can be toggled off entirely; the plain-language toggle is opt-in; the citation-graph mini-map is collapsed below the visible article footer. A reader who reads only the body receives the Wikipedia muscle-memory contract intact.

## What this article shell is planned to compete for

The substrate is planned to be structurally competitive in the same award framings as the home-page composition: Awwwards Site of the Day or Site of the Year; Webby Award in the Reference category; Information is Beautiful Awards in the Interactive / Tools & Services category; Communication Arts Interactive Annual in the Information Design subcategory; the GitNation JavaScript Open Source Awards; the European Open Source Awards; and editorial coverage in MIT Technology Review's annual technology surveys.

The article-shell-specific differentiator is the citation-authority ribbon and research-trail footer combination — the article's epistemological position made legible at the reading surface, in a way that no other public knowledge platform ships in 2026.

Whether any specific award lands depends on factors outside the substrate's control. The substrate's structural position is what is claimed here; awards are downstream consequence.

## Open editorial item

A public Talk-page surface for each article is planned. The substrate may surface a small inline-annotation affordance in a future iteration — a way for a reader to see that a particular sentence is contested or recently fact-checked without leaving the article. The substrate-design and engine surfaces for this are tracked in NEXT.md but not committed to a specific iteration.

## See also

- [[wikipedia-leapfrog-design]] — the muscle-memory contract: what is preserved verbatim from Wikipedia
- [[app-mediakit-knowledge]] — the engine that ships these primitives
- [[knowledge-wiki-home-page-design]] — home-page leapfrog design intent and the two-audience contract
- [[wiki-provider-landscape]] — the competitive landscape and why no provider has replaced Wikipedia

## Provenance

Authored 2026-04-30 by the project-knowledge cluster, synthesising parallel sub-agent research and direct workspace-document consultation. The substrate-internal design research at `clones/project-knowledge/.claude/drafts-outbound/research-wikipedia-leapfrog-2030.draft.md` is the source of truth for the primitive prioritisation. The companion DESIGN-COMPONENT recipes (`component-citation-authority-ribbon`, `component-research-trail-footer`, `component-freshness-ribbon`) define the substrate-canonical visual contract; this TOPIC is the public-facing narrative. Refined by project-language 2026-04-30.

Forward-looking statements per [ni-51-102] and [osc-sn-51-721] continuous-disclosure posture. Material assumptions: design-system substrate refines token-bundle and component recipes per the companion drafts; editorial labour for the project-language gateway is sustained; the engine work for per-section JSON-LD emission is shipped in a future project-knowledge cluster iteration tracked in NEXT.md.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
