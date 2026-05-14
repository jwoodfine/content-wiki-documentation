---
schema: foundry-doc-v1
title: "Knowledge wiki home page — design intent"
slug: knowledge-wiki-home-page-design
category: applications
type: topic
quality: complete
short_description: "Design intent behind documentation.pointsav.com's home page: the Wikipedia structural primitives preserved verbatim, the five leapfrog additions built on top, and what each audience — engineering reader and financial-community reader — encounters on arrival."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: knowledge-wiki-home-page-design.es.md
cites:
  - ni-51-102
  - osc-sn-51-721
---

The PointSav documentation wiki at `documentation.pointsav.com` is the canonical reading surface for the platform's architecture, services, operating systems, governance, infrastructure, applications, reference vocabulary, and design system. Its home page is structurally inherited from Wikipedia's Main Page — the gold-standard general-knowledge home page on the public internet — and extends that inheritance with primitives Wikipedia's volunteer-governance model has been structurally unable to ship in the past decade.

This article explains the design intent of the home page: what is preserved verbatim from Wikipedia (the muscle-memory contract billions of readers know by reflex), what is added beyond Wikipedia (the leapfrog primitives), and what financial-community readers and engineering readers each encounter on arrival.

## Two readers, one home page

The home page serves two audiences simultaneously: an engineering reader — an architect, a developer, a technical writer — who wants depth, source authority, and machine-readable structure; and a financial-community reader — an analyst, an auditor, an investor, a regulator — who wants the platform's posture, disclosure history, and company structure laid out in the same authoritative register as a regulatory filing.

Both audiences arrive at the same URL (`/`), see the same composition, and follow the same blue links into the corpus. The home page does not branch — it does not ask "are you an engineer or an investor?" before presenting content. The composition serves both because it inherits Wikipedia's most load-bearing editorial commitment: the absence of marketing copy and the presence of editorial labour. Statements about the platform are structural ("10 categories", "N articles", "last updated YYYY-MM-DD"), not promotional ("powerful", "world-class", "trusted by"). The reader who arrives sceptical adjusts their epistemic posture toward curiosity, not toward defence against a sales register.

## Wikipedia muscle-memory — preserved verbatim

Ten structural slots compose Wikipedia's English Main Page. Each carries a defined role, refresh cadence, and editorial maintainer. Removing any one breaks the contract that makes the Main Page the gold standard. The PointSav home page preserves the load-bearing primitives.

**Welcome banner — preserved.** Wikipedia opens with a single sentence and two statistics: scope and community scale (article count plus active editor count). PointSav opens with the equivalent: scope ("PointSav's platform documentation covers the architecture, services, operating systems, and governance of the PointSav substrate") and structural scale ("N articles across 10 categories, last updated YYYY-MM-DD"). Both are derived at render time, not authored as marketing copy. No adjectives of self-description appear in the banner.

**Featured article — preserved.** Wikipedia's Today's Featured Article is one article per day, drawn from the fraction of articles that have passed editorial review. The blurb is enforced to 909–1,009 characters — character count, not word count, because the constraint prevents both padding and truncation across the daily rotation. PointSav preserves the format invariant: bolded linked title, body-register paraphrase of the article lead, "→ Read" closer (encyclopedic prose continuation, not a marketing button). The featured article rotates as the editorial pipeline warrants; the rotation cadence is currently weekly rather than daily because contributor volume does not yet support a daily slot.

**Browse by category — preserved structurally, extended in scope.** Wikipedia's Main Page surfaces topics through categorised browse. PointSav surfaces all ten active categories — architecture, substrate, patterns, systems, services, applications, governance, infrastructure, reference, design-system — at the home page surface. The grid renders all ten even when a category is sparse, so the platform's intended scope is visible from launch rather than only when contributors fill it.

**Recent additions — preserved.** Wikipedia's Did You Know section surfaces recently created or expanded articles. PointSav's home page surfaces the top 5 articles by `last_edited` date in descending order. The intent matches Wikipedia's: signal that the corpus is actively maintained, give returning readers a reason to return, and provide a low-friction discovery surface for newly published material.

**Footer — preserved.** Wikipedia's footer carries licence, privacy, terms, contact, and last-updated timestamp. No advertising, no newsletter signup, no affiliate links. PointSav matches: CC BY 4.0 licence notice, links to the source-of-truth repositories, no commercial framing.

The blue link colour, the sans-serif heading on serif body register, the absence of bold except for article titles, the column grammar (left-dominant content with grid below), and the density-without-clutter measurement — all are inherited directly. These are what a reader recognises without conscious thought as "encyclopedic register". They are the signal that this is a reference work, not a product website.

## The leapfrog — what extends Wikipedia at the home page surface

