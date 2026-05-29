---
schema: foundry-doc-v1
title: "Machine-based authorization"
slug: machine-based-auth
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-22
editor: pointsav-engineering
paired_with: machine-based-auth.es.md
short_description: "Machine-based authorization replaces username and password structures with the cryptographic pairing of physical hardware — the pair is the permission, and an entire class of remote credential theft is eliminated by structure."
cites: []
references:
 - id: 1
 text: "Perrin, T. 'The Noise Protocol Framework.' noiseprotocol.org, 2016."
 url: "https://noiseprotocol.org/noise.html"
 - id: 2
 text: "Donenfeld, J. A. 'WireGuard: Next Generation Kernel Network Tunnel.' NDSS Symposium, 2017."
 url: "https://www.ndss-symposium.org/ndss2017/ndss-2017-programme/wireguard-next-generation-kernel-network-tunnel/"
---

Every password is a secret a person must remember, and therefore a secret an attacker can take. Phishing, password guessing, credential stuffing, social engineering — the entire class of remote credential theft exists because the credential is something a human knows.

Machine-based authorization removes the knowable secret. <!--claim id=pair-is-permission confidence=structural cites=[]-->Access is a cryptographic pairing of two pieces of physical hardware — the pair is the permission. When a device requests access, both ends demonstrate possession of complementary key material; if the pair verifies, the connection forms; if it does not, the machines are mutually invisible.<!--/claim-->

Because authorization binds to hardware rather than to a memorized secret, there is no users table to breach, no login form to phish, and no password to reset. <!--claim id=attack-class-eliminated confidence=structural cites=[]-->Revocation is physical: the pairing is severed at the machine, and the entire class of remote credential-theft attacks is eliminated by structure rather than by policy.<!--/claim-->

For a regulated buyer the consequence is concrete. An attack class disappears, and every access event is attributable to specific hardware in the audit ledger. This article covers how pairings work, the four pairing types, the structural advantages over passwords, and the relationship to the [[diode-standard|Diode]] and audit layers.

## How a pairing works

A pairing is a cryptographic handshake between two machines. The two ends hold complementary public and private key material. When a [[console-os|Command Ledger]] connects to a [[totebox-os|Totebox]], both sides demonstrate possession of the corresponding key. If the pair verifies, the connection is established. If it does not, the machines are invisible to each other.

`service-pairing` manages these pairings using the Noise Protocol [^1] and WireGuard-style keys [^2], derived from hardware attestation where the underlying platform supports it.

| Property | Behaviour |
|---|---|
| Authentication | The pairing key itself — no password is ever transmitted or stored |
| Authorisation | The presence of the pairing; permission is the pair |
| Revocation | The pairing is severed at one or both ends; the machines become mutually invisible |
| Hardware binding | Where possible, the private key is sealed in the host's hardware enclave |

## The four pairing types

A [[totebox-os|Totebox]] recognises four pairing types, distinguished by the relationship between the pair's endpoints and the data.

| Pairing | Endpoint | Access | Function |
|---|---|---|---|
| ADMIN | Owner's primary machine ↔ Totebox | Absolute | Master key for VM and hardware control, migration, and key management |
| INPUT | Operator's daily machine ↔ Totebox | Read / write | The default state — full agency over personal data, email, and files |
| USER | Restricted-access machine ↔ Totebox | Read-only | Consulting the data without modifying it — auditors, advisors |
| INTERFACE | Orchestration aggregator ↔ Totebox | Metadata only | Fleet visibility without record-level access |

<!--claim id=input-default confidence=structural cites=[]-->The INPUT pairing is the default and the most powerful type: a Totebox owner has full agency by default, and restrictions are deliberate downgrades rather than default settings.<!--/claim-->

## Why this beats passwords

Three structural advantages follow from replacing passwords with pairings.

<!--claim id=no-central-db confidence=structural cites=[]-->**No central database to breach.** There is no users table anywhere in the architecture. A successful breach of any one component yields no credential material useful elsewhere.<!--/claim-->

<!--claim id=no-phishing confidence=structural cites=[]-->**No phishing surface.** An operator cannot be tricked into typing a pairing into a fake login form, because a pairing is never typed. It is demonstrated cryptographically by the hardware itself.<!--/claim-->

<!--claim id=physical-revocation confidence=structural cites=[]-->**Physical revocation.** When an operator's access should end, the pairing is severed at the machine level. A retained copy of the software binary is inert without the key material; there is no password to reset.<!--/claim-->

## The boundary discipline

Pairing alone does not grant data access. It grants the ability to attempt access. The [[diode-standard|Diode Standard]] governs what flows through an established pair; the audit ledger records every command and every response. The pair is the prerequisite; the Diode and the [[worm-ledger-design|WORM ledger]] are the gates.

The combination — pairing as access, Diode as direction, audit as record — makes the system auditable end to end, with no password-rotation policy anywhere in it.

## Architecture connections

Machine-based authorization connects to three other architectural layers.

- **[[sel4-microkernel-substrate|seL4 microkernel]]** — the kernel enforces that capability tokens cannot be forged by software running at user privilege.
- **[[capability-based-security|Capability-based security]]** — the capability manager issues and revokes hardware-bound tokens; the access-control model depends on hardware binding for its security guarantees.
- **[[worm-ledger-design|WORM ledger]]** — every authorization event is logged to the append-only ledger, an externally verifiable record of which hardware reached which resource, and when.

## Why service-auth was rejected

<!--claim id=service-auth-rejected confidence=structural cites=[]-->Early designs considered `service-auth`, modelled on a traditional directory service, as the identity provider. The decision was reversed: a directory service is structured around users, passwords, and group hierarchies — the exact model [[pointsav-overview|PointSav]] is replacing.<!--/claim--> `service-pairing` was created as the deliberate alternative, and `service-auth` was removed from the architecture before any code was written. See [[pairing-as-permission|pairing as permission]].

## See also

- [[diode-standard]] — the unidirectional command flow that governs what passes through an established pair
- [[worm-ledger-design]] — the append-only audit ledger that records every authorization event
- [[sel4-microkernel-substrate]] — the seL4 microkernel that enforces capability-token integrity
- [[compliance-and-continuous-disclosure]] — how hardware-bound authorization supports continuous-proof compliance
- [[deployment-patterns]] — how MBA pairing applies across the six canonical deployment configurations
