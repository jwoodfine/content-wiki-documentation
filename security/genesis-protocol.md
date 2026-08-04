---
schema: foundry-doc-v1
title: "Genesis protocol"
slug: genesis-protocol
short_description: "The Genesis Protocol is the fleet-bootstrapping sequence every os-infrastructure node runs at first boot, reaching a secure claimable state with no prior configuration."
category: security
index_group: isolation-boundaries
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: en
paired_with: genesis-protocol.es.md
last_edited: 2026-07-28
editor: pointsav-engineering
---

The Genesis Protocol is the fleet-bootstrapping sequence used by every `os-infrastructure` node at first boot. It allows a node to become operational on isolated hardware — with no prior configuration, no connection to any control plane, and no knowledge of the eventual fleet it will join — and to remain in a secure, claimable state until an administrator is ready to bring it under management. The protocol inverts the conventional assumption that a control plane must exist before compute can be added to it.

**Major correction (2026-07-28):** the five-step sequence below does not match what the
live `os-infrastructure` crate currently does or currently builds. Two things are true at
once, and neither matches this article: (1) `os-infrastructure/src/main.rs`, `forge_iso.sh`,
and `build_iso/` are explicitly labeled "Existing scaffold" / "original ISO build scaffold"
in the crate's own `CLAUDE.md` — kept only until `moonshot-toolkit build` replaces them
end-to-end (task #14). That scaffold's raw bare-metal Rust code has no seL4 dependency and
generates no keypair from hardware entropy. (2) The crate's *current* path (Option B —
GRUB2 → seL4 microkernel → CAmkES VMM → Linux guest, per the same `CLAUDE.md`) has not
passed its own D7 three-node mesh test gate yet, and its real network stack —
`system-network-interface/src/lib.rs` — has `scan_for_peers()`, `send_genesis_handshake()`,
and `conduct_pairing_ceremony()` implemented as explicit stubs (`scan_for_peers` always
returns `NotFound`; `send_genesis_handshake` always returns `false`; `system_status()`
literally reports `"skeleton (NIC driver pending)"`). No "fiduciary keypair"/"hardware
entropy" concept, no "hardened WebSocket interface," and no PPN-mesh-port beacon protocol
of the shape described below were found anywhere in the crate's actual dependencies. The
real designed (not yet built) mechanism is materially different from this article's
five-step story: a UDP `GenesisHandshakeFrame` handshake followed by CPace PAKE (RFC 9382)
key exchange, with an 8-character Crockford base32 SAS code displayed on the framebuffer
and entered by the operator on `app-console-keys`' F12 panel — not a keypair the seL4
kernel silently verifies. **Flagged as a whole-article architectural mismatch, not
line-edited** — this may be an early design document that predates the crate's real
implementation direction, or the two have simply diverged. Needs project-totebox
confirmation of the actual current/intended Genesis Protocol design before this article is
corrected or rewritten — this is squarely a REWRITE-class finding per the disposition
rubric, not a targeted correction.

## The problem it solves

Conventional fleet management requires a sequencing dependency: the control plane must be configured, the network must be routed, and the node must be enrolled before the node becomes useful. For an operator shipping hardware to a distant location, this creates a coordination problem — the hardware arrives at a remote site before the fleet management layer is ready, or the reverse.

The Genesis Protocol removes the sequencing dependency. A node can ship to any location, boot in any network environment, and reach a secure, self-contained state without any pre-provisioning. The administrator claims it whenever they are ready.

## The five steps

### 1 — Blind boot

On first boot, the seL4 kernel generates a Tier-1 fiduciary keypair from hardware entropy. The node then enters blind-boot mode: it deliberately ignores DHCP and DNS, refusing to acquire a network address through conventional mechanisms. This prevents the node from being reached by, or reaching out to, any infrastructure it has not already verified.

### 2 — Scan

The node scans the local network for an `os-network-admin` beacon on the PPN mesh port. The scan uses the node's fiduciary public key as the identity it presents — so only a legitimate `os-network-admin` instance holding the corresponding administrative key material can respond authoritatively.

### 3 — Genesis fork

If the scan finds no `os-network-admin` beacon within the scan window, the node forms a Private Network of One. It seals all external ports except a single, hardened endpoint. It does not attempt to contact any external service. It does not fail. It holds.

A node that has genesis-forked is fully operational: it has its keypair, it has a sealed network perimeter, and it is waiting for a claim. It is not a broken node — it is a fleet-ready node that has not yet been claimed.

### 4 — Holding pattern

The single open endpoint is a hardened WebSocket interface. It accepts only one message class: an administrative claim request presenting a valid fiduciary keypair. Any other connection attempt is silently dropped. The node emits no identifying information to the network; to an external observer, the endpoint is opaque.

### 5 — Claim

When an administrator boots `os-network-admin` and presents the administrative fiduciary key, the holding-pattern endpoint verifies the key against the node's locally stored keypair. If the pair verifies:

1. The node binds to the fleet, accepting the `os-network-admin` instance as its authority
2. The node receives its WireGuard mesh configuration and joins the [[sovereign-mesh|sovereign mesh]]
3. The node's fiduciary keypair is registered in `os-network-admin`'s pairing registry as an ADMIN pairing
4. The sealed external ports open according to the fleet's Diode Standard policy

If the key does not verify, the claim is silently rejected. The node remains in its holding pattern and emits no error response.

## Deferred fleet assembly

The Genesis Protocol is designed for the case where hardware ships before the administrator is ready to manage it. An operator can ship fifty servers to fifty edge locations. Each arrives, boots, and forms a one-node PPN. Whenever the administrator is ready — days, weeks, or months later — `os-network-admin` claims all fifty in sequence. Each verifies the claim and joins the fleet. The operator never needs to physically touch the nodes after initial shipment.

This pattern works because the holding pattern is indefinitely stable. A node in the holding pattern draws minimal power, maintains its sealed perimeter, and presents no attack surface beyond the hardened claim endpoint.

## Relationship to machine-based authorization

The Genesis Protocol is the provisioning phase of [[machine-based-auth|machine-based authorization]]. The fiduciary keypair generated at first boot becomes the ADMIN pairing entry for that node in the fleet's pairing registry. After the claim:

- The node's keypair material is the sole basis for all subsequent authentication — no password is ever transmitted
- The pairing can be revoked by severing the ADMIN entry in the registry; the node becomes ungovernable by the fleet (though it continues to run its workloads standalone)
- The administrative fiduciary key authority resides physically with the administrator — it is never delegated to a cloud service

## See also

- [[infrastructure-os]] — the compute substrate that runs the Genesis Protocol at first boot
- [[os-network-admin]] — the control plane that executes the claim sequence
- [[sovereign-mesh]] — the WireGuard overlay the node joins after a successful claim
- [[machine-based-auth]] — the fiduciary keypair system the protocol relies on
- [[diode-standard]] — the authority hierarchy that governs the fleet after claim
