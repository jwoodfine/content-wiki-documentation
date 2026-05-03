---
schema: foundry-topic-v1
title: "Real-time collaboration via passthrough relay — a substrate pattern"
status: published
category: architecture
last_edited: 2026-04-30
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
research_done_count: 9
research_suggested_count: 2
open_questions_count: 1
research_provenance: project-knowledge cluster session 619abe3eff24497e
research_inline: false
cites:
  - doctrine-claim-29
  - doctrine-claim-16
---

## The pattern in one paragraph

The passthrough relay pattern inverts the normal assumption about where a collaborative editing server sits in the authority chain: the relay holds no document state, so the canonical git tree remains the sole authoritative record of every topic's content at every point in time. Concurrent editors connect over WebSocket to a `tokio::sync::broadcast` channel keyed by slug — one broadcast room per document — and the server's only job is to forward Yjs CRDT update messages between those clients. The server neither decodes nor stores the document state those messages encode. The sole persistence boundary in the entire system is the `POST /edit/{slug}` atomic-write path: when an editor saves, the client serialises its local Yjs document to Markdown, sends it over HTTP, and the server atomically renames the new file into place on disk — the same operation as a single-author save.

## Why a passthrough relay rather than a CRDT server

Tools such as Etherpad and HackMD operate on a server-authoritative document model: the collaborative editing server holds a live, mutable document object — an Operational Transformation log in Etherpad's case, a Y.Doc in HackMD's — and that object is the primary record of current content. A git export is a snapshot taken from that server record, not the other way around. The consequence is a permanent second authoritative state: two places in the system hold an answer to the question "what is the current text of this document," and they can drift if the export mechanism fails, the server crashes before a save, or the OT/CRDT log diverges from git history at a merge edge case.

The passthrough design eliminates that second record entirely. The server is a message conduit, not a store. When a Yjs client sends a binary update message to `GET /ws/collab/{slug}`, the Rust handler receives the raw bytes from the WebSocket and broadcasts them to all other clients in the same slug room via `tokio::sync::broadcast`. The server never deserialises the Yjs protocol; it never constructs a Y.Doc; it never writes anything to disk as a side effect of a relay operation. The only document state the server knows is whatever the client sends through `POST /edit` — the HTTP save path.

This matters for the disclosure-substrate posture in Doctrine claim #29 (Substrate Substitution). The canonical disclosure record is the git tree: every topic's content history is a sequence of signed commits, and that sequence is what a regulatory audit would produce. A server-authoritative CRDT store would exist in parallel with that sequence, would not be signed, and would represent content states that never appeared in git. Under the passthrough design, no such parallel record exists: in-flight CRDT state is definitionally not part of the disclosure record because it is never written anywhere. The record closes at `POST /edit` time, not before.

The 256-message lag buffer configured on each `tokio::sync::broadcast` channel addresses the one race this design must handle: a client that joins a collab session after other editors have already made changes will not have received those earlier Yjs update messages. Because Yjs CRDTs are convergent, a client that receives all prior update messages in any order arrives at the same document state. The 256-message buffer lets a late joiner catch up on recent activity without the server needing to materialise or store the full document state. If the buffer fills before a late joiner connects, Yjs's sync protocol handles the gap through its state-vector exchange on connection open — the server's job remains forwarding, not resolving.

## The implementation in `app-mediakit-knowledge`

The collab relay shipped in commit `05f1dab` as `src/collab.rs`, gated entirely behind the `--enable-collab` CLI flag. When the flag is absent — the default, and the production posture as of v0.1.29 — the WebSocket route `GET /ws/collab/{slug}` is not registered in the axum router, the `window.WIKI_COLLAB_ENABLED` template variable is set to `false`, and the client-side JavaScript bundle never loads. Zero collab code paths execute in the default-off configuration.

The server-side relay uses `tokio::sync::broadcast`, the standard Tokio multi-producer multi-consumer channel. Each slug gets its own broadcast channel with a buffer capacity of 256 messages, created on first connection and stored in a `DashMap<String, broadcast::Sender<Bytes>>` held in `AppState`. When a WebSocket client sends a Yjs update message, the handler reads the raw bytes and calls `sender.send(bytes)` — a single line that fans the message out to all other receivers on that channel. There is no `yrs` crate dependency; the Rust port of Yjs was specified in the original `PHASE-2-PLAN.md` Step 7 brief but was not used in the as-shipped implementation. The server relays raw Yjs binary protocol messages without deserialising them, so the server carries no document state at any point.

