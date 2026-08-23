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

The **sovereign mesh** is the WireGuard overlay that connects every PointSav Private Network (PPN) fleet node, running over a dedicated `wg0` interface. Two distinct, real mechanisms operate on top of it: a zero-broker JSON-payload broadcast (`system-udp`, port 8090) and a signed binary command channel (`app-network-admin`, port 9206) that carries the F8 Terminal's operator-issued commands. Each node communicates directly with its authorised peers; no central message broker sits on the path.

## Hub-and-spoke topology

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

- **Key agreement** — Noise Protocol IK handshake, WireGuard's own default; each node's long-term keypair is generated and stored at first mesh join, manually today on the control-plane node, or via the designed (not yet built) Genesis Protocol for bare-metal edge nodes
- **Encryption and integrity** — ChaCha20-Poly1305 per packet; no plaintext mesh traffic ever leaves a node
- **Peer reachability** — the cloud relay is the only statically-addressed peer; on-premises and leased nodes resolve each other through the relay until a direct routed path becomes available

WireGuard configuration for each node is held in the deployment instance directory (local-only, gitignored). Keypairs are never stored in any repository.

## Command protocol

Authority commands use a 16-byte binary packet format delivered over UDP on port 9206: a 2-byte op code (ping, isolate, pong), a 2-byte target-node selector, a 4-byte timestamp, and 8 reserved bytes. This is a distinct, smaller mesh from the JSON broadcast described above — `app-network-admin` owns it, not `system-udp`.

The command flow from operator to target node is:

```
Operator intent (plain language)
      ↓
F8 Terminal  —  app-network-admin  HTTP :8085  (/translate)
      ↓
Doorman :9080/v1/translate — returns a pending proposal
      ↓
Operator approval  —  app-network-admin HTTP :8085  (/authorize)
      ↓
16-byte binary command
      ↓
UDP unicast  →  wg0  →  WireGuard tunnel
      ↓
Target node  —  UDP port 9206
```

Translating an intent and authorising it are two separate calls — a command is never sent purely on the strength of the Doorman's proposal. See [[diode-standard]] for the broader authority hierarchy this two-step gate sits inside.

## Node roles in the mesh

### os-infrastructure — edge anchor

The bare-metal `os-infrastructure` node is a mesh peer, not a mesh controller. It listens for signed binary commands addressed to it and executes them; it does not initiate commands. The node's Broadcom 14e4:16b4 NIC carries mesh traffic via the `wg0` interface once the Genesis Protocol join sequence completes.

### app-network-admin — control plane

`app-network-admin` owns command authority for the mesh — not `os-network-admin`, which today is a static placeholder page with no service behind it. The F8 Terminal, a plain-language command surface on HTTP port 8085, accepts operator intent, forwards it to the Doorman for translation, and — once the operator explicitly authorises the resulting proposal — broadcasts the signed 16-byte command to one or more mesh peers on port 9206.

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

An operator running an on-premises node, a cloud relay for public reachability, and `app-network-admin` on an administrative workstation is intended to end up with a fleet that is not locked to any single hyperscaler. The [[worm-ledger-design|WORM discipline]] that governs PointSav data persistence applies to each node regardless of which trust profile it runs under.

## Genesis Protocol integration

A bare-metal node is designed to join the mesh through the [[genesis-protocol|Genesis Protocol]] rather than manual WireGuard provisioning: mDNS discovery of a pairing server, a UDP handshake carrying a short code, a CPace password-authenticated key exchange, an administrator-approved claim ceremony, and finally mesh-configuration handoff. The network driver work this sequence depends on hasn't landed yet — every step exists as designed code, not as running behavior. Manual `wg genkey` provisioning is the current runtime path for every node in the mesh today.

## Relationship to the Diode Standard

The [[diode-standard]] describes a one-way command flow — authority commands travel from `app-network-admin` to nodes, never the reverse — as a stated design rule for the platform. Only authority commands use the 16-byte binary format on port 9206; telemetry and sync traffic use WireGuard-encapsulated TCP or UDP on other ports. No single named component checks or enforces this directionality as a conformance-tested invariant; it holds because nothing in the mesh implements a reverse path, not because a dedicated adapter blocks one.

## See also

- [[os-infrastructure-ppn-node]] — the compute-substrate OS itself: current deployment state, Genesis Protocol sequence
- [[os-network-admin]] — the placeholder wiki entry for this node role; the real F8 Terminal service is the `app-network-admin` crate, not yet documented under its own name
- [[diode-standard]] — authority hierarchy and traffic category definitions
- [[machine-based-auth]] — Noise Protocol keypair management and pairing types
- [[ppn-command-protocol]] — the dedicated wire-format deep dive: design constraints, packet layout, dispatch sequence
