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

### 2026-05-08 — Step 5 register-correct rewrite pass (project-editorial)

Commits `96e221d`, `91b8910`, `f470a11`, `aad5c7d`, `09637ed`, `ad88bc3`, `1868a20`, `e7b14c3`, `11d617a`, `500f201` across two sessions.

**Complete:**
- 4 high-urgency architecture/governance EN+ES pairs rewritten (compounding-substrate,
  doorman-protocol, ontological-governance, leapfrog-2030-architecture) — `96e221d`
- 3 services EN+ES pairs rewritten (service-slm, service-email, service-fs-architecture) — `91b8910`
- 124 files: frontmatter bug (## headings inside YAML block) — batch fixed in `f470a11`
- 19 files: `{{gli|X}}` template markup — batch replaced with plain term in `f470a11`
- 5 Master Totebox Orchestration TOPIC EN+ES pairs published (totebox-orchestration-development,
  pairing-as-permission, os-orchestration, totebox-session, personnel-permissions) — `aad5c7d`,
  `09637ed`, `ad88bc3`
- 1 governance EN+ES pair published (favicon-matrix) — `1868a20`
- **12 services-remaining EN+ES pairs refined** (service-people, service-extraction, service-search,
  message-courier, service-business-clustering, service-places-filtering, fs-anchor-emitter,
  service-fs-security-compliance, service-fs-data-lake, service-slm-totebox-sysadmin,
  template-ledger, pointsav-gis-engine) — `e7b14c3` + `11d617a`
- 1 application EN+ES pair refined in-flight (app-mediakit-knowledge — schema upgrade + lead) — `500f201`

**Open — applications category (Phase 4c paused):** app-mediakit-marketing,
app-orchestration-gis, and others (Step 5 priority 4c)

**Open — GUIDEs (~72 files):** Step 5 priority 5

**Open — category migration:** root topic-*.md files → category subdirectories
(unblocked 2026-05-07 ratification). Tracked in existing open entry below.

**Open — competitor-name violation in zero-container-inference.md:** "What this rules out"
section names Cloud Run, Kubernetes, SkyPilot, cargo-chef explicitly. Workspace §6
prohibits competitive comparisons by name. Surfaced via Phase 3 of 2026-05-08 session;
not actioned in scope. Replace with generic categories (managed container orchestration
platforms, container runtime systems, multi-cloud abstraction frameworks, OCI image
registries) at next editorial pass.

Stage 6 promotions pending across 10 commits — Stage 6 reconciliation merge with origin/main
in progress this session.

---

## Closed

### 2026-05-06 — BIM batch: guide-climate-zone-tokens routed to TOPIC

`Closed: 2026-05-08.` Resolved via option (b) — converted to TOPIC and committed at `15d0942` as `reference/climate-zone-tokens.md` + `.es.md`. Stale GUIDE removed from woodfine-fleet-deployment cluster at `a928b70`.

### 2026-05-07 — Root layout defects: guide-proofreader-distillation.md + topic-radical-proofreader-ui.md

`Closed: 2026-05-08.` Both files were untracked drafts in `foundry-draft-v1` state. Removed with `rm`. Source drafts remain in project-proofreader cluster for proper pipeline routing.

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

### Older closed entries (full session-note text archived in `cleanup-log-archive.md`)

- **2026-04-23 — Naming convention draft:** `naming-convention.md` ratified 2026-05-07. Status promoted Draft → Active. Four operator decisions recorded in §13.
- **2026-04-23 — README-pointsav-wiki.md:** deleted 2026-04-28 at commit 6c1b178 (redundant draft).
- **2026-04-23 — glossary-documentation.csv:** closed 2026-05-02. Converted to `reference/glossary-documentation.md`.
- **2026-05-06 — CLAUDE.md §6 bilingual drift:** fixed 2026-05-07 — "English-only" updated to bilingual per workspace §6.
- **2026-05-06 — naming-convention.md §10 ratification:** ratified 2026-05-07. `design-system/` added as 10th category.
- **2026-05-06 — pointsav-gis-engine.md redlinks:** fixed 2026-05-07 — `[[guide-totebox-orchestration-gis]]` + `[[co-location-methodology]]` replaced with plain-text planned-article notes.
