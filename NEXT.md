# NEXT.md — content-wiki-documentation

> **Scope: this repo only.** Cross-repo and workspace-level open
> items live at `~/Foundry/NEXT.md`. Per-file defects and rolling
> cleanup decisions live at `.claude/rules/cleanup-log.md`; this
> file holds the higher-level work items.
>
> Read at session start when a Root Claude opens in this repo. Update
> at session end when repo-scope open items change.

Last updated: 2026-05-12.

---

## Currently open

- **Evolve `glossary-documentation.csv` as unified master glossary.**
  Slow and continuous — no single migration pass. (1) fill definitions
  and Spanish for existing terms; (2) add new terms as content lands
  from project-editorial pipeline; (3) add `Content_Scope` column when
  multi-type coverage warrants it.

- **`guide-climate-zone-tokens.md` — pending project-editorial routing.**
  Routing message sent to project-editorial inbox 2026-05-08. Decision:
  (a) commit to woodfine-fleet-deployment as GUIDE or (b) convert to
  TOPIC and commit to reference/climate-zone-tokens.md here.
  Tracked in `.agent/rules/cleanup-log.md`.

## Recently closed

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
- [x] `NetworkAdminOS` — `systems/os-network-admin.md` (stub created 2026-05-08)
- [ ] `OrchestrationOS` — `systems/os-orchestration.md` (stub needed)
- [x] `PrivateGitOS` — `systems/os-privategit.md` (stub created 2026-05-08)
- [ ] `ToteboxArchive` — `systems/os-totebox-archive.md` (stub needed)
- [ ] `ToteboxOS` — `systems/os-totebox.md` (stub needed)
- [x] `co-location-methodology` — `architecture/co-location-methodology.md` (stub created 2026-05-08)
- [x] `development-regions` — `architecture/development-regions.md` (stub created 2026-05-08)

## Pointers

- Workspace-level open items: `~/Foundry/NEXT.md`
- Per-file cleanup decisions: `.claude/rules/cleanup-log.md`
- Cross-repo handoffs: `.claude/rules/handoffs-outbound.md`
- Workspace changelog: `~/Foundry/CHANGELOG.md`
- Nomenclature Matrix: `~/Foundry/IT_SUPPORT_Nomenclature_Matrix_V8.md`