The WebSocket upgrade uses axum's built-in WS support. The route handler upgrades the HTTP connection, spawns a task per client that loops on incoming WebSocket frames and rebroadcasts each, and removes the client from the room's receiver set on disconnect. If the last client disconnects, the broadcast channel's receiver count drops to zero; the `DashMap` entry persists but holds an empty channel, ready for the next connection. No disk write occurs on last-client-disconnect — a deliberate departure from the `PHASE-2-PLAN.md` spec that originally called for snapshotting the Y.Doc to disk on last disconnect. The passthrough design makes that snapshot impossible because the server never holds the Y.Doc.

The client bundle `cm-collab.bundle.js` (~302 KB as shipped) is built from three npm packages vendored in `vendor-js/`: `yjs`, `y-codemirror.next`, and `y-websocket`. The bundle is committed to `static/vendor/` as a pre-built artefact, so no npm toolchain is required at runtime or in the Rust build path. The `static/saa-init.js` initialisation script checks `window.WIKI_COLLAB_ENABLED` at load time; if the flag is `false`, the import of `cm-collab.bundle.js` is never executed. The CodeMirror editor loads fully in either case — collab is additive to the editing surface, not a prerequisite.

Test coverage at commit `05f1dab` added 7 tests (3 unit + 4 integration) to bring the total from 90 to 97. The unit tests cover: the WebSocket route accepts a connection when `--enable-collab` is set; `tokio::sync::broadcast` rooms multiplex correctly across two clients on the same slug; the 256-message buffer drains to completion without panic; and the client bundle HTTP 200 is reachable only when the flag is set. The 4 integration tests cover flag-gated script-injection behaviour in rendered HTML. Visual cursor-presence verification requires a two-headed browser smoke with DOM inspection, which was judged out-of-scope for Phase 2 and is covered by the manual smoke procedure in `STEP-7-COLLAB-SMOKE.md`.

## What the server does not carry

The following is a precise enumeration of what the relay layer deliberately omits, relevant for security reviewers and architects evaluating the design:

- **No Yjs Rust port (`yrs` crate).** The `yrs` crate was specified in `PHASE-2-PLAN.md` Step 7 but is absent from the as-shipped `Cargo.toml`. The server forwards raw binary Yjs protocol messages without deserialising them. Yjs document semantics live entirely on the client side.
- **No document-state persistence at the relay layer.** No intermediate snapshot of CRDT state is written to disk at any point — not on connection open, not on broadcast, not on last-client-disconnect. The only write to disk in the entire collab path is the client-initiated `POST /edit/{slug}` save.
- **No auth-bearing identity beyond the WebSocket lifetime.** The relay does not assign persistent user identifiers, does not log which clients contributed which messages, and does not associate a WebSocket session with any account credential beyond the duration of that connection. Cursor colour identifiers visible in the collab UI are generated client-side and are not stored.
- **No application-level rate limit on the relay path.** The broadcast handler applies no rate limit on relay messages beyond axum defaults. A production deployment behind nginx inherits that proxy's connection limits; no relay-specific limit is enforced at the application layer.
- **No admin-accessible edit history on the server side.** Because the server stores no document state and no message log, there is no server-side edit history to inspect. The only edit history that exists is the git commit log produced by successive `POST /edit` saves.

## What this means for disclosure posture

In-flight CRDT state — the sequence of Yjs update messages exchanged between clients during a collab session — is not part of the disclosure record and cannot be, by construction. Because the relay never persists those messages, there is no server-side artefact that could later be produced in response to a disclosure obligation. The collab session leaves no shadow state on the server. This is not a gap in the record; it is a design property that aligns the collab implementation with Doctrine claim #29's requirement that canonical storage — here the git tree — be the sole authoritative record. A server-authoritative CRDT store would create a second authoritative record that is not git, not signed, and not suitable for regulatory production.

Saved edits enter the disclosure record through the same path as all other edits: `POST /edit/{slug}` sends the full Markdown text of the document, the server performs an atomic file rename, and the next git commit in the sequence captures that snapshot. From git's perspective, a collab-edited save is identical to a single-author save. The commit records what the document contained at save time; it does not record who typed which characters during the collab session. The disclosure unit is the committed document state, not the authorship decomposition of how that state was reached.

The `--enable-collab` flag's rollback path (documented in `STEP-7-COLLAB-SMOKE.md` §5) is non-destructive at every layer precisely because of this design. Removing the flag from the systemd unit's `ExecStart` line, running `systemctl daemon-reload` and `systemctl restart`, returns the service to default-off posture without losing any data — because no data was ever held on the server side. The collab CRDT overlay is ephemeral by construction; its removal on service restart is not a data loss event. Any content saved before the restart exists in the git tree and is fully recoverable.

## Generalising beyond the wiki

