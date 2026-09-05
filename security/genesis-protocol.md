---
schema: foundry-doc-v1
title: "Genesis protocol"
slug: genesis-protocol
short_description: "The Genesis Protocol is the designed fleet-bootstrapping sequence for os-infrastructure nodes: ship with no prior configuration, boot on any network, and reach a secure, claimable state with no control-plane contact required."
category: security
index_group: isolation-boundaries
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
paired_with: genesis-protocol.es.md
last_edited: 2026-08-22
editor: pointsav-engineering
---

The Genesis Protocol is the designed bootstrapping sequence for an `os-infrastructure` node. It lets a node ship to any location, power on with no prior configuration and no connection to a control plane, and reach a secure, claimable state that waits for an administrator rather than reaching out to one. The protocol inverts the usual order — instead of a control plane existing before compute can join it, the compute exists first and waits to be found.

A node shipped this way needs no pre-provisioning and exposes nothing to the network while it waits. An administrator can claim fifty nodes shipped to fifty locations whenever they're ready, days or months later, without touching any of them in between.

## How it works

The full sequence is designed and documented in the node's network stack, but not yet operational — the underlying NIC driver work it depends on hasn't landed. It runs in five stages once built:

1. **Discovery.** The node looks for a pairing server on the local network (an mDNS query), falling back to a pre-configured relay address if nothing answers within the discovery window. Finding neither, it holds — this is the expected state for a node waiting to be claimed, not a failure.
2. **Handshake.** If a pairing server responds, the node sends a handshake frame over UDP carrying an 8-character short code (Crockford base32).
3. **Key exchange.** A CPace password-authenticated key exchange (RFC 9382) follows the handshake. The resulting session key derives a 5-byte short authentication string, shown on the node's framebuffer.
4. **Ceremony.** The node registers a claim request with the pairing service and polls for a decision — up to ten minutes — while an administrator reviews the code and approves or denies it from their own console.
5. **Claim.** On approval, the node receives its mesh configuration and joins the [[sovereign-mesh|private network]], following the same node-join ceremony [[os-network-admin]] runs on the administrator's side.

**Nothing above is live yet.** Every step in the current code is an explicit placeholder: peer discovery always reports "not found," the handshake send always reports failure, and the crate's own status string is "skeleton — NIC driver pending." This describes the intended mechanism once the network driver work is complete, not current node behavior.

## Why the sequencing matters

Conventional fleet management requires the control plane to exist, be routed, and be ready before a node can join it — a coordination problem when hardware ships to a site before the management layer is ready, or the reverse. The Genesis Protocol removes that dependency: the node doesn't need the fleet to exist yet, only to eventually be found by it.

## Relationship to machine-based authorization

Once built, a successful claim is the entry point into [[machine-based-auth|machine-based authorization]]: the node-join ceremony's approval is what first registers the node with the fleet's pairing system, the same mechanism that governs every subsequent authentication.

## See also

- [[os-infrastructure-ppn-node]] — the node that runs the Genesis Protocol at first boot
- [[os-network-admin]] — the control plane that runs the claim/approval side of the ceremony
- [[sovereign-mesh]] — the private network overlay a node joins after a successful claim
- [[machine-based-auth]] — the authentication system a claimed node enters
