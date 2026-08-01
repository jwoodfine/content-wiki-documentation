---
schema: foundry-doc-v1
title: "MCP and AI-agent-consumable design systems"
slug: mcp-ai-agent-consumable-design-systems
short_description: "Explains why the PointSav Design System exposes a machine-readable surface — an on-prem Model Context Protocol endpoint, a token search API, and a DTCG token export — so AI coding agents can query current token and component data from the same registry that renders the human-facing documentation, without any query leaving the host's own infrastructure."
category: design-system
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: mcp-ai-agent-consumable-design-systems.es.md
cites: []
---

A design system is only as reliable as the code written against it. When that
code is written by an AI coding agent, the agent's picture of the system —
which tokens exist, what they resolve to, what the current markup for a
component is — usually comes from a training snapshot or a pasted excerpt of
the documentation. Both go stale the moment the system moves. The PointSav
Design System addresses this by publishing a machine-readable surface
alongside its human-readable one: a Model Context Protocol endpoint, a token
search API, and a versioned token export, all answered from the same registry
that renders every documentation page. An agent asking what a token resolves
to gets today's answer, from the same data a human reader is looking at.

Because the design system's server is self-hostable, that surface runs on the
adopting organization's own infrastructure. Every agent query — a single
token lookup or a full component sweep — is answered locally. Nothing about
the organization's codebase, prompts, or component usage is sent to a third
party.

## What MCP is

The Model Context Protocol (MCP) is an open protocol for connecting large
language model applications to external tools and data sources. Anthropic
introduced it in November 2024, and it has since been adopted broadly across
the industry, including by other major AI providers. The specification is
published openly at modelcontextprotocol.io; the revision current at the time
of writing is dated 2025-11-25.

Technically, MCP is a JSON-RPC 2.0 message protocol between three parties: a
host (the LLM application — a coding agent, an IDE assistant), a client (the
connector inside that host), and a server (the service exposing context and
capabilities). Servers offer three kinds of primitives: tools the model can
call, resources it can read, and prompt templates. The specification cites
the Language Server Protocol as an inspiration — the same way LSP let any
editor speak to any language toolchain, MCP lets any agent speak to any
context provider without a bespoke integration per pair.

One further property of the specification matters for this article: its
security section is explicit that hosts must obtain user consent before
exposing data to servers and must not transmit resource data elsewhere
without consent. The protocol anticipates deployments where the data behind
the server is private. A design-system server running on an organization's
own hardware is squarely that case.

## Design systems as agent context — prior art

Serving design-system context to coding agents over MCP is an established
pattern, not a PointSav invention. Figma ships a Dev Mode MCP server that
lets agents in tools such as VS Code, Cursor, and Claude Code read component,
style, and variable context from Figma files, and has argued publicly that
MCP servers are the mechanism by which design systems become useful to AI
tooling. zeroheight offers an MCP integration that surfaces a team's
component guidance, tokens, and usage rules to coding agents from its hosted
documentation platform.

What distinguishes this design system's implementation is not the idea but
the deployment model and the data path. The offerings above are hosted
services: the design-system context lives with a vendor, and agent queries
transit that vendor's infrastructure. Here, the MCP server ships inside the
same self-hostable binary as the documentation site itself. There is no
hosted variant of this surface — on-premises is the only way it is offered —
and there is no second copy of the data: the endpoint reads the same registry
the site's pages are rendered from.

## The machine surface, concretely

The design-system server exposes three machine entry points.

- **`POST /mcp`** — the MCP endpoint. It speaks JSON-RPC 2.0 per the
  specification and exposes four tools: `list_components` (every component
  the registry knows, filterable by origin), `get_component_recipe` (the
  HTML, CSS, ARIA guidance, consumed tokens, and variants for one named
  component — the same recipe the site renders live previews from),
  `get_token` (resolve a single design token by its CSS custom property name
  or its DTCG path), and `search_design_system` (full-text search across
  components, tokens, and research notes, for an agent that does not yet know
  the exact name of what it needs).
- **`GET /tokens/search`** — the same token index as a plain HTTP query, for
  tooling that would rather make an ordinary request than speak MCP.
- **`GET /bundles/:name/download`** — versioned file bundles, including the
  full token export in Design Tokens Community Group (DTCG) format. An agent
  or build pipeline that only needs token values can pull this file directly
  and never touch the MCP endpoint at all.

The design principle tying the three together is single-sourcing. Token
counts on the documentation pages, live component previews, MCP tool
responses, and the DTCG export are all read from one registry. If the
registry is wrong, everything is wrong in the same way at the same time —
there is no machine-only code path that can drift while the human-facing site
looks fine, and no cached mirror of the docs for an agent to trust after it
has gone stale.

## Why the token layer is the right altitude

An agent generating interface code does not need discretion over visual
decisions; it needs a small, current vocabulary of valid ones. Constraining
generation to the design system's token and component vocabulary — and giving
the agent a live way to query that vocabulary — narrows what can go wrong in
generated code to the range the system allows. The agent selects a semantic
token rather than inventing a hex value, and reuses a component recipe rather
than approximating one from memory. This is the same argument that justifies
design tokens for human teams, applied to a consumer that reads JSON more
fluently than it reads prose.

## Licensing

Two different licenses apply to the material this article discusses, and the
distinction is worth being precise about. The design-token data — the DTCG
JSON that agents, plugins, and build pipelines consume — is published under
Apache-2.0, the same convention used by major open design systems. The server
that answers MCP and registry queries is published under AGPL-3.0-or-later.
And this article itself, as part of the documentation wiki, is licensed
CC BY 4.0 — a content license, distinct from both. Consuming the tokens
carries Apache-2.0 terms; running the server carries AGPL terms; reusing this
text carries CC BY attribution terms.

## Scope and limits

Stated plainly: the endpoint set described above — `/mcp` with its four
tools, `/tokens/search`, and the bundle download route — is implemented in
the design-system server's source and is the surface a self-hosted instance
exposes. The v3 public documentation of that surface, including the Agents
page that presents it to human readers, is under operator review at the time
of writing and is described here in terms of the server capability, not of
any specific published page. No claim is made about agent code quality
improving by a measured amount; the single-registry architecture is a design
decision whose rationale is given above, not a benchmarked result. Comparisons
to hosted offerings are structural — deployment model and data path — and are
based on those vendors' own public documentation as of this writing.

---

*This article is background for readers encountering the design system's
machine-integration surface for the first time, ahead of the operational
guide on connecting a specific agent to a self-hosted instance.*
