---
schema: foundry-doc-v1
title: "MediaKit knowledge application"
slug: app-mediakit-knowledge
category: applications
type: topic
quality: complete
short_description: "app-mediakit-knowledge is the single-binary Rust wiki engine that serves PointSav's engineering documentation at documentation.pointsav.com — a view over a markdown tree, not a content repository, where the markdown commits are canonical and every running binary is a throwaway derived state."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: app-mediakit-knowledge.es.md
cites:
 - ni-51-102
 - osc-sn-51-721
 - c2sp-tlog-tiles
 - constitutional-ai-2212-08073
references:
 - id: 1
 text: "CommonMark Specification."
 url: "https://commonmark.org/"
 - id: 2
 text: "comrak — CommonMark-compliant Markdown processor in Rust."
 url: "https://github.com/kivikakk/comrak"
 - id: 3
 text: "Tantivy full-text search engine."
 url: "https://www.tantivy-search.org/"
 - id: 4
 text: "Schema.org TechArticle schema."
 url: "https://schema.org/TechArticle"
 - id: 5
 text: "Atom Syndication Format — RFC 4287."
 url: "https://datatracker.ietf.org/doc/html/rfc4287"
 - id: 6
 text: "JSON Feed Version 1.1."
 url: "https://www.jsonfeed.org/version/1.1/"
 - id: 7
 text: "llmstxt.org convention for LLM crawlers."
 url: "https://llmstxt.org/"
 - id: 8
 text: "Wikipedia Manual of Style — Layout."
 url: "https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Layout"
---

`app-mediakit-knowledge` is the single-binary Rust wiki engine that serves PointSav's engineering documentation at `https://documentation.pointsav.com`. The engine combines an `axum` HTTP server, a `comrak` CommonMark renderer[^1][^2] with platform-specific extensions for wikilinks, footnotes, table of contents, and section anchors, a `tantivy` full-text search backend[^3], and a `maud` templating layer with four article templates. The engine reads markdown files from a content directory the operator names at startup, renders them on demand into HTML, and returns them with caching headers tuned for a documentation audience.

The engine is a *view* over a markdown tree, not a content repository. The markdown tree is canonical; the running binary is a view that any number of operators can stand up over the same content tree, or different content trees, with no shared mutable state on the binary side. This source-of-truth inversion is the single most important design choice and is treated in detail in the next section.

The engine's first public deployment went live on 2026-04-27 at 16:25 UTC, serving a four-file placeholder content tree at `https://documentation.pointsav.com`. The full route surface from build phases 1, 1.1, 2, and 3 is operational; phases 4 through 8 are planned but not yet implemented.

## Source-of-truth inversion

The substrate's load-bearing design choice: **git is canonical; the running binary is a view; CRDT, when collaborative editing is enabled, is session-ephemeral**.

Every concrete artefact a reader encounters — the HTML page, the Atom feed entry, the JSON-LD block, the search-result hit, the wikilink graph — is derived at request time from the markdown tree on disk. The disk state is what gets committed, reviewed, replicated, and disclosed. The HTML is throwaway. The Tantivy index is throwaway, rebuilt from the markdown tree on startup. The redb wikilink graph (Phase 4) is throwaway. The collab CRDT (Phase 2 Step 7, default-off) is throwaway between sessions.

This inversion reverses the traditional MediaWiki model, where the database is canonical and the file system is a derived working copy. Here, the file system is canonical and the database (search index, link graph) is a derived working copy. The motivation is operational simplicity — a content-tree backup is a `git clone`; a content-tree replication is a `git pull`; a content-tree audit is a `git log` — and a substrate-level invariant: every published claim is a signed git commit; the disclosure record is the git history; the BCSC continuous-disclosure posture is enforced by structure rather than by policy alone.

Other patterns follow from the inversion. The wiki has no preview-then-publish workflow because the canonical state is what got committed; an edit committed is a publication. The wiki has no scheduled-publish workflow because the same property holds. The wiki has no server-side draft state because drafts live in the contributor's git working copy or in the editorial pipeline, not in a database the wiki engine owns.

## Route surface

The engine exposes a tight set of HTTP routes. Each is independent; no route depends on session state or on a database the engine owns.

