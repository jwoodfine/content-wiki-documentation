---
schema: foundry-doc-v1
document_version: 0.1.0
title: "app-mediakit-knowledge — the wiki engine"
slug: topic-app-mediakit-knowledge
category: applications
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
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
---

## §1 What it is

`app-mediakit-knowledge` is the wiki engine that serves PointSav's engineering documentation at `https://documentation.pointsav.com`. The engine is a single-binary Rust service composed of an `axum` HTTP server, a `comrak` CommonMark renderer with PointSav-specific extensions for wikilinks, footnotes, table of contents, and section anchors; a `tantivy` full-text search backend; and a `maud` templating layer that ships four article templates and accompanying static-asset bundles. The engine reads markdown files from a content directory the operator names at startup, renders them on demand into HTML, and returns them with caching headers tuned for a documentation audience.

The engine is a *view* over a markdown tree, not a content repository. The markdown tree is canonical; the running binary is a view that any number of operators can stand up over the same content tree, or different content trees, with no shared mutable state on the binary side. This source-of-truth inversion is the single most important design choice and is treated more substantively in §2.

The engine's first public deployment went live on 2026-04-27 at 16:25 UTC, serving a four-file placeholder content tree at `https://documentation.pointsav.com`. The full route surface from build phases 1, 1.1, 2, and 3 is operational; phases 4 through 8 are planned but not yet implemented.

## §2 Source-of-truth inversion

The substrate's load-bearing design choice: **git is canonical; the running binary is a view; CRDT (when collaboration is enabled) is session-ephemeral**.

Every concrete artefact a reader of the wiki interacts with — the HTML page, the Atom feed entry, the JSON-LD block, the search-result hit, the wikilink graph — is derived at request time from the markdown tree on disk. The disk state is what gets committed, reviewed, replicated, and disclosed. The HTML is throwaway. The Tantivy index is throwaway (rebuilt from the markdown tree on startup). The redb wikilink graph (Phase 4) is throwaway. The collaborative CRDT (Phase 2 Step 7, default-off) is throwaway between sessions.

This inversion is the inverse of MediaWiki's traditional model, where the database is canonical and the file system is a derived working copy. The engine flips that: the file system is canonical, and the database (search index, link graph) is a derived working copy. The motivation is operational simplicity — a content-tree backup is a `git clone`; replication is a `git pull`; audit is a `git log` — and a substrate-level invariant: every published claim is a signed git commit, the disclosure record is the git history, and the BCSC continuous-disclosure posture per `conventions/bcsc-disclosure-posture.md` is enforced by the substrate's structure rather than by policy alone.

Other patterns follow from the inversion. The wiki has no preview-then-publish workflow because the canonical state is what was committed; an edit committed *is* a publication. There is no scheduled-publish workflow because the same property holds. There is no server-side draft state because drafts live in the contributor's git working copy or in the project-knowledge cluster's drafts-outbound port (per `conventions/cluster-wiki-draft-pipeline.md`), not in a database the wiki engine owns.

## §3 The route surface

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
| `/ws/collab/{slug}` | WebSocket passthrough relay (default-off behind `--enable-collab`) | 2.7 |

Phase 4 is intended to add `/history/{slug}`, `/blame/{slug}`, `/diff/{a}/{b}`, `/backlinks/{slug}`, an MCP server route `[mcp-spec]` for agent clients, and a read-only Git remote over smart-HTTP — letting any git client clone the served content tree as a regular git repository, riding the existing TLS termination.

The engine emits JSON-LD `TechArticle` and `DefinedTerm` schema `[json-ld-schema-org]` in every rendered article's `<head>` block (Phase 2 Step 1) for search-engine and LLM-crawler comprehension. The structured data is generated from the article's frontmatter, not hand-authored per page; the schema shape is consistent across the corpus.

## §4 Wikipedia muscle-memory chrome (Phase 1.1)

The engine ships with a deliberately Wikipedia-recognisable chrome. A reader of any Wikipedia article will navigate the engine without prompting, and a reader unfamiliar with Wikipedia will pick up the patterns in seconds because they are well-documented conventions.

What was kept (per `UX-DESIGN.md` §1):

