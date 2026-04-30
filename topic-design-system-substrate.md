---
schema: foundry-doc-v1
title: "Design-System Substrate"
slug: topic-design-system-substrate
category: architecture
type: topic
quality: complete
short_description: "The design-system substrate is a self-hosted, customer-owned design-system engine that stores tokens and components in the customer's own Git repository, serves them through a machine-readable MCP endpoint, and uses the W3C DTCG token format to remain editor-agnostic."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - mcp-spec
  - sigstore-rekor-v2
  - c2sp-tlog-tiles
  - ni-51-102
  - osc-sn-51-721
paired_with: topic-design-system-substrate.es.md
---

# Design-System Substrate

> The design-system substrate is a self-hosted, customer-owned design-system engine that stores tokens and components in the customer's own Git repository, serves them through a machine-readable MCP endpoint, and uses the W3C DTCG token format to remain editor-agnostic.

The PointSav **design-system substrate** is a self-hosted, customer-owned design-system engine. The vendor showcase at `design.pointsav.com` is the canonical instance. Each SMB customer who forks the substrate runs their own instance at their own domain. Single codebase, single deployment shape, two contexts — vendor showcase and customer instance.

Most SMB design systems are hosted on hyperscaler infrastructure. Enterprise-scale platforms — IBM Carbon, Google Material, Salesforce Lightning — place the design system inside the hyperscaler's own infrastructure. Enterprise SaaS tools in the design-system space carry entry pricing of $40–100 per seat per month. The SMB below the enterprise tier has structurally been underserved by this arrangement.

The substrate inverts that pattern on three structural axes: the customer's design system lives in the customer's Git repository, signed by the customer's key, replayable into any tool; design-decision research lives in the same vault as the tokens and components, served through the same Model Context Protocol endpoint `[mcp-spec]` that AI agents use; and tokens are stored in the W3C Design Tokens Community Group (DTCG) format, keeping the substrate editor-agnostic by construction.

## Vault structure

The substrate's content lives in a per-tenant vault directory:

```
<tenant-vault>/
├── tokens/        DTCG primitive + semantic + component layers
├── components/    HTML+CSS+ARIA recipe files
├── themes/        per-brand semantic-layer overrides
├── research/      AI-readable design-decision rationale (markdown)
└── exports/       derived caches (Figma, Tailwind, Style Dictionary)
```

The vault is the only canonical layer. Rendered exports — Figma Variables JSON, Tailwind config, CSS variables, Style Dictionary builds — are derived caches recomputable from the canonical four directories above.

The substrate engine is a stateless HTTP service that reads the vault from disk. Per-tenant isolation is achieved by running one engine process per tenant, each pointed at its own vault. Persistence above the vault filesystem is via the substrate's WORM ledger (service-fs). Token and component history is anchored monthly to Sigstore Rekor `[sigstore-rekor-v2]`, producing a customer-rooted Merkle log using the C2SP tlog-tiles format `[c2sp-tlog-tiles]` per Doctrine claim #33.

## AI-readable research backplane

The `research/` directory is the substrate's most structurally novel element. Every design decision lives as a structured markdown file:

```
---
schema: foundry-design-research-v1
component_or_token: button-primary
decision_type: component-introduction
authored: 2026-04-28
authored_by: design-team-member-name OR ai-agent-id
status: ratified
brand_voice_alignment: [confident, direct, professional]
accessibility_targets: [wcag-2-2-aa, focus-visible]
ai_consumption_hint: "When generating a button for a primary
  action, use this component. When the action is destructive, use
  button-danger instead."
---
```

The frontmatter is machine-readable; the body is prose-readable. AI agents consume the research through the substrate's MCP endpoint `[mcp-spec]` at decode time. Methods include `list_tokens`, `list_components`, `list_research`, and `describe`. An AI agent registers the substrate as an MCP server, then queries it during UI generation to align with the SMB's brand intent.

Design systems that publish only token values and component shapes omit the rationale behind those choices. The substrate publishes both, in the same machine-readable tier, served through the same endpoint.

## Editor-agnostic via DTCG

The W3C Design Tokens Community Group format reached its 2025.10 stable specification in October 2025. Figma ships native DTCG import and export; Penpot has been DTCG-native since Penpot 2.x; Style Dictionary, Specify, and Tokens Studio all consume DTCG.

