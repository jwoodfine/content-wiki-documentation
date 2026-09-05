---
schema: foundry-doc-v1
title: "Five-stage supply chain"
slug: five-stage-supply-chain
category: security
index_group: supply-chain-controls
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "The path from a contributor's commit to a customer deployment crosses three repository tiers and two organisations, gated by a heavily guarded promotion script. There is no pull request and no second-party review."
paired_with: five-stage-supply-chain.es.md
---

**The supply chain** is the path a change travels from the machine where it was written to the
deployment where it runs, together with the controls applied at each handover. Its security value
comes from the handovers themselves: each boundary is a place where a change can be inspected,
filtered, or refused, and where the identity of what crossed is recorded. This platform's chain
crosses three repository tiers held by two organisations and one intermediate mirror layer, with
the substantive gating concentrated in a single promotion script. It is described here as five
stages — a description of the path this article organises for clarity, not a citation of a
pre-existing named framework (see below for why that distinction matters).

Two structural facts shape everything else. First, contributors and customers never share a
repository — a contributor writes into a personal staging mirror and a customer reads from a
separate organisation's catalogue, with the vendor repository between them. Second, the automated
gates are content and shape filters, not human review.

## The five stages

| Stage | Actor | Action today |
|---|---|---|
| 1 — Backup | Contributor | Push work-in-progress to a personal staging mirror |
| 2 — Offer | Contributor → Vendor | Commit via the workspace commit helper, directly visible to the administrator |
| 3 — Audit | Vendor administrator | Promotion tooling replays verified commits onto the canonical branch and pushes |
| 4 — Transfer | Vendor → Customer | Governance propagation mirrors verified state to the customer organisation |
| 5 — Deploy | Customer → Production | Fast-forward-only pull onto production hosts |
| (Loop) — Reset | Vendor → Contributor | Fetch canonical and rebase the next cycle's work on top |

**Stage 1 — Backup.** The contributor pushes work-in-progress to their own staging mirror. It is a
private safety net; nothing in the vendor's canonical record is affected.

**Stage 2 — Offer.** Today, the offer *is* the commit — there is no pull-request or review-gate
step in the current tooling. The workspace commit helper produces the commit on the working branch
with a verified contributor identity as author, an SSH signature, and identifying trailers, and
that committed work is directly visible to the vendor administrator once pushed to staging.

**Stage 3 — Audit.** The vendor's promotion script carries verified work onto the canonical branch.
It does not merge in the ordinary sense: for a working branch, it checks out a temporary branch
from the canonical head and replays each qualifying commit onto it individually, filtering out
session-state and workspace-internal paths so only reviewable code reaches the canonical record.

**Stage 4 — Transfer.** A separate governance propagation step mirrors the verified release from
the vendor organisation to the customer organisation's deployment catalogue. The customer receives
finished, verified state and never sees in-flight contributor commits.

**Stage 5 — Deploy.** The customer pulls the verified state onto production hosts under a
fast-forward-only constraint, so production cannot silently diverge from the customer's own
catalogue.

**The Loop.** The contributor fetches the canonical result and rebases the next cycle's work onto
it, so every participant starts each cycle from the same verified point rather than building for
weeks atop a diverging branch.

## Repository tiers and the double-blind separation

Three content tiers exist, and the flow between them is one-directional by design.

**Source.** The vendor organisation holds the canonical repositories — the authoritative copy of
the code and the only tier that a promotion writes to.

**Catalogue.** The customer organisation holds the deployment catalogue — the packaged, versioned
descriptions from which an instance is provisioned. Content reaches it by the separate governance
propagation step named as Stage 4 above.

**Instances.** Provisioned deployments live outside version control entirely, are local to the
machine that runs them, and are excluded from every repository.

Alongside these sit two personal staging accounts used purely as mirrors. Every working clone
carries three remotes: the canonical repository reached through an administrative access alias, and
one staging mirror per contributor identity. Work is pushed to the staging mirrors freely; only the
promotion script writes to the canonical remote, and only from a session holding the canonical key.

This arrangement produces the chain's defining security property: who cannot see whom. A
contributor pushing to their own mirror has no path to the customer catalogue, and a customer
reading the catalogue has no visibility of the mirror — neither can observe the other's activity
through the repositories they can reach, and the vendor is the sole party with visibility of both
ends. This scales with contributor count: adding contributors adds Stage 1–2 activity, not new
paths into the customer's environment.

## Committing

Every commit is created through a single helper script rather than by invoking Git directly — a
rule enforced by the commit-time gate described in [[pre-commit-defense-in-depth]].

