# NEXT.md — content-wiki-documentation

> **Scope: this repo only.** Cross-repo and workspace-level open
> items live at `~/Foundry/NEXT.md`. Per-file defects and rolling
> cleanup decisions live at `.claude/rules/cleanup-log.md`; this
> file holds the higher-level work items.
>
> Read at session start when a Root Claude opens in this repo. Update
> at session end when repo-scope open items change.

Last updated: 2026-04-30.

---

## Currently open

- **Evolve `glossary-documentation.csv` as unified master glossary.**
  The file at repo root is now the active unified glossary covering
  TOPIC-*, GUIDE-*, README-*, and DESIGN-* vocabulary — do not wait
  for service-content to own it programmatically. Current state
  preserved as `glossary-documentation-v1-2026-04-30.csv` (snapshot).
  Evolution plan: (1) fill definitions and Spanish for existing 271
  terms; (2) add new terms as TOPIC/GUIDE/DESIGN content lands from
  project-language and project-design pipelines; (3) add `Content_Scope`
  column when multi-type coverage warrants it. Slow and continuous —
  no single migration pass.

- **Content normalisation to contract-conforming layout.**
  Execute the migration described in `cleanup-log.md`: add
  `index.md` at repo root, create category directories
  (`architecture/`, `services/`, `governance/`, others tbd), move
  and rename existing topic files, classify structured-record YAML
  files, write category `_index.md` pages, rewrite cross-references
  to `[[slug]]` wikilinks. Sequencing candidate: one category at a
  time, beginning with `architecture/` (already seeded).

- **Remove the `upstream` remote.** Points at
  `pointsav/pointsav-monorepo.git`, unused by this repo's flow.
  Removal is `git remote remove upstream` — non-destructive but
  requires explicit operator approval.

## Recently closed

- 2026-04-23 — Repo-level `CLAUDE.md` created.
- 2026-04-23 — `.claude/rules/` bootstrap complete:
  `content-contract.md`, `repo-layout.md`, `cleanup-log.md`,
  `handoffs-outbound.md` all written.

## Pointers

- Workspace-level open items: `~/Foundry/NEXT.md`
- Per-file cleanup decisions: `.claude/rules/cleanup-log.md`
- Cross-repo handoffs: `.claude/rules/handoffs-outbound.md`
- Workspace changelog: `~/Foundry/CHANGELOG.md`
- Nomenclature Matrix: `~/Foundry/IT_SUPPORT_Nomenclature_Matrix_V8.md`
