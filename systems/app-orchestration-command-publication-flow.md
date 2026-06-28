---
artifact: topic
schema: foundry-draft-v1
status: draft
language_protocol: TOPIC
route: project-editorial
target_wiki: documentation.pointsav.com
created: 2026-06-20
session: Session 111 (Command@claude-code)
research_trail:
  source_briefs: [command-10x-dev-environment]
  cross_checks: [BRIEF-10x-dev-environment.md, pairings.yaml, AGENT.md]
  forbidden_terms_cleared: false
---

# How app-orchestration-command Publishes Archive Changes

`app-orchestration-command` is the coordinator service that moves tested code from individual Totebox Archives into the canonical `pointsav/*` and `woodfine/*` repositories. This article explains what publication means, who may initiate it, and how the system behaves when the coordinator is unavailable.

## What Publication Means

Publication is the act of committing reviewed, tested code from a Totebox Archive to the authoritative upstream repository. The result is a signed, permanent entry in the canonical history — one that cannot be revised or retracted without explicit governance action.

Publication moves code only. Working-state files — session memory, draft documents, operational notes — are excluded at the filtering layer and never appear in canonical history. This separation is deliberate: canonical history is an audit record, not an operational journal.

## Why a Central Coordinator

`app-orchestration-command`, running on `os-orchestration`, holds the administrator SSH credential required to write to the canonical repositories. Concentrating publication authority in one place serves three purposes:

1. **Single audit boundary.** Every publication event is recorded by the coordinator. There is no secondary path that could produce an unlogged commit to canonical.
2. **Conflict prevention.** Two archives publishing simultaneously could produce conflicting canonical states. The coordinator serializes publication requests, ensuring each is a clean fast-forward.
3. **History integrity.** The coordinator enforces that only commits passing the publication filter reach `origin/main`. No working-state content enters canonical history regardless of which archive submitted the request.

## Publication Criteria

Before initiating publication, the coordinator verifies:

- The archive's local branch is current with `origin/main` (rebased, no conflicts).
- The working tree is clean (no uncommitted modifications).
- The build and test suite pass (enforced by the pre-publication gate).
- The commit set contains at least one code change (publication with only working-state commits is a no-op and exits cleanly).

Commits that touch only working-state files are detected and skipped automatically. They remain on the archive's isolated branch and are pushed to the staging mirror for durability.

## Eligibility Model

Each Totebox Archive declares a self-service capability level that the coordinator reads before deciding how to handle a publication request:

| Capability level | Who runs publication |
|---|---|
| Full coordinator required | The coordinator must run publication on the archive's behalf. The archive submits a request and waits. |
| Self-service *(planned/intended)* | The archive may initiate publication directly, provided the administrator key is reachable from the archive's environment. The coordinator validates the request after the fact. |
| Not eligible | The archive is in a planning or dormant state. Publication requests are rejected until the archive transitions to an active state. |

The capability level is set by the archive's operator and reviewed during archive provisioning. Upgrading the level requires coordinator approval.

## Offline Behavior

If `app-orchestration-command` is unavailable — scheduled maintenance, a hardware event, or a network partition — archives with pending publication requests write those requests to a durable queue. The coordinator drains the queue on next startup, processing each entry in submission order.

Archives in self-service mode *(planned/intended)* may also write to this queue as a fallback when the administrator key is temporarily unreachable. No publication attempt is silently discarded.

## Related Topics

- [The Per-Archive Branch Model in app-orchestration-command](TOPIC-app-orchestration-command-branch-model.draft.md) — how archive isolation prevents working-state contamination of canonical history
- [Scaling Coordinated Development Across Many Sovereign Archives](TOPIC-scaling-coordinated-development-sovereign-archives.draft.md) — the coordination challenge as archive count grows
