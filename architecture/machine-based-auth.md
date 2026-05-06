---
schema: foundry-doc-v1
title: "Machine-Based Authorization"
slug: machine-based-auth
category: architecture
type: topic
quality: stub
short_description: "Machine-based authorization is the authentication model used in the PointSav platform, replacing username and password structures with cryptographic pairing of physical hardware verified by the capability manager."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: machine-based-auth.es.md
---

# Machine-Based Authorization

> Machine-based authorization is the authentication model used in the PointSav platform, replacing username and password structures with cryptographic pairing of physical hardware verified by the capability manager.

**Machine-based authorization** replaces traditional username and password credential structures with a model where authorization requires the cryptographic pairing of physical hardware. The capability manager verifies a cryptographic handshake between the requesting device and the platform before granting access. Because authorization is bound to hardware — not to a memorized secret that can be phished, guessed, or stolen through social engineering — the entire class of remote credential-theft attacks is structurally eliminated. A session cannot be established from hardware that has not completed the cryptographic pairing, regardless of what credentials an attacker may have obtained.

<!-- EXPAND: lead needs 200+ words -->

## Overview

Conventional authentication relies on shared secrets: the user knows a password, and the server checks it against a stored hash. This model creates a persistent attack surface — passwords can be leaked, guessed, intercepted, or extracted through social-engineering techniques that bypass the technical security of the platform entirely. Machine-based authorization shifts the trust anchor from "something the user knows" to "something the hardware holds and can prove cryptographically."

In the PointSav platform, the cryptographic pairing is managed by the capability-based security layer. Each authorized device holds a key pair generated at provisioning time; the private key never leaves the device. When the device requests a capability grant from the platform, it presents a cryptographic proof of possession of that key. The capability manager verifies the proof and issues capability tokens appropriate for the device's declared role. The capability tokens govern exactly what the device can access — no capability token, no access, regardless of any other credential presented.

## Architecture

Machine-based authorization connects to three other architectural layers:

- **seL4 foundation** — the kernel enforces that capability tokens cannot be forged by software running at user privilege.
- **Capability-based security** — the capability manager issues and revokes hardware-bound tokens; the access-control model depends on the hardware-binding for its security guarantees.
- **service-fs audit ledger** — every authorization event is logged to the WORM ledger, providing an externally verifiable record of which hardware accessed which resources and when.

## See Also

- [[capability-based-security]]
- [[sel4-foundation]]
- [[worm-ledger-architecture]]
- [[crypto-attestation]]
- [[3-layer-stack]]

## References

- `conventions/system-substrate-doctrine.md` — capability ledger substrate; hardware-binding within the capability model
- `DOCTRINE.md §XIV` — Compounding Substrate context; machine-based authorization as part of the Boot-Anywhere Capability Recovery mechanism
- `conventions/three-ring-architecture.md` — Ring 1 boundary ingest; where machine-based authorization applies at the service layer


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
