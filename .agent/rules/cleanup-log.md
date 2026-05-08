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

Last updated: 2026-05-08.

---

## Open

### 2026-05-07 — Root layout defects: guide-proofreader-distillation.md + topic-radical-proofreader-ui.md

`Closed: 2026-05-08.` Both files were untracked drafts in `foundry-draft-v1` state (not yet through language-pass pipeline). Removed with `rm` — not committed, so no `git rm` needed. Source drafts remain in project-proofreader cluster for proper pipeline routing.

### 2026-05-06 — BIM batch: 5 EN+ES TOPIC pairs committed (project-editorial)

Commit `c6d233d` — `reference/bim-token-what-it-is.md`, `bim-token-three-layers.md`, `open-bim-regulatory-acceptance.md` + pairs; `architecture/building-design-system-bim.md`, `city-code-as-composable-geometry.md` + pairs.

**Open:** `guide-climate-zone-tokens.md` — commit 9e6d311 on `cluster/project-language` was lost when project-language renamed to project-editorial (commit 7876f28). Source draft is intact at `clones/project-bim/.agent/drafts-outbound/guide-climate-zone-tokens.draft.md` and has been routed to project-editorial inbox. NEXT.md has delivery item.

### 2026-05-06 — Body H1 batch remediation (project-editorial)

103 files fixed via batch script — duplicate body H1 removed from all category articles with foundry-doc-v1 frontmatter.

**Open — `infrastructure/guide-telemetry.md`:** starts with H1 + no frontmatter; Woodfine-specific operational content. Decision needed: (a) normalize as wiki article, (b) move to woodfine-fleet-deployment as GUIDE, or (c) remove. H1 retained until disposition decided.

**Open — `applications/user-guide-2026-03-30-v2.md`:** no frontmatter, uses `# Part I:` / `# Part II:` as chapter markers. Needs classification pass.

### 2026-05-06 — Phase D + E batch (project-editorial)

Phase D: 28 Spanish strategic-adaptation pairs committed across architecture/, governance/, services/, systems/. Phase E: bcsc_class + status sweep — 213 files total.

### 2026-05-06 — GIS service topics + design-system/ category (project-editorial)

Commits 4d5a499 + 0bf2f6d: GIS service topics, app-orchestration-gis bilingual pair, design-system/ category (30 files — 6 foundation TOPICs + 16 component guides). Named competitor references stripped per C15 decision.

### 2026-04-30 — Wikipedia normalization pass + 5 architecture/reference TOPIC pairs

40 root topic-*.md files normalized (frontmatter, quality grades, See Also, References, body H1 removed). 5 new bilingual pairs committed to `architecture/` and `reference/`.

`Closed (migration): 2026-05-08.` Root `topic-*.md` files verified already migrated to category directories in prior sessions — no root-level tracked `topic-*.md` files remain. Cleanup-log entry was stale.

**Open:** `topic-compounding-substrate.md` at root — verified does NOT exist in git (already migrated or removed). Entry is stale; closing. `architecture/compounding-substrate.md` is canonical.

### 2026-04-28 — 12 bilingual TOPIC pairs + rename + deletions (project-language)

12 bilingual TOPIC pairs committed at repo root. `topic-service-parser` renamed to `topic-service-extraction`. `README-pointsav-wiki.md` deleted (commit 6c1b178).

**Open:** category migration for these root-pattern files — pending (migration unblocked as of 2026-05-07 ratification).

### 2026-04-27 — Phase 4 + Part D + style-guide TOPICs (project-language, 3 sessions)

14 bilingual TOPIC pairs added at repo root: Phase 4 substrate-explainers, Part D apprenticeship/compounding/contributor-model, style-guide-readme/topic/guide pairs.

**Open:** category migration for all these root-pattern files (unblocked 2026-05-07). `topic-contributor-model.md` is canonical form (not `topic-four-tier-contributor-model.md`).

### 2026-04-23 — Migration to contract-conforming layout

Normalisation pass required: add `index.md` at root, create category directories, move legacy `topic-*.md` / `TOPIC-*.md` / `TOPIC_*.md` files into categories normalising to lowercase kebab, write `_index.md` per category, rewrite wikilinks. Sequencing: migrate one category at a time. Category taxonomy now ratified (2026-05-07).

### 2026-04-23 — YAML-only structured records need classification

`Closed: 2026-05-08.` All YAML records converted to bilingual stub articles and git rm'd:
- `sys-adr-06` through `sys-adr-19` → `governance/sys-adr-{06,07,08,10,11,13,14,15,16,17,18,19}.md` + `.es.md`
- `service-content-01.yaml`, `service-egress-01.yaml` → `services/service-content.md`, `services/service-egress.md` + pairs
- `service-email-01.yaml`, `service-people-01.yaml` → existing articles in `services/`; YAMLs removed
- `os-workplace-01.yaml` → `systems/os-workplace.md` + `.es.md`
- `3d-asset-tokens.yaml` → `architecture/3d-asset-tokens.md` + `.es.md`
- `system-slm.yaml` → existing `services/service-slm.md`; YAML removed
- `system-udp.yaml` → `architecture/sovereign-mesh.md` + `.es.md`

### 2026-04-23 — Filename-case normalisation

`Closed: 2026-05-08.` Root-level tracked `TOPIC-*.md` / `TOPIC_*.md` files verified absent — already migrated in prior sessions. No action needed.

### 2026-04-23 — `RESEARCH-BIM-MARKET.md` classification needed

`Closed: 2026-05-08.` Converted to `reference/bim-market-context.md` + `.es.md` stub. Section 3 (competitive landscape with named vendors) removed per C15 decision. Standards/regulatory/technical content preserved. `RESEARCH-BIM-MARKET.md` git rm'd.

### 2026-04-23 — `app-mediakit-knowledge.zip` cross-repo handoff

`Closed: 2026-05-08.` Crate landed in `pointsav-monorepo/app-mediakit-knowledge/` via Stage 6 promotion (prior sessions). ZIP was untracked; confirmed already deleted from filesystem. Handoff entry in `handoffs-outbound.md` pending closure.

### 2026-04-23 — `upstream` remote is a legacy artefact

**Open:** `git remote remove upstream` pending explicit operator approval (non-destructive; points to pointsav-monorepo which is not this repo's flow).

---

## Closed

> Full session-note text archived in `cleanup-log-archive.md`.

- **2026-04-23 — Naming convention draft:** `naming-convention.md` ratified 2026-05-07. Status promoted Draft → Active. Four operator decisions recorded in §13.
- **2026-04-23 — README-pointsav-wiki.md:** deleted 2026-04-28 at commit 6c1b178 (redundant draft).
- **2026-04-23 — glossary-documentation.csv:** closed 2026-05-02. Converted to `reference/glossary-documentation.md`.
- **2026-05-06 — CLAUDE.md §6 bilingual drift:** fixed 2026-05-07 — "English-only" updated to bilingual per workspace §6.
- **2026-05-06 — naming-convention.md §10 ratification:** ratified 2026-05-07. `design-system/` added as 10th category.
- **2026-05-06 — pointsav-gis-engine.md redlinks:** fixed 2026-05-07 — `[[guide-totebox-orchestration-gis]]` + `[[co-location-methodology]]` replaced with plain-text planned-article notes.
