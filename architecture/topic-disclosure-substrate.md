---
schema: foundry-doc-v1
title: "The Continuous-Disclosure Substrate"
slug: topic-disclosure-substrate
category: architecture
type: topic
quality: published
short_description: A documentation wiki that serves simultaneously as the issuer's continuous-disclosure record, with signed-commit provenance, cryptographic timestamping, and per-jurisdiction regulatory export adapters built in from the start.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - sec-17a-4-f
  - eidas-qualified-preservation
  - ixbrl-esef
  - opentimestamps
  - rfc-3161
  - cloud-act-us
  - mcp-spec
  - w3c-verifiable-credentials
paired_with: topic-disclosure-substrate.es.md
---

The **Continuous-Disclosure Substrate** is the architectural pattern by which a PointSav knowledge wiki functions simultaneously as operational documentation and as the issuer's authoritative disclosure record. Rather than maintaining internal documentation, an investor-relations website, and statutory filings as three separately authored bodies of text on three different vendor stacks, the substrate collapses them to a single Markdown corpus rendered into every required surface from one canonical source.

## The substrate inversion

Conventional issuers maintain overlapping records: an internal document system, a vendor-hosted IR site, and periodic filings submitted to national regulators. These three bodies of text are frequently inconsistent, maintained on different update cycles, and held at providers whose jurisdiction may not match the issuer's.

The Continuous-Disclosure Substrate inverts the pattern. One set of Markdown TOPIC files, committed with signed provenance to a wiki repository hosted on the issuer's own infrastructure, generates all required outputs: rendered HTML for public readers, iXBRL documents for ESEF-compliant EU filings, SEDAR+ submission packages for Canadian continuous disclosure, EDGAR XBRL submissions for US reporting issuers, and equivalents for further jurisdictions via pluggable export adapters. The same Markdown source that a reader browses on `documentation.pointsav.com` is the disclosure record.

## Cryptographic provenance

Every TOPIC carries two layers of cryptographic provenance. The Git commit SHA plus the file path form a stable, verifiable content identity. A BLAKE3 content hash exposed in each rendered page allows external indexers, citing documents, and regulator-fetch pipelines to pin to a specific content state.

Two timestamping mechanisms anchor every commit on the wiki branch. OpenTimestamps provides free, externally verifiable proof via the Bitcoin blockchain that a specific content state existed at a specific block height. RFC 3161 Time-Stamp Authority timestamping provides formal legal recognition in EU and most common-law jurisdictions. Both are applied redundantly; neither requires trust in any Foundry service.

A two-clock discipline distinguishes `published_at` (when the wiki rendered the content state) from `valid_at` (when the underlying fact holds). The distinction addresses the standard disclosure gap: publication time does not equal fact-validity time. Both timestamps are anchored independently.

## Per-jurisdiction export adapters

A pluggable export adapter per regulatory surface transforms the Markdown corpus plus frontmatter annotations into each regulator's required submission format:

- `export-edgar` — SEC EDGAR XBRL submission package
- `export-sedar` — SEDAR+ submission format for Canadian filings
- `export-esef` — ESEF iXBRL package for EU annual reports
- `export-edinet` — EDINET XBRL package for Japan filings
- `export-dart` — DART XBRL package for Korea filings
- `export-magna` — MAGNA iXBRL package for Israel filings

Each adapter is a separable crate. New jurisdictions are additive; they do not require changes to the substrate.

## Substrate-native API surface

Rather than implementing compatibility shims for legacy systems, the substrate ships a compact set of native interfaces that cover the full range of agent and application integrations:

- MCP server (Model Context Protocol) — the 2026 de facto standard for AI-to-knowledge integrations
- REST + OpenAPI 3.1 — documented HTTP contract
- Atom and JSON Feed — feed subscription for RSS-class consumers
- JSON-LD + Schema.org markup — semantic data embedded in rendered HTML
- ActivityPub + WebFinger — W3C federation protocol enabling distributed wiki networks
- Read-only Git remote — the full Markdown corpus publicly cloneable
- Markdown bulk export — complete wiki as a versioned tarball

