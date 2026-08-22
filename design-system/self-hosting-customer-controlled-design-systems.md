---
schema: foundry-doc-v1
title: "Self-hosting a design system, and why it's separate from using the tokens"
slug: self-hosting-customer-controlled-design-systems
short_description: "Explains the two distinct offers of the PointSav Design System — using the Apache-2.0 token data directly, which requires nothing, and separately self-hosting the serving engine to run a different organization's own in-house design system — including the real five-step fork procedure, the three-variable configuration surface, git-based governance, and the precise license boundaries between token data, server source, and article text."
category: design-system
type: topic
content_type: topic
quality: complete
index_group: token-concepts-and-tooling
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: self-hosting-customer-controlled-design-systems.es.md
cites: []
---

The PointSav Design System makes two offers, and they are aimed at different
readers. The first — the primary one — is the token data itself: color,
typography, spacing, motion, content-voice, and document-format decisions
published as W3C DTCG-format JSON under Apache-2.0. Anyone can use it the way
teams use IBM's Carbon or Google's Material — pull the token graph into a
build and go. Nothing else is required: no account, no server, no fork, no
relationship with PointSav at all.

The second offer is self-hosting the engine that serves this site. That offer
is not a bigger version of the first, and it is not a way to mirror PointSav's
tokens on your own hardware. It is for a different organization that wants to
build and run its **own** design system — its own tokens, its own brand, its
own domain — on the same publishing machinery PointSav runs, addressing the
same enterprise-tier-pricing market gap that [[design-philosophy]] describes
for PointSav's own substrate. The two offers are separable by design, and
conflating them misstates both. This article explains each on its own terms,
and exactly where the line between them sits.

## Using the tokens requires nothing

The design-token *format* problem is solved. The W3C Design Tokens Community
Group published the first stable version of its Format Module in October
2025, and the format is implemented across the major authoring and build
tools. PointSav's token graph — over 200 resolved leaf tokens across primitive,
semantic, and dark-theme tiers, growing as the system does — is published in that
format, under Apache-2.0, in a public git repository.

That is the whole transaction. A team that wants the tokens clones or
downloads the data, resolves it with whatever tooling it already uses, and
ships. The tokens do not phone home, do not require the PointSav server to
exist, and carry no obligation beyond Apache-2.0's attribution terms. If
design.pointsav.com disappeared tomorrow, every copy of the token data would
keep working, because the data was never coupled to the service that
publishes it.

If that is what you came for, you can stop reading here.

## What self-hosting actually is

Self-hosting addresses a different problem: not "how do I consume a token
graph" but "how does my organization govern, version, document, and publish
its own token graph over time." The software that does this — the layer
occupied commercially by zeroheight, Supernova, Knapsack, and similar
platforms — is delivered almost exclusively as vendor-hosted
software-as-a-service, which requires the customer's token data to live on
the vendor's infrastructure. The zeroheight Design Systems Report 2026 finds
that only 40% of surveyed teams have an automated token pipeline at all; the
rest synchronize by hand. And for a specific class of buyer — financial
services, legal, government — vendor hosting is not merely inconvenient but
frequently disqualifying, because the compliance posture that governs where
an organization's artifacts may reside rarely carves out an exception for
design assets. Research on cloud vendor lock-in documents the underlying
asymmetry: Opara-Martins, Sahandi and Tian, surveying 114 enterprise
practitioners in 2016, identified data portability and integration
incompatibility as the dominant lock-in risks once assets move to
vendor-controlled infrastructure.

The self-hosting offer is the engine behind this site, run by another
organization for that organization's own system. The forking company does
not inherit PointSav's brand decisions — it replaces them. What it inherits
is the machinery: the vault structure, the token-gallery rendering, the
resolved-export pipeline, the machine-readable endpoints, and the governance
model. PointSav's own tokens are, to a self-hosting customer, example
content.

## The mechanism: fork and run

The documented procedure is five steps: fork the public repository; clone
the fork to your own server; edit the vault's themes directory to declare
your brand's primitive overrides; run the serving binary pointed at your
vault directory; put your own reverse proxy and TLS certificate in front of
it, under your own domain.

The entire tenancy-configuration surface is three environment variables.
`DESIGN_VAULT_DIR` names the filesystem path to your vault. `DESIGN_TENANT`
names your brand, matching a theme filename in that vault. `DESIGN_BIND`
names the address the process listens on. One binary serves one tenant's
vault per process — there is no multi-tenant database and no shared
infrastructure between one organization's deployment and another's. Nothing
in the procedure transmits your token or theme data to PointSav, and the
running instance makes no request-time call to PointSav's infrastructure.
Moving providers, or taking the deployment fully offline for an audit, means
moving a directory and restarting a process, because there is no data-export
step: the data never lived anywhere but your own repository.

Governance comes from the same place. Hosted platforms provide edit
permissions, version history, and change review through application-layer
controls on a vendor-operated database; the fork-and-run model provides the
equivalent through the customer's own version control. Token changes are
commits, edit rights are branch protection, history is the git log, review
is a pull request — infrastructure a regulated buyer already operates and
has already audited.

## Which license applies to what

The two offers also split cleanly at the license boundary, and precision
here matters:

- **Token and component data — Apache-2.0.** The DTCG JSON, component
  recipes, and research files in the design-system repository. This is the
  layer you consume directly, and the layer a fork replaces with its own
  content.
- **Server source — AGPL-3.0-or-later.** The serving engine
  (`app-privategit-design` in the PointSav monorepo). Running it unmodified
  for your own organization carries no unusual burden; an organization that
  modifies the server and offers it to users over a network takes on AGPL
  Section 13's obligation to offer those users the modified source. For
  organizations that cannot accept that obligation, the project's licensing
  matrix ratifies a commercial Apache-compatible alternative tier; its exact
  presentation to self-hosting customers is still being settled.
- **This article — CC BY 4.0**, the license of the documentation wiki it is
  published in. The article text is neither token data nor server source,
  and none of the three licenses stands in for the others.

## Scope and limits

Stated plainly: the fork procedure is documented, and each of its steps uses
ordinary, independently verifiable tooling — git, environment variables, a
systemd unit, a reverse proxy. But as of this writing no organization outside
PointSav has run the procedure end-to-end in production; PointSav's own
instance is the only deployment. Every claim in this article about external
self-hosting is therefore architectural and procedural — a pattern the
system is built and intended to support — not a report of observed
third-party adoption. The companion research manuscript states the same
limitation, alongside a falsification programme for the claims involved, and
this article prefers to publish with that status visible rather than imply a
customer base it cannot show.

---

*This article is background for readers of the PointSav Design System
documentation deciding which of the two offers they need. The operational
runbook for the fork procedure is maintained separately as a guide; the
research-grade treatment of the architecture, including its formal hypotheses
and limitations, is the companion manuscript on customer-controlled
design-system infrastructure.*
