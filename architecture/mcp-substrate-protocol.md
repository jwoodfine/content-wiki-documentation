---
schema: foundry-doc-v1
title: "MCP as Substrate Protocol"
slug: mcp-substrate-protocol
category: architecture
type: topic
quality: published
short_description: "Every Foundry Ring 1 and Ring 2 service exposes a Model Context Protocol server interface as its primary external contract, with the Doorman as the MCP gateway."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: mcp-substrate-protocol.es.md
---

**MCP-as-Substrate-Protocol** designates the Model Context Protocol (MCP) as the wire contract for all inter-service composition in the Foundry platform. Every Ring 1 and Ring 2 service exposes an MCP server interface as its primary external contract. The Doorman (`service-slm`) is the MCP gateway. Customer extensions plug in as additional MCP servers. This is not a preference or an implementation convenience — it is a structural decision encoded in Doctrine claim #46.

## Why MCP is substrate-level

The Model Context Protocol has become the industry standard for AI-native application composition. It defines a stable, machine-readable interface between clients, servers, and host processes. Foundry adopts it at the substrate level because the alternative — bespoke per-service wire formats — accumulates versioning debt, per-pair contract testing costs, and custom client implementations in every consumer. MCP is the coordination point that prevents that drift.

The practical result: a customer-built agent, an IDE extension, and the Foundry operator TUI all interact with the same service interfaces using the same protocol. There is no "developer API" distinct from the "user API." The wire contract is unified.

## How the three-ring architecture maps to MCP roles

MCP defines three roles. Foundry's architecture maps onto them directly:

**MCP Server** — each Ring 1 and Ring 2 service: the file system ledger, the knowledge runtime, the extraction service, the input service, the people service, the email service, and the egress service. When Phase 5 delivers the marketplace and settlement services, those are MCP servers too.

**MCP Client** — the Doorman (consuming Ring 1 and Ring 2 services as tools during inference); the operator TUI; customer-built agents; IDE extensions.

**MCP Host** — the Doorman for inference-traffic flows; the operator TUI for operator-traffic flows.

The Doorman is both MCP Client (calling `service-content` for graph grounding) and MCP Host (presenting the unified inference interface to upstream callers). The reuse is deliberate: the same process that holds inference credentials also mediates tool composition.

## Tool semantics

Each Foundry service exposes a small set of named MCP tools. `service-content` exposes graph query, graph mutation, vector search, and temporal query. The file ledger service exposes ledger append, ledger query, and checkpoint. The extraction service exposes entity extraction and classification. The people service exposes person lookup, upsert, and relationship query.

The marketplace service (planned Phase 5) is intended to expose listing creation, listing query, and transaction initiation as MCP tools. Customers extending Foundry add new MCP servers that expose their own vertical-specific tools. The Doorman discovers new tools at session start via MCP's describe mechanism; no core code changes are required to accommodate a new extension.

## The Doorman as MCP gateway

When any caller — task session, operator TUI, or customer agent — sends an inference request to the Doorman, the Doorman is simultaneously a client (calling `service-content` for graph context per [[knowledge-graph-grounded-apprenticeship]]) and a gateway (routing the request to the appropriate compute tier). This mediation point is where graph grounding, audit logging, tier selection, and compute-boundary enforcement all converge.

## Customer extensions

A customer with a vertical-specific data source writes an MCP server that exposes that system's data as tools. The Doorman discovers and uses those tools in subsequent inference calls alongside the built-in tools. This is the structural opening for the [[vertical-seed-packs-marketplace]]: each planned pack is intended to ship with a reference MCP server for that vertical's typical data sources.

## Composition with Code-for-Machines First

MCP is the structural realization of the [[code-for-machines-first]] principle. Every service contract is machine-readable and introspectable at runtime. Human-facing surfaces — the TUI, web interfaces — are clients of the same MCP interfaces that any other agent would use. There is no human-only data surface in Foundry.

## OpenAI-compatible HTTP boundary preserved

The Doorman's existing OpenAI-compatible HTTP interface is preserved alongside MCP. Third-party clients that use the OpenAI SDK continue to work without modification. MCP is added as the substrate-level composition standard, not as a replacement for existing compatibility.

## See Also

- [[single-boundary-compute-discipline]] — the Doorman as the single MCP gateway for inference
- [[knowledge-graph-grounded-apprenticeship]] — graph query and mutation are MCP tool calls
- [[code-for-machines-first]] — MCP as the structural realization of machine-first service contracts
- [[vertical-seed-packs-marketplace]] — planned packs ship with vertical-specific MCP server extensions

## References

1. Doctrine claim #46 — MCP-as-Substrate-Protocol (ratified v0.1.0).
2. MCP specification — https://modelcontextprotocol.io/specification/2025-11-25
3. `conventions/single-boundary-compute-discipline.md` — claim #43 composition.

---

## Provenance

Source: `convention-mcp-substrate-protocol.md` (refined 2026-04-30). Workspace-internal file paths, migration tables, and open questions removed. Phase 5 marketplace and settlement references carry "planned" and "intended" framing per BCSC continuous-disclosure posture.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
