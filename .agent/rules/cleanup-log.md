# Cleanup log — media-knowledge-documentation

> Rolling log of in-flight cleanup work, decisions, and open
> questions in this repo. Most-recent entries at top. Entries
> move from Open to Closed in place; closed entries retain
> their opened-on date for historical reference.
>
> Trivial edits (single-file typo fixes, formatting tweaks) do
> not belong here. Meaningful cleanup — renames across files,
> layout-rule enforcement, defect resolution, surfaced open
> questions — does.

Last updated: 2026-07-09.

---

## Open

---

### 2026-07-09 — project-console drafts-outbound sweep: 3 TOPIC drafts already consolidated (2026-06 Phase C); 1 live banned-vocab defect fixed: COMPLETE

`Closed: 2026-07-09.`

**Scope:** project-editorial swept 6 drafts staged by project-console in
`.agent/drafts-outbound/` (all `route_to: project-editorial`, never
previously actioned per the routing audit that surfaced them). Consolidation
check against this repo before authoring found that 3 of the 6 — the TOPIC
drafts — were **already published**, merged into canonical articles during
the 2026-06-20 "Phase C A1d" batch (commit `9ad6df5`, which explicitly lists
`capability-geometry` as one of "2 merge-checks resolved") and the earlier
Phase C A1b rebalance (`aeec5eb`) for `os-console-architecture`:

