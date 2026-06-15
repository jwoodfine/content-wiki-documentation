---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: data-sovereignty-telemetry
short_description: "The platform collects only anonymized, IP-masked geospatial telemetry with no personally identifiable information retained, appending mandatory regulatory disclosure to public-facing interfaces."
title: "Data sovereignty and zero-state telemetry"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: data-sovereignty-telemetry.es.md
last_edited: 2026-05-25
category: architecture
---



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
