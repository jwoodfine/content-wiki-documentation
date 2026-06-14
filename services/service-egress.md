---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-egress
short_description: "The data sovereignty service that physically transfers cloud-stored payloads to local cold storage, executing flow-through protocols that eliminate vendor-side data retention and cloud storage dependency."
title: "Egress service"
category: services
language: en
paired_with: service-egress.es.md
status: stub
last_edited: 2026-05-07
editor: pointsav-engineering
---

[[service-fs-architecture|`service-egress`]] is the data sovereignty engine that physically transfers cloud-stored payloads to local cold storage, executing the flow-through protocol that removes vendor-side data retention and eliminates dependency on cloud storage continuity. Transferred payloads are written to the per-tenant [[worm-ledger-design|WORM ledger]] managed by [[service-fs-architecture]], where they become append-only records. The service works alongside [[service-email]] to ensure every message ingested from a cloud mailbox has a permanent local copy before the cloud source is cleared. See the [[sovereign-airlock-doctrine|sovereign airlock]] for the architectural principle that governs data flow direction.
