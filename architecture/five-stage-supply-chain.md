---
schema: foundry-doc-v1
title: "The five-stage sovereign supply chain"
slug: five-stage-supply-chain
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: five-stage-supply-chain.es.md
short_description: "The five-stage sovereign supply chain describes how code moves from a contributor's local environment to a production deployment through five distinct stages, with a double-blind air-gap that lets contributors work on production systems without ever touching production credentials or seeing production data."
cites: []
references:
 - id: 1
 text: "OpenSSF. 'Supply Chain Levels for Software Artifacts (SLSA) v1.0.' Open Source Security Foundation, 2023."
 url: "https://slsa.dev/spec/v1.0/"
 - id: 2
 text: "Hammant, P. 'Trunk Based Development.' trunkbaseddevelopment.com, 2017."
 url: "https://trunkbaseddevelopment.com/"
---

Code moves from a contributor's local environment to a production deployment through five distinct stages — each with a defined actor, a specific action, and an industry-standard counterpart. The arrangement is deliberately circular: every working session begins by resetting to the freshly-verified vendor truth, eliminating the logic drift that accumulates when contributors build atop their own outdated branches. A single governance gate — the administrator's squash-and-merge — is where intellectual property transfers and experimental commits are collapsed into a single corporate record. [^1] This article covers the five stages, the double-blind air-gap, and the repository topology.

## The five stages

| Stage | Actor | Action | Industry equivalent |
|---|---|---|---|
| 1 — Backup | Contributor | `git push` to their personal GitHub fork | Remote backup / feature branch push |
| 2 — Offer | Contributor → Vendor | Open pull request into `pointsav/<repo>` | Code review submission |
| 3 — Audit | Vendor (`ps-administrator`) | Squash-and-merge into the vendor ledger | Atomic commit / golden master creation |
| 4 — Transfer | Vendor → Customer | Mirror push of the verified release tag | Release propagation |
| 5 — Deploy | Customer → Production | `git pull --ff-only` onto production hosts | Golden image deployment |
| (Loop) — Reset | Vendor → Contributor | `git fetch upstream && git rebase` | Trunk-based synchronisation |

## What each stage accomplishes

**Stage 1 — Backup.** The contributor pushes work-in-progress to their own GitHub fork (`jwoodfine/...` or `pwoodfine/...`). The fork is the contributor's private safety net. Nothing in the corporate ledger is yet affected.

**Stage 2 — Offer.** The contributor opens a pull request from their fork into the vendor organisation (`pointsav/...`). The work becomes visible to the administrator. Automated checks may run; code review begins.

**Stage 3 — Audit.** The administrator (`ps-administrator`) performs a squash-and-merge. This is the legally significant moment: the contributor's commit history is collapsed into a single corporate commit signed by the administrator's SSH key. Ownership transfers to PointSav Digital Systems. Earlier experimental commits, prototype attempts, and abandoned approaches do not survive into the corporate ledger.

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
| `github.com/pointsav` | Vendor — source of truth | `ps-administrator` only (accepts merges); `jwoodfine`/`pwoodfine` (fork and PR) |
| `github.com/woodfine` | Customer — production ledger | `mcorp-administrator` only |
| Contributor personal accounts | Forge — sandbox | The contributor owns their fork outright |

The canonical repositories as of mid-2026 include:

| Repository | Role |
|---|---|
| `pointsav/pointsav-monorepo` | All `os-*`, `app-*`, `service-*`, `system-*` code |
| `pointsav/content-wiki-documentation` | Public documentation wiki |
| `woodfine/woodfine-fleet-deployment` | Customer deployment catalogue and GUIDE articles |

## Why this structure scales

A new contributor does not need to learn a new protocol. They fork, they push, they open a pull request. The architectural gates — the squash-merge IP transfer, the customer mirror, the fast-forward deploy, the trunk-based reset — happen above them. The contributor's daily experience is just Stage 1.

The structure scales to many contributors without losing the air-gap, because the air-gap is enforced by the administrator gate, not by social rules.

## See also

- [[three-layer-architecture]] — the SOFTWARE / SHOWCASE / INSTANCES layers that the supply chain spans
- [[six-tier-sovereignty-matrix]] — the directory taxonomy of the vendor monorepo at Stage 1
- [[legal-and-ip-structure]] — the IP transfer mechanics that Stage 3 implements
