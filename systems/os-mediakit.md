---
schema: foundry-doc-v1
content_type: topic
title: "OS mediakit"
slug: os-mediakit
short_description: "The public-web tier of the PointSav OS family — os-mediakit owns TLS, systemd lifecycle, and gateway-mediated data access; app-mediakit-knowledge/marketing/distribution own domain logic. Ubuntu 24.04 today; the planned end state is one seL4 VM per deployment instance, not a single combined appliance."
category: systems
index_group: publishing-and-media
last_edited: 2026-08-06
editor: pointsav-engineering
status: stable
bcsc_class: no-disclosure-implication
---

**os-mediakit** is the guest operating system image for the `vm-mediakit` VM tier in
the PointSav Private Network hypervisor layer. It isolates the MediaKit service surface
— knowledge wikis, marketing sites, and compliance/distribution feeds — from the source
vault and orchestration tiers.

## OS / app boundary

`os-mediakit` (the operating system) and `app-mediakit-*` (the applications it hosts)
have a fixed division of responsibility, ratified as part of the OS family's tier
definitions.

`os-mediakit` provides: TLS termination (nginx and certbot), systemd unit lifecycle,
the per-tenant filesystem layout, log rotation with forwarding into the WORM ledger,
MBA pairing to the fleet gateway, Doorman client TLS bootstrap, rate limiting, and
static asset serving.

`app-mediakit-*` provides: domain logic — page rendering, search, payment
verification, taxonomy queries, the editorial UI, wiki wikilink resolution, and
license issuance. Each `app-mediakit-*` binary is a tenant of the OS, not part of it.

## Deployments and data flow

Every `app-mediakit-*` instance reaches Totebox data through the fleet gateway only —
`media-* → outbound MBA → gateway-orchestration-command-1 → Doorman audit →
cluster-totebox-*`. **No `app-mediakit-*` process reads Totebox storage directly**; the
gateway is the only crossing point, and every read is recorded to the audit ledger on
its way through.

| Instance | Binary | Surface | Status |
|---|---|---|---|
| `media-knowledge-documentation-1` | app-mediakit-knowledge | documentation.pointsav.com | Live |
| `media-knowledge-projects-1` | app-mediakit-knowledge | projects.woodfinegroup.com | Live |
| `media-marketing-landing-1` | app-mediakit-marketing | home.woodfinegroup.com | Live |
| `media-marketing-landing-2` | app-mediakit-marketing | home.pointsav.com | Live |
| `media-intranet-1` | nginx (no app binary) | VPN-only internal preview of the above | Live, WireGuard-gated |
| `media-knowledge-corporate-1` | app-mediakit-knowledge | corporate.woodfinegroup.com | Not yet deployed |
| `media-distribution-*` | app-mediakit-distribution | Compliance/press-release feed | Not yet deployed |

Two things worth stating plainly rather than smoothing over. First, the fleet-gateway
MBA pairing this data-flow model depends on is not yet wired for any `media-*`
instance today — each one currently reaches its content locally rather than through
the gateway, a known, tracked gap. Second, `software.pointsav.com` — sometimes
associated with `app-mediakit-distribution` in early planning — is in practice served
by the separate `app-privategit-marketplace`/`app-privategit-source` binaries; no
`app-mediakit-distribution` instance is deployed there today.

## Stack position

The four-layer Totebox stack places os-mediakit in the **Hypervisor layer**:

```
Operator
  ↓
PPN (WireGuard mesh, os-network-admin control plane)
  ↓
Hypervisor layer  ←— os-mediakit guest OS runs here
  ↓
Totebox Orchestration (app-mediakit-*, service-fs, system-core)
```

os-mediakit is one guest among three in the three-VM layout:

| VM | Guest OS | Tier |
|---|---|---|
| vm-workspace | host OS (Linux) | os-privategit (permanent host) |
| vm-intelligence | os-intelligence (planned) | os-totebox + inference |
| vm-mediakit | **os-mediakit** | os-mediakit |

The host — foundry-workspace GCP VM — runs QEMU to manage all guests. The hypervisor
itself is `os-infrastructure` (the Genesis Protocol boot layer).

---

## Phase 1: Ubuntu 24.04 interim (present)

The first deployment of vm-mediakit uses an **Ubuntu 24.04 server cloud x86_64 QCOW2** as
the guest OS. This is the production interim while the per-instance seL4 VMs are developed.

Ubuntu 24.04 is required — not Debian 12 — because all service binaries compiled on the
GCP host (Ubuntu 24.04, glibc 2.39) link against `GLIBC_2.39` symbols. Debian 12 provides
only glibc 2.36 and would fail to execute the binaries at load time.

What is running today:
- Ubuntu 24.04 booted via `provision-vm-mediakit.sh` under QEMU/TCG (GCP workspace has no
  hardware KVM; TCG is adequate for Phase 1 testing)
