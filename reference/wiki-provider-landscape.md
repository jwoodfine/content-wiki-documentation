---
schema: foundry-topic-v1
title: "Wiki provider landscape — what the 2026 wiki, knowledge-base, and documentation field looks like"
status: published
category: reference
last_edited: 2026-04-30
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
research_done_count: 25
research_suggested_count: 4
open_questions_count: 1
research_provenance: web-fetch + web-search across 25 providers + workspace-direct-consultation, 2026-04-30
research_inline: false
cites:
  - ni-51-102
  - osc-sn-51-721
---

The PointSav documentation wiki at `documentation.pointsav.com` is one entrant in a field where twenty-five distinguishable providers ship some variation of "wiki-shaped knowledge surface" in 2026. Most of them are not encyclopedic-knowledge platforms; they are private-team productivity tools, developer-documentation site generators, or personal-knowledge networked-thought systems. None of them has replaced Wikipedia for general-knowledge encyclopedic depth. This TOPIC documents the field, names the structural reasons no provider has closed the gap, and identifies the genuine advantages each provider has over Wikipedia — features worth preserving as the substrate iterates.

The audit is structural, not promotional. Each provider is described factually with its strongest published positioning and the structural limitation that prevents it from filling the encyclopedic-knowledge gap. The conclusion is not a claim that any single provider wins; it is that the gap is structural and is not closing under the current commercial-incentive structure of the wiki market.

## The four groups

Twenty-five providers in four groups by their target use case.

- **Group A — Collaborative knowledge bases**: Notion, Confluence, Coda, ClickUp Docs. Built for private organisational knowledge management. Sell seat licences to enterprise IT.
- **Group B — Public-facing wiki engines**: Wiki.js, BookStack, Outline, MediaWiki (what Wikipedia runs on), Fandom, Wikidot, DokuWiki, TiddlyWiki. The closest in shape to a Wikipedia-class platform; widest variance in editorial governance.
- **Group C — Developer documentation site generators**: Docusaurus, MkDocs Material, VitePress, Nextra, Fumadocs, Astro Starlight, GitBook, Read the Docs. Generate docs sites for software projects; static-site-first; collaborative-editing-second or none.
- **Group D — Personal and networked-thought tools**: Obsidian Publish, Roam Research, Logseq, Capacities, Quartz v4. Single-author personal-knowledge-management primarily; some publish surfaces.

## Per-provider descriptions

### Notion (notion.com)

In 2026 Notion is an enterprise productivity suite with Custom Agents, autonomous Q&A routing, and integration across Gmail, Slack, GitHub, and HubSpot. The article shell is a free-form block canvas: headings, callouts, toggles, inline databases — no fixed structure and no enforced schema. The encyclopedic-depth gap is categorical: Notion has no canonical article namespace, no red-link discovery, no Talk-page editorial debate, no Neutral Point of View policy, no notability gate, and no footnote-citation infrastructure where references are load-bearing rather than decorative. A Notion knowledge base degrades to informal, inconsistent prose at scale because there is no editorial constitution enforcing it.

### Confluence (atlassian.com/software/confluence)

Confluence in 2026 is an AI-powered workspace backed by Atlassian's Gartner Magic Quadrant Leader designation. The article shell is a Confluence page in nested spaces with structured templates. Reviewer consensus: native search returns broad, poorly-ranked results; without governance, pages sprawl and go stale; simultaneous-edit conflicts corrupt content. At encyclopedic scale Confluence has no equivalent of Wikipedia's category graph, "What links here," or Manual of Style — the knowledge graph is a flat filing cabinet rather than a navigable semantic network.

### Coda (coda.io)

Coda is "Your all-in-one collaborative workspace" combining docs, databases, and applications. The article shell blends document and spreadsheet — tables, buttons, formulas, and automations co-exist on a page. The encyclopedic-depth gap: Coda's structural power is relational (cross-doc formulas, synced tables) — useful for project tracking, but creates no stable article topology. There is no article schema discipline, no citation surface, no Talk-layer, and no discovery mechanism beyond search.

### ClickUp Docs (clickup.com/features/docs)

ClickUp positions Docs as contextual knowledge management embedded in task and project management. The article shell is a nested-pages rich text editor with task-embedding. The encyclopedic gap is structural by design: docs live inside projects and inherit project context; there is no concept of a standalone encyclopedic article. Real-time collaboration degrades above five concurrent editors.

### Wiki.js (js.wiki)

