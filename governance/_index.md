---
schema: foundry-doc-v1
title: "Governance — Category Landing"
slug: _index
category: governance
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
---

## Governance

This category covers the formal decision records, licensing posture, contributor model, and compliance requirements that govern how the PointSav platform is built, licensed, and changed over time. Governance articles are the written record of decisions that have been made and the rationale behind them; they are not aspirational statements.

The twelve binding [[architecture-decisions|architecture decisions]] are the most important entries in this category for technical due diligence and regulatory review: they define where automated processing stops and human authority begins, how data is separated, and where cryptographic keys must reside. Licensing articles explain the licence matrix that governs each repository and its contents. The contributor model article describes the three-tier structure through which code and content flow from contributors to the canonical platform. The BCSC disclosure posture article documents the requirements of Canadian securities continuous-disclosure obligations as they apply to the platform and its public documentation.

## Articles in this category

### Institutional due diligence

Start here for procurement, security, and compliance evaluation.

- [[procurement-overview]] — What a regulated buyer acquires: customer-owned hardware deployment, no vendor-held data, no minimum-spend commitment, and the compliance properties enforced by architecture rather than contractual promise.
- [[security-overview]] — The platform's security posture: capability-based isolation, the Diode unidirectional command-flow standard, the Doorman AI boundary, the WORM audit ledger, and how each property is enforced by architecture.
- [[compliance-and-continuous-disclosure]] — How the platform produces continuous-disclosure-grade records and what that means for regulated buyers.
- [[bcsc-disclosure-posture]] — The BCSC continuous-disclosure posture and how the platform satisfies it by structure.

### Formal decision records

- [[architecture-decisions]] — The twelve binding architecture decisions that constrain all future engineering; grouped by compliance weight, data separation, deployment custody, and operational integrity.

### Licensing and contribution

- [[contributor-model]] — The three-tier contributor model: open community, paid integrators, and the canonical vendor tier; how work flows between them.
- [[canadian-simple-copyright]] — The Canadian-simple copyright posture: licence selection, attribution requirements, and the Canadian legal context.

## See also

- [Wiki home](/)
- [Architecture](/architecture/)
- [Infrastructure](/infrastructure/)
- [Reference](/reference/)
