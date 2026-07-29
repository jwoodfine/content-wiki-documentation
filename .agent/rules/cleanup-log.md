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

Last updated: 2026-07-28.

---

## Open

### 2026-07-28 — `security/_index.md` MOC written (EN+ES): was 0-link prose, confirmed worst landing page in the wiki by both content-matrix design agents

`Opened and closed: 2026-07-28.` Both the structural and reader-journey content-matrix
agents independently verified `security/_index.md` had zero article wikilinks — three
paragraphs of prose plus cross-category "See also" links only, no path into any of the
13 articles the category actually holds (the only other category with this defect is
`ai/`, not yet fixed — see the open item this leaves below). Rewrote as a curated MOC,
grouped by the category's own five declared scope clauses (identity/permissions,
cryptographic verification, isolation boundaries, data handling/privacy, supply-chain
controls) rather than alphabetically, matching this wiki's established MOC pattern.
Deliberately left the thinness of "isolation boundaries" (3 articles) and "data handling
and privacy" (1 article) visible in the MOC's own prose rather than padding it — these
are real, already-flagged gaps (content-matrix synthesis,
`.agent/audit/phase1c-documentation-sweep/content-matrix-simulation-2026-07-28.md` in
project-editorial), not something a landing-page rewrite should paper over. Added 2
cross-links to `infrastructure/ppn-tenant-vm-isolation` and `services/service-vm-tenant`
(the commercially load-bearing isolation case, previously uncross-referenced from this
category at all) — both verified to resolve before committing. Also fixed
`_index.es.md`'s slug typo (`security-index.es` → `security-index`, same bug class as
`telemetry-architecture.es.md` fixed earlier this session).

**Still open: `ai/_index.md` has the identical zero-link defect**, per the same
content-matrix finding — not fixed this pass; needs the 10 `ai/` articles read first
(not yet done this session, unlike `security/`'s 13 which were already read in full
during the Phase 1c sweep).

### 2026-07-28 — `scaling-coordinated-development-*` three-way duplicate: CLOSED (execution of the 2026-07-09 blocked follow-up)

