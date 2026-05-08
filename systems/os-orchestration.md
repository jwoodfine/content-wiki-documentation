---
schema: foundry-doc-v1
title: "OrchestrationOS"
slug: os-orchestration
category: systems
type: os
quality: complete
short_description: "OrchestrationOS is the operating-system layer that manages a Totebox Archive cluster — aggregating archives, exposing a unified interface for operators, and routing AI session coordination messages between archives."
status: active
bcsc_class: forward-looking
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: os-orchestration.es.md
---

OrchestrationOS (`os-orchestration`) is the operating-system layer that manages a Totebox Archive cluster. It aggregates the archives it oversees, exposes a unified interface for operators and other orchestration nodes, and routes AI session coordination messages between archives. Three per-project instances are operationally live in the workspace today; the planned `app-orchestration-command` aggregator that exposes the unified interface is the next implementation milestone.

This article describes the two roles an orchestration instance can occupy, the live per-project instances, and how cross-archive coordination preserves the [[pairing-as-permission]] invariant.

## Roles

**Command** — A single Command instance is paired to every Totebox Archive, both os-mediakit nodes, and both os-privategit nodes. The Command is the hub of the Totebox Orchestration topology. It is the only node with full cross-archive visibility; its pairing list is the operational topology record.

**Per-project instances** — Each active project cluster runs its own orchestration instance scoped to that cluster's archives. A per-project instance is paired to its own archives only. It has no pairing with the Command (communication flows by message, not direct connection) and no pairing with sibling per-project instances.

## Live per-project instances

The following per-project orchestration instances are currently live in the Foundry workspace:

| Instance | Cluster | Scope |
|---|---|---|
| `gateway-orch-bim-1` | `project-bim` | Building-information archives |
| `gateway-orch-gis-1` | `project-gis` | Geographic-information archives |
| `gateway-orch-proofreader` | `project-proofreader` | Proofreader application archives |

Additional per-project instances are planned as remaining clusters complete their tetrad legs.

## CommandCentre

`app-orchestration-command` — referred to as CommandCentre — is the intended hub aggregator application running on the Command orchestration instance. It is planned to expose:

- `GET /archives` — health and tetrad status of all paired Totebox Archives
- `POST /message` — accepts a cross-archive coordination message, validates per-caller scope (the confused-deputy defence), and routes to the target archive
- `GET /personnel/<user>` — returns a contributor's permission tier and pairing set

CommandCentre is the intended implementation of the Command hub. The cluster (`project-command`) is provisioned; the application is pending implementation.

## Relationship to os-mediakit

Orchestration and os-mediakit run on separate physical nodes by design. The orchestration node handles development, staging, and all archive work. The os-mediakit node handles public website delivery. They communicate through a human-gated rsync bridge — a deliberate deployment gate consistent with `SYS-ADR-19` (no automated AI publishing to verified ledgers).

## Cross-archive coordination

Per-project orchestration instances do not connect to each other directly. When `project-bim` needs information from `project-editorial`, it sends a message to the Command. The Command, paired to both, fetches the data and returns it, or routes the message onward. No lateral connection is created. The topology does not change. PairingAsPermission is preserved.

The pattern — isolated processes plus a message-passing hub — means a compromised per-project instance cannot reach sibling archives. The connection literally does not exist. See [[pairing-as-permission]] for the formal security basis.

## See also

- [[totebox-orchestration-development]]
- [[pairing-as-permission]]
- [[totebox-session]]
- [[doorman-protocol]]

## References

- **`DOCTRINE.md`** — Foundry constitutional charter; Totebox Orchestration topology.
- **`MANIFEST.md`** — workspace passport; Command instance identity declaration.
