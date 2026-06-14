---
schema: foundry-doc-v1
title: "Totebox orchestration"
slug: totebox-orchestration
category: systems
type: topic
content_type: topic
quality: complete
short_description: "Totebox Orchestration describes the coordination layer that manages multiple Totebox data-archive containers, keeping software execution engines isolated from passive corporate ledgers across deployments."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: totebox-orchestration.es.md
---


Totebox Orchestration is the coordination layer that provisions, monitors, and manages multiple [[totebox-archive|Totebox archive]] instances within a single PointSav deployment. When an operator maintains separate archives for contracts, financial records, and correspondence, the orchestration layer ensures each container keeps its own isolated [[worm-ledger-design|ledger]], runs its own integrity verification pass, and reports health status through a unified monitoring surface — without allowing any container to share mutable state with another. For a regulated operator, this means a compromise in one domain cannot propagate to records held in another.

## Container isolation

Each Totebox runs as an independent unit backed by the [[sel4-microkernel-substrate|seL4 microkernel's]] hardware isolation guarantees. No container shares a ledger directory with any other container. A compromise in one container's asset directory does not propagate to sibling containers, because there is no shared mutable state at the ledger layer.

## Integrity verification

The orchestration layer schedules periodic checksum audits across all managed containers. Results are written to a consolidated audit record. Any checksum mismatch raises a flag at the orchestration level before surfacing to the operator.

## Provisioning and lifecycle

A new Totebox container is provisioned with a three-directory skeleton — `app-console-input/`, `assets/`, and `ledger/` — and registered with the orchestration layer at creation time. The orchestration layer tracks container state across its operational lifecycle: active, suspended, or archived. The [[deployment-patterns|deployment patterns]] article describes how Totebox Orchestration appears in each canonical fleet configuration.

## See also

- [[totebox-os]] — the operating system running inside each managed Totebox
- [[totebox-archive]] — the fundamental unit of data storage being orchestrated
- [[infrastructure-os]] — the compute substrate hosting the Totebox instances
- [[console-os]] — the Command Ledger that operators use to interact with orchestrated archives
- [[os-orchestration]] — the fleet-level OS aggregator for multi-entity commercial deployments