| Draft | Already-published canonical | Verdict |
|---|---|---|
| `TOPIC-capability-geometry.draft.md` | `substrate/capability-geometry.md` | CONSOLIDATED — published version is the draft + wikilinks + trademark footer + Doctrine-citation strip. No new content to merge. |
| `TOPIC-capability-geometry.es.draft.md` | `substrate/capability-geometry.es.md` | CONSOLIDATED — same. |
| `TOPIC-os-console-architecture.draft.md` | `systems/os-console-architecture.md` + `.es.md` (bilingual pair already exists — draft's `bilingual_pair_required: true` / bare ES gap was stale) | CONSOLIDATED — published version is a strict superset (accurate `Cartridge` trait matching source, full six-cartridge registration table, terminal-negotiation detail, OSC 8 section) of the thinner draft. No new content to merge. |

No new wiki commits were needed for these three articles' bodies. Verification
pass over the two live articles while confirming the consolidation surfaced one
real defect, fixed this session: `systems/os-console-architecture.md` +
`.es.md` carried a descriptive (non-proper-noun) use of "Sovereign" —
`## Sovereign deployment intent` / `## Intención de despliegue soberano` —
which is on the workspace Do-Not-Use list (`POINTSAV-Project-Instructions.md`
§5). Retitled to `## Customer-rooted deployment intent` /
`## Intención de despliegue centrada en el cliente`; body text needed no
further change. `last_edited` bumped to 2026-07-09 on both files. (`Two-Bottoms
Sovereign Substrate` in `capability-geometry.md`/`.es.md` was checked and left
unchanged — it is an established proper noun used consistently across the
substrate corpus, e.g. `substrate/system-substrate-doctrine.md`,
`substrate/capability-ledger-substrate.md`.)

The 3 stale draft copies were removed from `project-editorial`'s
`.agent/drafts-outbound/` in the same session (cluster-branch commit, not
this repo) since their content is superseded by the live articles.

The remaining 3 drafts from the same batch (`GUIDE-jennifer-2-migration-stack`,
`GUIDE-machine-pairing-f11`, `GUIDE-os-console-getting-started`) are GUIDEs
destined for `woodfine-fleet-deployment`, outside this repo's and this
session's write access — refined in place in drafts-outbound and routed to
Command Session via mailbox for customer/ commit.

---

### 2026-07-01 — Named-company benchmarking removed from public wiki content: COMPLETE

`Closed: 2026-07-01.`

**Scope:** Operator flagged that TOPIC/GUIDE content should not name specific real companies (Goldman Sachs, Bloomberg, etc.) as writing-quality benchmarks, and that the style-guide articles in particular shouldn't be on the public wiki. Full audit + fix this session:

- **Consolidated + relocated:** 16 `reference/style-guide-*.md` articles (32 files w/ `.es.md`) — previously rendered live (`bcsc_class: public-disclosure-safe`, `status: active`) despite being contributor/editorial-process documentation, not reader content — merged into `.internal/style-guide.md` + `.internal/style-guide.es.md`. `.internal/` is a new, permanent, non-wiki-category directory: `app-mediakit-knowledge`'s content loader already skips dotted directories, so nothing here is rendered, with no engine change required. See `naming-convention.md` §13 Decision #9 and `repo-layout.md` for the ratified convention.
- **Genericized in place** (stayed public, removed only the named-company benchmark phrasing): `reference/editorial-language-registers.md`+`.es.md`, `reference/_index.md`+`.es.md`, `reference/editorial-philosophy.md`+`.es.md`, `applications/app-mediakit-knowledge.md`, `architecture/language-protocol-substrate.md`+`.es.md`, `governance/anti-homogenization-discipline.md`, `systems/console-os.md`+`.es.md`, plus `media-knowledge-corporate/about.md`+`.es.md` in the corporate wiki.
- **Left unchanged** (factual integration references, not tone benchmarks): `leapfrog-2030-architecture.md`, `service-wallet-settlement.md` (Stripe Connect as an actual payment rail).
- **Backlinks fixed** so no public page links to the now-unpublished `.internal/` slugs: `index.md`, `substrate/language-protocol-substrate.md`+`.es.md`, `services/template-ledger.md`, `reference/glossary-documentation.md`+`.es.md`, `reference/editorial-philosophy.md`+`.es.md`, `reference/editorial-language-registers.md`+`.es.md`, `reference/_index.md`+`.es.md`.
- **New enforcement:** `.agent/scripts/editorial-lint.py` + `.agent/editorial-qa/banned-vocabulary.txt` + new `.agent/editorial-qa/banned-company-names.txt` created in this archive (were referenced by other archives' copies but did not exist here — see NEXT.md). Added a WARN-level (not ERROR — see file header for rationale) named-company check to the linter, scoped to a curated list that deliberately excludes real integration/standards partners (Stripe, Cloudflare, RIBA) to avoid false-positiving on legitimate factual references. Verified against `media-knowledge-projects` and `media-knowledge-corporate`: the linter correctly flagged (WARN) 3 files with Morgan Stanley/Bank of America/JPMorgan mentions, all of which on inspection are legitimate factual references (market research citations, real historical employers in city economic profiles) — no changes needed there, confirming the WARN-not-ERROR design choice.

**Verification:** `grep -rliE "goldman sachs|bloomberg|stripe|cloudflare|riba|financial times|the economist"` across all three wikis (excluding `.internal/` and `.agent/`) returns only the two intentionally-left Stripe Connect references and two CLAUDE.md files (not wiki-rendered).

### 2026-05-26 — Guide section taxonomy + Operational Guide Catalog: COMPLETE

`Closed: 2026-05-26.` Commit `0ecaaf4` (Jennifer Woodfine).

**Scope:** Added `section:` frontmatter field to all 81 guides in woodfine-fleet-deployment (commit `142bcd2`, Peter Woodfine) and created bilingual Operational Guide Catalog TOPIC in this repo.

**Changes in media-knowledge-documentation:**
- `reference/guide-catalog.md` + `reference/guide-catalog.es.md` — new bilingual article; 10 H2 sections grouping all 81 operational guides by purpose (Provisioning & Deployment, BIM & Property, GIS & Geospatial, Personnel & Identity, Network & Infrastructure, Console & Operations, Content & Media, Source Control, AI & Intelligence, Workspace & Development).
- Published at `/reference/guide-catalog`.

**In woodfine-fleet-deployment (separate commit 142bcd2):**
- 81 guides across 20 deployment folders each received `section: <key>` immediately after `type: guide` in YAML frontmatter.
- Verification clean: `grep -rL "^section:" --include="guide-*.md"` → 0 files; no invalid section values.
- woodfine-fleet-deployment has no staging mirrors; awaits Command Session Stage 6 push to woodfine canonical.

**Pushed:** media-knowledge-documentation jwoodfine staging mirror confirmed (`0ecaaf4`).

---

### 2026-05-25 — Institution quality pass + drafts-outbound routing: COMPLETE

`Closed: 2026-05-25.` Commit `61ed7fe` (Jennifer Woodfine).

**Scope:** Full quality pass across all four wiki repos + floating TOPIC/GUIDE routing from cluster drafts-outbound queues. 338 published articles elevated to banker/asset-manager POV standard.

**Changes in media-knowledge-documentation:**
- 97 articles modified (governance vocabulary removed, ledes rewritten, register corrected)
- 32 new articles from drafts-outbound (6 pairs in architecture, 3 pairs in applications, 3 pairs in design-system, 1 pair in infrastructure, 1 pair in services, 3 pairs in systems)
- LICENSE + CODE_OF_CONDUCT.md trailing newline corrected per verify-repo-compliance.sh
- factory-release-engineering/mapping/repo-license-map.yaml updated to add media-knowledge-* entries (canonical push cc9ad42)

**Other repos (separate commits):**
- media-knowledge-projects: 30 modified + 16 new (commit f110d62, Peter Woodfine)
- media-knowledge-corporate: 28 modified including critical fix — CC-BY-ND footer was `by/4.0` in all 28 articles; corrected to `by-nd/4.0` (commit d5bcc7f, Jennifer Woodfine)
- woodfine-fleet-deployment: 73 guides modified + 7 new guides (commit 319497d, Peter Woodfine)

**Pushed:** jwoodfine staging mirrors confirmed. pwoodfine staging mirror has pre-existing SSH key auth issue (noted in cleanup-log 2026-05-23 rename entry). woodfine-fleet-deployment has no staging mirrors; awaits Command Session Stage 6.

**Open items surfaced (not actioned this session):**
- DUPLICATE_CANDIDATES: `three-layer-architecture` + `3-layer-stack`; `sovereign-telemetry` + `telemetry-architecture`; `location-intelligence-platform` + `location-intelligence-ux`
- STUBS still pending expansion: `architecture/3d-asset-tokens`, `architecture/identity-ledger-schema-design` (also has "sustrato" in EN body — editorial defect), `substrate/nightly-datagraph-rebuild`
- `identity-ledger-schema-design.md`: Spanish word "sustrato" appears in EN body — editorial defect to fix next pass

### 2026-05-23 — Repo rename: `content-wiki-documentation` → `media-knowledge-documentation`

GitHub canonical and staging mirror URLs updated to `media-knowledge-documentation`. CLAUDE.md, AGENT.md, and repo-layout.md updated. Local directory name (`content-wiki-documentation/`) and `PROJECT-CLONES.md` registry entry pending Command Session rename (`mv`).

Staging mirror GitHub accounts (`jwoodfine/`, `pwoodfine/`) not yet renamed — local `origin-staging-*` remotes currently pointing to old names as a stopgap. Operator must rename staging mirrors, then Command Session updates `.git/config` staging remote URLs.

---

### 2026-05-23 — `archive/` empty directory at repo root

`Closed: 2026-05-24.` Directory was already absent from the filesystem when checked — not tracked by git, not present on disk. No `rmdir` needed. Entry closed.

---

### 2026-05-19 — foundry-services-slice-model slug contains governance vocabulary — logged, no action

`Closed: 2026-05-19.` Slug `foundry-services-slice-model` was published with "foundry" (workspace-internal governance vocabulary) in the slug. Per naming-convention.md §5 slug immortality rule, the slug cannot be changed after publish. Title fixed to sentence case this session (was title case). No further action — slug drift is a known accepted artefact; if the article is ever significantly restructured, add `aliases:` for the current slug and publish a new slug without the vocabulary leak.

---

### 2026-05-09 — Body-level Doctrine/Convention vocabulary scrub — COMPLETE

`Closed: 2026-05-16.` Phase 2 sub-phases 2g + 2j completed this scrub in full.
Sub-phase 2g verified that 4 remaining "Convention" uses in the corpus are legitimate
English and not governance vocabulary. Sub-phase 2j ran a final grep across all
non-architecture categories and returned zero hits. Phase 2 §9.4 verification:
Foundry/Doctrine CLEAN. No further action required.

Original entry retained below for reference.

---

Per operator constraint (workspace v0.1.x; saved as feedback memory
`feedback_no_doctrine_convention_in_public.md`): "Doctrine" and
"Convention" are workspace-internal governance vocabulary and must
not appear in public-facing wiki content. A Goldman Sachs banker
reading the public wiki should encounter the underlying idea in
institutional prose, not internal naming for the governance machinery.

**Scope of leak** (audit performed 2026-05-09 during the home-page
muscle-memory work):

| Wiki | Files mentioning "Doctrine" | Files mentioning "Convention" |
|---|---|---|
| corporate | 0 | 0 |
| projects | 0 | 0 |
| **documentation** | **72** | **49** |

Documentation wiki carries the entire load. With overlap between the
two terms, the unique-file count is approximately 120.

**Title-level scrub completed this session** (3 files, 6 with EN+ES
pairs):
- `governance/sovereign-airlock-doctrine.md` + `.es.md` — title now
  "The Sovereign Airlock" / "La Exclusa Soberana"
- `reference/bim-aec-muscle-memory.md` + `.es.md` — title now
  "AEC Muscle Memory and Interface Patterns" / "Memoria Muscular AEC
  y Patrones de Interfaz"
- `architecture/foundry-doctrine-architecture.md` + `.es.md` — title
  now "Foundry — Architectural Overview" / "Foundry — Visión
  Arquitectónica"

Slugs retained unchanged per content-contract.md §3 immortality rule;
URLs unaffected.

**Body-level scrub deferred — phased approach** (this entry surfaces
the work; execution is multi-session):

1. **First sweep — Featured rotation pool (12 banker-relevant articles).**
   Scrub Doctrine/Convention from the 12 articles that will rotate
   through the home-page Featured Article slot
   (compounding-substrate, doorman-protocol, disclosure-substrate,
   economic-model, leapfrog-2030-architecture, sovereign-ai-commons,
   customer-hostability, three-ring-architecture, llm-substrate-decision,
   worm-ledger-design, knowledge-commons, substrate-native-compatibility).
   Highest editorial value; narrow scope; one session.

2. **Second sweep — substrate/ + architecture/ categories.** Where
   the body text leaks workspace governance vocabulary, replace
   "Doctrine claim #N — X" with "X" + wikilink to the underlying
   TOPIC; replace "per Convention X" with the rule expressed in
   prose. ~50 files; multi-session.

3. **Third sweep — remaining categories.** services/, systems/,
   patterns/, reference/, governance/, infrastructure/, design-system/,
   applications/. Remaining ~60 files.

**Per-file editorial discipline:**
- Some matches are legitimate references to outside concepts (e.g.,
  general English "doctrine" or "convention" usage). Per-file judgment
  required; not a mechanical find-replace.
- Where the term is being defined within the article (e.g., a TOPIC
  about Foundry's governance machinery), retain with plain-language
  translation immediately preceding — same discipline as
  vocabulary-retirement list per Editorial Reference Plan.
- Bilingual ES pairs follow the EN scrub in lockstep.

**Triggered by:** workspace constraint surfaced 2026-05-09 during
Plan #7 (Wikipedia Main Page institutional adaptation). Slot designs
this session removed all Doctrine/Convention vocabulary; this entry
extends that discipline to the article corpus.

---

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

- **2026-07-01/03 — Slug collision `language-protocol-substrate` (architecture/ vs substrate/): RESOLVED.** Editorial call (Phase C re-categorization judgment call, [[project-editorial-category-redesign-phase-c]]): read both articles in full. `substrate/language-protocol-substrate.md` is the platform editorial-infrastructure article (service-disclosure crate, four adapter families, 18 genre templates, BCSC-cited, `quality: complete`) — confirmed as the intended target of **every one of the ~35 corpus-wide `[[language-protocol-substrate]]` wikilinks** (adapter composition, proofreader pipeline, decode-time constraints, etc. — all cite substrate/'s content). `architecture/language-protocol-substrate.md` is a genuinely different article about Foundry's own internal editorial-draft classification/routing mechanism (`.agent/drafts-outbound/`, operator verdicts, archive-to-gateway routing) with **zero wikilinks citing it under this slug**. Resolution: `substrate/` keeps the slug unchanged (no aliases or link-fixes needed — already correct). `architecture/` renamed (EN+ES) to `editorial-draft-routing-protocol`, a slug describing its actual subject; `redirects.yaml` entry added for the URL move. Flagged for a later session: the renamed article's body leans on Foundry-internal vocabulary (`.agent/`, "operator", "archive session") that may warrant the same editorial stripping already applied to other architectural TOPICs (see `feedback-architectural-topic-editorial-stripping` memory) — not actioned here, out of scope for a categorization pass.
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
