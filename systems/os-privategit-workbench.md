---
schema: foundry-doc-v1
title: "os-privategit browser workbench"
slug: os-privategit-workbench
short_description: "app-privategit-workbench is a browser-based file editor included in os-privategit that provides a three-column interface for working with archive files without a terminal session."
category: systems
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: os-privategit-workbench.es.md
---

`app-privategit-workbench` is a browser-based file editor included in the [[os-privategit|`os-privategit`]] host operating system. It presents a local HTTP endpoint that serves a single-page application with a three-column layout: a file tree sidebar, a content viewer, and a plain-text editor.

The workbench is the primary authoring and review surface for [[totebox-orchestration|Totebox Orchestration]] operators and Community Members who want direct browser-based access to their [[totebox-archive|archive tree]] without a terminal session. It is not a publication surface — it writes to the local filesystem and relies on the existing commit and promote pipeline for version control.

## Architecture

The workbench is a single Rust crate (`app-privategit-workbench`, Apache 2.0) in `pointsav-monorepo`. It has two components.

**Write-service (Rust/axum):** An HTTP server that handles file reads and writes. It binds to a loopback address and is never exposed directly to external networks. The service enforces root containment, an extension allowlist, and mtime-based conflict detection.

**Single-page application:** A self-contained HTML file embedded into the binary at compile time via `include_str!`. The SPA makes API calls through an nginx proxy to the write-service for file reads and writes, and to nginx autoindex routes for directory listings. No external resources are loaded at runtime.

The binary is compiled for the `os-privategit` host and managed by a systemd unit. The nginx intranet service routes `/_api/edit/*` to the write-service and serves autoindex JSON at configured prefix paths.

## File tree

The sidebar lists the roots declared in `config.toml`. Each root maps a URL prefix to a filesystem path. Roots may be writable or read-only. The Command workspace root is always read-only; archive roots are writable.

Directory contents are fetched on expand from nginx autoindex JSON. The tree supports nested expansion to arbitrary depth.

## Viewer

The center column renders the selected file according to its extension: Markdown files are rendered as HTML using a built-in parser with fenced code blocks, headings, lists, links, and tables; HTML files are displayed in a sandboxed iframe; images are displayed inline; all other types are displayed as plain text.

Click-to-source from rendered headings and paragraphs moves the editor cursor to the corresponding source line.

## Editor

The editor panel appears when the open file is in a writable root. It provides line numbers with active-line highlight, cursor position indicator, dirty state indicator for unsaved changes, save via Cmd+S with mtime-based conflict detection, incremental find/replace, a document outline panel listing all Markdown headings or TOML table headers, line comment toggle, go to line, bracket auto-close, and line move/duplicate operations.

## Security model

The write-service enforces four layers of containment aligned with the [[pre-commit-defense-in-depth|defence-in-depth]] approach used throughout the platform:

**Root containment:** Every path is canonicalized with `std::fs::canonicalize` and verified to remain within the declared root's filesystem path. Paths that resolve outside the root are rejected with HTTP 400.

**CSRF guard:** Every `PUT /file` request requires the `X-Foundry-Editor: 1` header. The browser's cross-origin policy prevents third-party pages from adding this header.

**Extension allowlist:** Writes are permitted only for recognized plain-text and source-code extensions. Binary formats and unknown extensions are read-only through the workbench.

**Writable flag:** The `writable = false` declaration in a root entry causes all write attempts to that root to be rejected with HTTP 403, regardless of filesystem permissions.

The systemd unit runs with `ProtectSystem=strict` and `ReadWritePaths=` scoped to the declared writable roots. Adding a new writable root requires updating both `config.toml` and the systemd service file.

## Relationship to os-privategit

`app-privategit-workbench` is included in the `os-privategit` host operating system alongside `app-privategit-design-system` and `service-privategit`. It is the authoring surface for operators who use the privategit tier — a locally-hosted development environment for Totebox Orchestration instances.

The crate is licensed under the Apache License, Version 2.0 and is intended for downstream deployment in customer-tier instances of `os-privategit`. Operational setup documentation is available in the customer fleet deployment guide.

Phase 4 is planned to integrate CodeMirror 6 for syntax highlighting and to introduce authenticated roots with per-user writable scope.

## See also

- [[os-privategit]] — the host operating system that includes the workbench
- [[totebox-archive]] — the Totebox Archive that operators work with through the workbench
- [[machine-based-auth]] — the authorization model for authenticated workbench roots
- [[os-family-overview]] — the eight-OS family and how os-privategit fits
