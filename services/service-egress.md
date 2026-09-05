---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-egress
short_description: "service-egress compresses and chunks local mail data for outbound transfer, and only deletes the local source once an external counterpart confirms receipt with a cryptographic proof — an outbound release valve, not a cloud-to-local import."
title: "Egress service"
category: services
index_group: ring-2-knowledge-and-processing
quality: stub
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
paired_with: service-egress.es.md
status: stub
last_edited: 2026-09-05
editor: pointsav-engineering
---

`service-egress` moves local mail data outward — the reverse of what its name might suggest at first glance. It doesn't pull anything in from the cloud; it stages local data for outbound transfer and only removes the local copy once it has proof the transfer succeeded.

## The loop

Running continuously, the service repeats two steps:

1. **Stage.** Any local mail file not yet staged is compressed and split into fixed-size chunks in an outbound queue, ready for an external counterpart process to pick up.
2. **Wipe on receipt.** When that external process confirms it has received a transfer — a cryptographic receipt, not a simple acknowledgement — `service-egress` deletes both the original local file and its staged chunks. Nothing is removed until that receipt exists.

## Why the ordering matters

This ordering means data loss during a transfer is impossible on this service's side: the local original stays in place through staging and transfer, and disappears only after independent confirmation that the outbound copy landed. A crash mid-transfer simply leaves the local original and its staged chunks both present for the next cycle to pick back up.

This service has no IMAP or object-store client, and never calls into the [[worm-ledger-design|WORM ledger]] interface — the WORM ledger's append-only guarantees are real elsewhere in the platform, just not part of this particular service.

## See also

- [[service-email]] — the mail ingestion service whose local Maildir this service stages for outbound transfer
