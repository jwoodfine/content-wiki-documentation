---
schema: foundry-doc-v1
title: "Enroll a PPN node"
slug: enroll-ppn-node
short_description: "Enrolls a machine into a PPN compute fleet by setting service-vm-host's three required environment variables, running it under systemd, and confirming the node in the controller listing."
category: machine-authorization
index_group: fleet-enrollment
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); fleet operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: enroll-ppn-node.es.md
research_trail:
  sources: [pointsav-monorepo service-vm-host (environment-variable configuration, heartbeat loop), service-vm-fleet (route table, node record struct, staleness sweep, in-memory state), infrastructure systemd unit for service-vm-host]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; the three required and three optional environment variables, their exact defaults, the hardcoded controller port, the full route list, the replace-not-merge heartbeat semantics, the 30-second staleness drop, and the absence of both a /healthz route and any ledger write were each confirmed at their definition site — correcting an earlier, unverified correction note that had claimed a 30-second default heartbeat interval (the real default is 10 seconds) and a WORM ledger entry per heartbeat (no such write exists anywhere in this code)"
---

## Prerequisites

- The `service-vm-host` binary deployed on the machine you are enrolling
- Network reachability from that machine to the fleet controller on port 9203 — the controller's port is hardcoded and not configurable
- A node identifier unique within the fleet
- The node's WireGuard IP address
- systemd, or another supervisor that restarts a failed process

## Purpose

Register a machine with `service-vm-fleet` by starting the per-node heartbeat agent on it — about five minutes, after which the node appears in the controller's listing within one heartbeat interval.

## Procedure

1. Set the three required environment variables for `service-vm-host`. The agent has no CLI flags and reads no config file; it refuses to start unless all three are present:

   ```bash
   VM_FLEET_ENDPOINT=http://<fleet-controller-host>:9203
   VM_NODE_ID=<unique-node-identifier>
   VM_WG_IP=<node-wireguard-ip>
   ```

2. Optional: override any of the three defaults, each of which is usable as shipped:

   | Variable | Default | Effect |
   |---|---|---|
   | `VM_HEARTBEAT_INTERVAL_S` | `10` | Seconds between heartbeats to the controller |
   | `VM_SPAWN_PORT` | `9204` | Port the agent's own local API listens on |
   | `VM_RESERVED` | `false` | Marks the node last-resort-only for placement |

3. Start `service-vm-host` under systemd, configured to restart automatically on failure. The agent begins heartbeating to `POST /v1/nodes/heartbeat` immediately and needs no separate registration call first.

4. Confirm the node reached the controller:

   ```bash
   curl -s http://<fleet-controller-host>:9203/v1/nodes/<VM_NODE_ID>
   ```

## Expected outcome

The node appears in `GET /v1/nodes` and `GET /v1/fleet` within one heartbeat interval — ten seconds with the default. Its record carries `node_id`, `hostname`, `wg_ip`, `ram_available_mb`, `vm_count`, `kvm_available`, `reserved`, and `last_heartbeat` as an RFC3339 timestamp.

## Verification

```bash
curl -s http://<fleet-controller-host>:9203/v1/nodes    # full node list
curl -s http://<fleet-controller-host>:9203/v1/fleet    # whole-fleet status
```

Look for your `VM_NODE_ID` with a `last_heartbeat` no older than one heartbeat interval. There is no `status` field on a node record — recency of `last_heartbeat` is the only liveness signal the controller exposes, and a node that stops heartbeating for more than 30 seconds is dropped from the listing entirely rather than shown as stale or offline. A node absent from `/v1/nodes` is therefore either never-enrolled or more than 30 seconds silent; the API does not distinguish the two.

> **Note:** `service-vm-fleet` has no `/healthz` route. To confirm the controller itself is answering, call `GET /v1/fleet`.

> **Note:** each heartbeat replaces the controller's record of that node wholesale — VMs and resource stats are overwritten, not merged into the previous state.

> **Note:** to inspect a VM, list VMs with `GET /v1/vms` (optionally filtered with `?tenant_id=`) and filter client-side. `DELETE /v1/vms/:vm_id` exists, but there is no GET for a single VM by id.

> **Warning:** fleet state is held in memory on the controller only. If the controller process restarts, every node and VM record is lost until nodes heartbeat again. No ledger entry is written on enrollment or on heartbeat, so a restart leaves no record of what the fleet contained beforehand.

## Rollback

Stop the `service-vm-host` process. After roughly 30 seconds without a heartbeat the controller drops the node from its listing on its own. No unenroll call is needed, and none exists.

Re-enrolling is the same procedure: start the agent again with the same `VM_NODE_ID` and the node reappears at the next heartbeat.

## Next steps

- [[add-a-fleet-node]] — the fleet-side companion procedure
- [[service-vm-fleet]] — the controller's state model and route surface
- [[ppn-small-business-compute]] — the fleet architecture this node joins
- [[os-infrastructure-ppn-node]] — the node image built around this agent