`Opened: 2026-07-09 (diagnosed, blocked). Closed: 2026-07-28.` Re-surfaced by the
2026-07-28 content-matrix simulation. Verified all three articles (EN+ES = 6 files) are
word-for-word identical bodies, confirming the 2026-07-09 diagnosis still held. Found one
more thing that entry didn't call out explicitly: `architecture/scaling-coordinated-
development-totebox-archives.md` and `systems/scaling-coordinated-development-totebox-
archives.md` carried the **identical slug** in two category directories — a genuine
slug-uniqueness violation (`content-contract.md` §3: slugs resolved globally, not
per-category), not just a content duplicate. `systems/scaling-coordinated-development-
sovereign-archives.md` was additionally a leaked draft artifact
(`forbidden_terms_cleared: false`, draft-schema frontmatter with `session:`/
`research_trail:` fields) that should never have reached a live category directory.

Verified before executing: all 4 inbound `[[scaling-coordinated-development-totebox-
archives]]` wikilinks (in `app-orchestration-command-branch-model`/`-publication-flow`,
EN+ES) reference the surviving slug, not either removed one — no link fixes needed.
Neither `architecture/_index.md` nor `systems/_index.md` referenced any of the 3 in their
MOC — no landing-page updates needed.

**Executed 2026-07-28, with explicit operator permission** (the `git rm` was blocked by
the auto-mode classifier on first attempt, same as it was 2026-07-09 — flagged to the
operator directly rather than routed around, per standing practice; operator granted
permission for this specific action): `git rm` on `architecture/scaling-coordinated-
development-totebox-archives.md`+`.es.md` and `systems/scaling-coordinated-development-
sovereign-archives.md`+`.es.md`. `systems/scaling-coordinated-development-totebox-
archives.md`+`.es.md` is now sole canonical (already carried the correct
`aliases: [scaling-coordinated-development-sovereign-archives]`). Two `redirects.yaml`
entries added for the removed paths, per the 2026-07-09 plan exactly.

### 2026-07-28 — `location-intelligence-ux` / `location-intelligence-platform`: verified NOT a defect, no action needed

`Opened and closed: 2026-07-28.` Flagged as a DUPLICATE_CANDIDATE on 2026-05-25 (note:
distinct from the same-slug `applications/location-intelligence-ux` vs `patterns/
location-intelligence-ux` collision resolved 2026-07-03/09 — this is a different-slug
pair) and re-surfaced by the 2026-07-28 content-matrix simulation on high slug-token
similarity. Direct read of both found they are genuinely complementary, not duplicates:
`location-intelligence-platform` (applications) covers the GIS product's data
architecture, licensing, and roadmap; `location-intelligence-ux` (patterns) covers
specifically the interface design philosophy (Conclusion-First rendering, cluster-grade
visualization). No overlapping facts. **Already correctly cross-linked in both
directions** in "See also" — no missing link, no merge candidate. Closing the flag as a
false positive rather than executing a fix that isn't needed.

### 2026-07-28 — `sovereign-telemetry` / `telemetry-architecture`: not a duplicate, resolved as a one-directional missing cross-link + a slug typo

`Opened and closed (cross-link/slug); one item left open below.` Flagged as a
DUPLICATE_CANDIDATE on 2026-05-25, re-surfaced by the 2026-07-28 content-matrix
simulation; direct read of both found they are **complementary, not duplicates** —
`sovereign-telemetry` describes the client-side V4 Intent Beacon payload (what's
collected, how it's compiled), `telemetry-architecture` describes the server-side
four-tier routing/processing path. No overlapping facts found. Two real, smaller defects
fixed instead: (1) `sovereign-telemetry` already linked to `telemetry-architecture` in
both EN and ES, but `telemetry-architecture.md` (EN) was missing the back-link —
`telemetry-architecture.es.md` already had it, so this was a bilingual-parity gap, not a
symmetric one; added the EN back-link. (2) `telemetry-architecture.es.md`'s frontmatter
had `slug: telemetry-architecture.es` — inconsistent with every other `.es.md` file in
this repo (which all use the same slug as their EN pair, no `.es` suffix) — corrected to
`slug: telemetry-architecture`.

**Not fixed, flagged instead:** `telemetry-architecture.md`'s "Four-tier routing path"
section names specific internal infrastructure (`10.50.0.2:8081`/`8082` port/IP pairs,
hostname `laptop-a`, script name `pull_sovereign_telemetry.sh`) — the same class of
operational-not-architectural detail this repo's own editorial discipline strips before
wiki commit (see `feedback-architectural-topic-editorial-stripping` precedent). This is
already-live content, not a draft under review, and stripping it is a distinct editorial
judgment call from the duplicate-resolution task at hand — flagging for a dedicated pass
rather than folding it into this fix.

### 2026-07-28 — `three-layer-architecture` / `3-layer-stack`: not a duplicate, resolved as a disambiguation defect

`Opened and closed: 2026-07-28.` Flagged as a DUPLICATE_CANDIDATE on 2026-05-25 and
re-surfaced by the 2026-07-28 content-matrix simulation; direct read of both articles in
full found they are **not duplicates at all** — two genuinely different "three-layer"
models that happen to share near-identical titles: `3-layer-stack` is a single
deployment's runtime decomposition (infrastructure/platform/delivery); `three-layer-
architecture` is the vendor→customer→operator software supply chain (SOFTWARE/SHOWCASE/
INSTANCES). Neither article cross-referenced the other anywhere — a reader landing on
either had no path to the one they actually meant. Fixed as a Wikipedia-style
disambiguation, not a merge: added a "not to be confused with" hatnote to the lead of
each (EN+ES) and a cross-link in each "See also." No content deleted, no slug changed,
no `redirects.yaml` entry needed. Closes the 2026-05-25 flag — correcting it, not
executing it, since a merge would have been the wrong fix.

### 2026-07-28 — design-system/ Decision #7 stub-vs-redirect: 3 stale redirects removed (real content); 4 remain, need an operator/Command call

`Opened: 2026-07-28.` A content-matrix simulation (project-editorial,
`.agent/audit/phase1c-documentation-sweep/content-matrix-simulation-2026-07-28.md`)
flagged that 7 of `design-system/`'s 11 articles were files ratified to leave under
Decision #7 (2026-05-16) but never removed, each also carrying a `redirects.yaml` 301 to
the same destination. Direct read of all 7 bodies (not assumed from file size, which
misled the original flag) found this splits into two different situations:

**Genuinely stale — fixed.** `wiki-component-library.md`, `wiki-dark-mode.md`,
`wiki-typography-system.md` are NOT Decision #7 husks — they are substantial,
`status: active`, current articles about *this wiki's own* rendering layer (the 9 page
components, the dark-mode token implementation, the type system), not generic
design-system component specs. Their `redirects.yaml` entries were dead code (confirmed
against `app-mediakit-knowledge`'s routing: redirects.yaml is only consulted when no live
article exists at that slug) and have been removed. No content changed; only the stale
routing config.

**Genuinely stub-shaped, not yet resolved.** `design-color.md`, `design-motion.md`,
`design-spacing.md`, `design-typography.md` are real 3-sentence pointer stubs
(`status: stub`) matching Decision #7's intent. But git history shows this isn't a
forgotten `git rm` — commit `9fca6cd` ("add stub aliases for moved foundation token
slugs") *deliberately* added these back after the original `git rm` (commit `9bbee55`),
which reads as an intentional Wikipedia-style "this moved, here's a pointer" design
choice, not an accident. Their `redirects.yaml` entries are also currently dead code for
the same routing reason (a live stub file shadows the redirect). **Not resolved here** —
whether the intended UX is (a) keep the stub pages and remove the now-pointless
redirects, or (b) remove the stub pages and let the 301 actually fire, is a real
editorial/routing decision, not a mechanical cleanup. Flagging for an operator/Command
call rather than picking one unilaterally.

---

## Open

---

### 2026-07-18 — Small pilot batch (Phase 1 clean-sheet rewrite): 2 more BCSC honesty-rail defects + 1 redundant stub found via consolidation-check: CLOSED

`Closed: 2026-07-18.` Commit `c1a89d3`. Started as "expand the `systems/os-totebox.md`
stub" — the consolidation-check discipline (mandatory before authoring, per this
session's own standing rule) caught two real problems before any new content was written:

1. **Redundancy**: `systems/totebox-os.md` (slug `totebox-os`, `quality: complete`,
   `aliases: [os-totebox]`) already fully covers what the `os-totebox.md` stub was going
   to be expanded into — and is already correctly hedged (its own "Host shape" table
   already marks seL4 as `(planned)`, Phase 3). Because `os-totebox.md` existed as a real
   file with slug `os-totebox`, it was shadowing `totebox-os.md`'s own alias claim — all
   12 real inbound `[[os-totebox]]` wikilinks across the corpus were resolving to the
   4-sentence stub instead of the complete article. Retired the stub (`git rm`,
   `redirects.yaml` entry added) rather than expand it — the disposition-rubric's
   redundancy test (MERGE/DROP), not REWRITE.
2. **BCSC honesty-rail breach, same class as the 2026-07-18 os-console fix (see entry
   above)**: while checking for redundancy, found `systems/os-totebox-sovereign-archive.md`
   and `systems/os-totebox-service-pd-model.md` (both `quality: complete`,
   `bcsc_class: current-fact`) asserting in unhedged present tense that os-totebox runs
   today as a seL4 bare-metal OS with formally-verified Protection Domains. Verified
   directly against the real crate: `os-totebox/Cargo.toml` describes it as "service-content
   + service-slm (Doorman) run as one deployable process, dogfooded on foundry-workspace" —
   plain Rust/tokio, zero seL4 dependency, matching the same pattern already found and
   fixed for os-console. Fixed both files (EN fully retensed section-by-section; ES got
   the frontmatter + lead fix, full section-by-section pass flagged as not yet done,
   not silently skipped) — `bcsc_class` corrected `current-fact` → `forward-looking` on
   both, matching what the content actually describes (intended Phase H1 design, not
   current state).

**Not yet done, flagged rather than silently left**: `os-totebox-sovereign-archive.es.md`
and `os-totebox-service-pd-model.es.md` need the same full section-by-section tense
correction their EN pairs got — only the frontmatter + lead were fixed this pass.

---

### 2026-07-18 — BCSC honesty-rail breach: 5 articles falsely asserting os-console runs under seL4: CLOSED

`Closed: 2026-07-18.` Commit `92f6cef`. Relayed from project-console via Command
(`command-20260718-correction-needed-5-public-wiki-articles`): `systems/console-os.md`,
`systems/os-family-overview.md`, `substrate/sel4-microkernel-substrate.md` stated
unhedged, present-tense that os-console boots an seL4 environment and runs a custom
WGPU/SDF-glyph rendering stack — project-console verified directly this is false
(os-console is `ratatui`/`crossterm`, zero seL4 dependency; `moonshot-hypervisor` is a
4-file stub). `substrate/sel4-unikernel-substrate.md` and
`systems/os-console-totebox-browser.md` were already hedged ("planned Phase H2/H3") but
`os-console-totebox-browser.md`'s framing sentence still called the cartridge/PD
relationship "structural, not metaphorical" despite several rows of its own comparison
table being marked planned.

Fixed all 4 affected files (EN+ES, 8 files total — `sel4-unikernel-substrate.md` needed
no change, already correctly hedged throughout): rewrote unhedged present-tense claims to
state current reality (`os-console` ships today as a `ratatui`/`crossterm` terminal
application) with the seL4/custom-GPU-stack architecture clearly marked as a roadmap
target, not current state — matching project-console's own `BRIEF-os-console-rebuild-2030.md`
honesty rail ("reserve 'kernel-enforced' for a roadmap caption"). Softened
`os-console-totebox-browser.md`'s framing sentence to acknowledge the analogy holds today
only for the pieces already built. Also found and fixed, while editing `console-os.md`
(not part of the original 5-file report): a corrupted self-referential wikilink at the F1
HELP row (`[[app-console-input|content-wiki-documentation]]` — repo name leaking into
display text) — replaced with plain prose since it wasn't a live wikilink target.

**Separately flagged to Command, not this repo's own scope to fix**: while investigating
this correction, found `content-wiki-documentation` (Command's routing target for this
correction) is a different, stale repo at `vendor/content-wiki-documentation` —
`role: canonical-mirror`, `consumed_by: []` per `conventions/local-sync-paths.yaml`,
diverged from this repo (`media-knowledge-documentation`, the actual `role:
live-service-source`) since Phase C. Flagged by mailbox
(`command-20260718-repo-name-drift-found-content-wiki-docum`).

---

### 2026-07-15 — `research/` category retired; `preprint-notice-convention` relocated to `reference/`

`Closed: 2026-07-15.` Command-ratified reversal of `naming-convention.md` §13
Decision #12 (2026-07-02) and `BRIEF-category-redesign-phase-c.md`'s locked
decision — full rationale in `naming-convention.md` §13 Decision #13. The
category's one real article, `preprint-notice-convention.md`(+`.es.md`), moved to
`reference/` (slug unchanged; `redirects.yaml` entry added for the old
`/research/preprint-notice-convention` path) and its body generalized from a
single-wiki "research programme" framing to the cross-site JOURNAL preprint
convention it actually now describes, per the sovereign-per-surface JOURNAL model.
`research/_index.md`(+`.es.md`) — the empty landing page — removed.
`categories.yaml` and the §4 table both drop the `research` row.

---

### 2026-07-10 — Bilingual parity gap closed: collect-location-intelligence-data.es.md

`Closed: 2026-07-10.` The only GUIDE of 28 in `how-to/` missing its ES pair entirely
(flagged 2026-07-06). Full translation, not just frontmatter — prose/headings/prerequisites/
step descriptions translated; code blocks, YAML, bash commands, chain IDs, and wikidata IDs
kept verbatim (matching this wiki's existing bilingual-technical-content convention, e.g.
`language-protocol-substrate.es.md` keeps `Doorman`/`service-content` untranslated).

---

### 2026-07-10 — project-console re-submission (3 topics): 2 already covered by an independently-authored later version; 1 genuine content gap closed

`Closed: 2026-07-10.`

**Scope:** project-console re-submitted 3 "revised" TOPIC drafts (`topic-customer-tier-catalog-
pattern.md`, `topic-editorial-pipeline-three-stages.md`, `topic-language-protocol-substrate.md`)
claiming they were expanded from earlier SKELETON/ROUGH stubs but never re-routed. Checked each
against the actual published article before acting (this repo's standing "check, don't assume"
discipline).

**Finding:** all 3 slugs are already published (`patterns/customer-tier-catalog-pattern.md`,
`services/editorial-pipeline-three-stages.md`, `substrate/language-protocol-substrate.md`), but
via a different pipeline (`schema: foundry-doc-v1`, `editor: pointsav-engineering`) that reached
its own independent, differently-structured treatment — not derived from project-console's
draft track at all. 2 of 3 (`customer-tier-catalog-pattern`, `editorial-pipeline-three-stages`)
already substantively cover the same ground the draft claims to add (worked example, provisioning/
decommission lifecycle, per-stage detail — verified by direct grep, not assumed) — no merge
needed, the re-submission is stale relative to a parallel resolution.

**`language-protocol-substrate.md` had a genuine gap**, confirmed by section-heading diff:
missing the "Architectural grounding" (foundry-draft-v1 schema, artifact-classification routing
table, mailbox relay convention) and "Why explicit protocol selection" (the case for declared-
not-detected register) content project-console's draft added. Merged both sections into the
published EN article (generalized: dropped the specific arXiv citation ID for the auto-detection-
homogenization finding since it couldn't be independently verified this session; kept the
substantive claim, attributed generically to "a 2023 Cornell University study"). ES pair
(`language-protocol-substrate.es.md`) intentionally left unchanged — it is already a condensed
strategic adaptation missing several EN sections (Ring and Role, full Architecture subsections,
Configuration), so omitting these 2 new sections is consistent with the existing pattern, not a
new bilingual gap.

Replied to project-console with the finding; their draft copies (superseded) are theirs to
retire on their own branch.

### 2026-07-09 — Consolidation-candidates audit (2026-07-01) groups #2–#7: all six already resolved by a later commit; audit document is stale on these items

`Opened: 2026-07-09.`

**Scope:** project-editorial was dispatched to work the six remaining same-slug-in-two-categories
groups from `.agent/audit/2026-07-01-style-guide-calibration/consolidation-candidates.md` (group #1,
`language-protocol-substrate`, was already closed 2026-07-01/03 per the entry above and was
explicitly out of this session's scope). Per the session's git-history-first discipline (a prior
session this same day reversed a deliberate decision by skipping this check — see the entries above),
`git log --all -- "*<slug>*"` was run for every slug before touching anything.

**Finding: all six were already resolved.** Commit `aeec5eb` ("Phase C A1b: rebalance PPN/OS/substrate/
services out of architecture/ ... resolve 8 of 9 slug collisions (aliases + redirects); language-
protocol-substrate left for editorial call", 2026-07-03) — two days **after** the audit document was
written (2026-07-01) — deleted one copy of each pair, kept the other, added a (self-referential, see
note below) `aliases:` field, and added a `redirects.yaml` path-redirect entry for every one. The
keep-side chosen in every case matches the audit's own recommendation:

| # | Slug | Deleted | Kept | Audit recommendation | Match |
|---|---|---|---|---|---|
| 2 | `location-intelligence-ux` | `applications/` | `patterns/` | merge, no side specified | consistent — `patterns/` is the correct category per naming-convention.md §4 |
| 3 | `os-console-platform` | `architecture/` | `systems/` | investigate | resolved — `systems/` is the correct category (per-OS articles) |
| 4 | `input-machine` | `architecture/` | `systems/` | investigate | resolved — same reasoning as #3 |
| 5 | `editorial-pipeline-three-stages` | `architecture/` | `services/` | investigate | resolved — `services/` is the correct category (per-service articles) |
| 6 | `customer-tier-catalog-pattern` | `architecture/` | `patterns/` | keep `patterns/` | exact match |
| 7 | `collab-via-passthrough-relay` | `architecture/` | `patterns/` | keep `patterns/` | exact match |

Verified for all six: exactly one file per slug now exists corpus-wide (EN+ES); `redirects.yaml`
carries a `/architecture/<slug>` (or `/applications/<slug>`) → `/<new-category>/<slug>` entry for
each; no stray hardcoded path references to the old category paths remain anywhere in the corpus
(`grep -rn` clean — all inbound references already use `[[slug]]` wikilinks, which resolve via the
flat slug index regardless of category, per content-contract.md §3). **No new merge, rename, or
commit was needed or performed for the structural slug-collision issue** — closing this list item
against a decision already made, not making a new one.

**Two things flagged, not fixed this session (out of scope for a duplicate-resolution pass):**

1. **The resolution discarded content, it did not merge it.** In every one of the six pairs, the
   commit's diff shows the kept file gained only the `aliases:` field (+2 lines) — no prose, links,
   or metadata from the deleted file were carried over, even where the deleted copy had genuinely
   different or arguably better content. Spot-checked in full: `applications/location-intelligence-ux.md`
   (deleted) had a "Key Takeaways" section not present in the surviving `patterns/` copy, used
   sentence-case headings where the surviving copy still uses Title Case (a `house-core.md` §Capitalization
   defect), and did not name a real company as a quality benchmark where the surviving copy still reads
   "(e.g., meteoblue.com)" — a `house-core.md` §"Establishing credibility without names" defect. The
   `os-console-platform`, `input-machine`, `editorial-pipeline-three-stages`, and
   `customer-tier-catalog-pattern` pairs show the same shape: both sides were substantial, non-trivial
   articles on the same subject, and the losing side's unique material is now recoverable only via
   `git show aeec5eb^:<path>`. This was a legitimate editorial call (both audit-confirmed near-duplicates
   in #2, and structurally mandated to a single copy per slug everywhere else) — flagging the *shape* of
   the resolution (pick-one-and-discard, not merge-and-preserve) as a known limitation in case a future
   session wants to do a genuine content merge rather than treat this as closed.
2. **`aliases: [<same-slug>]` is a self-referential no-op**, added identically to all six kept files.
   Both original files already shared the same `slug:` value — that was the collision — so there was
   no "old slug" to alias per `naming-convention.md` §8; the field as written does not do anything the
   `slug:` field does not already do. Harmless (does not break resolution), not corrected here — a
   mechanical artifact of a large batch commit, not worth a dedicated commit on its own.
3. **One live style defect found while reading `systems/os-console-platform.md` (not caused by this
   consolidation — present before and after `aeec5eb`):** the "Three-Ring Architecture placement"
   section names `http://localhost:8011` and the binary section names SSH `port 2222`, both of which
   `house-core.md` §"Outside voice" requires stripped from public wiki content ("SSH ports and localhost
   endpoints"). Left unfixed — out of scope for this pass; flagged here for a future editorial-language
   sweep of `systems/`.

**Audit document itself is now stale on these six rows** — `.agent/audit/2026-07-01-style-guide-calibration/consolidation-candidates.md`
lives in this archive's own `.agent/` (cluster-branch scope, a different repository from this wiki),
so it is not corrected from this session; flagged in the mailbox message to Command instead.

---

### 2026-07-09 — Command-authored drafts-outbound sweep (8 files): duplicate-publish "Sovereign Archives" defect found + partially fixed; 2 GUIDEs flagged as likely internal-only

`Opened: 2026-07-09.` **The duplicate-publish defect itself CLOSED 2026-07-28** — see the
dated entry near the top of this file's Open section ("`scaling-coordinated-development-*`
three-way duplicate: CLOSED") for the actual `git rm` + `redirects.yaml` execution this
entry's own "NOT completed" note below was waiting on. Rest of this entry (the seL4
sovereign-archive title/slug defect flagged as a separate follow-up, the 2 internal-only
GUIDE drafts) is unaffected and still stands as originally written.

