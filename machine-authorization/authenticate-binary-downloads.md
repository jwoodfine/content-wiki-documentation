---
schema: foundry-doc-v1
title: "Authenticate binary downloads"
slug: authenticate-binary-downloads
short_description: "Authenticates a release from software.pointsav.com: confirm the on-chain order, follow the download link that mints an Ed25519 token, and understand where verification actually happens."
category: machine-authorization
index_group: software-distribution
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: authenticate-binary-downloads.es.md
research_trail:
  sources: [pointsav-monorepo marketplace/ordering service behind software.pointsav.com (order page, on-chain payment watch, receipt derivation, download handoff), binary-release service (token minting, Ed25519 verification, release URL routing, verify-key publication), tool-wallet payment-verification tool]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; the token wire format and its unpadded base64url encoding, the server-side-only verification path, the receipt code's role as a record rather than a credential, the published key's hex encoding and path, the public-domain routing gap on that path, and the current $0 price on every listed product were each confirmed at their definition site, correcting an earlier, unverified correction note's fictional token format and its incorrect claim that client-side ssh-keygen verification applies to this system (that mechanism is real elsewhere on the platform, for an unrelated purpose)"
---

## Prerequisites

- The transaction hash of your Polygon USDC payment, if you placed a paid order
- A browser, or `curl` configured to follow redirects
- Nothing else — no local verification tool, key file, or signature utility is needed

## Purpose

Obtain a release from `software.pointsav.com` through the signed download path, and understand which part of that path actually authenticates the file — about two minutes once your payment has confirmed on-chain.

> **Note:** every product currently listed is priced at $0 for the BETA period and requires no license or payment today. The order-and-token path below is working code and is what a paid order will use, but at present you can download any current release without going through a paid order at all. Steps 1 and 2 apply only if you have placed one.

## Procedure

1. Open your order page at `https://software.pointsav.com/order/<tx_hash>`, where `<tx_hash>` is your payment transaction hash. The order reads as pending until `tool-wallet` confirms the payment on-chain.

2. Reload the page once confirmation lands. A receipt code appears — a deterministic identifier derived from the transaction. Keep it for your records; no download step asks for it, and it is not a download credential.

3. Follow the download link at `https://software.pointsav.com/order/<tx_hash>/download`. That request mints a fresh Ed25519-signed token and redirects straight to the release download with the token already attached as a URL parameter. There is no separate token to copy.

4. Let the download run to completion. The release service verifies the token's Ed25519 signature server-side before it streams a single byte, so there is no client-side verification command to run afterward.

5. Optional: address a release directly rather than through an order page, using the release URL pattern:

   ```text
   https://software.pointsav.com/releases/<product>/<version>/<platform>
   https://software.pointsav.com/releases/<product>/latest/<platform>
   ```

   The `latest` form redirects to the resolved current version.

## Expected outcome

You hold the release file, and the fact that you hold it is the proof that its download token verified: a request carrying a missing, malformed, or badly-signed token does not produce a release file. The token's wire format is `base64url(signature || payload_json)`, unpadded, and it is checked with Ed25519 on the server before the response body begins.

## Verification

Confirm you received a release file rather than an error page — check the file's size and type against what the release page advertised. The signature check itself has already happened at that point; it is not a step you repeat locally.

To inspect the platform's public signing key independently, the release service publishes it at `/verify-key.pub` as a plain hex string: 32 raw bytes, 64 hex characters.

> **Warning:** that path is not currently reachable through the public `software.pointsav.com` domain. The underlying service serves it correctly, but a routing gap in front of the public domain means a request to it there does not reach the handler. Treat independent key retrieval as unavailable over the public domain until that routing is fixed.

## Rollback

Downloading changes nothing on the server and nothing on your host outside the file you fetched, so there is nothing to reverse. Delete the file and start again from step 3 if a download is incomplete or corrupted.

Do not reuse a saved download URL from an earlier session. The token is minted fresh on each visit to the order page's download link, so a stale link is repaired by returning to the order page rather than by editing the URL.

## Next steps

- [[self-host-a-deployment]] — boot an appliance image once you have it
- [[private-git-paid-customer-endpoint]] — the ordering and distribution architecture behind these URLs
- [[software-distribution-substrate]] — how signed binary releases are delivered
