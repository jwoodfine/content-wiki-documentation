---
schema: foundry-doc-v1
title: "Foundry Architecture 2030 — An Overview"
slug: foundry-doctrine-overview
category: architecture
type: topic
quality: published
short_description: A faithful public summary of the Foundry constitutional charter — six pillars, fifty-two structural claims, eight cross-industry inventions, a three-tier compute model, three-ring service architecture, and the economic model that sustains it.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - constitutional-ai-2212-08073
  - mcp-spec
  - olmo3-allenai
  - lorax-predibase
  - opentimestamps
  - rfc-3161
  - ixbrl-esef
paired_with: foundry-doctrine-overview.es.md
---

**Foundry Architecture 2030** is the constitutional charter for the PointSav software development environment. It defines the six pillars of the platform's architecture, fifty-two structural claims that constitute its operational commitments, eight cross-industry operational inventions, and the economic model that sustains it across a small core team, paid contributors, and a large open-contributor population. The text is itself a public artifact — versioned, signed, and published under CC BY 4.0 at every MINOR version bump.

This article is a public summary of v0.1.0 ALPHA (ratified 2026-04-30). The authoritative text is available via the `pointsav/factory-release-engineering` repository.

## Core Structural Invariants

The six pillars are the invariants of the architecture. They are not aspirational principles; they are enforced constraints.

**1. Plain text only.** UTF-8 Markdown for prose, simple YAML frontmatter for routing. No binary formats, no databases, no daemons, no live indexes at the substrate level. The filesystem is the truth. Readable in 100 years with `cat`.

**2. Geometric scope.** A Claude session's role is determined by the directory it starts in — not by configuration, not by declaration, not by agreement. Master at the workspace root. Root at any engineering repository root. Task inside a per-project cluster directory. Enforced by a role-detection script and a role lock file. The scope is geometry.

**3. Unidirectional flow.** Software development always proceeds vendor → customer → deployments. No reverse direct writes. All cross-layer requests travel via a file-based mailbox.

**4. Mailbox at every boundary.** Each role has an inbox and an outbox — plain text Markdown files, version-controlled, durable. The 2026 answer to multi-agent coordination is plain-text mailbox files, not a coordination daemon. Files travel with Git history; messages are auditable.

**5. Self-describing artifacts.** Every directory worth talking to carries a `MANIFEST.md` that declares its origin, owner, lineage, and current state. A deployment instance is readable on its own, without reference to the session that created it.

**6. Human-on-the-loop assurance envelope.** Routine work runs autonomously. Human attention is reserved for the defined set of hard checkpoint events — deployments of new models into production, destructive operations, governance changes. The assurance envelope is explicit, not left to discipline.

## Architectural Commitments

The central thesis: a platform whose model fits entirely in plain text on one VM, runs without an external API, and survives 100 years on a hard drive becomes more valuable as global connectivity fragments and regulatory environments diverge. The architecture occupies structural ground that connectivity-dependent platforms cannot enter.

Fifty-two claims constitute this structural commitment. The sovereign-SMB architectural commitment includes:

**Single-Boundary Compute Discipline.** Every AI inference call in every Foundry deployment passes through a single service boundary — the {{gli|Doorman}}. Bearer tokens and compute endpoints for all inference tiers live exclusively in the {{gli|Doorman}}'s configuration. The audit ledger is complete and cryptographic because the boundary is exclusive, not preferred.

**Knowledge-Graph-Grounded Apprenticeship.** The inference service consults the per-tenant knowledge graph before every substantive request. Training tuples include the graph context alongside the query and response. Adapters trained on graph-grounded tuples generate graph-coherent responses, and accepted responses update the graph — a co-evolution loop.

**TUI-as-Corpus-Producer.** Every terminal interaction with the inference service through the system administrator TUI is a curated training contribution. Operator feedback in the form of `/feedback [good|bad]` produces DPO triples. The IT-support adapter is intended to reach production quality with 200–500 high-quality interaction triples because the domain is narrow and ground truth is unambiguous.

**MCP-as-Substrate-Protocol.** Every Ring 1 and Ring 2 service exposes a Model Context Protocol server interface as its primary external contract. The {{gli|Doorman}} is the {{gli|MCP}} gateway. Customer-specific extensions plug in as additional {{gli|MCP}} servers without modifying core services. {{gli|MCP}} is the substrate-level wire contract for service composition.

