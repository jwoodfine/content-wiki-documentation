---
schema: foundry-doc-v1
type: topic
slug: sys-adr-16
title: "SYS-ADR-16: Application-Level Unicast Mesh over WireGuard"
category: governance
language: en
paired_with: sys-adr-16.es.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

Architecture decision record replacing native UDP broadcast (incompatible with WireGuard Layer-3 routing) with an application-level unicast loop that delivers commands to each peer node individually.
