---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-input
title: "service-input — Document Ingest"
short_description: "service-input is the Ring 1 document-intake service that accepts files at the per-tenant boundary, routes them through format-specific parsers, and writes normalized output to the per-tenant WORM ledger via service-fs."
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: service-input.es.md
category: services
status: active
quality: complete
last_edited: 2026-06-23
editor: pointsav-engineering
---

`service-input` is the [[three-ring-architecture|Ring 1]] document-intake service in the PointSav system architecture. It accepts files at the per-tenant boundary, routes them through format-specific parsers, and writes the normalized output into the per-tenant [[worm-ledger-design|WORM Immutable Ledger]] via [[service-fs-architecture|`service-fs`]].

## The Anchor position (F12 / SYS-ADR-10)

The Ring 1 boundary is the trust perimeter of the system. Every artifact that crosses this boundary must pass through a deterministic, auditable processing step before it is committed to the WORM ledger. `service-input` occupies that position for structured documents.

[[sys-adr-10|SYS-ADR-10]] designates this position **The Anchor** (function F12): the single, mandatory intake point where document bytes enter Ring 1, undergo deterministic parsing, and are handed off to `service-fs` for permanent append-only storage. Nothing about parsing is delegated to an AI model; nothing about the output schema varies non-deterministically. The same input bytes, on the same parser version, always produce the same `ParsedDocument`.

This is the Anchor property: the document's presence in the WORM ledger is anchored to a reproducible deterministic transformation, not to a probabilistic AI inference.

## Architecture

```
Caller (Ring 2 or operator)
        │
        │  POST /mcp  (JSON-RPC 2.0, X-Foundry-Module-ID header)
        ▼
   MCP handler  (src/mcp.rs)
        │
        │  filename, source_id, bytes_base64
        ▼
   Dispatcher  (src/lib.rs)
        │
        │  detect_format → route to per-format Parser
        ▼
   Parser  (src/pdf.rs | markdown.rs | docx.rs | xlsx.rs)
        │
        │  ParsedDocument { format, source_id, text, metadata }
        ▼
   FsClient  (src/fs_client.rs)
        │
        │  POST /v1/append  (X-Foundry-Module-ID, JSON body)
        ▼
   service-fs  (Ring 1, WORM ledger)
```

The HTTP boundary exposes three endpoints: `GET /healthz`, `GET /readyz`, and `POST /mcp`. The MCP endpoint is the only write surface. There is no read surface in this service; reads happen at `service-fs` via its own MCP resource interface.

## Format detection

Format detection runs before parser dispatch. The `detect_format` function (in `src/lib.rs`) applies two strategies in order.

**Extension-first**: the filename extension is matched against the known set (`.pdf`, `.md` / `.markdown`, `.docx`, `.xlsx`). Extension matching is case-insensitive.

**Magic-byte fallback**: when the extension is absent or unrecognized, the first four bytes of the document are inspected for known magic sequences. PDF documents begin with `%PDF` (hex `25 50 44 46`). DOCX and XLSX documents are ZIP files and share the `PK` header (`50 4B 03 04`); at this fallback level the two formats are ambiguous, so format detection defers to the extension match. A file whose extension is neither `.docx` nor `.xlsx` but whose content is a ZIP archive is reported as `FormatUndetected`.

Format detection returns an `Option<Format>`. A `None` result causes the MCP handler to return a `-32602 Invalid params` error to the caller; the file is not written to the ledger. This detection algorithm is entirely deterministic — no AI inference — per [[sys-adr-07|SYS-ADR-07]].

## Parsers

### PDF — oxidize-pdf 2.x

The `PdfParser` (in `src/pdf.rs`) uses oxidize-pdf 2.x to extract text from PDF documents. The library exposes a file-path API rather than an in-memory reader; to handle this, `PdfParser` writes the input bytes to a uniquely named temporary file under the system temp directory, opens it via oxidize-pdf, extracts the text, and deletes the temporary file via an RAII drop guard. The temporary file is never left on disk after the method returns, even if parsing fails.

`ParsedDocument` produced: `text` is the concatenated text from all pages; `metadata` is `{ "page_count": N, "parser": "oxidize-pdf" }`.