Wiki.js is self-hosted Node.js, Markdown / visual / HTML editors, with storage backends including Git, AWS, Azure, and 50+ authentication integrations. Encyclopedic gap: Wiki.js has the right bones (version history, multi-language, wikilinks) but ships no editorial governance layer — no NPOV policy, no notability criteria, no Manual of Style enforcement, no Talk-page infrastructure in the Wikipedia sense, and no red-link system. A capable authoring engine that requires an editorial culture to be built entirely from scratch on top.

### BookStack (bookstackapp.com)

BookStack is self-hosted PHP/Laravel, MIT licensed, content organised in Books → Chapters → Pages. The article shell is a WYSIWYG page in a rigid three-tier hierarchy. The hierarchical model is the central limitation at encyclopedic scale: Wikipedia's article graph is a flat namespace with a category overlay, not a tree. Knowledge does not respect a single hierarchy. BookStack works well for documentation with clear ownership but collapses under cross-cutting topics that belong to multiple conceptual parents simultaneously.

### Outline (getoutline.com)

Outline is team-oriented with real-time multiplayer editing, AI-powered search, Slack integration, cloud or self-hosted. The article shell is a block editor with Markdown and slash commands. The encyclopedic gap mirrors Notion's: Outline is a private-team tool with no public-epistemics layer. No citation surface, no Talk-page equivalent, no category graph, no red-link system.

### MediaWiki (mediawiki.org)

MediaWiki is the reference implementation — Wikipedia's engine. Structural primitives: flat article namespace; `[[wikilink]]` with red-link signalling; category graph; Talk: namespace per article; Special:Random; Special:WhatLinksHere; Special:RecentChanges; full revision history; Wikidata integration; citation template system where references are structurally load-bearing. The platform runs "tens of thousands of websites." The 2026 gap is the opposite of competitors: it has the structural depth, but a 2000s-era UX that new contributors find hostile.

### Fandom (fandom.com)

Fandom is a MediaWiki-based platform hosting fan wikis for games, film, TV, and entertainment properties. The article shell is MediaWiki with Fandom-specific extensions: interactive maps, Table Progress Tracking, Game Companion tools. Encyclopedic gap: Fandom inherits MediaWiki's structural depth but deploys it inside an ad-supported commercial context, driving the ongoing migration of communities to independent wikis. Audience and scope are fanbase-specific rather than general.

### Wikidot (wikidot.com)

Wikidot is a cloud-hosted wiki-site builder with 106 million pages, 10.3 million registered users, and 24,653 daily edits, on a freemium model. Encyclopedic gap: stagnation. No significant platform updates in years; non-standard syntax; community ecosystem fragmented. Notable deployments maintain their own editorial cultures independent of platform tooling.

### DokuWiki (dokuwiki.org)

DokuWiki is a flat-file PHP-based wiki platform that stores content in plain text files rather than a database — easy to back up, version-control externally, and migrate. Preferred for intranet technical documentation among sysadmin communities. Encyclopedic gap: flat-file storage without structured metadata or semantic graph means cross-article discovery is search-only. No category graph, no red links, no Talk pages in the MediaWiki sense.

### TiddlyWiki (tiddlywiki.com)

TiddlyWiki v5.4.0 is "a non-linear personal web notebook" — self-contained, single-HTML-file knowledge system. The fundamental primitive is the tiddler (an atomic note); structure is entirely graph-based via linking. The UX is maximally personal and maximally unfamiliar to new readers. No concept of a public-facing article optimised for readers who are not the author.

### Docusaurus (docusaurus.io)

Docusaurus is Meta's React/MDX-based static site generator for open-source projects and technical documentation teams. The article shell is an MDX page rendered to static HTML with sidebar navigation, versioning, and Algolia search. Encyclopedic gap: Docusaurus generates a docs site, not a wiki. No inter-article linking discovery, no red links, no Talk pages, no category graph, no collaborative in-browser editing. Every Docusaurus site looks structurally identical because it ships a single enforced layout.

### MkDocs Material (squidfunk.github.io/mkdocs-material)

MkDocs Material is Python-based with 50,000+ users, instant browser-side search, responsive layout, extensive theming. Entered maintenance mode November 2025 — bug fixes and security patches continue, no new features. Same encyclopedic gap as Docusaurus: docs site, not wiki. Navigation primitive is a fixed sidebar tree which cannot represent a multi-parent category graph.

### VitePress (vitepress.dev)

