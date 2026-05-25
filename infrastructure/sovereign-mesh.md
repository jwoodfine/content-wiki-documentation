---
schema: foundry-doc-v1
type: topic
slug: sovereign-mesh
short_description: "The sovereign mesh is the application-level WireGuard overlay that connects every PointSav Private Network fleet node, carrying signed binary commands without relying on a centralized message broker."
title: "Sovereign mesh"
category: infrastructure
language: en
paired_with: sovereign-mesh.es.md
status: active
last_edited: 2026-05-25
editor: pointsav-engineering
---

The sovereign mesh is the application-level network overlay that connects every PointSav Private Network (PPN) fleet node. It runs over WireGuard cryptographic tunnels on a dedicated `ppn0` interface and carries signed binary commands without relying on a centralized message broker. Each node communicates directly with its authorized peers; the mesh layer enforces the same authority hierarchy as the [[diode-standard|Diode Standard]] as a structural property, not a configuration option.

## Hub-and-spoke topology

The mesh uses a hub-and-spoke arrangement. The cloud relay node sits at the center and relays packets between spoke nodes that may not have a direct path to each other.

| Role | Node | Planned address | Crate |
|---|---|---|---|
| Hub | Cloud relay (GCP) | `10.50.0.1` | `app-infrastructure-cloud` |
| Spoke | On-premises node | `10.50.0.2` | `app-infrastructure-onprem` |
| Spoke | Leased node | `10.50.0.3` | `app-infrastructure-leased` |

The `10.50.0.0/24` subnet is the intended PPN address range. All mesh traffic is encapsulated inside WireGuard before leaving a node; the underlying transport — public internet, private LAN, or GCP internal network — is irrelevant to the mesh layer.

## WireGuard overlay

Each node brings up a `ppn0` WireGuard interface as part of its boot sequence. WireGuard provides key agreement via Noise Protocol IK handshake, with each node's long-term keypair generated and stored at first mesh join; encryption and integrity via ChaCha20-Poly1305 per packet; and peer reachability through the cloud relay as the only statically-addressed peer.

WireGuard configuration for each node is held in the local deployments directory (local-only, not tracked in any repository). Keypairs are never stored in any repository.

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
16-byte binary command (authorized and signed)
      ↓
service-udp broadcast  →  ppn0  →  WireGuard tunnel
      ↓
Target node  —  UDP port 8090
```

Commands flow in one direction only — from `os-network-admin` outward to the mesh — a constraint enforced by `service-pointsav-link` at the application layer.

## Node roles in the mesh

`os-infrastructure` — the bare-metal node — is a mesh peer, not a mesh controller. It listens on port 8090 for signed binary commands addressed to it and executes them; it does not initiate commands. The node joins the mesh through the [[genesis-protocol|Genesis Protocol]] join sequence.

`os-network-admin` owns command authority for the mesh. The F8 Terminal accepts operator intent in natural language and routes it through `service-slm` to produce a signed 16-byte binary command, which is then broadcast over `service-udp` on port 8090 to one or more mesh peers.

The GCP cloud relay relays WireGuard-encapsulated packets between spoke nodes. It does not interpret mesh commands; it is a transport layer only.

## Genesis Protocol integration

A bare-metal node joins the mesh through the [[genesis-protocol|Genesis Protocol]] rather than manual WireGuard provisioning. At first boot, seL4 generates an entropy-seeded keypair; the node enters blind-boot mode and scans for the `os-network-admin` beacon on port 8090; if found, `os-network-admin` guides the node through the mesh-join handshake; if not found, the node self-geneses and awaits an admin claim.

This mechanism ensures that no node ever joins the mesh without a verified authority handshake.

## Relationship to the Diode Standard

The [[diode-standard|Diode Standard]] defines three mesh traffic categories: authority commands, telemetry, and inter-node sync. All three flow through the sovereign mesh, but only authority commands use the 16-byte binary format on port 8090. Telemetry and sync traffic use WireGuard-encapsulated TCP or UDP on other ports.

The Diode Standard's unidirectionality constraint is implemented at the mesh layer by `service-pointsav-link`, a hot-pluggable adapter that enforces the flow direction without requiring WireGuard policy changes.

## See also

- [[genesis-protocol]] — how bare-metal nodes join the mesh at first boot
- [[ppn-command-protocol]] — the 16-byte binary wire format for fleet commands
- [[service-pointsav-link]] — the adapter that enforces command flow direction
- [[diode-standard]] — authority hierarchy and traffic category definitions
- [[machine-based-auth]] — Noise Protocol keypair management and pairing types
- [[sovereign-telemetry]] — the zero-state telemetry architecture running over the mesh
