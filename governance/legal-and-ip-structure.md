---
schema: foundry-doc-v1
title: "Legal and IP structure"
slug: legal-and-ip-structure
short_description: "The three-corporation topology governing IP transfer from contributor to vendor to customer, with squash-and-merge as the atomic IP-transfer event."
category: governance
type: concept
content_type: topic
quality: complete
index_group: licensing-and-contribution
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
paired_with: legal-and-ip-structure.es.md
cites:
 - ni-51-102
 - np-51-201
---

The PointSav legal structure describes the three-corporation topology that governs intellectual property transfer from contributors to vendor to customer. A squash-and-merge git operation serves as the atomic IP-transfer event; the vendor is the only party bridging contributors and the customer. The design is intentional: contributor experimental commits never reach the customer, and the customer's operational records never reach the vendor. This article covers the three-corporation topology, the IP-transfer mechanic, the contributor protocol, the intended license structure, and the planned patent streams.

## The three corporations

PointSav exists inside a deliberate three-corporation topology:

| Entity | Type | Role |
|---|---|---|
| Woodfine Capital Projects Inc. | Parent | Owner of MCorp; PointSav currently operates as its trade name, planned to become a Woodfine subsidiary upon incorporation; real-property operating company |
| PointSav Digital Systems | Trade name (vendor); planned subsidiary upon incorporation | IP holder; designs and builds the technology |
| MCorp | Subsidiary (customer) | Operates real-property assets; PointSav's first and reference customer |

The intercompany flow is unidirectional: vendor builds → customer adopts → customer deploys. PointSav never receives the customer's operational records; the customer never edits vendor source.

## The squash-and-merge IP transfer

The most distinctive legal mechanic is how intellectual property moves from a contributor into the corporate vendor and onward to the customer. The transfer is treated as an atomic legal event implemented through a specific git operation: squash-and-merge.

| Phase | Actor | Action | Legal meaning |
|---|---|---|---|
| Bid | Contributor (`jwoodfine` or `pwoodfine`) | Push and open pull request | Submission of work product; not yet approved or paid |
| Acquisition | Vendor (PointSav) | Squash-and-merge | The contributor's commit history is stripped; a single corporate commit is minted; ownership transfers to PointSav |
| Distribution | Vendor (PointSav) | Tag a release | The audited code becomes a packaged Product Release |
| Procurement | Customer (MCorp) | Upstream sync | The customer pulls only signed release tags from the vendor; never touches the contributor |
| Execution | Production host | Deploy | The customer's licensed copy runs in production |
| Reset | Contributor | Trunk-based rebase | The contributor's local environment is wiped to match the vendor's verified standard, ready for the next cycle |

Squash-and-merge does the legal work because it rewrites history. The contributor's experimental commits, prototype attempts, and abandoned approaches do not survive into the corporate ledger. What survives is a single clean commit owned by PointSav and signed by the system administrator — consistent with the [[canadian-simple-copyright|first-ownership posture]] under Canadian Copyright Act § 13(3).

## The double-blind air-gap

A strict separation governs the three roles:

| Forbidden interaction | Reason |
|---|---|
| Contributor pushing directly to Woodfine repos | Eliminates the possibility of unaudited contractor code reaching the customer |
| Customer reading contributor forks | Eliminates exposure to in-progress or rejected work |
| Vendor permitting either of the above | Would dissolve the vendor as a verification gate |

PointSav (the vendor org on GitHub) is the only entity that sees both contributors and the customer. The bridge runs through the vendor and only through the vendor.

## Contributor assignment protocol

For paid contributors, the binding contract for a specific assignment is a handwritten note, not a digital ticket. The protocol enforces a deliberate, physical record of who agreed to what and when — an authority-of-assignment record that satisfies the documentation requirements of fiduciary and personnel-risk governance. The full contributor taxonomy is described in the [[contributor-model]].

A handwritten note is harder to forge, harder to lose, and clearer in its intent than a digital tracking entry or a messaging-platform thread.

## Contributor roles and fiduciary designation

Canadian regulatory practice distinguishes between roles with fiduciary authority — strategic and financial decision-making — and roles with operational authority — daily execution. PointSav's GitHub permissions reflect this split:

- The `pointsav` and `woodfine` GitHub organisations are owned by both the strategic and operational principals.
- Routine contributions flow through the staging-tier contributor identities (`jwoodfine` and `pwoodfine`), which alternate per commit.
- The system administrator identity (`ps-administrator`) holds the cross-org administrative key material and does not participate in routine staging-tier work.

Strategic and fiduciary decisions are escalated outside the routine contributor tier; the system administrator is the only identity with cross-org write access to canonical repositories.

## License strategy

Licensing follows an open-core model, ratified and assigned at the directory level (root `LICENSE`, "MULTI-LICENSE NOTICE" v1.2, effective 2026-08-02):

| Tier | Coverage | Represents |
|---|---|---|
| AGPL-3.0-or-later | The platform default — `os-console`, `os-workplace`, all `service-*`/`system-*`/`tool-*` (except `tool-wallet`), most `moonshot-*` directories, `app-console-*`, `app-workplace-*`, and workspace tooling | The open core |
| FSL-1.1-ALv2 | `os-totebox`, `os-infrastructure`, `os-privategit`, `os-mediakit`, `os-network-admin`, their `app-*` extensions, and 5 named `moonshot-*` overrides | A source-available tier that converts to Apache-2.0 on a future date |
| Apache-2.0 | `tool-wallet` only | A deliberate override — no revenue role, seeds the open-source binary shelf |
| PointSav-ARR (proprietary) | `os-orchestration` (the `os-interface` rename target) and `app-orchestration-*` | The commercial moat — not distributed under either open tier |

`os-totebox` is FSL-licensed; `os-console` and `os-workplace` are AGPL — the three components carry two different licenses, not one uniform "open core" tier. No "Sovereign Addendum" license extension exists anywhere in the real license text — the running-instance-portability property described below is a design goal, not a distinct license grant. `service-pointsav-link`, the [[diode-standard|Diode]] enforcement adapter, does not exist as a crate in the codebase, so it carries no license assignment.

The pattern follows the open-core model: the AGPL/FSL tiers attract adoption; the PointSav-ARR tier produces revenue.

## Patent strategy (intended)

Two distinct patent streams are planned. All patent claims are forward-looking statements subject to the BCSC continuous-disclosure posture [ni-51-102] [np-51-201]:

| Patent stream | Owner | Subject |
|---|---|---|
| Technical | PointSav Digital Systems (planned) | The seL4 microkernel bridging, the Capability-Based Manager, the [[diode-standard|Diode]] protocol |
| Operational | Woodfine (planned) | The Direct-Hold Solution and the systematic tokenisation of real property as a real asset |

The streams do not overlap: PointSav Digital Systems is intended to patent the substrate; Woodfine is intended to patent the customer business mechanism.

## The Sovereign Data Foundation (planned)

A planned governance partner, the Sovereign Data Foundation, is intended to oversee the integrity of the open-source components of the PointSav substrate. The Sovereign Data Foundation is referred to in planned and intended terms only; no active oversight role, equity position, or governance authority is asserted at this time. All references to the Sovereign Data Foundation in public communications carry planned and intended language only, per the BCSC continuous-disclosure posture [ni-51-102] [np-51-201].

## See also

- [[five-stage-supply-chain]] — the full git supply chain from contributor to customer
- [[diode-standard]] — the unidirectional command flow protocol
- [[compliance-and-continuous-disclosure]] — the BCSC continuous-disclosure posture governing all forward-looking statements in this article
- [[structural-positioning]] — the architectural commitments underlying the vendor/customer separation
