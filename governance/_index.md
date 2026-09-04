---
schema: foundry-doc-v1
title: "Governance and Standards"
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
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.es.md
---

This category covers the formal decision records, licensing posture, contributor model, and compliance requirements that govern how the PointSav platform is built, licensed, and changed over time. Governance articles are the written record of decisions that have been made and the rationale behind them; they are not aspirational statements.

The twelve binding [[architecture-decisions|architecture decisions]] are the most important entries in this category for technical due diligence and regulatory review: they define where automated processing stops and human authority begins, how data is separated, and where cryptographic keys must reside. Licensing articles explain the licence matrix that governs each repository and its contents. The contributor model article describes the three-tier structure through which code and content flow from contributors to the canonical platform. The BCSC disclosure posture article documents the requirements of Canadian securities continuous-disclosure obligations as they apply to the platform and its public documentation.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here** for procurement, security, and compliance evaluation: [[procurement-overview]] — what a regulated buyer acquires, and the compliance properties enforced by architecture rather than contractual promise.

<!-- END-START-HERE-HIGHLIGHT -->

## Institutional due diligence

Start here for procurement, security, and compliance evaluation.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: institutional-due-diligence -->
- [[procurement-overview]] — What a regulated buyer acquires deploying PointSav: hardware the customer owns outright, data the vendor never holds, and compliance enforced by architecture.
- [[security-overview]] — The platform's security posture: capability-based hardware isolation, the Diode command-flow standard, the Doorman AI boundary, and the WORM audit ledger.
- [[compliance-and-continuous-disclosure]] — The regulatory frameworks the PointSav architecture addresses, and its structural approach to exposing audit evidence continuously, not via annual certification.
<!-- END AUTO-GENERATED -->

## Formal decision records

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: formal-decision-records -->
- [[architecture-decisions]] — Twelve binding architecture decisions governing how the PointSav platform is built, constraining engineering work on data handling, oversight, and deployment custody.
- [[adr-07-zero-ai-in-ring-1]] — SYS-ADR-07 prohibits AI inference from all Ring 1 boundary-ingest services, enforcing deterministic-only operations at the WORM write path.
<!-- END AUTO-GENERATED -->

## Licensing and contribution

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: licensing-and-contribution -->
- [[contributor-model]] — The Three-Tier Contributor Model organises substrate contributors into Core (4-7 engineers), Paid (50-100 contractors), and Open (10,000+ public), with mobility paths.
- [[canadian-simple-copyright]] — The platform's IP vests in a single Canadian parent holding company by operation of Canadian Copyright Act § 13(3), without inter-company assignment.
- [[legal-and-ip-structure]] — The three-corporation topology governing IP transfer from contributor to vendor to customer, with squash-and-merge as the atomic IP-transfer event.
<!-- END AUTO-GENERATED -->

## Engineering sovereignty

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: engineering-sovereignty -->
- [[sovereign-replacement-initiative]] — The engineering governance program tracking third-party dependencies, isolating them in quarantine, and coordinating the moonshot programs replacing them.
- [[moonshot-initiatives]] — Moonshot initiatives are active engineering programs building native replacements for quarantined third-party dependencies, reducing vendor lock-in.
- [[sovereign-airlock-doctrine]] — The staged-commit protocol enforcing separation between staging identities and canonical repository identities — two staging authors, two admin push identities.
<!-- END AUTO-GENERATED -->

## Platform disciplines

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: platform-disciplines -->
- [[ontological-governance]] — Four reference vocabulary ledgers kept deliberately narrow, plus a human-verification loop that reviews extracted identity fragments before they enter the verified ledger.
- [[anti-homogenization-discipline]] — Anti-homogenization discipline resists AI writing assistants pulling contributors toward a single voice, by flagging potential issues rather than silently rewriting text.
- [[api-key-boundary-discipline]] — The rule that all external LLM API credentials belong exclusively at the gateway service and never at inference engines.
- [[favicon-matrix]] — The wiki serves a single static SVG favicon — a navy document-page glyph, linked from a static file, the same mark on every tab regardless of tenant.
- [[doctrine-invention-7-rekor-anchoring]] — How Foundry's anchor-emitter binary posts a signed ledger checkpoint to Sigstore Rekor each month, providing independently verifiable, third-party evidence of workspace state.
<!-- END AUTO-GENERATED -->

## See also

- [Wiki home](/)
- [How It's Built](/architecture/)
- [Where It Runs](/infrastructure/)
- [Reference](/reference/)
