---
schema: foundry-doc-v1
title: "OS Network Admin"
slug: os-network-admin
short_description: "os-network-admin is the control plane for a PointSav Private Network — providing WireGuard mesh routing, the node-join ceremony surface, and Diode-standard enforcement, without holding any archive-tier cryptographic authority."
category: systems
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
language: en
paired_with: os-network-admin.es.md
last_edited: 2026-05-30
editor: editorial
---

`os-network-admin` is the control plane for a PointSav Private Network (PPN). It runs on the network administrator's machine — typically bare metal at the operator's primary site or inside an LXC container on the on-premises fleet node — and provides two functions: a routing and tunnel-integrity substrate for the WireGuard mesh, and an operator approval surface for the node-join ceremony.

## Position in the stack

`os-network-admin` carries the `os-` prefix, marking it as a Foundation layer component — below the application layer, providing system-level services with no user-facing logic of its own. It is a Layer 1 companion to `os-console`, not one of the three archive-tier operating systems (`os-totebox`, `os-console`, `os-orchestration`).

| Component | Layer | Role |
|---|---|---|
| `os-totebox` | Archive tier | Sovereign data vault per entity |
| `os-console` | Archive tier | Keyboard-native operator terminal |
| `os-orchestration` | Archive tier | Multi-archive data aggregator |
| `os-network-admin` | **Foundation** | PPN control plane + ceremony surface |

This distinction matters: `os-network-admin` does not store or process business data. It does not hold archive keys, MBA credentials, or F-key cartridges. It is a blind, secure transport layer for the PPN infrastructure — the entity that manages which physical nodes are authorised on the mesh, not what runs on them.

## What it does

### Routing and tunnel integrity

`os-network-admin` establishes and maintains the WireGuard mesh on the `ppn0` interface. It manages peer-map distribution, monitors tunnel liveness, and enforces the Diode rules that constrain which nodes may send commands to which targets. It does not inspect the content of traffic flowing through the tunnels.

### Node-join ceremony

When a new physical node wants to join the PPN mesh, it generates a Crockford base32 short code (eight characters, approximately 40 bits of entropy). The operator enters this code into `os-network-admin`. A CPace PAKE exchange establishes a shared session key over the short-code channel; a Short Authenticated String (SAS) comparison closes the man-in-the-middle gap. Under this key, the joining node submits its WireGuard public key, receives a cluster CA–signed certificate, and the peer-map distributes automatically.

The current minimal implementation polls the `service-ppn-pairing` backend for pending requests and prints them to stdout. Operator approval is issued via curl:

```bash
PAIRING_SERVER=http://10.8.0.9:9202 ./os-network-admin

# Approve a pending join from another terminal:
curl -s -X POST http://10.8.0.9:9202/v1/node-join/approve \
     -H 'Content-Type: application/json' \
     -d '{"code":"XXXX-XXXX"}'
```

A full keyboard-driven TUI — with approve/deny keys (`a`/`d`), QR code display via `system-pairing-codes::qr_unicode`, and expiry countdown — is planned as the production operator surface.

## Relationship to app-network-admin

`app-network-admin` is the F8 Terminal interface that runs on top of `os-network-admin`. It provides two surfaces:

- **HTTP command surface** at port 8085 — accepts plain-language operator intent, routes it through `service-slm` to produce an authorised command, and dispatches it to the mesh
- **UDP mesh broadcast** at port 8090 — sends signed 16-byte binary payloads to PPN peer addresses

The `os-` / `app-` split follows the standard Foundation/Application naming convention: `os-network-admin` is the OS substrate; `app-network-admin` is the operator-facing application that runs on it.

## Relationship to route-network-admin

`route-network-admin` is the deployment instance name for the network admin node in the customer fleet. It is not a separate codebase. A `route-network-admin-1` entry in a fleet manifest means that a physical node at that location is running `os-network-admin` as its primary workload.

## Hardware target

The canonical reference hardware is an iMac 12,1 (Mid-2011) with an Intel Sandy Bridge i5-2400S and a Broadcom 14e4:16b4 NIC. This machine is purpose-suited as a command authority node: it has real hardware VT-x (for running VMs on the same machine if needed), a Broadcom NIC for which `system-substrate-broadcom` provides the silicon detection substrate, and a stable physical location at the operator's site.

For deployments where bare-metal dedication is impractical, `os-network-admin` can run inside an LXC container on the on-premises fleet node, with the WireGuard interface bridged from the host.

## Zero cryptographic authority

`os-network-admin` does not hold F-keys, MBA credentials, or payload capabilities. It cannot read the content of VM-internal state. It cannot approve archive access. Its role is to know which physical nodes are on the mesh and to enforce that membership — nothing more. This architectural constraint is intentional: keeping the network control plane separate from the data plane means a compromise of the routing layer does not yield access to archive contents.

## Diode discipline

Commands flow downward: `os-network-admin` → `os-infrastructure` (hypervisor layer) → VMs. No VM can issue commands back up to `os-network-admin`. No archive can instruct the mesh to add or remove a node. This unidirectional discipline is the same Diode standard that governs the archive tier (`os-console` → `os-orchestration` → `os-totebox`).

## See also

- [[sovereign-mesh]] — the WireGuard overlay and 16-byte binary command protocol
- [[genesis-protocol]] — the autonomous bootstrap sequence that `os-network-admin` executes on a fresh node
- [[machine-based-auth]] — the MBA pairing model that governs archive-tier access
- [[infrastructure-os]] — the Type I hypervisor layer that `os-network-admin` manages
- [[diode-standard]] — the authority hierarchy and traffic rules the control plane enforces
- [[os-family-overview|OS Family Overview]] — the full PointSav OS family