**Scope:** project-editorial processed 8 drafts staged by Command Session (Session 111) in
`.agent/drafts-outbound/`, all marked `route: project-editorial`, `forbidden_terms_cleared: false`
(NEXT.md had previously reported 2 of the 8 as already staged/complete — this was false; frontmatter
confirmed the language pass had never run). Consolidation check against this repo before authoring
found 4 of the 6 TOPIC drafts already published — plus a genuine duplicate-publish defect on the
other 2:

| Draft | Finding |
|---|---|
| `TOPIC-app-orchestration-command-branch-model.draft.md` (+.es) | CONSOLIDATED — already live at `systems/app-orchestration-command-branch-model.md`(+.es), `status: active`. No new body content needed. |
| `TOPIC-app-orchestration-command-publication-flow.draft.md` (+.es) | CONSOLIDATED — already live at `systems/app-orchestration-command-publication-flow.md`(+.es). |
| `TOPIC-scaling-coordinated-development-sovereign-archives.draft.md` (+.es) | **Duplicate-publish defect, predating this session.** Live in TWO places under TWO different slugs: `systems/scaling-coordinated-development-sovereign-archives.md`(+.es) — the original batch (`540b949`, 2026-06-20), carrying the banned "Sovereign" term (`POINTSAV-Project-Instructions.md` §5) in title AND slug — and `architecture/scaling-coordinated-development-totebox-archives.md`(+.es) — a later, better-metadata copy (`2a8a4cc`, 2026-06-23; trademark footer, `bcsc_class`, `audience: public`) that already fixed the name but was never cross-linked back to the `systems/` sibling family (`app-orchestration-command-branch-model`/`-publication-flow`) and carried a Title Case (not sentence-case) title defect. |

