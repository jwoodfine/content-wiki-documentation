# Category-fit design sweep — 2026-08-03

Re-derivation of a lost-transcript audit (two independent agents, "Fable" and "Opus",
checked every article's actual subject matter against its current category's charter
in `categories.yaml`, cross-checked against all other categories; outputs never saved).
This file is the durable record that pass should have produced. Written per this
session's own standing discipline of not losing audit work to a lost transcript.

Scope: `media-knowledge-documentation` only. Cross-wiki GUIDE placement
(`media-knowledge-projects`/`media-knowledge-corporate`) is explicitly out of scope
and was not touched.

---

## 1. Hard rule check — GUIDE-shaped content confined to `how-to/`

The task's named marker strings (`content_type: guide`, `type: guide`,
`language_protocol: PROSE-GUIDE`) do not literally appear anywhere in this wiki. This
wiki's actual GUIDE marker is `content_type: how-to` / `type: how-to` (56 files use
it; `language_protocol: PROSE-TOPIC`/`TOPIC` is used for ordinary TOPICs, and 2 files
use `language_protocol: GUIDE-OPERATIONS`).

**Verified: 100% of `content_type: how-to` / `type: how-to` files already live in
`how-to/`.** Zero violations of the hard rule found, using the wiki's real marker
values in place of the task's literal (non-matching) strings. No action needed.

## 2. The four numbered hypotheses

### 2.1 — Leaked internal draft-pipeline frontmatter fields (app-orchestration-command-*)

**Verified TRUE, and undercounted.** The task said "two files... likely
`app-orchestration-command-branch-model.md` and one other." Found:

