---
schema: foundry-doc-v1
title: "Sovereign mesh"
slug: sovereign-mesh
short_description: "The sovereign mesh is the application-level WireGuard overlay connecting every PPN fleet node, carrying signed binary commands without a centralised message broker."
category: infrastructure
index_group: network-and-telemetry
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: en
paired_with: sovereign-mesh.es.md
last_edited: 2026-08-01
editor: pointsav-engineering
---

The **sovereign mesh** is the application-level network overlay that connects every PointSav Private Network (PPN) fleet node. It runs over WireGuard cryptographic tunnels on a dedicated `wg0` interface and carries signed binary commands without relying on a centralised message broker. Each node communicates directly with its authorised peers; the mesh layer enforces the same authority hierarchy as the [[diode-standard|Diode Standard]] as a structural property, not a configuration option.

## Hub-and-spoke topology

**Correction (2026-08-02, verified against canonical `origin/main`):** several specific claims below don't match the real implementation. (1) Crate name — real crate is `system-udp`, not `service-udp` (confirmed absent on canonical). (2) `service-pointsav-link` — confirmed nonexistent anywhere in the codebase, corroborating this repo's own 2026-07-18 `diode-standard.md` finding; there is no separate adapter enforcing one-way flow. (3) Packet format — the real `system-udp/src/main.rs` sends a plain `serde_json` `MeshPayload{sender_id, intent, target, timestamp}` over UDP 8090, not a 16-byte binary format with an intent token/nonce/truncated signature; its only guard is an IP-prefix check. (4) The UEFI Secure Variable / port 9443 genesis claim doesn't match real code — `system-network-interface`'s genesis handshake is a 32-byte `GNES`-magic frame with no UEFI or port 9443 involvement, and `os-infrastructure/CLAUDE.md` explicitly states "No UEFI officially... do not implement UEFI until explicitly approved." Port 8090 and the `10.8.0.0/24` addressing are independently confirmed accurate. **Flagged, not resolved.**

The mesh uses a hub-and-spoke arrangement. The cloud relay node sits at the centre and relays packets between spoke nodes that may not have a direct path to each other. `os-infrastructure` runs identically in all three roles — the operator chooses where their compute lives, and the same WireGuard mesh spans any combination.

| Role | Node | Planned address | Crate | Trust profile |
|---|---|---|---|---|
| Hub | Cloud relay (GCP) | `10.8.0.1` | `app-infrastructure-cloud` | Lowest — the cloud provider retains physical access to the hardware; intended for stateless relay, not persistent storage |
| Spoke | On-premises node | `10.8.0.2` | `app-infrastructure-onprem` | Highest — the operator owns and can physically verify the hardware |
| Spoke | Leased node | `10.8.0.3` | `app-infrastructure-leased` | Hybrid — the operator controls the OS but cannot physically verify every boot |

WireGuard's encryption secures traffic between nodes, but it does not by itself address the leased and cloud profiles' trust gap: whoever owns the physical hardware can still access it directly. Closing that gap is intended to be seL4 microkernel isolation at the hardware layer — planned, not yet running on bare metal today.

The `10.8.0.0/24` subnet is the intended PPN address range. All mesh traffic is encapsulated inside WireGuard before leaving a node; the underlying transport — public internet, private LAN, or GCP internal network — is irrelevant to the mesh layer. A `10.42.0.0/16` addressing scheme is the ratified future target, with migration ("Part A") in progress; no deployed node uses it yet.

## WireGuard overlay

Each node brings up a `wg0` WireGuard interface as part of its boot sequence. WireGuard provides:

- **Key agreement** — Noise Protocol IK handshake; each node's long-term keypair is generated and stored at first mesh join by `os-network-admin` for the control-plane node, or via the Genesis Protocol for bare-metal edge nodes
- **Encryption and integrity** — ChaCha20-Poly1305 per packet; no plaintext mesh traffic ever leaves a node
- **Peer reachability** — the cloud relay is the only statically-addressed peer; on-premises and leased nodes resolve each other through the relay until a direct routed path becomes available

WireGuard configuration for each node is held in the deployment instance directory (local-only, gitignored). Keypairs are never stored in any repository.

## Command protocol

All mesh commands use a 16-byte binary packet format delivered over UDP on port 8090. The compact size is deliberate: the packet carries an intent token, a target selector, a nonce, and a truncated authority signature — sufficient to identify the command, verify its provenance, and detect replay attacks without requiring a full TLS session per command.

The command flow from operator to target node is:

