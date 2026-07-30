---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: data-sovereignty-telemetry
short_description: "The platform collects only anonymized, IP-masked geospatial telemetry with no personally identifiable information retained, disclosed on public-facing interfaces."
title: "Data sovereignty and zero-state telemetry"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: data-sovereignty-telemetry.es.md
last_edited: 2026-07-30
category: security
---

**Major correction (2026-07-30) — active compliance-relevant discrepancy, not just an
architecture description gap:** this article makes a public GDPR/PIPEDA compliance
claim — that IP masking is "applied at receipt," dropping the final octet before any
record is written, so "the platform never holds the full address." The real ingestion
code contradicts this directly. `app-mediakit-telemetry/src/bin/telemetry-daemon.rs`
reads the `x-forwarded-for` header verbatim and appends the **full, unmasked** IP
address — together with the raw timestamp, requested URI, and full user-agent string —
to a plaintext CSV file (`assets/ledger_telemetry.csv`), with no octet-dropping or
masking logic anywhere in the function. The downstream `omni-matrix-engine.rs` then
performs a MaxMind GeoIP lookup directly against that same full, unmasked
`std::net::IpAddr` (`ip_addr.parse()` at line 204) — a masked address (final octet
zeroed) would not resolve to a useful lookup, so the current design depends on holding
the complete address, the opposite of the article's claim. No cookie-related code was
checked as part of this pass (out of scope for this finding); the IP-masking claim
specifically is what this correction addresses. **Flagged as a live compliance/privacy
discrepancy, not resolved unilaterally** — this touches a real, publicly disclosed
privacy posture claim, not just an internal architecture description, so it is being
escalated to Command/project-totebox by mailbox in addition to this callout, per this
archive's standing practice for legal/compliance/anonymization content (draft
conservative, flag, never silently resolve).

[[pointsav-overview|PointSav]] platform interfaces operate on a zero-state telemetry architecture: no personally identifiable information (PII) is collected, no tracking cookies are deployed, and no session state is retained. Operational metrics are limited to anonymized, IP-masked geospatial signals used for infrastructure auditing. Operators in regulated industries gain a public-facing posture consistent with GDPR, PIPEDA, and equivalent data-minimisation requirements, without requiring cookie-consent frameworks. See also [[sovereign-telemetry|sovereign telemetry]] and [[telemetry-architecture|the telemetry architecture]].

## Key Takeaways

- Zero-state means no PII, no cookies, no session retention. A user visiting a public interface leaves no individual record — only a masked geospatial signal.
- IP masking is applied at receipt, not post-storage. The final octet is dropped before the record is written; the platform never holds the full address.
- No cookie-consent banner is required because no tracking cookies are deployed. There is nothing to consent to.
- All public-facing interfaces append a machine-readable privacy disclosure to their legal blocks. This is a current-state architectural fact, not a planned feature.

## No-cookie infrastructure

The platform prohibits tracking cookies, persistent local-storage tracking, and third-party analytics integrations. Public-facing interfaces carry no third-party analytics scripts, eliminating the legal obligation to present cookie-consent banners under ePrivacy and equivalent regimes.

## Geospatial anonymisation protocol

Operational metrics are gathered through a first-party ping architecture. The ingestion server applies mandatory IP masking — the final octet of the incoming IP address is dropped at receipt (for example, `192.168.1.45` becomes `192.168.1.0`). The resulting record is a coarse geospatial signal with no network-level identification. Interaction data — such as document-access events — is used to audit infrastructure security and measure platform usage patterns; no record is tied to an individual identity.

## Mandatory regulatory disclosure

All public-facing interfaces append the following disclosure to their legal blocks:

> "Digital Infrastructure and Privacy Posture: This interface operates on a zero-execution and zero-state telemetry architecture. It does not deploy tracking cookies, retain session states, or harvest personally identifiable information. System interactions are limited to the collection of anonymised, masked network routing data strictly for the purpose of auditing infrastructure security and verifying document access."

## See also

- [[sovereign-telemetry]]
- [[machine-based-auth]]
- [[zero-execution-routing]]
- [[cryptographic-ledgers]]