On the consumer side:

- **Figma** — via the Tokens Studio plugin or Figma's native variable system
- **Penpot** — imports DTCG natively; the substrate-Penpot pairing is the fully-open-source design workflow Foundry recommends to SMB customers who prefer a self-hostable editor
- **Sketch** — via the Tokens Studio Sketch plugin
- **Hand-authoring** — designers edit DTCG JSON directly; this is also the path most accessible to AI agents

The customer chooses the editor; the substrate does not require a particular one.

## IBM Carbon as the floor

The substrate imports IBM Carbon's primitive token vocabulary as the floor layer of every new instance. Color naming follows Carbon's convention (`gray-10` through `gray-100`). Type scale follows Carbon's productive and expressive families. Spacing follows Carbon's 8px grid. Focus ring follows Carbon's WCAG 2.2 AAA-conformant style.

Brand-specific work happens at the semantic layer (`themes/<brand>/`), not the primitive layer. SMB customers extend with brand overrides without re-learning a new component taxonomy.

Carbon was chosen for three reasons: familiarity surface (wide accessible-design muscle-memory footprint among practitioners), accessibility floor (WCAG 2.2 AAA conformance built into primitive choices), and permissive licensing on the form (Carbon's token values are publicly documented; IBM Plex is permissively licensed; the naming convention is a documentation artefact, not a trademarked asset).

What is not imported from Carbon: IBM Cloud-specific themes, React-specific component implementations, the IBM logo and "Carbon" wordmark, Carbon-specific component micro-interactions.

A planned future milestone may introduce an alternative primitive bottom — Untitled UI (MIT-licensed) is a candidate for a second primitive layer in a subsequent release. That work is intended and subject to technical evaluation; no timeline is committed. Forward-looking statements about future milestones are subject to the cautionary factors described in `[ni-51-102]` and `[osc-sn-51-721]`.

## Customer fork procedure

An SMB customer forks by cloning the source repository, building the substrate engine (a native Rust binary), initialising a vault from the canonical template, editing their brand's semantic layer in `themes/<smb-brand>.json`, and running the bootstrap script to configure the service and TLS. The operator runbook at `vault-privategit-design/GUIDE-deploy-design-substrate.md` covers the full procedure.

The customer ends up with a fully self-hosted, customer-owned design-system substrate. No SaaS dependency. No hyperscaler runtime. Their theme files and any research entries they author are their work product, in their Git repository, signed by their key.

## What makes the substrate structurally distinct

**Per-tenant Git ownership** requires a per-tenant signing identity (the customer's `allowed_signers` chain). Platforms hosted on shared infrastructure cannot accommodate this without becoming a Git hosting provider.

**AI-readable research backplane in customer-owned form** requires per-customer hosting. A platform can publish its own design research; it cannot publish the SMB customer's research, because it does not host the SMB customer's design system.

**Customer-rooted attestation.** The substrate's quarterly Trustworthy System Attestation combines the WORM ledger, Sigstore Rekor anchoring `[sigstore-rekor-v2]`, and per-tenant `allowed_signers`. The resulting attestation covers the customer's design data — not the platform provider's controls.

**Editor agnosticism.** Commercial design-system platforms have an incentive to keep the customer in their editor ecosystem. The substrate has no such incentive — DTCG is the common denominator.

The four properties compound. Removing any one weakens the others.

## What the substrate is not

The substrate is not a Storybook replacement. Storybook is a parallel renderer; the substrate owns its rendering.

It is not a design editor competitor. Design editors (Figma, Penpot, Sketch) are the tools designers work in; the substrate is the canonical store those editors interoperate with via DTCG.

It is not a SaaS platform. A managed-hosting option for SMB customers who prefer not to operate the service themselves is a planned future offering subject to operator capacity and customer demand; the substrate code will remain self-hostable in all cases.

It is not a JavaScript-framework choice. Components are HTML+CSS+ARIA recipes; the customer's chosen framework consumes the recipe.

It is not a container artefact. Per the zero-container-runtime convention, the substrate ships as a native binary deployed via systemd.

## See Also

- [[topic-compounding-substrate]]
- [[topic-substrate-native-compatibility]]
- [[topic-reverse-funnel-editorial-pattern]]
- [[topic-customer-hostability]]

## References
