---
schema: foundry-doc-v1
title: "Zero-State Telemetry Architecture"
slug: topic-sovereign-telemetry
category: architecture
type: topic
quality: stub
short_description: "The zero-state telemetry architecture describes how Foundry's V4 Intent Beacon collects behavioural and hardware signals from edge clients without cookies, session identifiers, or third-party analytics, using client-side compilation and asynchronous beacon transmission."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-sovereign-telemetry.es.md
---

# Zero-State Telemetry Architecture

> The zero-state telemetry architecture collects behavioural and hardware signals from edge clients using only native browser APIs — no cookies, no session identifiers, no third-party analytics aggregators — and transmits the compiled payload asynchronously at tab-close.

The **zero-state telemetry architecture** is the Foundry approach
to understanding user behaviour without accumulating persistent
client state. The current implementation, codename **V4 Intent
Beacon**, enforces a strict no-cookie, no-session-ID posture. Data
is compiled entirely on the client side using native browser APIs
and transmitted asynchronously via `navigator.sendBeacon` on the
`visibilitychange` event. No tracking pixels, session identifiers,
or third-party analytics providers are involved. The result is a
telemetry signal that is both privacy-preserving by structure and
operationally independent of external analytics platforms.

## Payload structure

The V4 Intent Beacon payload captures distinct signals, each drawn
from a native browser API:

| Field | Source | Notes |
|---|---|---|
| `user_agent` | `navigator.userAgent` | Device and browser identification |
| `viewport` | `window.innerWidth` / `innerHeight` | Rendering geometry |
| `timezone` | `Intl.DateTimeFormat().resolvedOptions().timeZone` | Regional mapping without IP geolocation |
| `device_memory` | `navigator.deviceMemory` | Estimated device RAM range |
| `hardware_cores` | `navigator.hardwareConcurrency` | CPU thread count |
| `dwell_seconds` | DOM load to tab-close delta (milliseconds) | Time-on-page signal |
| `scroll_depth` | Maximum vertical scroll percentage | Engagement depth |
| `intent_clicks` | Array of interaction targets | High-value click events (e.g., Fleet Manifest links, contact initiations) |

No field captures personally identifiable information. The
`timezone` field provides regional resolution without requiring IP
geolocation.

## Graceful degradation

The receiving Rust daemon (`telemetry-daemon`) uses `Option<T>`
serialisation for all V4 parameters. This ensures backward
compatibility with clients that have cached an older payload
format. When a legacy payload arrives, the daemon ingests the
available fields and writes `unknown` or `0` to the absent columns.
The immutable ledger record is written in either case, maintaining
alignment across all fleet deployments without requiring a
coordinated client-side rollout.

## Chronological synthesis

The `telemetry-synthesizer` binary parses the CSV ledger and
generates executive-grade Markdown reports partitioned into
standard financial reporting windows: 1D, 1W, 30D, 60D, 90D,
year-to-date, and inception-to-date.

## See Also

- [[topic-ontological-governance|Ontological Governance]]
- [[topic-verification-surveyor|Verification Surveyor]]
- [[topic-message-courier|Message Courier Service]]
- [[topic-customer-hostability|Customer Hostability]]

## References

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.