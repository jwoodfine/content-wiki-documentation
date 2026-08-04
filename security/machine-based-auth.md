---
title: "Machine-based authorization"
slug: machine-based-auth
category: security
index_group: identity-and-permissions
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "Access is granted to a device's key rather than to a person's password. A short-code pairing ceremony binds an SSH key fingerprint to a user record after operator approval, with no password stored anywhere."
paired_with: machine-based-auth.es.md
---

**Machine-based authorization** (MBA) grants access to a specific device's cryptographic key
rather than to a person's memorised secret. There is no password to store, transmit, guess, reuse,
or phish; what a user holds is a private key that never leaves their machine, and what the system
records is the fingerprint of the corresponding public key. Access is revoked by removing that
fingerprint, not by forcing a credential reset.

Every password is a secret a person must remember, and therefore a secret an attacker can phish,
guess, stuff, or socially engineer out of them — the entire category of remote credential theft
exists because the credential is something a human knows. Key-based authorisation moves the attack
to physical or persistent access to a specific machine, which is harder to achieve at scale and
much more visible when it happens.

## The pairing ceremony

The live implementation is the `system-gateway-mba` component, and it works as a request,
approval, and binding sequence rather than a login.

A device submits a pairing request carrying a username, an organisation, its public key, and that
key's fingerprint. The server records the request with a generated identifier, a short pairing
code, an attempt counter, a creation time, and an expiry time, and places it in the `pending`
state. An operator then approves or denies it out of band, having compared the short code shown on
the device against the one shown in the approval interface — the step that prevents a request from
an unknown machine being approved by mistake.

Approval moves the request to `approved` and creates the user record binding username,
organisation, and key fingerprint. Denial moves it to `denied`. A sweep marks requests whose expiry
has passed as `expired`. Five HTTP routes cover the ceremony: request, approve, deny, a listing of
pending requests, and a per-request status lookup.

The record shape is deliberately small. The request table holds identifier, code, username,
organisation, fingerprint, public key, role, state, attempt count, creation time, and expiry. The
user table holds fingerprint, username, organisation, role, an active flag, and creation time, with
the fingerprint unique and the organisation constrained to one of two permitted values. **No
password field exists in either table** — verifiable by reading the schema.

### What the fingerprint is

The authorisation module is ten lines and does exactly one thing: it computes an OpenSSH-format
SHA-256 fingerprint of a presented public key. The component's dependencies are an SSH library used
for key parsing and fingerprinting, an embedded SQLite database, a random-number source, and
ordinary serialisation and HTTP crates. The pairing code itself is generated from a
non-cryptographic random source in a human-transcribable alphabet — appropriate for a code an
operator reads aloud or retypes, and not a secret in its own right, since it is useless without
operator approval.

## Two independent layers: network membership and application pairing

MBA operates at the application layer, deliberately independent of network infrastructure. In
deployments using the platform's [[ppn-mesh-architecture|private mesh network]], reaching a machine
at all requires being a registered peer of the encrypted mesh — that is network membership, one
layer. MBA is the other: even a machine that can reach the target over the network is refused at
the application boundary unless its key fingerprint matches an approved pairing. A party that
operates network infrastructure — even the vendor — does not thereby gain application-layer access
to the data running on it: network reachability and data access are granted by different
mechanisms, held by different parties.

A separate node-join service runs the same request-approve-deny-expire shape for admitting compute
nodes to the private network itself. Its records carry a node identifier, a mesh public key, a
declared lower layer, and an architecture; approved nodes are appended to a log file that mesh
provisioning tooling reads. A small shared library provides the short-code generation,
normalisation, and terminal-rendered scannable code used by both ceremonies. The mesh public key is
worth a precise word: it is stored and passed through as an opaque string. Neither service performs
a mesh key exchange; provisioning is carried out by external tooling invoked from shell scripts, and
the placeholder directory nominally reserved for that tooling contains only a README.

## Roles, and what they are not

The role attached to a pairing user record is a plain string, not a typed set of values, and the
approval path writes a single hardcoded default into it. The database applies no constraint on its
content. No handshake-protocol implementation of the kind sometimes associated with this design — a
Noise-style or mesh-VPN-style key exchange — exists anywhere in the component's source; a
whole-tree search found no Noise implementation and no corresponding library anywhere in canonical
source.

