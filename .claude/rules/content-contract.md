# Content contract — content-wiki-documentation

> **Scope.** This rule describes the contract that content in this
> repo must satisfy to be consumed by `app-mediakit-knowledge`, the
> wiki server that renders this repo at `documentation.pointsav.com`.
>
> Authority for this contract is the live crate at
> `pointsav-monorepo/app-mediakit-knowledge/` once it lands there.
> This document is this repo's local reference and is kept in sync
> whenever the crate's render pipeline changes.

Last updated: 2026-04-23.

---

## 1. What lives in this repo

This repo is a flat-by-directory store of Markdown articles, organised
into category subdirectories. It is **content only** — no code, no
binaries. The renderer crate itself is `pointsav-monorepo/app-mediakit-knowledge/`,
not here.

Two classes of file exist at repo root:

**Repo-meta** — ignored by the app, kept at root:
`README.md`, `README.es.md`, `LICENSE`, `CODE_OF_CONDUCT.md`,
`CHANGELOG.md`, `NEXT.md`, `.gitignore`, `.github/`, `.claude/`.

**Wiki content** — consumed by the app:
`index.md` at root (wiki home), plus category subdirectories
containing articles and `_index.md` landing pages.

## 2. Directory layout

```
content-wiki-documentation/
├── index.md                          # wiki home
├── architecture/
│   ├── _index.md                     # category landing
│   ├── os-totebox.md                 # article
│   └── app-mediakit-knowledge.md
├── services/
│   ├── _index.md
│   ├── service-email.md
│   └── service-people.md
└── governance/
    ├── _index.md
    └── sys-adr-07.md
```

Depth is strictly two. Subcategories exist only as a front-matter
field (`subcategory:`), not as nested directories. The URL router
has no route for three-level paths.

## 3. Filename → slug rule

Filename stem **is** the slug. No exceptions.

- Lowercase ASCII only.
- Kebab-case: words separated by single hyphens.
- No leading/trailing hyphen; no repeated hyphens.
- Must match the `slug:` field in front-matter exactly.
- Must be unique across the entire repo — slugs are resolved
  globally by the wikilink resolver, not per-category.

Examples:

| Filename | Slug | Valid |
|---|---|---|
| `os-totebox.md` | `os-totebox` | ✓ |
| `app-mediakit-knowledge.md` | `app-mediakit-knowledge` | ✓ |
| `OS-Totebox.md` | — | ✗ (not lowercase) |
| `topic-os-totebox.md` | — | ✗ (`topic-` prefix is repo-legacy, not a slug component) |
| `TOPIC_TELEMETRY_ARCHITECTURE.md` | — | ✗ (underscore, uppercase) |

## 4. Front-matter schema

YAML front-matter between `---` delimiters at file start. Missing
front-matter parses to defaults (empty title) — the article will
render, but metadata is empty.

### Required fields

| Field | Type | Notes |
|---|---|---|
| `title` | string | Display title. Quoted in YAML if it contains a colon. |
| `slug` | string | Must equal filename stem (§3). |
| `category` | string | Must equal the parent directory name. `root` for `index.md`. |

### Optional fields

| Field | Type | Notes |
|---|---|---|
| `subcategory` | string | Metadata only. Does not affect URLs. |
| `last_edited` | YYYY-MM-DD | Date of last meaningful edit. |
| `editor` | string | Identity of last editor (e.g. `pointsav-engineering`). |
| `status` | enum | `stable` (default), `pre-build`, `draft`. Kebab-case. |
| `references` | list | See §6. Only cited entries render into the bibliography. |

### Example

```yaml
---
title: "ToteboxOS"
slug: os-totebox
category: architecture
subcategory: foundation-layer
last_edited: 2026-04-22
editor: pointsav-engineering
status: stable
references:
  - id: 1
    text: "Klein, G. et al. seL4: Formal Verification of an OS Kernel. ACM SOSP 2009."
    url: "https://sel4.systems/"
---
```

## 5. Body — Markdown conventions

Parser: `pulldown-cmark` with tables, footnotes, strikethrough, and
tasklists enabled. Autolinks are **not** enabled — write `<https://…>`
or explicit Markdown link syntax.

