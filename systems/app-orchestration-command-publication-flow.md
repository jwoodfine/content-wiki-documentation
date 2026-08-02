---
artifact: topic
schema: foundry-doc-v1
type: topic
content_type: topic
slug: app-orchestration-command-publication-flow
aliases:
  - app-orchestration-command-publication-flow
title: "How app-orchestration-command publishes archive changes"
category: systems
short_description: "Publication mechanics under app-orchestration-command — how tested code crosses from archive branches into signed canonical history, with code-only filtering."
status: active
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

**Correction (2026-08-02):** `app-orchestration-command` is not a PointSav software product — no crate of that name exists anywhere in the monorepo. This article's own `research_trail` cites `AGENT.md`/`pairings.yaml`, the Foundry *workspace's own internal* multi-archive coordination tooling (the Command Session), not a shipping product. See the companion article [[app-orchestration-command-branch-model]] for the full finding. The publication mechanics described below broadly match Foundry's real internal `bin/promote.sh`/Stage-6 flow, but are presented here as a customer-facing PointSav product running on `os-orchestration`, which is also not built. **Flagged, not resolved.**

`app-orchestration-command` is the coordinator service that moves tested code from individual [[totebox-archive|Totebox Archives]] into the canonical `pointsav/*` and `woodfine/*` repositories. This article explains what publication means, who may initiate it, and how the system behaves when the coordinator is unavailable.

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

- [[app-orchestration-command-branch-model]] — how archive isolation prevents working-state contamination of canonical history
- [[scaling-coordinated-development-totebox-archives]] — the coordination challenge as archive count grows
