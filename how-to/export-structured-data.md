---
schema: foundry-doc-v1
title: "Export structured data from the platform"
slug: export-structured-data
short_description: "Exports platform data through three real paths — DataGraph entity records via MCP tools, wiki Markdown read directly from git, and paginated ledger entries over service-fs's HTTP API."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: export-structured-data.es.md
research_trail:
  sources: [live MCP tool schemas for query_datagraph/get_entity_context, service-fs/src/http.rs (GET /v1/entries pagination), media-knowledge-* wiki repo structure]
  verification_method: "the guide's own prior Correction note already confirmed 2 of the original 4 export paths were fabricated (a fictional wiki export endpoint, a fictional service-fs CLI); this rewrite replaces both with what's real, drops the unverified GIS GeoJSON path rather than repeat a specific endpoint that couldn't be confirmed in this pass, and fixes the fabricated INPUT/USER tier-access framing found across this whole guide group"
---

## Prerequisites

- Access to the DataGraph MCP tools, for entity exports
- Read access to the relevant `media-knowledge-*` git repository, for wiki exports
- Network access to `service-fs` and your module identifier, for ledger exports
- A device paired to the workspace (see [[pair-a-new-device]])

## Purpose

Pick the right export path for what you're actually trying to get out of the platform — entity records, article content, or audit-grade ledger history each have a genuinely different real mechanism.

## Procedure

### Path 1: Entity data from the DataGraph

Use this for structured records about a person, organization, project, or service.

1. Call `query_datagraph` to identify the entity, then `get_entity_context` on its identifier to retrieve the full profile — see [[query-the-datagraph]] for the exact tool signatures.
2. The returned object is the authoritative entity record. Copy or pipe it to your destination.

There is no separate bulk-export operation for entity data beyond repeated `get_entity_context` calls — treat it as a lookup interface, not a bulk dump tool.

### Path 2: Wiki articles as Markdown

Use this for article content you need for downstream publication, processing, or indexing.

Wiki articles are plain Markdown files with YAML frontmatter, stored directly in the `media-knowledge-*` git repositories. Read or export them the same way you'd export any file from a git repository — clone or pull the relevant repo and read the files you need directly. There is no separate HTTP export endpoint; the git repository itself is the export surface.

### Path 3: Ledger entries for audit

Use this for tamper-evident records for compliance, legal discovery, or third-party audit.

Page through `GET /v1/entries?since=<cursor>` against your `service-fs` instance until the response is empty, then fetch `GET /v1/checkpoint` to anchor what you exported to a specific `tree_size`/`root_hash`. See [[read-the-command-ledger]] for the full procedure and [[verify-worm-ledger]] for confirming what you exported hasn't been altered. The exported entries and checkpoint are both plain JSON, verifiable with a standard SHA-256 utility — no proprietary tooling required.

## Choosing the right path

| What you need | Use path |
|---|---|
| Information about a named entity (person, project, service) | 1 — DataGraph |
| Article content for publishing or indexing | 2 — Wiki Markdown |
| Tamper-evident records for compliance or audit | 3 — Ledger entries |

> **Note:** if you're looking for a spatial/GIS export path (co-location clusters, archetype data), that's a separate system this guide doesn't cover — check the GIS-specific documentation for your deployment rather than assuming the generic paths above apply there.

## Expected outcome

The data you need, exported through the path that actually matches how the platform stores it — not a fabricated unified export endpoint that doesn't exist.

## Verification

For entity data, confirm the returned profile's freshness matches your expectation (see [[query-the-datagraph]]). For wiki content, confirm the frontmatter block parses and the `slug` matches what you expected to export. For ledger entries, verify the checkpoint's `tree_size` covers every cursor you exported.

## Rollback

All three paths are read-only. Nothing to undo.

## Next steps

- [[query-the-datagraph]] — the full entity-lookup procedure
- [[read-the-command-ledger]] — the full ledger-reading procedure
- [[verify-worm-ledger]] — confirm exported ledger entries haven't been altered

## See also

- [[service-content]] — the service that maintains the DataGraph
- [[service-fs]] — the WORM ledger these entries come from
