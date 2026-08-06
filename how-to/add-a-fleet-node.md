---
schema: foundry-doc-v1
title: "Add a node to a running fleet"
slug: add-a-fleet-node
short_description: "Adds a second node to an already-running PPN fleet using service-vm-host's real env-var configuration — the same mechanism as the first node, since nothing about enrollment changes once a fleet exists."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); fleet operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: add-a-fleet-node.es.md
research_trail:
  sources: [pointsav-monorepo service-vm-host and service-vm-fleet, already fully source-verified while rewriting enroll-ppn-node.md earlier this session]
  verification_method: "reused the already-confirmed real service-vm-host/service-vm-fleet mechanism from this session's Machine authorization batch rather than re-deriving it; this guide's own prior Correction note had already flagged the same fictional CLI flags and routes found on enroll-ppn-node.md, and this guide contradicted that already-corrected sibling until now"
---

## Prerequisites

- At least one node already enrolled and heartbeating (see [[enroll-ppn-node]])
- A second machine with `service-vm-host` deployed
- A `VM_NODE_ID` that doesn't collide with any node already in the fleet

## Purpose

Enroll a second (or third, or Nth) node into a fleet that's already running — a few minutes, and it's exactly the same procedure as enrolling the first node. There is no separate "add to a running fleet" mechanism; the fleet controller accepts new nodes at any time without disturbing existing ones.

## Procedure

1. Check the existing fleet's current node IDs so your new one doesn't collide:

   ```bash
   curl -s http://<fleet-controller-host>:9203/v1/nodes
   ```

   The fleet controller rejects nothing at enrollment time based on naming — but reusing an ID would just mean the new node's heartbeats overwrite the existing node's record, not a clean rejection. Pick a genuinely distinct `VM_NODE_ID`.

2. On the new machine, set the same three required environment variables as any node enrollment:

   ```bash
   VM_FLEET_ENDPOINT=http://<fleet-controller-host>:9203
   VM_NODE_ID=<new-unique-node-id>
   VM_WG_IP=<new-node-wireguard-ip>
   ```

3. Start `service-vm-host` under systemd, as with any node. It begins heartbeating immediately — no registration call, and no restart of the controller or any existing node is required.

## Expected outcome

The new node appears in the fleet controller's listing alongside every existing node, each heartbeating independently, within one heartbeat interval (10 seconds by default).

## Verification

```bash
curl -s http://<fleet-controller-host>:9203/v1/nodes
```

Confirm your new `VM_NODE_ID` appears with a recent `last_heartbeat`, and confirm every previously-existing node is still present and heartbeating too — adding a node doesn't touch any other node's state.

## Rollback

Stop the new node's `service-vm-host` process. It drops out of the fleet listing on its own after roughly 30 seconds without a heartbeat — no separate removal step, and no effect on the rest of the fleet.

## Next steps

- [[enroll-ppn-node]] — the same procedure in full, including every environment variable and its default
- [[configure-tenant-namespace]] — set up quotas for tenants placing VMs on this expanded fleet

## See also

- [[service-vm-fleet]] — the fleet controller's real route table and state model
- [[ppn-small-business-compute]] — the fleet architecture this node joins
