---
schema: foundry-doc-v1
title: "VM-* Architecture and OS Family"
slug: vm-architecture
short_description: "The PointSav platform organises its runtime deployments under five named VM types — VM-Totebox, VM-MediaKit, VM-Orchestration, VM-PrivateGit, and VM-Infrastructure — each corresponding exactly to one os-* source binary."
category: systems
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
language: en
paired_with: vm-architecture.es.md
last_edited: 2026-05-30
editor: editorial
---

The PointSav platform organises its runtime deployments under a set of named VM types — VM-Totebox, VM-MediaKit, VM-Orchestration, VM-PrivateGit, and VM-Infrastructure. Each VM type corresponds exactly to one `os-*` source binary. The runtime name and the source name are two identities for the same thing: what compiles as `os-totebox` runs as VM-Totebox.

This correspondence is not incidental. The platform is designed to be deployed the same way by a builder running a development environment as by a customer running a production system. The five VM types map directly to the five ways customers and community members engage with the platform.

## VM types and their purposes

### VM-Totebox

**Source binary:** `os-totebox`
**Purpose:** Per-entity sovereign data vault. The primary compute unit of the platform.

A VM-Totebox instance holds all of the structured data belonging to one entity — corporate records, personnel, real property, email, documents, and the ledgers derived from them. Data enters through Ring 1 ingest services and is processed by Ring 2 knowledge services. The vault is a WORM-disciplined archive: data may be appended and superseded but not silently deleted.

Each VM-Totebox is independently deployable — on a bare-metal server, a leased host, or a cloud VM. The disk image constitutes the archive. Migrating a Totebox means moving the image.

Services: `service-fs` (WORM block storage), `service-people`, `service-email`, `service-extraction`, `service-content`, and optional Ring 3 intelligence via `service-slm`.

### VM-MediaKit

**Source binary:** `os-mediakit`
**Purpose:** Public-facing web appliance. Runs independently of a Totebox.

VM-MediaKit hosts the websites and knowledge portals that a Reporting Issuer or small business presents to the public. It runs wiki-based knowledge portals, static marketing sites, and a newsroom. Each hosted application is a stateless service — it reads from a content directory but holds no per-entity ledger state.

The proofreader service co-locates in VM-MediaKit because its callers are MediaKit-resident. Moving it to VM-Totebox would route every editorial request across the PPN boundary — the placement rule enforces that co-location pressure dissolves at the network boundary.

Services: `app-mediakit-knowledge` (documentation, corporate, and projects wikis), `app-mediakit-marketing`, `service-proofreader`.

### VM-Orchestration

**Source binary:** `os-orchestration`
**Purpose:** Stateless multi-archive aggregator. Commercial paid tier.

VM-Orchestration queries multiple VM-Totebox instances and presents fleet-wide or portfolio-wide views. It holds no data of its own — it aggregates via the PointSav Protocol (PSP), which is a capability-based query protocol. A VM-Orchestration instance serves the BIM coordination terminal, the GIS fleet map, and the SLM broker chassis.

Services: `app-orchestration-bim`, `app-orchestration-gis`, `app-orchestration-slm` (:9180).

### VM-PrivateGit

**Source binary:** `os-privategit`
**Purpose:** Sovereign source control and design system hosting.

VM-PrivateGit runs Gitea as a bidirectional mirror of the canonical GitHub repositories, and optionally a design-system preview server. It provides source control independence from third-party hosting for intellectual property and brand assets. The Foundry workspace itself (`vault-privategit-source-1`) is the first deployment of this type, currently running on the GCP host directly.

Services: `app-privategit-source-control`, `app-privategit-design-system`.

### VM-Infrastructure

**Source binary:** `os-infrastructure`
**Purpose:** The host fleet itself — WireGuard PPN fabric, hypervisor, and VM placement.

VM-Infrastructure is not a VM in the conventional sense. It is the `os-infrastructure` binary running on bare metal, providing the hypervisor layer that hosts all other VM types. Three nodes form the minimum production fleet:

- **Laptop A (genesis-seed):** First node. Runs `provision-vm-infrastructure-onprem.sh --genesis`, which self-configures WireGuard and opens the pairing ceremony server. Hosts VM-Totebox-1.
- **Laptop B (relay):** Second node. Joins the mesh via `--join <short-code>` (CPace PAKE + SAS confirmation). Hosts the WireGuard hub.
- **GCP cloud node:** Third node. Joins via `provision-vm-infrastructure-cloud.sh --join <short-code>`. Hosts VM-MediaKit, VM-Orchestration, VM-PrivateGit.

VM-Infrastructure is a trust-meshed host fleet, not a resource-pooling cluster scheduler. Each node is independently provisioned. Placement decisions — which VM runs on which node — are operator policy, not automated scheduling. The PPN WireGuard mesh provides the name-to-endpoint binding.