VitePress is Vue/Vite-powered with hot-reload. Powers Vue's own documentation. Encyclopedic gap: same category as Docusaurus. "Beautiful docs in minutes" optimises for designer-smooth surfaces rather than structural rigour.

### Nextra (nextra.site)

Nextra is built on Next.js and MDX — the Next.js-ecosystem equivalent of Docusaurus. Server Components and ISR support give it rendering flexibility beyond typical static generators. Encyclopedic gap: developer documentation tool with no wiki primitives.

### Fumadocs (fumadocs.dev)

Fumadocs is a React.js documentation framework for component libraries and developer tools, with minimal aesthetics and headless customisation. Encyclopedic gap: explicitly positioned at component-library documentation; no public-wiki primitives, no editorial governance surface, no reader-navigation affordances beyond sidebar and search.

### Astro Starlight (starlight.astro.build)

Starlight is Astro's documentation site builder with built-in i18n, search, dark mode, sidebar, and accessibility focus. Encyclopedic gap: same category as Docusaurus and VitePress. The accessibility emphasis is a floor requirement, not a differentiator for encyclopedic depth.

### GitBook (gitbook.com)

GitBook in 2026 has pivoted to "AI-ready docs" and "knowledge system" language, positioning it against internal company knowledge tools rather than public encyclopedias. Encyclopedic gap: closed-source, commercially oriented, migrated away from open-source roots. No Talk-page model, no red-link mechanism, no NPOV policy surface, no category graph.

### Read the Docs (about.readthedocs.com)

Read the Docs is documentation hosting and build-automation supporting Sphinx, MkDocs, Docusaurus, Jupyter Book, and others. Encyclopedic gap: an infrastructure platform, not a knowledge-graph engine. Solves the CI/CD problem for documentation but adds nothing to article-structure, editorial-governance, or navigation-primitive dimensions.

### Obsidian Publish (obsidian.md/publish)

Obsidian Publish converts local Obsidian vaults into public-facing sites with hover previews, stacked pages, backlinks, and graph view. The article shell is a Markdown note with `[[wikilinks]]` and frontmatter — structurally the closest of any Group D tool to Wikipedia's article model. Encyclopedic gap: single-author publication tool, not a multi-author collaborative wiki. No collaborative in-browser editing, no Talk-page discussion layer, no NPOV enforcement, no notability gate, no community moderation infrastructure.

### Roam Research (roamresearch.com)

Roam Research is "A note taking tool for networked thought" — the originator of the modern bidirectional-link paradigm. By 2026 Logseq has absorbed most of Roam's market. The article shell is a page of nested bullets with `[[wikilinks]]` and block references, optimised for the author's non-linear associative workflow. Encyclopedic gap: a personal thought-capture tool. The structural model is explicitly anti-encyclopedic — no article-length atomic unit, no concept of a reader who is not the author.

### Logseq (logseq.com)

Logseq is local-first, open-source, block-based, with bidirectional links, graph view, Org-mode/Markdown support. In 2026 "the better choice" over Roam due to free tier and open codebase. Encyclopedic gap: same as Roam. The block-outline model is a personal-knowledge primitive, not an encyclopedic-article primitive.

### Capacities (capacities.io)

Capacities is a personal knowledge management system built on typed objects rather than files in folders. Object-based relationship modelling surfaces connections automatically. The article shell is a typed object with properties, linked to other typed objects — the most semantically rich data model in Group D. Encyclopedic gap: explicitly individual-focused; no collaborative editing, no public-epistemics model, no article-level citation infrastructure, no community governance layer.

### Quartz v4 (quartz.jzhao.xyz)

Quartz v4 transforms Markdown content into fully functional websites — targeting students, developers, and teachers publishing personal notes and digital gardens. Ships graph view and backlinks natively (more than most competitors) but no collaborative editing, no Talk-page layer, no notability mechanism, no NPOV infrastructure, no red-link system.

## Cross-cutting failure modes

The eight structural reasons no provider in this audit has replaced Wikipedia for general encyclopedic knowledge:

**(i) Audience mismatch.** Notion, Confluence, Coda, ClickUp, Outline, BookStack were built for private organisational knowledge management. Access-control model, pricing model, and UX assume a known trusted team. Public-encyclopedic publishing requires the opposite — anonymous editors, verifiable sourcing, reader-first navigation. These products cannot pivot without dismantling their commercial model.

