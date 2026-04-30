---
schema: foundry-doc-v1
title: "app-mediakit-knowledge"
slug: topic-app-mediakit-knowledge
category: applications
type: topic
quality: complete
short_description: "app-mediakit-knowledge is the single-binary Rust wiki engine that serves PointSav's engineering documentation at documentation.pointsav.com, treating a markdown file tree as the canonical record and the running binary as a stateless view over it."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - constitutional-ai-2212-08073
  - c2sp-tlog-tiles
  - mediawiki-action-api
  - mediawiki-xml-dump
  - mcp-spec
  - llguidance
  - json-ld-schema-org
paired_with: topic-app-mediakit-knowledge.es.md
---

# app-mediakit-knowledge

> app-mediakit-knowledge is the single-binary Rust wiki engine that serves PointSav's engineering documentation at documentation.pointsav.com, treating a markdown file tree as the canonical record and the running binary as a stateless view over it.

**app-mediakit-knowledge** is the wiki engine that serves PointSav's engineering documentation at `https://documentation.pointsav.com`. The engine is a single-binary Rust service composed of an `axum` HTTP server, a `comrak` CommonMark renderer with PointSav-specific extensions for wikilinks, footnotes, table of contents, and section anchors; a `tantivy` full-text search backend; and a `maud` templating layer that ships four article templates and accompanying static-asset bundles. The engine reads markdown files from a content directory named at startup, renders them on demand into HTML, and returns them with caching headers tuned for a documentation audience.

The engine's first public deployment went live on 2026-04-27 at 16:25 UTC. The full route surface from build phases 1, 1.1, 2, and 3 is operational; phases 4 through 8 are planned.

## Source-of-truth inversion

The engine's load-bearing design choice: **git is canonical; the running binary is a view; CRDT (when collaboration is enabled) is session-ephemeral**.

Every concrete artefact a reader encounters — the HTML page, the Atom feed entry, the JSON-LD block, the search-result hit, the wikilink graph — is derived at request time from the markdown tree on disk. The disk state is what gets committed, reviewed, replicated, and disclosed. The Tantivy index is throwaway (rebuilt from the markdown tree on startup). The redb wikilink graph (Phase 4, planned) is throwaway. The collaborative CRDT (Phase 2 Step 7, default-off) is throwaway between sessions.

This inverts the conventional model, where a database is canonical and the file system is a derived working copy. The motivation is operational simplicity — a content-tree backup is a `git clone`; replication is a `git pull`; audit is a `git log` — and a substrate-level invariant: every published claim is a signed git commit, and the BCSC continuous-disclosure posture `[ni-51-102]` is enforced by the substrate's structure rather than by policy alone.

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
| `/feed.atom` | RFC 4287 Atom syndication feed | 3 |
| `/feed.json` | JSON Feed 1.1 syndication | 3 |
| `/sitemap.xml` | sitemaps.org-compliant sitemap | 3 |
| `/robots.txt` | Crawler discovery | 3 |
| `/llms.txt` | llmstxt.org convention for LLM crawlers | 3 |
| `/git/{slug}` | Raw markdown source for git-clone-style ingestion | 3 |
| `/ws/collab/{slug}` | WebSocket passthrough relay (default-off) | 2.7 |

Phase 4 is intended to add `/history/{slug}`, `/blame/{slug}`, `/diff/{a}/{b}`, `/backlinks/{slug}`, an MCP server route `[mcp-spec]` for agent clients, and a read-only Git remote over smart-HTTP.

The engine emits JSON-LD `TechArticle` and `DefinedTerm` schema `[json-ld-schema-org]` in every rendered article's `<head>` block (Phase 2 Step 1). The structured data is generated from the article's frontmatter, consistent across the corpus.

## Wikipedia muscle-memory chrome

The engine ships with a deliberately Wikipedia-recognisable chrome. A reader who knows any Wikipedia article navigates the engine without prompting.

What was kept per `UX-DESIGN.md` §1:

