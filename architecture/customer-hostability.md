---
schema: foundry-doc-v1
title: "Customer Hostability"
slug: customer-hostability
category: architecture
type: topic
quality: core
short_description: "Customer hostability is the architectural commitment that every PointSav artefact can run on the customer's own hardware, against the customer's own keys, with the customer's own audit ledger — making self-hosted deployment the canonical pattern, not a tier."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: customer-hostability.es.md
---

# Customer Hostability

> Customer hostability is the architectural commitment that every PointSav artefact can run on the customer's own hardware, against the customer's own keys, with the customer's own audit ledger — making self-hosted deployment the canonical pattern, not a tier.

**Customer hostability** is the architectural commitment that every artefact a customer adopts can be run on the customer's own hardware, with the customer's own data, against the customer's own keys, with the customer's own audit ledger. The customer can fork it on day one.

This is not a pricing tier or a deployment option. It is the shape of the substrate. A version of Foundry that requires hosted-by-vendor infrastructure to function is, by construction, not Foundry.

## What self-ownership means

Three concrete commitments, each operationally testable:

1. **Self-hostable bootstrap.** Every Foundry service ships with a `bootstrap.sh` that brings the service up on the customer's own machine — no SaaS dependency, no provider login, no metered API. The pattern is established by the `infrastructure/local-slm/`, `infrastructure/local-doorman/`, and `infrastructure/local-knowledge/` precedents.
2. **Per-tenant adapters in the customer's filesystem.** When the customer's adapter trains on the customer's corpus, the resulting `.lora` lives at `data/adapters/` inside the customer's substrate. It never traverses the vendor's network. Loss-of-adapter risk falls on the customer's backup discipline, not on the vendor's continued operation.
3. **Customer-anchored audit ledger.** The apprenticeship corpus that records every editorial action and verdict lives at `data/training-corpus/apprenticeship/<task-type>/<tenant>/` inside the customer's substrate. Tenant-private records never leave per Doctrine §IV.b strict isolation.

## Why hyperscaler economics preclude this

Hyperscaler economics depend on central training, shared trust roots, and provider-rooted attestation. Per-customer continued pretraining does not pencil at SMB scale on those economics:

- Central training requires central data; customer-on-metal training requires the opposite.
- Shared trust roots concentrate the regulatory burden at the provider; customer-anchored attestation distributes it to the customer.
- Provider-rooted attestation makes a customer audit a vendor audit; customer-anchored attestation lets the customer audit themselves.

Foundry is built so the customer's regulatory posture does not depend on the vendor's. A BCSC reporting issuer per `[ni-51-102]` who deploys Foundry inside their own substrate can satisfy continuous-disclosure obligations against records they own and control. A vendor outage does not impair their ability to respond to a regulator's request.

## Bootstrap pattern

Each service ships with three artefacts:

| Artefact | Purpose |
|---|---|
| `bootstrap.sh` | Brings the service up on the customer's machine — installs systemd unit, configures storage paths, sets defaults. |
| `bootstrap.es.sh` | Spanish-language operator-friendly variant where applicable. |
| `MANIFEST.md` | Declares what this deployment provides, the substrate version it inherits from, and the operational state. |

Three already in production:

- `infrastructure/local-slm/` — local OLMo-3 inference
- `infrastructure/local-doorman/` — Tier-A routing on the workspace VM
- `infrastructure/local-knowledge/` — wiki-engine bootstrap

Each was built to the same shape so a Foundry-shaped customer substrate is predictable: the customer reads one bootstrap runbook and applies it across services.

## What customer hostability is not

It is not "open source under a permissive licence." Permissive licensing is necessary but not sufficient. A permissively-licensed service that requires a hosted control plane to function does not satisfy customer hostability — the customer cannot fork it without forking the control plane.

It is not "the vendor will host it for you." Vendor-hosted deployment is one operational option among several. Foundry runs at `documentation.pointsav.com` because PointSav itself is the canonical-tier customer of every package PointSav ships. Customer-hosted deployment is the canonical pattern; vendor hosting is a convenience.

It is not "you can export your data." Data export is a feature. Customer hostability is structural — the substrate does not have a data-export feature because the data was already on the customer's hardware from the moment it was written.

## Forward-looking — federated continued pretraining

Per `[osc-sn-51-721]`, the language describing the federated continued-pretraining trajectory is forward-looking. The shape is in place; the operational throughput matures over time.

The trajectory: a customer's adapter trains on the customer's corpus inside the customer's substrate (Tier B Yo-Yo or the customer's own GPU host). Aggregated improvements may feed back to a shared base model when the customer chooses to contribute, under explicit consent. Customers who do not contribute continue to benefit from base-model improvements driven by customers who do, with no leakage of corpus contents either direction.

This is the federated-LoRA pattern adapted to per-customer data ownership. Reasonable basis: the federated-learning literature 2024–2026 and the LoRA-aggregation work surveyed in the language-protocol-substrate convention §1.

## Operational test for customer hostability

A new Foundry service is customer-hostable if a customer can:

1. Clone the relevant repos.
2. Run `bootstrap.sh` on a machine they own.
3. Generate, store, and serve adapters from local disk.
4. Operate the service against the customer's data without ever contacting a vendor endpoint.
5. Audit every request, response, and adapter-update locally.

Each of these is testable in CI. A service that fails any test is, by definition, not customer-hostable yet — and the gap is treated as a defect, not a feature.

## See Also

- [[language-protocol-substrate]]
- [[anti-homogenization-discipline]]
- [[compounding-substrate]]
- [[contributor-model]]

## References
