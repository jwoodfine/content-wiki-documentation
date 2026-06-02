---
schema: foundry-doc-v1
title: "Totebox Archive"
slug: totebox-archive
short_description: "A Totebox Archive is a sovereign data vault assigned to a single entity — packaged as a freely transferable bootable disk image, storing data as WORM flat files, and accepting queries only via the Diode Standard and PointSav Protocol."
category: systems
type: topic
status: active
bcsc_class: public-disclosure-safe
language: en
paired_with: totebox-archive.es.md
last_edited: 2026-05-30
editor: editorial
---

A Totebox Archive is a sovereign data vault assigned to a single entity — a building, a company, a person, or any other unit the operator defines. It is the fundamental storage and identity unit of the PointSav stack. The archive is packaged as a bootable disk image and runs as a virtual machine on the PPN hypervisor layer. It is released under Apache 2.0 and available free of charge: one operator, one archive, is a free deployment.

## The disk image is the archive

The most important property of a Totebox Archive is that the bootable disk image and the archive are the same thing. There is no external database, no cloud storage bucket, and no central registry that holds the archive's data. The disk image contains everything: the data, the identity keypair, and the operating system that serves queries.

This means an archive can be:

- **Stopped** — the VM is shut down; no data is lost; nothing expires
- **Copied** — the disk image is a file that can be duplicated like any other file
- **Relocated** — the copy is started on a different PPN node; the destination node's hypervisor allocates resources from its own pool for the new VM
- **Resumed** — the archive continues from exactly the state it was in when stopped

The receiving node's hypervisor knows nothing about the data inside the VM. It allocates CPU and RAM from its per-node pool to host the VM. The archive's identity, keys, and data travel with the disk image unchanged. This is the freely transferable property.

## Storage model: WORM flat files

A Totebox Archive stores data as immutable flat files:

| Format | Content |
|---|---|
| JSONL | Structured records (ledger entries, event logs, entity metadata) |
| GeoParquet | Geospatial data (site boundaries, location records) |
| Markdown | Human-readable documents (memos, notes, reports) |

Every write appends; no record is ever modified or deleted. This is a Write Once, Read Many (WORM) ledger. The archive accumulates a complete, tamper-evident history of every entry ever recorded. There is no `DELETE` operation and no `UPDATE` operation — only append. An entry that must be superseded is followed by a correction entry; the original entry remains permanently visible in the log.

This design is intentional: the archive is a legal-grade record of what an entity knew and when it knew it. The immutability guarantee is structural, not a configuration option.

## Access model: Diode + PSP only

A Totebox Archive does not expose a general-purpose API. It responds only to queries delivered via the [[diode-standard|Diode Standard]] — the unidirectional command flow that governs the PointSav stack:

```
os-console  ──┐
               ├──▶  os-orchestration  ──▶  os-totebox (inside the archive VM)
               │         (PSP)
               └──▶  os-totebox (direct, single-archive)
```

Queries arrive as signed capability objects delivered over the PointSav Protocol (PSP), a capability-based binary protocol that tunnels over TLS. A capability object grants permission to read a specific row or set of rows — nothing more. The archive verifies the object's signature against its MBA keypair, executes the query, and returns only the matching result rows. It never returns raw records in bulk. It never accepts commands from a direction outside the Diode flow.

No VM can issue commands back up the Diode to the control plane. No archive can instruct the PPN mesh to add or remove a node. The flow is structurally unidirectional.

## Machine-Based Authorization keypair

Each Totebox Archive holds an Ed25519 keypair. This keypair is the archive's identity on the PointSav mesh. It is registered in `pairings.yaml`, the file that governs which operators and orchestrators are authorised to query the archive.

The pairing types are:

| Type | Access level |
|---|---|
| ADMIN | Full administrative authority over this archive |
| INPUT | Read-write; default pairing for active data entry |
| USER | Read-only |
| INTERFACE | Metadata-only; no record content |

An operator with no entry in `pairings.yaml` cannot query the archive, regardless of whether they are on the same PPN mesh. Network reachability and data access are separate planes with no shared authority.

## Cluster naming convention

Archives are named with the `cluster-totebox-` prefix followed by the data domain and an instance number:

| Instance name | Domain |
|---|---|
| `cluster-totebox-corporate-1` | Corporate entity records |
| `cluster-totebox-personnel-1` | Personnel records |
| `cluster-totebox-property-1` | Real property records |

The prefix `cluster-` indicates a VM instance managed by the PPN hypervisor layer. The number suffix allows multiple archives of the same domain to coexist on the same fleet.

## Relationship to the OS family

| Component | Role |
|---|---|
| `os-totebox` | The operating system that runs inside the archive VM; manages the WORM ledger and the PSP query surface |
| `os-console` | A keyboard-native terminal that connects to one archive at a time; free tier |
| `os-orchestration` | A stateless multi-archive aggregator that fans queries across many archives via PSP; paid tier |
| `os-infrastructure` | The Type I hypervisor that hosts archive VMs and manages the per-node resource pool |

`os-totebox` and `os-console` are Apache 2.0 — free. `os-orchestration` introduces the commercial boundary: querying a single archive directly via `os-console` is free; routing queries across multiple archives through `os-orchestration` is the paid tier.

## What a Totebox Archive is not

- **Not a database.** There is no query planner, no index, no transaction log in the relational-database sense. The archive is an append-only ledger that returns rows matching a signed capability object.
- **Not cloud storage.** There is no S3 bucket, no object storage API, no presigned URL. Data exits the archive only via the Diode + PSP path.
- **Not a file share.** There is no SMB share, no NFS mount, no SFTP endpoint. Operators access data through `os-console` or `os-orchestration`, not through filesystem protocols.
- **Not a VM in the general sense.** The VM is the packaging medium. The archive is the data, identity, and history it contains. When someone refers to "the Totebox Archive", they mean the disk image and its contents — not the hypervisor instance that happens to be running it at this moment.

## See also

- [[infrastructure-os]] — the Type I hypervisor that hosts archive VMs and manages the resource pool
- [[ppn-hypervisor-resource-pool]] — how the hypervisor gives and reclaims CPU/RAM from each VM
- [[machine-based-auth]] — the Ed25519 keypair model that governs archive access
- [[diode-standard]] — the unidirectional command flow that every archive query traverses
