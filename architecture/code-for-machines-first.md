---
schema: foundry-doc-v1
title: "Code for Machines First"
slug: code-for-machines-first
category: architecture
type: topic
quality: published
short_description: "Every Foundry inter-service contract, audit record, configuration, and ontology is machine-readable as a primary surface; human-facing interfaces are skins on machine-first APIs."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: code-for-machines-first.es.md
---

**Code-for-Machines First** is the design discipline that every Foundry inter-service contract, audit record, configuration file, and ontology must be machine-readable as its primary surface. Human-facing interfaces — the operator TUI, web interfaces, mobile clients — are skins over machine-first APIs. This discipline encodes Doctrine claim #51.

## The data formats

The platform uses a consistent set of formats across all surfaces:

Inter-service communication uses MCP (see [[mcp-substrate-protocol]]). The audit ledger uses JSONL with schema versioning. Seed taxonomies use JSON. Service configuration uses TOML or YAML. Conventions and documentation use Markdown with structured frontmatter. Per-tenant configuration uses YAML.

Every artefact is machine-mutable and machine-introspectable. The MCP `describe` endpoint on any service returns the current tool catalog in a machine-readable form. There is no configuration surface that requires a human operator to interpret undocumented fields.

## Why this matters

**Consistent observability.** Structured data at every layer means audit queries and metrics have a uniform shape across services and tenants. An operator query against the audit ledger and an automated compliance check query the same JSONL schema.

**Customer extension without forking.** Customers add vertical-specific data sources by writing MCP servers. They use the same protocol all built-in services use. There is no bespoke adapter required to connect a customer-built tool to the platform.

**AI-native composition.** The substrate is consumable by AI agents — task sessions, customer-built agents, partner integrations — without a retrofit step. This is what makes the [[knowledge-graph-grounded-apprenticeship]] pattern possible: the graph is already machine-readable; the Doorman can query it programmatically at inference time.

**Migration ease.** Data export is a routine machine operation producing an open-format bundle (see [[substrate-without-inference-base-case]]). There is no migration project involving vendor cooperation, because the data was never locked in a vendor-specific format.

## The two narrow exceptions

Doctrine and convention prose documents, including this article, have prose as their primary surface. The frontmatter is machine-readable; the body is written for human readers. Operations on the body — refining register, resolving citations — are AI-assisted, but the artefact's primary surface is human.

Topic and guide documentation follows the same pattern. Frontmatter is structured and machine-parseable; body prose is for readers. These exceptions are explicit and narrow. The default is machine-first.

## Composition

This discipline is the structural claim that [[mcp-substrate-protocol]] realizes at the wire level. Every service exposes its contract through MCP `describe`, which returns a machine-readable tool catalog. Human-facing surfaces consume this catalog the same way any automated client would.

## See Also

- [[mcp-substrate-protocol]] — the structural realization of machine-first service contracts via MCP
- [[knowledge-graph-grounded-apprenticeship]] — graph queries are machine-first MCP tool calls
- [[substrate-without-inference-base-case]] — export bundles are machine-readable open formats

## References

1. Doctrine claim #51 — Code-for-Machines First (ratified v0.1.0).
2. `conventions/mcp-substrate-protocol.md` — claim #46 as structural realization of this principle.

---

## Provenance

Source: `convention-code-for-machines-first.md` (refined 2026-04-30). Workspace-internal file paths removed. No forward-looking commercial claims present in this convention.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
