# Cleanup Log Archive — content-wiki-documentation/content-wiki-documentation

Closed entries archived from `cleanup-log.md`.
Open items remain in `cleanup-log.md`.

---

## Closed

### 2026-05-07 — Root layout defects: guide-proofreader-distillation.md + topic-radical-proofreader-ui.md

`Closed: 2026-05-08.` Both files were untracked drafts in `foundry-draft-v1` state. Removed with `rm`. Source drafts remain in project-proofreader cluster for proper pipeline routing.

### 2026-05-06 — BIM batch: guide-climate-zone-tokens routed to TOPIC

`Closed: 2026-05-08.` Resolved via option (b) — converted to TOPIC and committed at `15d0942` as `reference/climate-zone-tokens.md` + `.es.md`. Stale GUIDE removed from woodfine-fleet-deployment cluster at `a928b70`.

### 2026-05-06 — Body H1 batch remediation

`Closed: 2026-05-08.` 103 files fixed via batch script. `infrastructure/guide-telemetry.md` and `applications/user-guide-2026-03-30-v2.md` both deleted — neither conformed to contract and neither had frontmatter. No git rm needed (untracked).

### 2026-05-06 — Phase D + E batch (project-editorial)

`Closed: 2026-05-08.` Phase D: 28 Spanish pairs committed. Phase E: bcsc_class + status sweep — 213 files total. No open items.

### 2026-05-06 — GIS service topics + design-system/ category (project-editorial)

`Closed: 2026-05-08.` Commits 4d5a499 + 0bf2f6d complete. Named competitor references stripped per C15. No open items.

### 2026-04-30 — Wikipedia normalization pass + migration

`Closed: 2026-05-08.` Root `topic-*.md` files verified migrated to category directories. No root-level tracked `topic-*.md` files remain. `topic-compounding-substrate.md` does not exist in git — `architecture/compounding-substrate.md` is canonical.

### 2026-04-28 — 12 bilingual TOPIC pairs + rename + deletions (project-language)

`Closed: 2026-05-08.` Root-pattern files from this batch verified already migrated to category directories (architecture/, services/, systems/, governance/, reference/) in prior sessions. No root-level tracked `topic-*.md` files remain.

### 2026-04-27 — Phase 4 + Part D + style-guide TOPICs (project-language, 3 sessions)

`Closed: 2026-05-08.` All root-pattern files from this batch verified migrated. `topic-contributor-model.md` is canonical form. No root-level tracked `topic-*.md` files remain.

### 2026-04-23 — Migration to contract-conforming layout

`Closed: 2026-05-08.` Category directories created and populated. YAML records converted to bilingual stubs. Root `TOPIC-*.md` / `TOPIC_*.md` files absent. `index.md` at root exists. Layout conforms to contract.

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

`Closed: 2026-05-08.` Crate landed in `pointsav-monorepo/app-mediakit-knowledge/` via Stage 6 promotion (prior sessions). ZIP was untracked; confirmed already deleted from filesystem. Handoff entry in `handoffs-outbound.md` closed.

### 2026-04-23 — `upstream` remote is a legacy artefact

`Closed: 2026-05-08.` Remote was already absent — removed in a prior session. CLAUDE.md §5 table entry retained as historical note; no `git remote remove` needed.

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
