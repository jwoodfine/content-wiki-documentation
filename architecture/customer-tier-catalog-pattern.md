---
title: "The Customer-Tier Catalog Pattern"
slug: customer-tier-catalog-pattern
category: architecture
last_edited: 2026-06-29
editor: pointsav-engineering
status: stable
---

The **customer-tier catalog pattern** is the structural principle that separates what a deployment
*is* from where and how it *runs*. A catalog entry records the purpose, required artifacts, and
operational runbooks for a deployment class. An instance records the machine, tenant, version,
and current operational state for one live deployment. The two shapes are tracked in separate
locations under different visibility rules.

## Why catalog and instance are different shapes

A catalog entry is tenancy-agnostic. It contains no credentials, no runtime state, and no
tenant-specific configuration. Because a catalog entry does not change when a new instance is
provisioned, it can be tracked in a GitHub-connected repository and reviewed alongside the
software it deploys. Multiple instances — for different tenants, or for the same tenant at
different versions — can exist simultaneously against a single catalog entry, each carrying
its own MANIFEST.md.

An instance encodes the facts that vary between deployments: the machine it runs on, the
tenant it serves, the source version it was provisioned from, and the current operational
state. Instances may contain secrets or runtime artifacts that must not reach GitHub. They are
therefore local-only, numbered, and gitignored at the workspace level. The naming convention
makes the relationship readable: catalog entry `media-proofreader-woodfinegroup` produces
numbered instances `media-proofreader-woodfinegroup-1`, `media-proofreader-woodfinegroup-2`,
and so on.

## What lives in the catalog (tenancy-agnostic)

The customer-tier catalog lives in the `woodfine-fleet-deployment` repository, tracked in the
`woodfine` GitHub organization. Each deployment name has a subdirectory at
`woodfine-fleet-deployment/<name>/`. The required artifacts inside that subdirectory are:

- `README.md` and `README.es.md` — bilingual description of what the deployment does and
  how it is operated.
- `MANIFEST.md` using the deployment manifest template — records the deployment identity,
  source repository, dependencies, and platform leg assignments.
- One or more `guide-*.md` runbooks describing the steps required to provision, maintain,
  and decommission an instance.

The subdirectory boundary is the scope boundary. Guide files for a deployment belong inside
that subdirectory, not at the fleet-deployment root, which remains flat.

## What lives in the instance (numbered, local-only)

An instance directory lives under the local deployment workspace and is gitignored at the
workspace level. The `N` suffix is a monotonically increasing integer that distinguishes
concurrent or successive deployments of the same catalog entry. The required instance artifacts
are `MANIFEST.md` (filled from the catalog template), `README.md`, and `README.es.md`. The
MANIFEST records the specific source version the instance was provisioned from, enabling
reproducible reprovisioning from the catalog when the instance is later rebuilt or migrated.

Per-instance configuration — credentials, ports, hostnames, runtime state — lives in the
instance directory or under system paths that the MANIFEST records. None of it reaches git.

## The Tier-3 fleet-node naming convention

Deployment names follow the Nomenclature Matrix prefix taxonomy. Seven canonical prefixes
cover the full range of deployment types:

- `fleet-` — multi-node clusters with a shared coordination layer
- `gateway-` — single-endpoint ingress services with routing logic
- `cluster-` — colocated service groups sharing a compute boundary
- `node-` — single-process service instances
- `media-` — customer-facing content-processing deployments (editorial, proofreading,
  transformation)
- `vault-` — storage and secret-management services
- `route-` — traffic-shaping and proxy services

The prefix conveys the deployment shape without consulting the MANIFEST.
`media-proofreader-woodfinegroup` is readable immediately as a customer-facing
content-processing deployment for the Woodfine group tenant.

## A worked example — the proofreader deployment

`media-proofreader-woodfinegroup` illustrates the pattern concretely. The catalog entry at
`woodfine-fleet-deployment/media-proofreader-woodfinegroup/` contains the operational
definition: README pair, MANIFEST template, and the distillation runbook. The deployment
instance directory records the machine name, the source version in effect, and the paths of
the active service binaries.

The `woodfinegroup` suffix distinguishes this tenant-specific deployment from a future
`media-proofreader-pointsav` entry that would run the same software for the PointSav vendor
account. Tenant disambiguation at the name level — rather than through runtime flags — keeps
the catalog enumerable by inspection.

## How an instance is provisioned from the catalog

Provisioning is operator work. The provisioning engineer reads the `guide-*.md` runbooks in
the catalog entry, creates the instance directory, fills `MANIFEST.md` from the template
with instance-specific values (machine, tenant, source version, state: provisioning), and
copies or generates per-instance configuration files. Operator intervention is required at
defined carve-out points: credentials, billing records, DNS registration, and certificate
issuance. The instance MANIFEST advances through states — `provisioning → active →
maintenance → decommissioned` — as the deployment lifecycle progresses.

## Decommissioning — graceful tear-down by the owning session

Decommissioning follows a two-party model. The session that owns the instance performs
graceful tear-down: stops services, archives runtime state that must be retained, and removes
the instance directory. The command session audits that the tear-down completed and records
the result in the workspace changelog.

A distinction applies between graceful decommission (session-initiated, following the runbook
in sequence) and emergency decommission (command-initiated with explicit operator authority,
bypassing the graceful sequence when the instance is unresponsive or compromised). In both
cases the catalog entry remains intact. A future provisioning run can reconstruct a new
numbered instance from the same catalog entry.

## See also

- [[editorial-pipeline-three-stages]] — the pipeline the `media-proofreader-woodfinegroup`
  instance runs; companion article
- [[language-protocol-substrate]] — the substrate the editorial pipeline implements;
  companion article
