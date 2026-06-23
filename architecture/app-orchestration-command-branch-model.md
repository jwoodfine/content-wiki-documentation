---
schema: foundry-doc-v1
content_type: topic
title: "The Per-Archive Branch Model in app-orchestration-command"
slug: app-orchestration-command-branch-model
short_description: "Each Totebox Archive operates on its own isolated branch, separate from the canonical main that the coordinator manages. The coordinator's publication filter decides what crosses from the archive branch into canonical history."
category: architecture
type: reference
quality: complete
status: stable
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: app-orchestration-command-branch-model.es.md
cites: []
---

Each Totebox Archive in the `app-orchestration-command` topology operates on its own isolated branch — separate from the canonical `main` that the coordinator manages. This article explains why that isolation exists, what it protects, and how the coordinator enforces the boundary during publication.

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

Canonical `origin/main` behaves like a write-once, read-many (WORM) record: each published commit is cryptographically signed by the administrator identity and is permanent. The archive branch, in contrast, is mutable — archives rebase against `origin/main` before publication to resolve any divergence, which rewrites their local branch history. This rewrite never touches the canonical record.

## Parallel Velocity

Because each archive has its own isolated branch, development across 21 archives is concurrent. Archive A's 50 commits this week do not block Archive B from publishing its 3 commits, and Archive B's publication does not interfere with Archive A's pending work. The only serialized step is canonical publication itself — and that serialization is by design, to maintain audit integrity.

## Related Topics

- [[app-orchestration-command-publication-flow]] — criteria, eligibility model, and offline behavior
- [[scaling-coordinated-development-totebox-archives]] — the coordination challenge at scale

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