| Route | Purpose | Phase |
|---|---|---|
| `/healthz` | Liveness check (returns the literal string `ok`) | 1 |
| `/` | Index page (lists all articles in the served content tree) | 1 |
| `/wiki/{slug}` | Rendered article HTML | 1 |
| `/static/{*path}` | Static assets (CSS, JS, fonts) | 1 |
| `/edit/{slug}` | In-browser editor (CodeMirror 6) | 2 |
| `POST /edit/{slug}` | Atomic-write edit endpoint with squiggle linting | 2 |
| `/search?q=` | Full-text search results (Tantivy / BM25) | 3 |
| `/feed.atom` | RFC 4287 Atom syndication feed[^5] | 3 |
| `/feed.json` | JSON Feed 1.1 syndication[^6] | 3 |
| `/sitemap.xml` | sitemaps.org compliant sitemap | 3 |
| `/robots.txt` | Crawler discovery | 3 |
| `/llms.txt` | llmstxt.org convention for LLM crawlers[^7] | 3 |
| `/git/{slug}` | Raw markdown source for git-clone-style ingestion | 3 |
| `/ws/collab/{slug}` | WebSocket passthrough relay (default-off behind `--enable-collab`) | 2.7 |

Phase 4 is planned to add `/history/{slug}`, `/blame/{slug}`, `/diff/{a}/{b}`, `/backlinks/{slug}`, an MCP server route, and a read-only Git remote over smart-HTTP — letting any git client clone the served content tree as a regular git repository, riding the existing TLS termination. Phases 5 through 8 are planned; cautionary language applies per [ni-51-102] and [osc-sn-51-721].

The engine emits JSON-LD `TechArticle`[^4] and `DefinedTerm` schema in every rendered article's `<head>` block for search-engine and crawler comprehension. The structured data is generated from the article's frontmatter, not hand-authored per page; the schema is the same shape across the corpus.

## Wikipedia muscle-memory chrome

The engine ships with a deliberately Wikipedia-recognisable chrome. A reader of any Wikipedia article will navigate the engine without prompting, and a reader unfamiliar with Wikipedia will pick up the patterns quickly because they are well-documented conventions.[^8]

What was kept (per `UX-DESIGN.md` §1):

- Article / Talk tabs at the top of the page (Talk tab present in the template; Talk discussion is reserved for a future implementation)
- Read / Edit / View history tabs alongside the Article/Talk pair
- Per-section `[edit]` pencils on every `## H2` and `### H3` heading
- End-of-article ordering: References, See also, Categories, with a footer band naming the article's licence and the substrate
- Hatnote band at the top of the article for disambiguation and cross-references
- Lead first-sentence convention (bolded subject plus copula plus definition)
- Tagline directly under the article title
- Collapsible left-rail table of contents (built from H2 and H3 headings; deeper headings render normally but do not enter the TOC)
- Language switcher (currently English / Spanish; structurally ready for additional languages without re-templating)

What was added beyond Wikipedia:

- Citation badges next to inline `[citation-id]` references, with hover-card showing the registry entry
- Forward-Looking-Information cautionary banner when an article's frontmatter sets `forward_looking: true`
- BCSC `disclosure_class` field expressed in the JSON-LD structured data in every rendered article's `<head>` block (not visible as default chrome; consequential when the Phase 8 linter activates)
- Information Verifiability Citation (IVC) masthead band placeholder (Phase 7 is intended to provide the verification machinery)
- Reader density toggle (compact / comfortable; settings persist client-side)

The chrome is implemented in four `maud` HTML templates (`article.html`, `category.html`, `search.html`, `editor.html`) and a CSS bundle that tracks Vector 2022's spacing and typography rather than its colour palette. The aim is muscle memory, not literal mimicry — a reader who knows Wikipedia recognises the layout, but the visual identity is distinct.

## Editor surface

The wiki's editor is a CodeMirror 6 instance vendored into the binary's static-asset bundle, served at `/edit/{slug}`. It supports markdown highlighting with line numbers, configurable line wrap, and undo/redo history, with atomic disk write via `POST /edit/{slug}`.

Three substrate-aware features distinguish the implementation:

