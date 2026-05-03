---
schema: foundry-doc-v1
title: "Totebox Orchestration"
slug: topic-totebox-orchestration
category: systems
type: topic
quality: stub
short_description: "Totebox Orchestration describes the coordination layer that manages multiple Totebox data-archive containers, keeping software execution engines isolated from passive corporate ledgers across deployments."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-totebox-orchestration.es.md
---

# Totebox Orchestration

> Totebox Orchestration describes the coordination layer that manages multiple Totebox data-archive containers, keeping software execution engines isolated from passive corporate ledgers across deployments.

**Totebox Orchestration** is the layer responsible for provisioning, coordinating, and monitoring individual Totebox instances in a PointSav deployment. A Totebox is an isolated data container that separates active software engines from passive corporate ledgers. The container stores data as inert flat files; cryptographic checksums verify structural integrity on a permanent basis.

When a customer operates more than one Totebox — for example, separate archive containers for contracts, financial records, and correspondence — the orchestration layer ensures each container maintains its own isolated ledger, runs its own integrity verification pass, and reports health status through a unified monitoring surface.

## Container isolation

Each Totebox runs as an independent unit. No container shares a ledger directory with any other container. A compromise in one container's asset directory does not propagate to sibling containers, because there is no shared mutable state at the ledger layer.

## Integrity verification

The orchestration layer schedules periodic checksum audits across all managed containers. Results are written to a consolidated audit record. Any checksum mismatch raises a flag at the orchestration level before surfacing to the operator.

## Provisioning and lifecycle

A new Totebox container is provisioned with a three-directory skeleton — `app-console-input/`, `assets/`, and `ledger/` — and registered with the orchestration layer at creation time. The orchestration layer tracks container state across its operational lifecycle: active, suspended, or archived.

## See Also

- [[topic-os-totebox]]
- [[topic-customer-hostability]]
- [[topic-substrate-native-compatibility]]

## References
