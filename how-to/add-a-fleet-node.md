---
schema: foundry-doc-v1
title: "How to add a node to a running fleet"
slug: add-a-fleet-node
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: add-a-fleet-node.es.md
---

A running fleet has one or more PPN nodes already enrolled and actively sending heartbeats. Adding a node to a running fleet means enrolling a new machine without interrupting the existing nodes' operation. This guide covers the steps specific to adding to an active fleet, as opposed to enrolling the very first node.

For the initial node enrollment procedure, see [[enroll-ppn-node]]. For the fleet controller service, see [[service-vm-fleet]].

## Prerequisites

- At least one node already enrolled and the fleet controller running (see [[enroll-ppn-node]])
- A second machine prepared with `service-vm-host` installed
- A new unique `NODE_ID` that does not conflict with any existing node in the tenant namespace

## Step 1: Verify the fleet controller's current state

Before adding a node, confirm the existing fleet is healthy:

```
curl -s "http://<fleet-controller-host>:9203/v1/vms?tenant_id=<your-tenant-id>"
```

All existing nodes should show a recent `last_heartbeat` timestamp (within the last 60 seconds under default settings). A node showing a stale heartbeat has a connectivity problem — resolve it before adding a new node to avoid confusing the advisory placement algorithm.

## Step 2: Choose a node ID that does not conflict

The fleet controller rejects duplicate `NODE_ID` values within a tenant namespace. List the current IDs:

```
curl -s "http://<fleet-controller-host>:9203/v1/vms?tenant_id=<your-tenant-id>" \
  | jq '.[].node_id'
```

Pick an ID for the new node that follows the naming pattern of existing nodes (e.g., if existing nodes are `compute-west-01` and `compute-west-02`, name the new one `compute-west-03`).

## Step 3: Configure and start the heartbeat agent on the new machine

On the new machine, set the configuration and start `service-vm-host`:

```
FLEET_CONTROLLER_URL=http://<fleet-controller-host>:9203
TENANT_ID=<your-tenant-id>
NODE_ID=<new-unique-id>

service-vm-host --controller $FLEET_CONTROLLER_URL --tenant $TENANT_ID --node-id $NODE_ID
```

The agent registers on its first heartbeat. The fleet controller updates its advisory placement data automatically — no restart of the controller or other nodes is required.

## Step 4: Verify the new node appears in the fleet

Query the fleet again and confirm the new node appears alongside the existing ones:

```
curl -s "http://<fleet-controller-host>:9203/v1/vms?tenant_id=<your-tenant-id>"
```

The response should now include the new node with a `last_heartbeat` from within the last 60 seconds.

## Step 5: Confirm load distribution

The fleet controller's advisory placement algorithm balances new tenant VM placements across healthy nodes. After adding a node, submit a new VM placement request and verify the controller considers the new node as a candidate:

```
curl -s "http://<fleet-controller-host>:9203/v1/placement?tenant_id=<your-tenant-id>"
```

The response suggests a target node based on current capacity. If the new node does not appear as a candidate, check that its reported capacity fields are populated (memory, CPU) in the heartbeat data.

## Key takeaways

- The fleet controller accepts new nodes without requiring existing nodes to restart
- Duplicate `NODE_ID` values within a tenant namespace are rejected — verify current IDs before choosing one
- Advisory placement updates automatically when a new node's first heartbeat arrives
- A stale heartbeat from existing nodes should be resolved before adding new nodes to avoid placement skew

## See also

- [[enroll-ppn-node]] — enrolling the first node in a fleet from scratch
- [[service-vm-fleet]] — the fleet controller service that manages node inventory and advisory placement
- [[configure-tenant-namespace]] — the namespace that contains the fleet's nodes
- [[ppn-small-business-compute]] — the fleet architecture and the role of each node tier
- [[verify-worm-ledger]] — confirming that node enrollment events are permanently recorded