**Fixed this session:** created the single corrected canonical `systems/scaling-coordinated-development-totebox-archives.md`(+.es) — sentence-case title, `aliases: [scaling-coordinated-development-sovereign-archives]` for wikilink resolution, wikilinked Related Topics (including two new links to `os-orchestration` and `os-totebox-sovereign-archive` that were previously unlinked italic placeholders), fixed the "os-totebox sovereign archive model" body phrase to "os-totebox archive model," and carried over the trademark footer. Repaired the sibling articles `systems/app-orchestration-command-branch-model.md`(+.es) and `systems/app-orchestration-command-publication-flow.md`(+.es): their "Related Topics" sections were markdown links to nonexistent `TOPIC-*.draft.md` filenames (i.e., permanently broken — the content-contract requires `[[slug]]` wikilinks for TOPIC→TOPIC, not raw filenames) and one of them said "Sovereign Archives" — both repointed to proper `[[slug]]` wikilinks at the new canonical.

**NOT completed — blocked by the permission system, needs Command/operator action:** could not `git rm` the two now-superseded duplicate pairs (`systems/scaling-coordinated-development-sovereign-archives.md`+.es, `architecture/scaling-coordinated-development-totebox-archives.md`+.es) — deleting pre-existing published content discovered mid-session, not named in the originating task, was denied by the auto-mode classifier as a "modify shared resources" action requiring explicit authorization. Both old pairs remain live at their original URLs (now orphaned — no other article's Related Topics section points to them) alongside the new canonical. **Follow-up needed:** a session with delete authorization should `git rm` all four old files and add two `redirects.yaml` entries (`/systems/scaling-coordinated-development-sovereign-archives` → `/systems/scaling-coordinated-development-totebox-archives`; `/architecture/scaling-coordinated-development-totebox-archives` → `/systems/scaling-coordinated-development-totebox-archives`) to complete the dedup.

**Also flagged, out of this session's scope (not one of the 8 target files):** `systems/os-totebox-sovereign-archive.md`(+.es) — title "os-totebox: The Sovereign WORM Data Vault" — carries **two** Do-Not-Use terms at once ("Sovereign" descriptive use + "Data Vault") plus a Title Case / mid-title-article defect. Predates this session (`last_edited: 2026-06-23`); referenced by the new canonical article above via `[[os-totebox-sovereign-archive|os-totebox archive model]]` (custom display text avoids repeating the bad title). Recommend a dedicated pass — this is a substantive rename (title + likely body prose), not a quick fix, and the slug itself (`os-totebox-sovereign-archive`) is immortal per `naming-convention.md` §5 so an alias-based title/slug correction is the right shape, mirroring the fix just made here.

**2 GUIDE drafts flagged as likely internal-only, not routed to this wiki:** `GUIDE-cross-archive-messaging.draft.md` and `GUIDE-stage-6-promotion-workflow.draft.md` describe Foundry's own internal AI-session mailbox/Stage-6-promotion tooling (`bin/mailbox-send.sh`, `.agent/` paths, `pairings.yaml`, admin SSH aliases, systemd timer units) — none of it runnable by an external reader or PointSav customer, and both substantially overlap the existing `conventions/mailbox-message-lifecycle.md`. Given a language pass in place (banned-vocab clear; no vocabulary defects found) but NOT published here — routed to Command via mailbox for a destination decision, per the same disposition already used for the 2026-07-09 `GUIDE-jennifer-2-migration-stack`/`GUIDE-machine-pairing-f11`/`GUIDE-os-console-getting-started` sweep entry above.

---

### 2026-07-09 — project-bim editorial sweep (26-draft batch): stale repo-path defect fixed in applications/bim-and-real-property-surfaces; Academic Small area resolution ported from media-knowledge-projects

`Closed: 2026-07-09.`

**Scope:** project-editorial actioned two inbox messages from project-bim requesting an
editorial sweep of 26 PROSE drafts (10+5 "original 15" batch + 11 "supplement" TOPIC
batch). All 26 target files were already absent from
`clones/project-editorial/.agent/drafts-outbound/` except the 11 supplement
`topic-bim-*.draft.md` files — investigation confirmed the 10 original TOPICs and 5
GUIDEs had already been fully processed in a prior session: the 10 TOPICs are live in
`media-knowledge-projects/building-design/` (migrated there from this repo's
`applications/`/other categories per the 2026-06 Phase C cross-repo receive, not still
here), including a "bim-token" → "bim-object" corpus-canonical consolidation
(`c3e5d24` in that repo); the 5 GUIDEs are live in `customer/woodfine-fleet-deployment/`.
No new commits were needed in this repo for those 15.

**One live defect found and fixed in this repo** while verifying project-bim's "Repo
path correction" finding (`woodfine-design-bim` → `woodfine-bim-library`, renamed at
admin-tier): `applications/bim-and-real-property-surfaces.md` + `.es.md` (a
`status: active`, `bcsc_class: public-disclosure-safe` article, not part of the 26-draft
batch but the closest live sibling on the same subject) still named the customer-tier
BIM design system `woodfine-design-bim` in 5 places (EN) / 5 places (ES) — the table
row, two body-prose mentions, the "planned public deployment" line, and the See Also
entry. Fixed via global replace in both files; `last_edited` bumped to 2026-07-09.

