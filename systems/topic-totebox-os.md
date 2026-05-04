---
schema: foundry-doc-v1
title: "Totebox OS"
slug: topic-totebox-os
category: systems
type: topic
quality: complete
short_description: "Totebox OS is the microkernel-based data-archive operating system used by PointSav to store institutional records as inert flat files with cryptographic integrity verification at the filesystem level."
status: active
last_edited: 2026-05-04
editor: pointsav-engineering
cites: []
paired_with: os-totebox.es.md
---

# Totebox OS

**Totebox OS** is the core data-archive layer of the PointSav platform. It runs on an seL4 {{gli|microkernel}} and enforces a strict separation between software execution engines and the corporate ledgers those engines read and write. Every institutional record lives as an inert flat file — Markdown, YAML, or CSV — that requires no proprietary runtime to open or interpret decades later.

The architecture is designed to build **Trustworthy Systems** by rejecting the conventional multi-tenant database model. In the Totebox model, the execution software and the data it processes occupy distinct directories, connected only through explicit, audited access paths.

## Directory structure

A Totebox deployment follows a three-directory layout, as seen in the `cluster-totebox-jennifer` implementation:

```
cluster-totebox-corporate/
├── app-console-input/      # execution software
├── assets/                 # physical vault — PDFs, images
└── ledger/                 # state machine — YAML metadata, CSV ledgers
```

The `ledger/` directory is the canonical record. The `assets/` directory holds binary artefacts. The `app-console-input/` directory contains the execution software that reads and writes to the other two. None of the three directories are permitted to commingle their contents.

## Flat files over databases

A flat file is a static sequence of bytes on disk. A relational database is a running software engine with its own memory model, parser, and network surface. **Totebox OS** stores corporate knowledge as flat files because a `.yaml` ledger or `.csv` register is universally readable without proprietary tooling and remains structurally stable across hardware generations.

The practical consequence is that data migration cost falls toward zero: the customer always holds the source in a form any text editor can open.

## Machine Authorization

The architecture rejects traditional role-based authorization in favor of **Machine Authorization** and **Device-based Permissions**. Every transaction on a PointSav appliance is cryptographically anchored to a {{gli|WORM ledger}}, ensuring that only authorized hardware devices can modify the system state.

## Deployment model

A Totebox deployment operates as a **Freely Transferable** system. It is delivered as a **Bootable Disk Image** that can be deployed on {{gli|Bare metal resources}} or public cloud resources without structural dependency on the hosting provider.

The Vendor (PointSav Digital Systems) engineers the Rust-based execution engines that safely read and write to the Totebox directories. The Customer deploys the Totebox on their own hardware and holds the audit ledger directly. No vendor intermediary sits between the customer's records and the customer's filesystem.

## See Also

- [[topic-totebox-archive]]
- [[topic-totebox-orchestration]]
- [[topic-console-os]]
- [[topic-infrastructure-os]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
