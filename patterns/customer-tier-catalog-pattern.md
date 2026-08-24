---
schema: foundry-doc-v1
title: "Customer-tier catalog pattern"
slug: customer-tier-catalog-pattern
aliases:
  - customer-tier-catalog-pattern
short_description: "Catalog-versus-instance discipline at the customer tier — reusable deployment definitions tracked in git, tenant-specific instances kept out of shared repositories."
category: patterns
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: customer-tier-catalog-pattern.es.md
index_group: deployment-and-configuration
---

The customer tier separates deployment definitions from deployment instances. The catalog records what a deployment is — its runbooks and operational scope. Numbered instances record where and how a specific copy of that deployment runs. **A reader evaluating any single running deployment is looking at an instance; the definition it was provisioned from lives somewhere else entirely.** Changes to one never silently change the other. The two shapes live at different paths and serve different purposes — conflating them is a recurring operational mistake in fleet management.

## Catalog and instance are different shapes

A catalog entry describes a deployment without encoding any tenant-specific or environment-specific values. It is reusable: multiple instances of the same deployment name may run in parallel across different tenants, or at different times for the same tenant. The catalog is what a new instance is provisioned *from*, not what it runs *as*.

An instance encodes the values that make the catalog concrete: the running service version, the environment-specific configuration, and any runtime state local to this copy. Instance data may include credentials or binding details that must not reach a shared code repository. The instance is what is actually running.

## What lives in the catalog

Catalog entries live in the fleet-deployment repository, one directory per deployment name. A catalog entry is tenancy-agnostic: its contents describe the deployment as a service definition, not as a running copy. In practice a catalog entry carries a bilingual README describing what the deployment does, plus operational runbooks scoped to that specific deployment. The runbooks live inside the catalog entry directory, not anywhere else in the repository, precisely because they describe one deployment rather than a general pattern.

## What lives in the instance

Instances live in a gitignored local directory, one per numbered copy of a deployment. This path does not appear in any repository. An instance carries a MANIFEST recording the fields that distinguish it from other copies of the same deployment: the running source version, the instance number, and the current lifecycle state. An instance may accumulate additional runtime artefacts after provisioning — log files, local configuration, connection details — that are specific to the running environment and not appropriate for shared version control.

**The manifest that actually describes a specific running copy lives with that copy, not in the shared catalog** — checking two real deployments confirms this in practice: neither carries a manifest file in its catalog entry, only in its provisioned instance.

## Deployment names and the prefix taxonomy

Deployment names follow the fleet prefix taxonomy. Seven canonical prefixes define the semantic scope of each deployment category:

| Prefix | Scope |
|---|---|
| `fleet-` | Multi-node distributed fleet services |
| `route-` | Routing and traffic management layers |
| `gateway-` | External-facing gateway services |
| `cluster-` | Cluster-level coordination and archive services |
| `node-` | Single-node services in a named node role |
| `media-` | Customer-facing content-processing and knowledge services |
| `vault-` | Storage, ledger, and cryptographic services |

The prefix makes the deployment's role readable without opening its catalog entry. A deployment named `gateway-orchestration-gis` is immediately classifiable: it is an external-facing gateway service, the GIS orchestration variant.

## Worked example: gateway-orchestration-gis

The GIS orchestration deployment demonstrates the catalog/instance pattern directly. Its catalog entry carries the README pair describing the geospatial-orchestration service and the operational runbooks for provisioning, pipeline rebuilds, and adding a new country or chain to the dataset. This catalog entry is version-controlled and visible to any contributor with access to the fleet-deployment repository.

The running instance carries the actual deployed configuration and application state accumulated since provisioning. The instance number is the numeric suffix on the instance directory name. If the deployment were reprovisioned from scratch, or a parallel instance created for testing, the next number would increment.

## Provisioning and decommissioning

Provisioning a new instance begins by reading the catalog entry: the README and runbooks describe the deployment's purpose and the steps to bring it up. The provisioning session creates the instance directory, writes a manifest, and applies any per-instance configuration. Credentials, external API keys, and DNS bindings are operator-supplied at provisioning time — they are not part of the catalog entry and do not travel through version control.

Decommissioning follows a two-party model. The session that owns the instance performs the graceful tear-down: it stops the running service, archives any runtime state worth preserving, and removes the instance directory. A separate workspace coordination step records the completion of the tear-down.

The catalog entry persists after decommissioning. A future instance of the same deployment name can be provisioned from the same catalog entry without any changes to the fleet-deployment repository. The catalog is the definition; the instance is the transient realisation of that definition.

## See also

- [[editorial-pipeline-three-stages]] — an example of a catalog-defined pipeline that a provisioned instance runs
- [[language-protocol-substrate]] — the genre family substrate an editorial-pipeline instance implements
- [[totebox-os]] — the operating environment in which cluster-type deployments run
