---
artifact: topic
schema: foundry-doc-v1
type: topic
content_type: topic
slug: app-orchestration-command-branch-model
aliases:
  - app-orchestration-command-branch-model
title: "Per-archive branch model in app-orchestration-command"
category: applications
short_description: "Isolated per-archive branches under the app-orchestration-command coordinator — contamination prevention and independent pace ahead of publication to canonical."
status: active
language_protocol: TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
---

**Correction substantially revised, 2026-08-02.** An earlier pass in this session concluded `app-orchestration-command` "is not a PointSav software product" and "no crate of that name exists anywhere in the monorepo." **That conclusion was wrong**, and the error is itself an important, corpus-wide finding: this archive's local working-tree checkout (`cluster/project-editorial` branch) is stale relative to canonical (`origin/main`) for multiple crates, including this one, `os-orchestration`, and `service-fs`. Checked directly against `origin/main`: `app-orchestration-command/` is real and substantial — a "CommandCentre" HTTP server (`crates/orchestration-command-server/src/main.rs`) with `pairing.rs`, `fleet.rs`, `routing.rs`, `personnel.rs`, `license.rs`, `invite.rs` modules, binding `127.0.0.1:8020` by default, explicitly configured against `COMMAND_PAIRINGS_PATH` (default `/srv/foundry/pairings.yaml`) and `COMMAND_CLONES_ROOT` (default `/srv/foundry/clones`) — real Foundry-workspace paths, consistent with (not a misattribution of) this article's subject. `os-orchestration/` is also real on `origin/main`, though its own `src/lib.rs` is a 4-line placeholder scaffold — the aggregator functionality itself isn't built there yet, so hedging that specific claim to planned/intended still likely applies, but "the crate doesn't exist" was the wrong framing.

**What this correction does NOT do**: verify the *specific* branch-isolation/publication mechanics this article describes (the per-archive branch model, the coordinator's filter logic) against the real `orchestration-command-*` crates found above — that re-verification hasn't happened yet and is a needed follow-up, not something to assume either confirmed or refuted. Treat every earlier correction in this documentation category that asserted "os-orchestration/app-orchestration-command doesn't exist as a built crate" with the same caution — see the BRIEF's 2026-08-02 entry for the full list of affected articles and their status.

Each [[totebox-archive|Totebox Archive]] in the `app-orchestration-command` topology operates on its own isolated branch — separate from the canonical `main` that the coordinator manages. This article explains why that isolation exists, what it protects, and how the coordinator enforces the boundary during publication.

## Why Isolated Branches

A Totebox Archive's isolated branch serves as a private development surface. It holds the full working history of the archive: code commits, working-state commits, and anything in between. The canonical `main`, by contrast, holds only what has been published — code that passed the pre-publication gate, is signed, and is permanently on the record.

Isolated branches exist for two reasons:

1. **Contamination prevention.** Without isolation, every session commit — including operational notes, drafts, and session-memory updates — would risk entering canonical history. The isolated branch is the containment layer. Only the coordinator's publication filter decides what crosses into canonical.
2. **Independent pace.** Twenty-one archives running on a single shared branch would block each other constantly. Each archive's isolated branch develops at its own rate. Commits to one archive's branch have no effect on another's.

## What Goes to Canonical

When the coordinator publishes an archive's work, it cherry-picks only the commits that modify source code:

- Source files (`.rs`, `.ts`, `.html`, `.css`, and so on)
- Build manifests (`Cargo.toml`, `Cargo.lock`, package files)
- Tests and fixtures
- Documentation that ships with the code (inline, `README.md` files in the crate)

These commits are applied to `origin/main` as a fast-forward or, where the archive branch has diverged, as a filtered cherry-pick sequence.

## What Stays on the Archive Branch

Working-state files are durable and valuable to the archive but are not suitable for canonical history:

- Session memory and operator preference digests
- Draft documents awaiting editorial review
- Operational notes and inter-archive messages
- In-progress briefs

These commits remain on the archive's isolated branch indefinitely. For durability, the coordinator pushes the archive branch to the staging mirror (the `jwoodfine` or `pwoodfine` remote) so it is preserved off-machine. It never reaches `origin/main`.

## The Coordinator's Publication Filter

During publication, `app-orchestration-command` walks the commit list between the archive's branch tip and the current `origin/main` HEAD. For each commit, it applies the filter:

- **Code commit** → cherry-pick to `origin/main`.
- **Working-state-only commit** → skip; remain on archive branch.
- **Mixed commit** (code + working-state) → resolve in favour of the incoming code changes; working-state files are excluded from the cherry-picked result.

The filter runs identically regardless of whether the archive initiated publication itself or delegated the request to the coordinator.

## WORM History Relationship

Canonical `origin/main` behaves like a [[worm-ledger-architecture|write-once, read-many (WORM) record]]: each published commit is cryptographically signed by the administrator identity and is permanent. The archive branch, in contrast, is mutable — archives rebase against `origin/main` before publication to resolve any divergence, which rewrites their local branch history. This rewrite never touches the canonical record.

## Parallel Velocity

Because each archive has its own isolated branch, development across 21 archives is concurrent. Archive A's 50 commits this week do not block Archive B from publishing its 3 commits, and Archive B's publication does not interfere with Archive A's pending work. The only serialized step is canonical publication itself — and that serialization is by design, to maintain audit integrity.

## Related Topics

- [[app-orchestration-command-publication-flow]] — criteria, eligibility model, and offline behavior
- [[scaling-coordinated-development-totebox-archives]] — the coordination challenge at scale