- 6 GiB RAM (`-m 6144`), 20 GB QCOW2 disk
- User-mode NAT networking: host port-forwards `1xxxx → :xxxx` for each service
- `virtio-balloon` device: dynamic RAM adjustment without guest reboot
- cloud-init first boot: hostname `vm-mediakit`, user `foundry`, systemd-native
- nginx/1.24.0 and build-essential installed post-boot

Services running inside the Ubuntu 24.04 guest (Phase 1 state, 2026-05-29):

| Service | Port | Purpose | Phase 1 status |
|---|---|---|---|
| local-proofreader | 9092 | Proofreader service | ✓ active |
| local-knowledge-documentation | 9090 | Documentation wiki | ✓ active |
| local-knowledge-corporate | 9095 | Corporate wiki | ✓ active |
| local-knowledge-projects | 9093 | Projects wiki | ✓ active |
| local-marketing-pointsav | 9101 | PointSav marketing site | ✓ active |
| local-marketing | 9102 | Woodfine marketing site | ✓ active |
| service-fs | 9100 | WORM ledger — data ingest backbone | pending (project-data build) |
| local-bim-orchestration | 9096 | BIM gateway | pending (depends on service-fs) |
| system-core | — | Capability Ledger substrate | pending (project-system install) |
| system-ledger | — | Ledger state-machine | pending (project-system install) |

The systemd host unit `infrastructure/local-vm-mediakit/vm-mediakit.service` manages the
QEMU process and handles graceful shutdown via the QEMU monitor socket.

---

## Phase 3: one seL4 VM per deployment instance (planned)

The ratified moonshot topology for the OS family does not package `os-mediakit` as one
combined seL4 appliance the way `os-orchestration` consolidated Command and SLM into a
single guest. Instead, each `app-mediakit-*` **deployment instance** — not each
service type — gets its own dedicated seL4/Microkit VM, using the same
Microkit-plus-`vendor-libvmm`-Linux-guest pattern already proven for `os-totebox`.

| Planned VM | Hosts |
|---|---|
| `mediakit-knowledge-vm-1` | `media-knowledge-documentation-1` (documentation.pointsav.com) |
| `mediakit-knowledge-vm-2` | `media-knowledge-projects-1` (projects.woodfinegroup.com) |
| `mediakit-knowledge-vm-3` | `media-knowledge-corporate-1` (corporate.woodfinegroup.com, not yet deployed) |
| `mediakit-marketing-vm` | the marketing landing instances |
| `mediakit-dist-vm` | the distribution/compliance-feed instance, once built |

The rationale mirrors `os-privategit`'s three separate instances (source vault,
software distribution, design assets): different public surfaces carry different
attack profiles, and a compromise of one wiki instance should not put a sibling
instance's process space at risk. This is a planned milestone, not yet started — no
`os-mediakit` VM, combined or per-instance, runs under seL4 today.

---

## What changes vs Phase 1, what stays the same

| Property | Ubuntu 24.04 (Phase 1, today) | seL4 per-instance VMs (Phase 3, planned) |
|---|---|---|
| Guest OS | Ubuntu 24.04 Linux 6.x (glibc 2.39), one guest for all co-tenant instances | seL4 microkernel, one guest per deployment instance |
| Host | QEMU/TCG (x86_64) | QEMU/KVM or bare metal AArch64 |
| Service binaries | Same (cross-compiled) | Same, recompiled for the target seL4 guest |
| Isolation boundary | Process/filesystem separation within one shared guest | A full VM boundary per instance |
| Port numbers | Same (9090, 9093, 9095, ...) | Same, reachable over the PPN mesh |
| virtio-balloon | Present | Present (hypervisor layer unchanged) |
| Key custody | OS file permissions | Per-VM key material, no shared guest to compromise |

---

## Relationship to os-infrastructure and Genesis Protocol

`os-infrastructure` is the hypervisor boot layer — it runs Genesis Protocol on the physical
host to establish the PPN node's WireGuard identity and claim ceremony. os-mediakit is a
*guest* that runs above os-infrastructure. They are different layers and different binaries.

The Genesis Protocol first-boot sequence applies to the **host node**
(os-infrastructure), not to the guest (os-mediakit). A new vm-mediakit guest joins the mesh
via the MBA pairing ceremony after the host node is already a PPN member.

---

## See also

- [[ppn-hypervisor-resource-pool]] — how virtio-balloon manages RAM for vm-mediakit
- [[totebox-archive]] — what the Totebox Archive tier does above the guest OS
- [[os-network-admin]] — the PPN control plane; vm-mediakit joins the mesh through it
- [[os-family-overview|OS Family Overview]] — the full PointSav OS family
