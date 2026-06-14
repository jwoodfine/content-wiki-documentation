---
schema: foundry-doc-v1
title: "Personnel and permissions"
slug: personnel-permissions
category: architecture
type: topic
content_type: topic
quality: complete
short_description: "Contributor identity and permissions in Totebox Orchestration are expressed through cryptographic pairings — not roles stored in a database or checked at request time — and a contributor can reach a resource only if their os-console is paired with the orchestration node that manages it."
status: active
bcsc_class: forward-looking
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: personnel-permissions.es.md
---

In [[totebox-orchestration|Totebox Orchestration]], contributor identity and permissions are expressed through cryptographic pairings — not through roles stored in a database or checked at request time. The permission model is [[pairing-as-permission|PairingAsPermission]]: a contributor can reach a resource only if their [[console-os|`os-console`]] instance is paired with the orchestration node that manages that resource. The four permission tiers (P1 through P4) describe what a contributor's pairing set looks like; enforcement is always through the pairing topology.

This article describes contributor identity, the four tiers, how permissions are granted, and the relationship to the planned `app-orchestration-command` aggregator.

## Contributor identity

Each contributor has:

- A **machine identity** — an [[console-os|`os-console`]] instance with a cryptographic certificate tied to that specific hardware. The certificate is the identity; there is no username-and-password authentication.
- A **personnel record** — an entry in the data tier holding the contributor's display name, role, SSH public key, and permission tier.
- A **pairing set** — the list of nodes their [[console-os|`os-console`]] is paired with, establishing which archives, [[mediakit-os|`os-mediakit`]] nodes, and [[os-privategit|`os-privategit`]] instances they can reach.

The personnel store is itself a [[totebox-archive|Totebox Archive]] — it does not use a separate identity service.

## Permission tiers

Four tiers describe what a contributor's pairing set looks like. The tier is not a runtime check; it is a human description of the pairings. Enforcement is always through the pairing topology.

**P1 — System Administrator**
Pairing set: the hub session, every Totebox Archive, both `os-privategit` nodes, both `os-mediakit` nodes, virtual-machine infrastructure.
Can: provision archives, update workspace documentation, run code promotion flows, add new pairings, manage the identity store, perform virtual-machine system administration.

**P2 — Package Manager**
Pairing set: specific archives plus promotion paths.
Can: commit and promote within assigned archives. Cannot provision new archives or modify workspace-level documents.

**P3 — User**
Pairing set: specific archives only. No hub pairing.
Can: work within assigned archives — write code, commit to staging, draft wiki content. Cannot: access cross-archive resources directly, modify other archives, or run promotion flows. Cross-archive requests are sent as messages for the hub session to process.

**P4 — Interface**
Pairing set: read-only API surface only.
Can: query read-only endpoints exposed by archives in the pairing set.
Cannot: write or commit anything.

## How permissions are granted

A new contributor pairing is a P1 operator action:

1. The contributor generates a key pair on their `os-console`.
2. The P1 operator adds the contributor's public key to the relevant node's accepted-peers list and to the Command's `pairings.yaml`.
3. The cryptographic handshake is established.
4. The pairing is recorded as an immutable ledger entry.

There is no approval workflow in a separate system. The pairing is the approval. The ledger entry is the audit trail.

## Example contributor scopes

**A System Administrator (P1):**
Paired to the hub session, every active Totebox Archive, both `os-privategit` nodes, both `os-mediakit` nodes, and the personnel archive. Scope: full workspace. Can ratify tetrad milestones, manage the identity store, provision new archives, run promotion flows.

**A P3 User:**
Paired to a specific project archive — for example, `project-bookkeeping` — and to a local-staging `os-mediakit` for review. Scope: archive work and staging review only. No hub pairing. Cannot access the identity store, other archives, or the canonical source trees.

## Relationship to app-orchestration-command

The planned `app-orchestration-command` aggregator (CommandCentre) is intended to expose a `GET /personnel/<unix-user>` endpoint that returns a contributor's permission tier and pairing set, derived from the personnel archive's data-tier record. CommandCentre is intended to use this to enforce per-caller scope on cross-archive message routing — the confused-deputy defence. The endpoint is part of the next-phase implementation scope.

## See also

- [[pairing-as-permission]]
- [[totebox-orchestration-development]]
- [[totebox-session]]
- [[doorman-protocol]]