**(ii) No editorial constitution.** Wikipedia's NPOV, Notability, Reliable Sources, No Original Research, and Manual of Style constitute a multi-decade-refined editorial constitution. No provider in this audit ships an equivalent. The absence is a missing governance organisation, not a missing feature.

**(iii) Information density floor.** Docusaurus, MkDocs, VitePress, GitBook, and Obsidian Publish optimise for prose elegance, developer aesthetics, and clean typography. Wikipedia articles are deliberately dense — infoboxes, hatnotes, references with 100+ footnotes, navboxes, stub tags, disambiguation pages. No documentation site generator ships this density model because target users actively want the opposite.

**(iv) Navigation primitive missing.** Wikipedia's navigation stack — `[[wikilink]]` with red-link signalling, Special:Random, Special:WhatLinksHere, category graph, disambiguation pages, navbox templates, sister-project interlinking — exists complete in MediaWiki and at most one or two members elsewhere. Most competitors do not even ship the red-link mechanism, which is structural to Wikipedia's growth model.

**(v) Citations are decorative, not load-bearing.** Wikipedia's footnote system makes claims verifiable at the statement level. Across Group A, C, and D providers, citations are absent entirely, implemented as inline hyperlinks with no formal structure, or supported as page-level frontmatter rather than claim-level.

**(vi) No Talk-page substrate.** Each Wikipedia article has a Talk: page that is the public record of editorial dispute. Confluence and Notion have inline comments — not archived public editorial debate.

**(vii) Structural brittleness.** Notion's block format, Coda's pack structure, ClickUp's embedded docs are proprietary serialisation formats. Content created in 2020 is at vendor lock-in risk by 2026. Wikipedia's wikitext is plain text that can be exported, archived, and mirrored.

**(viii) Template homogenisation.** Every Docusaurus, Starlight, VitePress, and MkDocs site looks structurally identical. This is the documentation aesthetic every engineering team knows. It is also what a Wikipedia reader does not associate with encyclopedic authority.

## What each provider does better than Wikipedia

The honesty floor of the audit. Each provider has a genuine advantage over Wikipedia in some dimension:

| Provider | Genuine advantage |
|---|---|
| Notion | Inline @-mentions linking people, tasks, dates inside prose; database-as-page model embedding live structured data |
| Confluence | Macro ecosystem for dynamic content embedding (Jira ticket status, roadmaps); enterprise SSO and granular permissions |
| Coda | Cross-document formula language: relational knowledge made visible without a separate database |
| ClickUp Docs | Contextual attachment: docs live adjacent to the tasks they describe |
| Wiki.js | Git-backed storage: every article version is a git commit, fully portable and diffable with standard tooling |
| BookStack | Operational simplicity: runs on a $2.50 VPS with single PHP install — lowest cost-to-first-article of any self-hosted wiki engine |
| Outline | Real-time multiplayer editing with operational-transform conflict resolution; smoother concurrent editing than MediaWiki's section-locking |
| MediaWiki | Everything that is the benchmark — full navigation primitive stack, NPOV enforcement, category graph, Talk pages, Wikidata integration |
| Fandom | Interactive maps and progress-tracking tables embedded natively in wiki articles; best media-gallery integration |
| Wikidot | Community-site builder supporting custom CSS per wiki + sub-wikis under a shared domain |
| DokuWiki | Zero-database flat-file storage — most portable, least infrastructure-dependent knowledge store |
| TiddlyWiki | Single-file portability — entire knowledge base is one HTML file; extreme durability |
| Docusaurus | MDX: React components embedded in Markdown enabling interactive documentation (live code playgrounds, API sandboxes) |
| MkDocs Material | Instant client-side search with offline support and zero external dependencies; fastest search-to-result |
| VitePress | Hot-module reload during authoring: sub-second preview updates as you write |
| Nextra | Server Components: docs pages can fetch live data at render time |
| Fumadocs | Headless architecture: complete design-system override without forking |
| Astro Starlight | Island architecture: zero JavaScript shipped by default; best Lighthouse scores |
| GitBook | Git bidirectional sync: write in IDE or visual editor; both stay synchronised |
| Read the Docs | PR preview builds with visual diffs |
| Obsidian Publish | Graph view with hover-preview; most visually legible representation of a personal knowledge graph |
| Roam Research | Block-level transclusion: any block embeddable by reference into any other document |
| Logseq | Free + open-source + local-first with bidirectional links — the combination Roam never offered |
| Capacities | Typed objects with automatic relationship discovery — closest to a semantic knowledge graph |
| Quartz v4 | Native Obsidian vault publishing with wikilinks, popover previews, and graph view in a static site |

