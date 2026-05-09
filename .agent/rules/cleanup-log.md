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

### 2026-05-09 — Category-balance audit: COMPLETE — taxonomy ratified, all imbalances resolved

`Closed: 2026-05-09.` 5 commits closed the audit:
- `729c39b` — Schema scrub (24 files; foundry-topic-v1 → foundry-doc-v1, missing-schema fills, slug-collision setup)
- `d0b5b58` — 5 slug collisions resolved (10 files git rm'd, kept canonical version of each)
- `333a59d` — 7 articles moved architecture/ → services/ (2) + infrastructure/ (5)
- `eaac482` — 11 articles moved reference/ → design-system/ (visual/UX content)
- `2e843fb` — Taxonomy ratified: architecture/ split into architecture/+substrate/+patterns/; company/+help/ retired

Final wiki state: 10 active categories, no empties, no category >2× mean. naming-convention.md §4 + §13 updated. Original 4 imbalances all resolved (architecture oversized → split; reference oversized → trimmed; applications/infrastructure undersized → infrastructure populated, applications stable; company/help empty → retired).

Original 2026-05-09 entry kept here for audit trail:

### 2026-05-09 — Category-balance analysis: 4 imbalances surfaced; 7 mechanical moves done; 3 deeper questions for operator

Operator dispatched a category-balance check before live wiki updates: "we don't want any blanks or categories that are too big or too small."

**Pre-rebalance distribution (after schema-clean + slug-collision fix):**

| Category | EN | Status |
|---|---|---|
| architecture | 82 | TOO BIG (~4× mean) |
| reference | 55 | TOO BIG (~2.5× mean) |
| design-system | 25 | OK |
| governance | 20 | OK (at mean) |
| services | 17 | OK |
| systems | 10 | borderline-small |
| applications | 4 | TOO SMALL |
| infrastructure | 4 | TOO SMALL |
| company | 0 | EMPTY |
| help | 0 | EMPTY |

**Mean: 21.7. Median: 17.** Four imbalances: 2 oversized, 2 undersized, 2 empty.

**Mechanical moves done this session (commit `<this-commit>`):**

7 articles (14 files) moved from architecture/ to better-fit categories:
- → services/ (was 17, now 19): service-slm-yoyo-operational, service-wallet-settlement (both were named services in the wrong category).
- → infrastructure/ (was 4, now 9): worm-ledger-architecture, worm-ledger-design, worm-ledger-storage-architecture (storage = infrastructure), sovereign-mesh, sovereign-telemetry (network/telemetry = infrastructure).

**Post-rebalance distribution:**

| Category | EN | Δ |
|---|---|---|
| architecture | 75 | −7 |
| reference | 55 | (unchanged this commit) |
| design-system | 25 | — |
| governance | 20 | — |
| services | 19 | +2 |
| systems | 10 | — |
| infrastructure | 9 | +5 |
| applications | 4 | — |
| company | 0 | — |
| help | 0 | — |

**Three deeper questions surfaced for operator:**

1. **Split architecture/?** At 75 EN articles it's still 3× the mean. Natural sub-groupings exist (substrate concepts, design patterns, doctrine articles) but URL depth is capped at 2 per content-contract.md §2 — splitting requires adding a top-level category, which is a naming-convention.md taxonomy change. Candidate splits: substrate/ (compounding-substrate, apprenticeship-substrate, language-protocol-substrate, etc., ~25 articles); patterns/ (article-shell-leapfrog, source-of-truth-inversion, meta-repo-pattern, etc., ~10 articles).

2. **Split reference/ or move design-system articles out?** reference/ has 55 articles including ~11 that look like they belong in design-system/ (brand-family-swatch, brand-typography, country-filter-chips, map-side-drawer, map-stats-panel, neurodiversity-typography-standards, properties-panel-accessibility, spatial-tree-accessibility, viewport-3d-accessibility, climate-zone-tokens, zoom-tier-reveal-pattern). Moving these would: reference/ 55 → 44, design-system/ 25 → 36.

3. **Populate company/ and help/, or retire from taxonomy?** Per naming-convention.md §13 ratification, both are intentional first-class categories — but they're empty. Either populate (write stub articles for `pointsav`, `woodfine-management-corp`, `roadmap-2026-2028`, `bcsc-disclosures`, `contributing-as-engineer`, etc.) or retire and reduce taxonomy from 10 → 8 categories.

This session: actioned the unambiguous mechanical moves (7 files) + slug collision fix (separate commit `d0b5b58`). The taxonomy-level decisions on (1)–(3) need operator input. Surfaced via outbox addendum.

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
