---
schema: foundry-doc-v1
title: "The PPN Command Protocol"
slug: ppn-command-protocol
short_description: "The PPN Command Protocol is the 16-byte binary wire format used by os-network-admin to issue commands to os-infrastructure nodes across the WireGuard mesh, with no central broker and no session overhead."
category: architecture
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: en
paired_with: ppn-command-protocol.es.md
last_edited: 2026-06-23
editor: pointsav-engineering
---

The PPN Command Protocol is the wire format used by every `os-network-admin` control plane to issue commands to `os-infrastructure` nodes across the PointSav Private Network. It transmits fleet commands as 16-byte binary packets broadcast over UDP port 8090 on the WireGuard mesh — with no central broker, no queue, and no third-party service in the path. Every node in the fleet receives every packet simultaneously; only the addressed node acts.

## Design constraints

The protocol was shaped by three requirements that exclude conventional approaches:

**No broker.** A message broker is a single point of failure and a trust boundary problem — it must be authenticated, maintained, and trusted. The PPN command protocol eliminates the broker entirely. The control plane broadcasts; the mesh delivers; the node decides.

**No plaintext.** The protocol runs exclusively over the WireGuard mesh. WireGuard's Noise Protocol IK handshake authenticates every peer before any packet is delivered. A command packet never travels over an unencrypted link.

**No verbosity.** Commands are 16 bytes. There is no session negotiation, no acknowledgement handshake, no framing overhead. At the receiving node, a 16-byte read either matches a known operation or it does not.

## The packet format

Each command is exactly 16 bytes. The first two bytes constitute the operation code: one byte identifying the operation class, one byte identifying the target node. The remaining 14 bytes are available to carry operation-specific payload — node address, isolation policy, or other parameters depending on operation class.

```
 0               1               2               3  ...  15
 ┌───────────────┬───────────────┬───────────────────────────┐
 │  op class (1) │  target (1)   │  payload (14 bytes)       │
 └───────────────┴───────────────┴───────────────────────────┘
```

The operation code is produced by `service-slm` running locally on the `os-network-admin` node — the natural-language sentence the administrator types never reaches the wire.

## The dispatch sequence

1. The administrator types plain-language intent at the F8 terminal — for example, instructing the fleet to isolate a specific edge node.
2. `service-slm` running locally on the `os-network-admin` node parses the sentence and produces the two-byte operation code identifying the operation class and target.
3. `service-udp` constructs the full 16-byte packet and broadcasts it across the WireGuard mesh on UDP port 8090.
4. Every node in the fleet receives the packet simultaneously. Only the node whose address matches the target byte acts; all others discard.

The translation layer is invisible at the protocol boundary — the mesh sees only the binary command, not the natural-language sentence. There is no audit record of the original text at the protocol layer; that record lives in the F8 terminal log on `os-network-admin`, not in the mesh.

## Why simultaneous broadcast

The broadcast model is deliberate. A unicast model would require the control plane to maintain a routing table with individual addresses for each node, and would require per-node TCP sessions or acknowledgements. Both introduce state that can drift out of sync.

Broadcast over a WireGuard mesh eliminates both problems. Every peer receives every packet. The addressed node acts; the others discard at the first byte comparison. The control plane has no routing state to maintain beyond the mesh peer list, which is managed by `os-network-admin`'s mesh routing policy function.

The security constraint is satisfied by the mesh itself: non-members cannot receive mesh packets because they do not hold a valid WireGuard handshake with the hub.

## Relationship to the Diode Standard

The PPN Command Protocol is the wire implementation of the [[diode-standard|Diode Standard]]'s downstream control category. It flows from authority (`os-network-admin`) to subject (`os-infrastructure`) and never the reverse. There is no upstream command path in the protocol: the packet format contains no reply-to address, no acknowledgement field, and no mechanism for a Subject node to initiate a packet toward the Authority.

Upstream telemetry — logs, heartbeats, status — travels over a separate, strictly sanitised channel. The command protocol and the telemetry channel are intentionally decoupled so that a failure in one does not affect the other.

## See also

- [[os-network-admin]] — the control plane that produces and broadcasts command packets
- [[infrastructure-os]] — the compute substrate nodes that receive and execute commands
- [[diode-standard]] — the authority hierarchy and traffic rules the protocol implements
- [[sovereign-mesh]] — the WireGuard overlay the protocol runs over
- [[service-slm]] — the local semantic router that translates intent into the two-byte operation code
- [[machine-based-auth]] — the fiduciary keypairs that secure the mesh peers
- [[pointsav-private-network|PointSav Private Network]] — infrastructure overview; the command protocol runs over this mesh
