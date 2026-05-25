---
schema: foundry-doc-v1
title: "Knowledge wiki home page — design intent"
slug: knowledge-wiki-home-page-design
short_description: "How the documentation.pointsav.com home page inherits Wikipedia's structural conventions and extends them for engineering and financial-community readers."
category: applications
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: knowledge-wiki-home-page-design.es.md
cites: [ni-51-102, osc-sn-51-721]
---

# Knowledge wiki home page — design intent

The PointSav documentation wiki at documentation.pointsav.com is the canonical reading surface for the platform's architecture, services, operating systems, governance, infrastructure, applications, and reference vocabulary. Its home page inherits Wikipedia's Main Page structural conventions — the gold standard for general-knowledge home pages — and extends that inheritance with capabilities Wikipedia's governance model has been structurally unable to ship.

This article explains the design intent: what is preserved from Wikipedia, what is added beyond it, and what engineering and financial-community readers each encounter when they arrive.

---

## Two readers, one home page

The home page serves two audiences simultaneously.

An engineering reader — an architect, a developer, a technical writer — wants depth, source authority, and machine-readable structure. A financial-community reader — an analyst, an auditor, an investor, a regulator — wants the substrate posture, the disclosure history, and the company structure in the same authoritative register as a regulatory filing.

Both audiences arrive at the same URL (`/`), see the same composition, and follow the same links into the corpus. The home page does not branch by audience. It serves both by inheriting Wikipedia's most load-bearing editorial commitment: the absence of marketing copy and the presence of editorial labour. Statements about the platform are structural ("9 categories", "N articles", "last updated YYYY-MM-DD"), not promotional.

---

## Wikipedia conventions preserved

Ten structural slots compose Wikipedia's English Main Page. The PointSav home page preserves the load-bearing primitives.

**Welcome banner.** Wikipedia opens with scope and community scale. The PointSav home page opens with scope ("PointSav's platform documentation covers the architecture, services, operating systems, and governance conventions of the PointSav substrate") and structural scale ("N articles across 9 categories, last updated YYYY-MM-DD"). Both are derived at render time, not authored as marketing copy.

**Featured article.** Wikipedia's Today's Featured Article enforces a 909–1,009 character blurb — character count, not word count. The PointSav home page preserves the format invariant: bolded linked title, body-register paraphrase of the article lead, "→ Read" closer. The featured article rotates as the editorial pipeline warrants; the current rotation cadence is weekly.

**Browse by category.** Wikipedia surfaces topics through its category system. The PointSav home page surfaces all nine ratified categories — architecture, services, systems, applications, governance, infrastructure, company, reference, help — in a 3×3 grid. The grid renders all nine even when a category is empty, so the platform's intended scope is visible at launch.

**Recent additions.** The top five articles by `last_edited` date, in descending order. The intent matches Wikipedia's Did You Know section: signal that the corpus is actively maintained and give returning readers a reason to return.

**Footer.** License, privacy, terms, contact, last-updated timestamp. No advertising, no newsletter signup, no affiliate links. The PointSav footer matches: CC BY 4.0 license notice and links to the source-of-truth GitHub repositories.

The blue link colour, sans-serif headings, the absence of bold except for article titles, the column grammar, and the density-without-clutter target (15–25 independently navigable units above the fold) are all inherited directly.

---

## Extensions beyond Wikipedia

Five primitives extend Wikipedia's home-page composition. Three are available in the current iteration. Two are planned for later iterations.

### Machine-readable slot structure

Wikipedia's home page has no structured data describing its slots. The PointSav home page emits JSON-LD per slot — the featured-article slot as a typed `Article` reference, the recent-additions slot as an `ItemList`, the category grid as a typed `WebPageElement` collection. Downstream consumers — feed readers, voice interfaces, language models — receive structure rather than prose to infer.

### Editorial-labour cadence as visible signal

The home page surfaces editorial labour cadence through the "last updated" timestamp in the welcome banner (derived from the maximum `last_edited` across the corpus), the rotating featured article, and the recent-additions feed. A future iteration is intended to rank the recent-additions feed by `content_reviewed_on` — a separate frontmatter field denoting last editorial review — rather than by recency of edit. Substantive content review, not cosmetic edits, would signal freshness.

### Editor-as-onramp signal

An "Other areas" block links to GitHub source repositories and to the design-system, governance, and contribution-onboarding articles. The path from reader to contributor is visible from the home page and is one click away.

### Per-section research-trail aggregate (planned)

The article shell ships a research-trail footer showing each article's editorial epistemic frontier — research done, suggested research, open questions. The home page is intended to surface an aggregate widget: "Open editorial questions across the corpus: N". This widget is planned for a future iteration, once the article-level research-trail discipline is widely adopted.

### Citation-graph entry point (planned)

The home page is planned to include a citation-graph entry point, allowing a reader to explore the corpus's knowledge graph as a visual surface — typed nodes, weighted edges, and red-link gaps visible as unrealised nodes. This is planned after the Phase 4 redb wikilink graph ships and the corpus reaches the size where graph traversal pays off the editorial cost (target: 200 or more articles).

---

## What the home page deliberately omits

The home page does not display advertising, collect newsletter signups, invoke marketing copy, branch by audience, surface social-media share buttons, or present calls-to-action. Engagement metrics (article views, edit counts, contributor leaderboards) are not presented at the home-page surface.

Each absence is intentional. A home page optimised for conversion or engagement signals to readers that they are reading marketing rather than reference. Wikipedia's home page contains no adjectives of self-description. The PointSav home page inherits the discipline directly.

---

## Forward-looking items

The following are planned or intended, not committed. Cautionary language applies per [ni-51-102] and [osc-sn-51-721]. Material assumptions include sustained editorial labour cadence and operator clearance of each phase.

The platform is intended to reach the structural standard required by major design and editorial-publishing awards in the reference and information-design categories. Whether any specific recognition results depends on factors outside the platform's control — submission timing, jury composition, competitive entries — and no specific award is claimed here.

---

## See Also

- [[app-mediakit-knowledge]]
- [[wikipedia-leapfrog-design]]
- [[wiki-component-library]]
- [[language-protocol-substrate]]
