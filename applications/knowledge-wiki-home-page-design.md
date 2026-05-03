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
  - external:en.wikipedia.org/wiki/Main_Page
  - external:en.wikipedia.org/wiki/Wikipedia:Today%27s_featured_article
  - external:mediawiki.org/wiki/Skin:Vector/2022/Design_documentation
  - vendor/pointsav-monorepo/app-mediakit-knowledge/src/server.rs
  - vendor/pointsav-monorepo/app-mediakit-knowledge/docs/UX-DESIGN.md
  - content-wiki-documentation/.claude/rules/naming-convention.md
---

The PointSav documentation wiki at documentation.pointsav.com is the canonical reading surface for the platform's architecture, services, operating systems, governance, infrastructure, applications, company posture, reference vocabulary, and contributor help. Its home page is structurally inherited from Wikipedia's Main Page — the gold-standard general-knowledge home page on the public internet — and extends that inheritance with primitives Wikipedia's volunteer-governance model has been structurally unable to ship in the past decade.

This TOPIC explains the design intent of the home page: what is preserved verbatim from Wikipedia (the muscle-memory contract), what is added beyond Wikipedia (the leapfrog primitives), and what financial-community readers and engineering readers each see when they arrive.

## Two readers, one home page

The home page serves two audiences simultaneously: an engineering reader (an architect, a developer, a technical writer) who wants depth, source authority, and machine-readable structure; and a financial-community reader (an analyst, an auditor, an investor, a regulator) who wants the substrate posture, the disclosure history, and the company structure laid out in an authoritative register.

Both audiences arrive at the same URL (`/`), see the same composition, and follow the same blue links into the corpus. The home page does not branch — it does not ask "are you an engineer or an investor?" before presenting content. The composition serves both because it inherits Wikipedia's most load-bearing editorial commitment: the absence of marketing copy and the presence of editorial labour. Statements about the platform are structural ("9 categories", "N articles", "last updated YYYY-MM-DD"), not promotional. The reader who arrives sceptical adjusts their epistemic posture toward curiosity, not toward defence against a sales register.

## Wikipedia muscle-memory — preserved verbatim

Ten structural slots compose Wikipedia's English Main Page. Each carries a defined role, refresh cadence, and editorial maintainer. Removing any one breaks the contract that makes the Main Page the gold standard. The PointSav home page preserves the load-bearing primitives as follows.

**Welcome banner — preserved.** Wikipedia opens with a single sentence and two statistics: scope and community scale. PointSav opens with the equivalent: scope ("PointSav's platform documentation covers the architecture, services, operating systems, and governance conventions of the PointSav substrate") and structural scale ("N articles across 9 categories, last updated YYYY-MM-DD"). Both are derived at render time, not authored as marketing copy. No adjectives of self-description appear in the banner.

**Featured article — preserved.** Wikipedia's Today's Featured Article is one article per day drawn from the 0.1% that have passed Featured Article Candidates review. The blurb is enforced to 909–1,009 characters — character count, not word count, because the constraint prevents both padding and truncation across the daily rotation. PointSav preserves the format invariant: bolded linked title, body-register paraphrase of the article lead, "→ Read" closer (a deliberate non-CTA — it reads as encyclopedic prose continuation, not as a marketing button). The featured article rotates as the editorial pipeline warrants; the rotation cadence is currently weekly rather than daily because contributor volume does not yet support a daily slot.

**Browse by category — preserved structurally, extended in scope.** Wikipedia's Main Page surfaces topics through a sidebar of project links and the categorised browse facility on individual articles. PointSav surfaces all nine ratified categories — architecture, services, systems, applications, governance, infrastructure, company, reference, help — in a 3×3 grid at the home page surface. The grid renders all nine even when a category is empty ("0 articles — in preparation") so the platform's intended scope is visible at launch rather than only when contributors fill it. The 9-category set is operator-ratified per `naming-convention.md` §10 Q5-A and is not subject to runtime reordering.

**Recent additions — preserved.** Wikipedia's Did You Know section surfaces recently created or expanded articles. PointSav's home page surfaces the top 5 articles by `last_edited` date in descending order. The intent matches Wikipedia's: signal that the corpus is actively maintained, give returning readers a reason to return, and provide a low-friction discovery surface for newly published material.

**Footer — preserved.** Wikipedia's footer carries license, privacy, terms, contact, and last-updated timestamp. No advertising, no newsletter signup, no affiliate links. PointSav matches: CC BY 4.0 license notice, link to the source-of-truth GitHub repositories, no commercial framing.

The blue link colour, the sans-serif heading on serif body register, the absence of bold except for article titles, the column grammar, and the density-without-clutter measurement — all are inherited directly. These are what a reader recognises without conscious thought as "encyclopedia register". They signal that this is a reference work, not a product website.

## The leapfrog — what extends Wikipedia at the home page surface

Five primitives extend Wikipedia's home-page composition. Three are first-class — the substrate ships them at iteration 1 when authoring labour permits. Two are second-class — the substrate defines their token and engine surfaces, and ships them when corpus scale and editorial labour pay off the cost.

### Machine-readable slot structure

Wikipedia's home page has no structured data describing its slots. A scraper or AI consumer parsing the rendered HTML can extract visible content but cannot identify which slot a content fragment belongs to without inferring from headings. The PointSav home page emits JSON-LD per slot — the featured-article slot is a typed `Article` reference, the recent-additions slot is an `ItemList` of typed `Article` references, the category grid is a typed `WebPageElement` collection. Downstream consumers — feed readers, voice interfaces, language models — receive structure rather than prose to infer.

