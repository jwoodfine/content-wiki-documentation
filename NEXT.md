# NEXT.md — content-wiki-documentation

> **Scope: this repo only.** Cross-repo and workspace-level open
> items live at `~/Foundry/NEXT.md`. Per-file defects and rolling
> cleanup decisions live at `.claude/rules/cleanup-log.md`; this
> file holds the higher-level work items.
>
> Read at session start when a Root Claude opens in this repo. Update
> at session end when repo-scope open items change.

Last updated: 2026-05-18.

---

## Currently open

- **Evolve `glossary-documentation.csv` as unified master glossary.**
  Slow and continuous — no single migration pass. (1) fill definitions
  and Spanish for existing terms; (2) add new terms as content lands
  from project-editorial pipeline; (3) add `Content_Scope` column when
  multi-type coverage warrants it.

- **D1/D2: Verify `featured-topic.yaml` + `leapfrog-facts.yaml` slugs** are path-qualified after Wave 1 migration. Quick grep check.

- **D10: Wikilink validation pass** — run after Stage 6 binary rebuild to confirm P0-C (bare-slug resolver) fixes all 280+ previously-broken links.

## Currently open

- **D10: Wikilink validation pass** — run after Stage 6 binary rebuild to confirm P0-C (bare-slug resolver) fixes all 280+ previously-broken links.

## Recently closed

- 2026-05-19 — **D3 COMPLETE** — `substrate/` + `patterns/` _index MOC pages expanded to full coverage (7→32 and 3→10 articles, EN+ES, commit `cf72e67`).
- 2026-05-19 — **D6 COMPLETE** — governance category: `sovereign-airlock-doctrine` rewritten; `moonshot-initiatives`, `ontological-governance`, `sovereign-replacement-initiative` elevated stub→complete; `_index.md`+`.es.md` expanded with 8 unlisted articles (commit `a07bdf5`).
- 2026-05-19 — **D1/D2 VERIFIED** — `featured-topic.yaml` + `leapfrog-facts.yaml` slugs confirmed path-qualified.
- 2026-05-18 — **D5 COMPLETE** — `short_description` added to all 162 EN+ES articles (`c8192fc`). All wiki articles now surface subtitle text in article chrome.
- 2026-05-18 — **D8 COMPLETE** — `governance/_index.md` + `design-system/_index.md` frontmatter fixed (type, quality, short_description, paired_with).
- 2026-05-18 — **D7/D9 MOOT** — D7: guide-component files moved to design-system repo (Batch 2 handoff); D9: AGENT.md allowed per repo-layout.md + SYSTEM_FILE_STEMS.
- 2026-05-18 — `substrate/nightly-datagraph-rebuild.md` + `.es.md` stub content expanded from placeholder to full article.
- 2026-05-13 — `os-network-admin`, `os-privategit`, `co-location-methodology`, `development-regions` — **full prose expanded** (EN+ES pairs, `status: stable`, `quality: complete`). Four commits on staging.
- 2026-05-13 — `guide-climate-zone-tokens` routing decision closed — option (b): `design-system/climate-zone-tokens.md` (prior session commit `15d0942`).
- 2026-05-08 — Content normalisation to contract-conforming layout **complete.** Category dirs created; YAML records → bilingual stubs; root `TOPIC-*.md` files migrated; `index.md` at root exists. See `cleanup-log.md`.
- 2026-05-08 — `upstream` remote **removed** (was already absent from prior session).
- 2026-05-08 — 4 red-link stubs created: `systems/os-network-admin.md`, `systems/os-privategit.md`, `architecture/co-location-methodology.md`, `architecture/development-regions.md`.
- 2026-05-08 — `content-contract.md §4` updated: `index.md` / `category: root` example added.
- 2026-04-23 — Repo-level `CLAUDE.md` created.
- 2026-04-23 — `.agent/rules/` bootstrap complete.

## Authorship Roadmap (Red Links)

Stubs exist (status: stub) — red links resolved. Full prose pending:

- [ ] `ConsoleOS` — `systems/os-console.md` (stub needed)
- [ ] `InfrastructureOS` — `systems/os-infrastructure.md` (stub needed)
- [ ] `MediaKitOS` — `systems/os-mediakit.md` (stub needed)
- [x] `NetworkAdminOS` — `systems/os-network-admin.md` (**full prose 2026-05-13**)
- [ ] `OrchestrationOS` — `systems/os-orchestration.md` (stub needed)
- [x] `PrivateGitOS` — `systems/os-privategit.md` (**full prose 2026-05-13**)
- [ ] `ToteboxArchive` — `systems/os-totebox-archive.md` (stub needed)
- [ ] `ToteboxOS` — `systems/os-totebox.md` (stub needed)
- [x] `co-location-methodology` — `architecture/co-location-methodology.md` (**full prose 2026-05-13**)
- [x] `development-regions` — `architecture/development-regions.md` (**full prose 2026-05-13**)

## Pointers

- Workspace-level open items: `~/Foundry/NEXT.md`
- Per-file cleanup decisions: `.claude/rules/cleanup-log.md`
- Cross-repo handoffs: `.claude/rules/handoffs-outbound.md`
- Workspace changelog: `~/Foundry/CHANGELOG.md`
- Nomenclature Matrix: `~/Foundry/IT_SUPPORT_Nomenclature_Matrix_V8.md`