These surfaces emerge from the substrate's existing primitives — Markdown files in Git, hash-addressable TOPICs, frontmatter citations — rather than being retrofitted as compatibility layers.

## Substrate-enforced AI grounding

The substrate is intended to refuse to render any TOPIC whose proof-of-grounding chain does not verify. When AI assists in authoring a TOPIC, every claim must be paired with a citation ID resolvable in the workspace registry. Each citation's content hash is verified against the registry's stored hash. An adversary-AI evaluation confirms the claim is grounded in the cited source's actual content. That verdict is signed as a W3C Verifiable Credential and committed inside the same Git commit as the TOPIC. The renderer will not publish a TOPIC that fails this chain.

This mechanism is planned for the `project-disclosure` cluster phase. When operational, it means the substrate is structurally incapable of publishing ungrounded AI output — a property required for the wiki-as-disclosure-record framing to hold under regulatory scrutiny.

## Jurisdictional posture

For jurisdictions with strong statutory repositories (US, Canada, EU, Japan, Korea), the substrate is the continuous-freshness complement to periodic filings. For jurisdictions where the statutory repository is closed, proprietary, or inaccessible to public readers, the substrate becomes the canonical open record. For cross-border issuers and private companies with no applicable continuous-disclosure framework, the substrate is the record that would otherwise not exist.

The disclosure record lives on the issuer's own infrastructure under the issuer's own jurisdiction. The substrate is jurisdiction-portable by construction; a customer in Riyadh and a customer in Düsseldorf run the same binary against their own repository, anchor to timestamping authorities in their jurisdiction, and generate their locally required regulatory output via the appropriate adapter.

## Implementation state

The wiki engine (Rust, axum + comrak + maud) is operational. Edit endpoints, bilingual sibling navigation, JSON-LD baseline, TOPIC frontmatter schema, MCP server, REST API, and feed subscription are planned for subsequent phases. The iXBRL extraction module, per-jurisdiction export adapters, OpenTimestamps and RFC 3161 timestamping, and the substrate-enforced AI grounding mechanism are planned for a dedicated `project-disclosure` cluster.

## See Also

- [[compounding-doorman]] — the inference boundary that enforces sanitise-outbound discipline on every AI-assisted editorial call
- [[knowledge-commons]] — the public-vs-paid line; TOPIC content is the public layer
- [[topic-language-protocol-substrate]] — the editorial pipeline that produces TOPIC content to the required register
- [[worm-ledger-architecture]] — the append-only ledger underlying the substrate's audit guarantees

## References

1. NI 51-102 Continuous Disclosure Obligations — Canadian Securities Administrators.
2. OSC Staff Notice 51-721 Forward-Looking Information Disclosure.
3. SEC Rule 17a-4(f) — electronic records preservation.
4. eIDAS Regulation — EU electronic signature and trust services.
5. ESEF Regulation — European Single Electronic Format, iXBRL.
6. OpenTimestamps — Bitcoin-anchored timestamping, open source.
7. RFC 3161 — Internet X.509 PKI Time-Stamp Protocol.
8. CLOUD Act (2018) — US Clarifying Lawful Overseas Use of Data Act.
9. MCP Specification — Model Context Protocol, Anthropic, 2024.
10. W3C Verifiable Credentials Data Model.

---

## Provenance

Source material: `conventions/disclosure-substrate.md` (ratified 2026-04-26, doctrine v0.0.6). Refinement disciplines applied: no body H1; structural-positioning discipline (competitor names removed; capability framing retained); BCSC forward-looking framing applied to AI grounding mechanism and iXBRL extraction (planned); banned-vocabulary pass (no substitutions required); workspace-internal operational details (cluster paths, author attribution) stripped.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
