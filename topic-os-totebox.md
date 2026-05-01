---
schema: foundry-doc-v1
title: "ToteboxOS"
slug: topic-os-totebox
category: systems
type: topic
quality: stub
short_description: "ToteboxOS is the microkernel-based data-archive operating system used by PointSav to store institutional records as inert flat files with cryptographic integrity verification at the filesystem level."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-os-totebox.es.md
---

# ToteboxOS

> ToteboxOS is the microkernel-based data-archive operating system used by PointSav to store institutional records as inert flat files with cryptographic integrity verification at the filesystem level.

**ToteboxOS** is the core data-archive layer of the PointSav platform. It runs on an seL4 microkernel and enforces a strict separation between software execution engines and the corporate ledgers those engines read and write. Every institutional record lives as an inert flat file — Markdown, YAML, or CSV — that requires no proprietary runtime to open or interpret decades later.

The design rejects the conventional multi-tenant database model, in which a shared database engine becomes a single point of failure and exposure for every customer record it holds. In the Totebox model, the execution software and the data it processes occupy distinct directories, connected only through explicit, audited access paths.

## Directory structure

A Totebox deployment follows a three-directory layout:

```
cluster-totebox-corporate/
├── app-console-input/      execution software
├── assets/                 physical vault — PDFs, images
└── ledger/                 state machine — YAML metadata, CSV ledgers
```

The `ledger/` directory is the canonical record. The `assets/` directory holds binary artefacts. The `app-console-input/` directory contains the execution software that reads and writes to the other two. None of the three directories are permitted to commingle their contents.

## Flat files over databases

A flat file is a static sequence of bytes on disk. A relational database is a running software engine with its own memory model, parser, and network surface. ToteboxOS stores corporate knowledge as flat files because a `.yaml` ledger or `.csv` register is universally readable without proprietary tooling and remains structurally stable across hardware generations.

The practical consequence is that data migration cost falls toward zero: the customer always holds the source in a form any text editor can open.

## Cryptographic integrity

Because flat files cannot defend themselves against tampering, ToteboxOS enforces integrity at the filesystem level. When a physical asset — such as a contract document — enters the Totebox, the system generates a SHA-256 checksum of that file and records it in the `ledger/`. Any subsequent modification to the asset invalidates the recorded checksum, flagging the vault as compromised.

## Deployment model

The Vendor (PointSav Digital Systems) engineers the Rust-based execution engines that safely read and write to the Totebox directories. The Customer deploys the Totebox on their own hardware — an isolated cloud node or on-premise bare metal — and holds the audit ledger directly. No vendor intermediary sits between the customer's records and the customer's filesystem.

## See Also

- [[topic-totebox-orchestration]]
- [[topic-substrate-native-compatibility]]
- [[topic-customer-hostability]]
- [[topic-compounding-substrate]]

## References

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.