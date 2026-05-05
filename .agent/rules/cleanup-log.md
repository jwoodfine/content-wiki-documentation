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

Last updated: 2026-04-30.

---

## Open

### 2026-04-30 — Wikipedia normalization pass + 5 architecture/reference TOPIC pairs committed

Session: project-language Task (session 2026-04-30, continuation from session 12376c0e4bc33ea7).

**Commits this session** (6 commits, alternating Jennifer/Peter Woodfine):

1. `07d2d25` — Wikipedia-structure normalization of all 40 root topic-*.md files + index.md: foundry-doc-v1 frontmatter, quality grades (complete/core/stub), See Also + References sections, body H1 removed per content-contract §5.2, ADR/emoji headers removed. topic-sovereign-telemetry retitled to "Zero-State Telemetry Architecture" (descriptive "sovereign" removed per BCSC posture).

2. `5aa030f` — NEW: `architecture/compounding-substrate.md` + `architecture/compounding-substrate.es.md` bilingual pair. Slug = `compounding-substrate` (matches featured-topic.yaml pin; `topic-` prefix is content-contract legacy per §3). Closes the featured-pin gap on documentation.pointsav.com home page. Competitive-by-name references removed (structural positioning discipline); BCSC forward-looking framing on quarterly federation cadence.

3. `4c5cca7` — NEW: `architecture/brief-queue-substrate.md` + `.es.md` and `architecture/service-slm-yoyo-operational.md` + `.es.md`. Operational state as of workspace v0.1.91. BCSC forward-looking framing on LoRA training cycle targets.

4. `5c4674c` — NEW: `architecture/pointsav-llm.md` + `.es.md`. Planned Tier 3 product. Competitive comparison section (Sierra/Decagon/Cresta) removed per structural-positioning discipline; replaced with structural market-gap analysis.

5. `cec1003` — NEW: `reference/wikipedia-structure.md` + `.es.md`. 9-panel Main Page anatomy, 16-element article structure, 3 quality tiers, infobox schemas. Research conducted via live web-fetch sub-agent.

**Open state after this session**:
- All 40 root topic-*.md files are now Wikipedia-normalized but remain at root (legacy flat-at-root pattern). Category migration (topic-*.md → architecture/<slug>.md, services/<slug>.md, etc.) is still pending, tracked in the 2026-04-23 cleanup item below. The new architecture/ and reference/ articles use the correct category subdirectory pattern.
- `topic-compounding-substrate.md` at root is now superseded by `architecture/compounding-substrate.md` (the featured-pin version). The root file should be retired at next migration pass.
- `quality:` frontmatter field is in active use across all TOPICs; visual badge rendering is project-knowledge engine scope (not yet implemented).
- Doorman Tier B (`has_yoyo=true`) is live; editorial bilingual passes are a candidate for routing through Doorman (pending `bin/doorman-editorial-call.sh` helper from Master).

### 2026-04-28 — substantial productivity wave (15 new TOPIC publications + 1 collision-merge update)

Session 17230305b03d3e32 (project-language Task) shipped 11 commits to this repo across 2026-04-27 → 2026-04-28, publishing **12 bilingual TOPIC pairs + 1 mid-session merged update**. All at repo root in legacy `topic-*.md` pattern matching the existing flat-at-root convention; future migration to category subdirectories per `naming-convention.md` §10 ratification (still pending operator decision on the 4 §10 sub-questions).

Commits to this repo this session:

