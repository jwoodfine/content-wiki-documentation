---
schema: foundry-doc-v1
title: "Private binary download endpoint for paying customers"
slug: private-git-paid-customer-endpoint
aliases:
  - topic-private-git-paid-customer-endpoint
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: private-git-paid-customer-endpoint.es.md
short_description: "The binary release server behind software.pointsav.com verifies Ed25519 license tokens and streams compiled binaries — stateless, holding no payment records or keys, with some products served openly and no license check at all."
cites: []
---

The binary release server is the component of `software.pointsav.com` that delivers
compiled binaries to paying customers. It is a thin, stateless gate: it holds no payment
records, no customer data, and no signing keys. Its sole responsibility is to verify that
a presented license token is genuine and authorises the requested product, then stream
the binary file.

## Route structure

**Product and version discovery.** An unauthenticated products index lists every product
with releases on the server; a per-product index lists that product's available versions.
Both are designed for tooling — package managers, installer scripts, CI pipelines.

**Versioned binary download.** The primary gated endpoint serves a binary for a specific
product, version, and platform, and requires a valid license token — with one exception:
a product whose manifest sets `requires_license: false` is served to anyone, no token
required. A detached Ed25519 signature file for each binary is available at a
corresponding path and is always unauthenticated — detached signatures are public by
design, letting any party verify a binary's authenticity without holding a license.

**Latest-version redirect.** A convenience endpoint resolves the highest available version
for a given product and platform and issues a redirect to the versioned download path,
forwarding the license token through. It only redirects to a platform for which a release
actually exists.

**Release manifest and install script.** A per-version manifest endpoint and a per-product
`install.sh` endpoint are both unauthenticated, letting tooling inspect a release or fetch
an installer without a license token.

**Token introspection.** An authenticated endpoint checks a presented token against a
product and returns its validity, product ID, version floor, channel expiry, and
entitlements — without initiating a download. A separate endpoint serves the server's own
public verification key in hex, so a client can verify a detached signature independently.
A health-probe endpoint supports uptime monitoring.

## Authentication

The release server accepts a license token as an `Authorization: Bearer` header or as a
`token` query parameter. The query-parameter form exists specifically for browser-initiated
one-click downloads: a storefront can generate a URL carrying the token so a customer can
download directly from their browser with no header configuration. Both forms are equally
secure — neither exposes the token to any party beyond the client and the server.

## Verification logic

A token is `base64url(signature[64 bytes] || payload_json)` — an Ed25519 signature over
the payload bytes, prepended to the payload itself. The server splits the token, verifies
the signature against its stored public key, then checks the payload's product field
against the requested product and confirms the channel hasn't expired. A bad or malformed
signature returns 401; a valid signature for the wrong product, or an expired channel,
returns 403.

## Platform strings

Platform strings follow the Rust target triple convention — `x86_64-unknown-linux-gnu`,
`aarch64-unknown-linux-gnu`, `x86_64-apple-darwin`, and similar. The server maps product,
version, and platform directly to a file path in the releases directory; a combination
with no built binary returns 404. The latest-version redirect only targets platform
strings for which a release file actually exists.

## Key management and fail-safe behaviour

The server loads its public Ed25519 verification key at startup from configuration. If no
key is configured, it does not silently accept every token — the download and
introspection endpoints return 503 instead. A correctly configured instance accepts only
tokens signed by the corresponding private key.

## What the server does not do

The Git protocol path is a stub: it returns a 503 with a pointer to the public GitHub
repository, not a live proxy and not an HTTP redirect — smart-HTTP Git access is not yet
enabled.

## See also

- [[crypto-license-sales-architecture]] — how payments are processed and tokens are issued upstream of this server
- [[software-distribution-substrate]] — overview of the three-component system this server belongs to
- [[authenticate-binary-downloads]] — step-by-step guide: verify Ed25519-signed binary releases from the private distribution endpoint
- [[issue-capability-token]] — step-by-step guide: generate a scoped Ed25519 capability token for a device or service
