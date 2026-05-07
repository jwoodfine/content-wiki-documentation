---
schema: foundry-doc-v1
title: "Knowledge Wiki Leapfrog Architecture"
slug: knowledge-wiki-leapfrog-architecture
category: architecture
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-07
editor: pointsav-engineering
cites: []
paired_with: knowledge-wiki-leapfrog-architecture.es.md
---

`app-mediakit-knowledge` is the PointSav knowledge platform engine, a Rust binary that serves three wiki instances — `documentation.pointsav.com`, `projects.woodfinegroup.com`, and `corporate.woodfinegroup.com` — from flat Markdown files stored in git repositories. The engine renders content with Wikipedia-shaped chrome: sticky table of contents, wikilink resolution with red-link signalling, category pages, edit history, and full-text search. As of May 2026, it implements approximately 78 percent of the full Wikipedia muscle-memory surface. A planned multi-sprint roadmap is intended to bring that figure to approximately 95 percent before adding a Leapfrog 2030 differentiation layer that goes beyond what Wikipedia offers.

## Why not port MediaWiki

MediaWiki is the software that runs Wikipedia. Porting it to Rust would not serve the platform's goals.

MediaWiki was designed in 2003 for a PHP-and-MySQL stack. Its parser — the component that converts wikitext into HTML — was described by its original author as "a huge pile of regular expressions." The Parsoid project, MediaWiki's attempt to replace that parser with a clean bidirectional HTML↔wikitext converter, took ten years to ship and is still completing its rollout as of 2025.

The wikitext template system is the core of MediaWiki's content richness — infoboxes, navboxes, citation templates, and geographic coordinate templates are all implemented as wiki pages in the `Template:` namespace, processed by a recursive macro expansion interpreter that calls back into the database during parsing. This design couples the parser to the database, complicates caching, and makes the system difficult to run without MySQL.

The architectural goal of `app-mediakit-knowledge` is not to replicate this design but to achieve the same reader experience through a fundamentally different stack. The content format is Markdown with YAML frontmatter, not wikitext. Version control is git, not a MySQL revision table. The search backend is Tantivy — embedded, zero operational overhead — not an Elasticsearch-backed cluster. Template transclusion is replaced by six native block types that cover the vast majority of what templates are actually used for on Wikipedia.

## MediaWiki architecture, understood

MediaWiki's namespace system defines 30 namespaces in two axes: subject pages (Article, User, File, Template, Category, Help, Module, Draft) paired with Talk pages. Special pages form a separate class of software-generated pages with no talk equivalent.

The Vector 2022 skin divides every page into: a sticky header (logo, search, language switcher, personal tools), a left sidebar (navigation menu and table of contents), an article header (namespace tabs, view tabs, title, short description, hatnotes), the article body (infobox floated right, body text, tables, images, footnote superscripts), an appendix (See also, References, External links), navboxes, category strip, and a footer (last-edited timestamp, licence, legal links).

The Cite extension handles footnotes: `<ref>citation text</ref>` in the article body inserts a numbered superscript; `<references/>` at the section bottom renders the numbered list. Reference Tooltips — a JavaScript gadget — shows citation text on hover without requiring the reader to scroll.

These elements constitute the muscle memory that Wikipedia readers have developed over two decades. A wiki missing the infobox, the sticky TOC, the `[1][2][3]` footnote superscripts, or the navboxes does not feel like Wikipedia regardless of how good its content is.

## Current feature state

As of May 2026, `app-mediakit-knowledge` implements approximately 78 percent of the full Wikipedia muscle-memory surface. The following elements are fully operational:

- Wikilinks with blue/red distinction (existing articles link blue; missing articles link red)
- Sticky collapsible table of contents, Vector 2022 pattern
- Read / Edit / View History tabs and per-section edit pencils
- Article/Talk tabs (Article tab functional; Talk tab is a functional stub)
- Full-text search via Tantivy BM25
- Edit history, blame, and unified diff via git
- CodeMirror 6 editor with citation autocomplete and SAA squiggle linting
- Quality badges (complete / core / stub) and stub notice
- Category pages and category strip at article bottom
- Home page with 3×3 category grid, featured article pin, and leapfrog facts panel
- Atom 1.0 and JSON Feed 1.1 syndication
- Hover card page previews
- Glossary auto-linker with tooltips
- Authentication and edit review queue
- Read-only git remote (smart-HTTP protocol)
- MCP server (JSON-RPC 2.0) for agent integration
- Notify-based incremental search reindex
- Mobile hamburger navigation

The following elements are stubbed or absent, ranked by muscle-memory impact:

