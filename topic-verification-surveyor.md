---
schema: foundry-doc-v1
title: "Verification Surveyor"
slug: topic-verification-surveyor
category: architecture
type: topic
quality: stub
short_description: "The Verification Surveyor is the human-in-the-loop component of service-people that presents extracted identity fragments to an operator for manual verification before they are permanently committed to the verified ledger."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-verification-surveyor.es.md
---

# Verification Surveyor

> The Verification Surveyor is the architectural checkpoint in service-people that prevents automated extraction errors from compounding by requiring a human operator to confirm each identity fragment against an off-network source before it is committed to the verified ledger.

Unsupervised extraction algorithms accumulate errors. A fully
automated ingestion pipeline processing large volumes of email
will inevitably produce false positives — an "Unsubscribe" link
parsed as a person's name, a role title extracted from a footer
rather than a bio. The **Verification Surveyor** is the deliberate
architectural bottleneck that forces all extracted identity
fragments through a human cognitive filter before they are
permanently written into the verified ledger. The design accepts
the throughput cost in exchange for high-fidelity, long-term
institutional data.

## Human-in-the-loop philosophy

Every identity fragment extracted by `service-people` is held as
unverified until an operator confirms it. The Surveyor presents the
fragment — the extracted text, the inferred entity type, the source
context — to the operator. The operator then looks up the individual
using their own personal browser and their own personal account on
an external directory (such as LinkedIn), confirms the entity, and
pastes the verified URL back into the terminal. The platform never
initiates the external lookup itself.

This design is deliberate. API-based lookups against external
directories would require persistent foreign tokens, incur
per-query costs, and expose the platform to rate-limiting or
IP-ban risk. The air-gapped approach avoids all three.

## Daily throughput limit

The Surveyor enforces a hard limit of ten verifications per
operator per day. The limit is not a capacity constraint; it is a
quality control mechanism. High-volume data entry at speed
produces habitual approvals rather than genuine verification. Ten
careful verifications per day produce roughly 3,650 confirmed
institutional relationships per year with negligible error rate.
The scarcity is structural: it transforms what would otherwise be
a mechanical clearing task into a deliberate, high-attention
operational step.

## See Also

- [[topic-ontological-governance|Ontological Governance]]
- [[topic-message-courier|Message Courier Service]]
- [[topic-sovereign-telemetry|Zero-State Telemetry Architecture]]
- [[topic-moonshot-initiatives|Moonshot Initiatives]]

## References

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.