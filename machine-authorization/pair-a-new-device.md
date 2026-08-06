---
schema: foundry-doc-v1
title: "Pair a new device"
slug: pair-a-new-device
short_description: "Pairs an unpaired os-console device onto the PPN mesh: read the pairing code from the startup screen, have an administrator approve it, and confirm network admission."
category: machine-authorization
index_group: pairing-and-tokens
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); network administrators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: pair-a-new-device.es.md
research_trail:
  sources: [pointsav-monorepo service-ppn-pairing (join-request, pending, approve, deny, status routes), app-console-keys (pairing screen, QR rendering, status polling), os-network-admin (approval tool), app-network-admin (mesh-admission poller)]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; endpoint paths, request/response payload shapes, the Crockford base32 charset, the 600-second code lifetime, the 2-second client poll, the 5-second admin poll, and the 30-second mesh-admission poll were each confirmed at their definition site rather than inferred from prior documentation"
---

## Prerequisites

- A device running `os-console` that has not yet been paired — Machine-Based Authorization is inactive on it (see [[machine-based-auth]])
- A WireGuard keypair present on that device; the client submits its public key as part of the join request
- Network reachability from the device to your pairing server, port 9205 by default
- An administrator who can reach the same pairing server and run `os-network-admin`
- A node identifier in `<username>@<tenant>` form for the device

## Purpose

Register an unpaired device with `service-ppn-pairing` so an administrator can approve it onto the WireGuard mesh — about five minutes of active work across two people, plus an unbounded wait between approval and actual network reachability.

## Procedure

### On the device being paired

1. Start `os-console` on the unpaired device. The pairing screen opens automatically at startup and holds the entire screen until the device is paired; there is no menu path or F-key that reaches it.

2. Read the eight-character pairing code from the screen. It is displayed as `XXXX-XXXX` and drawn from the Crockford base32 charset `0123456789ABCDEFGHJKMNPQRSTVWXYZ` — I, L, O, and U are absent, so a code read aloud carries no O/0 or I/1 ambiguity to resolve.

3. Optional: scan the QR block beside the code instead of transcribing it. The QR encodes `PAIR:<code>` with the dash stripped, rendered as a pixel image on terminals supporting the Kitty or Sixel graphics protocols, or as a Unicode half-block image otherwise.

4. Hand the code to your administrator within 600 seconds. The code expires ten minutes after issue, and the client must submit a fresh join request after that.

5. Leave the device on the pairing screen. The client polls its status every two seconds and will not move off the screen until that poll returns approved, denied, or expired.

### On the administrator's workstation

6. Start `os-network-admin`. It polls the pending-request list every five seconds and prints each request with its code, node ID, `bottom` (target substrate), and `arch`.

7. Match the printed code against the code read off the device screen. This comparison is the only identity check in the flow — the endpoints themselves perform none.

   > **Warning:** the approve and deny endpoints carry no access-control check of their own. Anyone who can reach the pairing server's port and holds a valid code can approve or deny a request. Network access to port 9205 is the entire security boundary for this mechanism; place and firewall the pairing server on that basis.

8. Approve the request with the curl command `os-network-admin` prints next to it:

   ```bash
   curl -s -X POST http://<pairing-server>:9205/v1/node-join/approve \
     -H 'Content-Type: application/json' \
     -d '{"code":"XXXX-XXXX"}'
   ```

   To reject the request instead, post the same body shape to `/v1/node-join/deny`.

9. Wait for mesh admission to run separately. Approval appends one record — node ID, WireGuard public key, `bottom`, `arch`, and an approval timestamp — to a file on the pairing server. It does not put the device on the network. A background process polls the fleet controller every 30 seconds and runs the WireGuard command that admits the peer only once the approved node has also appeared in the compute fleet.

## Expected outcome

The device's pairing screen transitions to an Approved state, the request no longer appears in the pending list, and the approval record is on disk on the pairing server. Approved and reachable are two different states: the device becomes reachable on the mesh only after the 30-second admission poller has seen it in the fleet and run WireGuard.

## Verification

On the device: the screen moves to Approved within roughly two seconds of approval, on the next status poll.

On the administrator's side, confirm the request has left the queue:

```bash
curl -s http://<pairing-server>:9205/v1/node-join/pending
```

An approved request is absent from that response. Neither check proves network reachability — that is a later, separate state produced by the admission poller described in step 9.

> **Note:** the `bottom` field in the join request is derived from the device's architecture, not chosen — `aarch64` maps to `seL4`, `x86_64` maps to `netbsd-compat`. There is also no access tier, role, or permission level anywhere in this flow. Network admission is the only thing this mechanism grants.

## Rollback

Before approval: post the code to `/v1/node-join/deny`, or do nothing and let the 600-second expiry close the request.

After approval: no built-in un-pairing command exists today. Removing a paired device means contacting your administrator to remove the WireGuard peer manually on the mesh side — there is no revoke endpoint and no console action that undoes an approval.

## Next steps

- [[navigate-console-tui]] — work the console once the pairing screen releases it
- [[machine-based-auth]] — the authorization model this pairing activates
- [[enroll-ppn-node]] — enroll the machine into a compute fleet, a separate procedure from mesh pairing
