---
schema: foundry-doc-v1
title: "PointSav Private Network"
slug: pointsav-private-network
short_description: "The PointSav Private Network is the private WireGuard mesh that connects Woodfine's fleet nodes, providing encrypted transport without granting application-layer access to the services running on those nodes."
category: infrastructure
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: pointsav-private-network.es.md
---

The PointSav Private Network (PPN) is the private WireGuard mesh that connects Woodfine's fleet nodes. It is an infrastructure layer: it provisions the virtual machines that run `os-*` services, routes encrypted traffic between them, and provides a static topology that Totebox Orchestration runs on top of.

The PPN is not an authorization system. It grants no access to application data. Being on the PPN means a machine can reach the network; it does not mean a machine can open any door. Authorization is handled at the application layer by machine-based authorization, which operates independently of and above the PPN.

## The hub-and-spoke topology

The PPN uses a hub-and-spoke topology with three node roles:

| Node | Role | WireGuard position |
|---|---|---|
| `fleet-infrastructure-cloud` | GCP compute instance; static public IP | Hub — accepts all spoke connections |
| `fleet-infrastructure-onprem` | iMac 12.1 (on-premises) | Spoke — dials out to cloud hub |
| `fleet-infrastructure-leased` | Laptop endpoints | Spoke — dials out to cloud hub |

All traffic initiates from the spokes. The hub never dials in to nodes. The public internet cannot initiate connections to spoke nodes. The cloud relay provides a stable, publicly-addressable endpoint for WireGuard peer discovery and relays encrypted WireGuard packets between spokes. It does not decrypt application-layer traffic.

## NODE-IMAC-12 and master key custody

The on-premises spoke — the iMac 12.1 running Linux Mint — holds the master cryptographic keys for the entire network. This is a deliberate physical custody decision: the machine that holds the WireGuard master keys sits under physical custody of Woodfine Management Corp.

If the cloud relay is destroyed, the on-premises node retains the master keys and can immediately provision a new relay by dialing into a new cloud IP. The WireGuard key material that defines the network topology is in physical possession of the customer, not the vendor.

The on-premises node is also the primary deployment target for `os-console`. It is the machine from which the operator uses the Totebox Archive interface.

## WireGuard cryptographic fabric

WireGuard uses Curve25519 elliptic-curve key pairs: one private and public pair per node. The private key never leaves its node. Public keys are distributed to peers and recorded in WireGuard configuration on the hub.

Private keys are stored on-device only and never transmitted. `route-network-admin` holds the authoritative peer key registry and subnet assignments. The intended PPN address range is `10.50.0.0/24`.

The PPN uses a zero-broker UDP broadcast approach for fleet health commands: commands are broadcast as UDP signals across the mesh to all active nodes simultaneously, without routing through any central broker.

## Mesh Fusion: joining the network

Binding a new physical node to the PPN is called Mesh Fusion:

1. Install the host operating system on the target hardware.
2. Generate a WireGuard Curve25519 key pair on the new node.
3. Register the public key with `route-network-admin`.
4. Configure the WireGuard interface on the new node with the hub endpoint and subnet IP.
5. Establish the encrypted tunnel: the node dials the cloud relay.
6. Verify connectivity.

Mesh Fusion is infrastructure-layer provisioning only. It does not establish any `os-*` application pairings. After Mesh Fusion, the node is on the network; application pairing ceremonies are performed separately to grant application-layer access.

## The F8 Terminal: mesh management interface

The PPN is managed through `os-network-admin`, exposed as the F8 Terminal — a keyboard-driven interface at the `route-network-admin` node. Operators submit network management commands in natural English. The interface uses a two-step execution protocol to ensure human-in-the-loop oversight of all network changes: the operator types a command in natural English; the interface halts and displays the machine-translated action payload proposed by the language model; the operator visually confirms the translation and explicitly clicks EXECUTE to broadcast the command. No network action executes without the operator's visual confirmation.

## Deliberate isolation from the application layer

The most important architectural property of the PPN: it is deliberately isolated from the `os-*` application layer.

The PPN was designed to carry packets and provision virtual machines. It was not designed to grant access to what runs inside those VMs. This means a machine on the PPN cannot read `os-totebox` data without an application pairing. PointSav Digital Systems, as vendor and PPN operator, has no application-layer access to customer Totebox Archives through the network infrastructure. Compromising the network relay does not compromise customer data. The vendor owns the pipes. The customer owns the doors.

## PPN and machine-based authorization: two independent security layers

The PPN and machine-based authorization are designed to be independent. Neither depends on the other for its security guarantees.

The PPN (WireGuard) protects network topology and encrypts transit traffic, is managed by PointSav Digital Systems, and does not grant `os-*` application access. Machine-based authorization protects `os-*` application access, is managed by the machine's operator, and does not depend on PPN topology.

An attacker who fully compromises the PPN gains encrypted WireGuard traffic between VMs and nothing more — they cannot read application data without application pairings. An operator who revokes an application pairing blocks application access even if the machine remains on the PPN.

## See also

- [[machine-based-auth]] — the application-layer authorization that operates above the PPN
- [[sovereign-mesh]] — the mesh architecture detail
- [[ppn-command-protocol]] — the 16-byte binary wire format for fleet commands
- [[genesis-protocol]] — how new nodes join the fleet securely
