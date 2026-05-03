---
schema: foundry-doc-v1
title: "Foundry Doctrine 2030 — An Overview"
slug: foundry-doctrine-overview
category: architecture
type: topic
quality: published
short_description: A faithful public summary of the Foundry Doctrine constitutional charter — six pillars, fifty-two leapfrog claims, eight cross-industry inventions, a three-tier compute model, three-ring service architecture, and the economic model that sustains it.
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

**Foundry Doctrine 2030** is the constitutional charter for the PointSav software development environment. It defines the six pillars of the platform's architecture, fifty-two leapfrog claims that constitute its structural commitments, eight cross-industry operational inventions, and the economic model that sustains it across a small core team, paid contributors, and a large open-contributor population. The doctrine is itself a public artifact — versioned, signed, and published under CC BY 4.0 at every MINOR version bump.

This article is a public summary of doctrine v0.1.0 ALPHA (ratified 2026-04-30). The authoritative text is DOCTRINE.md, available via the `pointsav/factory-release-engineering` repository.

## The Six Pillars

The six pillars are the invariants of the architecture. They are not aspirational principles; they are enforced constraints.

**1. Plain text only.** UTF-8 Markdown for prose, simple YAML frontmatter for routing. No binary formats, no databases, no daemons, no live indexes at the substrate level. The filesystem is the truth. Readable in 100 years with `cat`.

**2. Geometric scope.** A Claude session's role is determined by the directory it starts in — not by configuration, not by declaration, not by agreement. Master at the workspace root. Root at any engineering repository root. Task inside a per-project cluster directory. Enforced by a role-detection script and a role lock file. The scope is geometry.

**3. Unidirectional flow.** Software development always proceeds vendor → customer → deployments. No reverse direct writes. All cross-layer requests travel via a file-based mailbox.

**4. Mailbox at every boundary.** Each role has an inbox and an outbox — plain text Markdown files, version-controlled, durable. The 2026 answer to multi-agent coordination is plain-text mailbox files, not a coordination daemon. Files travel with Git history; messages are auditable.

**5. Self-describing artifacts.** Every directory worth talking to carries a `MANIFEST.md` that declares its origin, owner, lineage, and current state. A deployment instance is readable on its own, without reference to the session that created it.

**6. Human-on-the-loop assurance envelope.** Routine work runs autonomously. Human attention is reserved for the defined set of hard checkpoint events — deployments of new models into production, destructive operations, governance changes. The assurance envelope is explicit, not left to discipline.

## The Leapfrog Claims

The doctrine's central thesis: a platform whose model fits entirely in plain text on one VM, runs without an external API, and survives 100 years on a hard drive becomes more valuable as global connectivity fragments and regulatory environments diverge. The leapfrog is not catching up cheaper — it is occupying structural ground that connectivity-dependent platforms cannot enter.

