---
schema: foundry-doc-v1
title: "Project Triad Discipline"
slug: project-triad-discipline
category: reference
type: topic
quality: published
short_description: The predecessor three-leg structural rule for project clusters — vendor code, customer runbook, and deployment instance — now superseded by the Project Tetrad Discipline.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: project-triad-discipline.es.md
---

The Project Triad Discipline was the structural rule, introduced in Doctrine version 0.0.4, that required every active project cluster to maintain three legs simultaneously: vendor-tier source code, a customer-facing operational runbook, and a working deployment instance. It has been superseded by the [[project-tetrad-discipline]] as of Doctrine version 0.0.10, which adds a fourth mandatory leg for wiki TOPIC contributions. This article documents the Triad's design rationale, which remains the foundation of the Tetrad.

## The problem the Triad addressed

Without structural enforcement, software projects drift toward three predictable failure modes. Code matures without accompanying runbooks, leaving each new deployment dependent on the original contributor's tribal knowledge. Runbooks mature without corresponding code, producing documentation for software that does not yet exist. Both legs mature without any tested runtime, leaving the first production deployment as the de-facto test environment.

The Triad made all three failure modes structurally impossible by requiring that a cluster articulate where each of its three legs lives before it can be ratified as a milestone-bearing project. A cluster that cannot locate its customer leg has not yet earned its cluster.

## The three legs

**Vendor leg.** Generic, tenancy-agnostic source code committed on the cluster's feature branch in a sub-clone drawn from a vendor-tier canonical repository. Vendor-leg code is parameterised by module identifier rather than hardcoded to a specific tenant, allowing the same crate to serve the PointSav reference deployment and any future customer deployment without modification.

**Customer leg.** Operational runbooks in a fleet-deployment catalog subfolder. The convention names the subfolder by deployment shape and tenant. Runbooks cover the operator's perspective: provisioning, day-to-day operation, upgrades, decommissioning, recovery, and monitoring. Their voice is pragmatic and operator-facing rather than engineering-facing.

**Deployment leg.** A numbered runtime instance in the deployment instances directory. The instance carries a manifest declaring its tenant, purpose, source version, and current state. Multiple projects may share a deployment instance when they cohabit at runtime. The instance is local-only — never published to a version-control remote — because it contains runtime state, configuration with potentially sensitive values, and transient data that have no place in a shared history.

## Why this is a cluster-level, not a commit-level, discipline

Individual commits may touch one leg only. A commit that adds a feature to a Rust crate without touching any runbook is not a violation. The discipline applies to the cluster's output over the cluster's lifetime: all three legs must be walking at any ratified milestone, even if they walk at unequal pace. A cluster may be eighty percent vendor work and twenty percent runbook and deployment work; what matters is that the non-dominant legs are present and advancing.

## Tenancy mapping

The customer leg always points to a fleet-deployment catalog subfolder that matches the deployment's tenant. A cluster deploying under the PointSav tenant uses the PointSav fleet-deployment catalog; a cluster deploying under a customer tenant uses that customer's fleet-deployment catalog. A project deploying under both tenancies carries two customer legs, one in each catalog.

## Trajectory capture

Every commit on a cluster's feature branch, from any leg, enters the engineering corpus. The corpus is leg-aware through the files-changed field on each structured record, making it possible to observe whether a cluster is drifting toward single-leg maintenance over time. A cluster adapter trained across all three legs learns code-writing, runbook-writing, and deployment-procedure-writing as a single composable capability rather than three separate skills.

## Relationship to the Tetrad

The Triad is retained here as a historical reference. All new clusters, and all existing clusters after their Tetrad-upgrade broadcast, follow the [[project-tetrad-discipline]]. The Triad's three legs are unchanged inside the Tetrad; only the fourth leg is new.

## See also

- [[project-tetrad-discipline]] — The current four-leg discipline that supersedes this convention.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
