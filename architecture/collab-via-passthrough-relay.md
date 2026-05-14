---
schema: foundry-doc-v1
title: "Real-time collaboration via passthrough relay"
slug: collab-via-passthrough-relay
category: architecture
type: topic
quality: complete
short_description: "The passthrough relay pattern for real-time collaborative editing: the server holds no document state, git remains the sole canonical record, and CRDT state is session-ephemeral by construction — as implemented in app-mediakit-knowledge's collab feature."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: collab-via-passthrough-relay.es.md
references:
  - id: 1
    text: "Yjs — Conflict-free replicated data type library for collaborative applications."
    url: "https://github.com/yjs/yjs"
  - id: 2
    text: "y-codemirror.next — Yjs binding for CodeMirror 6."
    url: "https://codemirror.net/"
  - id: 3
    text: "tokio::sync::broadcast — Tokio multi-producer multi-consumer channel documentation."
    url: "https://docs.rs/tokio/latest/tokio/sync/broadcast/"
---

The passthrough relay pattern inverts the normal assumption about where a collaborative editing server sits in the authority chain: the relay holds no document state at all, so the canonical git tree remains the sole authoritative record of every article's content at every point in time. Concurrent editors connect over WebSocket to a `tokio::sync::broadcast` channel keyed by slug — one broadcast room per document — and the server's only job is to forward Yjs CRDT update messages between those clients.[^1] The server neither decodes nor stores the document state those messages encode. The sole persistence boundary in the entire system is the `POST /edit/{slug}` atomic-write path, which is unchanged from the single-author case: when an editor saves, the client serialises its local Yjs document to Markdown, sends it over HTTP, and the server atomically renames the new file into place on disk — exactly the same operation as a non-collab save.

## Why a passthrough relay rather than a CRDT server

Tools such as Etherpad and HackMD operate on a server-authoritative document model: the collaborative editing server holds a live, mutable document object — an Operational Transformation log in Etherpad's case, a Y.Doc in HackMD's — and that object is the primary record of current content. A git export is a snapshot taken from that server record, not the other way around. The consequence is a permanent second authoritative state: two places in the system hold an answer to the question "what is the current text of this document," and they can drift apart if the export mechanism fails, the server crashes before a save, or the OT/CRDT log diverges from the git history due to a merge edge case.

The passthrough design eliminates that second record entirely. The server is a message conduit, not a store. When a Yjs client sends a binary update message to `GET /ws/collab/{slug}`, the Rust handler receives the raw bytes from the WebSocket and broadcasts them to all other clients in the same slug room via `tokio::sync::broadcast`.[^3] The server never deserialises the Yjs protocol; it never constructs a Y.Doc; it never writes anything to disk as a side effect of a relay operation. The only state of the document the server knows is whatever the client sends through `POST /edit` — the HTTP save path.

This matters for the disclosure posture. The canonical disclosure record in this system is the git tree: every article's content history is a sequence of signed commits, and that sequence is what a regulatory audit produces. A server-authoritative CRDT store would exist in parallel with that sequence, would not be signed, and would represent content states that never appeared in git. Under the passthrough design, no such parallel record exists: in-flight CRDT state is definitionally not part of the disclosure record because it is never written anywhere. The record closes at `POST /edit` time.

The 256-message lag buffer configured on each `tokio::sync::broadcast` channel addresses the one race this design must handle: a client that joins a collab session after other editors have already made changes will not have received those earlier Yjs update messages. Because Yjs CRDTs are convergent, a client that receives all prior update messages in any order will arrive at the same document state. The 256-message buffer ensures a late joiner can catch up on recent activity without the server needing to materialise or store the full document state. If the buffer fills before a late joiner connects, Yjs's sync protocol handles the gap through its awareness and state-vector exchange mechanism on connection open — the server's job remains forwarding, not resolving.

## Implementation in app-mediakit-knowledge

