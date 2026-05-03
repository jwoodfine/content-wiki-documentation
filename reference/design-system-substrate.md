---
schema: foundry-doc-v1
title: "Design System Substrate"
slug: design-system-substrate
category: reference
type: topic
quality: published
short_description: A self-hosted, customer-owned, AI-readable design system architecture that SMB customers run on their own infrastructure, with per-tenant Git ownership and a machine-readable research backplane.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: design-system-substrate.es.md
---

A design system that lives inside a vendor's infrastructure is a design system the customer rents. The vendor controls the token vocabulary, the component shapes, the brand-voice guidelines, and the migration cost. The design system substrate inverts this: each customer owns their design system as a Git repository running on their own infrastructure, with the vendor's canonical showcase serving as both the reference implementation and the product the customer self-hosts.

## Three structural inversions

**Per-tenant ownership.** Each customer owns their design system as a Git repository with a vault-as-canonical structure. The customer's design system lives in the customer's version control, with cryptographic commit signing keyed to the customer's identity. Migration cost falls toward zero: the customer always has the source, and the substrate architecture — three layers of vault, engine, and showcase — means a customer can take the vault to any infrastructure that can run the engine binary.

**AI-readable research backplane.** Every design decision lives as a structured markdown file alongside the token definitions and component recipes. Hyperscaler design systems publish token values and component shapes; this substrate publishes token values, component shapes, and the rationale for every decision — in a format AI agents can read at code-generation time. When an AI agent generates UI that needs to align with an SMB's brand, it queries the research backplane and reads the WHY behind existing decisions, not just the WHAT. The customer's competitive advantage in the AI era is the substrate, not the labor it took to build it.

**Editor-agnostic via open token format.** Tokens are stored in W3C Design Tokens Community Group format, which is the industry-standard interchange format as of the 2025 specification. Design tools that support this format can consume the same token source; downstream tools — CSS variable generators, style dictionaries, design-software export formats — all read from the same DTCG bundle. The substrate remains neutral on which design tool the customer uses.

## Three-layer architecture

**Layer 1 — The vault.** The canonical content store: token definitions, component HTML and CSS recipes, ARIA specifications, themes, an AI-readable research directory, and derived export formats. Append-only via the platform's immutable ledger service. The vault is the source of truth; everything else derives from it.

**Layer 2 — The substrate engine.** A stateless service that reads the vault and composes token sets, bridges between the DTCG format and design-tool export formats, and exposes the research surface to AI agents. Stateless infrastructure: it can be replaced or upgraded without touching the vault.

**Layer 3 — The showcase.** The web application that serves the design system at a domain: browsable token reference, component gallery, research documentation, and export endpoints. The vendor's own showcase at `design.pointsav.com` is the same codebase and architecture as any customer instance. Single codebase, two deployment shapes.

## IBM Carbon as the floor

The substrate imports IBM Carbon's primitive token vocabulary as the floor layer of every new instance. Designers already familiar with Carbon's token naming conventions recognize the structure immediately. Customer-specific brand overrides happen at the semantic layer — `interactive-primary`, `surface-elevated` — without requiring the customer to define a complete token vocabulary from scratch. The Carbon floor reduces the initial setup burden while the brand override layer ensures the result is the customer's, not IBM's.

## AI consumption via the MCP interface

The substrate exposes tokens, components, and research through a Model Context Protocol server interface. AI agents query this interface at code-generation time to read the current token vocabulary, retrieve component recipes with their ARIA specifications and research notes, search the research backplane by topic, and validate proposed UI against brand-voice and accessibility constraints. This is designed to close the gap between AI-generated UI and brand-coherent UI: instead of having AI generate a button and then having a designer correct the brand alignment, the AI queries the research backplane first and generates UI that already reflects the brand intent.

As of late 2025, the majority of design systems in production are not structured for AI consumption. The substrate's AI-readable research backplane is intended to represent a structural lead in this dimension that is planned to compound as AI code-generation adoption increases [ni-51-102].

## What the market gap looks like

As of 2026, design-system tooling is concentrated at the enterprise end of the market. Platforms targeting this space position toward large engineering teams; their pricing, onboarding, and governance models reflect enterprise IT buyers. An SMB customer that wants a custom design system aligned to their brand, self-hosted on their own infrastructure, AI-readable, and editor-agnostic has no equivalent option in the current market. The substrate addresses this gap directly.

## See also

- [[data-vault-bookkeeping-substrate]] — the parallel vault-as-canonical architecture for financial records
- [[cluster-design-draft-pipeline]] — the pipeline that routes design contributions into this substrate
- [[compounding-substrate]] — the broader substrate sovereignty pattern

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/design-system-substrate.md` (ratified 2026-04-28). Forward-looking statements (MCP interface, structural market lead, AI adoption trajectory) carry intended/planned framing per [ni-51-102]. Material assumptions: the substrate development trajectory described in current platform documentation remains on course; actual outcomes depend on implementation scope and timeline.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