**Squiggle linting (Phase 2 Step 4).** Seven deterministic rules flag editorial issues at typing time, each with a cited authority in a hover-card. The rules cover banned vocabulary, forward-looking framings without the cautionary-banner pattern, BCSC-discipline checks, and Bloomberg-article-standard register checks. The rules are deterministic at edit time; structured constrained decoding at inference time is intended to harden these into compile-time-equivalent guarantees once the service-slm Doorman ships the grammar-constraint integration.

**Citation autocomplete (Phase 2 Step 5).** Pressing `[` triggers a typeahead populated from the workspace citation registry. The contributor types `[ni-51` and the list narrows to `ni-51-102` (BCSC continuous disclosure) plus any other matches. Selecting an entry inserts the canonical `[citation-id]` form and adds the citation to the article's frontmatter `cites:` list automatically. The pattern keeps citation discipline cheap to follow and expensive to skip.

**Three-keystroke ladder for Doorman (Phase 2 Step 6 stubs).** Tab opens a ladder of "ask Doorman" affordances at the cursor position — find a citation, suggest a hatnote target, generate a disambiguation link, propose a section heading. These return 501 stubs in the v0.1.29 binary; Phase 4 is planned to wire them to the service-slm Doorman.

The editor's atomic-write semantics are conservative: the engine writes new file content to a temporary path in the same directory, fsyncs, and renames over the destination. A failed write is visible to the contributor and leaves the canonical content untouched. Concurrent edits from two non-collab sessions race at the rename step; the last-writer-wins convention is documented.

## Search, feeds, and ingestion

The engine indexes the content tree on startup and incrementally on edit. The index is on-disk Tantivy (BM25 by default) at `<state-dir>/search/`, rebuilt from the content tree if it is missing. The Tantivy `IndexWriter` is held in an `Arc<Mutex<>>` per the crate's typical pattern and released before reader reload to avoid the asynchronous-reload race.

Three syndication formats render the corpus to crawlers:

- **`/feed.atom`** — RFC 4287 Atom syndication. Each article is a feed entry with `title`, `summary`, `published`, `updated`, and the article's `cites:` list resolved against the registry.
- **`/feed.json`** — JSON Feed 1.1 syndication. Identical content shape to the Atom feed; format differs.
- **`/sitemap.xml`** — sitemaps.org compliant. Lists every article URL with its last-modified date.

Two crawler-discovery files round out the surface: **`/robots.txt`** and **`/llms.txt`**. The `/git/{slug}` route serves raw markdown source. A crawler or a future federation peer can ingest the content tree by following `/llms.txt` to discover the article list, then fetching `/git/{slug}` for each article's source. The route accepts an optional `.md` suffix for tools that expect markdown URLs to end in `.md`.

## Real-time collaboration

The engine optionally supports real-time collaborative editing via the Yjs CRDT. The feature is default-off behind the `--enable-collab` CLI flag; the production deployment at v0.1.29 does not enable it.

The implementation follows the source-of-truth inversion: **the server is a passthrough WebSocket relay, not a Yjs server**. Yjs document state never lives on the server. The relay is a thin `tokio::sync::broadcast` per-slug room with a 256-message lag buffer; clients send Yjs update packets, the server forwards them to other clients in the room, and persistence flows through the existing `POST /edit/{slug}` save path on deliberate save. When all clients leave the room, the room closes and any unsaved CRDT state is discarded.

A long-lived Yjs document on the server would create a parallel canonical record that drifts from git, complicates audit, and conflicts with the BCSC disclosure posture. The passthrough relay keeps git canonical and the CRDT session-ephemeral.

The client lazy-loads `cm-collab.bundle.js` (302 KB) only when the template's `window.WIKI_COLLAB_ENABLED` flag is set by the server, so production deployments without `--enable-collab` never load any Yjs JavaScript. A manual two-client smoke test (two browsers editing the same article, seeing each other's cursors) is the current ratification path for cursor-rendering UX, which is a visual property that is awkward to assert programmatically.

## Substrate-native compatibility surface

The engine is a substrate-native wiki, not a MediaWiki shim. This reflects architectural decisions ratified at workspace v0.1.10 and refined at v0.1.14.

What was kept: the **`xml-dump` import path** for one-time corpus migration; **URL conventions** (`/wiki/{slug}`); **wikilink syntax** (`[[slug]]` and `[[slug|display text]]`); **footnote syntax** (`[^1]`).

