---
schema: foundry-doc-v1
title: "MediaKit knowledge application"
slug: app-mediakit-knowledge
category: applications
type: topic
content_type: topic
quality: complete
index_group: knowledge-and-editorial-applications
short_description: "Single-binary Rust wiki engine serving documentation.pointsav.com — a view over a markdown tree where git commits are canonical and the running binary is disposable."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: app-mediakit-knowledge.es.md
cites: []
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
  - id: 7
    text: "llmstxt.org convention for LLM crawlers."
    url: "https://llmstxt.org/"
  - id: 8
    text: "Wikipedia Manual of Style — Layout."
    url: "https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Layout"
---

`app-mediakit-knowledge` is the single-binary Rust wiki engine that serves PointSav's engineering documentation at `https://documentation.pointsav.com`. The engine combines an `axum` HTTP server, a `comrak` CommonMark renderer[^1][^2] with platform-specific extensions for wikilinks, footnotes, table of contents, and section anchors, a `tantivy` full-text search backend[^3], and a `maud` templating layer. The engine reads markdown files from a content directory the operator names at startup, renders them on demand into HTML, and returns them with caching headers tuned for a documentation audience.

The engine is a *view* over a markdown tree, not a content repository. The markdown tree is canonical; the running binary is a view that any number of operators can stand up over the same content tree, or different content trees, with no shared mutable state on the binary side. This source-of-truth inversion is the single most important design choice and is treated in detail in the next section.

The engine's first public deployment went live on 2026-04-27 at 16:25 UTC, serving a four-file placeholder content tree at `https://documentation.pointsav.com`.

## Source-of-truth inversion

The substrate's load-bearing design choice: **git is canonical; the running binary is a view**.

Every concrete artefact a reader encounters — the HTML page, the Atom feed entry, the JSON-LD block, the search-result hit — is derived at request time from the markdown tree on disk. The disk state is what gets committed, reviewed, replicated, and disclosed. The HTML is throwaway. The Tantivy index is throwaway, rebuilt from the markdown tree on startup.

### Inversion of the MediaWiki model

This inversion reverses the traditional MediaWiki model, where the database is canonical and the file system is a derived working copy. Here, the file system is canonical and the database (search index, link graph) is a derived working copy. The motivation is operational simplicity — a content-tree backup is a `git clone`; a content-tree replication is a `git pull`; a content-tree audit is a `git log` — and a substrate-level invariant: every published claim is a signed git commit; the disclosure record is the git history; the BCSC continuous-disclosure posture is enforced by structure rather than by policy alone.

### Workflows the inversion removes

Other patterns follow from the inversion. The wiki has no preview-then-publish workflow because the canonical state is what got committed; an edit committed is a publication. The wiki has no scheduled-publish workflow because the same property holds. The wiki has no server-side draft state because drafts live in the contributor's git working copy or in the editorial pipeline, not in a database the wiki engine owns.

## Route surface

The engine exposes a tight set of HTTP routes. Each is independent; no route depends on session state or on a database the engine owns.

| Route | Purpose |
|---|---|
| `/healthz`, `/health` | Liveness check |
| `/` | Index page (lists all articles in the served content tree) |
| `/wiki/{slug}` | Rendered article HTML |
| `/es/wiki/{slug}` | Rendered Spanish-pair article HTML |
| `/category/{name}` | Category landing page |
| `/history/{slug}` | Per-article revision history, reading directly from the git log and rendering the diff each revision made |
| `/special/all-pages` | Full article index |
| `/special/recent-changes` | Recently edited articles |
| `/search?q=` | Full-text search results (Tantivy) |
| `/sitemap.xml` | sitemaps.org compliant sitemap |
| `/robots.txt` | Crawler discovery |
| `/feed.atom` | RFC 4287 Atom syndication feed[^5] |
| `/llms.txt` | llmstxt.org convention for LLM crawlers[^7] |
| `/static/{*path}` | Static assets (CSS, JS, fonts) |

There is no in-browser editor and no write route — every article is edited in its source git repository and picked up on the next render, not through the engine itself.

### JSON-LD article schema

The engine emits JSON-LD `TechArticle`[^4] and `DefinedTerm` schema in every rendered article's `<head>` block for search-engine and crawler comprehension. The structured data is generated from the article's frontmatter, not hand-authored per page; the schema is the same shape across the corpus.

## Wikipedia muscle-memory chrome

The engine ships with a deliberately Wikipedia-recognisable chrome. A reader of any Wikipedia article will navigate the engine without prompting, and a reader unfamiliar with Wikipedia will pick up the patterns quickly because they are well-documented conventions.[^8]

### Conventions kept from Wikipedia

What was kept (per `UX-DESIGN.md` §1):

- Article / Talk tabs at the top of the page (Talk tab present in the template; Talk discussion is reserved for a future implementation)
- A View history tab alongside the Article/Talk pair, reading directly from the article's git log
- End-of-article ordering: References, See also, Categories, with a footer band naming the article's licence and the substrate
- Hatnote band at the top of the article for disambiguation and cross-references
- Lead first-sentence convention (bolded subject plus copula plus definition)
- Tagline directly under the article title
- Collapsible left-rail table of contents (built from H2 and H3 headings; deeper headings render normally but do not enter the TOC)
- Language switcher (currently English / Spanish; structurally ready for additional languages without re-templating)

### Additions beyond Wikipedia

What was added beyond Wikipedia:

- Forward-Looking-Information cautionary banner when an article's frontmatter sets `forward_looking: true`
- BCSC `disclosure_class` field expressed in the JSON-LD structured data in every rendered article's `<head>` block (not visible as default chrome; consequential when the Phase 8 linter activates)
- Information Verifiability Citation (IVC) masthead band placeholder (Phase 7 is intended to provide the verification machinery)
- Reader density toggle (compact / comfortable; settings persist client-side)

### Template and CSS implementation

The chrome is implemented in `maud` HTML templates and a CSS bundle that tracks Vector 2022's spacing and typography rather than its colour palette. The aim is muscle memory, not literal mimicry — a reader who knows Wikipedia recognises the layout, but the visual identity is distinct.

## Editing model

There is no in-browser editor, no write API, and no locking or collaborative-session model — the engine is read-only from a visitor's perspective. An article is edited in its source git repository, through whatever normal editorial workflow produces the commit, and the change appears on the next render with no service restart. The revision history a reader sees on `/history/{slug}` is that same git log, read directly rather than duplicated into a separate database.

## Search and syndication

The engine indexes the content tree on startup. The index is on-disk Tantivy at `<state-dir>/search/`, rebuilt from the content tree if it is missing.

### Syndication and crawler discovery

- **`/feed.atom`** — RFC 4287 Atom syndication feed of the corpus.
- **`/sitemap.xml`** — sitemaps.org compliant. Lists every article URL with its last-modified date.
- **`/robots.txt`** and **`/llms.txt`** — crawler and LLM-crawler discovery files[^7].

## Substrate-native compatibility surface

The engine is a substrate-native wiki, not a MediaWiki shim. This reflects architectural decisions made during early platform development.

### Kept and dropped MediaWiki surfaces

What was kept: the **`xml-dump` import path** for one-time corpus migration; **URL conventions** (`/wiki/{slug}`); **wikilink syntax** (`[[slug]]` and `[[slug|display text]]`); **footnote syntax** (`[^1]`).

What was dropped: the **MediaWiki Action API shim** — the shim was scoped at v0.1.10 and dropped at v0.1.14 because maintenance scales with MediaWiki's velocity and compliance audit scales with the API surface. The substrate-native surface (article HTML, JSON-LD, Atom, sitemap, llms.txt, search via `/search?q=`) covers the same use cases without a parallel authoritative interface requiring separate maintenance. **MediaWiki templates and parser functions** were dropped because the engine's rendering path is CommonMark with PointSav-specific extensions, not a MediaWiki parser. **The pywikibot ecosystem** was dropped because the substrate's automation path is the existing workspace tooling, not the pywikibot framework.

### Narrower surface, coherent posture

The trade-off is a narrower compatibility surface against a substrate-coherent posture. A reader migrating from a MediaWiki deployment loses templates and the Action API; gains source-of-truth inversion, deterministic rendering, BCSC-grounded disclosure posture, and a smaller attack surface.

A separate sibling article ([[substrate-native-compatibility]]) covers the rationale in full.

## Content federation

The engine is intended to serve content from multiple git repositories through a single rendered surface, using a declarative mount manifest (`knowledge.toml`) that the operator places at the content directory root. Each mount entry names a source repository, a local mount path, and a blueprint — the schema that determines how files in that mount are validated, routed, and linked. This capability is planned; the architecture described here is the intended design, and the single-repository model is the current deployed form.

### Mounts and blueprint schemas

*Mounts and blueprints.* A content mount is a directory subtree derived from a named git repository. Blueprints are named schemas that constrain the content a mount may contain and determine the URL pattern it occupies. Two blueprints are built in: `topic` (the standard wiki article, consuming files in the standard content-contract format) and `guide` (operational documents, rendered with a distinct chrome and excluded from the primary article index). Operators may register additional blueprints — `regional-market`, `adr`, `changelog`, and similar domain-specific schemas — as plugins when Phase 6 ships.

*Per-instance isolation.* Each wiki instance reads only the mounts declared in its own `knowledge.toml`. A `documentation.pointsav.com` deployment and a `projects.woodfinegroup.com` deployment may source overlapping repositories but present entirely independent article surfaces — mount definitions are per-instance configuration, not global registry state.

### Provenance and edit-routing across instances

*Provenance.* Every article rendered from a declarative mount carries provenance frontmatter identifying the source repository and path. Since the engine has no write surface of its own, this keeps the source-of-truth inversion intact across a federated surface by construction: no wiki instance can write to a repository it did not originate from, because no wiki instance writes to any repository at all.

Phase 6 is planned to deliver the `knowledge.toml` schema specification, blueprint plugin API, and provenance frontmatter handling. Phase 7 is planned to deliver content-addressed retrieval, `blake3`-anchored federation, and the verification machinery that connects federated content to the IVC masthead band. See [[federation-via-content-mounts]] for the pattern in depth.

## Build status

The engine is deployed and serving `documentation.pointsav.com` today: rendering, wikilinks, category pages, per-article history, search, and the syndication/crawler surface above are all live. There is no editor, no write API, and no collaborative-editing surface — an article's only path to publication is a commit to its source git repository, read by the engine on the next render.

## See also

- [[source-of-truth-inversion]] — the canonical / view / ephemeral pattern generalised across the substrate
- [[substrate-native-compatibility]] — the Action API drop rationale and the substrate-native surface set
- [[wikipedia-leapfrog-design]] — the 95%/5% muscle-memory and leapfrog headroom design philosophy
- [[knowledge-wiki-home-page-design]] — the home page design intent and slot structure
- [[deploy-knowledge-instance]] — step-by-step guide: build and start app-mediakit-knowledge pointed at a local content repository
- [[use-knowledge-mounts]] — step-by-step guide: add a secondary content repository via declarative knowledge.toml mounts