- Article / Talk tabs at the top of the page (Talk reserved for a future implementation; tab structure present today)
- Read / Edit / View history tabs alongside the Article / Talk pair
- Per-section `[edit]` pencils on every `## H2` and `### H3` heading
- End-of-article ordering: References, See also, Categories, with a footer band naming the article's licence and the substrate
- Hatnote band at the top of the article (used for disambiguation and cross-references)
- Lead first-sentence convention (the article's subject is the bolded subject of the lead sentence)
- Tagline directly under the article title
- Collapsible left-rail TOC (built from `## H2` and `### H3` headings; deeper headings render normally but do not enter the TOC)
- Language switcher (currently English / Spanish; structurally ready for additional languages without re-templating)

What was added (substrate-specific, not Wikipedia-traditional):

- Citation badges next to inline `[citation-id]` references; hover reveals the registry entry from `~/Foundry/citations.yaml`
- Forward-Looking-Information cautionary banner (Phase 8 is intended to harden this into a linter check `[ni-51-102]` `[osc-sn-51-721]`; today the banner renders when an article's frontmatter sets `forward_looking: true`)
- BCSC `disclosure_class` field rendered as a small badge in the article header (`narrative` / `financial` / `governance`); not visible in default chrome but exposed in the JSON-LD
- Information Verifiability Citation (IVC) masthead band placeholder (Phase 7 is intended to light up the IVC machinery; the band is a visual surface only at this time)
- Reader density toggle (compact / comfortable; settings persist client-side)

The chrome is implemented in four `maud` HTML templates (`article.html`, `category.html`, `search.html`, `editor.html`) and a CSS bundle that tracks the Wikipedia *Vector* skin's spacing and typography rather than imitating its colour palette. The target is muscle memory, not literal mimicry; a reader who knows Wikipedia recognises the layout, but the visual identity is distinct.

## §5 Editor surface (Phase 2)

The wiki's editor is a CodeMirror 6 instance vendored into the binary's static-asset bundle, served at `/edit/{slug}`. It supports markdown highlighting with line numbers, configurable line wrap, undo/redo history with a keyboard accelerator, and atomic disk write via the engine's `POST /edit/{slug}` endpoint.

Three substrate-aware editor features distinguish the implementation:

**Squiggle linting (Phase 2 Step 4).** Seven deterministic rules flag editorial issues at typing time, each with a cited authority visible in a hover-card. The rules cover banned vocabulary, forward-looking framings without the cautionary banner pattern, BCSC-discipline checks (Sovereign Data Foundation referenced in current-tense without a planned/intended qualifier `[ni-51-102]`), and a set of Bloomberg-article-standard register checks. The rules are deterministic at edit time; the AS-2 grammar-time constraint (Doctrine claim #31, Constitutional Constrained Author `[constitutional-ai-2212-08073]`) is intended to harden these into compile-time-equivalent guarantees once the service-slm Doorman ships the `llguidance` `[llguidance]` integration.

**Citation autocomplete (Phase 2 Step 5).** Pressing `[` triggers a typeahead populated from the workspace citation registry at `~/Foundry/citations.yaml`. The contributor types `[ni-51` and the list narrows to `[ni-51-102]` (BCSC continuous disclosure) plus any other matches. Selecting an entry inserts the canonical `[citation-id]` form and adds the citation to the article's frontmatter `cites:` list automatically. The pattern keeps citation discipline straightforward to follow and difficult to skip.

**Three-keystroke ladder for Doorman (Phase 2 Step 6 stubs).** Tab opens a ladder of "ask Doorman" affordances at the cursor position — find a citation, suggest a hatnote target, generate a disambiguation link, propose a section heading. The affordances return 501 stubs in the v0.1.29 binary; Phase 4 is intended to wire them to the service-slm Doorman per `conventions/three-ring-architecture.md` Ring 3 routing.

The editor's atomic-write semantics are conservative: the engine writes the new file content to a temporary path in the same directory, fsyncs, and renames over the destination. A failed write is visible to the contributor (the page returns an error state) and leaves the canonical content untouched. Concurrent edits from two non-collab sessions race at the rename step; the last-writer-wins convention is documented.

## §6 Search, feeds, and ingestion (Phase 3)

The engine indexes the content tree on startup and incrementally on edit. The index is on-disk Tantivy (BM25 by default) at `<state-dir>/search/`, rebuilt from the content tree if missing. Re-indexing on edit is triggered from the `POST /edit/{slug}` flow; the Tantivy `IndexWriter` is held in an `Arc<Mutex<>>` per the crate's typical pattern and released before reader reload to avoid the asynchronous-reload race identified during Phase 3 work.

Three syndication formats render the corpus to crawlers: `/feed.atom` (RFC 4287 — each article is a feed entry with `title`, `summary`, `published`, `updated`, and the article's `cites:` list resolved against the registry), `/feed.json` (JSON Feed 1.1 — identical content shape, format differs), and `/sitemap.xml` (sitemaps.org-compliant — every article URL with last-modified date).

Two crawler-discovery files round out the surface: `/robots.txt` (User-agent rules; currently permissive) and `/llms.txt` (the llmstxt.org convention for LLM crawlers, listing the corpus's authoritative source URLs and the per-article markdown URLs at `/git/{slug}` for ingestion).

The `/git/{slug}` route serves raw markdown source. An LLM crawler or a future federation peer can ingest the content tree by following `/llms.txt` to discover the article list, then fetching `/git/{slug}` for each article's source. This is the substrate's content-addressed federation path; Phase 7 is intended to harden it with blake3 hashing (Phase 4 Step 4.5 lays the groundwork). The route accepts an optional `.md` suffix on the slug for tools that expect markdown URLs to end in `.md`.

## §7 Real-time collaboration (Phase 2 Step 7)

The engine optionally supports real-time collaborative editing via Yjs CRDT. The feature is default-off behind the `--enable-collab` CLI flag; the production deployment at v0.1.29 does not enable it.

The implementation follows the substrate's source-of-truth inversion: **the server is a passthrough WebSocket relay, not a Yjs server**. Yjs document state never lives on the server. The relay is a thin `tokio::sync::broadcast` per-slug room with a 256-message lag buffer; clients send Yjs update packets, the server forwards them to other clients in the room, and persistence flows through the existing `POST /edit/{slug}` save path on deliberate save (not on every keystroke). When all clients leave the room, the room closes and any unsaved CRDT state is discarded.

The motivation: the substrate's canonical record is git, not a Yjs document. A long-lived Yjs document on the server would create a parallel canonical record that drifts from git, defeats the disclosure-substrate posture, and complicates audit. The passthrough relay keeps git canonical and the CRDT session-ephemeral.

The client lazy-loads `cm-collab.bundle.js` (302 KB; built out-of-tree and committed to `static/vendor/`) only when the template's `window.WIKI_COLLAB_ENABLED` flag is set by the server, so production deploys without `--enable-collab` never load any of the Yjs JavaScript and never expose the `/ws/collab/{slug}` route.

## §8 Substrate-native compatibility surface

The engine is a substrate-native wiki, not a MediaWiki shim. This reflects DOCTRINE claim #29 (Substrate Substitution) ratified at workspace v0.1.10 and refined at v0.1.14.

What was kept: the `xml-dump` import path (the engine accepts MediaWiki XML dumps `[mediawiki-xml-dump]` for one-time corpus migration; a future `import-mediawiki-xml` tool consumes the dump format and emits the engine's markdown + frontmatter shape; the migration is one-shot, the live wiki does not run a MediaWiki API), URL conventions (`/wiki/{slug}` matches MediaWiki's URL layout so existing links from external sites continue to resolve), wikilink syntax (`[[slug]]` and `[[slug|display text]]` match Wikipedia's convention), and footnote syntax (`[^1]` matches CommonMark).

What was dropped: the MediaWiki Action API shim `[mediawiki-action-api]` (scoped at v0.1.10, dropped at v0.1.14 — substrate-native API surface covers the use cases without introducing a parallel authoritative interface), MediaWiki templates / parser functions (rendering path is CommonMark with PointSav-specific extensions, not a MediaWiki parser; templates not supported), and the pywikibot ecosystem (substrate's automation path is the workspace's existing tooling, not pywikibot).

The trade-off is a narrower compatibility surface against a substrate-coherent posture. A reader migrating from a MediaWiki deployment loses templates and the Action API; they gain source-of-truth inversion, deterministic rendering, a BCSC-grounded disclosure posture `[ni-51-102]`, and a smaller attack surface. For PointSav's engineering documentation use case, the trade is favourable. A separate sibling TOPIC ([substrate-native-compatibility](topic-substrate-native-compatibility.md)) goes deeper on the rationale.

## §9 Inventions catalogue

`INVENTIONS.md` at the crate root catalogues eight engine-specific inventions (current count as of v0.1.29; the catalogue grows as phases ratify). The inventions are substantive design choices that distinguish this engine from a generic markdown-served-as-HTML implementation:

1. **Source-of-truth inversion** — git canonical, binary view, CRDT ephemeral; covered in §2 above.
2. **Substrate-native compatibility** — Doctrine claim #29; covered in §8 above.
3. **Constitutional Constrained Author (CCA)** — Doctrine claim #31 `[constitutional-ai-2212-08073]`; the editor's squiggle linter at edit time plus the AS-2 grammar constraint at decode time produce text that is structurally incapable of violating the BCSC disclosure posture or the workspace banned-vocabulary policy.
4. **Information Verifiability Citation (IVC)** — Phase 7+ (planned); the masthead band that surfaces verification status of every published claim. Today a placeholder; the IVC machinery is substantive intended future work.
5. **Substrate-Authored Affordances (SAA)** — the squiggle linter's seven deterministic rules; visible at edit time via hover-cards with cited authority.
6. **`verify://` URL scheme** — Phase 7+ (planned); intended to resolve a citation ID to its verifiable source via the substrate's verification path, not a public DNS lookup.
7. **The passthrough WebSocket relay** — covered in §7 above; the collaboration implementation that does not introduce a parallel authoritative record.
8. **The substrate-native API surface set** — the route table in §3 above; what the Action API shim would have replicated, done coherently with the substrate's other invariants.

The catalogue is open. New inventions land in `INVENTIONS.md` with a brief description, the substrate justification, the implementation phase, and the references that anchor it.

## §10 Build phases trajectory

The engine is shipped through a sequenced build plan documented in `ARCHITECTURE.md` §3. As of 2026-04-27 the engine is at the end of Phase 3:

- **Phase 1** — axum server, comrak rendering, four templates, static assets, `/healthz` + `/` + `/wiki/{slug}` + `/static/{*path}` (shipped; 8 tests)
- **Phase 1.1** — Wikipedia muscle-memory chrome; covered in §4 above (shipped; 19 tests)
- **Phase 2** — JSON-LD baseline + atomic edit endpoint + CodeMirror vendoring + squiggle linter + citation autocomplete + Doorman ladder stubs + collaboration passthrough relay (Steps 1–7 all shipped; 97 tests)
- **Phase 3** — Tantivy search backend + on-disk index + `/search?q=` + edit-triggers-reindex + `/feed.atom` + `/feed.json` + `/sitemap.xml` + `/robots.txt` + `/llms.txt` + `/git/{slug}` (Steps 3.1–3.4 shipped)
- **Phase 4** — git2 commit-on-edit + `/history` + `/blame` via gix + `/diff` + redb wikilink graph + `/backlinks` + blake3 federation seam + MCP server `[mcp-spec]` via rmcp + smart-HTTP read-only Git remote + OpenAPI 3.1 specification (planned; Phase 4 plan document landed at v0.1.29; seven open questions require operator clearance before implementation begins)
- **Phase 5** — image and asset handling (planned)
- **Phase 6** — per-tenant shaping for Customer wikis (planned)
- **Phase 7** — federation and content-addressed retrieval against the blake3 substrate; IVC machinery (planned)
- **Phase 8** — disclosure-class linter intended to harden the BCSC invariants into compile-time-equivalent checks (planned)

Phases 4–8 are planned; cautionary language applies per `[ni-51-102]` and `[osc-sn-51-721]`. Material changes to the build plan are recorded in the phase plan documents at `docs/PHASE-N-PLAN.md` and in the workspace `CHANGELOG.md`.

## See also

- [Decode-Time Constraints](topic-decode-time-constraints.md)
- [The Reverse-Funnel Editorial Pattern](topic-reverse-funnel-editorial-pattern.md)
- [Substrate-Native Compatibility](topic-substrate-native-compatibility.md)
- [documentation.pointsav.com Launch](topic-documentation-pointsav-com-launch-2026-04-27.md)
