---
schema: foundry-doc-v1
title: "Browser developer workbench"
slug: app-privategit-workbench
category: applications
type: topic
quality: in-progress
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-05-28
editor: jwoodfine
short_description: "app-privategit-workbench is a browser-based file editor included in the os-privategit host operating system, presenting a three-column interface — file tree, viewer, and editor — for working with plain-text and source files across the cluster archive tree without a terminal session."
paired_with: app-privategit-workbench.es.md
cites: []
---

`app-privategit-workbench` is a browser-based file editor included
in the [[os-privategit|`os-privategit`]] host operating system. It presents a local
HTTP endpoint that serves a single-page application with a
three-column layout: a file tree sidebar, a content viewer, and a
plain-text editor.

The workbench is the primary authoring and review surface for
[[totebox-orchestration|Totebox Orchestration]] operators and Community Members who want
direct browser-based access to their [[totebox-archive|archive tree]] without a terminal
session. It is not a publication surface — it writes to the local
filesystem and relies on the git-based version-control pipeline
for history and promotion.

---

## Architecture

The workbench is a single Rust crate (`app-privategit-workbench`,
Apache 2.0) in the `pointsav-monorepo`. It has two components:

**Write-service (Rust/axum):** An HTTP server that handles file reads
and writes. It binds to a loopback address and is never exposed
directly to external networks. The service enforces root containment
(all paths are canonicalized and checked against declared roots),
an extension allowlist, and mtime-based conflict detection.

**Single-page application:** A self-contained HTML file embedded into
the binary at compile time via `include_str!`. The SPA makes API
calls through an nginx proxy to the write-service for file reads and
writes, and to nginx autoindex routes for directory listings. No
external resources are loaded at runtime.

The binary is compiled for the `os-privategit` host and managed by
a systemd unit. The nginx intranet routes `/_api/edit/*` to the
write-service and serves autoindex JSON at `/_api/command/`,
`/_api/clones/`, and per-sandbox prefixes.

---

## File tree

The sidebar lists the roots declared in `config.toml`. Each root maps
a URL prefix (for example, `_clones/project-development`) to a
filesystem path (for example, `/srv/foundry/clones/project-development`).
Roots may be writable or read-only. The Command workspace root
(`/srv/foundry`) is always read-only; archive roots are writable.

Directory contents are fetched on expand from nginx autoindex JSON.
The tree supports nested expansion to arbitrary depth.

---

## Viewer

The centre column renders the selected file according to its extension:

- **Markdown (`.md`):** Rendered as HTML using a built-in parser.
  Fenced code blocks, inline code, headings, lists, links, and tables
  are supported. Click-to-source from rendered headings and paragraphs
  moves the editor cursor to the corresponding source line.
- **HTML (`.html`):** Displayed in a sandboxed iframe.
- **Images:** Displayed inline.
- **All other types:** Displayed as plain text.

The viewer and editor operate independently. Opening a read-only file
shows the viewer without the editor panel.

---

## Editor

The right column appears when the open file is in a writable root. The
editor is a `<textarea>` with the following features:

- Line number gutter with active-line highlight
- Cursor position indicator (line and column) in the editor bar
- Dirty state indicator (orange dot) when unsaved changes are present
- Save: `Cmd+S` or the Save button — writes via `PUT /file` with the
  current mtime to detect concurrent edits; shows a conflict dialog on
  HTTP 409
- Find / Replace bar (`Cmd+F`): incremental match highlighting, previous
  / next navigation, Replace and Replace All; preserves native undo stack
  via `execCommand`
- Document Outline panel (`Cmd+Shift+O`): lists all markdown headings
  (H1–H6) or TOML table headers from the current file; filter by typing;
  click or press Enter to jump the cursor to that symbol
- Toggle line comment button: extension-aware (`//` for Rust/JS/TS,
  `#` for TOML/YAML/shell); toggles selected lines
- Go to line (`Ctrl+G`)
- Tab inserts two spaces
- Bracket auto-close for `{`, `[`, `(`
- Line move up / down (`Alt+↑` / `Alt+↓`)
- Line duplicate (`Shift+Alt+↓`)

---

## Security model

The write-service enforces four layers of containment aligned with the [[pre-commit-defense-in-depth|pre-commit defence-in-depth]] approach used across the platform:

**Root containment:** Every path is canonicalized with `std::fs::canonicalize`
and verified to remain within the declared root's filesystem path. Paths
that resolve outside the root are rejected with HTTP 400.

**CSRF guard:** Every `PUT /file` request requires the `X-Foundry-Editor: 1`
header. The browser's cross-origin policy prevents third-party pages from
adding this header.

**Extension allowlist:** Writes are permitted only for recognized plain-text
and source-code extensions. Binary formats and unknown extensions are
read-only through the workbench.

**Writable flag:** The `writable = false` declaration in a root entry causes
all write attempts to that root to be rejected with HTTP 403, regardless of
filesystem permissions.

The systemd unit runs with `ProtectSystem=strict` and `ReadWritePaths=`
scoped to the declared writable roots. Adding a new writable root requires
updating both `config.toml` and the systemd service file; missing the
service file update causes silent write failures at the filesystem layer.

---

## Relationship to os-privategit

`app-privategit-workbench` is included in the [[os-privategit|`os-privategit`]] host
operating system alongside `app-privategit-design-system` and
`service-privategit`. It is the authoring surface for operators who
use the privategit tier — a locally-hosted, network-isolated development
environment for [[totebox-orchestration|Totebox Orchestration]] instances. Access to writable roots is governed by the [[machine-based-auth|machine-based authorization]] model.

The crate is licensed under the Apache License, Version 2.0 and intended
for downstream deployment in customer-tier instances of `os-privategit`.
An operational setup guide is available in the customer fleet deployment
catalog.

---

## Planned additions

- **Phase 4 (planned/intended):** CodeMirror 6 integration for syntax
  highlighting; authenticated roots with per-user writable scope.

## See also

- [[os-privategit]] — the host operating system that includes this workbench
- [[totebox-archive]] — the archive tree that operators work with through the workbench
- [[machine-based-auth]] — the authorization model governing writable root access
- [[pre-commit-defense-in-depth]] — the defence-in-depth discipline applied by the write-service