### Markdown — pulldown-cmark 0.12

The `MarkdownParser` (in `src/markdown.rs`) uses pulldown-cmark 0.12. Unlike the PDF parser, Markdown parsing operates on the in-memory byte slice directly — no temporary file is needed. The parser collects all `Text` and `Code` events, strips HTML tags from the event sequence, and concatenates the results. Heading text is collected separately and returned in metadata.

`ParsedDocument` produced: `text` is all visible text content; `metadata` is `{ "headings": ["Heading 1", "Heading 2", ...], "parser": "pulldown-cmark" }`.

### DOCX — docx-rust 0.1.x

The `DocxParser` (in `src/docx.rs`) uses docx-rust 0.1.x to extract paragraph text from Word Open XML (DOCX) documents. DOCX files are ZIP archives; the parser first confirms the magic-byte signature (`PK\x03\x04`) before attempting extraction. If the bytes do not match, `FormatMismatch` is returned immediately without attempting ZIP extraction, guarding against mistaken dispatch of non-DOCX ZIP files.

`ParsedDocument` produced: `text` is paragraph text concatenated with newline separators; `metadata` is `{ "paragraph_count": N, "parser": "docx-rust" }`.

### XLSX — calamine 0.34

The `XlsxParser` (in `src/xlsx.rs`) uses calamine 0.34. Like DOCX, XLSX files are ZIP archives and receive the same magic-byte guard. The parser opens the workbook from an in-memory `Cursor` (no temporary file), iterates all sheets, and serializes all rows as tab-separated columns. Sheet boundaries are separated by newlines in the output text.

`ParsedDocument` produced: `text` is tab-separated cell values, one row per line, all sheets concatenated; `metadata` is `{ "sheet_count": N, "sheets": ["Sheet1", ...], "parser": "calamine" }`.

## Dispatcher

The `Dispatcher` (in `src/lib.rs`) is a per-format registry of `Box<dyn Parser + Send + Sync>` instances. It is constructed at daemon startup with the four supported parsers registered via a builder API:

```
Dispatcher::new()
    .with_pdf(Box::new(PdfParser))
    .with_markdown(Box::new(MarkdownParser))
    .with_docx(Box::new(DocxParser))
    .with_xlsx(Box::new(XlsxParser))
```

Two dispatch methods are available:

- `dispatch(format, source_id, bytes)` — caller has already identified the format. Returns `ParseError::UnsupportedFormat` if no parser is registered for the given format.
- `dispatch_with_detection(filename, bytes)` — runs format detection internally, then dispatches. Convenience wrapper for callers that have not yet run detection.

The `Parser` trait is object-safe:

```rust
pub trait Parser: Send + Sync {
    fn parse(&self, source_id: &str, bytes: &[u8]) -> Result<ParsedDocument, ParseError>;
}
```

## ParsedDocument

All four parsers return a normalized `ParsedDocument`:

```rust
pub struct ParsedDocument {
    pub format: Format,
    pub source_id: String,
    pub text: String,
    pub metadata: serde_json::Value,
}
```

- `format`: one of `Format::{Pdf, Markdown, Docx, Xlsx}`
- `source_id`: passed through from the caller (the ledger `payload_id`)
- `text`: extracted text content; format-specific encoding (see parser sections above)
- `metadata`: JSON object with parser-specific fields; always includes `"parser"` key

The `ParsedDocument` type derives `Serialize`. The FsClient wraps it as the `payload` field in the service-fs append request.

## FsClient

`FsClient` (in `src/fs_client.rs`) submits `ParsedDocument` records to `service-fs`'s `/v1/append` endpoint.

Wire format:

```json
POST /v1/append
X-Foundry-Module-ID: <module_id>
Content-Type: application/json

{
  "payload_id": "<doc.source_id>",
  "payload": { ...ParsedDocument... }
}
```

The `X-Foundry-Module-ID` header identifies the per-tenant caller. The service-fs server validates this header against its own `FS_MODULE_ID` configuration and returns HTTP 403 if the values do not match. This is the per-tenant boundary enforcement at the WORM ledger layer.