**Seed Taxonomy as SMB Bootstrap.** Every tenant deployment is provisioned with a four-part seed taxonomy as the bootstrap of its knowledge graph: Archetypes (institutional role personas), Chart of Accounts, Domains, and Themes. The taxonomy is compact, explainable, and customer-tunable from day one. Industry-specific seed packs provide starter taxonomies for first-day operation.

**Customer-Owned Graph IP.** The per-tenant knowledge graph is the customer's intellectual property. PointSav has no claim to aggregate or resell tenant graph data without explicit per-tenant opt-in. The graph exports in open format. Per-tenant {{gli|LoRA}} weights are also the customer's property.

**Tier 0 Customer-Side Sovereign Specialist.** The reference Tier 0 deployment is a small-form-factor appliance running the full deterministic substrate plus a 1B sysadmin specialist model — no GPU required. A $7/month shared-core VM demonstrates the full substrate running at this size before dedicated hardware is procured.

**Vertical Seed Packs Marketplace.** Industry-specific seed packs are distributed as starter taxonomies for new tenant deployments: restaurant SMB shape, law firm shape, regional hospital shape, real estate shape, and others. Customers customize from the pack and may contribute refinements back to the marketplace.

**Code-for-Machines First.** Every inter-service contract, audit record, configuration, and ontology is machine-readable as a primary surface. Human-facing surfaces are skins on machine-first APIs — they consume the same {{gli|MCP}} servers any other client would.

**Reverse-Flow Substrate.** The same {{gli|Doorman}} gateway and audit ledger that enforce inbound discipline also enforce outbound commercial flows: a data marketplace for customer data assets and an ad exchange for first-party audience inventory. Both flows are opt-in per tenant, disabled by default, and require per-record cryptographic provenance.

**Service-Wallet Settlement.** Marketplace and ad-exchange revenue accrues to a per-tenant internal accounting ledger. PointSav's transaction fee is an accounting deduction at the time of incoming credit. The customer withdraws to their bank or cryptocurrency address on their own schedule. PointSav is never a custodial intermediary.

**Substrate-Without-Inference Base Case.** The Totebox Archive remains fully operational and freely transferable even when no inference tier is available. The deterministic substrate — {{gli|WORM}} ledger, knowledge graph, ingest pipeline, TUI in deterministic-only mode — provides complete data sovereignty operations without any AI dependency.

Selected earlier claims of structural significance:

- **Continued-pretraining path** to customer-owned base model. The substrate compounds without vendor lock at the model layer.
- **The Compounding Substrate.** Every interaction improves the substrate for subsequent interactions, within the customer's infrastructure.
- **Adapter Composition Algebra.** The {{gli|Doorman}} is a kernel; adapters are processes; `service-content` is the filesystem. Composable intelligence.
- **Knowledge Commons / Service Commerce.** Knowledge artifacts are public and CC-licensed. The commercial threshold is multi-Totebox aggregation.
- **Designed-for-Breakout Tenancy.** Customer exit is the designed endgame, not a support exception.
- **Constrained-Constitutional Authoring.** The substrate's document schema is compiled into a context-free grammar and enforced at AI decode time. The AI cannot emit content that fails the schema.
- **The Capability Ledger Substrate.** The running system's capability state IS the append-only ledger. Ownership transfers via a single apex-cosigning ceremony.
- **The Two-Bottoms Sovereign Substrate.** seL4 for verified deployments; NetBSD for boot-anywhere sovereignty. Same binaries on both.

## Deterministic Substrate Rings

The platform organises services into three rings. Rings 1 and 2 are deterministic and function fully without Ring 3.

**Ring 1 — Boundary Ingest (per-tenant, MCP servers).** Services handle document ingestion, people data, email, and direct input. Each Ring 1 service implements an {{gli|MCP}} server interface. Customer extensions plug in as additional {{gli|MCP}} servers.

**Ring 2 — Knowledge and Processing (multi-tenant via moduleId).** Services handle extraction, content graph, search, and egress. The deterministic core of the platform. Functionally complete without AI.

