---
schema: foundry-topic-v1
title: "Source-of-truth inversion"
status: published
category: architecture
last_edited: 2026-04-30
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
research_done_count: 6
research_suggested_count: 2
open_questions_count: 0
research_provenance: project-knowledge cluster, sub-agent brief 03, 2026-04-28
research_inline: false
cites:
  - doctrine-claim-29
  - doctrine-claim-34
  - ni-51-102
  - osc-sn-51-721
---

## Pattern statement

Source-of-truth inversion is a named Foundry substrate pattern. In each PointSav application, one storage layer is declared canonical — the authoritative record that is committed, signed, replicated, and disclosed. A second layer is a derived view: the running process's in-memory index, rendered output, or computed summary — rebuilt deterministically from the canonical record on demand and discardable without loss. A third layer, when collaborative editing is enabled, is session-ephemeral: it exists for the duration of a shared editing session and does not write back to canonical until a human author makes a deliberate commit.

The pattern recurs across the wiki engine, the Ring 2 extraction pipeline, and the planned `app-workplace-presentation` and `app-workplace-proforma` applications. In each case, the choice of what is canonical follows the same structural logic: the layer with the longest durability requirement, the strongest audit obligation, and the cleanest replication story is canonical. Everything else is derived.

## Application: wiki engine (anchor instance)

The full treatment of source-of-truth inversion in the wiki engine appears in [[topic-app-mediakit-knowledge]] §2. The summary here: git is canonical; the running binary is a view; the CRDT passthrough relay (Phase 2 Step 7, planned, default-off) is session-ephemeral.

The Tantivy full-text search index, the redb wikilink graph (planned, Phase 4), and all rendered HTML are derived on demand from the Markdown tree on disk. Any of those derived artefacts can be discarded and rebuilt; none is backed up; none is disclosed. The git tree is what is backed up, replicated, signed, and disclosed. The binary cannot accumulate state that the git tree does not have.

This case grounds the pattern with a live deployment: `https://documentation.pointsav.com` has served this substrate since 2026-04-27.

## Application: service-extraction (Ring 2 multi-author review pipeline)

`service-extraction` is the Ring 2 service that runs the multi-author document review pipeline. The source-of-truth mapping:

**Canonical**: the extraction event log committed to the WORM immutable ledger managed by `service-fs` (live on the workspace VM since v0.1.23, binding `127.0.0.1:9100`, ledger root at `/var/lib/local-fs/ledger/`). An extraction event is durably sequenced the moment it is appended to the ledger; the ledger enforces total order over all events. Ledger entries are not modifiable after the fact — that is what WORM (Write Once Read Many) means structurally, not just operationally. The WORM ledger as canonical storage is an instance of Doctrine claim #29 (Substrate Substitution) applied to Ring 2: instead of a mutable relational database as the authority for review state, the substrate is an append-only signed log.

**View**: the review queue shown to each reviewer is derived from the set of ledger entries that have not yet received a verdict commit. The per-reviewer verdict summary is derived similarly. Neither the queue nor the summary is stored separately — both re-derive on each query from the ledger. The derivation is deterministic: the same ledger produces the same queue and summary every time it is queried.

**Ephemeral**: reviewer annotations made before a verdict commit are session-ephemeral. One reviewer's working annotations cannot see or corrupt another reviewer's working annotations, because those annotations have not yet been committed to the canonical ledger. Concurrent reviewers work against their own in-process state; the ledger reconciles when a verdict commit lands. The total-order enforcement of the ledger is the substrate mechanism that makes concurrent review safe without coordination locks.

## Application: app-workplace-presentation (deck collaboration, planned)

`app-workplace-presentation` is a planned application for collaborative slide-deck authoring. The intended source-of-truth mapping follows the same pattern:

**Canonical**: the slide deck source, intended to be committed to the customer's Git repository under the vault pattern — the customer's Git repository is the canonical authority for presentation content, not a proprietary document server. A commit to the deck's Git repository is the disclosure event; the deck's git history is the audit record.

**View**: rendered slide frames served to browser clients, computed from the committed deck source on demand. The rendered frames are not stored persistently; they are rebuilt from the committed source on each request.

