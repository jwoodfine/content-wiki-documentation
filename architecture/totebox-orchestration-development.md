---
schema: foundry-doc-v1
title: "Totebox Orchestration as the Development Environment"
slug: totebox-orchestration-development
category: architecture
type: topic
quality: complete
short_description: "PointSav's development environment is itself deployed as a Totebox Orchestration instance — the workspace that builds the platform runs on the same architecture the platform delivers to customers."
status: active
bcsc_class: forward-looking
last_edited: 2026-05-08
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: totebox-orchestration-development.es.md
---

PointSav's development environment is deployed as a Totebox Orchestration instance — the same architecture the platform delivers to customers. The Foundry workspace, where the platform is written and shipped, runs as a hub coordinating thirteen Totebox Archives over a single shared `service-slm` access-control gateway. The development workflow is the customer workflow. There is no test environment that diverges from production architecture; the environment that produces the code is the architecture the code describes.

This article documents how the workspace maps onto Totebox Orchestration, what the Command Session and Totebox Sessions own, and which components are operationally live versus planned.

## What Totebox Orchestration is

Totebox Orchestration organises work into Totebox Archives — self-contained units, each holding source code, operational guides, a live deployment, and a wiki contribution. A Command Session acts as the hub: it holds pairings to every archive and coordinates cross-archive work. A Totebox Session opens within a single archive and operates only within that archive's declared scope.

The Foundry workspace maps directly onto this topology:

| Foundry concept | Totebox Orchestration equivalent |
|---|---|
| The workspace at `~/Foundry/` | Command Session — hub, identity store, cross-archive coordination |
| Each `clones/project-*/` directory | A Totebox Archive |
| A session opened in a cluster clone | A Totebox Session |
| `service-slm` access-control gateway | The shared Orchestration AI routing layer |
| `vault-privategit-source-1` (declared in `MANIFEST.md`) | The Command instance identity |

Thirteen Totebox Archives are currently active in the workspace, covering the building-information, geographic-information, editorial, design, knowledge, marketing, bookkeeping, proofreading, and platform-infrastructure concerns. Two additional development archives are planned to complete the topology — `project-source` for PointSav canonical-tier work and `project-woodfine` for Woodfine customer-tier work.

## The Command Session

The Command Session starts at the workspace root. Its scope:

- Workspace documentation and conventions
- The identity store at `identity/` — cryptographic keys for every contributor identity
- The `bin/` toolchain — scripts for committing, promoting, and opening archives
- Cross-archive governance: ratifying milestones, routing messages, sweeping outboxes
- Virtual-machine system administration
- `pairings.yaml` — the operational topology record (see [[pairing-as-permission]])

The Command Session is the only session that can write workspace-level files. Individual Totebox Sessions route cross-archive requests as messages to the Command Session rather than reaching across archives directly.

## Totebox Sessions

A Totebox Session opens within a specific archive at `~/Foundry/clones/<archive>/`. It works inside that archive — writing code, committing to staging branches, drafting wiki content, updating the deployment. It does not write to other archives, does not modify workspace files, and does not have direct access to the identity store.

The intended entry point is `bin/open-archive.sh <archive-name>`, planned to read the archive manifest, surface the archive's tetrad status and pending messages, set archive-scoped environment variables, and open a session at the archive's root directory. This is intended to mirror how a customer or community member opens a Totebox Archive via `os-console`: the development workflow is the same as the customer workflow.

## The retired Root session

Earlier versions of the workflow included a Root session that opened directly inside engineering repositories (`vendor/content-wiki-*`, `vendor/pointsav-design-system`). Customers never had an equivalent — there is no Root mode in the Totebox model — so the role had no architectural justification.

The replacement uses two dedicated development Totebox Archives: `project-source` for PointSav canonical-tier work and `project-woodfine` for Woodfine customer-tier work, both planned. All repository work is intended to flow through these archives, then promote to the canonical ledger via Stage 6 (`bin/promote.sh`). The `vendor/` and `customer/` directories are canonical ledger destinations — work is pushed to them, never opened in them for AI sessions.

## The Project Tetrad

Every Totebox Archive declares a Project Tetrad: four legs that together represent its complete contribution to the platform.

| Leg | What it holds |
|---|---|
| vendor | Source code in `pointsav-monorepo` — the implementation |
| customer | Operational guides in `woodfine-fleet-deployment` — how to use it |
| deployment | Live instance in `~/Foundry/deployments/` — the running service |
| wiki | Articles in `content-wiki-documentation` or `content-wiki-projects` — the knowledge contribution |

An archive with all four legs ratified is complete. Archives with pending legs carry `leg-pending` status and a plan. The Command Session ratifies tetrad completeness as part of milestone review.

## The shared access-control gateway

Every Totebox Archive routes inference through the same `service-slm` access-control gateway instance. The gateway is multi-tenant: it accepts requests tagged with an `X-Foundry-Module-ID` header identifying which archive is making the request, routes to the appropriate compute tier, and enforces per-tenant boundaries on every call.

A single `service-slm` instance currently serves all thirteen active archives. Each archive's manifest declares `slm_endpoint: http://localhost:8011`, pointing at this shared instance. When archives eventually move to separate virtual machines, each machine is intended to run its own gateway instance — the manifest field updates with no other changes required of calling code.

## The two-node architecture

The workspace is intended to run on two separate compute nodes:

**os-orchestration node** — the development environment. Hosts the Command Session, all Totebox Archives, the `service-slm` access-control gateway, source code, and workspace tooling. Intelligence work, code development, and staging are intended to happen here. Not accessible from the public internet.

**os-mediakit node** — the delivery layer. Hosts the live public websites, nginx, and production service instances. Receives deployments from the os-orchestration node via a deliberate human-gated rsync bridge. No source code, no development work, no direct connection to the os-orchestration node.

The separation is designed so that a development incident — a failing test, a disk-full event, an unfinished feature — cannot affect the live public websites. The rsync bridge is intended as the deliberate human gate between development and production, consistent with the [[sys-adr-19|SYS-ADR-19]] discipline of no automated publishing to live environments.

## "We built PointSav on PointSav"

The architectural claim is provable from artefacts already in place:

- The workspace is declared as `vault-privategit-source-1` in `MANIFEST.md` — a Totebox instance in the canonical sense.
- Thirteen Totebox Archives are active, each following the Project Tetrad discipline.
- The shared `service-slm` access-control gateway is operationally live (177 of 177 tests passing) and serves as the Orchestration AI routing layer.
- The commit flow — staging branches promoted via `bin/promote.sh` to the canonical ledger — is the Totebox promotion pipeline.
- The inbox-and-outbox file protocol is the AI session coordination protocol — the same pattern customers are intended to use for cross-archive communication.

The intended next step is the planned `app-orchestration-command` application: a hub aggregator exposing a live HTTP interface for archive health, message routing, and personnel permission checks. The cluster (`project-command`) is provisioned; the application is the next implementation milestone.

## See also

- [[pairing-as-permission]]
- [[doorman-protocol]]
- [[compounding-substrate]]
- [[apprenticeship-substrate]]