Fifty-two claims constitute this structural commitment. The claims added in v0.1.0 (claims #43–#54) constitute the sovereign-SMB architectural commitment:

**Single-Boundary Compute Discipline (#43).** Every AI inference call in every Foundry deployment passes through a single service boundary — the Doorman. Bearer tokens and compute endpoints for all inference tiers live exclusively in the Doorman's configuration. The audit ledger is complete and cryptographic because the boundary is exclusive, not preferred.

**Knowledge-Graph-Grounded Apprenticeship (#44).** The inference service consults the per-tenant knowledge graph before every substantive request. Training tuples include the graph context alongside the query and response. Adapters trained on graph-grounded tuples generate graph-coherent responses, and accepted responses update the graph — a co-evolution loop.

**TUI-as-Corpus-Producer (#45).** Every terminal interaction with the inference service through the system administrator TUI is a curated training contribution. Operator feedback in the form of `/feedback [good|bad]` produces DPO triples. The IT-support adapter is intended to reach production quality with 200–500 high-quality interaction triples because the domain is narrow and ground truth is unambiguous.

**MCP-as-Substrate-Protocol (#46).** Every Ring 1 and Ring 2 service exposes a Model Context Protocol server interface as its primary external contract. The Doorman is the MCP gateway. Customer-specific extensions plug in as additional MCP servers without modifying core services. MCP is the substrate-level wire contract for service composition.

**Seed Taxonomy as SMB Bootstrap (#47).** Every tenant deployment is provisioned with a four-part seed taxonomy as the bootstrap of its knowledge graph: Archetypes (institutional role personas), Chart of Accounts, Domains, and Themes. The taxonomy is compact, explainable, and customer-tunable from day one. Industry-specific seed packs (claim #50) provide starter taxonomies for first-day operation.

**Customer-Owned Graph IP (#48).** The per-tenant knowledge graph is the customer's intellectual property. PointSav has no claim to aggregate or resell tenant graph data without explicit per-tenant opt-in. The graph exports in open format. Per-tenant LoRA weights are also the customer's property.

**Tier 0 Customer-Side Sovereign Specialist (#49).** The reference Tier 0 deployment is a small-form-factor appliance running the full deterministic substrate plus a 1B sysadmin specialist model — no GPU required. A $7/month shared-core VM demonstrates the full substrate running at this size before dedicated hardware is procured.

**Vertical Seed Packs Marketplace (#50).** Industry-specific seed packs are distributed as starter taxonomies for new tenant deployments: restaurant SMB shape, law firm shape, regional hospital shape, real estate shape, and others. Customers customize from the pack and may contribute refinements back to the marketplace.

**Code-for-Machines First (#51).** Every inter-service contract, audit record, configuration, and ontology is machine-readable as a primary surface. Human-facing surfaces are skins on machine-first APIs — they consume the same MCP servers any other client would.

**Reverse-Flow Substrate (#52).** The same Doorman gateway and audit ledger that enforce inbound discipline also enforce outbound commercial flows: a data marketplace for customer data assets and an ad exchange for first-party audience inventory. Both flows are opt-in per tenant, disabled by default, and require per-record cryptographic provenance.

**Service-Wallet Settlement (#53).** Marketplace and ad-exchange revenue accrues to a per-tenant internal accounting ledger. PointSav's transaction fee is an accounting deduction at the time of incoming credit. The customer withdraws to their bank or cryptocurrency address on their own schedule. PointSav is never a custodial intermediary.

**Substrate-Without-Inference Base Case (#54).** The Totebox Archive remains fully operational and freely transferable even when no inference tier is available. The deterministic substrate — WORM ledger, knowledge graph, ingest pipeline, TUI in deterministic-only mode — provides complete data sovereignty operations without any AI dependency.

Selected earlier claims of structural significance:

- **Claim #15** — Continued-pretraining path to customer-owned base model. The substrate compounds without vendor lock at the model layer.
- **Claim #18** — The Compounding Substrate. Every interaction improves the substrate for subsequent interactions, within the customer's infrastructure.
- **Claim #22** — Adapter Composition Algebra. The Doorman is a kernel; adapters are processes; `service-content` is the filesystem. Composable intelligence.
- **Claim #23** — Knowledge Commons / Service Commerce. Knowledge artifacts are public and CC-licensed. The commercial threshold is multi-Totebox aggregation.
- **Claim #28** — Designed-for-Breakout Tenancy. Customer exit is the designed endgame, not a support exception.
- **Claim #31** — Constrained-Constitutional Authoring. The substrate's document schema is compiled into a context-free grammar and enforced at AI decode time. The AI cannot emit content that fails the schema.
- **Claim #33** — The Capability Ledger Substrate. The running system's capability state IS the append-only ledger. Ownership transfers via a single apex-cosigning ceremony.
- **Claim #34** — The Two-Bottoms Sovereign Substrate. seL4 for verified deployments; NetBSD for boot-anywhere sovereignty. Same binaries on both.

## The Three-Ring Architecture

The platform organises services into three rings. Rings 1 and 2 are deterministic and function fully without Ring 3.

**Ring 1 — Boundary Ingest (per-tenant, MCP servers).** Services handle document ingestion, people data, email, and direct input. Each Ring 1 service implements an MCP server interface. Customer extensions plug in as additional MCP servers.

**Ring 2 — Knowledge and Processing (multi-tenant via moduleId).** Services handle extraction, content graph, search, and egress. The deterministic core of the platform. Functionally complete without AI.

**Ring 3 — Optional Intelligence (single instance, multi-tenant).** The Doorman (`service-slm`) is the entirety of Ring 3. It routes among three compute tiers: Tier A local (OLMo 1B on customer hardware, zero marginal cost), Tier B GPU burst (OLMo 32B Think on a short-lived GPU instance, customer-controlled), and Tier C external API (external vendor API with explicit per-request allowlist, audit-logged at the customer's ledger). Ring 3 is structurally optional — the platform's sovereign posture is the default, not an opt-in.

## The Eight Cross-Industry Inventions

The doctrine draws operational patterns from eight domains outside software:

1. **Workspace Passport** (maritime) — every workspace and instance carries a MANIFEST.md that travels with it.
2. **NOTAM** (aviation) — time-sensitive operational warnings read at session start.
3. **Recall Procedure** (pharmaceutical) — defective commits trigger RECALL-NOTICE.md entries that propagate to affected deployments.
4. **Bill of Lading** (maritime shipping) — cross-realm handoffs produce append-only log entries.
5. **Time-Vested Operation** (banking/fiduciary) — destructive operations post to a queue with a vesting date and cannot execute until the date passes.
6. **Apprentice Mode** (aviation type-rating / medical residency) — new model versions run in apprentice mode; actions land in a shadow outbox; the senior reviews before promoting.
7. **Integrity Anchor** (notarization / public timestamping) — monthly and per-MINOR-bump, the workspace state hash is posted to Sigstore Rekor public transparency log. Externally verifiable; anyone can prove this state existed at this time under this identity.
8. **Constitutional Convention** (IETF RFC 2026 Last Call / constitutional amendment) — doctrine MAJOR bumps require a 30-day public comment period in the `factory-release-engineering` repository.

## The Economic Model

The economic architecture follows from claim #23. Knowledge artifacts are the public layer — published under open licenses (CC BY 4.0, Apache 2.0, MIT) at every Doctrine MINOR bump, freely reusable. The commercial threshold is multi-Totebox aggregation: cross-Totebox query, federated search, cross-instance integration, and access to hosted LLM capacity. A single Totebox is sovereign infrastructure; operations that cross Totebox boundaries are paid service.

The contributor model that sustains this: 4–7 Core employees, 50–100 paid contributors under outcome-based contracts, and an intended 10,000+ open contributors building on the public substrate. The open tier sustains features and coverage that a small core could not maintain alone.

## Governance

The doctrine versions independently of any single repository. PATCH increments per accepted commit; MINOR per shipped feature milestone; MAJOR per breaking change. v1.0.0 is the first declared-stable doctrine; v0.1.0 ALPHA is the current state.

Doctrine MAJOR bumps require a 30-day public comment period (Constitutional Convention, Invention #8). MINOR bumps produce a signed, versioned, publicly-citable bundle. Every commit is signed with SSH-based signing and anchored to a public transparency log via the Integrity Anchor (Invention #7).

The BCSC Continuous Disclosure Posture applies to all doctrine claims, conventions, and public artifacts: forward-looking statements carry "planned," "intended," or "may" language with a stated basis and cautionary framing. The doctrine does not describe future capabilities as current facts.

## See Also

- [[compounding-substrate]] — the five structural properties of the Compounding Substrate (Doctrine claim #18)
- [[compounding-doorman]] — the single-boundary compute discipline (Doctrine claim #43) at the inference layer
- [[adapter-composition]] — the Adapter Composition Algebra (Doctrine claim #22)
- [[knowledge-commons]] — the Knowledge Commons / Service Commerce model (Doctrine claim #23)
- [[system-substrate-doctrine]] — the Capability Ledger and Two-Bottoms Sovereign Substrate (Doctrine claims #33, #34)
- [[disclosure-substrate]] — the Continuous-Disclosure Substrate (Doctrine claim #31 applied to the wiki layer)

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

Source material: `DOCTRINE.md` v0.1.0 ALPHA (ratified 2026-04-30). Summary covers: Six Pillars (§I), selected Leapfrog Claims from §II (full treatment of #43–#54 plus selected earlier claims), Eight Cross-Industry Inventions (§III), Three-Ring Architecture (from §IV context and CLAUDE.md §11), economic model (from claim #23 and `conventions/knowledge-commons.md`). Stripped: §III identity store paths, §V full action matrix table specifics, mailbox file paths, cluster manifest YAML schemas, commit-flow mechanics, personal contributor identity details. BCSC forward-looking framing applied to all planned capabilities. No body H1. Structural positioning throughout.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