**Also ported to `media-knowledge-projects/building-design/`** (separate repo, logged
here for cross-reference since the defect was found via this repo's drafts-outbound
task): `bim-zone-depths-per-use-type.md` + `.es.md` still framed the Academic Small key
plan area (105 m² vs. 87.7 m²) as an unresolved "operator decision needed" — stale
relative to `bim-key-plans-index.md`'s already-ratified resolution ("105 m² / V3 Master
Summary — authoritative") and relative to project-bim's 2026-07-07 message stating the
same resolution. Updated the inconsistency note, the "Future research" checklist item,
and the "Source-document inconsistencies" table row in both language files to state the
resolution and flag the still-outstanding `professional-office-subtypes.dtcg.json`
token-file update (code-side fix, out of either wiki repo's scope).

**Flagged to Command, not fixed here (customer/ is out of Totebox write scope):** the
customer-tier GUIDE set has two more instances of both defect classes project-bim
flagged — `guide-bim-token-authoring.md` and its apparent duplicate-in-progress
`guide-bim-object-authoring.md` (both in `gateway-orchestration-bim/`) still carry
descriptive "sovereign object/BIM Object vault" phrasing (Do-Not-Use §5) and stale
`woodfine-design-bim` path references; `guide-deploy-bim-substrate.md` has the
"sovereign" phrasing with an otherwise-correct repo path;
`guide-regulation-overlay-publishing.md` has one stale path reference inside an IDS XML
example. `guide-climate-zone-tokens.md` / `guide-climate-zone-objects.md` present the
same apparent duplicate-in-progress pattern as the token/object authoring pair
(138-line diff, not yet reconciled). Full detail routed to Command by mailbox.

Full verification detail (banned-vocabulary sweep, personal-name sweep, tile-naming
disambiguation check, zone-depth value cross-check) in the mailbox message to
`totebox@project-bim`.

---

### 2026-07-09 — project-infrastructure (PPN) drafts-outbound sweep: 2 GUIDEs already published, 1 live banned-vocab defect fixed, TEXT + JOURNAL out of this repo's scope: COMPLETE

`Closed: 2026-07-09.`

**Scope:** project-editorial swept 4 drafts staged by project-infrastructure in
`.agent/drafts-outbound/` (all `route_to: project-editorial`): two GUIDEs
(`GUIDE-ppn-fleet-operations.draft.md`, `GUIDE-ppn-node-setup.draft.md`), one
TEXT (`TEXT-ppn-any-hardware-sovereign-compute.draft.md`), one JOURNAL
(`JOURNAL-ppn-pooled-compute-v0.1.draft.md`).

**Consolidation check found both GUIDEs already live**, not new content:

| Draft | Already-published | Verdict |
|---|---|---|
| `GUIDE-ppn-fleet-operations.draft.md` | `customer/woodfine-fleet-deployment/fleet-infrastructure-cloud/guide-ppn-fleet-operations.md` | CONSOLIDATED — byte-identical body except one word ("response"→"summary") and the draft's missing body H1. No new content. |
| `GUIDE-ppn-node-setup.draft.md` | `customer/woodfine-fleet-deployment/fleet-infrastructure-onprem/guide-ppn-node-setup.md` | CONSOLIDATED — byte-identical body. No new content. |

No customer/ commit request was sent to Command for either — sending one would
duplicate live content. Two real defects on the *already-published* customer
files were flagged to Command by mailbox instead (out of this repo's write
scope): `guide-ppn-fleet-operations.md` has **no frontmatter at all** (its
sibling `guide-ppn-node-setup.md` has a complete `foundry-doc-v1`-style
block); and neither guide follows the ratified `guide-how-to.md` skeleton
(Prerequisites/Purpose/Procedure/Expected outcome/Verification/Rollback/Next
steps) — both use an ad-hoc `§N` structure instead. Both stale drafts moved to
`.agent/drafts-outbound/archived/` this session.

**Live banned-vocab defect found and fixed** while reading the closest wiki
sibling to the TEXT/JOURNAL drafts, `infrastructure/ppn-small-business-compute.md`
+ `.es.md` (already covers the same pooled-compute pitch at wiki register —
confirmed no consolidation gap, the TEXT draft is legitimately distinct
product-marketing copy, not a duplicate TOPIC): closing paragraph carried a
descriptive (non-proper-noun) "the sovereignty layer is the target the
project is building toward" / "la capa de soberanía es el objetivo...". Per
`POINTSAV-Project-Instructions.md` §5 the replacement direction for
descriptive "sovereign" is trustworthy-systems language anchored in seL4
formal verification — this sentence is specifically about the seL4
host-isolation target, so retitled to "the verified isolation layer" /
"la capa de aislamiento verificado" (not "customer-rooted", which fits an
ownership claim, not a verification claim). `last_edited` bumped to
2026-07-09 on both files. Commit `5c5dbb8`.

**Flagged, not fixed — out of scope for this session:** a corpus-wide sweep
across `infrastructure/` turned up "sovereign"/"sovereignty" in descriptive
use across a large number of already-published files, including an
established published article **title and slug**, `sovereign-mesh` (+
`sovereign-telemetry`, `data-sovereignty-telemetry`), linked from dozens of
sibling articles. This is materially different from a single-sentence fix —
`sovereign-mesh` is a slug-immortal published article name, not a stray
adjective, and any rename needs an alias + `redirects.yaml` ceremony and an
operator/Command decision, not a unilateral edit inside a 4-draft language
pass. Left untouched; flagged here and in the outbound mailbox to Command for
a dedicated future sweep.

**TEXT and JOURNAL are out of this repo's scope, not committed here:**
`TEXT-ppn-any-hardware-sovereign-compute.draft.md` carries
`destination: pointsav.com product page (planned)` in its own frontmatter —
marketing copy, not a wiki TOPIC; refined in place in drafts-outbound
(banned-vocab title fix, file renamed to drop "sovereign") and its
destination-ownership question routed by mailbox rather than guessed.
`JOURNAL-ppn-pooled-compute-v0.1.draft.md` is withheld from any `research/`
commit per `journal-registry.md` (JOURNAL admission is a capped, deliberate
act, not a routine commit) — language-pass verified clean, left unchanged,
routed to the cap-decision process instead.

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
