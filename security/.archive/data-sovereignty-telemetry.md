---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: data-sovereignty-telemetry
short_description: "The platform's telemetry architecture today: what is actually collected, how it is used, and a known gap against the zero-state design it is intended to reach."
title: "Data sovereignty and zero-state telemetry"
audience: vendor-public
bcsc_class: forward-looking
language: en
paired_with: data-sovereignty-telemetry.es.md
last_edited: 2026-07-30
category: security
status: archived
archived: 2026-08-03
archived_reason: "superseded by fresh-draft-first authoring pilot against new content-schema tokens (schema-topic.yaml)"
superseded_by: data-sovereignty-telemetry
---

**Major correction (2026-07-30):** this article previously described a live, in-force
IP-masking mechanism ("the final octet is dropped before the record is written") and
framed the platform's telemetry posture as a present-tense GDPR/PIPEDA-compliant
zero-state architecture. Verified directly against the real ingestion code
(`app-mediakit-telemetry/src/bin/telemetry-daemon.rs`, `omni-matrix-engine.rs`): no
masking exists anywhere in the pipeline today. The body below has been rewritten to
describe current behavior accurately, rather than the originally intended design.
Escalated to Command/project-totebox by mailbox (`command-20260730-active-privacy-
compliance-discrepancy-se`) given the compliance stakes — not resolved unilaterally.
This rewrite reflects only what was verified about IP handling; the no-cookie and
no-session-state claims below were not independently re-checked in this pass and are
carried forward from the original article as previously stated, not re-verified.

[[pointsav-overview|PointSav]]'s stated design goal is a zero-state telemetry architecture — no personally identifiable information retained, no tracking cookies, no session state. **That goal is not fully met today.** The real ingestion pipeline currently records the requester's full, unmasked IP address, timestamp, requested URI, and user-agent string for every request — the opposite of the masked, anonymized signal this article previously claimed. This is a known gap against the intended design, not a currently-accurate compliance posture. See also [[sovereign-telemetry|sovereign telemetry]] and [[telemetry-architecture|the telemetry architecture]].

## Key Takeaways

- The intended design is zero-state: no PII, no cookies, no session retention. **The IP-handling piece of that design is not implemented today** — see below.
- No IP masking currently occurs. The full IP address is written to a plaintext record as received; it is not dropped, truncated, or anonymized at any point in the pipeline.
- No cookie-consent banner is currently displayed; the platform's public-facing interfaces do not appear to deploy tracking cookies (carried forward from the original article, not independently re-verified this pass).
- Any disclosure text describing this system's privacy posture in present tense should be treated as describing the *intended* design until the IP-masking gap closes, not the system as it runs today.

## What the pipeline actually does today

The real ingestion path is `app-mediakit-telemetry/src/bin/telemetry-daemon.rs`: it reads the `x-forwarded-for` header verbatim off each incoming request and appends the full IP address — together with the raw timestamp, requested URI, and full user-agent string — to a plaintext CSV file (`assets/ledger_telemetry.csv`). No octet-dropping, truncation, or hashing occurs anywhere in this function. A downstream process, `omni-matrix-engine.rs`, then performs a MaxMind GeoIP lookup directly against that same full IP address to derive coarse geographic signal for usage reporting — a masked address (e.g. final octet zeroed) would not resolve to a useful lookup, so the pipeline's current design actively depends on holding the complete address rather than incidentally retaining it.

## Known gap and remediation

Closing this gap — so the system actually matches the zero-state design intent — requires either masking the IP before persistence (accepting coarser geolocation) or restructuring the GeoIP step to work from an already-masked value. Neither has been implemented as of this writing. This is flagged to the team that owns `app-mediakit-telemetry` as a real remediation item, not merely a documentation correction — the underlying system, not just this article, needs to change before the zero-state claim can be made accurately again.

## Regulatory disclosure — treat as intent, not current state

Some public-facing interfaces may carry disclosure language describing this system in zero-state, masked terms. Until the gap above closes, any such disclosure should be understood as describing the platform's intended posture, not a currently accurate technical claim — this wiki does not reproduce that disclosure text here in order to avoid restating a claim known to be inaccurate today.

## See also

- [[sovereign-telemetry]]
- [[machine-based-auth]]
- [[zero-execution-routing]]
- [[cryptographic-ledgers]]