The passthrough relay is a substrate pattern, not a wiki-specific feature. Any service that wants concurrent editing semantics faces the same architectural question: does the collab infrastructure need to hold document state on the server, or can that state live entirely on the clients and in canonical storage? The answer depends on what the canonical storage is and whether a CRDT server sitting between the clients and that storage would compete with it for authority.

**`service-extraction` multi-author review pipeline.** The canonical storage for extraction results is the deterministic parser-combinator output written to structured records. The framing question: would a stateful CRDT server compete with the structured record store for authority? If the CRDT server materialises partial corrections that have not yet been committed back to the structured store, the answer is yes — and the passthrough design would not directly apply without an adapter layer that serialises CRDT state to the canonical structure format on save. The passthrough pattern applies in its simplest form only when the CRDT document type maps cleanly to the canonical storage type.

**`app-workplace-presentation` deck collaboration.** The canonical storage for a presentation is the slide deck source committed to the customer's Git repository. The framing question: would a stateful CRDT server compete with the slide file for authority? Yes — a server-authoritative presentation service by definition holds the authoritative deck object. The passthrough design applies if and only if the on-disk file format is the canonical record and the CRDT overlay is treated as session-ephemeral on top of it. For a deck stored as a committed git artefact, that posture is achievable; for a deck stored in a third-party format that regenerates from a server-side object, it is not. Note: CRDT collaboration for `app-workplace-presentation` is planned; it is not yet implemented as of 2026-04-27.

**`app-workplace-proforma` table collaboration.** The canonical storage for a proforma is structured tabular data — rows and columns with typed values, stored as TOML or structured JSON alongside the git tree. Collaborative editing of table cells requires a different CRDT type than character-level text merging (`Y.Map` and `Y.Array` rather than `Y.Text`), but the `yjs` library handles this. If the proforma's canonical storage is git-committed structured data and the CRDT overlay is session-ephemeral, the passthrough design applies with the same logic as the wiki case. The difference from the text case is that the serialisation step must produce valid structured data, adding a validation requirement at `POST /save` time. Note: CRDT collaboration for `app-workplace-proforma` is planned; it is not yet implemented as of 2026-04-27.

## References

- **Yjs** — Conflict-free replicated data type library for collaborative applications. Client-side CRDT engine used in `cm-collab.bundle.js`. https://github.com/yjs/yjs
- **CodeMirror collab integration** — `y-codemirror.next` binds a Yjs `Y.Text` to a CodeMirror 6 editor state; cursor presence is rendered via CodeMirror's `DecorationSet` API. https://codemirror.net/
- **`tokio::sync::broadcast`** — Multi-producer multi-consumer channel used as the per-slug relay room. 256-message buffer is the channel capacity argument passed to `broadcast::channel(256)`. https://docs.rs/tokio/latest/tokio/sync/broadcast/
- **`PHASE-2-PLAN.md` §1 Step 7** — Original Step 7 brief specifying the collab design. `vendor/pointsav-monorepo/app-mediakit-knowledge/docs/PHASE-2-PLAN.md`
- **`STEP-7-COLLAB-SMOKE.md`** (commit `ea26118`) — Manual two-client smoke procedure, pre-staged systemd unit diff, and rollback runbook for production enable. `vendor/pointsav-monorepo/app-mediakit-knowledge/docs/STEP-7-COLLAB-SMOKE.md`
- **`ARCHITECTURE.md` §11** — Full API surface set table listing `/ws/collab/{slug}` as a Phase 2+ opt-in route. `vendor/pointsav-monorepo/app-mediakit-knowledge/ARCHITECTURE.md`
- **`UX-DESIGN.md` §4.7** — Collab UX wireframe and cursor-presence pattern for the SAA editor surface. `vendor/pointsav-monorepo/app-mediakit-knowledge/UX-DESIGN.md`
- **Doctrine claim #29** (Substrate Substitution) — Establishes that the canonical disclosure record is git; no parallel server-side store may compete with it for authority. `~/Foundry/DOCTRINE.md`

## See also

- [[source-of-truth-inversion]] — The canonical / view / ephemeral three-layer storage taxonomy that this pattern instantiates.
- [[app-mediakit-knowledge]] — Architecture of the wiki engine that ships this pattern.
- [[substrate-native-compatibility]] — Why the wiki engine declines interface mimicry in favour of substrate-native surfaces.
- [[disclosure-substrate]] — The broader disclosure-posture convention this design satisfies.

## Provenance

Authored by project-knowledge Task Claude (session 619abe3eff24497e, 2026-04-28). Refined by project-language, 2026-04-30. Source references are the `app-mediakit-knowledge` implementation files listed above and Doctrine claim #29.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
