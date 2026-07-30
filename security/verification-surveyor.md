---
schema: foundry-doc-v1
title: "Verification surveyor"
slug: verification-surveyor
category: security
type: topic
content_type: topic
quality: stub
short_description: "The Verification Surveyor is the human-in-the-loop component of service-people presenting extracted identity fragments for manual verification before permanent commit."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-30
editor: pointsav-engineering
cites: []
paired_with: verification-surveyor.es.md
---

**Major correction (2026-07-30):** this article describes a live "Verification
Surveyor" human-in-the-loop workflow in `service-people` — a hard 10-verifications-
per-day limit, a terminal UI presenting extracted fragments, and an operator
pasting back a verified external-directory URL. No such mechanism exists in the real
`service-people` crate: a corpus-wide grep for "surveyor," any daily-limit constant,
or external-lookup/LinkedIn logic across every `.rs` file (`acs.rs`, `person.rs`,
`mcp.rs`, `people_store.rs`, `fs_client.rs`, `http.rs`) returns zero hits. This is the
same unbuilt-feature pattern already found and corrected this session in
`capability-based-security.md`, `crypto-attestation.md`, `diode-standard.md`, and
`genesis-protocol.md`. The article's own `quality: stub` field already signals
incompleteness, but `status: active` and unhedged present tense throughout still
present it as an operating mechanism. **Flagged as a whole-article architectural
mismatch, not line-edited** — needs project-totebox confirmation of whether this is a
planned design or was simply never built, before rewriting.

> The Verification Surveyor is the architectural checkpoint in [[service-people]] that prevents automated extraction errors from compounding by requiring a human operator to confirm each identity fragment against an off-network source before it is committed to the verified ledger.

## Key Takeaways

- Every identity fragment extracted by `[[service-people]]` is held as unverified until a human operator confirms it against an external directory source using their own personal browser and personal account. The platform never initiates the external lookup itself.
- Hard limit of 10 verifications per operator per day — a deliberate quality-control constraint, not a capacity ceiling. High-volume mechanical approval at speed produces habitual confirmation; the limit forces deliberate attention on each record.
- The air-gapped external-lookup design avoids three operational risks: no persistent foreign API tokens required, no per-query costs, and no exposure to rate-limiting or IP-ban from external directory services.
- At 10 verifications per day, roughly 3,650 confirmed institutional relationships accumulate per operator per year with negligible error rate — the throughput constraint is part of the data-quality guarantee.

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

Every identity fragment extracted by [[service-people|`service-people`]] is held as
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

## See also

- [[ontological-governance|Ontological Governance]]
- [[message-courier|Message Courier Service]]
- [[sovereign-telemetry|Zero-State Telemetry Architecture]]
- [[moonshot-initiatives|Moonshot Initiatives]]