The helper alternates between two contributor identities on each commit, tracked by a toggle file
under the identity store and protected by a file lock so that concurrent sessions cannot race it;
the toggle is written atomically through a temporary file and rename. It signs each commit with
that identity's own SSH key, and repairs the local repository's signature-verification
configuration on first use so that later log inspection verifies without extra setup. It adds three
trailers recording the archive, the engine, and the session; detection failures degrade to an
"unknown" value rather than blocking the commit.

The helper does not stage files and does not push. Both are deliberate: staging is explicit so that
no change is swept in unintentionally, and pushing is a separate decision made later.

## Promotion to canonical

The promotion script is where the chain's real gating lives, and its length is substantially guard
code. For a working branch it replays each qualifying commit individually onto a temporary branch
from the canonical head, handling merge commits against their first parent, regenerating the
dependency lockfile where that is the only conflict, and stopping for manual resolution on a
genuine code conflict. For the administrative repositories it performs a fast-forward push only,
after confirming the canonical head is an ancestor of the local head.

Session-state files never cross: a filter matches the agent state directory, the engine
instruction files, the session configuration, the working-notes and changelog files, and staging
directories, strips them from any commit landing during promotion, and a final gate re-checks the
tree about to be pushed and refuses outright if any such path survived.

The remaining guards, each of which can stop a promotion: a lock directory preventing concurrent
runs; a scope check confirming the session is entitled to promote; a formatting, lint, and test
gate; a required-remotes check; a branch-match check; a clean-working-tree check; a
staging-mirror-synchronisation check; a fast-forward-possible check that blocks true divergence; a
business-data path filter that exits without self-certification; a mass-deletion guard above a
configured threshold; a silent-revert guard above the same threshold for content quietly reverted
to an older canonical state; a content-pattern check for real entity names in the design repository; a top-level path
allowlist for the canonical repository; forced interactive confirmation for the publicly visible
repositories even in non-interactive mode; and a final confirmation prompt. The deletion and revert
overrides are themselves logged to a bypass record.

Archives granted a self-service permission may instead push their own branch to the staging mirrors
and append a record to a promotion queue file, which prepends a notification to the coordinating
session's inbox. That script never writes to the canonical remote — it is an asynchronous work
queue for a later, privileged promotion run, not a promotion in itself.

## What the chain does not include

There is no pull request anywhere in this pipeline. A whole-tree search of canonical source and the
workspace scripts for source-forge API clients, pull-request creation and merge commands, and
review tooling returned matches only inside vendored third-party projects' own upstream continuous
integration configuration — none belonging to this platform.

The consequence is that the ownership transfer at the vendor boundary is accomplished by a single
replayed commit under the promotion script's guards, not by a reviewed and squashed pull request.
The outcome — the change becoming part of the vendor's canonical history, ownership transferring to
PointSav Digital Systems — is the same either way; the mechanism is not, and describing it as a
review-gated merge would misstate what protects the boundary.

## What this is not

**This is not a five-stage sequence that the platform's own documentation defines.** A search of
every top-level governance document and the conventions directory found no definition of a "Stage
1" through "Stage 4" anywhere as an established, cross-referenced term. Exactly two numbered stages
are named in existing material: a governance propagation step toward the customer catalogue, and
the canonical promotion step. The five-part framing above is this article's own descriptive
organisation of the real pipeline steps, not a citation of a pre-existing canonical term.

**There is no pull request and no code review gate.** The only human step in promotion is a
confirmation prompt answered by the operator running the script — the same party performing the
promotion. No second party approves a change before it reaches canonical.

**Promotion is not a squash merge.** For working branches it is a commit-by-commit replay onto a
branch taken from the canonical head; for administrative repositories it is a fast-forward push.
Contributor commit history is not collapsed by the administrator.

**The guards are shape filters, not judgement.** They match paths, count deleted files, and detect
reverted content. They do not assess whether a change is correct, safe, or desirable.

**Three tiers is not three organisations.** Two organisations hold repositories; the third tier is
local, unversioned deployment instances. The staging mirrors are personal accounts, not
organisations.

**The chain is not the platform's data plane.** Customer data never travels this path in either
direction — its protections are the [[cryptographic-ledgers|ledger]] and
[[machine-based-auth|authorization]] layers, not the supply chain.

## See also

- [[pre-commit-defense-in-depth]] — the commit-time checks preceding every promotion
- [[contributor-model]] — the two-identity contribution arrangement and its rationale
- [[registry-driven-releases]] — how a promoted change becomes a versioned release
- [[legal-and-ip-structure]] — the ownership arrangement the vendor boundary implements
- [[software-distribution-substrate]] — how released artefacts reach customers
- [[authenticate-binary-downloads]] — verification available to a recipient of a built artefact
- [[machine-based-auth]]
