---
schema: foundry-doc-v1
title: "Input machine"
slug: input-machine
aliases:
  - input-machine
short_description: "The Input Machine is the mandatory document ingest gate in os-console, bound permanently to F12 and backed by service-input on the Totebox Archive."
category: systems
type: topic
content_type: topic
index_group: operator-surfaces
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: input-machine.es.md
---

The Input Machine is the mandatory ingest gate through which all documents and text enter [[os-console|os-console]] workflows. It occupies the F12 key slot permanently across all keyboard configurations. Every [[os-console|cartridge]] in os-console depends on the Input Machine for its source material. No workflow bypasses it.

## Why the position is permanent

F12 occupies the boundary position on the function-key row, physically separated from F1–F11 by a wider gap on most keyboards. This positioning is deliberate. The Input Machine is not a workflow feature; it is a boundary control. It must be immediately and unambiguously locatable regardless of which cartridge is currently active.

System architecture decision SYS-ADR-10 establishes F12 as the mandatory human checkpoint for all ingest operations. The assignment cannot be bypassed by another pane and cannot be remapped. These constraints are enforced in the [[app-console-keys|`app-console-keys`]] event dispatcher rather than by convention.

## What happens when F12 is pressed

Pressing F12 at any point in os-console suspends the currently-active cartridge and opens the Input Machine modal. The operator completes the ingest workflow. The cartridge then resumes.

The ingest workflow runs as follows:

1. A modal presents the file path input field.
2. The operator enters and confirms the path. Passive submission is not accepted — explicit confirmation is required.
3. `app-console-input` posts the path, submitting username, and tenant to `service-input`'s `/v1/append` endpoint on the Totebox Archive.
4. `service-input` reads the file, hashes it, and skips it if that hash has already been processed. New files are tagged with a coarse target label — `service-research` or `service-minutebook` if the path contains that string, `service-content` otherwise — and forwarded to `service-fs` under that label.
5. `service-input` writes its own ledger entry (payload ID, path, hash, timestamp, target label) and `app-console-input` writes a local record (timestamp, operator, tenant, path, status).
6. The active cartridge resumes with the ingested document available in its context.

## service-input: the ingest boundary service

`service-input` is the server-side counterpart of the Input Machine cartridge, running on the Totebox Archive. It reads a document once, deduplicates it by content hash, and forwards it to [[service-fs|service-fs]] under a coarse label. It does not classify document type, and it does not route to different downstream services by content — every non-duplicate file ends up in `service-fs`, distinguished only by its label, with no separate path to `service-proofreader`, a BIM-specific handler, or any other content-aware destination.

`service-input` performs no AI inference — the label assignment is a plain substring check on the file path, not a MIME-type or structural-signature classifier. This keeps the ingest step reproducible and independent of model availability, consistent with SYS-ADR-07.

## The audit trail

Every document that passes through the Input Machine generates two records.

A local SQLite log on the os-console machine records the timestamp, operator, tenant, file path, and a status field. This local record persists even if the [[totebox-archive|Totebox Archive]] is unreachable.

A separate ledger entry on `service-input` itself records the payload ID, file path, content hash, timestamp, and the target label assigned. Together these two records establish when a document arrived, who submitted it, and where it was forwarded — but neither one records a content classification, since none is performed.

## The app-console-input cartridge

`app-console-input` is the F12 cartridge crate in `pointsav-monorepo`. It implements the Input Machine workflow on the os-console client side: it renders the file path input modal, sends the POST to `service-input` with a 30-second timeout, and writes the local SQLite audit entry. Control returns to the previously-active cartridge once ingest completes.

`app-console-input` is always installed and the modal is always reachable via F12. This is not configurable.

## ADR-07 compliance

SYS-ADR-07 states that no structured data passes through AI inference. The Input Machine enforces this at the ingest boundary — `service-input`'s label assignment is a plain, deterministic substring check on the file path, not a model call. Given the same file, `service-input` always produces the same label, and the audit record never depends on model versions or inference availability.

## The Zero-Form architecture

The Input Machine is the foundation of what operational documentation describes as the Zero-Form architecture. Traditional document workflows require forms — the operator fills in fields to contextualize a document before it enters a system. The Input Machine inverts this: the operator provides a document and confirms intent, and the system logs, labels, and forwards it without further data entry. The only input required is the document itself and an explicit confirmation of intent to submit.

Explicit confirmation is a compliance design choice. It means the audit trail reflects a deliberate human decision, not an accidental submission.

## Resumption after ingest

Every cartridge uses the same Input Machine for its source material, and F12 always returns control to whichever cartridge was active when it was pressed. It is the active cartridge, not the assigned target label, that determines what happens to the document next. The target label `service-input` assigns is independent of which F-key opened the modal — it reflects only where the file's path text matched, not which cartridge submitted it.

## See also

- [[os-console]] — the platform context for the Input Machine
- [[machine-based-auth]] — the authorization mechanism os-console uses
- [[three-ring-architecture]] — service-input Ring 1 placement
- [[os-console]] — the cartridge architecture and F-key map
- [[worm-ledger-design]] — the append-only ledger discipline for audit records
