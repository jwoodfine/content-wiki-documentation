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

## Key Takeaways

- The flow-through protocol is three steps in order: download from cloud → write to local WORM → clear the cloud source. The original cloud copy is removed; the local WORM record is the permanent copy.
- Transferred payloads become append-only WORM records. The egress path cannot overwrite or delete prior records — data sovereignty is enforced structurally, not by policy.
- service-egress operates at the sovereignty boundary. Once a payload crosses from cloud to local WORM storage, it is no longer subject to the cloud provider's data retention, compelled-disclosure, or service-termination policies.
- The service depends on [[service-email]] for mailbox ingestion and on [[service-fs-architecture]] for the WORM storage interface. These three services together constitute the inbound data sovereignty stack.

## Flow-through protocol

The flow-through protocol proceeds as follows:

1. **Acquire** — `service-egress` connects to the cloud source (a mailbox via IMAP, an object store, or a cloud file system) and fetches the payload.
2. **Write** — the payload is written to the per-tenant WORM ledger via `service-fs`. The write is acknowledged only when the ledger confirms the record is durable on local storage.
3. **Clear** — only after a confirmed durable local write does `service-egress` issue the delete or archive command to the cloud source. The clearing step is conditional: if the write fails, the cloud copy is preserved.

This ordering ensures that payload loss is impossible within the service's failure domain. A crash between steps 2 and 3 leaves the payload in both places; the next run deduplicates before retrying the clear.

## See also

- [[sovereign-airlock-doctrine]] — the architectural principle governing unidirectional data flow into the WORM ledger
- [[service-email]] — the email ingestion service that coordinates with service-egress for mailbox ingest
- [[service-fs-architecture]] — the file-system service providing the WORM ledger interface
- [[worm-ledger-design]] — the append-only storage discipline that egress records enter
