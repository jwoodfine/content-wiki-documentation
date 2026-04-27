# Cleanup log — content-wiki-documentation

> Rolling log of in-flight cleanup work, decisions, and open
> questions in this repo. Most-recent entries at top. Entries
> move from Open to Closed in place; closed entries retain
> their opened-on date for historical reference.
>
> Trivial edits (single-file typo fixes, formatting tweaks) do
> not belong here. Meaningful cleanup — renames across files,
> layout-rule enforcement, defect resolution, surfaced open
> questions — does.

Last updated: 2026-04-23.

---

## Open

### 2026-04-27 — Three style-guide TOPICs added at repo root (legacy pattern, frontmatter present)

Six new files landed at repo root on `cluster/project-language` from
the project-language Task session, following workspace `NEXT.md`
Phase 2 of the cluster brief:

- `topic-style-guide-readme.md` + `.es.md`
- `topic-style-guide-topic.md` + `.es.md`
- `topic-style-guide-guide.md` + `.es.md`

These are Phase 2 of the language-protocol-substrate convention —
public-facing operational documents explaining how to write each
genre. They are the customer-facing pair of
`pointsav-monorepo/service-disclosure/templates/*.toml`.

Layout state: at repo root in the legacy `topic-*.md` pattern,
matching every other existing `topic-*.md` file. **Improvement vs
existing files**: these carry proper YAML frontmatter per
`content-contract.md` §4 (title, slug, category, status,
last_edited, editor, cites). Most existing `topic-*.md` files do
not.

Bilingual pair: the workspace-tier rule (`~/Foundry/CLAUDE.md` §6)
requires bilingual TOPICs and overrides this repo's local
"English-only wiki content" note. Spanish files follow strategic-
adaptation pattern per DOCTRINE.md §XII — not 1:1 translation.
The repo `CLAUDE.md` "wiki content English-only" line is
inherited drift from before the bilingual rule was workspace-
tier; surfacing for a future repo-CLAUDE update pass.

Pending future migration into `reference/` category directory as
part of the broader category-migration item already tracked
above. The new files migrate alongside the existing legacy
topics; no separate migration is needed.

Categorisation hint: `category: reference` is declared in
frontmatter, so the migration into `reference/<slug>.md` is a
straightforward `git mv` plus updating the slug field to drop the
`topic-` prefix (current frontmatter has slug
`topic-style-guide-readme`; future slug becomes
`style-guide-readme` per `naming-convention.md` §5).

### 2026-04-23 — Naming convention draft awaiting ratification

`.claude/rules/naming-convention.md` drafted, status `Draft`.
Four operator decisions pending (see §10 of that file): category
set, investor-audience disposition, front-matter schema changes,
ID format. Until ratified, the nine-category taxonomy and front-
matter extensions are proposed-not-binding; content migration
waits on ratification to avoid migrating twice.

### 2026-04-23 — Migration to contract-conforming layout

The repo's existing content predates `content-contract.md` and the
layout rule. A normalisation pass is required. Scope:

- Add `index.md` at repo root (wiki home).
- Create category directories for the existing content
  (`architecture/`, `services/`, `governance/` at minimum; final
  taxonomy tbd).
- Move existing `topic-*.md` / `TOPIC-*.md` / `TOPIC_*.md` files
  into category directories, normalising filenames to lowercase
  kebab and adding front-matter where absent.
- Write a `_index.md` per category.
- Rewrite cross-article references to `[[slug]]` wikilinks.

Sequencing not yet decided — candidate is to migrate one category
at a time, beginning with `architecture/` (already seeded by the
app-mediakit-knowledge article written 2026-04-23).

### 2026-04-23 — YAML-only structured records need classification

Files at repo root without Markdown bodies, requiring per-file
disposition:

| File | Candidate disposition |
|---|---|
| `sys-adr-06.yaml` … `sys-adr-19.yaml` (11 files) | Become `governance/sys-adr-NN.md` articles with the YAML becoming front-matter plus narrative body |
| `service-content-01.yaml`, `service-egress-01.yaml`, `service-email-01.yaml`, `service-people-01.yaml` | Pair with `services/<name>.md` articles; YAML becomes front-matter structured block |
| `os-workplace-01.yaml` | Become `architecture/os-workplace.md` |
| `topic-3d-asset-tokens.yaml`, `topic-system-slm.yaml`, `topic-system-udp.yaml` | Pair with existing / future topic articles |

No migrations executed yet. Decisions to be made per-file; each
disposition will be logged here when it lands.

### 2026-04-23 — Filename-case normalisation

Three conventions coexist for topic files at repo root:
`topic-*.md`, `TOPIC-*.md`, `TOPIC_*.md`. The content contract
requires lowercase kebab filenames (= slugs). Every existing `.md`
file is renamed as part of the category-migration pass above.
Wikilinks pointing to renamed slugs are rewritten in the same
commit.

### 2026-04-23 — `RESEARCH-BIM-MARKET.md` classification needed

Untracked file at repo root dated 2026-04-22. Not yet read.
Questions: is this repo the right home for market-research
material? If yes, does it belong in a `research/` category or is
it internal-only and should not be committed at all? If no, where
does it go? Decision needed before any commit touches this file.

### 2026-04-23 — `app-mediakit-knowledge.zip` cross-repo handoff

Untracked ZIP at repo root containing the `app-mediakit-knowledge`
Rust crate. Per Nomenclature Matrix §3, `app-*` prefix belongs in
`pointsav-monorepo`. Handoff entry opened in
`handoffs-outbound.md`. This repo will delete the local ZIP once
the destination commit lands in the monorepo; because the ZIP is
untracked, deletion is a plain `rm` rather than `git rm`.

### 2026-04-23 — `upstream` remote is a legacy artefact

Remote `upstream` on this repo points to
`git@github.com:pointsav/pointsav-monorepo.git`. Not used by this
repo's flow; appears to be residual from when wiki content may
have lived inside the monorepo. Removal is non-destructive (`git
remote remove upstream`) but requires explicit approval before a
session executes it.

### 2026-04-23 — `README-pointsav-wiki.md` possibly redundant

File at repo root alongside `README.md`. Contents not yet read.
If it duplicates `README.md` it should be removed; if it carries
unique material it should be merged into `README.md` or moved into
the wiki as an article.

### 2026-04-23 — `glossary-documentation.csv` has no contracted home

CSV at repo root (~8 KB). The content contract describes Markdown
articles, not tabular data. Options: (a) convert to an article
`reference/glossary.md` where terms appear in a table; (b) move to
the monorepo under a service that owns term definitions; (c) leave
until a contract decision is made. Defer until the taxonomy above
is decided.

---

## Closed

### 2026-04-23 — Bootstrap of `.claude/rules/`

`Closed: 2026-04-23.`
`.claude/rules/` directory created; `content-contract.md`,
`repo-layout.md`, `cleanup-log.md`, `handoffs-outbound.md` drafted
and written. Repo-level `CLAUDE.md` created referencing all four.

### 2026-04-23 — Repo-level `CLAUDE.md` created

`Closed: 2026-04-23.`
Closed `NEXT.md` item 1 ("Repo-level `CLAUDE.md` missing"). File
at repo root describes scope, role expectations, relationship to
`app-mediakit-knowledge`, local rules, commit flow, and migration
state. `NEXT.md` itself still lists the item as open pending a
refresh pass.
