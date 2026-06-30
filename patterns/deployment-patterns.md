---
schema: foundry-doc-v1
title: "Deployment patterns"
slug: deployment-patterns
category: patterns
type: concept
content_type: topic
quality: complete
short_description: "Deployment patterns describes the six canonical configurations in which the PointSav substrate is deployed — each built on the same five primitives and OS surface, with the Chart of Accounts and compliance surface adapted per segment."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: deployment-patterns.es.md
references:
  - id: 1
    text: "Jackson, Cam. 'Micro Frontends.' martinfowler.com, 2019. The foundational technical article describing the micro-frontend architectural pattern applied in modern web engineering."
    url: "https://martinfowler.com/articles/micro-frontends.html"
  - id: 2
    text: "The Open Group, TOGAF Standard, 10th Edition, 2022. Chapter 20: Architecture Patterns. Canonical treatment of reusable deployment configurations in enterprise architecture."
    url: "https://www.opengroup.org/togaf"
---

Deployment patterns describes the six canonical configurations in which the PointSav substrate is deployed across different institutional contexts, each built on the [[three-ring-architecture|three-ring architecture]]. Each configuration rests on the same five primitives — People, Communications, Drafts, Records, Money — and the same [[console-os|Command Ledger]] surface; what changes per configuration is the [[archetypes-and-chart-of-accounts|Chart of Accounts]] and the compliance surface. The substrate does not fork across segments; it adapts. By the end of this article, a reader will understand the Companion positioning, the six canonical patterns, and the micro-frontend isolation model that makes independent-versioning practical across all six.

## Five primitives that span every institutional context [^2]

Every context in which institutional users operate maps to the same five primitive categories of records. A regulated professional managing patient files, a litigator managing case discovery, and a household managing tax receipts each maintain documents that fall into exactly these categories:

| Primitive | What it covers |
|---|---|
| People | Contacts, personnel records, identity relationships |
| Communications | Email, correspondence, meeting records |
| Drafts | Work in progress — documents under active authorship |
| Records | Signed, sealed, or executed documents |
| Money | Financial records, invoices, ledger entries |

The [[console-os|Command Ledger]] exposes each primitive as a dedicated F-key surface. The operator presses a key; the chassis loads the relevant plugin; the plugin displays the records for that primitive within the current [[totebox-os|Totebox]] context. No context switch between segments requires a different architecture — the five primitives are universal.

## How the platform operates alongside incumbent tools

The platform is positioned as a complementary engine, not a replacement for existing operational tools. Customers continue to use the professional and productivity applications they already operate; the substrate runs alongside, routing records from those applications into sovereign [[totebox-os|Totebox]] archives.

| Incumbent tool category | What the substrate adds |
|---|---|
| Professional email client | [[service-email|service-email]] ingests each message into a WORM Maildir; the cloud copy may rotate while the sovereign copy remains sealed |
| Spreadsheet applications | The intended sovereign spreadsheet surface stores executed financial models in the [[worm-ledger-design|WORM ledger]] |
| Word-processing applications | The intended sovereign word-processing surface uses Typst for print-fidelity output; F4 in the [[console-os|Command Ledger]] synthesises content from structured records |
| Professional networking platforms | [[service-people]] is intended to harvest verified contact data into the Totebox identity ledger |
| Corporate document repositories | service-minutebook cryptographically seals signed records against the [[worm-ledger-design|WORM ledger]] substrate |

The customer is not asked to abandon any working tool. The substrate operates in the background; the Command Ledger provides a sovereign view over the records the incumbent tools produce.

## Six canonical deployment configurations

The six configurations represent distinct GUIDE families in the fleet-deployment catalogue. Each is a configuration, not a separate product; the underlying [[totebox-os]], [[console-os|os-console]], and services are identical across all six.

| Configuration | Primary records | [[archetypes-and-chart-of-accounts|Chart of Accounts]] adaptation |
|---|---|---|
| Real-property asset manager | Lease documents, building information models, tenant communications, permits | Real Estate / Leasing / Tenants / Municipalities anchors |
| Public-company Reporting Issuer | Press releases, regulatory filings, board minutes, executive commentary | Investor Relations / Finance / Media anchors |
| Medical or surgical practice | Patient records, diagnostic files, clinical billing | Compliance and Local Administration anchors |
| Law firm | Case files, discovery materials, signed court filings | Compliance / Counsel anchor |
| Family office | Tax records, estate documents, household contracts | Adapted Personnel and Local Administration anchors |
| Household | Receipts, warranties, family correspondence | Simplified single-Profile Chart |

Each row is a configuration, provisioned from a named template in the fleet-deployment catalogue. The pattern for a real-property deployment differs from the pattern for a law firm only in its Chart of Accounts configuration and compliance surface — the underlying substrate components are identical.

## Micro-frontend isolation inside the Command Ledger [^1]

The [[console-os|Command Ledger]] is not a monolithic HTML application. It is an empty chassis that loads small, isolated plugins on demand. When the operator presses F2, the chassis requests the `/app-console-people/` view; when they press F3, it destroys that view and loads `/app-console-email/`.

| Isolation property | Effect |
|---|---|
| Mathematical disk isolation | The People plugin cannot read the Email plugin's state; they occupy separate directory trees |
| Independent versioning | An update to the Bookkeeper plugin does not require an update to the Content plugin |
| Bandwidth efficiency | Only the active plugin's HTML, CSS, and JS is loaded; the rest remains on disk |
| No external dependency | No CDN, no third-party UI library, no telemetry; plugins ship inside the same binary as the chassis |

The isolation model is derived from the micro-frontend architectural pattern[^1] applied with sovereign discipline: the entire surface ships as a single Rust binary, no plugin fetches assets from an external host, and no plugin can observe another plugin's state. The isolation is mathematical — a property of the directory structure — not a security policy that must be enforced at runtime.

## How deployment templates map to the fleet catalogue

Each canonical configuration has a corresponding subdirectory under the fleet-deployment catalogue. The customer-facing catalogue is the public record of how the substrate is operated for each configuration type.

| Template | Function | Status |
|---|---|---|
| `vault-privategit-source-1` | Internal source-control deployment; the workspace is an instance of this template | Active |
| Real-property asset-management | The reference operational deployment for a real-property firm | Planned |
| Reporting Issuer | An [[mediakit-os]] and [[totebox-os]] pair for public-company disclosure | Planned |

Templates in the Showcase Layer correspond to numbered instances in the Instance Layer — private to the operator, gitignored from all public repositories. See [[three-layer-architecture]] for the three-layer model.

## The visible-operational-first deployment cadence

Deployment patterns are launched with a visible-operational-first cadence: the URL resolves and a recognisable surface answers before any polish or hardening work begins. A pattern that has not yet been provisioned as a working deployment is described in planning terms, not as live infrastructure.

This cadence prevents two common failure modes: designs that are specced but never built, and builds that are technically complete but never publicly visible. The definition of "operational" is strict — the URL must resolve to a surface a human can use — and that bar is cleared before any configuration is described as deployed.

## See also

- [[three-ring-architecture]] — the ring architecture that each configuration deploys
- [[three-layer-architecture]] — the Software / Showcase / Instance three-layer model underlying the template catalogue
- [[archetypes-and-chart-of-accounts]] — the Chart of Accounts taxonomy that adapts per configuration
- [[console-os|os-console]] — the Command Ledger surface common to all six configurations
- [[totebox-os]] — the Totebox operating system that hosts each configuration's archives
- [[self-host-a-deployment]] — step-by-step guide: deploy a configuration from this catalogue on customer-owned infrastructure
