---
schema: foundry-doc-v1
title: "The design-system substrate"
slug: topic-design-system-substrate
category: architecture
status: published
last_edited: 2026-04-28
editor: pointsav-engineering
bcsc_class: current-fact + forward-looking
cites:
  - mcp-spec
  - sigstore-rekor-v2
  - c2sp-tlog-tiles
  - ni-51-102
  - osc-sn-51-721
doctrine_claims:
  - "38"
  - "36"
  - "34"
  - "33"
  - "29"
  - "28"
  - "22"
  - "18"
---

## What it is

The PointSav design-system substrate is a self-hosted, customer-owned design-system engine. The vendor showcase at `design.pointsav.com` is the canonical instance. Each SMB customer who forks the substrate runs their own instance at their own domain. Single codebase, single deployment shape, two contexts — vendor showcase and customer instance.

Most SMB design systems are hosted on hyperscaler infrastructure. Major enterprise platforms — IBM Carbon, Google Material, Salesforce Lightning, and others — place the design system inside the hyperscaler's own infrastructure. Enterprise SaaS tools in the design-system space carry entry pricing of $40–100 per seat per month. The SMB below the enterprise tier has structurally been underserved by this arrangement.

The substrate inverts that pattern on three structural axes:

1. The customer's design system lives in the customer's Git repository, signed by the customer's key, replayable into any tool. Migration cost falls toward zero — the customer always holds the source.
2. Design-decision research lives in the same vault as the tokens and components, served through the same Model Context Protocol (MCP) endpoint `[mcp-spec]` that AI agents use to query everything else. The well-structured substrate is the message the SMB sends to its implementation partners.
3. Tokens are stored in the W3C Design Tokens Community Group (DTCG) format. Design editors — Figma, Penpot, Sketch, and hand-authoring workflows — all interoperate. The substrate stays editor-agnostic by construction.

The structural gap that motivates the substrate is grounded in current data:

- 39% of design-system practitioners work at companies with 5,000 or more employees (2026 Design Systems Report). The practitioner population is concentrated at enterprise scale; SMBs without an in-house practitioner have had limited access to the discipline.
- Major commercial design-system platforms announced explicit enterprise-only positioning in 2025. Purpose-built SMB tooling did not follow.
- Only 23% of design systems were structured for AI consumption as of December 2025. A self-hosted MCP-serving substrate on the customer-owned, editor-agnostic side addresses a gap that proprietary platforms do not.

The substrate is what fills that gap.

## The vault-as-canonical pattern

The substrate's content lives in a per-tenant vault directory:

```
<tenant-vault>/
├── tokens/        DTCG primitive + semantic + component layers
├── components/    HTML+CSS+ARIA recipe files
├── themes/        per-brand semantic-layer overrides
├── research/      AI-readable design-decision rationale (markdown)
└── exports/       derived caches (Figma, Tailwind, Style Dictionary)
```

The vault is the only canonical layer. Rendered exports — Figma Variables JSON, Tailwind config, CSS variables, Style Dictionary builds — are derived caches recomputable from the canonical four directories above. Migration cost falls toward zero because the canonical state is what gets committed, reviewed, replicated, and disclosed.

The substrate engine is a stateless HTTP service that reads the vault from disk. Restarting the engine re-reads the vault. Per-tenant isolation is achieved by running one engine process per tenant, each pointed at its own vault. Multi-tenant fan-out is operational, not architectural — the architecture is single-tenant per process, by design.

