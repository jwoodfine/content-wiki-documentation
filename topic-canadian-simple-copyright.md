---
schema: foundry-doc-v1
title: "Canadian-Simple Copyright Posture"
slug: topic-canadian-simple-copyright
category: governance
type: topic
quality: core
short_description: "Foundry's intellectual property vests in a single Canadian parent holding company by operation of Canadian Copyright Act § 13(3), without inter-company assignment, and is designed to be evolved incrementally as the corporate structure matures."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: topic-canadian-simple-copyright.es.md
---

# Canadian-Simple Copyright Posture

> Foundry intellectual property vests in Woodfine Capital Projects Inc. by operation of Canadian Copyright Act § 13(3) without requiring inter-company assignment, preserving both share-sale optionality and a clean downstream-rollover path at incorporation.

Foundry's intellectual property is held under a deliberately
minimal corporate posture chosen to preserve flexibility while
the project matures. Copyright vests at a single Canadian holding
entity by operation of statute rather than by inter-company
assignment. This article describes the posture, names the
statutes that make it work, and lists the trigger events that
require it to be revisited.

This article is the public-facing complement to the operational
section in `factory-release-engineering/README.md` §6. It is
**not legal advice**. Counsel review is appropriate before any
trigger event below.

## The holder

Copyright is held by **Woodfine Capital Projects Inc.** ("WCP
Inc."), a British Columbia corporation that sits as the parent
holding entity of the Foundry trajectory.

## The statutory basis — Canadian Copyright Act § 13(3)

Canadian Copyright Act § 13(3) makes the employer the **first
owner** of copyright in works made by an employee in the course
of employment under a contract of service. § 13(3) creates
first-ownership, not assignment. It does not require a separate
written instrument for the right to vest. The resulting
ownership is not subject to the § 14(1) reversionary interest
that applies to § 13(4) assignments.

This is the load-bearing statute. Every other element of the
posture follows from it.

## The corporate structure

Three entities of differing status are operative:

| Entity | Status | Role |
|---|---|---|
| Woodfine Capital Projects Inc. | Incorporated (BC); parent holding | Copyright + trademark holder for all software, documentation, content, and brand IP |
| Woodfine Management Corp. | Incorporated (BC); operating sub | Operations / shield-blocker; does not generate IP-derived revenue using WCP IP |
| PointSav Digital Systems | Yet to be incorporated | Operated as a trade name of WCP Inc. pre-incorporation; eventual BC operating subsidiary |

## Why this works without inter-company IP agreements

The structure has **no inter-company IP flow** while it operates
this way:

- WCP holds IP and, through its employees, creates and uses it
  directly.
- Woodfine Management Corp. is genuinely non-operating with
  respect to WCP IP.
- "PointSav Digital Systems" is a trade name of WCP, not a
  separate legal person.

Canadian Copyright Act § 13(3) is sufficient for vesting. CRA
§ 247 transfer-pricing documentation requirements, which attach
to inter-company IP use, do not attach when there is no inter-
company use to document.

## Operational disciplines that maintain the posture

The posture depends on the following disciplines being kept:

- **Employee-only contributors.** Every IP-creating contributor
  is a bona fide WCP Inc. employee on T4 payroll, performing
  in-scope work under WCP direction. Independent contractors
  retain copyright by default under Canadian law and would
  require separate written assignment under § 13(4). Until
  counsel-drafted contractor IP-assignment templates are in
  place, the posture admits no contractor contributions to
  in-scope work.
- **Woodfine Management Corp. stays non-operating** with
  respect to WCP IP. If Woodfine Management Corp. begins using
  WCP IP to generate revenue, an inter-company licence with
  arm's-length pricing documentation becomes expected.
- **"PointSav Digital Systems" is a trade name of WCP** under
  BC's Partnership Act until incorporation. A Declaration of
  Trade Name with the BC Registrar should be filed if the brand
  is used commercially before incorporation.
- **Moral rights gap acknowledged.** § 14.1 moral rights cannot
  be assigned, only waived in writing. § 13(3) does not waive
  them. The current posture admits this residual gap and does
  not paper it; counsel-drafted moral-rights waivers may be
  added later as the structure matures.

## Trigger events that require revisiting

When any of the following occurs, the posture upgrades and
counsel-drafted agreements (master IP assignment, inter-company
IP-assignment agreement, moral-rights waivers) become standard:

- First hire who is not a founder or officer.
- First contractor contribution to in-scope code, content, or
  design work.
- First external revenue generated using WCP IP.
- Reporting-issuer status under BCSC `[ni-51-102]`.
- PointSav Digital Systems Inc. incorporation event (handled at
  the rollover; Income Tax Act § 85 rollover transfers the IP
  estate to the new entity in a single transaction).
- Any inter-company IP use between WCP and an operating
  subsidiary.

## Why this preserves equity value

Holding IP at the parent enables **share-sale** transactions:
selling WCP equity transfers the entire IP estate in one
transaction. No per-asset assignments. No Bulk Sales Act
triggers. No customer consents required.

Asset-sale alternatives at sub-co level require enumerated IP
schedules, individual assignments, and customer consents. The
asymmetry runs forward in time as well: pushing IP **down** to
PointSav Digital Systems Inc. on incorporation via § 85
rollover is a single-event transaction. Pulling IP **up** from
a sub-holder later requires § 13(4) assignment + § 247
documentation + potential GST/HST implications + fair-market-
value crystallisation.

The posture preserves both share-sale optionality today and the
cleaner downstream-rollover path at incorporation.

## What this posture is not

It is not a permanent state. It is the minimum viable structure
chosen for the current state of the Foundry trajectory, designed
to be evolved as the project matures without unwinding pre-
existing agreements.

It is not a substitute for counsel-drafted agreements at scale.
The trigger events above each call for counsel-drafted
agreements that supersede the statutory default. The structure
is intentionally minimal so the supersession can be staged.

It is not BCSC-style continuous-disclosure. The disciplines
described here govern how copyright vests and what the
corporate structure looks like; the disclosure regime per
`[ni-51-102]` operates on a different surface and applies
whether or not the relevant entity is currently a reporting
issuer.

## See Also

- [[topic-customer-hostability|Customer Hostability]]
- [[topic-contributor-model|Contributor Model]]
- [[topic-sovereign-replacement-initiative|Sovereign Replacement Initiative]]
- [[topic-ontological-governance|Ontological Governance]]

## References

- Canadian Copyright Act — <https://laws-lois.justice.gc.ca/eng/acts/c-42/>
- BC Business Corporations Act — <https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/02057_00>
- Income Tax Act § 85 (rollover) — <https://laws-lois.justice.gc.ca/eng/acts/i-3.3/section-85.html>
