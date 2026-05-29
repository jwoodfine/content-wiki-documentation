---
schema: foundry-doc-v1
title: "The Input Machine"
slug: input-machine
short_description: "The Input Machine is the mandatory document ingest gate in os-console, bound permanently to F12 and backed by service-input on the Totebox Archive."
category: systems
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: input-machine.es.md
---

The Input Machine is the mandatory ingest gate through which all documents and text enter [[console-os|os-console]] workflows. It occupies the F12 key slot permanently across all keyboard configurations. Every [[os-console-platform|cartridge]] in os-console depends on the Input Machine for its source material. No workflow bypasses it.

## Why the position is permanent

F12 occupies the boundary position on the function-key row, physically separated from F1–F11 by a wider gap on most keyboards. This positioning is deliberate. The Input Machine is not a workflow feature; it is a boundary control. It must be immediately and unambiguously locatable regardless of which cartridge is currently active.

System architecture decision SYS-ADR-10 establishes F12 as the mandatory human checkpoint for all ingest operations. The assignment cannot be bypassed by another pane and cannot be remapped. These constraints are enforced in the [[app-console-input|`app-console-keys`]] event dispatcher rather than by convention.

## What happens when F12 is pressed

Pressing F12 at any point in os-console suspends the currently-active cartridge and opens the Input Machine modal. The operator completes the ingest workflow. The cartridge then resumes.

The ingest workflow runs as follows:

1. A modal presents the file path input field.
2. The operator enters and confirms the path. Passive submission is not accepted — explicit confirmation is required.
3. The Input Machine validates that the file exists and is readable.
4. The validated file is sent to `service-input` on the Totebox Archive.
5. `service-input` classifies the document and determines the routing target.
6. `service-input` routes the document to the appropriate service — for example, to `service-proofreader` for editorial content or to `service-fs` for archiving.
7. An immutable audit log entry is written: timestamp, file path, classification, routing target, and operator identity.
8. The active cartridge resumes with the ingested document available in its context.

## service-input: the Ring 1 boundary service

`service-input` is a Ring 1 service in the [[three-ring-architecture|Three-Ring Architecture]] — a per-tenant boundary ingest service that handles generic document ingestion. It is the server-side counterpart of the Input Machine cartridge.

Ring 1 placement means `service-input` is per-tenant, a data-ingest boundary through which data flows in but never out, and an [[mcp-substrate-protocol|MCP server]] implementing the Model Context Protocol boundary.

`service-input` performs three functions: classify the document type and appropriate processing pipeline; route the document to the correct Ring 2 or Ring 1 service; and write an immutable record of the ingest event to the ledger.

`service-input` performs no AI inference. Classification uses deterministic rules per SYS-ADR-07, which states that structured data does not pass through AI inference. This ensures the audit trail is reproducible and not dependent on model availability.

## The audit trail

Every document that passes through the Input Machine generates two audit trail entries.

A local SQLite log on the os-console machine records the timestamp, file path, classification, and routing target. This local record persists even if the [[totebox-archive|Totebox Archive]] is unreachable.

A canonical record in the `service-input` ledger on the Totebox Archive is written as an immutable append. Together these entries ensure that every document that entered a workflow is logged with when it arrived, how it was classified, where it was sent, and who submitted it. This dual-entry approach mirrors the [[worm-ledger-design|WORM ledger discipline]] used across the platform.

## The app-console-input cartridge

`app-console-input` is the F12 cartridge crate in `pointsav-monorepo`. It implements the Input Machine workflow on the os-console client side: it renders the file path input modal, sends the POST to `service-input` on the Totebox Archive with a 30-second timeout, writes the local SQLite audit entry, and returns control to the previously-active cartridge after ingest completes.

`app-console-input` is always installed and the modal is always reachable via F12. This is not configurable.

## ADR-07 compliance

SYS-ADR-07 states that no structured data passes through AI inference. The Input Machine enforces this at the ingest boundary. `service-input`'s classification is deterministic — it uses file extension, MIME type, and structural signatures. Given the same file, `service-input` always produces the same classification. The audit record is not dependent on model versions or inference availability.

## The Zero-Form architecture

The Input Machine is the foundation of what operational documentation describes as the Zero-Form architecture. Traditional document workflows require forms — the operator fills in fields to contextualize a document before it enters a system. The Input Machine inverts this: the operator provides a document and the system classifies, routes, and contextualizes it automatically. The only input required is the document itself and an explicit confirmation of intent to submit.

Explicit confirmation is a compliance design choice. It means the audit trail reflects a deliberate human decision, not an accidental submission.

## Routing across cartridges

Each cartridge uses the Input Machine for its source material. The routing decision — which cartridge receives the document after ingest — is made by `service-input` based on classification, not by which cartridge was active when F12 was pressed.

- F4 (Content): submitted documents become the source text for proofreading or draft generation.
- F5 (Minutebook): meeting notes and resolution documents are processed by the governance workflow.
- F6 (Bookkeeper): financial documents enter the ledger pipeline.
- F7 (BIM): IFC model files are routed to `service-bim`.

## See also

- [[console-os]] — the platform context for the Input Machine
- [[machine-based-auth]] — the authorization mechanism os-console uses
- [[three-ring-architecture]] — service-input Ring 1 placement
- [[os-console-platform]] — the cartridge architecture and F-key map
- [[worm-ledger-design]] — the append-only ledger discipline for audit records
