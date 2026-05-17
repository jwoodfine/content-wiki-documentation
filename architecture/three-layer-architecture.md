---
schema: foundry-doc-v1
title: "Three-layer architecture"
slug: three-layer-architecture
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: three-layer-architecture.es.md
short_description: "PointSav deliverables move through three architectural layers — SOFTWARE (vendor monorepo), SHOWCASE (customer deployment catalogue), and INSTANCES (private running deployments) — with a strict one-way flow from vendor to customer to operator that separates public demonstration from operational reality."
cites: []
---

PointSav deliverables move through three architectural layers, each with a distinct purpose, a distinct audience, and a distinct ownership posture. The first layer is the vendor monorepo — the canonical home of every line of code in the family. The second is the customer's public catalogue of deployment patterns — operational runbooks and manifests showing how the vendor substrate is used in practice. The third is the private layer of actual running deployments, local to the operator and never committed to any shared repository.

## The three layers

| Layer | Name | Lives at | Visibility | Owner |
|---|---|---|---|---|
| 1 | SOFTWARE | `pointsav/pointsav-monorepo` | Public | PointSav Digital Systems (vendor) |
| 2 | SHOWCASE | `woodfine/woodfine-fleet-deployment` | Public | Woodfine Management Corp. (customer reference catalogue) |
| 3 | INSTANCES | Local storage on operator hardware | Private — not tracked in any shared repository | Each individual operator |

The directionality is strict: vendor builds → customer adopts → operators deploy. There is no reverse path. Customer-side adjustments do not flow back into the vendor monorepo. Operator-specific configurations do not flow back into the customer catalogue.

## Layer 1 — SOFTWARE

The vendor monorepo is the canonical home of every line of code in the PointSav family. All `os-*` operating systems, all `app-*` user surfaces, all `service-*` daemons, and all `system-*` infrastructure crates live here.

| Property | Value |
|---|---|
| Repository | `github.com/pointsav/pointsav-monorepo` |
| Layout | Six-tier sovereignty matrix (`app-*`, `asset-*`, `moonshot-*`, `os-*`, `service-*`, `system-*`) |
| Write access | `ps-administrator` only |
| Read access | Public |
| Commit attribution | Vendor administrator identity, SSH-signed |
| Release cadence | Tag-based, semver |

Contributors do not push directly into this repository. They push to personal forks and open pull requests. The administrator squash-merges; the corporate commit is born; the IP transfer is complete.

## Layer 2 — SHOWCASE

The Showcase Layer is the customer's public-facing catalogue of deployment patterns. It is a curated set of operational runbooks and deployment manifests showing how a customer of PointSav uses the vendor's substrate to operate real businesses.

| Property | Value |
|---|---|
| Repository | `github.com/woodfine/woodfine-fleet-deployment` |
| Layout | One subdirectory per named deployment |
| Write access | `mcorp-administrator` only |
| Read access | Public |
| Content type | `GUIDE-*` operational runbooks; `MANIFEST.md` per deployment |

The Showcase Layer is not a private deployment record. It is the customer's published demonstration of how the vendor's substrate is used in practice — visible to other potential customers, to investors, and to regulators. It functions as a living showroom.

## Layer 3 — INSTANCES

Layer 3 holds the actual running deployments. Each deployment is a numbered instance of a named template from the Showcase Layer. These instances are private to the operator and never appear in any GitHub repository.

| Property | Value |
|---|---|
| Location | Local storage on operator hardware |
| GitHub status | Not committed to any shared repository |
| Required files | `MANIFEST.md`, `README.md` + `README.es.md` |
| Per-deployment customisation | Environment variables, customer-specific keys, local overrides |

The strict privacy rule is structural: a deployment instance contains customer-specific configuration, key material, and operational state. None of it belongs in a public ledger. The Showcase Layer publishes the recipe; the Instance Layer is the actual cooking — in the customer's kitchen, with the customer's ingredients.

## Why three layers, not two

A simpler architecture would collapse Layers 2 and 3: the customer's actual deployments would be the customer's public catalogue. PointSav separates them deliberately:

| Problem with two layers | How three layers solves it |
|---|---|
| Public deployments expose customer-specific keys and configurations | Layer 3 is private; only the Layer 2 template is public |
| Customer hesitates to publish a real deployment | Layer 2 is a catalogue of templates, not real environments |
| Other potential customers cannot see how the vendor's substrate is used | Layer 2 provides exactly that demonstration without exposing operational state |
| Operator updates to a private deployment would dirty the public ledger | Layer 3 instances never appear in any shared repository |

The split is the structural answer to a question every B2B vendor faces: how to demonstrate the product in production without leaking the customer's operational reality.

## The Tetrad

Every PointSav project archive declares four legs — vendor, customer, deployment, and wiki. The three architectural layers above account for three of the four; the fourth is the public documentation content that explains the substrate to human readers. The Tetrad ensures that every project simultaneously has source code in the SOFTWARE layer, a deployment template in the SHOWCASE layer, a real instance in the INSTANCES layer, and explanatory articles in the documentation wiki — and that none of the four is missing.

## See also

- [[five-stage-supply-chain]] — how code moves between the three layers
- [[six-tier-sovereignty-matrix]] — the directory taxonomy that organises the SOFTWARE layer
- [[deployment-patterns]] — the named deployment patterns that populate the SHOWCASE layer