Five primitives extend Wikipedia's home-page composition. Three are first-class — the substrate ships them when authoring labour permits. Two are second-class — the substrate defines their token and engine surfaces, and ships when corpus scale and editorial labour pay off the cost.

### Machine-readable slot structure

Wikipedia's home page has no structured data describing its slots. A scraper or AI consumer parsing the rendered HTML can extract the visible content but cannot identify which slot a content fragment belongs to without inferring from headings and surrounding markup. The PointSav home page emits JSON-LD per slot — the featured-article slot is a typed `Article` reference, the recent-additions slot is an `ItemList` of typed `Article` references, the category grid is a typed `WebPageElement` collection. Downstream consumers — feed readers, voice interfaces, language models — receive structure rather than prose to infer.

### Editorial-labour cadence as visible signal

Wikipedia's home page works because its rotating sections are maintained by named editorial coordinators. Most engineering documentation home pages have no equivalent labour — a "Latest Changes" section last updated six months ago signals abandonment regardless of article quality. The PointSav home page surfaces the editorial labour cadence visibly through the "last updated" timestamp in the welcome banner (derived from the maximum `last_edited` across the corpus), the rotating featured article (signalling recent editorial review), and the recent-additions feed (signalling continuous contribution).

A planned future iteration extends this with an editorial quality gate on the recent-additions feed: rather than ranking by `last_edited` (recency) the substrate may rank by `content_reviewed_on` (a separate frontmatter field denoting last substantive editorial review). The design intent is to replace Wikipedia's recency-driven Did You Know with a quality-gated Recently Reviewed surface. The field and ranking logic are *planned*; cautionary language applies per [ni-51-102] and [osc-sn-51-721].

### Reader-to-contributor onramp signal

Wikipedia's home page surfaces participation surfaces — Community portal, Village pump, Help desk — below the main content area. The PointSav home page extends this with an "Other areas" block linking to source repositories and to the design system, governance, and contribution-onboarding articles. The reader is not required to participate, but the path from reader to contributor is visible from the home page and is one click away.

### Per-section research-trail teaser (planned)

The article shell ships a research-trail footer showing each article's editorial epistemic frontier — research completed, suggested research, open questions. The home page is *intended* to surface a small aggregate widget: "Open editorial questions across the corpus: N". This widget is *planned* for a future iteration; it requires the article-level research-trail discipline to be widely adopted before the aggregate is meaningful. As of the current iteration, the substrate ships the article-level trail and defers the home-page aggregate.

### Citation-graph entry point (planned)

Wikipedia's What-links-here returns a paginated flat list per article. The PointSav substrate is *planned* to ship a citation-graph mini-map at the article foot and an aggregate citation-graph entry point on the home page. The home page entry would let a reader explore the corpus's knowledge graph as a visual surface — typed nodes, weighted edges, red-link gaps visible as unrealised nodes. Both are *intended* for after the corpus reaches the size where graph traversal pays off the editorial cost.

## What the home page deliberately does not do

The home page does not display advertising. It does not collect newsletter signups. It does not invoke marketing copy. It does not branch by audience. It does not surface social-media share buttons. It does not present "Get started" or "Get a demo" calls-to-action. It does not display engagement metrics at the home-page surface.

Each of these absences is load-bearing. A home page that ships any of them would be optimised for conversion or engagement — the documentation aesthetic of product marketing — and that aesthetic, however well-executed, signals to the reader that they are reading marketing rather than reference. Wikipedia's home page contains zero adjectives of self-description because adjectives of self-description destroy encyclopedic register. The PointSav home page inherits the discipline directly.

## What this home page is designed to be competitive for

The PointSav substrate is designed to be structurally competitive in recognised design and editorial-publishing evaluation contexts: Awwwards in site design; the Webby Awards in the Reference category (where Wikipedia itself has won); Information is Beautiful Awards in the Interactive and Tools categories; Communication Arts Interactive Annual in Information Design; and editorial coverage in technology-journalism annual surveys.

The substrate is not pre-emptively claiming any recognition. The home page surface, the article shell, the editorial pipeline, and the design-token vocabulary are designed and shipped to the structural standard those evaluations assess against. Whether any specific recognition follows depends on factors outside the substrate's control — submission timing, competitive entries, editorial coverage — and is not a load-bearing claim of this article. The substrate's structural position is what is described here; recognition is a downstream consequence, not a premise.

## See also

- [[wikipedia-leapfrog-design]] — the 95%/5% muscle-memory contract and chrome design intent
- [[article-shell-leapfrog]] — the five article-shell primitives beyond Wikipedia
- [[app-mediakit-knowledge]] — the wiki engine architecture and route surface
- [[wiki-provider-landscape]] — the landscape of wiki and documentation providers assessed against Wikipedia's structural primitives
- [[substrate-native-compatibility]] — why the engine ships its own surface rather than reusing an existing wiki engine
