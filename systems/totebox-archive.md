---
schema: foundry-doc-v1
title: "Totebox archive"
slug: totebox-archive
category: systems
type: topic
quality: complete
short_description: "A Totebox Archive is a self-contained, freely transferable micro-virtual machine that persists institutional data as immutable flat files."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
---

A Totebox Archive is the fundamental unit of data storage and sovereignty within the PointSav platform — a self-contained micro-virtual machine that persists institutional records as immutable flat files and can be physically transferred between cloud providers, private servers, or bare-metal hardware without losing its cryptographic integrity. Each archive is cryptographically anchored to a Write-Once-Read-Many (WORM) ledger, creating a permanent and verifiable audit trail for every transaction and state change.

## Immutable data layer

Unlike traditional databases that require active processes to access data, a Totebox Archive persists information as immutable flat files — JSONL, GeoParquet, and Markdown — so the data remains accessible and readable even if the original software engine is no longer running. No proprietary runtime is required to read the records decades later.

## Freely transferable design

A Totebox Archive is packaged as a bootable disk image that can be moved between physical servers, private clouds, or bare-metal hardware without losing integrity or historical context. The operator picks up the image and moves it; there is no host operating system underneath that holds the keys.

## Asset specialization

Totebox Archives are typically deployed as domain-specific containers for distinct institutional assets. Common archive types include:

| Archive type | Contents |
|---|---|
| Personnel | Encrypted records and identification |
| Corporate | Tax identification, formation documents, and minutes |
| Property | Land titles, zoning records, and construction ledgers |

## See also

- [[totebox-os]]
- [[totebox-orchestration]]
- [[infrastructure-os]]
- site-ledger-integration