Persistence happens above the vault filesystem via the substrate's WORM ledger (service-fs, the workspace's append-only audit infrastructure). Token and component history is anchored monthly to Sigstore Rekor `[sigstore-rekor-v2]`, producing a customer-rooted Merkle log apex using the C2SP tlog-tiles format `[c2sp-tlog-tiles]` per the Capability Ledger Substrate (Doctrine claim #33). SMB customers receive a Trustworthy System Attestation (TSA) every quarter — the customer's substrate operator signs a report citing the vault checkpoints, the customer's `allowed_signers` chain, and the WORM ledger record.

## AI-readable research backplane

The `research/` directory is the substrate's most structurally novel element. Every design decision lives as a TOPIC-style markdown file with explicit structure:

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

The frontmatter is machine-readable; the body is prose-readable. AI agents consume the research through the substrate's MCP endpoint `[mcp-spec]` at decode time. JSON-RPC 2.0 over HTTP POST; methods include `list_tokens`, `list_components`, `list_research`, and `describe`. An AI agent registers the substrate as an MCP server, then queries it during UI generation to align with the SMB's brand intent.

The research closes the AI-productivity / brand-coherence trade-off. Workflows that treat AI as a substitute for the lowest-skill design step (suggest a button color) leave the practitioner re-deciding established questions every session. The substrate treats AI as a substitute for the highest-volume design step — applying established brand intent across thousands of UI surfaces. Creative designers work at their actual advantage point: taste, craft, and brand evolution.

Design systems that publish only the token values and component shapes omit the rationale behind those choices. The substrate publishes both, in the same machine-readable tier, served through the same endpoint. That is the structural inversion.

## Editor-agnostic via DTCG

The W3C Design Tokens Community Group format reached its 2025.10 stable specification in October 2025. Figma ships native DTCG import and export; Penpot (the open-source, BSD-licensed, self-hostable design editor) has been DTCG-native since Penpot 2.x; Style Dictionary, Specify, and Tokens Studio all consume DTCG. A Git-based DTCG-canonical token store is structurally future-aligned because the 2026–2030 tool roadmap converges on DTCG as the interchange format.

On the consumer side:

- **Figma** — via the Tokens Studio plugin or via Figma's native variable system; the substrate ships an `exports/figma-variables.json` converter for the latter.
- **Penpot** — imports DTCG natively; the substrate-Penpot pairing is the fully-open-source design workflow Foundry recommends to SMB customers who prefer a self-hostable editor.
- **Sketch** — via the Tokens Studio Sketch plugin.
- **Hand-authoring** — designers edit DTCG JSON directly; this is also the path most accessible to AI agents, which author DTCG natively.

The customer chooses the editor; the substrate does not require a particular one. DTCG is the common denominator. The substrate stays editor-agnostic by construction, with no commercial incentive to favour any particular editing tool.

## IBM Carbon as the floor

The substrate imports IBM Carbon's primitive token vocabulary as the floor layer of every new instance. Color naming follows Carbon's convention (`gray-10` through `gray-100`, `blue-10` through `blue-80`). Type scale follows Carbon's productive and expressive families. Spacing follows Carbon's 8px grid. Motion follows Carbon's productive and expressive easing curves. Focus ring follows Carbon's WCAG 2.2 AAA-conformant style.

Brand-specific work happens at the semantic layer (`themes/<brand>/`), not the primitive layer. SMB customers extend with brand overrides without re-learning a new component taxonomy.

Carbon was chosen for three reasons:

1. **Familiarity surface.** Among the global design-system practitioner population, Carbon carries one of the widest accessible-design muscle-memory footprints. The convention is cognitively cheap to recover.
2. **Accessibility floor.** Carbon ships with WCAG 2.2 AAA conformance built into its primitive choices.
3. **Permissive licensing on the form.** Carbon's token values are publicly documented; the IBM Plex font is permissively licensed; the naming convention is a documentation artefact, not a trademarked asset.

What is NOT imported from Carbon: IBM Cloud-specific themes, React-specific component implementations, the IBM logo and "Carbon" wordmark, Carbon-specific component micro-interactions.

A planned future milestone may introduce an alternative primitive bottom. Untitled UI (MIT-licensed, no brand association) is a candidate for a second primitive layer in a subsequent release. That work is intended and subject to technical evaluation; no timeline is committed.

*Forward-looking statement: the preceding sentence describes intended product direction. Actual milestones depend on engineering capacity, licensing confirmation, and customer prioritisation. This constitutes forward-looking information under `[ni-51-102]` and `[osc-sn-51-721]`.*

## The AI codegen frontier

In the 2026–2030 design tooling environment, an SMB's design-system substrate is a medium. Its form — machine-readability, editor-agnostic interop, self-hostability, AI-consumable research — shapes how the SMB's brand intent reaches every customer-facing surface. Marshall McLuhan's observation that "the medium is the message" (*Understanding Media*, 1964) describes this property at the level of communications media; the substrate operationalises it at the level of an SMB's design decisions.

What the substrate's AI consumption pattern looks like in practice:

- An AI agent generating UI for an SMB-tenant surface registers `https://design.<smb-name>.com/mcp` as a Model Context Protocol `[mcp-spec]` server in its agent runtime.
- At UI-generation time, the agent calls `list_tokens` to fetch the DTCG bundle, `list_components` to discover the SMB's component recipes, and `list_research` to discover available decision rationale.
- For any non-trivial generation step, the agent fetches the relevant research entry and reads the brand-voice rules, accessibility targets, and anti-patterns before deciding what to generate.
- The output aligns with the SMB's brand intent without re-deciding the same questions each session.

The first self-hosted substrate shipping a complete MCP layer (tokens + component APIs + research entries) is intended to maintain an 18–24 month structural lead before mainstream tooling converges on the same pattern.

*Forward-looking statement: the 18–24 month structural lead estimate is based on assumptions about competitive market evolution that may change. This constitutes forward-looking information under `[ni-51-102]` and `[osc-sn-51-721]`.*

## Customer fork procedure

The catalog entry is the productized substrate. An SMB customer forks by cloning the source repository, building the substrate engine (a native Rust binary), initialising a vault from the canonical template, editing their brand's semantic layer in `themes/<smb-brand>.json`, and running the provided bootstrap script to configure the service and TLS. The operator runbook at `vault-privategit-design/GUIDE-deploy-design-substrate.md` covers the full procedure.

The customer ends up with a fully self-hosted, customer-owned design-system substrate. No SaaS dependency. No hyperscaler runtime. Their theme files and any research entries they author are their work product, in their Git repository, signed by their key.

## What makes the substrate structurally distinct

Some of the substrate's structural choices might appear replicable by platforms already operating at scale. On close examination they are not:

1. **Per-tenant Git ownership** requires a per-tenant signing identity (the customer's `allowed_signers` chain). Platforms hosted on shared infrastructure cannot accommodate this without becoming a Git hosting provider — which is a fundamentally different business.
2. **AI-readable research backplane in customer-owned form** requires per-customer hosting. A platform can publish its own design research; it cannot publish the SMB customer's research, because it does not host the SMB customer's design system.
3. **Customer-rooted attestation.** The substrate's TSA pattern combines the WORM ledger, Sigstore Rekor anchoring `[sigstore-rekor-v2]`, and per-tenant `allowed_signers`. The resulting attestation covers the customer's design data — not the platform provider's controls.
4. **Editor agnosticism.** Commercial design-system platforms have an incentive to keep the customer in their editor ecosystem. The substrate has no such incentive — DTCG is the common denominator and the substrate is editor-neutral by construction.

The four properties compound. Removing any one weakens the others.

## What the substrate is NOT

- The substrate is **not** a Storybook replacement. Storybook is a parallel renderer; the substrate owns its rendering.
- The substrate is **not** a design editor competitor. Design editors (Figma, Penpot, Sketch) are the tools designers work in; the substrate is the canonical store those editors interoperate with via DTCG.
- The substrate is **not** a SaaS platform. It is self-hosted by design. A managed-hosting option for SMB customers who prefer not to operate the service themselves is a planned future offering, subject to operator capacity and customer demand; the substrate code will remain self-hostable in all cases.
- The substrate is **not** a JavaScript-framework choice. Components are HTML+CSS+ARIA recipes; the customer's chosen framework consumes the recipe.
- The substrate is **not** a container artefact. Per the zero-container-runtime convention, the substrate ships as a native binary deployed via systemd.

*Forward-looking statement: the managed-hosting option described above is intended future direction and is not a commitment. Availability depends on engineering and operational capacity. This constitutes forward-looking information under `[ni-51-102]`.*

## Where to look next

**Operational documentation:**

- Substrate engine source — `pointsav-monorepo/app-privategit-design/`
- Catalog entry — `pointsav-fleet-deployment/vault-privategit-design/`
- Operator runbook — `vault-privategit-design/GUIDE-deploy-design-substrate.md`
- Canonical vault template — `pointsav-design-system/dtcg-vault/`

**Doctrine and convention:**

- Doctrine claim #38 — `DOCTRINE.md` §III row 38
- Convention — `conventions/design-system-substrate.md`
- Cluster manifest — `clones/project-design/.claude/manifest.md`

## See also

- [The Compounding Substrate](topic-compounding-substrate.md)
- [Substrate-native compatibility](topic-substrate-native-compatibility.md)
- [The Reverse-Funnel Editorial Pattern](topic-reverse-funnel-editorial-pattern.md)
