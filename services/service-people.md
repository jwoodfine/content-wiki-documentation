---
schema: foundry-doc-v1
title: "service-people — the identity ledger service"
slug: service-people
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-1-boundary-ingest
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: service-people.es.md
short_description: "service-people is the F2 surface in os-console — an MCP server over an append-only, WORM-backed identity ledger with three tools: append, lookup, and regex-based email scanning."
cites: []
references: []
---

`service-people` is the F2 surface in `os-console` and the platform's identity ledger. It
exposes three tools over an MCP endpoint — appending a person record, looking one up, and
scanning free text for email addresses — backed by an append-only store that never overwrites
a conflicting identity. The full record schema (the `Person` type, its deterministic ID
derivation, and the store's conflict behavior) is documented in
[[identity-ledger-schema-design]]; this article covers the service surface and the automated
extraction path.

## The three MCP tools

| Tool | What it does |
|---|---|
| `identity.append` | Writes a new `Person` record to the ledger |
| `identity.lookup` | Looks up a record by email or by ID |
| `identity.scan_text` | Scans a block of text for email addresses and produces a record per address found |

All three are called over a single `POST /mcp` endpoint; the service also exposes
`/healthz` and `/readyz`. There is no separate REST route per operation — the MCP protocol
is the entire API surface.

## Automated extraction is regex, and it is email-only today

`identity.scan_text` is implemented by an internal engine the source itself calls
"ACS" — Anchor-Claim-Source, not a three-entity model with a "Semantic Socket" bridge. It
matches email addresses with a single regular expression and, for each match, derives a
stable ID (UUIDv5 of the lowercased address) and produces an anchor-and-claim pair recording
where the address was seen. This is deliberately narrow: no phone numbers, names, or
organisation strings are extracted, and no other matching strategy — Aho-Corasick or
otherwise — runs anywhere in this path. Per its own source comment, the design goal is
determinism: "ADR-07: zero AI — extraction is regex-only."

## What has no basis in the current code

No "Chart-of-Accounts" socket, gravity score, or aging-out mechanism exists in
`service-people`. An extracted identity is not classified, scored, or expired after any
elapsed time by this crate — it is appended to the ledger and stays there. Cross-referencing
against other services to promote or retire a record, if it happens at all, is not code this
crate contains.

## The flat-file substrate

Records are written through `service-fs`'s append path rather than to disk directly, keeping
the ledger's write-once guarantee — a portable, auditable store that does not require a
database migration when the schema grows.

## See also

- [[identity-ledger-schema-design]] — the full `Person` record schema, ID derivation, and
  conflict-handling behavior
- [[service-email]] — an ingest path that can feed text into `identity.scan_text`
- [[service-fs]] — the append-only store `service-people` writes through
- [[totebox-os]] — the platform this ledger's WORM storage belongs to