### 5.1 Wikilinks

```
[[slug]]                 → [Resolved Title](../<category>/<slug>)
[[slug|Display Text]]    → [Display Text](../<category>/<slug>)
[[unknown-slug]]         → <span class="wiki-redlink">unknown-slug</span>
```

Unknown slugs render as red links (consistent with Wikipedia).
Cross-references to other articles use `[[slug]]`, not raw paths.

### 5.2 Headings and TOC

- `# H1` — reserved for article title; the template supplies the h1
  from `title:` front-matter. **Do not** write an `# H1` in the body.
- `## H2` and `### H3` — enter the TOC. Each gets an anchor id via
  the slugifier (lowercase, non-alphanumerics → hyphen).
- `#### H4` and deeper — do not enter the TOC but render normally.

### 5.3 Footnotes

Body syntax: `[^N]` where N is a numeric id.

Resolution: N must match the `id:` field of an entry in the
front-matter `references:` array. Entries defined but never cited
in the body are filtered from the rendered bibliography.

Reference definition structure (front-matter):

```yaml
references:
  - id: 1
    text: "Citation text as it appears in the bibliography."
    url: "https://example.com"      # optional — external link
    internal: false                   # optional — true for in-repo cross-refs
    path: "architecture/os-totebox"   # optional — used with internal: true
```

### 5.4 Code blocks

Fenced code blocks (triple-backtick). Syntax highlighting via syntect
is the target; until the corresponding renderer stage is implemented
in the crate, code renders as plain `<pre><code>`.

## 6. Article status lifecycle

| Status | Meaning | Visibility |
|---|---|---|
| `draft` | In-progress; prose incomplete | Renders; caller responsibility to suppress from nav |
| `pre-build` | Content drafted, awaiting factual review or technical build-out | Renders |
| `stable` | Reviewed, current, and maintained | Renders |

The renderer treats all three identically today. Category landings
and navigation filtering by status is not yet wired in the crate.

## 7. URL layout — reference

Derived from §2 and the crate's route table. Informational; content
authors do not configure URLs.

| URL | File | Notes |
|---|---|---|
| `/` | `index.md` | Wiki home |
| `/:category` | `<category>/_index.md` | Category landing; article list auto-built from `*.md` in directory, excluding `_index.md` |
| `/:category/:slug` | `<category>/<slug>.md` | Article |
| `/search?q=…` | — | Full-text search results (Tantivy) |
| `/edit/:category/:slug` | — | Browser editor; requires MBA auth and `EDITOR_ENABLED=true` |

## 8. ADR compliance expected of content

- **SYS-ADR-07** — no AI-generated content may be committed without
  human review. The renderer and search paths contain no AI; the
  editor commit path requires MBA-verified human identity.
- **SYS-ADR-19** — every commit to this repo must originate from a
  verified human author. The staging-tier commit flow
  (`~/Foundry/tool-commit-as-next.sh`) satisfies this for local
  authoring; the browser editor satisfies it via MBA auth.
- **BCSC disclosure rule** (workspace §6) — Sovereign Data
  Foundation is referred to in planned / intended terms only.
  Never as a current equity holder or active governance body.
  Applies to all content in this repo, as content is publicly
  served at `documentation.pointsav.com`.

## 9. Gaps and migration state

As of 2026-04-23, the repo does not yet conform to this contract.
The normalisation migration is tracked in `cleanup-log.md` and
coordinated against the open items in `NEXT.md`.

Notable gaps:

- No `index.md` at root.
- No category subdirectories; all articles currently at repo root.
- Filename-case inconsistency: three conventions present
  (`topic-*.md`, `TOPIC-*.md`, `TOPIC_*.md`).
- `topic-*.yaml`, `sys-adr-*.yaml`, `service-*-01.yaml` files are
  structured records without markdown bodies; each needs classification
  (becomes article / becomes article front-matter / moves cross-repo).

## 10. Authority and change control

If the `app-mediakit-knowledge` crate's render pipeline changes in a
way that alters the contract (new required field, different footnote
syntax, additional markdown extension, etc.), this file is updated in
the same change-set that touches the crate, and the content
normalisation work is re-scoped.

The crate is the ground truth; this file is the local mirror.
