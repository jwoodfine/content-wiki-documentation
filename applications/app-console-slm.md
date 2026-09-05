---
schema: foundry-doc-v1
title: "app-console-slm — inference infrastructure monitoring console"
slug: app-console-slm
category: applications
type: app
content_type: topic
quality: complete
index_group: input-and-developer-surfaces
short_description: "Terminal console cartridge showing live AI inference infrastructure state — model health, the burst-GPU fleet, queue depth, and daily spend — read-only, with no controls of its own."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
cites: []
references: []
paired_with: app-console-slm.es.md
---

app-console-slm is a terminal user interface (TUI) cartridge for the operator console
that displays the live state of the AI inference infrastructure: local model health,
the burst-GPU fleet, the entity graph, queue depth, and the current day's spending.
It is a read-only dashboard. Every write operation it displays — routing policy,
[[spot-vm-lifecycle-kill-switch|the kill switch]] — happens through a separate API surface, not through this console.

The console runs in a terminal window on the same node as the [[service-slm|inference gateway]]. It
requires no browser, no network connection to an external service, and no
authentication beyond local shell access.

## Display panels

The console organizes information into five panels that refresh automatically every
ten seconds. The operator can trigger an immediate refresh at any time with the R key.

### Gateway panel

Shows whether the router is running, the local model's reachability and
tokens-per-second throughput, the burst tier's circuit-breaker state, and the node
class currently serving requests.

### YoYo Fleet panel

Lists each configured burst-compute node by name alongside its lifecycle state: one
of unknown, stopped, staging, running, available, failed to start, or zombie
(running but no longer answering health probes). The panel highlights only
available nodes as healthy; stopped, failed, and zombie nodes share a muted style.

### DataGraph panel

Shows the total entity count in the knowledge graph and the burst tier's
circuit-breaker state (the same circuit shown in the Gateway panel, since both
reflect the same tier).

### Queue panel

Shows extraction-queue depth: pending, in flight, paused, and completed counts,
plus how many jobs sit in quarantine. A poison count — jobs that failed enough
retry attempts to need operator review — is highlighted whenever it is non-zero.

### Cost Today panel

Shows the current day's total spend, broken into the burst-compute portion and the
VM-hours portion, alongside the day's request count.

## Keyboard controls

| Key | Action |
|---|---|
| R | Immediate refresh — re-queries all status endpoints |
| ? | Help overlay — show all keybindings |
| Esc | Close the help overlay |
| Q | Quit |

Routing-policy changes and the kill switch are real, operator-controlled mechanisms.
The kill switch is a hard stop no request can bypass; the routing policy (balanced,
drain-batch, drain-express, or local-only) is switchable at runtime. Both live behind
the gateway's own API, not this console — it only displays their effects.

## Technical characteristics

The console is a library crate that implements the Cartridge trait for the operator
console chassis. It loads at [[use-f-key-model|slot F9]]. Communication with the inference gateway uses
standard HTTP against the gateway's monitoring endpoints.

The console uses a background polling task that fetches status data every ten seconds
and sends it to the rendering task via a channel. The rendering task does not block
on network requests; it displays whatever data arrived most recently, so the console
stays responsive even when the gateway is slow to respond.

Plain-text mode is available via the `--plain` flag for terminal environments without
unicode support. Unicode status symbols are replaced with ASCII equivalents.

## Relationship to the inference gateway

The console is a pure observer: it makes no write calls to the inference gateway at
all. It is deployed alongside the gateway on the same node and requires no network
connectivity to external services. If the gateway is unreachable, the console keeps
running and shows each panel as unavailable rather than crashing.

## See also

- [[app-console-keys]] — the chassis that hosts this cartridge; defines the Cartridge trait
- [[os-console]] — the os-console product overview and F-key surface
- [[service-slm]] — the inference gateway whose state this console displays
- [[spot-vm-lifecycle-kill-switch]] — the kill switch this console surfaces but does not control
- [[app-console-email]] — a sibling cartridge on the same console chassis
