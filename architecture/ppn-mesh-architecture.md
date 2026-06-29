---
schema: foundry-doc-v1
title: "PPN mesh architecture"
slug: ppn-mesh-architecture
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: ppn-mesh-architecture.es.md
short_description: "The PointSav Private Network uses a hub-and-spoke WireGuard mesh to connect fleet nodes, with physical key custody on the operator's premises; this article covers mesh topology, node joining (Mesh Fusion), the F8 Terminal human-in-the-loop protocol, and the deliberate isolation between the network layer and the application authorization layer."
cites: []
references:
  - id: 1
    text: "Donenfeld, J. A. 'WireGuard: Next Generation Kernel Network Tunnel.' NDSS Symposium, 2017."
    url: "https://www.ndss-symposium.org/ndss2017/ndss-2017-programme/wireguard-next-generation-kernel-network-tunnel/"
---

The PointSav Private Network (PPN) is the encrypted WireGuard mesh that connects Woodfine's fleet nodes. It is a network infrastructure layer: it provides encrypted transit between virtual machines, maintains stable node topology, and hosts the `os-*` services that run Totebox Archives and orchestration gateways.

The PPN is not an authorization system. Network membership does not confer application access. A machine on the PPN can reach other mesh nodes; it cannot read the contents of any archive without a separate [[machine-based-auth|Machine-Based Authorization]] pairing established at the application layer. The two mechanisms address different problems and are covered separately. This article covers the PPN.

For the four-layer model of the PPN as a compute platform — operator layer, network layer, VM layer, and application layer — see [[ppn-architecture-overview]].

## Hub-and-spoke topology

The PPN uses a hub-and-spoke topology. Traffic between spoke nodes transits the cloud hub rather than flowing peer-to-peer directly. This arrangement provides two properties: spoke nodes with dynamic or private IP addresses can always reach each other through the hub's stable public endpoint, and no spoke node needs to accept inbound connections from the public internet.

| Node class | Deployment | WireGuard role |
|---|---|---|
| Cloud relay | GCP compute instance with static public IP | Hub — always listening; relays encrypted WireGuard packets between spokes |
| On-premises workstation | Operator's primary machine on the local network | Spoke — dials out to cloud hub at startup |
| Portable endpoints | Laptops and field machines | Spoke — dials out to cloud hub when online |

All connections initiate from spokes. The hub never dials in to spoke nodes. Public internet traffic cannot reach spoke nodes directly — they do not listen for inbound connections.

The cloud relay performs packet relay only. It moves encrypted WireGuard frames between spoke peers; it does not terminate application-layer connections, cannot decrypt `os-*` service traffic, and has no access to archive data.

## Physical key custody

NODE-IMAC-12, the on-premises workstation, holds the master WireGuard configuration for the fleet: the authoritative peer registry, the subnet assignments, and the WireGuard private key for that node. Placing this custody on a physical machine under the operator's direct control is deliberate.

If the cloud relay is destroyed or deprovisioned, the master configuration survives at NODE-IMAC-12. A replacement relay requires only a new cloud instance with a new IP; the WireGuard keys that define the network remain with the customer, not with the vendor. The network can be rebuilt without vendor involvement.

NODE-IMAC-12 is also the primary deployment target for `os-console`, the keyboard-native console interface for Totebox Archive operations (see [[os-console-platform]]).

## The WireGuard cryptographic fabric

WireGuard [^1] uses Curve25519 elliptic-curve key pairs: one private and one public key per node. The private key never leaves the node on which it was generated. Public keys are distributed to peers and recorded in the hub's WireGuard peer configuration.

The key lifecycle follows minimum-exposure principles: private keys are stored on-device only, never transmitted to any other party. The peer registry — the record of which machines are members of the mesh — is maintained at `route-network-admin`, the administrative interface for the network. Subnet address assignments are managed alongside the peer registry.