- `8bc17cb` — banned-vocab + legacy-name fixes in 3 substrate-explainer TOPICs (compounding-substrate, sovereign-ai-routing, service-slm)
- `6ecc9d1` + `2e0ba67` — rename topic-service-parser → topic-service-extraction (legacy name retired per pointsav-monorepo cleanup-log Completed migrations); body edits applied as follow-up after git-mv state-tracking gap
- `6c1b178` — DELETE README-pointsav-wiki.md (redundant draft per Sonnet sub-agent #14 classification; closed the 2026-04-23 layout-defect entry)
- `73642a8` — Phase 1B explainer TOPIC `topic-decode-time-constraints` bilingual pair (Master's confirmed next-session direction post-Phase 3 substrate-readiness)
- `8d2396f` — meta-recursive Reverse-Funnel TOPIC bilingual pair (first end-to-end pipeline pilot per Doctrine claim #35)
- `bad779c` — PL.6 batch refining 3 PK TOPIC drafts (app-mediakit-knowledge, documentation-pointsav-com-launch, substrate-native-compatibility) bilingual pairs (570 lines, 3 Sonnet sub-agents in parallel)
- `8b6f91a` — PL.1.a collision merge (Master's reverse-funnel draft over my 8d2396f publication; preserved structural skeleton + added Operational implications section + cites updated)
- `fd1ff64` — Wave 2 top-3 substrate-explainer TOPICs (trajectory-substrate, citation-substrate, disclosure-substrate) bilingual pairs (1093 lines, 3 Sonnet sub-agents in parallel)
- `70e0ff2` — Wave 3a refining 2 PD substantives (design-system-substrate, worm-ledger-architecture) bilingual pairs (527 lines)

Plus 1 commit to woodfine-fleet (`7f710f4` — moved GUIDE-mesh-execution → route-network-admin/) + 1 to pointsav-fleet (`362bba0` — refined GUIDE-operate-knowledge-wiki to media-knowledge-documentation/) + 1 to woodfine-fleet (`eb21c6c` — Wave 3b GUIDE-fs-anchor-emitter to vault-privategit-source/).

Total wiki-leg deliverables this milestone: **12 bilingual TOPIC pairs + 2 English-only GUIDEs = 26 markdown files published**. Completed_topics_this_milestone counted in cluster manifest = 21 (tracking TOPICs only; GUIDEs counted separately).

Disciplines applied per cluster-wiki-draft-pipeline.md §6:

1. Banned-vocab grammar — substitutions made in compounding-substrate (next-generation→subsequent), sovereign-ai-routing (leverage→use), substrate-native-compatibility (leverage→control), design-system-substrate (leverage→advantage point), worm-ledger (robust + seamless removed)
2. BCSC continuous-disclosure posture — forward-looking sections in worm-ledger §10-11, decode-time §6, design-system §5/§9, disclosure-substrate §6/§9, reverse-funnel §6, all carry planned/intended/may + cautionary framing per ni-51-102 + osc-sn-51-721
3. Citation registry resolution — 21 unique IDs cited across the 12 TOPIC pairs; all registered in /srv/foundry/citations.yaml
4. Bilingual pair generation per DOCTRINE §XII — Spanish strategic-adaptation overviews (~250-400 words each)

NO body H1 in the new TOPICs (renderer supplies from frontmatter `title:` per content-contract.md §5.2). Discipline correction vs prior Phase 4/Part D files — those still have body H1 from the legacy authoring pattern.

Process note (added to feedback memory `feedback_never_chmod_canonical_identity_store.md`): Bash wrappers for `bin/commit-as-next.sh` invocations should NOT chmod the canonical identity store at `/srv/foundry/identity/`. Per CLAUDE.md §11 action matrix, that's workspace-tier infrastructure (Master scope). Canonical at 0600 mathew-only is the deliberate posture per workspace v0.1.36+ jennifer-setup.md. Tasks that need other identities use per-user copies at `$HOME/.ssh/foundry-keys/` via the commit-as-next.sh `get_sigkey()` resolver. The chmod-then-restore workaround codified in earlier outbox messages is REJECTED.

### 2026-04-27 — Three more substrate-explainer TOPICs (Part D)

Six new files landed at repo root following Master's 2026-04-27 v0.1.26
reply confirming Option 4 as the next-session direction:

- `topic-apprenticeship-substrate.md` + `.es.md`
- `topic-compounding-substrate.md` + `.es.md`
- `topic-contributor-model.md` + `.es.md`

Same legacy `topic-*.md` pattern at root, frontmatter present per
content-contract.md §4. category fields anticipate future migration to
`architecture/` (apprenticeship + compounding) and `governance/`
(contributor-model).

**Naming-convention note**: Master's v0.1.26 reply named the third
TOPIC as `topic-four-tier-contributor-model.md`. The authoritative
convention at `~/Foundry/conventions/knowledge-commons.md` §7 names
the model as "Three-Tier Contributor Model" with three numbered
subsections (Core / Paid / Open). Per workspace CLAUDE.md §6 "use
the operationally correct name in new work; do not silently
propagate stale forms" — landed as `topic-contributor-model.md`
(concise canonical form matching the convention's three-tier
naming). Surfaced to Master in outbox.

### 2026-04-27 — Phase 4 substrate-explainer TOPICs added at repo root

Eight new files landed at repo root on `cluster/project-language` from
the project-language Task session, following the GO AHEAD in Master's
2026-04-27 v0.1.24 reply:

- `topic-language-protocol-substrate.md` + `.es.md`
- `topic-customer-hostability.md` + `.es.md`
- `topic-anti-homogenization-discipline.md` + `.es.md`
- `topic-canadian-simple-copyright.md` + `.es.md`

These are Phase 4 of the project-language cluster brief — public-
facing TOPICs explaining the substrate convention, the customer-
hostability architecture, the anti-homogenization editorial posture,
and the Canadian-simple copyright posture (the operational complement
in `factory-release-engineering/README.md` §6 is the source of
truth; this TOPIC is the public-facing pair).

Layout state: at repo root in the legacy `topic-*.md` pattern,
matching Phase 2 and every existing `topic-*.md` file. **Frontmatter
present** per `content-contract.md` §4 (improvement vs existing
legacy files which mostly carry no frontmatter).

Bilingual pairs per workspace CLAUDE.md §6 (which overrides the
local "English-only wiki content" line in this repo's CLAUDE.md §6;
that drift is logged in workspace NEXT.md v0.1.24 for future Root
pickup per Master's 2026-04-27 v0.1.24 reply).

cites discipline: `ni-51-102` and `osc-sn-51-721` used where the
disclosure language warrants. The Cornell / arXiv 2409.11360 study
on AI homogenization is referenced in prose (no citations.yaml
entry yet — descriptive reference avoids a registry gap). The
Canadian-simple TOPIC references the doctrine without depending
on the GitHub URL of the workspace v0.1.21 / commit `7266884`
that established it (held local-only pending operator decision
per Master's note).

Categorisation hint for the future migration:

| File | Future category |
|---|---|
| `topic-language-protocol-substrate.md` | `architecture/` |
| `topic-customer-hostability.md` | `architecture/` |
| `topic-anti-homogenization-discipline.md` | `architecture/` |
| `topic-canadian-simple-copyright.md` | `governance/` |

Frontmatter `category` fields already declare the targets.
Migration is a `git mv` plus dropping the `topic-` prefix from
the slug field at that time.

### 2026-04-27 — Three style-guide TOPICs added at repo root (legacy pattern, frontmatter present)

Six new files landed at repo root on `cluster/project-language` from
the project-language Task session, following workspace `NEXT.md`
Phase 2 of the cluster brief:

- `topic-style-guide-readme.md` + `.es.md`
- `topic-style-guide-topic.md` + `.es.md`
- `topic-style-guide-guide.md` + `.es.md`

These are Phase 2 of the language-protocol-substrate convention —
public-facing operational documents explaining how to write each
genre. They are the customer-facing pair of
`pointsav-monorepo/service-disclosure/templates/*.toml`.

Layout state: at repo root in the legacy `topic-*.md` pattern,
matching every other existing `topic-*.md` file. **Improvement vs
existing files**: these carry proper YAML frontmatter per
`content-contract.md` §4 (title, slug, category, status,
last_edited, editor, cites). Most existing `topic-*.md` files do
not.

Bilingual pair: the workspace-tier rule (`~/Foundry/CLAUDE.md` §6)
requires bilingual TOPICs and overrides this repo's local
"English-only wiki content" note. Spanish files follow strategic-
adaptation pattern per DOCTRINE.md §XII — not 1:1 translation.
The repo `CLAUDE.md` "wiki content English-only" line is
inherited drift from before the bilingual rule was workspace-
tier; surfacing for a future repo-CLAUDE update pass.

Pending future migration into `reference/` category directory as
part of the broader category-migration item already tracked
above. The new files migrate alongside the existing legacy
topics; no separate migration is needed.

Categorisation hint: `category: reference` is declared in
frontmatter, so the migration into `reference/<slug>.md` is a
straightforward `git mv` plus updating the slug field to drop the
`topic-` prefix (current frontmatter has slug
`topic-style-guide-readme`; future slug becomes
`style-guide-readme` per `naming-convention.md` §5).

### 2026-04-23 — Naming convention draft awaiting ratification

`.claude/rules/naming-convention.md` drafted, status `Draft`.
Four operator decisions pending (see §10 of that file): category
set, investor-audience disposition, front-matter schema changes,
ID format. Until ratified, the nine-category taxonomy and front-
matter extensions are proposed-not-binding; content migration
waits on ratification to avoid migrating twice.

### 2026-04-23 — Migration to contract-conforming layout

The repo's existing content predates `content-contract.md` and the
layout rule. A normalisation pass is required. Scope:

- Add `index.md` at repo root (wiki home).
- Create category directories for the existing content
  (`architecture/`, `services/`, `governance/` at minimum; final
  taxonomy tbd).
- Move existing `topic-*.md` / `TOPIC-*.md` / `TOPIC_*.md` files
  into category directories, normalising filenames to lowercase
  kebab and adding front-matter where absent.
- Write a `_index.md` per category.
- Rewrite cross-article references to `[[slug]]` wikilinks.

Sequencing not yet decided — candidate is to migrate one category
at a time, beginning with `architecture/` (already seeded by the
app-mediakit-knowledge article written 2026-04-23).

### 2026-04-23 — YAML-only structured records need classification

Files at repo root without Markdown bodies, requiring per-file
disposition:

| File | Candidate disposition |
|---|---|
| `sys-adr-06.yaml` … `sys-adr-19.yaml` (11 files) | Become `governance/sys-adr-NN.md` articles with the YAML becoming front-matter plus narrative body |
| `service-content-01.yaml`, `service-egress-01.yaml`, `service-email-01.yaml`, `service-people-01.yaml` | Pair with `services/<name>.md` articles; YAML becomes front-matter structured block |
| `os-workplace-01.yaml` | Become `architecture/os-workplace.md` |
| `topic-3d-asset-tokens.yaml`, `topic-system-slm.yaml`, `topic-system-udp.yaml` | Pair with existing / future topic articles |

No migrations executed yet. Decisions to be made per-file; each
disposition will be logged here when it lands.

### 2026-04-23 — Filename-case normalisation

Three conventions coexist for topic files at repo root:
`topic-*.md`, `TOPIC-*.md`, `TOPIC_*.md`. The content contract
requires lowercase kebab filenames (= slugs). Every existing `.md`
file is renamed as part of the category-migration pass above.
Wikilinks pointing to renamed slugs are rewritten in the same
commit.

### 2026-04-23 — `RESEARCH-BIM-MARKET.md` classification needed

Untracked file at repo root dated 2026-04-22. Not yet read.
Questions: is this repo the right home for market-research
material? If yes, does it belong in a `research/` category or is
it internal-only and should not be committed at all? If no, where
does it go? Decision needed before any commit touches this file.

### 2026-04-23 — `app-mediakit-knowledge.zip` cross-repo handoff

Untracked ZIP at repo root containing the `app-mediakit-knowledge`
Rust crate. Per Nomenclature Matrix §3, `app-*` prefix belongs in
`pointsav-monorepo`. Handoff entry opened in
`handoffs-outbound.md`. This repo will delete the local ZIP once
the destination commit lands in the monorepo; because the ZIP is
untracked, deletion is a plain `rm` rather than `git rm`.

### 2026-04-23 — `upstream` remote is a legacy artefact

Remote `upstream` on this repo points to
`git@github.com:pointsav/pointsav-monorepo.git`. Not used by this
repo's flow; appears to be residual from when wiki content may
have lived inside the monorepo. Removal is non-destructive (`git
remote remove upstream`) but requires explicit approval before a
session executes it.

### 2026-04-23 — `README-pointsav-wiki.md` possibly redundant

File at repo root alongside `README.md`. Contents not yet read.
If it duplicates `README.md` it should be removed; if it carries
unique material it should be merged into `README.md` or moved into
the wiki as an article.

### 2026-04-23 — `glossary-documentation.csv` has no contracted home

`Closed: 2026-05-02.` The glossary has been converted to `reference/glossary-documentation.md` in markdown table format, with proper frontmatter.

---


## Closed

> Closed entries archived to `cleanup-log-archive.md`.
