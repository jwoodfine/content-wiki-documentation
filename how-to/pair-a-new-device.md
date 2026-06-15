---
schema: foundry-doc-v1
title: "How to pair a new device"
slug: pair-a-new-device
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: pair-a-new-device.es.md
---

Pairing a device registers it with the platform using machine-based authorization — a cryptographic handshake that binds access to your hardware rather than to a username and password. Once a device is paired, it holds the keys required to establish connections. A device without a pairing has no pathway to the protected resources at all — not access-denied, but structurally unreachable.

For the theory behind this model, see [[machine-based-auth]] and [[pairing-as-permission]].

## Prerequisites

- A PointSav account with at least P3 access (see [[personnel-permissions]])
- The `os-console` application installed on the device you are pairing
- Network access to the Command endpoint assigned to your account

## Steps

### 1. Open the pairing request from os-console

Launch `os-console` on the new device and navigate to **Settings → Devices → Pair this device**. The console generates a temporary pairing code — a short, human-readable string that is valid for 10 minutes.

### 2. Approve the pairing on a trusted device

On a device already paired to your account (your INPUT-tier daily machine), open `os-console` and navigate to **Settings → Devices → Pending pairings**. The new device's pairing code and hardware fingerprint appear here.

Verify that the fingerprint shown on the new device matches the fingerprint shown on your trusted device before approving. This cross-check prevents a rogue device from inserting itself.

### 3. Select the pairing type

Choose the access tier for the new device:

| Tier | What it can do |
|---|---|
| INPUT | Full read/write access to your archives and data — use for your daily machine |
| USER | Read-only access — use for shared or secondary devices |
| INTERFACE | Metadata only — use for orchestration and monitoring integrations |

ADMIN pairings require the approval of the system administrator and cannot be self-issued.

### 4. Confirm and complete

Approve the pairing from your trusted device. The new device's `os-console` refreshes automatically and the Totebox session becomes available. The pairing event is recorded to the audit ledger immediately.

## Verify the pairing

On the new device, open `os-console` and navigate to **Settings → Devices → This device**. The device status should show **Paired** with the tier you selected and the timestamp of the pairing event.

Run a test read-operation on any archive to confirm connectivity.

## Revoke a pairing

To remove a device from your account, navigate to **Settings → Devices** on any paired device, select the target device, and choose **Revoke**. The revoked device becomes mutually invisible to your resources immediately — no logout or TTL wait is required.

## Key takeaways

- The pairing IS the permission; there is no central access-control list to update
- Always verify the hardware fingerprint cross-check before approving a new pairing
- INPUT pairings grant full read/write access — assign them to machines you control directly
- Revocation is immediate and hardware-level; no session or token expiry needed

## See also

- [[machine-based-auth]] — how machine-based authorization works architecturally
- [[pairing-as-permission]] — the Object Capability pattern that pairing implements
- [[personnel-permissions]] — the four access tiers and what each can do
- [[open-first-totebox-session]] — open a session on a newly paired device
