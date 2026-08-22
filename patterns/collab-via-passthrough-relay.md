---
schema: foundry-doc-v1
title: "Collaboration via passthrough relay — a removed substrate pattern"
slug: collab-via-passthrough-relay
aliases:
  - collab-via-passthrough-relay
short_description: "A real-time collaborative editing design that held no document state on the server, forwarding CRDT updates directly between clients — implemented in the wiki engine, then removed."
status: active
category: patterns
type: topic
content_type: topic
quality: complete
index_group: collaboration-and-editorial-workflow
last_edited: 2026-08-22
editor: pointsav-engineering
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
paired_with: collab-via-passthrough-relay.es.md
cites:
 - doctrine-claim-29
 - doctrine-claim-16
---

## The pattern in one paragraph

The passthrough relay pattern was a real-time collaborative editing design implemented in the wiki engine and later removed. It inverted the normal assumption about where authority sits in a collaborative editing system: the relay server held no document state at all, so the canonical git tree remained the sole authoritative record of every article's content at every point in time. Concurrent editors connected over WebSocket to a per-document broadcast channel, and the server's only job was to forward CRDT update messages between those clients — it never decoded or stored the document state those messages encoded. The design is documented here because the reasoning behind it is worth understanding even though the implementation is gone: it is a clean answer to a question any collaborative-editing feature has to answer eventually.

## Why a passthrough relay rather than a CRDT server

Tools such as Etherpad and HackMD operate on a server-authoritative document model: the collaborative editing server holds a live, mutable document object, and that object is the primary record of current content. A git export is a snapshot taken from that server record, not the other way around. The consequence is a permanent second authoritative state — two places in the system hold an answer to "what is the current text of this document," and they can drift if the export mechanism fails or the server crashes before a save.

The passthrough design eliminates that second record entirely. The server acts as a message conduit, not a store — it relays update messages between clients without ever deserializing or persisting the document state they carry. The only document state the server knows in this design is whatever a client sends through the ordinary save path.

**A reader saving an article never depends on the collaboration server having done anything right.** Every edit that reaches the canonical record does so through the same save path a single-author edit would use — collaboration is additive to that path, never a second route into it.

## What this meant for disclosure posture

This mattered for the disclosure-substrate posture the wiki engine follows. The canonical disclosure record is the git tree: every article's content history is a sequence of signed commits, and that sequence is what an audit would produce. A server-authoritative CRDT store would exist in parallel with that sequence, unsigned, representing content states that never appeared in git. Under the passthrough design, no such parallel record existed — in-flight CRDT state was never written anywhere, so it was never part of the disclosure record to begin with. The record closed at save time, not before.

## Current status

The collaboration feature this pattern describes has been removed from the wiki engine. It shipped gated behind an opt-in flag, was never enabled by default, and was later deleted outright rather than left dormant — the engine today has no collaborative-editing code path at all. This article documents the design as a historical record of a pattern that was built, worked as designed, and was subsequently withdrawn; it does not describe current wiki-engine behavior.

## Generalising beyond the wiki

The passthrough relay is a substrate pattern, not a wiki-specific feature, and the underlying design question outlives this particular implementation. Any service that wants concurrent-editing semantics faces the same question: does the collaboration infrastructure need to hold document state on the server, or can that state live entirely on the clients and in canonical storage? The passthrough answer applies cleanly when the collaborative document type maps directly onto the canonical storage type — a text document collaboratively edited into a git-committed Markdown file, for instance. It applies less cleanly where the canonical storage is a different shape than the live editing session's document model, and where mapping one onto the other would require an adapter layer the passthrough design does not itself provide.

## See also

- [[source-of-truth-inversion]] — the canonical / view / ephemeral three-layer storage taxonomy this pattern instantiated
- [[app-mediakit-knowledge]] — architecture of the wiki engine this pattern was implemented in and later removed from
- [[worm-ledger-design]] — the WORM ledger substrate that closes the disclosure record at save time
- [[substrate-native-compatibility]] — why the wiki engine declines interface mimicry in favour of substrate-native surfaces
- [[disclosure-substrate]] — the broader disclosure-posture convention this design satisfied
