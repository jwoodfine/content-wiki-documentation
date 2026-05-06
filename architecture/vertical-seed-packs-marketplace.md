---
schema: foundry-doc-v1
title: "Vertical Seed Packs Marketplace"
slug: vertical-seed-packs-marketplace
category: architecture
type: topic
quality: published
short_description: "Foundry intends to distribute curated industry-specific seed packs as starter taxonomies, enabling tenants to contribute refinements back through a planned marketplace."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: vertical-seed-packs-marketplace.es.md
---

The **Vertical Seed Packs Marketplace** is a planned distribution mechanism for industry-specific starter taxonomies that provision the knowledge graph of a new Foundry tenant. Each pack bundles Archetypes, a Chart of Accounts, Domains, Themes, a glossary, and MCP server extensions suited to a particular business vertical. Customers may install packs at provisioning, update them as new versions are released, and are intended to be able to contribute refinements back to the marketplace for other operators in the same vertical. This pattern encodes Doctrine claim #50.

## Pack content

Each pack is a curated bundle in open formats:

- Archetypes JSON file — industry-specific role identities
- Chart of Accounts JSON file — industry-specific business profiles
- Domains JSON file — macro work categories
- Themes JSON file — starter time-bound initiatives (typically sparse; the customer adds their own)
- Glossary CSV — terms in common use in the vertical
- MCP server extensions configuration — vertical-specific tools (for example, a point-of-sale integration for a restaurant or an electronic health record integration for a hospital)
- Pack manifest — metadata, version, license, and contributors

## Reference packs

Foundry intends to develop and maintain a set of reference packs at Phase 5 launch. The planned set includes a pack for small and mid-size restaurants, one for law firms of thirty to three hundred lawyers, one for small and rural hospitals, one for mid-size property development firms, and a universal default pack for businesses that do not fit a specific vertical.

The Woodfine real estate pack is the current reference implementation, derived from the Woodfine deployment's existing seed taxonomy and validated in production operation.

## How packs are intended to be distributed

The planned distribution mechanism routes through the marketplace gateway. Operators are intended to browse available packs within the TUI, install a pack with a single command, and receive a diff preview before applying future pack updates. The install process imports the pack's JSON files into the per-tenant knowledge graph in `service-content` and immediately enables content classification. The operator then customizes the installed taxonomy for their specific business.

## Customer contribution

When a customer extends their pack with additions useful to others in the same vertical, they may be able to contribute the additions back. The intended flow guides the operator through review, sanitization, and consent before creating a marketplace contribution. Accepted contributions are intended to land in the next pack version, benefiting other tenants in the vertical without requiring Foundry to author all pack content.

This contribution mechanism is the structural opening for community-driven vertical evolution. Its governance model — how contributions are reviewed and accepted — is a pending operator decision that will be determined during Phase 5 implementation.

## Pack licensing

Reference packs are intended to ship under a permissive license. Customer-contributed additions would retain customer copyright but grant distribution rights for marketplace inclusion.

The [[customer-owned-graph-ip]] principle applies at the instance level, not the pack level: the customer's running knowledge graph (their customized instance of a pack) is their intellectual property; the pack itself is permissively licensed material that the customer customized from.

## Composition

Vertical Seed Packs are the distribution mechanism for the [[seed-taxonomy-as-smb-bootstrap]] pattern — they carry the canonical form of the four-part taxonomy for a specific industry. The planned [[reverse-flow-substrate]] marketplace is intended to include packs as first-class inventory alongside data listings and adapter weights.

## See Also

- [[seed-taxonomy-as-smb-bootstrap]] — the four-part taxonomy structure that packs instantiate
- [[customer-owned-graph-ip]] — the customer's customized instance is their IP; the pack itself is licensed
- [[reverse-flow-substrate]] — the planned marketplace gateway that would distribute packs
- [[mcp-substrate-protocol]] — pack MCP server extensions plug into the Doorman's tool discovery

## References

1. Doctrine claim #50 — Vertical Seed Packs Marketplace (ratified v0.1.0).
2. Reference pack: Woodfine real estate seed at `vendor/pointsav-monorepo/service-content/seeds/`.

---

## Provenance

Source: `convention-vertical-seed-packs-marketplace.md` (refined 2026-04-30). Workspace-internal file paths and open questions removed. All distribution, contribution, and governance claims carry "planned," "intended," and "may" framing per BCSC continuous-disclosure posture, as Phase 5 implementation has not begun.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
