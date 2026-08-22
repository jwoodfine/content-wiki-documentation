---
schema: foundry-doc-v1
title: "app-mediakit-marketing — agent-authored marketing landing server"
slug: app-mediakit-marketing
category: applications
type: concept
content_type: topic
quality: complete
index_group: knowledge-and-editorial-applications
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: app-mediakit-marketing.es.md
short_description: "app-mediakit-marketing is a Rust web server delivering marketing landing sites from typed page manifests — AI authors via MCP, a human approves before anything publishes. Serves home.woodfinegroup.com and home.pointsav.com."
cites: []
---

`app-mediakit-marketing` is a Rust web server that delivers marketing landing sites — server-rendered, agent-first. A page is a typed manifest, not free-form Markdown or HTML: it composes a title, description, language, and an ordered list of typed sections (a hero, for instance) drawn from the shared [[app-mediakit-shell|`app-mediakit-shell`]] section vocabulary. The binary validates every manifest against that vocabulary before it can render, so a manifest either conforms or is rejected — there is no partial or malformed page.

## Agent-first authoring, human-gated publish

Content on this platform is meant to be authored by an AI agent and approved by a human before it goes live, the same [[architecture-decisions|SYS-ADR-10]]/SYS-ADR-19 human-checkpoint pattern applied elsewhere on the platform. An MCP server, mounted at `POST /api/mcp` when explicitly enabled, exposes tools an AI author calls directly: list the available section types, read an existing page, validate a draft manifest against the section contract, propose a new or revised page, and list what's currently pending.

An AI author never writes to the live content tree. `propose_page` validates the manifest and stages it as a pending item; nothing is published until a human reviews the proposed manifest against what's currently live and approves it. There is no automated publish path.

## Architecture

### Binary

A single statically linked Rust binary (`app-mediakit-marketing`) runs the server, built on Axum. No runtime dependencies beyond the OS kernel and a libc.

### Multi-tenant via environment variables

A single binary supports multiple tenants. Tenant identity is set at startup via `SERVICE_MARKETING_MODULE_ID` (e.g., `woodfine`, `pointsav`); content directory, bind port, and site title resolve from this value.

Two instances running the same binary on the same host demonstrate this:

| Instance | Tenant | Domain | Port |
|---|---|---|---|
| media-marketing-landing-1 | woodfine | home.woodfinegroup.com | 9102 |
| media-marketing-landing-2 | pointsav | home.pointsav.com | 9101 |

Each instance is a systemd service with its own unit file and environment block. Neither instance knows about the other.

## Sovereignty and Tier 0 alignment

The [[compounding-substrate|Compounding Substrate]] discipline defines Tier 0 as an operator-owned system that functions without any vendor cloud dependency. `app-mediakit-marketing` meets this bar:

- Single binary with no external runtime dependencies
- File-based content storage — page manifests on disk, no database
- nginx reverse proxy handles TLS; no managed load balancer required
- Runs on the smallest commercially available VPS ($7/month)

An SMB operator can run their own marketing landing site on hardware they own, with software built from auditable source, without any ongoing vendor relationship.

## Deployment pattern

`app-mediakit-marketing` is deployed behind nginx. nginx handles:
- TLS termination (Let's Encrypt via certbot)
- Static file serving for `robots.txt` and `sitemap.xml`
- HTTP→HTTPS redirect
- Reverse proxy to the binary's loopback port

The binary never listens on a public port. All public traffic passes through nginx.

```
Internet → nginx :443 (TLS) → 127.0.0.1:PORT → app-mediakit-marketing
                              │
                              └→ CONTENT_DIR/ (page manifests)
```

## Live reference deployments

Two deployments are active as of 2026-05-07 on `foundry-workspace`:

- **home.woodfinegroup.com** — MCorp customer-tier marketing site. Demonstrates the customer pattern: operator-branded, operated under the customer's identity.
- **home.pointsav.com** — PointSav vendor-tier open reference deployment. Demonstrates the vendor pattern: a public reference that prospective customers can inspect before deploying their own instance.

Both sites run the same `app-mediakit-marketing` binary. The difference is content and theme tokens.

## See also

- [[app-mediakit-knowledge]] — sibling Rust server for knowledge-base content (same architectural pattern)
- [[app-mediakit-shell]] — the shared typed-section vocabulary this crate composes pages from
- [[compounding-substrate]] — sovereign architecture discipline
- [[totebox-archive]] — the Totebox Archive that holds canonical content for each tenant
