---
schema: foundry-doc-v1
title: "Five-stage sovereign supply chain"
slug: five-stage-supply-chain
category: security
type: concept
content_type: topic
quality: complete
status: archived
archived: 2026-08-03
archived_reason: "superseded by fresh-draft-first authoring pilot against new content-schema tokens (schema-topic.yaml)"
superseded_by: five-stage-supply-chain
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-30
editor: pointsav-engineering
paired_with: five-stage-supply-chain.es.md
short_description: "Code path from contributor environment to production in five stages, with a double-blind air-gap keeping production credentials and data out of contributors' reach."
cites: []
references:
  - id: 1
    text: "OpenSSF. 'Supply Chain Levels for Software Artifacts (SLSA) v1.0.' Open Source Security Foundation, 2023."
    url: "https://slsa.dev/spec/v1.0/"
  - id: 2
    text: "Hammant, P. 'Trunk Based Development.' trunkbaseddevelopment.com, 2017."
    url: "https://trunkbaseddevelopment.com/"
---

**Correction — Stages 2/3 rehedged to planned/intended (2026-07-30):** this article
described a GitHub fork → pull-request → squash-and-merge model in unhedged present
tense for Stages 2 and 3. The current, real commit/promotion mechanism works
differently: `~/Foundry/bin/commit-as-next.sh` commits directly to the working branch
with alternating `jwoodfine`/`pwoodfine` author identity (no PR, no review gate), and
`~/Foundry/bin/promote.sh` cherry-picks commits directly onto the canonical branch and
pushes — confirmed by reading both scripts, and reconfirmed by a broader cross-archive
sweep (grep for `octokit`/`api.github.com/repos`/`gh pr create`/`gh pr merge`/
`create_pull` across every script and crate in all ~25 Totebox archives: zero matches
anywhere). `AGENT.md`'s own "How to commit" section documents the same
direct-commit-then-promote flow. The double-blind air-gap concept and the
three-organisation topology (`pointsav`/`woodfine`/personal staging mirrors) remain
accurate structural descriptions and are left as current-tense fact below — only
Stages 2 and 3's specific PR/squash-merge mechanics are rehedged to planned/intended
language per operator direction, since the real mechanism achieves a similar
end-to-end effect (contributor commit → vendor-side audit/consolidation → canonical
record) through direct-commit-and-cherry-pick rather than a GitHub PR review gate.

Code moves from a contributor's local environment to a production deployment through five distinct stages — each with a defined actor, a specific action, and an industry-standard counterpart. The arrangement is deliberately circular: every working session begins by resetting to the freshly-verified vendor truth, eliminating the logic drift that accumulates when contributors build atop their own outdated branches. A single governance gate — the administrator's squash-and-merge — is where intellectual property transfers and experimental commits are collapsed into a single corporate record. [^1] This article covers the five stages, the double-blind air-gap, and the repository topology.

## The five stages

| Stage | Actor | Action | Industry equivalent |
|---|---|---|---|
| 1 — Backup | Contributor | `git push` to their personal GitHub fork | Remote backup / feature branch push |
| 2 — Offer *(planned mechanics)* | Contributor → Vendor | Today: direct commit via `commit-as-next.sh`. Intended design: open pull request into `pointsav/<repo>` | Code review submission |
| 3 — Audit | Vendor (`ps-administrator`) | Today: `promote.sh` cherry-picks the commit onto the canonical branch. Intended design: squash-and-merge into the vendor ledger | Atomic commit / golden master creation |
| 4 — Transfer | Vendor → Customer | Mirror push of the verified release tag | Release propagation |
| 5 — Deploy | Customer → Production | `git pull --ff-only` onto production hosts | Golden image deployment |
| (Loop) — Reset | Vendor → Contributor | `git fetch upstream && git rebase` | Trunk-based synchronisation |

## What each stage accomplishes

**Stage 1 — Backup.** The contributor pushes work-in-progress to their own GitHub fork (`jwoodfine/...` or `pwoodfine/...`). The fork is the contributor's private safety net. Nothing in the corporate ledger is yet affected.

**Stage 2 — Offer.** Today, the contributor's committed work becomes visible to the administrator directly through `commit-as-next.sh`'s commit — there is no pull-request or review-gate step in the current tooling. The intended design calls for the contributor to open a pull request from their fork into the vendor organisation (`pointsav/...`), with automated checks and code review; this is not yet how the mechanism runs.

**Stage 3 — Audit.** Today, `promote.sh` cherry-picks the verified commit directly onto the canonical branch and pushes — this is the actual mechanism that transfers a contribution into the vendor ledger. The intended design describes this instead as a squash-and-merge performed by the administrator (`ps-administrator`), collapsing the contributor's commit history into a single corporate commit signed by the administrator's SSH key; that specific mechanic is not what runs today, though the effect — ownership transferring to [[pointsav-overview|PointSav Digital Systems]] via a single canonical commit — is accomplished either way.

**Stage 4 — Transfer.** Vendor administration mirrors the verified release tag from `pointsav/<repo>` to `woodfine/<repo>`. The customer receives only signed tags and never sees in-flight contributor commits. This is the release propagation step that firewalls the customer from upstream risk.

**Stage 5 — Deploy.** The customer pulls the verified tag onto its production hosts. The `--ff-only` constraint ensures that production cannot accumulate merge conflicts — it must mirror the customer's GitHub ledger exactly. If a deploy fails, the failure surfaces immediately rather than silently diverging.

**The Loop — Reset.** The contributor fetches the verified vendor state into their local environment and rebases their next work on top. Every working session begins from the same point as every other contributor. [^2]

## The double-blind air-gap

The cycle has one structural rule beyond its mechanics: the contributor never pushes to the customer's organisation, and the customer never reads contributor forks. The vendor is the only entity that sees both ends. The contributor and the customer are mutually invisible to each other through the supply chain.

This is the air-gap that lets contractors work on production systems without ever touching production credentials or seeing production data.

## Repository topology

The supply chain operates across three GitHub organisations, each with a specific role:

| Organisation | Purpose | Who writes |
|---|---|---|
| `github.com/pointsav` | Vendor — source of truth | `ps-administrator` only (promotes/pushes); `jwoodfine`/`pwoodfine` (commit to staging mirrors) |
| `github.com/woodfine` | Customer — production ledger | `mcorp-administrator` only |
| Contributor personal accounts | Forge — sandbox | The contributor owns their fork outright |

The canonical repositories as of mid-2026 include:

| Repository | Role |
|---|---|
| `pointsav/pointsav-monorepo` | All `os-*`, `app-*`, `service-*`, `system-*` code (see [[os-family-overview|OS family overview]]) |
| `pointsav/content-wiki-documentation` | Public documentation wiki |
| `woodfine/woodfine-fleet-deployment` | Customer deployment catalogue and GUIDE articles |

## Why this structure scales

A new contributor does not need to learn a new protocol. Today, that means: commit via `commit-as-next.sh`, and the promotion gates — cherry-pick to canonical, the customer mirror, the fast-forward deploy, the trunk-based reset — happen above them. The contributor's daily experience is just Stage 1.

The structure scales to many contributors without losing the air-gap, because the air-gap is enforced by the administrator gate, not by social rules.

## See also

- [[three-layer-architecture]] — the SOFTWARE / SHOWCASE / INSTANCES layers that the supply chain spans
- [[six-tier-sovereignty-matrix]] — the directory taxonomy of the vendor monorepo at Stage 1
- [[legal-and-ip-structure]] — the IP transfer mechanics that Stage 3 implements
