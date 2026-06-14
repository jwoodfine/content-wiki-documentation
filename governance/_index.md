---
schema: foundry-doc-v1
title: "Governance"
slug: _index
category: governance
type: topic
content_type: topic
quality: complete
short_description: "Formal decision records, licensing posture, contributor model, and compliance requirements that govern how the PointSav platform is built, licensed, and changed — including the twelve binding architecture decisions, the BCSC continuous-disclosure posture, and the licence matrix."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-19
editor: pointsav-engineering
paired_with: _index.es.md
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
- [[legal-and-ip-structure]] — The three-corporation IP topology: how intellectual property transfers from contributors to vendor to customer, with squash-and-merge as the atomic IP-transfer event.

### Engineering sovereignty

- [[sovereign-replacement-initiative]] — The formal program that records every third-party dependency in a structured ledger, enforces quarantine isolation, and retires each dependency when a native replacement reaches structural parity.
- [[moonshot-initiatives]] — The nine active engineering programs building native replacements for quarantined third-party dependencies, from the kernel layer up through the build toolchain.
- [[sovereign-airlock-doctrine]] — The staged-commit protocol that enforces a structural separation between staging identities (commit authors) and canonical push identities, with no direct path between them.

### Platform disciplines

- [[ontological-governance]] — The four throttled control ledgers and human-verification loop that prevent automated classification drift from undermining the integrity of long-lived institutional data.
- [[anti-homogenization-discipline]] — The architectural posture that resists AI writing assistants pulling contributors toward a single voice, defaulting to flagging rather than silent rewriting.
- [[api-key-boundary-discipline]] — The rule that all external LLM API credentials belong exclusively at the gateway service and never at inference engines or downstream consumers.
- [[favicon-matrix]] — The icon matrix governing visual identity across all platform surfaces: one distinct glyph per service, OS, and application, enforced at the asset-pipeline layer.

## See also

- [Wiki home](/)
- [Architecture](/architecture/)
- [Infrastructure](/infrastructure/)
- [Reference](/reference/)
