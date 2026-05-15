---
schema: foundry-doc-v1
title: "os-infrastructure — The Compute Substrate"
slug: infrastructure-os
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: infrastructure-os.es.md
short_description: "os-infrastructure is the compute substrate that hosts PointSav operating systems across on-premises, leased, and cloud hardware. It creates the PointSav Private Network and bootstraps isolated fleets through the Genesis Protocol."
cites: []
---

`os-infrastructure` is the compute substrate that hosts the other PointSav operating systems. One instance runs on one piece of hardware — a bare-metal server in an office, a colocated rack, or a cloud virtual machine. Taken together, a fleet of `os-infrastructure` nodes forms the PointSav Private Network (PPN): an encrypted WireGuard mesh that ties Toteboxes, Consoles, MediaKits, and PrivateGit instances together without exposing any node to the public internet. This article covers the three deployment postures, the Genesis Protocol that bootstraps a fleet, and the structural gap in conventional cloud offerings that the design exploits.

## The three deployment postures

`os-infrastructure` is the same OS in three postures. The operator chooses where their compute lives — and can blend any combination in a single fleet:

| App surface | Hardware | Trust profile |
|---|---|---|
| `app-infrastructure-onprem` | Servers on the operator's own premises | Highest trust; the operator owns and can physically verify the hardware |
| `app-infrastructure-leased` | Colocated bare-metal at an external data centre | Hybrid trust; the operator controls the OS but cannot physically verify every boot |
| `app-infrastructure-cloud` | Hyperscaler VMs (GCP, AWS, Azure) | Lowest trust; used for stateless edge relay, not persistent storage |

The same WireGuard mesh runs across all three. An operator can start with a single cloud relay and add on-premises nodes later without restructuring software.

## The Genesis Protocol

Conventional fleet management requires a control plane to exist before any compute node can join. `os-infrastructure` inverts this. When a node boots and finds no PPN beacon, it does not fail — it declares itself a Private Network of One.

1. **Blind boot.** The node ignores DHCP and DNS conventions. The seL4 kernel generates a Tier-1 fiduciary keypair at first boot.
2. **Scan.** The node looks for an `os-network-admin` beacon on the local mesh.
3. **Genesis fork.** If nothing answers, the node creates its own one-node PPN and seals all external ports except one.
4. **Holding pattern.** A single hardened WebSocket endpoint waits for an administrative claim.
5. **Claim.** When an administrator boots `os-network-admin` and presents the administrative fiduciary key, the node verifies the claim, binds to the fleet, and joins the mesh.

A customer can ship fifty servers to fifty edge locations. Each boots, forms a single-node PPN, and holds. Whenever the administrator is ready, the central `os-network-admin` claims all of them, merging them into one global fleet. The nodes do not need to know in advance how many siblings they will eventually have.

## The PointSav Private Network

Every `os-infrastructure` node is a member of the PPN — the WireGuard overlay that connects all PointSav appliances in a fleet:

- Encrypted data transfer: Totebox archive images move between locations without touching the public internet.
- Linguistic signalling: `os-network-admin` broadcasts 16-byte binary commands across the mesh; every node receives simultaneously, only the addressed node acts.
- Remote administration: `os-console` pairs to `os-totebox` instances through the PPN without requiring a VPN client on the operator's host machine.

## The Hyperscaler Gap

The architecture deliberately exploits a structural gap in conventional cloud offerings:

| Conventional cloud | os-infrastructure |
|---|---|
| Couples compute to proprietary storage; charges egress for data movement | Treats the cloud as a stateless relay; persistent storage stays on the operator's hardware |
| Provides rental access; withholds custodial ownership | The operator can physically unplug and move the substrate |
| Requires network engineering before compute can be added | Nodes self-bootstrap via the Genesis Protocol |
| Single-vendor control plane as a single point of failure | Every `os-infrastructure` node can genesis a fleet independently |

An operator running `os-infrastructure` on a single server in their office, a cloud relay node for public connectivity, and `os-network-admin` on an administrative workstation has built a fleet that is not locked to any hyperscaler and is inaccessible to external attackers without a valid fiduciary key.

## See also

- [[os-network-admin]] — the control plane that commands `os-infrastructure` fleets
- [[os-family-overview]] — the full eight-OS family and how each member fits
- [[totebox-os]] — the archive OS hosted on `os-infrastructure` nodes
- [[diode-standard]] — the protocol that governs command flow between nodes
- [[machine-based-auth]] — how fiduciary keypairs and pairings secure fleet membership
- [[deployment-patterns]] — the six canonical fleet configurations