The collab relay shipped in commit `05f1dab` as `src/collab.rs`, gated entirely behind the `--enable-collab` CLI flag. When the flag is absent — which is the default and the current production posture as of v0.1.29 — the WebSocket route `GET /ws/collab/{slug}` is not registered in the axum router, the `window.WIKI_COLLAB_ENABLED` template variable is set to `false`, and the client-side JavaScript bundle never loads. Zero collab code paths execute in the default-off configuration.

The server-side relay is implemented using `tokio::sync::broadcast`, the standard Tokio multi-producer multi-consumer channel. Each slug gets its own broadcast channel with a buffer capacity of 256 messages, created on first connection and stored in a `DashMap<String, broadcast::Sender<Bytes>>` held in `AppState`. When a WebSocket client sends a Yjs update message, the handler reads the raw bytes and calls `sender.send(bytes)` — a single line that fans the message out to all other receivers on that channel. There is no `yrs` crate dependency: the `yrs` Rust port of Yjs was specified in the original Step 7 brief but was not used in the as-shipped implementation. The server relays raw Yjs binary protocol messages without deserialising them, which means the server carries no document state at any point.

The WebSocket upgrade uses axum's built-in WS support (`axum::extract::ws`). The route handler upgrades the HTTP connection, spawns a task per client that loops on incoming WebSocket frames and rebroadcasts each, and removes the client from the room's receiver set on disconnect. If the last client disconnects, the broadcast channel's receiver count drops to zero; the `DashMap` entry persists but holds an empty channel, ready for the next connection. No disk write occurs on last-client-disconnect — a deliberate departure from the original Phase 2 plan, which called for snapshotting the Y.Doc to disk on last disconnect. The passthrough design makes that snapshot impossible because the server never holds the Y.Doc.

The client bundle `cm-collab.bundle.js` (approximately 302 KB as shipped) is built from three npm packages vendored in `vendor-js/`: `yjs`, `y-codemirror.next`[^2], and `y-websocket`. The bundle is committed to `static/vendor/` as a pre-built artefact, so no npm toolchain is required at runtime or in the Rust build path. The `static/saa-init.js` initialisation script checks `window.WIKI_COLLAB_ENABLED` at load time; if the flag is `false`, the import of `cm-collab.bundle.js` is never executed. The CodeMirror editor loads fully in either case — collab is additive to the editing surface, not a prerequisite.

The `src/server.rs` template layer injects the flag: when `--enable-collab` is set, the HTML template for `/edit/{slug}` includes `<script>window.WIKI_COLLAB_ENABLED = true;</script>` immediately before the editor initialisation script tag. When the flag is absent, that script tag is omitted entirely rather than set to `false` — preventing the JavaScript engine from evaluating the collab code path during bundle parse.

Test coverage at commit `05f1dab` added 7 tests (3 unit, 4 integration) to bring the total from 90 to 97. The unit tests cover: the WebSocket route accepts a connection when `--enable-collab` is set; broadcast rooms multiplex correctly across two clients on the same slug; the 256-message buffer drains to completion without panic; and the client bundle loads (HTTP 200 for `cm-collab.bundle.js`) only when the flag is set. The integration tests cover flag-gated script-injection behaviour in rendered HTML. The suite does not cover the visual cursor-presence property — that requires a two-client browser smoke with DOM inspection, documented separately as a manual verification step.

## What the server does not carry

The following is a precise enumeration of what the relay layer deliberately omits, relevant for security reviewers and architects evaluating the design:

**No Yjs Rust port.** The `yrs` crate was specified in the original Phase 2 plan but is not present in the as-shipped `Cargo.toml`. The server forwards raw binary Yjs protocol messages without deserialising them. Yjs document semantics live entirely on the client side.

**No document-state persistence at the relay layer.** No intermediate snapshot of CRDT state is written to disk at any point — not on connection open, not on broadcast, not on last-client-disconnect. The only write to disk in the entire collab path is the client-initiated `POST /edit/{slug}` save.

**No auth-bearing identity longer than the WebSocket lifetime.** The relay does not assign persistent user identifiers, does not log which clients contributed which messages, and does not associate a WebSocket session with any account credential beyond the duration of that WebSocket connection. Cursor colour identifiers visible in the collab UI are generated client-side and are not stored.

