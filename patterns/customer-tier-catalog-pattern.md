---
schema: foundry-doc-v1
title: "The Customer-Tier Catalog Pattern"
slug: customer-tier-catalog-pattern
category: patterns
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-10
editor: pointsav-engineering
paired_with: customer-tier-catalog-pattern.es.md
---

The customer tier separates deployment definitions from deployment instances. The catalog records what a deployment is — its runbooks, required artefacts, and operational scope. Numbered instances record where and how a specific copy of that deployment runs. The two shapes live at different paths, follow different tracking rules, and serve different purposes. Conflating them is a recurring operational mistake in fleet management; the naming convention and path structure make the distinction visible at a glance.

## Catalog and Instance Are Different Shapes

A catalog entry describes a deployment without encoding any tenant-specific or environment-specific values. It is reusable: multiple instances of the same deployment name may run in parallel across different tenants, or at different times for the same tenant. The catalog is what a new instance is provisioned *from* — not what it runs *as*.

An instance encodes the values that make the catalog concrete: the tenant identifier, the running service version, the environment-specific configuration, and any runtime state local to this copy. Instance data may include credentials or binding details that must not reach a shared code repository. The instance is what is actually running.

This distinction informs two further properties: how each shape is tracked and where each lives in the filesystem.

## What Lives in the Catalog

Catalog entries live at `customer/woodfine-fleet-deployment/<deployment-name>/` and are tracked in the fleet-deployment repository. A catalog entry is tenancy-agnostic: its contents describe the deployment as a service definition, not as a running copy.

Required artefacts in a catalog entry:

- `README.md` and `README.es.md` — plain-language description of what the deployment does
- `MANIFEST.md` — structured metadata covering deployment name, source version, and lifecycle state
- `guide-*.md` files — operational runbooks for the deployment; these belong inside the catalog entry directory, not at the fleet-deployment repository root

The GUIDE files inside a catalog entry are the operational counterparts to the TOPIC articles that describe what the service does. A GUIDE describes *how to operate this deployment* for the person running it. It is scoped to a specific deployment name, not to a general pattern, which is why it lives in the catalog entry rather than anywhere else in the repository.

## What Lives in the Instance

Instances live at `~/Foundry/deployments/<deployment-name>-N/` where `N` is a one-based sequential integer distinguishing concurrent or successive instances of the same deployment name. This path is gitignored at the workspace level: instances do not appear in any repository.

Required artefacts in an instance:

- `MANIFEST.md` — created from the shared deployment MANIFEST template; carries the fields that distinguish this instance from others: tenant, source version, instance number, and current lifecycle state
- `README.md` and `README.es.md` — copied or generated at provisioning time

An instance may accumulate additional runtime artefacts after provisioning: log files, local configuration, connection details, and similar materials that are specific to the running environment and not appropriate for shared version control. The gitignore boundary keeps these local by default.

## Deployment Names and the Prefix Taxonomy

Deployment names follow the fleet prefix taxonomy drawn from the nomenclature matrix. Seven canonical prefixes define the semantic scope of each deployment category:

| Prefix | Scope |
|---|---|
| `fleet-` | Multi-node distributed fleet services |
| `route-` | Routing and traffic management layers |
| `gateway-` | External-facing gateway services |
| `cluster-` | Cluster-level coordination and archive services |
| `node-` | Single-node services in a named node role |
| `media-` | Customer-facing content-processing and knowledge services |
| `vault-` | Storage, ledger, and cryptographic services |

The prefix makes the deployment's role readable without consulting its MANIFEST. A deployment named `media-proofreader-woodfinegroup` is immediately classifiable: it is a media-tier content-processing service, the proofreader variant, scoped to the `woodfinegroup` tenant. The tenant segment at the end of the name supports future multi-instance expansion — a second tenant would use a different suffix rather than creating a naming collision.

## Worked Example: media-proofreader-woodfinegroup

The proofreader service for the `woodfinegroup` tenant demonstrates the catalog/instance pattern directly.

The catalog entry at `customer/woodfine-fleet-deployment/media-proofreader-woodfinegroup/` carries the README pair describing the editorial pipeline service, the deployment MANIFEST, and the operational runbooks for initial setup and day-to-day operation. This catalog entry is version-controlled and visible to any contributor with access to the fleet-deployment repository.

The instance at `~/Foundry/deployments/media-proofreader-woodfinegroup-1/` carries the running configuration: the service version pinned at provisioning time, the tenant-specific binding details, and any runtime state accumulated since startup. The `-1` suffix is the instance number. If the deployment were reprovisioned from scratch, or if a parallel instance for testing were created, the next number would increment.

The MANIFEST in the catalog entry records the deployment name and source version at the time the catalog entry was authored. The MANIFEST in the instance records the same fields plus the tenant, the instance number, and the current lifecycle state. Reading the two MANIFESTs side by side makes the catalog-to-instance relationship explicit without requiring external documentation.

## Provisioning and Decommissioning

Provisioning a new instance begins by reading the catalog entry: the README and GUIDE files describe the deployment's purpose and the steps to bring it up. The provisioning session creates the `deployments/<name>-N/` directory, writes a MANIFEST from the template, and applies any per-instance configuration. Credentials, external API keys, and DNS bindings are operator-supplied at provisioning time; they are not part of the catalog entry and do not travel through version control.

Decommissioning follows a two-party model. The session that owns the instance performs the graceful tear-down: it stops the running service, archives any runtime state worth preserving, and removes the `deployments/<name>-N/` directory. A separate workspace coordination step records the completion of the tear-down in the workspace change log.

The catalog entry persists after decommissioning. A future instance of the same deployment name can be provisioned from the same catalog entry without any changes to the fleet-deployment repository. The catalog is the definition; the instance is the transient realisation of that definition.

## See Also

- [[editorial-pipeline-three-stages]] — the three-stage pipeline that the proofreader service instance runs
- [[language-protocol-substrate]] — the genre family substrate the pipeline implements
- [[os-totebox]] — the operating environment in which cluster-type deployments run