The PPN uses a Zero-Broker UDP broadcast pattern for fleet health signalling: health commands are broadcast simultaneously to all active nodes across the mesh, without routing through a central broker. Every node that is online responds. The pattern eliminates the single point of failure that a central command broker would introduce.

## Mesh Fusion: joining the network

Joining a new physical node to the PPN is called Mesh Fusion. The procedure is infrastructure-layer provisioning only:

1. Install the host operating system on the target hardware.
2. Generate a WireGuard Curve25519 key pair on the new node.
3. Register the public key with the peer registry at `route-network-admin`.
4. Configure the WireGuard interface on the new node: hub endpoint, assigned subnet IP, and allowed peers.
5. Establish the encrypted tunnel: the new spoke dials the cloud relay.
6. Verify connectivity: the hub observes the new spoke; the spoke can reach other mesh nodes.

Mesh Fusion completes at step 6. The node is now a network member. No application-layer permissions are conferred. For a node to access a Totebox Archive — to read files, execute editorial workflows, or manage governance records — [[machine-based-auth|Machine-Based Authorization pairing ceremonies]] must be performed separately.

## The F8 Terminal: human-in-the-loop mesh management

The PPN is managed through `os-network-admin`, accessed via the F8 slot in `os-console`. The interface enforces a two-step protocol that ensures human confirmation of all network state changes.

The operator submits a management intent in natural language. The system translates the intent into a structured command payload using the local inference service. The interface pauses and displays the proposed action for visual inspection before broadcasting. The operator explicitly confirms before the command executes.

No network change broadcasts from an ambiguous or unreviewed translation. The inference service translates; the human authorizes.

## Deliberate application-layer isolation

The most significant architectural property of the PPN is what it deliberately does not do: grant access to the application data running on the nodes it connects.

The network layer carries encrypted packets between virtual machines. A machine on the PPN that holds no MBA pairings can reach the mesh and cannot access any archive. This isolation produces a specific security boundary: the infrastructure vendor — the party that built and operates the PPN — has no application-layer access to customer Totebox Archives through the network infrastructure. The vendor holds the network. The customer holds the authorization.

## PPN and MBA: independent layers

The PPN and [[machine-based-auth|Machine-Based Authorization]] are designed to be independent. Neither depends on the other for its security guarantees.

| Layer | What it secures | Managed by | Does not do |
|---|---|---|---|
| PPN (WireGuard) | Network topology; encrypts transit traffic between nodes | Infrastructure operator (vendor) | Does not grant application-layer access to `os-*` services |
| MBA (peer-to-peer) | Application-layer access to `os-*` services | Machine's operator (customer) | Does not depend on PPN topology for its security properties |

An attacker who fully compromises the cloud relay gains access to encrypted WireGuard traffic between VMs and nothing further — application data is not accessible without MBA pairings. An operator who revokes an MBA pairing blocks application access regardless of whether the machine remains on the PPN.

The two layers together provide defence in depth. They also enforce a sovereignty boundary: the vendor controls the infrastructure; the customer controls authorization.

## Cold Storage Entanglement

Large archive data that exceeds the scope of in-network storage — architectural drawings, IoT sensor logs, extensive media assets — is managed through cryptographic splitting and physical custody. External storage media is mathematically bound to a specific archive using a key derived from that archive's identity. The bound media is unreadable on any other system.

Cold Storage Entanglement operates outside the PPN. It is a physical custody mechanism, not a network mechanism. The binding key resides on the archive node; the media reads only when connected to that specific node. The core operating environment remains lightweight; overflow data stays under the customer's physical custody.

## See also

- [[ppn-architecture-overview]] — the four-layer model of PPN as a compute platform
- [[machine-based-auth]] — the application-layer authorization mechanism that operates above the PPN
- [[os-console-platform]] — the console interface for operators using archives connected through the PPN
- [[three-ring-architecture]] — the service architecture that runs on the PPN infrastructure