**Ephemeral**: CRDT multi-cursor collaboration state for real-time co-authoring sessions is planned as session-ephemeral. Participating authors see each other's edits in real time via a passthrough relay analogous to the wiki engine's Phase 2 Step 7 relay design. That session-state does not persist between sessions without an explicit commit by a human author. Note: the CRDT collaboration layer for `app-workplace-presentation` is planned; it is not yet implemented as of 2026-04-27.

## Application: app-workplace-proforma (table collaboration, planned)

`app-workplace-proforma` is a planned application for collaborative structured-data editing — proforma tables, financial schedules, and structured documents used in regulated business contexts. The source-of-truth mapping:

**Canonical**: the proforma table, intended to be committed as structured data (CSV or structured Markdown with a schema declaration) in the customer's Git repository. The schema declaration travels with the data, making the committed artefact self-describing.

**View**: the rendered table UI with computed fields — totals, cross-row references, conditional formatting — derived from the canonical structured data on each render. Computed fields are not stored in the canonical record; they re-derive. This matters for proforma contexts where a formula change must produce consistent derived values everywhere the formula is referenced, with no cached stale values possible because the cache is not canonical.

**Ephemeral**: CRDT cell-level collaboration state during shared editing sessions is planned as session-ephemeral, following the same commit-gated persistence model as `app-workplace-presentation`. Nothing persists to the canonical record until an explicit commit. The authoritative number is the one committed and signed in git — not the rendered value in a browser tab that may reflect unsaved session edits. The pattern enforces that distinction structurally: the only way to change the canonical record is a commit. Note: the CRDT collaboration layer for `app-workplace-proforma` is planned; it is not yet implemented as of 2026-04-27.

## Why this pattern matters

**BCSC continuous-disclosure posture.** In each application, canonical is the disclosed state. Per `conventions/bcsc-disclosure-posture.md` and [ni-51-102] continuous-disclosure requirements, the record that is disclosed is the record that is signed, committed, and replicated — not the rendered view, not the search index, not the session-ephemeral CRDT buffer. Source-of-truth inversion enforces this by construction: the substrate cannot accidentally disclose a view-layer artefact as authoritative because the view is explicitly not the record. The audit trail for any disclosed claim is a `git log`; the claim lives in a signed commit. This property is not achieved by policy — it is a structural consequence of the storage layer designation.

**Doctrine claim #34 (Two-Bottoms Sovereign Substrate).** Claim #34 establishes that the same `os-*` binaries run on both substrate bottoms (native seL4 and compatibility NetBSD) via a thin shim. The application-layer consequence is that canonical storage must be kernel-agnostic: a signed git tree and a signed WORM ledger entry are valid records regardless of which OS kernel the view process runs on. Source-of-truth inversion achieves this — by keeping the canonical record as signed structured data (git commits, ledger entries) and the view as a derived process, the substrate binaries can move between bottoms without the canonical record changing its identity. The deeper seL4/NetBSD design is treated in [[topic-substrate-native-compatibility]]; the connection here is only the kernel-agnostic canonical storage claim.

The pattern is not application-specific. It recurs because the same structural logic applies wherever a substrate needs a clear audit record, clean replication, and collaboration that does not corrupt the canonical state. The four applications above are four instances of one pattern, not four independent design decisions.

## See also

- [[topic-app-mediakit-knowledge]] — Anchor instance of the pattern (git as canonical).
- [[collab-via-passthrough-relay]] — The session-ephemeral layer in detail.
- [[topic-substrate-native-compatibility]] — Kernel-agnostic canonical storage in the context of Two-Bottoms Sovereign Substrate.
- [[topic-disclosure-substrate]] — The broader disclosure-posture convention this pattern satisfies.

## Provenance

Authored by project-knowledge Task Claude (sub-agent brief 03, 2026-04-28). Refined by project-language, 2026-04-30. Load-bearing references: Doctrine claims #29 and #34, `app-mediakit-knowledge/ARCHITECTURE.md` §2, `infrastructure/local-fs/` (service-fs WORM ledger), `conventions/disclosure-substrate.md`.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
