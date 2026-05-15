---
schema: foundry-doc-v1
title: "Machine-Based Authorization"
slug: machine-based-auth
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: machine-based-auth.es.md
short_description: "Machine-based authorization replaces username and password structures with cryptographic pairing of physical hardware — the pair is the permission."
cites: []
---

Machine-based authorization replaces username and password structures with cryptographic pairing of physical hardware — the pair is the permission. When a device requests access, both sides of the pair demonstrate possession of complementary key material; if the pair verifies, the connection is established; if not, the machines are mutually invisible. Because authorization is bound to hardware rather than a memorized secret, the entire class of remote credential-theft attacks — phishing, password guessing, and social engineering — is structurally eliminated. This article covers how pairings work, the four pairing types, the structural advantages over passwords, and the relationship to the [[diode-standard|Diode]] and audit layers.

## How a pairing works

A pairing is a cryptographic handshake between two machines. The two ends of the pair hold complementary public/private key material. When a [[console-os|Command Ledger]] connects to a [[totebox-os|Totebox]], both sides demonstrate possession of the corresponding key. If the pair verifies, the connection is established. If it does not, the machines are invisible to each other.

`service-pairing` manages these pairings using Noise Protocol and WireGuard-style keys, derived from hardware attestation where the underlying platform supports it.

| Property | Behaviour |
|---|---|
| Authentication | The pairing key itself — no password is ever transmitted or stored |
| Authorisation | The presence of the pairing; permission is the pair |
| Revocation | The pairing is severed at one or both ends; the machines become mutually invisible |
| Hardware binding | Where possible, the private key is sealed in the host's hardware enclave |

## The four pairing types

A [[totebox-os|Totebox]] recognises four pairing types, distinguished by the relationship between the pair endpoints and the data:

| Pairing | Endpoint | Access | Sovereign function |
|---|---|---|---|
| ADMIN | Owner's primary machine ↔ Totebox | Absolute | Master key for VM and hardware control, migration, and key management |
| INPUT | Operator's daily machine ↔ Totebox | Read / Write | The default state — full agency over personal data, email, and files |
| USER | Restricted-access machine ↔ Totebox | Read-only | Consulting the data without modifying it — auditors, advisors |
| INTERFACE | Orchestration aggregator ↔ Totebox | Metadata only | High-level fleet visibility without granting record-level access |

The INPUT pairing is the default and the most powerful pairing type. The Totebox's owner has full agency by default; restrictions are deliberate downgrades, not default settings.

## Why this beats passwords

Three structural advantages emerge from replacing passwords with pairings:

**No central database to breach.** There is no "users table" anywhere in the architecture. A successful breach of any one component yields no credential material useful elsewhere.

**No phishing surface.** An operator cannot be tricked into typing their pairing into a fake login form because the pairing is never typed. It is demonstrated cryptographically by the hardware itself.

**Physical revocation.** When an operator's access should be removed, the pairing is severed at the machine level. Even if they retain a copy of the software binary, they lack the key material to connect. There is no password to reset; the machine is simply no longer paired.

## The boundary discipline

Pairing alone does not grant data access. It grants the ability to attempt access. The [[diode-standard|Diode Standard]] governs what flows through any established pair. The audit ledger records every command and every response. The pair is the prerequisite; the Diode and the [[worm-ledger-design|WORM ledger]] are the gates.

The combination — pairing as access, Diode as direction, audit as record — makes the system auditable end-to-end without ever requiring a password rotation policy.

## Architecture connections

Machine-based authorization connects to three other architectural layers:

- **[[sel4-microkernel-substrate|seL4 microkernel]]** — the kernel enforces that capability tokens cannot be forged by software running at user privilege.
- **Capability-based security** — the capability manager issues and revokes hardware-bound tokens; the access-control model depends on hardware-binding for its security guarantees.
- **[[worm-ledger-design|WORM ledger]]** — every authorization event is logged to the append-only ledger, providing an externally verifiable record of which hardware accessed which resources and when.

## Why service-auth was rejected

Early designs considered `service-auth`, modelled on a traditional directory service, as the identity provider. The decision was reversed: a traditional directory service is structured around users, passwords, and group hierarchies — the exact model PointSav is replacing. `service-pairing` was created as a deliberate alternative, and `service-auth` was removed from the architecture before any code was written.

## See also

- [[diode-standard]] — the unidirectional command flow that governs what passes through an established pair
- [[worm-ledger-design]] — the append-only audit ledger that records every authorization event
- [[sel4-microkernel-substrate]] — the seL4 microkernel that enforces capability-token integrity
- [[compliance-and-continuous-disclosure]] — how hardware-bound authorization supports continuous-proof compliance
- [[deployment-patterns]] — how MBA pairing applies across the six canonical deployment configurations