Three of these advantages are particularly worth integrating into a Wikipedia-class chrome without breaking the muscle-memory contract: MkDocs Material's instant client-side search; Capacities' typed-object relationship surface rendered as navigable article metadata; and Obsidian Publish's hover-preview popover on `[[wikilinks]]`.

## Why the gold-standard market gap exists in 2026

The gap is structural and has five reinforcing causes.

**Commercial incentive misalignment.** Notion, Confluence, GitBook, Coda, and ClickUp make money by selling seat licences to organisations managing internal knowledge. Their roadmaps are driven by enterprise IT buyers — investing in NPOV enforcement, Talk-page infrastructure, or red-link discovery does not convert to enterprise seat revenue.

**The editorial-labour problem cannot be automated.** Wikipedia's structural authority is twenty years of accumulated editorial labour. AI-generated content cannot replicate the transparent editorial process, source verification standards, or community governance that make Wikipedia trusted. Replicating the credibility surface requires replicating the governance — and no commercial entity has bootstrapped that from a product launch.

**Open-source coordination cost.** MediaWiki's codebase is 25 years old, carries enormous legacy compatibility surface, requires Wikimedia Foundation resources to maintain. No independent open-source project has shipped a "MediaWiki v2 with modern UX" because the coordination cost is prohibitive.

**Scope creep on one side, narrow scope on the other.** Group A providers expanded into "everything platforms"; their knowledge-base features compete with AI agents, project management, and enterprise integrations. Group C providers are deliberately minimal static-site generators — no collaborative editing model by design.

**The Wikipedia muscle-memory gap.** No competitor has invested in replicating the specific reader-navigation UX billions of Wikipedia users know by reflex. This is an information-architecture commitment, not a CSS problem. Documentation sites ship sidebars because their readers navigate a product's API. Encyclopedia readers arrive from search, orient via the infobox, follow blue links sideways, and exit via categories.

## What this means for documentation.pointsav.com

Closing the gap requires simultaneously building governance software, a navigation primitive set, and an editorial culture. The PointSav substrate-sovereignty posture, three-tier compute routing under the optional intelligence layer, apprenticeship-corpus capture, and the editorial pipeline (project-language gateway with the reverse-funnel pattern and research-trail discipline) are the preconditions the five structural causes above require.

The wiki engine `app-mediakit-knowledge` becomes the customer-installable demonstration of that substrate. The structural argument for the leapfrog claim is what this TOPIC documents: the gap exists because of the five structural causes above; closing it requires those preconditions; the substrate has those preconditions as design intent. The award framings in [[knowledge-wiki-home-page-design]] §5 and [[article-shell-leapfrog]] §5 are the planned downstream consequences, not delivery commitments.

## Open editorial item

This audit was conducted 2026-04-30 with web-fetch primary research across all 25 providers. Provider positioning shifts; periodic re-audit (annual cadence is planned) is required to keep this TOPIC current. The next re-audit is intended for approximately 2027-04. If a provider in this list ships a structural change between audits — for example, MediaWiki ships a 21st-century UX layer, or Wiki.js adds NPOV-style editorial discipline — this TOPIC is amended in transit; the change is logged in the article's research trail.

## See also

- [[knowledge-wiki-home-page-design]] — The home page design intent and award competitive framing.
- [[article-shell-leapfrog]] — The article-shell leapfrog primitives that pair with the competitive analysis here.
- [[wikipedia-leapfrog-design]] — The design narrative behind the 95%/5% muscle-memory contract.
- [[substrate-native-compatibility]] — Why the substrate ships its own surface rather than adapting an existing provider.

## Provenance

Authored 2026-04-30 by a project-knowledge Task Claude session (Opus parent synthesis from Sonnet sub-agent C report that conducted web-fetch primary research across all 25 providers). Refined by project-language, 2026-04-30. This TOPIC is structural competitive analysis — its purpose requires naming providers and describing their limitations factually, consistent with workspace `CLAUDE.md` §6 "Structural positioning (no competitive comparison)": each provider is described factually with its strongest positioning and named genuine advantages; PointSav's substrate is framed structurally, not as a "winner" claim.

Forward-looking framings follow [ni-51-102] and [osc-sn-51-721] continuous-disclosure posture. Material assumptions: the substrate's governance and editorial preconditions remain on the design trajectory described in Foundry DOCTRINE.md and workspace NEXT.md.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