```
Operator intent (plain language)
      ↓
F8 Terminal  —  os-network-admin  HTTP :8085
      ↓
service-slm semantic router
      ↓
16-byte binary command (authorised and signed)
      ↓
service-udp broadcast  →  wg0  →  WireGuard tunnel
      ↓
Target node  —  UDP port 8090
```

Commands flow in one direction only — from `os-network-admin` outward to the mesh — a constraint enforced by `service-pointsav-link` at the application layer. See [[diode-standard]] for the full authority hierarchy.

## Node roles in the mesh

### os-infrastructure — edge anchor

The bare-metal `os-infrastructure` node is a mesh peer, not a mesh controller. It listens on port 8090 for signed binary commands addressed to it and executes them; it does not initiate commands. The node's Broadcom 14e4:16b4 NIC carries mesh traffic via the `wg0` interface once the Genesis Protocol join sequence completes.

### os-network-admin — control plane

`os-network-admin` owns command authority for the mesh. The F8 Terminal — a plain-language command surface on HTTP port 8085 — accepts operator intent and routes it through `service-slm` to produce a signed 16-byte binary command. The command is then broadcast over `service-udp` on port 8090 to one or more mesh peers. `os-network-admin` also hosts the pairing registry and manages new-node admission via the [[machine-based-auth|machine-based auth]] handshake.

### Cloud relay — hub

The GCP cloud relay node relays WireGuard-encapsulated packets between spoke nodes. It does not interpret mesh commands; it is a transport layer only. The relay's fixed public IP and static WireGuard configuration make it the anchor point that allows on-premises and leased nodes to find each other without DNS or DHCP dependency.

## The gap this design targets

The hub-and-spoke topology above is designed to exploit a structural gap in conventional cloud offerings, not merely to work around it:

| Conventional cloud | This design's intent |
|---|---|
| Couples compute to proprietary storage; charges egress for data movement | Treat the cloud relay as a stateless pass-through; persistent storage stays on the operator's own hardware |
| Provides rental access; withholds custodial ownership of the underlying machine | The operator can physically unplug and relocate an on-premises or leased node |
| Requires network engineering before compute can be added | A node is intended to be able to join the mesh with minimal manual WireGuard provisioning, once the join sequence described below is fully built |
| A single vendor's control plane is a single point of failure | Each node is designed so that a fleet does not depend on any one hyperscaler remaining available |

An operator running an on-premises node, a cloud relay for public reachability, and `os-network-admin` on an administrative workstation is intended to end up with a fleet that is not locked to any single hyperscaler. The [[worm-ledger-design|WORM discipline]] that governs PointSav data persistence applies to each node regardless of which trust profile it runs under.

## Genesis Protocol integration

A bare-metal node joins the mesh through the [[genesis-protocol|Genesis Protocol]] rather than manual WireGuard provisioning. At first boot:

1. seL4 generates an entropy-seeded keypair from hardware sources
2. The node enters blind-boot mode — ignoring all DHCP and DNS — and scans for the `os-network-admin` beacon on port 8090
3. If the beacon is found, `os-network-admin` guides the node through the mesh-join handshake: WireGuard peer registration, IP assignment, and keypair binding to the pairing registry
4. If no beacon is found within the scan window, the node self-geneses: it writes its keypair to UEFI Secure Variable storage and enters a holding pattern on port 9443, awaiting an admin claim

This mechanism ensures that no node ever joins the mesh without a verified authority handshake. Manual `wg genkey` workflows apply during initial fleet provisioning only; they are not the runtime join path for production nodes.

## Relationship to the Diode Standard

The [[diode-standard]] defines three mesh traffic categories: authority commands, telemetry, and inter-node sync. All three flow through the sovereign mesh, but only authority commands use the 16-byte binary format on port 8090. Telemetry and sync traffic use WireGuard-encapsulated TCP or UDP on other ports.

The Diode Standard's unidirectionality constraint — authority commands flow from `os-network-admin` to nodes, never the reverse — is implemented at the mesh layer by `service-pointsav-link`, a hot-pluggable adapter that enforces the flow direction without requiring WireGuard policy changes.

## See also

- [[os-infrastructure-ppn-node]] — the compute-substrate OS itself: current deployment state, Genesis Protocol sequence
- [[os-network-admin]] — F8 Terminal, service-slm integration, mesh policy ownership
- [[diode-standard]] — authority hierarchy and traffic category definitions
- [[machine-based-auth]] — Noise Protocol keypair management and pairing types
- [[ppn-command-protocol]] — the dedicated wire-format deep dive: design constraints, packet layout, dispatch sequence
