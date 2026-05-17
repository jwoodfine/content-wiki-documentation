---
schema: foundry-doc-v1
title: "Fleet control plane"
slug: os-network-admin
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: os-network-admin.es.md
short_description: "os-network-admin is the control plane for a PointSav fleet — one instance per fleet, managing the pairing registry, Diode rules, and mesh routing policy. Commands are composed on an F8 semantic terminal and broadcast as 16-byte binary packets across the WireGuard mesh."
cites: []
---

`os-network-admin` is the control plane for a PointSav fleet — one instance per deployment, managing the pairing registry, Diode enforcement rules, and WireGuard mesh routing policy for all `os-infrastructure` nodes in the fleet. Administrators compose commands on an F8 semantic terminal, where plain-language intent is translated locally by `service-slm` into 16-byte binary commands that broadcast across the mesh simultaneously to every node. There is no central message broker and no third-party service involved in this path. This article covers the control plane's role, the command dispatch architecture, and the relationship between `os-network-admin` and the `os-infrastructure` nodes it governs.

## The control plane role

`os-network-admin` runs one instance per fleet. Its responsibilities are:

| Function | Description |
|---|---|
| Pairing registry | Maintains the authoritative list of valid `service-pairing` entries across the fleet; issues and revokes hardware-bound fiduciary tokens |
| Diode rule enforcement | Defines which command flows are permitted between fleet members per the [[diode-standard|Diode Standard]]; changes propagate to all nodes via mesh broadcast |
| Mesh routing policy | Manages the WireGuard overlay topology — peer lists, allowed IP ranges, handshake schedules |
| Fleet claims | Accepts incoming Genesis Protocol claim requests from new `os-infrastructure` nodes joining the fleet |

## The F8 terminal and command dispatch

`os-network-admin` operates an F8 terminal — a keyboard-driven semantic input surface. An administrator types plain-language intent; `service-slm` running locally on the same node translates it into a binary command without contacting any external service.

The dispatch sequence:

1. The administrator types intent at the F8 terminal — for example, instructing the system to isolate a specific edge node.
2. `service-slm` (running on the same `os-network-admin` node) parses the sentence and produces a two-byte binary command identifying the operation and the target node.
3. `service-udp` broadcasts the 16-byte command packet across the WireGuard mesh on port 8090.
4. Every node in the fleet receives the packet simultaneously. Only the addressed node acts; the others discard.

The translation layer is invisible at the protocol boundary — the mesh sees only the binary command, not the natural-language sentence. The administrator sees only the F8 terminal, not a chat interface.

## Relationship to os-infrastructure

`os-network-admin` and `os-infrastructure` are designed as a pair:

| Layer | Role |
|---|---|
| `os-infrastructure` | Compute substrate — boots on hardware, runs the WireGuard peer, hosts Totebox and other OS instances |
| `os-network-admin` | Control plane — governs the fleet, owns the pairing registry, broadcasts commands |

A minimal fleet is one `os-network-admin` instance and one or more `os-infrastructure` nodes. The control plane does not run on the same node as the compute substrate in production deployments, though a single-machine development configuration is possible.

## See also

- [[infrastructure-os]] — the compute substrate nodes that `os-network-admin` governs
- [[os-family-overview]] — the eight-OS family and how each member fits
- [[diode-standard]] — the protocol governing unidirectional command flow across the fleet
- [[service-slm]] — the local semantic language model that translates commands
- [[machine-based-auth]] — the fiduciary keypairs and pairing registry `os-network-admin` manages
- [[deployment-patterns]] — the six canonical fleet configurations