This addresses a structural problem the Wikimedia Foundation named in its 2025-2026 Product and Technology OKRs: 65% of Wikipedia's most expensive requests come from scraper bots collecting AI training data, and the structure provided does not match the structure AI consumers need.

### Editorial-labour cadence as visible signal

Wikipedia's home page works because Today's Featured Article, Did You Know, In the News, and On This Day are maintained daily by named editorial coordinators. Most engineering documentation home pages have no equivalent — a "Latest Changes" section last updated six months ago signals abandonment regardless of article quality. The PointSav home page surfaces the editorial labour cadence visibly through the "last updated" timestamp in the welcome banner (derived from the maximum `last_edited` across the corpus), the rotating featured article (signalling recent editorial review), and the recent-additions feed (signalling continuous contribution).

A future iteration is intended to extend this with an explicit ratification gate on the recent-additions feed: rather than ranking by `last_edited` (recency), the substrate may rank by `content_reviewed_on` (a separate frontmatter field denoting last editorial review). The distinction matters because cosmetic edits should not signal freshness; only substantive content review should.

### Editor-as-onramp signal

Wikipedia's home page surfaces participation surfaces — Community portal, Village pump, Help desk — below the main content area. The PointSav home page extends this with an "Other areas" block linking to GitHub source repositories and to the design-system, factory-release-engineering, and contribution-onboarding articles. The reader is not required to participate, but the path from reader to contributor is visible from the home page and is one click away.

### Per-section research-trail teaser (planned)

The article shell ships a research-trail footer showing each article's editorial epistemic frontier — research done, suggested research, open questions. The home page is *intended* to surface a small aggregate widget: "Open editorial questions across the corpus: N". This widget is planned for a future iteration; it requires the article-level research-trail discipline to be widely adopted before the aggregate is meaningful.

### Citation-graph entry point (planned)

The PointSav substrate is *planned* to ship a citation-graph mini-map at the article foot and an aggregate citation-graph entry point on the home page. The home-page entry will let a reader explore the corpus's knowledge graph as a visual surface — typed nodes, weighted edges, red-link gaps visible as unrealised nodes. Both are deferred until the corpus reaches ≥200 articles where graph traversal pays off the editorial cost.

## What the home page deliberately does not do

The home page does not display advertising. It does not collect newsletter signups. It does not invoke marketing copy. It does not branch by audience. It does not surface social-media share buttons. It does not present "Get started" or "Get a demo" calls-to-action. It does not display engagement metrics at the home-page surface.

Each of these absences is load-bearing. A home page that ships any of them would be optimised for conversion or engagement, which is the documentation aesthetic of SaaS product marketing — and that aesthetic signals to the reader that they are reading marketing rather than reference. Wikipedia's home page contains zero adjectives of self-description because adjectives of self-description destroy encyclopedic register.

## What this home page is planned to compete for

The PointSav substrate is designed to be structurally competitive in seven realistically reachable design and editorial-publishing awards: Awwwards Site of the Day or Site of the Year; Webby Award in the Reference category; Information is Beautiful Awards in the Interactive / Tools & Services category; Communication Arts Interactive Annual in the Information Design subcategory; the GitNation JavaScript Open Source Awards; the European Open Source Awards; and editorial coverage in MIT Technology Review's annual technology surveys.

The substrate is not pre-emptively claiming any of these awards. The home page surface, the article shell substrate, the editorial pipeline, and the design-token vocabulary are designed and shipped to the structural standard those juries evaluate against. Whether any specific award lands depends on factors outside the substrate's control — submission timing, jury composition, competitive entries — and is not a load-bearing claim of this TOPIC.

## Open editorial item

A public Talk-page surface for each article is planned. As of this writing, editorial discussion is preserved in the per-cluster mailbox infrastructure and is not surfaced at the article reading view. Adding a public Talk surface is a future iteration tracked in the project-knowledge cluster's NEXT.md. Per [ni-51-102] continuous-disclosure posture, the current absence of a public Talk surface is intentional pending the editorial-substrate decision; the substrate may surface Talk as a separate URL pattern (`/talk/<slug>`) when the corpus and editorial labour support it.

## See also

- [[article-shell-leapfrog]] — the article-shell leapfrog primitives: five additions beyond Wikipedia at the individual article surface
- [[app-mediakit-knowledge]] — the engine architecture; chrome inventory and compatibility surface
- [[wiki-provider-landscape]] — the competitive-landscape audit and why no provider has replaced Wikipedia
- [[substrate-native-compatibility]] — why this engine ships its own surface rather than reusing an existing wiki engine
- [[wikipedia-leapfrog-design]] — the Phase 1.1 chrome design intent and the 95%/5% muscle-memory contract

## Provenance

Authored 2026-04-30 by the project-knowledge cluster based on parallel sub-agent research and direct workspace-document consultation. The companion design-research draft at `clones/project-knowledge/.claude/drafts-outbound/research-wikipedia-leapfrog-2030.draft.md` (entering project-design's gateway in the same pickup batch) is the substrate-internal source of truth; this TOPIC is its public-facing narrative. Refined by project-language 2026-04-30.

Forward-looking statements about planned iterations and award competitiveness follow [ni-51-102] and [osc-sn-51-721] continuous-disclosure posture. Material assumptions: editorial labour cadence is sustained; corpus growth follows the staged trajectory in NEXT.md; design-system substrate refines token-bundle additions per the companion DESIGN-TOKEN-CHANGE draft.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
