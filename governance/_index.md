---
schema: foundry-doc-v1
title: "Governance"
slug: governance-index
category: governance
type: topic
content_type: topic
quality: complete
short_description: "Formal decision records, licensing posture, contributor model, and compliance requirements that govern how the PointSav platform is built, licensed, and changed — including the twelve binding architecture decisions, the BCSC continuous-disclosure posture, and the licence matrix."
index_type: thematic
index_scope: governance
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: _index.es.md
---

## Governance

This category covers the formal decision records, licensing posture, contributor model, and compliance requirements that govern how the PointSav platform is built, licensed, and changed over time. Governance articles are the written record of decisions that have been made and the rationale behind them; they are not aspirational statements.

The twelve binding [[architecture-decisions|architecture decisions]] are the most important entries in this category for technical due diligence and regulatory review: they define where automated processing stops and human authority begins, how data is separated, and where cryptographic keys must reside. Licensing articles explain the licence matrix that governs each repository and its contents. The contributor model article describes the three-tier structure through which code and content flow from contributors to the canonical platform. The BCSC disclosure posture article documents the requirements of Canadian securities continuous-disclosure obligations as they apply to the platform and its public documentation.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here** for procurement, security, and compliance evaluation: [[procurement-overview]] — what a regulated buyer acquires, and the compliance properties enforced by architecture rather than contractual promise.

<!-- END-START-HERE-HIGHLIGHT -->

## Institutional due diligence

Start here for procurement, security, and compliance evaluation.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: institutional-due-diligence -->
- [[procurement-overview]] — What a regulated buyer acquires: customer-owned hardware deployment, no vendor-held data, no minimum-spend commitment, and the compliance properties enforced by architecture rather than contractual promise.
- [[security-overview]] — The platform's security posture: capability-based isolation, the Diode unidirectional command-flow standard, the Doorman AI boundary, the WORM audit ledger, and how each property is enforced by architecture.
- [[compliance-and-continuous-disclosure]] — How the platform produces continuous-disclosure-grade records and what that means for regulated buyers.
<!-- END AUTO-GENERATED -->

## Formal decision records

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: formal-decision-records -->
- [[architecture-decisions]] — The twelve binding architecture decisions that constrain all future engineering; grouped by compliance weight, data separation, deployment custody, and operational integrity.
- [[adr-07-zero-ai-in-ring-1]] — Why the four Ring 1 boundary-ingest services are restricted to deterministic-only operations, and where AI inference is permitted to begin.
<!-- END AUTO-GENERATED -->

## Licensing and contribution

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: licensing-and-contribution -->
- [[contributor-model]] — The three-tier contributor model: open community, paid integrators, and the canonical vendor tier; how work flows between them.
- [[canadian-simple-copyright]] — The Canadian-simple copyright posture: licence selection, attribution requirements, and the Canadian legal context.
- [[legal-and-ip-structure]] — The three-corporation IP topology: how intellectual property transfers from contributors to vendor to customer, with squash-and-merge as the atomic IP-transfer event.
<!-- END AUTO-GENERATED -->

## Engineering sovereignty

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: engineering-sovereignty -->
- [[sovereign-replacement-initiative]] — The formal program that records every third-party dependency in a structured ledger, enforces quarantine isolation, and retires each dependency when a native replacement reaches structural parity.
- [[moonshot-initiatives]] — Nine named engineering programs targeting native replacements for quarantined third-party dependencies; three carry substantial active engineering today, six remain early-stage scaffolds.
- [[sovereign-airlock-doctrine]] — The staged-commit protocol that enforces a structural separation between staging identities (commit authors) and canonical push identities, with no direct path between them.
<!-- END AUTO-GENERATED -->

## Platform disciplines

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: platform-disciplines -->
- [[ontological-governance]] — The four reference vocabulary ledgers and human-verification loop that keep the platform's identity classification legible over time.
- [[anti-homogenization-discipline]] — The architectural posture that resists AI writing assistants pulling contributors toward a single voice, defaulting to flagging rather than silent rewriting.
- [[api-key-boundary-discipline]] — The rule that all external LLM API credentials belong exclusively at the gateway service and never at inference engines or downstream consumers.
- [[favicon-matrix]] — The single static SVG favicon served across every wiki tenant, and why the mechanism is a linked file rather than an inline data URI.
- [[doctrine-invention-7-rekor-anchoring]] — How the platform posts a monthly signed ledger checkpoint to the public Sigstore Rekor transparency log, giving auditors independently verifiable evidence outside the platform's own infrastructure.
<!-- END AUTO-GENERATED -->

## See also

- [Wiki home](/)
- [Architecture](/architecture/)
- [Infrastructure](/infrastructure/)
- [Reference](/reference/)