What was dropped: the **MediaWiki Action API shim** — the shim was scoped at v0.1.10 and dropped at v0.1.14 because maintenance scales with MediaWiki's velocity and compliance audit scales with the API surface. The substrate-native API surface (article HTML, JSON-LD, Atom, JSON Feed, sitemap, llms.txt, raw markdown via `/git/{slug}`, search via `/search?q=`, edit via `POST /edit/{slug}`) covers the same use cases without a parallel authoritative interface requiring separate maintenance. **MediaWiki templates and parser functions** were dropped because the engine's rendering path is CommonMark with PointSav-specific extensions, not a MediaWiki parser. **The pywikibot ecosystem** was dropped because the substrate's automation path is the existing workspace tooling, not the pywikibot framework.

The trade-off is a narrower compatibility surface against a substrate-coherent posture. A reader migrating from a MediaWiki deployment loses templates and the Action API; gains source-of-truth inversion, deterministic rendering, BCSC-grounded disclosure posture, and a smaller attack surface.

A separate sibling article ([[substrate-native-compatibility]]) covers the rationale in full.

## Inventions catalogue

`INVENTIONS.md` at the crate root catalogues eight engine-specific inventions (count as of v0.1.29):

1. **Source-of-truth inversion** — git canonical, binary view, CRDT ephemeral; the single most important design choice, covered above
2. **Substrate-native compatibility** — the architectural decision to build a coherent substrate-native API surface rather than a MediaWiki shim; covered above
3. **Constitutional Constrained Author (CCA)** — the editor's squiggle linter at edit time, combined with structured constrained decoding at inference time, produces text structurally incapable of violating the BCSC disclosure posture or the banned-vocabulary policy
4. **Information Verifiability Citation (IVC)** — Phase 7 planned; the masthead band that surfaces verification status of every published claim; today a placeholder
5. **Substrate-Authored Affordances (SAA)** — the squiggle linter's seven deterministic rules, visible at edit time via hover-cards with cited authority
6. **`verify://` URL scheme** — Phase 7 planned; resolves a citation ID to its verifiable source via the substrate's verification path
7. **The passthrough WebSocket relay** — the collab implementation that does not introduce a parallel authoritative record; covered above
8. **The substrate-native API surface set** — the route table above; what the Action API shim would have replicated, done coherently with the substrate's other invariants

The catalogue is open. New inventions land in `INVENTIONS.md` with a brief, the substrate justification, the implementation phase, and the references that anchor it.

## Build phases trajectory

As of 2026-04-27 the engine is at the end of Phase 3:

- **Phase 1** — axum server, comrak rendering, four templates, static assets, core routes (shipped, 8 tests)
- **Phase 1.1** — Wikipedia muscle-memory chrome (shipped, 19 tests)
- **Phase 2** — JSON-LD baseline, atomic edit endpoint, CodeMirror editor, squiggle linter, citation autocomplete, Doorman ladder stubs, collab passthrough relay (shipped, 97 tests)
- **Phase 3** — Tantivy search backend, syndication feeds, sitemap, crawler discovery (shipped)
- **Phase 4** — git2 commit-on-edit, `/history` and `/blame` via gitoxide, `/diff`, redb wikilink graph, `/backlinks`, blake3 federation seam, MCP server via rmcp, smart-HTTP read-only Git remote, OpenAPI 3.1 specification (planned; Phase 4 plan document landed at v0.1.29; awaiting operator clearance of seven open questions before implementation begins)
- **Phase 5** — image and asset handling
- **Phase 6** — per-tenant shaping for customer wikis
- **Phase 7** — federation and content-addressed retrieval against the blake3 substrate; IVC machinery
- **Phase 8** — disclosure-class linter that hardens the BCSC invariants into compile-time-equivalent checks

Phases 4–8 are *planned*; cautionary language applies per [ni-51-102] and [osc-sn-51-721]. Material changes to the build plan are recorded in the phase plan documents and the workspace changelog.

## See also

- [[source-of-truth-inversion]] — the canonical / view / ephemeral pattern generalised across the substrate
- [[substrate-native-compatibility]] — the Action API drop rationale and the substrate-native surface set
- [[collab-via-passthrough-relay]] — the WebSocket relay implementation in depth
