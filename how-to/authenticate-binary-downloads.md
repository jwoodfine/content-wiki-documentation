---
schema: foundry-doc-v1
title: "How to authenticate binary downloads"
slug: authenticate-binary-downloads
category: how-to
content_type: how-to
type: how-to
status: stub
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: authenticate-binary-downloads.es.md
---

The PointSav private distribution endpoint at `software.pointsav.com` issues Ed25519-signed binary releases. Every download is verified against the publisher's public key before the binary executes. This guide covers requesting a licence token, downloading a release, and verifying the signature.

For the architecture behind the distribution system, see [[private-git-paid-customer-endpoint]] and [[software-distribution-substrate]].

## See also

- [[private-git-paid-customer-endpoint]] — the paid customer endpoint architecture
- [[software-distribution-substrate]] — the software distribution substrate
- [[machine-based-auth]] — how access to the distribution endpoint is authorized
