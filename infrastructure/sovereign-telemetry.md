---
schema: foundry-doc-v1
title: "Zero-state telemetry architecture"
slug: sovereign-telemetry
category: infrastructure
index_group: network-and-telemetry
type: topic
content_type: topic
quality: complete
short_description: "Zero-state telemetry: a single unload beacon carrying URI and timestamp, paired server-side with the requester's IP and user agent, written unmasked to an append-only CSV ledger."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: sovereign-telemetry.es.md
---

The zero-state telemetry architecture is the platform's approach to understanding site traffic without cookies, session identifiers, or a third-party analytics provider. A page sends one small beacon when the visitor leaves; the server captures it alongside the requester's IP address and writes an append-only ledger line. There is no client-side accumulation of state between visits — "zero-state" describes the client, not the server-side record.

## Payload

On `unload`, the page sends `navigator.sendBeacon` a JSON body with two fields: `uri` (the page path) and `timestamp` (the client's clock, in milliseconds). No cookies, tracking pixels, or third-party analytics script are involved — the beacon is a single same-origin POST.

The server pairs that payload with two values it reads from the request itself: the requester's IP address (from a forwarding header, first entry if the header carries a chain) and the `User-Agent` string. All four values — IP, timestamp, URI, user agent — are appended as one line to a plaintext CSV ledger. **None of the four fields is masked or truncated.** See [[data-sovereignty-telemetry|the security-category article on this same daemon]] for the compliance implications of the unmasked IP specifically, already escalated separately — this article isn't re-raising that finding, just describing the same real payload from the infrastructure side.

## See also

- [[telemetry-architecture]] — how the beacon payload is routed and processed after it reaches the server
- [[ontological-governance|Ontological Governance]] — the governance layer that this telemetry substrate serves
- [[verification-surveyor|Verification Surveyor]] — the verification pattern that this telemetry architecture supports
- [[customer-hostability|Customer Hostability]] — the customer-rooted data custody principle this architecture implements