- `systems/app-orchestration-command-branch-model.md` + `.es.md`
- `systems/app-orchestration-command-publication-flow.md` + `.es.md`
- **A third file with the identical leak, not named in the hypothesis:**
  `systems/scaling-coordinated-development-totebox-archives.md` + `.es.md` — directly
  related content (cross-linked from both articles above's "Related Topics"), from the
  same Session 111 / `command-10x-dev-environment` draft batch.

All 6 files carried the same leaked fields: `route: project-editorial`,
`target_wiki: documentation.pointsav.com`, `session: Session 111 (Command@claude-code)`,
`created: 2026-06-20`, and a `research_trail:` block (`source_briefs`, `cross_checks`,
`forbidden_terms_cleared`) — none of which are part of the published-article schema in
`content-contract.md` §4; all are `foundry-draft-v1`-style pipeline fields that never
should have survived into a published, `status: active` wiki article.

**Fixed:** stripped `route`, `target_wiki`, `session`, `created`, `research_trail` from
all 6 files. Left every other frontmatter field and all body content untouched.
`last_edited` bumped to 2026-08-03 on the two files that lacked it (the
`scaling-coordinated-development-*` pair already had a `last_edited` field, left
unbumped — only the leaked fields were touched there since the category didn't change).

### 2.2 — `app-orchestration-command-branch-model` / `-publication-flow`: systems/ → applications/?

**Verified TRUE.** Both are `app-*` prefixed per the Nomenclature Matrix.
`naming-convention.md` §5 and §13 (Decision #11's rebalancing, and the 2026-07-30
`os-privategit-workbench` precedent) establish `os-*` → `systems/`, `app-*` →
`applications/` as the corpus-wide convention. Confirmed empirically: every other
`app-*`-slugged article in the corpus (`app-orchestration-gis`, `app-mediakit-knowledge`,
`app-mediakit-marketing`, `app-console-{email,input,keys,slm}`,
`app-privategit-workbench`) already lives in `applications/`. `app-orchestration-gis` —
same `app-orchestration-*` family — is the closest sibling precedent.

Content also supports the move: both articles describe `app-orchestration-command` as a
real, running coordinator service (a "CommandCentre" HTTP server per the articles' own
2026-08-02 correction notes, verified against canonical `origin/main`) — matching
`applications/`'s charter ("applications people actually use... from public knowledge
sites to internal consoles") rather than `systems/`'s charter ("the operating systems
PointSav ships").

**Fixed:** `git mv` both EN+ES pairs to `applications/`; `category:` updated in all 4
files. Neither article was referenced in any `_index.md` MOC before the move (verified
by grep), so no MOC edit was needed on the `systems/` side. `applications/_index.md`'s
curated MOC was **not** updated to add entries for these two articles — deferred, not
forgotten; see §4 below.

### 2.3 — `systems/totebox-archive.md` → infrastructure/?

**Verified TRUE**, on balance, after weighing both directions explicitly:

*For staying in `systems/`:* the article carries a "Relationship to the OS family"
section cross-referencing `os-totebox`/`os-console`/`os-orchestration`/
`os-infrastructure`, and draws the plurality of its 68 inbound wikilinks from `systems/`
itself (28 of 68, across 7 categories total) — the same shape of argument that kept
`system-substrate-doctrine.md` and `disclosure-substrate.md` in place in the two
already-resolved disputes.

*For moving to `infrastructure/`:* by volume, the article is overwhelmingly about
deployment/storage mechanics — disk-image/VM packaging, the WORM flat-file storage
model, the Diode+PSP access model, the MBA keypair, cluster naming — matching
`infrastructure/`'s charter almost exactly ("Where the platform physically runs:
customer hardware, deployment, storage..."). Critically, **the systems-composition role
this article's "OS family" section partially performs is already fully owned by
`systems/os-family-overview.md`** (title: "OS family — eight operating systems, one
substrate" — the article the `systems/_index.md` MOC itself names as "the entry point
for readers new to the family"), and the OS itself (distinct from the archive/VM
concept) already has its own dedicated `systems/` article, `totebox-os.md`
(`aliases: [os-totebox]`). `totebox-archive.md` isn't needed to carry the
family-composition weight in `systems/` — it can be the infrastructure-side deployment
article and still be reached from `systems/` via wikilink cross-reference (which,
being slug-based, works identically regardless of which category directory the file
lives in).

**Fixed:** `git mv` both EN+ES to `infrastructure/`; `category:` updated in both.
Removed the `systems/_index.md`/`.es.md` MOC bullet; added a new MOC bullet to
`infrastructure/_index.md`/`.es.md` under "Storage substrate" (the section already
covering WORM ledger/storage articles — a good content fit).

**Secondary finding, not actioned:** while reading `totebox-archive.md` against
`totebox-os.md` for this decision, found real content overlap between the two (both
describe the WORM/flat-file storage discipline) — not confirmed as a duplicate requiring
merge (this wasn't one of the four named hypotheses and wasn't investigated to that
depth), but flagged here for a future merge-candidate pass to check explicitly.

### 2.4 — Merge candidates

**`infrastructure/os-orchestration-stateless-hub.md` vs `systems/os-orchestration.md` —
verified NOT a simple duplicate. Not merged.** Both describe `os-orchestration`, and
there is real topical overlap (statelessness, commercial tiering, aggregation), but the
two articles diverge substantively:

- `systems/os-orchestration.md` is a product-overview article: licence-model table
  (AGPL/FSL/Proprietary), the aggregation mechanics (3-step protocol walkthrough), a
  "commercial features" table (Aggregation/Multi-tenancy/Complex viewports), Diode
  discipline, and buyer-facing "when to deploy" guidance.
- `infrastructure/os-orchestration-stateless-hub.md` is a deep-dive on one specific
  architectural property: a Protection-Domain federation model (per-archive
  "capability-broker PD") not mentioned at all in the systems/ article; a **different**
  commercial framing (a Rings/Tier-A/Tier-B/marketplace model, rather than the
  licence-table model the systems/ article uses for the same product); and a "Yo-Yo GPU
  Broker" section (`app-orchestration-slm`) absent from the systems/ article entirely.

This is the same shape as the already-resolved `mediakit-os.md` vs `os-mediakit.md`
case in `cleanup-log.md` (2026-07-30): two articles about the same subject with
materially different, partially contradictory framings (here: two different commercial
models for the same product), where the correct resolution was flagging the conflict,
not merging or deleting either side. **Not merged. Flagged, not resolved** — the
Rings-model-vs-licence-table commercial-framing contradiction needs a dedicated pass;
recorded here rather than silently left implicit. No file changes made to either
article.

**`reference/quick-start.md` vs `reference/getting-started.md` — verified GENUINE
duplicate-purpose pair. Merged.** Both are `quality: stub` articles in `reference/`
serving the identical function (first-session/onboarding orientation for a new
engineer or evaluator), both link to the same three targets (`guide-catalog`,
`ppn-small-business-compute`, `machine-based-auth`), and **neither was referenced from
any curated MOC anywhere in the corpus** (`reference/_index.md` lists neither; the only
inbound wikilink to either was each file's own `.es.md` sibling pointing back to its EN
pair) — both were fully orphaned duplicate stubs.

**Fixed:** kept `getting-started` as canonical (broader "Where to start" scope,
including GIS/data, which `quick-start` lacked). Merged `quick-start`'s "Prerequisites"
and "First steps" sections into `getting-started.md` (EN) and translated the same into
`getting-started.es.md` (ES) — quick-start's ES pair was itself only a stub-of-a-stub
(no unique untranslated content to lose). Added `aliases: [quick-start]` to both
`getting-started` files. `git rm` on `reference/quick-start.md` + `.es.md`. Added a
`redirects.yaml` entry (`/reference/quick-start` → `/reference/getting-started`).

**Incidental fix made while merging (not one of the four hypotheses, but touching the
exact lines being rewritten):** `getting-started.es.md` still had the unfixed Spanish
equivalent of a Do-Not-Use violation ("una pila de software soberana") that the EN
sibling had already corrected in a 2026-08-02 pass (to "an independently verifiable,
operator-controlled software stack"). Applied the same correction in Spanish
("verificable de forma independiente y controlada por el operador") with a matching
correction-note parenthetical, for EN/ES parity. Also resolved, rather than re-flagged,
`quick-start`'s already-known "host agent" vs. "per-node agent" naming-drift note (used
the correct term, "per-node agent," directly in the merged text instead of carrying the
flagged inconsistency forward).

## 3. Step-4 spot-check re-scan

Rather than picking 2-3 categories arbitrarily, ran a corpus-wide grep for the same
prefix-vs-category mismatch pattern that produced the two confirmed hypotheses above
(`app-*` outside `applications/`, `service-*` outside `services/`, `os-*` outside
`systems/`) — cheaper and more systematic than a manual per-category skim, and directly
informed by what 2.2/2.3 found.

Three more candidates surfaced beyond the two already-confirmed violations:

- **`architecture/app-orchestration-graph-federation.md`** — checked and **confirmed
  correctly placed**. Content is about the architectural design-decision question of
  when a federation feature graduates from `app-orchestration-slm` into a dedicated
  service (`app-orchestration-graph`) — the latter doesn't exist as a shipped product
  yet (per project-registry, `app-orchestration-graph` is `Reserved-folder` state).
  This is design/decision content matching `architecture/`'s charter ("the business and
  publication model built on that shape"), not a per-application description. Left in
  place.
- **`architecture/os-products-distribution-model.md`** — checked and **confirmed
  correctly placed**. Content is a pricing/licensing/distribution-channel article
  (`software.pointsav.com` product listing, USDC pricing) — squarely matches
  `architecture/`'s "business and publication model" charter clause, not a per-OS
  systems description. Left in place.
- **`reference/service-slm-operationalization-plan.md`** — checked; **not confidently
  a violation, not moved.** Its subject (a multi-year rollout/evaluation-criteria plan
  for `service-slm`) doesn't fit `reference/`'s literal charter ("every term defined in
  plain words... catalogues and standard definitions") especially well, and could
  arguably suit `architecture/` or `services/` better. However, `reference/_index.md`
  deliberately created an "Operational reference" section that names this exact
  article by curatorial choice — it is not simply mis-filed, it was placed there on
  purpose by an earlier session. Left in place; noted here as a genuine judgment call
  that a future session or the operator may want to revisit, not something this pass
  is confident enough to move unilaterally.

Also spot-checked `reference/` for other stub-pairs with the same shape as
quick-start/getting-started (same `quality: stub` scan across the whole directory):
**no other candidate pair found** — `quick-start`/`getting-started` were the only two
stub articles in the category.

Also spot-checked `systems/` for other near-duplicate title patterns around
"totebox"/"orchestration" (`totebox-orchestration.md`, `os-totebox-service-pd-model.md`,
`os-totebox-sovereign-archive.md`, `vm-architecture.md`, `input-machine.md`): all read
as genuinely distinct subjects, already cross-referenced as complementary within the
corpus itself (e.g. `os-orchestration.md`'s own "See also" explicitly distinguishes
itself from `totebox-orchestration.md`'s scope). No action taken.
`os-totebox-sovereign-archive.md` is a known, separately-tracked naming/Do-Not-Use
defect per `cleanup-log.md` — out of this pass's scope, not touched.

## 4. Explicitly deferred — needs operator/Command sign-off or a dedicated pass

1. **`infrastructure/os-orchestration-stateless-hub.md` vs `systems/os-orchestration.md`
   commercial-model contradiction** (§2.4) — Rings/Tier model vs. licence-table model
   for the same product's commercial structure. Flagged, not resolved.
2. **Possible `totebox-archive.md` / `totebox-os.md` content overlap** (§2.3 secondary
   finding) — surfaced incidentally, not investigated to merge-candidate depth. Needs a
   dedicated read-both-in-full pass.
3. **`reference/service-slm-operationalization-plan.md` category fit** (§3) — a genuine
   but not confidently-actionable judgment call between `reference/` (current, and
   deliberately curated there), `architecture/`, and `services/`.
4. **`applications/_index.md` MOC not updated** to add curated entries for the two
   newly-moved `app-orchestration-command-*` articles (§2.2). They will still appear via
   the engine's auto-generated per-category article list (per `content-contract.md`
   §"category landings" — MOC prose and the auto-list are both shown), so this is a
   cosmetic/curatorial gap, not a functional one.

## 5. Files changed this pass

- `applications/app-orchestration-command-branch-model.md` + `.es.md` (moved from
  `systems/`; frontmatter leak stripped; category fixed)
- `applications/app-orchestration-command-publication-flow.md` + `.es.md` (same)
- `infrastructure/totebox-archive.md` + `.es.md` (moved from `systems/`; category fixed)
- `systems/scaling-coordinated-development-totebox-archives.md` + `.es.md` (frontmatter
  leak stripped only; stays in `systems/`)
- `systems/_index.md` + `.es.md` (removed `totebox-archive` MOC bullet)
- `infrastructure/_index.md` + `.es.md` (added `totebox-archive` MOC bullet)
- `reference/getting-started.md` + `.es.md` (merged in `quick-start` content; added
  `aliases: [quick-start]`; incidental Do-Not-Use ES-parity fix)
- `reference/quick-start.md` + `.es.md` (removed — `git rm`)
- `redirects.yaml` (4 new entries)
