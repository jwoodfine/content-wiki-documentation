---
schema: foundry-doc-v1
title: "The Input Machine"
slug: input-machine
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: input-machine.es.md
short_description: "The Input Machine is the mandatory ingest boundary for all documents entering os-console workflows, permanently assigned to F12 and implemented by service-input on the Totebox Archive — every workflow's source material passes through this single, auditable gate."
cites: []
references: []
---

Every document management system must answer a foundational question: when a document arrives in a workflow, how did it get there? In most systems, the answer is distributed and implicit — files appear in folders, are attached to emails, are uploaded through web forms, and the system reconstructs the ingest chain after the fact when compliance requires it.

The Input Machine inverts this design. A single, permanently-fixed gateway handles all document ingest. Every document that enters an os-console workflow passes through it. Every passage is logged. The question of how a document entered the system has one answer: through F12, at a specific time, with an explicit operator confirmation.

## The Anchor: F12 as mandatory ingest gate

F12 is permanently assigned to the Input Machine in os-console. This assignment is architectural, not configurational — it cannot be changed by the operator or overridden by another cartridge. F12 occupies the boundary position on the keyboard's function-key row, physically separated from F1–F11 by a wider gap on most keyboard layouts. The position is intentional: the ingest gate must be immediately and unambiguously findable in any workflow state, by any operator, at any moment.

The constraint that F12 is immovable is recorded in [[sys-adr-10]]. No workflow may bypass the Input Machine to submit a document to a backend service through another path. This constraint is enforced in the `app-console-keys` event dispatcher at the chassis level, not by convention in individual cartridges.

## The ingest workflow

Pressing F12 in any os-console context — regardless of which cartridge is currently active — triggers the Input Machine modal. The active cartridge suspends. The operator completes the ingest workflow:

1. The file path input field opens.
2. The operator provides the path and confirms explicitly — passive or accidental submission is not accepted.
3. The Input Machine validates that the file exists and is readable.
4. The validated file is transmitted to `service-input` on the Totebox Archive.
5. `service-input` classifies the document using deterministic rules, without AI inference.
6. `service-input` routes the document to the appropriate backend service.
7. An immutable audit entry is written: timestamp, file path, classification result, routing target, operator identity.
8. The previously-active cartridge resumes, with the ingested document available in its context.

Step 5 applies the constraint from [[sys-adr-07]]: no structured data passes through AI inference at the ingest boundary. Classification is deterministic — file extension, MIME type, and structural signatures determine document type. The classification result in the audit log is reproducible: given the same file, `service-input` produces the same classification regardless of model availability.

## The Zero-Form architecture

The Input Machine implements a design principle called Zero-Form architecture. In conventional workflows, documents enter systems through forms: the operator fills in metadata fields to contextualize a document before it enters a processing pipeline. Zero-Form inverts this. The operator provides a document. The system classifies it, determines the processing target, and generates the contextualizing metadata automatically. The only manual input required is the document itself and an explicit confirmation of intent to submit.

This is not a convenience feature. The architectural value is compliance precision: the audit trail reflects a deliberate human decision for every document. No document enters a workflow through habit, automation, or accident. The operator's explicit confirmation is the event that the audit log records.

## service-input: the boundary ingest service

`service-input` is the server-side counterpart of the Input Machine on the Totebox Archive. It is a boundary ingest service — a distinct, per-tenant process that handles all document ingest for one archive. Each Totebox Archive runs its own `service-input` instance; there is no shared ingest service across archives.

`service-input` performs three functions:

**Classification.** Deterministic document-type identification using file extension, MIME type, and structural signatures. No AI inference at this stage — the classification rule is encoded in the service, not delegated to a language model.

**Routing.** Dispatch to the appropriate backend service based on classification: editorial content to the proofreading service, archival material to `service-fs`, governance documents to the governance workflow. The routing decision belongs to `service-input`; the operator does not specify the destination.

**Audit.** An immutable log entry written at the moment of ingest, capturing the full context of the event: what was submitted, when, how it was classified, and where it was routed.

## The audit trail

Every document that passes through the Input Machine produces two log entries. A local log on the operator's machine captures the ingest event immediately, persisting even if the Totebox Archive is temporarily unreachable. The `service-input` ledger on the archive is the canonical record, written once the transmission completes.

The dual record is a resilience property: if a network interruption occurs mid-ingest, the local log preserves evidence of the attempt; the canonical ledger confirms the delivery.

## Per-cartridge routing

Each cartridge uses the Input Machine for its source material, but the routing decision belongs to `service-input`, not to the active cartridge. An operator in the F4 editorial cartridge and an operator in the F7 building-information cartridge both press F12 to submit material. `service-input` routes to the proofreading service or the BIM service based on what was submitted — not based on which cartridge was active when F12 was pressed. The Input Machine is a shared gateway; classification determines destination.

## See also

- [[os-console-platform]] — the platform context and cartridge architecture within which the Input Machine operates
- [[machine-based-auth]] — the authorization mechanism connecting os-console to service-input on the Totebox Archive
- [[sys-adr-10]] — the architectural decision record establishing F12 as the mandatory ingest checkpoint
- [[sys-adr-07]] — the architectural decision record prohibiting AI inference on structured data at the ingest boundary