A typed pairing role does exist elsewhere in the platform: `PairingRole` in the orchestration
command component (`app-orchestration-command`), an enum with three values — `User` (read/write,
daily operator), `Admin` (full access), and `Interface` (metadata-only, for the orchestration
aggregator). It is not the same field, does not live in this component, and does not carry a fourth
value. Descriptions of four named authorisation tiers implemented as code constructs in this
pairing system are not supported by the source; the separate four-tier `PermissionTier` model that
does exist (`P1`–`P4`) is described in [[personnel-permissions]] and belongs to a different
component and a different data path — the two enums live in the same crate but govern unrelated
concerns and should not be conflated.

The component itself has grown since it was last measured — it now runs to roughly 870 lines across
its source files, not the smaller figure sometimes quoted for it — though its shape (request table,
user table, five HTTP routes, ten-line fingerprint module) is unchanged.

## The transport gap

One honest limitation belongs in the body rather than a footnote. Host-native access over the
public internet currently runs through an SSH port-forwarded tunnel that does **not** verify the
remote server's identity. The intended property — that the vendor cannot read operator data in
transit — is therefore not delivered over that hop today. It becomes true when verified mutual TLS
lands on that path; until then, the pairing ceremony authenticates the device to the service, but
the service is not cryptographically authenticated back to the device across that specific tunnel.

## Why pairing rather than accounts

Three properties follow from binding authority to a device rather than a person.

**Revocation is exact.** Removing a fingerprint removes one machine's access. A compromised laptop
is dealt with without disturbing the same person's other devices or forcing an organisation-wide
credential reset. A departed contractor's retained software copies are inert without approved key
material, and the approval workflow's request records double as an audit trail of who was granted
what, and when.

**Enrolment is observed.** A device becomes known through an approval decision made by a person who
compared a code, not through a self-service form. There is no path by which a device enrols itself,
and no phishing surface exists: a pairing is never typed, so an operator cannot be tricked into
entering it into a counterfeit form.

**The stored value is not a secret.** A fingerprint discloses nothing usable. A breach of the
pairing database yields a list of which keys were trusted — useful reconnaissance, but not
credentials, which is a materially different exposure from a leaked password store. A quieter,
compounding advantage follows: the model has no credential-hygiene liturgy — no rotation schedules,
no complexity policies, no expiring passwords generating helpdesk resets. What remains is a short,
inspectable list of approved machine keys per tenant, which is a security posture a reviewer can
actually audit to completion.

## What this is not

**There is no Noise Protocol handshake and no key exchange in this component.** The cryptography
present is SSH public-key fingerprinting; the mesh keys the pairing services handle are opaque
strings passed to external tooling.

**The component is not named `service-pairing`.** No component of that name exists. The live
implementation is `system-gateway-mba`, and the node-join ceremony is a separate service again.

**The role field is not an enforced tier.** It is an unconstrained string with a hardcoded default
at approval time, not a typed enumeration and not a checked authorisation level. A three-value typed
role does exist, but in a different component for a different purpose, and it is not the four-tier
taxonomy sometimes described for this one.

**MBA is not multi-factor authentication layered on passwords.** There is no password anywhere to
add factors to; the model replaces the category. Nor is it biometric: nothing about a human body is
measured or stored, and the bound entity is a machine, not a person — which also means MBA alone
does not tell you *which human* was at the keyboard of an approved machine; personnel-level
identity and tiering are the separate [[personnel-permissions|personnel and permissions]] layer.

**Pairing is not a login session.** It establishes that a device is known. What that device may
then do is governed by the permission model described elsewhere, which draws on a different data
source entirely, the [[diode-standard|Diode Standard]]'s directional rules, and the
[[worm-ledger-design|append-only audit ledger]] every access event lands in. The pair is the
prerequisite; the direction rules and the ledger are the gates.

**A pairing code is not a credential.** It is a short human-transcribable value from a
non-cryptographic random source, meaningful only during the approval window and only alongside an
operator decision.

**End-to-end transport confidentiality is not currently delivered over the remote-access tunnel.**
See the transport gap above; this is stated as intended, not achieved.

## See also

- [[pairing-as-permission]] — the principle that the pairing record is itself the authorisation
- [[pair-a-new-device]] — the operator procedure for running the ceremony
- [[personnel-permissions]] — the four-tier permission model and where it actually lives
- [[enroll-ppn-node]] — the node-join variant of the same ceremony
- [[app-console-keys]] — the device-side interface presenting the pairing code
- [[capability-based-security]] — the authority model above device authentication
- [[diode-standard]]
- [[ppn-mesh-architecture]]
