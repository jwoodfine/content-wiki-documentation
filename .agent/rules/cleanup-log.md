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

Commits `96e221d`, `91b8910`, `f470a11`, `aad5c7d`, `09637ed`, `ad88bc3`, `1868a20`, `e7b14c3`, `11d617a`, `500f201`, `dcec4f6`, `5f17aa1`, `5880bd0`, `dc9acec`, `0a5b96f` across two sessions; canonical promote landed at 2026-05-08T20:55Z (5880bd0). Two further commits on staging (dc9acec, 0a5b96f) since the promote.

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
- **Step 5 priority 4c — applications category COMPLETE.** 3 named app-* EN+ES pairs (`500f201` app-mediakit-knowledge; `5f17aa1` app-mediakit-marketing + app-orchestration-gis); 4 design-intent articles moved `applications/` → `architecture/` + location-intelligence-platform refined + launch announcement retired (`dc9acec`); frontmatter+lead edits to 4 moved articles (`0a5b96f`).
- Stage 6 reconciliation merge with origin/main (`dcec4f6` — 7 conflicts resolved) and cleanup-log archive split (`5880bd0`) both promoted to canonical at 2026-05-08T20:55Z.

**Open — GUIDEs (~77 files):** Step 5 priority 5 — in progress this session;
scaffold-batch + operational-starter dispatched.

---

## Closed

> Detailed session-note text archived in `cleanup-log-archive.md`.

- **2026-05-08 — competitor-name violation in zero-container-inference.md:** fixed 2026-05-08 — "What this rules out" section now uses generic categories (managed container orchestration platforms, container runtime systems, etc.) per workspace §6.
- **2026-05-08 — Category migration verification:** verified complete 2026-05-08 — `find content-wiki-documentation -maxdepth 1 -name 'topic-*.md'` returns no tracked root-level legacy files; migration to category subdirectories complete from earlier sessions.
- **2026-05-07 — Root layout defects (guide-proofreader-distillation, topic-radical-proofreader-ui):** untracked drafts removed `rm`; source drafts remain in project-proofreader cluster.
- **2026-05-06 — BIM batch: guide-climate-zone-tokens routed to TOPIC:** option (b) — `15d0942` (TOPIC) + `a928b70` (stale GUIDE removed).
- **2026-05-06 — Body H1 batch remediation:** 103 files batch-fixed; `infrastructure/guide-telemetry.md` + `applications/user-guide-2026-03-30-v2.md` both deleted in canonical sweep `c2b7ac9`.
- **2026-05-06 — Phase D + E batch:** 28 ES pairs committed; bcsc_class + status sweep on 213 files.
- **2026-05-06 — GIS service topics + design-system/ category:** `4d5a499` + `0bf2f6d` complete; named competitors stripped per C15.
- **2026-04-30 — Wikipedia normalization pass + migration:** root `topic-*.md` files verified migrated; canonical at `architecture/compounding-substrate.md`.
- **2026-04-28 — 12 bilingual TOPIC pairs + rename + deletions:** all root-pattern files from this batch migrated to category directories.
- **2026-04-27 — Phase 4 + Part D + style-guide TOPICs:** all root-pattern files migrated; `topic-contributor-model.md` is canonical form.
- **2026-04-23 — Migration to contract-conforming layout:** category directories created + populated; layout conforms to contract.
- **2026-04-23 — YAML-only structured records classification:** 14 YAML records converted to bilingual stub articles (sys-adr-06–19, service-content/egress/email/people, os-workplace, 3d-asset-tokens, system-slm, system-udp); originals git rm'd.
- **2026-04-23 — Filename-case normalisation:** root-level `TOPIC-*.md` / `TOPIC_*.md` verified absent.
- **2026-04-23 — RESEARCH-BIM-MARKET.md classification:** converted to `reference/bim-market-context.md` + `.es.md` stub; competitive landscape section removed per C15.
- **2026-04-23 — app-mediakit-knowledge.zip cross-repo handoff:** crate landed in `pointsav-monorepo/app-mediakit-knowledge/` via Stage 6.
- **2026-04-23 — `upstream` remote legacy artefact:** remote absent; CLAUDE.md §5 table entry retained as historical note.
- **2026-04-23 — Naming convention draft:** `naming-convention.md` ratified 2026-05-07; four operator decisions recorded in §13.
- **2026-04-23 — README-pointsav-wiki.md:** deleted 2026-04-28 at commit `6c1b178`.
- **2026-04-23 — glossary-documentation.csv:** closed 2026-05-02; converted to `reference/glossary-documentation.md`.
- **2026-05-06 — CLAUDE.md §6 bilingual drift:** fixed 2026-05-07 — "English-only" updated to bilingual per workspace §6.
- **2026-05-06 — naming-convention.md §10 ratification:** ratified 2026-05-07; `design-system/` added as 10th category.
- **2026-05-06 — pointsav-gis-engine.md redlinks:** fixed 2026-05-07; `[[guide-totebox-orchestration-gis]]` + `[[co-location-methodology]]` replaced with plain-text planned-article notes.
