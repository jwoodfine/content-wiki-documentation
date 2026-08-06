---
schema: foundry-doc-v1
title: "Machine Authorization"
slug: machine-authorization-index
category: machine-authorization
type: topic
content_type: topic
index_type: thematic
index_scope: machine-authorization
quality: complete
short_description: "Pairing devices and nodes onto the network, issuing and rotating service-to-service capability tokens, and authenticating binary downloads."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: _index.es.md
---

**Machine authorization** covers the credential and admission mechanisms that gate who and what can act on the platform — pairing a device onto the WireGuard mesh, issuing and rotating the Ed25519 capability tokens services use to authenticate to each other, enrolling a compute node into a fleet, and authenticating a signed binary download. These are genuinely separate mechanisms, not one system under different names; each guide states plainly where its own mechanism's real limits are, including where no revocation or un-pairing command exists today.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[pair-a-new-device|Pair a new device]] — registers a device with the pairing server and walks through administrator approval, the most common entry point into this category.

<!-- END-START-HERE-HIGHLIGHT -->

## Pairing and tokens

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: pairing-and-tokens -->
- [[pair-a-new-device|Pair a new device]] — register an os-console device and get it approved onto the WireGuard mesh
- [[issue-capability-token|Issue a capability token]] — mint an Ed25519-signed token and register it with a peer service
- [[rotate-keys|Rotate keys and capability tokens]] — replace a credential within the system's real 24-hour expiry limits
<!-- END AUTO-GENERATED -->

## Fleet enrollment

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: fleet-enrollment -->
- [[enroll-ppn-node|Enroll a PPN node]] — start the per-node heartbeat agent and confirm it in the fleet controller
<!-- END AUTO-GENERATED -->

## Software distribution

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: software-distribution -->
- [[authenticate-binary-downloads|Authenticate binary downloads]] — confirm an order and follow the signed download path for a release
<!-- END AUTO-GENERATED -->

Each guide carries its own prerequisites, verification steps, and rollback procedure; this
page doesn't repeat them. Day-to-day operation of a running deployment is in
[How You Run It](/category/how-to).

## See also

- [How You Run It](/category/how-to) — the remaining day-to-day operational guides
- [Security and Trust](/category/security) — the identity and permissions model these mechanisms participate in
- [Self-Hosting](/category/self-hosting) — deploying the appliances these credentials authenticate against