- Article / Talk tabs at the top of the page
- Read / Edit / View history tabs alongside the Article / Talk pair
- Per-section `[edit]` pencils on every H2 and H3 heading
- End-of-article ordering: References, See also, Categories, with a footer band
- Hatnote band at the top of the article
- Lead first-sentence convention (the article's subject is the bolded subject of the lead sentence)
- Collapsible left-rail TOC built from H2 and H3 headings
- Language switcher (currently English / Spanish)

What was added (substrate-specific):

- Citation badges next to inline `[citation-id]` references
- Forward-Looking-Information cautionary banner `[ni-51-102]`
- BCSC `disclosure_class` field rendered as a small badge in the article header
- Information Verifiability Citation (IVC) masthead band placeholder (Phase 7, planned)
- Reader density toggle (compact / comfortable)

The chrome is implemented in four `maud` HTML templates and a CSS bundle that tracks the Wikipedia Vector skin's spacing and typography rather than imitating its colour palette.

## Editor surface

The wiki's editor is a CodeMirror 6 instance vendored into the binary's static-asset bundle, served at `/edit/{slug}`. It supports markdown highlighting with line numbers, configurable line wrap, and atomic disk write via the engine's `POST /edit/{slug}` endpoint.

Three substrate-aware editor features distinguish the implementation:

**Squiggle linting (Phase 2 Step 4).** Seven deterministic rules flag editorial issues at typing time, each with a cited authority visible in a hover-card. The rules cover banned vocabulary, forward-looking framings without the cautionary banner, BCSC-discipline checks, and Bloomberg-article-standard register checks. The AS-2 grammar-time constraint (Doctrine claim #31, Constitutional Constrained Author `[constitutional-ai-2212-08073]`) is intended to harden these into compile-time-equivalent guarantees once the service-slm Doorman ships the `llguidance` `[llguidance]` integration.

**Citation autocomplete (Phase 2 Step 5).** Pressing `[` triggers a typeahead populated from the workspace citation registry. Selecting an entry inserts the canonical `[citation-id]` form and adds the citation to the article's frontmatter `cites:` list automatically.

**Three-keystroke ladder for Doorman (Phase 2 Step 6 stubs).** Tab opens a ladder of "ask Doorman" affordances — find a citation, suggest a hatnote target, generate a disambiguation link, propose a section heading. The affordances return 501 stubs in the current binary; Phase 4 is intended to wire them to the service-slm Doorman.

The editor's atomic-write semantics are conservative: the engine writes the new file content to a temporary path, fsyncs, and renames over the destination. A failed write leaves the canonical content untouched.

## Search, feeds, and ingestion

The engine indexes the content tree on startup and incrementally on edit. The index is on-disk Tantivy (BM25 by default), rebuilt from the content tree if missing.

Three syndication formats render the corpus to crawlers: `/feed.atom` (RFC 4287), `/feed.json` (JSON Feed 1.1), and `/sitemap.xml` (sitemaps.org-compliant). Two crawler-discovery files round out the surface: `/robots.txt` and `/llms.txt`.

The `/git/{slug}` route serves raw markdown source. An LLM crawler or a future federation peer can ingest the content tree by following `/llms.txt` to discover the article list, then fetching `/git/{slug}` for each article's source.

## Real-time collaboration

The engine optionally supports real-time collaborative editing via Yjs CRDT, default-off behind the `--enable-collab` CLI flag.

The implementation follows the source-of-truth inversion: the server is a passthrough WebSocket relay, not a Yjs server. Yjs document state never lives on the server. The relay is a thin `tokio::sync::broadcast` per-slug room; clients send Yjs update packets, the server forwards them to other clients, and persistence flows through the existing `POST /edit/{slug}` save path on deliberate save. When all clients leave the room, the room closes and any unsaved CRDT state is discarded.

## Substrate-native compatibility

The engine is substrate-native, not a MediaWiki shim. This reflects Doctrine claim #29 (Substrate Substitution). What was kept: xml-dump import path, URL conventions (`/wiki/{slug}`), wikilink syntax (`[[slug]]`), and footnote syntax (`[^1]`). What was dropped: the MediaWiki Action API shim `[mediawiki-action-api]`, MediaWiki templates and parser functions, and the pywikibot ecosystem. See [[topic-substrate-native-compatibility]] for the full rationale.

## Build phases trajectory

As of 2026-04-27 the engine is at the end of Phase 3:

- **Phase 1** — axum server, comrak rendering, four templates, static assets, core routes (shipped; 8 tests)
- **Phase 1.1** — Wikipedia muscle-memory chrome (shipped; 19 tests)
- **Phase 2** — JSON-LD baseline, atomic edit endpoint, CodeMirror vendoring, squiggle linter, citation autocomplete, Doorman ladder stubs, collaboration passthrough relay (Steps 1–7 all shipped; 97 tests)
- **Phase 3** — Tantivy search backend, on-disk index, `/search?q=`, edit-triggers-reindex, `/feed.atom`, `/feed.json`, `/sitemap.xml`, `/robots.txt`, `/llms.txt`, `/git/{slug}` (Steps 3.1–3.4 shipped)
- **Phase 4** — git2 commit-on-edit, history and blame via gix, diff, redb wikilink graph, backlinks, blake3 federation seam, MCP server via rmcp, smart-HTTP read-only Git remote, OpenAPI 3.1 specification (planned)
- **Phases 5–8** — image handling, per-tenant shaping, federation, disclosure-class linter (planned)

Phases 4–8 are planned; cautionary language applies per `[ni-51-102]` and `[osc-sn-51-721]`. Material changes to the build plan are recorded in the workspace `CHANGELOG.md`.

## See Also

- [[topic-substrate-native-compatibility]]
- [[topic-reverse-funnel-editorial-pattern]]
- [[topic-documentation-pointsav-com-launch-2026-04-27]]
- [[topic-decode-time-constraints]]

## References
