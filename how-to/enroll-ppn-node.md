---
schema: foundry-doc-v1
title: "How to enroll a PPN node"
slug: enroll-ppn-node
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: enroll-ppn-node.es.md
---

A PPN (PointSav Private Network) node is a physical or virtual machine that joins the platform's compute fleet. Enrolling a node means registering it with the fleet controller, starting the heartbeat agent, and verifying the node appears in the fleet's active inventory. This guide covers the enrollment sequence for a single node.

For the fleet architecture, see [[ppn-small-business-compute]]. For the service that manages fleet state, see [[service-vm-fleet]].

## Prerequisites

- A machine with network access to the fleet controller endpoint
- The `service-vm-host` binary deployed on the node (the per-node heartbeat agent)
- The fleet controller address and tenant ID provided by the platform administrator
- A terminal session on the node being enrolled

## Step 1: Verify the fleet controller is reachable

From the node, confirm the fleet controller responds before starting the heartbeat agent:

```
curl -s http://<fleet-controller-host>:9203/health
```

A successful response returns `{"status":"ok"}`. If the controller is unreachable, verify network routing and firewall rules before proceeding. Enrollment requires a live connection to the controller.

## Step 2: Configure the heartbeat agent

The `service-vm-host` heartbeat agent reads its configuration from environment variables or a local config file. Set the minimum required values:

```
FLEET_CONTROLLER_URL=http://<fleet-controller-host>:9203
TENANT_ID=<your-tenant-id>
NODE_ID=<unique-node-name>
```

`NODE_ID` must be unique within the tenant's namespace. Use a descriptive name that identifies the machine's role and location (e.g., `compute-west-01`). Once set, this identifier appears in the fleet inventory and in the WORM audit ledger.

## Step 3: Start the heartbeat agent

Start `service-vm-host` as a systemd service or directly from the command line:

```
service-vm-host --controller $FLEET_CONTROLLER_URL --tenant $TENANT_ID --node-id $NODE_ID
```

The agent sends an initial heartbeat immediately and then on its configured interval (default: 30 seconds). The first successful heartbeat registers the node with the fleet controller.

## Step 4: Verify enrollment in the fleet inventory

From a session with access to the fleet controller API, query the fleet for the new node:

```
curl -s "http://<fleet-controller-host>:9203/v1/vms?tenant_id=<your-tenant-id>"
```

The response includes an array of enrolled nodes. Find the entry for the `NODE_ID` you set in step 2. The entry shows `status`, `last_heartbeat`, and resource capacity fields populated from the first heartbeat.

If the node does not appear within 60 seconds of starting the agent, check the agent logs for connection errors. The most common causes are a wrong controller URL or a firewall blocking outbound connections on port 9203.

## Step 5: Confirm the ledger entry

Every heartbeat writes a WORM ledger entry. From the fleet controller or from `service-fs`, confirm a ledger record exists for the new node:

```
service-fs read --filter node-id=<NODE_ID> --limit 5
```

A successful enrollment produces at least one `NODE_HEARTBEAT` entry. The ledger entry is the permanent enrollment record — it cannot be deleted or altered.

## Key takeaways

- Enrollment happens on first heartbeat; no separate registration step is needed
- `NODE_ID` must be unique per tenant namespace; the fleet controller rejects duplicates
- A WORM ledger entry is created for every heartbeat — enrollment is permanently recorded
- If the node does not appear after 60 seconds, check the agent logs before assuming a network problem

## See also

- [[ppn-small-business-compute]] — the PPN fleet architecture and tenant model
- [[service-vm-fleet]] — the fleet controller service that manages enrolled nodes
- [[add-a-fleet-node]] — how to add a node to a running multi-node fleet (operational follow-on)
- [[verify-worm-ledger]] — verifying the ledger entries created during enrollment
- [[pair-a-new-device]] — the pairing protocol that governs device-level access tiers
