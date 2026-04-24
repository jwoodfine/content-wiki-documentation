# content-wiki-documentation — Repo Guide

> This file is the repo-level complement to `~/Foundry/CLAUDE.md`.
> A session that opens here inherits the workspace guide and then
> applies the repo-specific rules below. Read cold at session start.

Last updated: 2026-04-23.

---

## 1. What this repo is

`content-wiki-documentation` holds the engineering documentation wiki
for the PointSav platform as flat-by-category Markdown content.
Scope:

- Platform reference articles (architecture, services, ADRs, glossary).
- Topic pages used for internal explanation and external publication.
- Category landing pages and a single repo-root `index.md` serving
  as the wiki home.

This repo is **content only**. It holds no code and no compiled
binaries. Runtime is elsewhere (see §3).

Classification per workspace §8: **content-wiki repo** — flat
content collection, no project registry, no cluster-clone pattern.
The per-project-cluster mechanism from workspace §9 does not apply
here; sessions in this repo operate as Root Claude throughout.

## 2. Role expectations

A session that opens in this repo is **Root Claude for
`content-wiki-documentation`**. Scope of writes per workspace §9:

- Repo-level `CLAUDE.md` (this file).
- `.claude/rules/*.md` — local rule files (see §4).
- `NEXT.md` — repo-scope open items.
- Article Markdown files in category subdirectories.
- Main-branch maintenance via the staging-tier commit flow.

Out of scope for sessions here:

- Workspace files under `~/Foundry/`.
- Code anywhere in the monorepo.
- Direct pushes to the canonical `origin` remote (see §5).

## 3. Relationship to `app-mediakit-knowledge`

This repo's content is consumed by `app-mediakit-knowledge`, a Rust
wiki server that renders the content at `documentation.pointsav.com`.

- The **crate** lives in `pointsav-monorepo/app-mediakit-knowledge/`
  per Nomenclature Matrix §3 (`app-*` prefix = monorepo project).
- **This repo** is the crate's sole content source.
- The **contract between them** is pinned in
  `.claude/rules/content-contract.md` — front-matter schema,
  directory layout, wikilink and footnote conventions, URL routing.
  When in doubt about how to shape content, read the contract.

The crate is the ground truth for the render pipeline. If the crate
changes the contract (new required field, different markdown
extension, etc.), `.claude/rules/content-contract.md` is updated
in the same change-set.

## 4. Local rules — `.claude/rules/`

| File | Purpose |
|---|---|
| `content-contract.md` | Contract that content must satisfy for `app-mediakit-knowledge`. Read this before adding or editing articles. |
| `naming-convention.md` | Category taxonomy, slug composition, front-matter extensions, MOC pattern, stub/redirect/wanted conventions. Currently Draft — pending operator ratification of four decisions (§10 of that file). |
| `repo-layout.md` | Allowed files at repo root and category directories; defect-closure procedure. |
| `cleanup-log.md` | Rolling log of in-flight cleanup work, decisions, and open questions. Most-recent entries at top. |
| `handoffs-outbound.md` | Passive outbox for cross-repo file moves per workspace §9. |

Workspace §10 requires a session to read these at start and to
append a dated entry to `cleanup-log.md` at session end when
meaningful cleanup happens. Trivial edits (single-file typo fixes,
formatting tweaks) do not belong in the log.

## 5. Commit flow (reminder)

This repo is an **engineering repo with staging mirrors** — not an
admin-only repo. Commits flow through the staging tier per
workspace §4 and §7.

- Use `~/Foundry/tool-commit-as-next.sh` for every commit. Author
  identity alternates between `jwoodfine` and `pwoodfine` per commit.
- Staged-file discipline: `git add <specific files>`, never
  `git add .` or `git add -A`.
- Pushing is deferred to the workspace §7 "Stage 6" promotion flow.
  Do not push from this repo without explicit operator approval.
- **Do not** commit directly to `origin` (canonical
  `pointsav/content-wiki-documentation`). Humans do not write to
  canonical directly for engineering repos.

### Remotes currently configured

| Remote | Target | Notes |
|---|---|---|
| `origin` | `pointsav/content-wiki-documentation` | Canonical. Push only via Stage 6 promotion. |
| `origin-staging-j` | `jwoodfine/content-wiki-documentation` | Staging-tier mirror — Jennifer. |
| `origin-staging-p` | `pwoodfine/content-wiki-documentation` | Staging-tier mirror — Peter. |
| `upstream` | `pointsav/pointsav-monorepo` | **Legacy artefact.** Not used by this repo's flow. Candidate for removal — tracked in `NEXT.md`. |

Commit signing is not yet enabled in this repo; workspace §3
tracks signing extension as a Tier 1 Phase B2 item.

## 6. Content rules specific to this repo

Inherited from workspace §6 and reaffirmed here because this repo's
content is publicly served at `documentation.pointsav.com`:

- **Bilingual READMEs.** `README.md` and `README.es.md` at repo root
  are both maintained. The wiki content itself (articles in category
  subdirectories) is English-only unless a future decision adds
  Spanish content.
- **Canonical names.** Names from the Nomenclature Matrix are used
  verbatim in article titles, slugs, and wikilink targets. No
  synonyms, no legacy prefixes.
- **BCSC disclosure rule.** Sovereign Data Foundation is referred
  to in planned / intended terms only. Never as a current equity
  holder or active governance body. This rule applies with full
  weight here because content in this repo is public once served.
- **ADR hard rules.** SYS-ADR-07 (no AI on structured data), SYS-ADR-10
  (F12 checkpoint), SYS-ADR-19 (no automated AI publishing). Content
  in this repo does not invoke AI; articles that describe these
  ADRs must describe them accurately as written.
- **Edit in place.** No `_V2` / `_V3` duplicate files. Use Git
  history for versioning.

## 7. Migration state (as of 2026-04-23)

This repo predates the `app-mediakit-knowledge` contract. Rule
scaffolding is now in place — the four files under `.claude/rules/`
describe what valid content looks like, where files belong, what
cleanup is in flight, and what is queued for cross-repo handoff.

The content itself still does not conform to the contract. Visible
gaps:

- No `index.md` at repo root.
- No category subdirectories; articles are currently flat at root.
- Filename-case inconsistency: `topic-*.md`, `TOPIC-*.md`, `TOPIC_*.md`
  all coexist.
- Structured-record files (`topic-*.yaml`, `sys-adr-*.yaml`,
  `service-*-01.yaml`, `os-workplace-01.yaml`) sit at root without
  markdown bodies; each needs classification (become article / become
  article front-matter / move cross-repo to the owning service crate
  in the monorepo).

Normalisation is queued, not executed. Per-file decisions are
tracked in `.claude/rules/cleanup-log.md`; higher-level work items
are tracked in `NEXT.md`.

## 8. Where to look next

- `NEXT.md` — repo-scope open items and migration queue.
- `.claude/rules/content-contract.md` — what valid content looks like.
- `~/Foundry/CLAUDE.md` — workspace guide (inherited).
- `~/Foundry/IT_SUPPORT_Nomenclature_Matrix_V8.md` — names, prefixes,
  conventions (authoritative per workspace §5).
- `~/Foundry/NEXT.md` — workspace-level open items, including anything
  cross-repo that touches this repo.