**No application-level rate limit on the relay path.** Axum's default connection-handling and Tokio's scheduler provide the only backpressure. A production deployment behind a reverse proxy inherits that proxy's connection limits; no relay-specific limit is enforced at the application layer.

**No server-side edit history.** Because the server stores no document state and no message log, there is no server-side edit history to inspect. The only edit history that exists is the git commit log produced by successive `POST /edit` saves. An administrator inspecting the server has no privileged view of what was typed during a collab session that was not subsequently saved.

## What this means for disclosure posture

In-flight CRDT state — the sequence of Yjs update messages exchanged between clients during a collab session — is not part of the disclosure record and cannot be, by construction. Because the relay never persists those messages, there is no server-side artefact that could later be produced in response to a disclosure obligation. The collab session leaves no shadow state on the server.

Saved edits enter the disclosure record through the same path as all other edits: `POST /edit/{slug}` sends the full Markdown text of the document, the server performs an atomic file rename, and the next git commit in the sequence captures that snapshot. From git's perspective, a collab-edited save is identical to a single-author save. The commit records what the document contained at save time; it does not record who typed which characters during the collab session. The disclosure unit is the committed document state, not the authorship decomposition of how that state was reached.

The `--enable-collab` flag's rollback path is non-destructive at every layer. Removing the flag from the systemd unit's `ExecStart` line, running `systemctl daemon-reload` and `systemctl restart`, returns the service to default-off posture without losing any data — because no data was ever held on the server side. The collab CRDT overlay is ephemeral by construction; its removal on service restart is not a data loss event. Any content that was saved before the restart exists in the git tree and is fully recoverable; any content that was in-flight and not saved before the restart is lost in exactly the same way as unsaved content in a single-author editor session.

## Generalising beyond the wiki

The passthrough relay is a substrate pattern, not a wiki-specific feature. Any service that wants concurrent editing semantics faces the same architectural question: does the collab infrastructure need to hold document state on the server, or can that state live entirely on the clients and in canonical storage? The answer depends on what the canonical storage is and whether a CRDT server sitting between the clients and that storage would compete with it for authority. Three concrete candidates inside the Foundry substrate illustrate the generalisation:

**Multi-author review in the extraction pipeline.** The canonical storage for extraction results is the deterministic parser-combinator output written to structured records, not a live editable document. Multi-author review — multiple people annotating or correcting an extraction result — would naturally benefit from presence awareness and live conflict resolution. The framing question: would a stateful CRDT server compete with the structured record store for authority? If the CRDT server materialises partial corrections not yet committed back to the structured store, the answer is yes — and the passthrough design would not directly apply without an adapter layer that serialises CRDT state to the canonical structure format on save. The passthrough pattern applies in its simplest form only when the CRDT document type maps cleanly to the canonical storage type.

**Presentation deck collaboration.** The canonical storage for a presentation is the slide deck file confirmed in git. The framing question: would a stateful CRDT server compete with the slide file for authority? The passthrough design applies if and only if the presentation's on-disk file is the canonical record and the CRDT overlay is session-ephemeral overlay on top of it. For a deck stored as a committed git artefact, that posture is achievable; for a deck stored in a format that regenerates from a server-side object, it is not.

**Proforma table collaboration.** The canonical storage for a proforma is structured tabular data — rows and columns with typed values, stored as TOML or structured JSON alongside the git tree. Collaborative editing of table cells requires a different CRDT type than character-level text merging: `Y.Map` and `Y.Array` rather than `Y.Text`. If the proforma's canonical storage is git-committed structured data and the CRDT overlay is session-ephemeral, the passthrough design applies with the same logic as the wiki case. The difference is that the serialisation step must produce valid structured data, adding a validation requirement at `POST /save` time.

## See also

- [[app-mediakit-knowledge]] — the wiki engine; collab implementation in the build phases section
- [[source-of-truth-inversion]] — the canonical / view / ephemeral pattern this design depends on
- [[substrate-native-compatibility]] — the broader substrate-native posture
