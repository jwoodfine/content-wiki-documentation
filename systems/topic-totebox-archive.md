---
schema: foundry-doc-v1
title: "Totebox Archive"
slug: topic-totebox-archive
category: systems
type: topic
quality: complete
short_description: "A Totebox Archive is a self-contained, freely transferable micro-virtual machine that persists institutional data as immutable flat files."
status: active
last_edited: 2026-05-04
editor: pointsav-engineering
cites: []
---

# Totebox Archive

A **Totebox Archive** is the fundamental unit of data storage and sovereignty within the PointSav platform. It operates as a **Micro Virtual Machine** that provides self-contained services for specific institutional assets.

## Immutable Data Layer

Unlike traditional databases that require active processes to access data, a Totebox Archive persists information as **immutable flat files** (JSONL, GeoParquet, Markdown). This decoupling ensures that the data remains accessible and readable even if the original software engine is no longer running.

Each archive is cryptographically anchored to a {{gli|WORM ledger}}, creating a permanent, verifiable {{gli|Audit trail}} for all transactions and state changes.

## Freely Transferable System

A key architectural requirement of the PointSav system is that data must be an asset, not a liability. A Totebox Archive is designed to be **Freely Transferable**. It is packaged as a **Bootable Disk Image** that can be moved between physical servers, private clouds, or bare metal resources without losing its integrity or historical context.

## Asset Specialization

Totebox Archives are typically deployed as specialized containers for distinct institutional domains. Common archive types seen in the `cluster-totebox-jennifer` deployment include:

*   **Totebox Archive - Personnel:** Encrypted records and identification.
*   **Totebox Archive - Corporate:** Tax identification, formation documents, and minutes.
*   **Totebox Archive - Property:** Land titles, zoning records, and construction ledgers.

## See Also

- [[topic-totebox-os]]
- [[topic-totebox-orchestration]]
- [[topic-infrastructure-os]]
- [[topic-site-ledger-integration]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
