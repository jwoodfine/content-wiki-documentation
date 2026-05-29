---
schema: foundry-doc-v1
title: "Totebox session"
slug: totebox-session
category: architecture
type: topic
quality: complete
short_description: "A Totebox Session is an AI-assisted contributor session opened within a single Totebox Archive — scoped to the archive's declared repositories, unable to write outside them, and the standard entry point for all development work in Totebox Orchestration."
status: active
bcsc_class: forward-looking
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: totebox-session.es.md
---

A Totebox Session is an AI-assisted contributor session opened within a single [[totebox-archive|Totebox Archive]]. It is scoped to the archive's declared repositories and cannot write outside them. From the contributor's perspective, opening a Totebox Session is how every development task in [[totebox-orchestration|Totebox Orchestration]] begins. The session protocol mirrors the customer experience: the contributor's entry point in the workspace and the customer's entry point through [[console-os|`os-console`]] perform the same function.

This article describes how a session is opened, what it can and cannot do, the four permission tiers, and the inbox-and-outbox protocol that coordinates work across archives.

## How to open a session

The intended entry point is the `open-archive` console command, planned for invocation from the hub session. When invoked, it is intended to:

1. Read the archive manifest at `clones/<archive>/.agent/manifest.md`
2. Print the archive name, tetrad status, AI gateway endpoint, and count of pending inbox messages
3. Check the contributor's permission tier against the personnel record (see [[personnel-permissions]])
4. Set the `FOUNDRY_ARCHIVE` and `FOUNDRY_MODULE_ID` environment variables
5. Open an AI session at the archive's root directory

This mirrors the customer experience: a community member or customer opens a [[totebox-archive|Totebox Archive]] through [[console-os|`os-console`]]. The development workflow uses the same entry point, adapted for the workspace.

## Session scope

A Totebox Session:

- Writes to any repository declared in the archive's manifest
- Commits to the archive's staging branch (never directly to the canonical `main`)
- Routes inference through the shared [[service-slm|`service-slm`]] access-control gateway ([[doorman-protocol|Doorman]]) using the archive's module identifier
- Sends cross-archive requests as messages to the hub session (never writes to other archives)
- Stages wiki drafts in `.agent/drafts-outbound/` for the editorial pipeline

A Totebox Session does not:

- Write workspace-level configuration or tool files
- Write to the identity store
- Access the canonical source trees directly (those receive content by promotion, not direct write)
- Open connections to sibling archive sessions

## The Project Tetrad

Every Totebox Archive declares four legs of the Project Tetrad. A session's work contributes to all four:

| Leg | Session writes to |
|---|---|
| vendor | Feature code in the archive's `pointsav-monorepo` clone |
| customer | Operational guides in the archive's `woodfine-fleet-deployment` clone |
| deployment | Provisioning the running instance in the deployment directory |
| wiki | TOPIC draft files staged in `.agent/drafts-outbound/` |

The hub session ratifies tetrad completeness when all four legs are present.

## The AI session coordination protocol

Sessions communicate through the inbox-and-outbox file protocol:

- Each archive holds `.agent/inbox.md` and `.agent/outbox.md` files
- A Totebox Session reads its inbox at session start and archives actioned messages
- Outbound requests to other archives or to the hub session are prepended to `.agent/outbox.md` (newest on top)
- The hub session sweeps archive outboxes during workspace review and routes messages

In the planned next phase, `app-orchestration-command` (CommandCentre) is intended to broker all cross-archive messages by HTTP, with each message transiting the access-control gateway and the immutable ledger automatically. The file-based protocol is intended to remain as the fallback and the development-mode mechanism.

## Permission tiers

Four tiers govern what a contributor — and the session they open — can do:

| Tier | Label | Pairing set |
|---|---|---|
| P1 | System Administrator | Command + every archive + every infrastructure node |
| P2 | Package Manager | Specific archives plus Stage 6 promotion paths |
| P3 | User | Specific archives; no Command pairing; read-only cross-archive |
| P4 | Interface | Read-only API surface only |

Tiers are enforced by pairings, not string comparisons. A P3 contributor's `os-console` is not paired to the Command — the connection does not exist. See [[pairing-as-permission]] for the formal mechanism.

## Relationship to os-console

[[console-os|`os-console`]] is the customer-facing entry point for opening a [[totebox-archive|Totebox Archive]]. In the development workspace, the `open-archive` command is the equivalent. Both are intended to perform the same function: read the archive manifest, validate the contributor's permission scope, set the session context, and open a working session inside the archive. The development environment uses the same pattern the customer is intended to use.

## See also

- [[totebox-orchestration-development]]
- [[pairing-as-permission]]
- [[personnel-permissions]]
- [[doorman-protocol]]