`FsClient::submit` returns the `cursor: u64` assigned by service-fs — a monotonically increasing integer that serves as the stable reference for this ledger entry. The cursor is returned to the MCP caller in the tool response. `FsClient` uses ureq 3.x for blocking HTTP I/O; the blocking call is acceptable at Ring 1 boundary-ingest throughput where one document is processed per MCP call.

## MCP interface

**Endpoint:**

```
POST /mcp
Content-Type: application/json
X-Foundry-Module-ID: <module_id>
```

**Protocol:** JSON-RPC 2.0 (Streamable HTTP transport — single JSON response per request).

### document.ingest

Detect the document format, parse the bytes, and write the parsed document into service-fs's WORM ledger.

**Input schema:**

| Field | Type | Required | Description |
|---|---|---|---|
| `filename` | string | Yes | Original filename; used for format detection (extension-first, magic-byte fallback) |
| `source_id` | string | Yes | Caller-side document identifier; forwarded as the ledger `payload_id` |
| `bytes_base64` | string | Yes | Base64-encoded document bytes (standard encoding) |

**Success response:**

```json
{
  "content": [{"type": "text", "text": "{\"cursor\": 42, \"source_id\": \"doc-001\", \"format\": \"Pdf\"}"}],
  "isError": false
}
```

**Error responses:**

- `-32602 Invalid params`: format undetected, base64 decode failure, or missing arguments
- `-32603 Internal error`: parser failure or service-fs transport error

### Per-tenant boundary

All MCP requests require the `X-Foundry-Module-ID` header. The header value must match the module ID the daemon was started with (`INPUT_MODULE_ID`). A mismatch or absent header returns a `-32600 Invalid request` JSON-RPC error. This enforcement is at the MCP handler layer, before any parsing or ledger write is attempted.

## ADR-07 compliance

[[sys-adr-07|SYS-ADR-07]] prohibits AI inference in Ring 1. `service-input` maintains this constraint throughout:

- **Format detection** is deterministic: extension matching followed by magic-byte inspection. No trained classifier.
- **Parsing** is done by purpose-built libraries (oxidize-pdf, pulldown-cmark, docx-rust, calamine) that apply deterministic algorithms to structured byte sequences. No generative model is involved at any stage.
- **Text normalization** is purely structural: whitespace joining, event-stream text extraction, cell serialization. No semantic processing.

A consequence of this constraint is that `service-input` does not attempt to extract meaning from the parsed text. The `text` field of `ParsedDocument` is a faithful, deterministic extraction of the document's textual content. Semantic interpretation is the responsibility of [[service-extraction|Ring 2]] (`service-extraction`).

## Deployment configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `INPUT_MODULE_ID` | Yes | — | Per-tenant module identifier; must match `FS_MODULE_ID` on the service-fs instance |
| `INPUT_FS_URL` | Yes | — | service-fs base URL (e.g., `http://127.0.0.1:9100`) |
| `INPUT_BIND_ADDR` | No | `0.0.0.0:9200` | Address and port the MCP HTTP server binds to |

The binary is a single-process Tokio daemon. It starts the axum HTTP server and serves incoming MCP requests until terminated.

## Relations to other Ring 1 services

`service-input` is one of four Ring 1 boundary-ingest services. Each addresses a distinct document intake channel:

| Service | Input channel | Output |
|---|---|---|
| `service-input` | Generic documents (PDF, DOCX, XLSX, Markdown) | `ParsedDocument` → WORM ledger |
| [[service-email]] | Microsoft Exchange mailboxes (EWS SOAP) | Raw MIME → WORM ledger |
| [[service-people]] | Identity records | `Person` record → WORM ledger |
| `service-fs` | WORM ledger itself | Provides `/v1/append` and `/v1/entries` |

All four write through `service-fs`. [[service-extraction]] (Ring 2) reads from `service-fs` and applies AI-assisted analysis downstream, outside the Ring 1 boundary.

## See also

- [[fs-anchor-emitter]] — the WORM ledger anchoring service
- [[three-ring-architecture]] — Ring 1 boundary placement and service-input's role
- [[worm-ledger-design]] — WORM ledger architecture and append semantics
- [[service-fs-architecture]] — service-fs MCP resource interface