**Ring 3 — Optional Intelligence (single instance, multi-tenant).** The {{gli|Doorman}} (`service-slm`) is the entirety of Ring 3. It routes among three compute tiers: Tier A local (OLMo 1B on customer hardware, zero marginal cost), Tier B GPU burst (OLMo 32B Think on a short-lived GPU instance, customer-controlled), and Tier C external API (external vendor API with explicit per-request allowlist, audit-logged at the customer's ledger). Ring 3 is structurally optional — the platform's sovereign posture is the default, not an opt-in.

## Cross-Domain Operational Patterns

The architecture draws operational patterns from eight domains outside software:

1. **Workspace Passport** (maritime) — every workspace and instance carries a MANIFEST.md that travels with it.
2. **NOTAM** (aviation) — time-sensitive operational warnings read at session start.
3. **Recall Procedure** (pharmaceutical) — defective commits trigger RECALL-NOTICE.md entries that propagate to affected deployments.
4. **Bill of Lading** (maritime shipping) — cross-realm handoffs produce append-only log entries.
5. **Time-Vested Operation** (banking/fiduciary) — destructive operations post to a queue with a vesting date and cannot execute until the date passes.
6. **Apprentice Mode** (aviation type-rating / medical residency) — new model versions run in apprentice mode; actions land in a shadow outbox; the senior reviews before promoting.
7. **Integrity Anchor** (notarization / public timestamping) — monthly and per-MINOR-bump, the workspace state hash is posted to Sigstore {{gli|Rekor}} public transparency log. Externally verifiable; anyone can prove this state existed at this time under this identity.
8. **Constitutional Convention** (IETF RFC 2026 Last Call / constitutional amendment) — MAJOR bumps require a 30-day public comment period in the `factory-release-engineering` repository.

## Open Commons Economic Structure

The economic architecture follows from the Knowledge Commons model. Knowledge artifacts are the public layer — published under open licenses (CC BY 4.0, Apache 2.0, MIT) at every MINOR bump, freely reusable. The commercial threshold is multi-Totebox aggregation: cross-Totebox query, federated search, cross-instance integration, and access to hosted LLM capacity. A single Totebox is sovereign infrastructure; operations that cross Totebox boundaries are paid service.

The contributor model that sustains this: 4–7 Core employees, 50–100 paid contributors under outcome-based contracts, and an intended 10,000+ open contributors building on the public substrate. The open tier sustains features and coverage that a small core could not maintain alone.

## Sovereign Versioning Discipline

The text versions independently of any single repository. PATCH increments per accepted commit; MINOR per shipped feature milestone; MAJOR per breaking change. v1.0.0 is the first declared-stable version; v0.1.0 ALPHA is the current state.

MAJOR bumps require a 30-day public comment period. MINOR bumps produce a signed, versioned, publicly-citable bundle. Every commit is signed with SSH-based signing and anchored to a public transparency log via the Integrity Anchor.

The BCSC Continuous Disclosure Posture applies to all claims, conventions, and public artifacts: forward-looking statements carry "planned," "intended," or "may" language with a stated basis and cautionary framing. The text does not describe future capabilities as current facts.

## See Also

- [[compounding-substrate]] — the five structural properties of the Compounding Substrate
- [[compounding-doorman]] — the single-boundary compute discipline at the inference layer
- [[adapter-composition]] — the Adapter Composition Algebra
- [[knowledge-commons]] — the Knowledge Commons / Service Commerce model
- [[system-substrate-doctrine]] — the Capability Ledger and Two-Bottoms Sovereign Substrate
- [[disclosure-substrate]] — the Continuous-Disclosure Substrate applied to the wiki layer

## References

1. NI 51-102 Continuous Disclosure Obligations — Canadian Securities Administrators.
2. OSC Staff Notice 51-721 Forward-Looking Information Disclosure.
3. Constitutional AI: Harmlessness from AI Feedback, Bai et al., arXiv 2212.08073.
4. MCP Specification — Model Context Protocol, Anthropic, 2024.
5. OLMo 3 — Allen Institute for AI, Apache 2.0.
6. LoRAX — Predibase multi-LoRA inference server.
7. OpenTimestamps — Bitcoin-anchored timestamping.
8. RFC 3161 — Internet X.509 PKI Time-Stamp Protocol.
9. ESEF Regulation — European Single Electronic Format, iXBRL.

---

## Provenance

Source material: v0.1.0 ALPHA (ratified 2026-04-30). Summary covers: Six Pillars, selected Architectural Claims (full treatment of #43–#54 plus selected earlier claims), Eight Cross-Industry Inventions, Three-Ring Architecture, economic model. Stripped: full action matrix table specifics, mailbox file paths, cluster manifest YAML schemas, commit-flow mechanics, personal contributor identity details. BCSC forward-looking framing applied to all planned capabilities. No body H1. Structural positioning throughout.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
