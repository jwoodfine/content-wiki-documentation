---
schema: foundry-doc-v1
title: "Customer-First Ordering"
slug: customer-first-ordering
category: reference
type: topic
quality: published
short_description: The principle that a software vendor building something a customer will install should build it in the same order the customer will install it, on the same substrate the customer will use.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: customer-first-ordering.es.md
---

A software vendor that builds its own tools out of order — shipping the API before the client, the runbook after the deployment, the configuration documentation months after the first user — delivers a product that reflects the vendor's development convenience rather than the customer's operational reality. Customer-first ordering is the discipline that prevents this by making the customer's installation sequence the vendor's build sequence.

## The principle

When building something a customer will install, build it in the same order the customer will install it, on the same substrate the customer will use. The vendor's own deployment of its product is the first installation of that product. If the vendor's installation works cleanly in that order on that substrate, the customer's runbook is true by construction.

## Why vendor-as-first-customer matters

The workspace on which a software platform is developed is declared as an instance of the catalog entry that the platform ships. This is structural, not stylistic: the workspace is the first numbered instance of the deployment it describes. Every package the platform ships is installed on this workspace first, in the same numbered sequence, using the same bootstrap and deploy scripts a customer would run.

The consequence is that gaps in the customer experience surface during vendor development rather than on a customer's first day. If a bootstrap script fails, a configuration file is undocumented, or a dependency is missing from a runbook, the vendor discovers it before publishing. The customer receives a runbook verified against an actual installation.

## Three-layer responsibility

The principle maps to a three-layer responsibility structure:

**Operator-level steps** mirror what the customer does at hardware boundaries — purchasing equipment, configuring network access, running authentication flows against cloud providers from outside the running system. These steps cannot be automated from inside the running system; they require human action at the physical or network boundary.

**Platform-level steps** mirror what the customer does to install and configure the platform — running bootstrap scripts, installing service packages, provisioning runtime infrastructure. These are executed by whoever is playing the customer role in the current development context.

**Feature-level steps** mirror what the customer does to extend the platform — adding data ingest, configuring AI routing, integrating with external services. These are the construction work of the platform itself.

A useful test for any work item: if the step appears in the customer's installation runbook, it belongs to the platform-level or operator-level layer. If the step is "build the package the customer installs," it belongs to the feature-level layer.

## Documented carve-outs

Some steps cannot be dogfooded because they are structurally impossible to perform from inside a running system:

**Hardware-boundary steps.** A script that stops a virtual machine cannot run on that virtual machine. The customer's equivalent is purchasing and racking hardware — also not performed from inside a running system. Both require action at the hardware or account boundary.

**Publisher steps.** Building images, publishing packages, and configuring public artifact repositories are upstream activities that customers consume but do not perform. Only the publishing organization performs these steps; customers consume the result.

**Pre-production research.** Validating a model configuration before publishing recommended defaults is research that produces the recommendation. Customers consume the recommendation; the vendor does the research that produces it.

## Connection to the vendor-customer topology

The customer-first ordering principle is the operational form of the three-tier topology — vendor source code, customer guide catalog, deployment instances — applied at the development level. The vendor builds software (feature layer); the customer installs it following a guide (platform layer); the operator provisions the hardware it runs on (hardware boundary layer). Customer-first ordering keeps these three levels aligned: the vendor develops against the same sequence the customer installs, preventing the vendor's internal shortcuts from becoming the customer's first-day problems.

## See also

- [[compounding-substrate]] — the substrate architecture this principle serves
- [[data-vault-bookkeeping-substrate]] — an example of a product built in customer-installation order

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/customer-first-ordering.md` (version 0.0.1).

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