| Missing feature | Impact | Notes |
|---|---|---|
| Infobox (structured right-column summary) | 9/10 | Most recognisable Wikipedia element; absent entirely |
| Navbox (bottom navigation template) | 8/10 | Creates topic clusters; absent entirely |
| Citation `[1][2][3]` CSS rendering | 8/10 | Footnotes parse correctly; CSS unstyled |
| Citation hover tooltip | 8/10 | JavaScript gadget not yet written |
| Two-column word-level diff | 7/10 | Unified diff exists; two-column Wikipedia style absent |
| Talk/Discussion pages | 7/10 | Tab renders as disabled; no backend |
| Redirects | 6/10 | No `redirect_to` frontmatter processing |
| Disambiguation pages | 6/10 | No page type flag or chrome |
| Special:RecentChanges | 6/10 | Git log data exists; HTML page absent |
| Special:AllPages | 5/10 | Article list endpoint absent |
| `/random` article | 5/10 | Absent |
| Edit summary field | 5/10 | Git commit message populated from author and time only |
| Definition lists | 4/10 | comrak extension disabled; one-line fix |

## The native block types approach

Rather than implementing a wikitext macro expansion engine, `app-mediakit-knowledge` is designed to use six native block types as fenced code blocks parsed during the comrak AST walk. These are intended to cover the vast majority of what Wikipedia templates are actually used for.

**Infobox** — a YAML-body fenced block intended to render as a `<table class="infobox">` floated at the right margin of the article. The author writes:

````markdown
```infobox
name: PointSav Digital Systems
founded: 2024
jurisdiction: British Columbia, Canada
sector: Enterprise software
```
````

The engine walks the comrak AST, matches `CodeBlock` nodes with `info = "infobox"`, parses the YAML body, and replaces the node with an `HtmlInline` table. No template database, no macro expansion, no Lua interpreter.

**Navbox** — a similar fenced block intended to render a collapsible horizontal table at the article bottom, grouping related article links under a shared title. JavaScript collapses navboxes when two or more appear on the same page, matching Wikipedia's `autocollapse` behaviour.

**Cite block** — inline citation syntax (`[^id]` with `[^id]: text` at article bottom) that the comrak footnotes extension already parses. The remaining work is CSS styling and a JavaScript hover tooltip.

Implementing the infobox and navbox block types requires upgrading comrak from version 0.29 to 0.52 as a planned step. The newer version adds the `block_directive` extension (`:::infobox`, `:::navbox` syntax), which is cleaner than fenced code blocks for multi-line Markdown content inside the block body. The API is stable across these versions.

## The Leapfrog 2030 layer

Wikipedia muscle memory is the floor, not the ceiling. Once `app-mediakit-knowledge` achieves full Wikipedia parity, three planned first-class primitives are intended to distinguish it from incumbent alternatives.

**Citation Authority Ribbon** — a planned per-article visual indicator of source verification status. Inline citations resolved against `citations.yaml` are intended to display a coloured ribbon: green for verified, amber for unverified, red for contested. Wikipedia has no equivalent; all citations are treated as equally reliable regardless of their actual verification state.

**Research Trail Footer** — every article declares five frontmatter fields (research method, depth, confidence, date, limitations) intended to be rendered as a collapsible footer section. This would make the provenance of every claim visible to readers, supporting NI 51-102 continuous-disclosure obligations for regulated issuers. Wikipedia has talk-page archives and edit history but no structured research provenance at the article level.

**AI-integrated editor** — the CodeMirror 6 editor includes a three-keystroke ladder: Tab (complete the current sentence), Ctrl+K (ask a question about the content), Alt+J (insert a citation). These affordances are planned to call `app-orchestration-command` via the Doorman proxy. They are currently stubbed as 501 endpoints, pending service-slm operationalisation. When activated, they are intended to provide author assistance that traditional wiki editing surfaces do not offer.

**BCSC squiggle linting** — the editor currently enforces seven deterministic SAA rules via coloured underlines. The planned complete set includes forward-looking statement detection, Do-Not-Use vocabulary flagging, Sovereign Data Foundation current-tense detection, competitive comparison flagging, and citation-required prompts. This is built into the editing surface rather than applied as a post-publication compliance check.

## Structural positioning

Incumbent wiki platforms built on hierarchical organisation models — books, chapters, spaces, folders — break the flat hyperlink graph that makes Wikipedia useful. A hierarchical wiki creates knowledge silos; a flat wiki with a category DAG creates a knowledge commons.

Platforms that impose hierarchical organisation typically lack redlinks (the signal that a page is missing and should be created), backlinks, navboxes, and the full Special pages framework. Several lack talk pages entirely.

`app-mediakit-knowledge` is designed as a Rust-native, git-backed, flat-file wiki engine targeting full Wikipedia muscle memory for regulated SMBs operating under continuous-disclosure obligations.

## See also

- [[app-mediakit-knowledge]] — application overview, deployment configuration, and phase roadmap
- [[leapfrog-2030-architecture]] — Leapfrog 2030 doctrine and eight-invention framework
- [[wikipedia-structure]] — Wikipedia article structure research: 16-element anatomy and infobox schemas
- [[compounding-substrate]] — the broader compounding pattern that the wiki leg implements
