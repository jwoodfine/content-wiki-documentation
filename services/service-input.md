---
schema: foundry-doc-v1
title: "service-input"
slug: service-input
short_description: "service-input is the Ring 1 document ingest service that accepts files at the per-tenant boundary, routes them through format-specific parsers, and writes normalized output to the WORM ledger via service-fs."
category: services
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: service-input.es.md
---

`service-input` is the [[three-ring-architecture|Ring 1]] document-intake service in the PointSav system architecture. It accepts files at the per-tenant boundary, routes them through format-specific parsers, and writes the normalized output into the per-tenant [[worm-ledger-design|WORM Immutable Ledger]] via [[service-fs-architecture|`service-fs`]].

## The Anchor position

The Ring 1 boundary is the trust perimeter of the system. Every artifact that crosses this boundary must pass through a deterministic, auditable processing step before it is committed to the WORM ledger. `service-input` occupies that position for structured documents.

[[architecture-decisions|SYS-ADR-10]] designates this position The Anchor (function F12 on [[os-console-platform|`os-console`]]): the single, mandatory intake point where document bytes enter Ring 1, undergo deterministic parsing, and are handed off to `service-fs` for permanent append-only storage. Nothing about parsing is delegated to an AI model; nothing about the output schema varies non-deterministically. The same input bytes, on the same parser version, always produce the same `ParsedDocument`.

This is the Anchor property: the document's presence in the WORM ledger is anchored to a reproducible deterministic transformation, not to a probabilistic AI inference.

## Architecture

The service is structured as an [[mcp-substrate-protocol|MCP]] handler that receives document bytes via `POST /mcp`, dispatches them through a format detector and per-format parser, and forwards the parsed result to `service-fs` via its FsClient. The HTTP boundary exposes three endpoints: `GET /healthz`, `GET /readyz`, and `POST /mcp`. The MCP endpoint is the only write surface. There is no read surface in this service; reads happen at `service-fs` via its own MCP resource interface.

## Format detection

Format detection runs before parser dispatch. The `detect_format` function applies two strategies in order.

Extension-first matching checks the filename extension against the known set: `.pdf`, `.md` or `.markdown`, `.docx`, `.xlsx`. Extension matching is case-insensitive.

Magic-byte fallback: when the extension is absent or unrecognized, the first four bytes of the document are inspected for known magic sequences. PDF documents begin with `%PDF` (hex `25 50 44 46`). DOCX and XLSX documents are ZIP files sharing the `PK` header (`50 4B 03 04`).

Format detection returns an `Option<Format>`. A `None` result causes the MCP handler to return a `-32602 Invalid params` error to the caller; the file is not written to the ledger. This detection algorithm is entirely deterministic — no AI inference — per SYS-ADR-07.

## Parsers

Four format-specific parsers are registered at daemon startup:

**PDF** — uses oxidize-pdf 2.x. Writes the input bytes to a temporary file, opens it via oxidize-pdf, extracts all page text, and deletes the temporary file via an RAII drop guard. The temporary file is never left on disk after the method returns.

**Markdown** — uses pulldown-cmark 0.12. Operates on the in-memory byte slice directly. Collects all `Text` and `Code` events from the pulldown-cmark event stream, strips HTML tags, and concatenates results.

**DOCX** — uses docx-rust 0.1.x. Confirms the magic-byte signature before attempting ZIP extraction. Extracts paragraph text with newline separators.

**XLSX** — uses calamine 0.34. Opens the workbook from an in-memory `Cursor`, iterates all sheets, and serializes all rows as tab-separated columns.

All four parsers return a normalized `ParsedDocument` with a `format` field, a `source_id` passed through from the caller, `text` as extracted text content, and a `metadata` JSON object including a `"parser"` key.

## MCP interface

The MCP endpoint accepts JSON-RPC 2.0 requests via `POST /mcp` with a required `X-Foundry-Module-ID` header. The `document.ingest` tool accepts `filename` (used for format detection), `source_id` (the caller-side document identifier), and `bytes_base64` (base64-encoded document bytes).

On success, the response includes the `cursor` — a monotonically increasing integer assigned by service-fs — as the stable ledger reference for this entry. On error, `-32602 Invalid params` indicates a format detection failure, and `-32603 Internal error` indicates a parser failure or service-fs transport error.

## ADR-07 compliance

[[architecture-decisions|ADR-07]] prohibits AI inference in Ring 1. `service-input` maintains this constraint throughout: format detection uses extension matching followed by magic-byte inspection; parsing uses purpose-built libraries that apply deterministic algorithms; text normalization is purely structural. A consequence of this constraint is that `service-input` does not attempt to extract meaning from the parsed text. Semantic interpretation is the responsibility of [[service-extraction|Ring 2 services]] downstream.

## Deployment configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `INPUT_MODULE_ID` | Yes | — | Per-tenant module identifier; must match `FS_MODULE_ID` on the service-fs instance |
| `INPUT_FS_URL` | Yes | — | service-fs base URL |
| `INPUT_BIND_ADDR` | No | `0.0.0.0:9200` | Address and port the MCP HTTP server binds to |

## Relations to other Ring 1 services

`service-input` is one of four Ring 1 boundary-ingest services. Each addresses a distinct document intake channel: `service-input` handles generic documents (PDF, DOCX, XLSX, Markdown); [[service-email]] handles Microsoft Exchange mailboxes; [[service-people]] handles identity records; and `service-fs` is the WORM ledger itself that all three write through. [[service-extraction]] in Ring 2 reads from `service-fs` and applies AI-assisted analysis downstream, outside the Ring 1 boundary.

## See also

- [[fs-anchor-emitter]] — the WORM ledger anchoring service
- [[three-ring-architecture]] — Ring 1 boundary placement and service-input's role
- [[input-machine]] — the F12 client-side interface to service-input