## Placement principle

A service belongs in the VM whose `os-*` namespace owns its data lifecycle and trust boundary — not the VM where its binary first ran.

Derivations from this rule:
- `service-fs` (WORM ledger) belongs in VM-Totebox. It is the Totebox storage substrate.
- `app-orchestration-bim` belongs in VM-Orchestration. Its name declares its class.
- `service-proofreader` belongs in VM-MediaKit. Its callers are MediaKit-resident.
- WireGuard and the pairing ceremony belong in VM-Infrastructure. These are fabric concerns.

If a service requires loopback co-location with a service in a different VM, that is a design signal. The PPN boundary is where services of different types communicate.

## Customer deployment paths

The VM types correspond directly to the ways customers and community members engage with the platform.

**PointSav Private Network users** deploy VM-Infrastructure on their own hardware — at minimum one on-prem node (Laptop A) and the GCP cloud relay. The Genesis Protocol bootstraps the mesh from a single node. No external certificate authority is required.

**Totebox Orchestration users** deploy VM-Totebox (data vault) and VM-Orchestration (fleet view). A single VM-Totebox instance is sufficient for a small business. Larger organisations add VM-Orchestration to aggregate across multiple archives.

**Independent systems users** deploy VM-MediaKit (websites and knowledge portals) or VM-PrivateGit (source control) without a Totebox dependency. These are standalone appliances — they do not require a WireGuard mesh to function, though they may optionally join one.

## Unikernel roadmap

Phase 1 for all VM types uses Ubuntu 24.04 under QEMU (KVM-accelerated where available, TCG fallback for hardware without virtualisation extensions). This is the operational baseline.

Phase 2 introduces lighter-weight hosting per VM type: FreeBSD jails for MediaKit's per-workload isolation, Alpine Linux with musl-linked static binaries for Totebox, and gVisor sandboxing for Orchestration aggregators.

Phase 3 is the intended unikernel target. VM-Totebox and VM-MediaKit are intended to run as seL4 Microkit protection domains on AArch64 hardware (gated on hardware acquisition). VM-Orchestration aggregator processes are intended to target NanoVMs/OPS; SLM inference and GPU-accelerated workloads are intended to remain on a full Linux host. The host fleet itself (VM-Infrastructure) is intended to run the `os-infrastructure` binary on NetBSD/NVMM (x86-64 compat bottom, Phase 2) or seL4+Microkit (AArch64 native bottom, Phase 3).

Microkit 2.2.0 includes an `x86_64_generic_vtx` target, but x86-64 Microkit is capacity-capped to one vCPU per guest and requires Intel VT-x. AArch64 is the intended production Phase 3 path. Phase 2 on x86-64 uses NetBSD/NVMM — NVMM (NetBSD Virtual Machine Monitor) is NetBSD's native bare-metal hypervisor, mainline since NetBSD 9.0, using QEMU with the `-accel nvmm` flag. Both compat and native bottoms share the same capability ledger (`system-core`).

## Resource pooling

The three-node WireGuard mesh (one cloud node and up to two on-premises nodes) forms a unified VM resource pool. This pooling is a free-tier PPN primitive — operators do not pay per node joined to the pool.

Two services implement the pool. `service-vm-host` runs on each infrastructure node: it polls local CPU and RAM utilisation every ten seconds and sends a heartbeat to the fleet controller. `service-vm-fleet` runs on the cloud node and receives those heartbeats, evicting any node that goes silent for more than thirty seconds. When an operator requests a new VM, the fleet controller applies advisory placement — selecting the node with the most available RAM above a safety margin — and dispatches the creation request.

Live VM migration is permanently excluded. WireGuard bandwidth over typical internet links would make migrating a live VM impractical; VMs are placed once and remain on their assigned node. This is an architectural invariant, not a configuration option.

Creating a VM is an operator action and requires explicit confirmation in the `app-network-admin` F9 panel. The fleet controller's node selection is advisory infrastructure and does not require confirmation. VM-Totebox instances must always be assigned to a specific node, because WORM archive data is not transferable over the network.

## See also

- [[infrastructure-os]] — the Type I hypervisor OS that hosts all other VM types
- [[os-network-admin]] — Foundation OS layer; control plane for the PPN mesh
- [[totebox-archive]] — the sovereign WORM data vault running inside VM-Totebox
- [[ppn-architecture-overview]] — four-layer PPN overview: operator, PPN, hypervisor, orchestration
- [[ppn-distributed-vm-fabric]] — planned cross-node extension: virtio-mem lending, capability ledger, cross-node scheduler
- [[genesis-protocol]] — the node-join ceremony that bootstraps the mesh from a single node
