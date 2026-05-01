---
schema: foundry-doc-v1
title: "Ontological Governance"
slug: topic-ontological-governance
category: governance
type: topic
quality: stub
short_description: "Ontological governance describes the four self-healing control ledgers that govern how service-content classifies and accumulates knowledge, and the human-verification loop that keeps extracted identity data accurate before it is permanently committed."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-ontological-governance.es.md
---

# Ontological Governance

> Ontological governance is the discipline of governing what the platform *means* by its categories over time — enforced through four throttled CSV ledgers that define classification vocabulary, and a human-verification loop that prevents automated extraction errors from compounding.

**Ontological governance** is the framework that keeps the
platform's classification vocabulary stable and its extracted
identity data accurate. It operates across two mechanisms: the
four control ledgers that govern how `service-content` classifies
knowledge, and the verification surveyor that forces extracted
identity fragments through human review before they are permanently
written into the verified ledger. These two mechanisms are
structurally separate but serve the same goal: preventing
accumulated classification drift from undermining the integrity of
long-lived institutional data.

## The three-stage extraction pipeline

Data extraction across the platform is mechanically isolated into
three services:

1. **`service-email` (ingestion).** Processes MIME payloads and
   deposits raw text and CSV files into the spool. No
   classification is applied at this stage.
2. **`service-people` (identity resolution).** Scans the spool
   for human identity clusters and routes them to the verification
   surveyor before committing to the verified ledger.
3. **`service-content` (linguistic classification).** Scans the
   spool for narrative knowledge and cross-references text against
   the four control ledgers.

## The four control ledgers

`service-content` is governed by four CSV ledgers that update at
heavily throttled rates to preserve longitudinal data stability:

| Ledger | Minimum update interval | Governs |
|---|---|---|
| Archetypes | More than 24 months | The psychological and functional identity of the firm (for example, "The Fiduciary") |
| Chart of Accounts | 18–24 months; requires executive override | The structural and financial geometry of the operation (for example, "Compliance", "IT Support") |
| Domains | More than 12 months | Bilingual glossaries defining the macro-categories: Corporate (Finance), Projects (Real Estate), Documentation (Technology) |
| Themes | 3–8 months | The active frontline narratives (for example, "Co-Location Expansion") |

Update rates are intentionally asymmetric. The slowest ledgers
(Archetypes, Chart of Accounts) capture what the firm fundamentally
is; the fastest (Themes) capture what it is currently working on.
Premature updates to the slower ledgers corrupt the longitudinal
coherence of the data corpus.

## The verification loop

`service-people` uses a human-in-the-loop verification step to
prevent automated extraction errors from entering the verified
ledger. The process is described in detail at
[[topic-verification-surveyor|Verification Surveyor]]. In brief:
the system isolates unverified identity fragments for operator
review; the operator verifies each entity using their own personal
browser and off-network lookup; the verified result is then
committed to the ledger. The daily throughput limit ensures that
operator attention remains high-fidelity rather than habitual.

## See Also

- [[topic-verification-surveyor|Verification Surveyor]]
- [[topic-message-courier|Message Courier Service]]
- [[topic-moonshot-initiatives|Moonshot Initiatives]]
- [[topic-sovereign-replacement-initiative|Sovereign Replacement Initiative]]

## References

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.