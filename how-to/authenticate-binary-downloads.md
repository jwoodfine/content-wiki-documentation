---
schema: foundry-doc-v1
title: "How to authenticate binary downloads"
slug: authenticate-binary-downloads
category: how-to
content_type: how-to
type: how-to
status: stable
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: authenticate-binary-downloads.es.md
---

The PointSav private distribution endpoint at `software.pointsav.com` issues Ed25519-signed binary releases. Every download is verified against the publisher's public key before the binary executes. This guide covers requesting a licence token, downloading a release, and verifying the signature.

For the architecture behind the distribution system, see [[private-git-paid-customer-endpoint]] and [[software-distribution-substrate]].

## Before you begin

You need:

- A verified account at `software.pointsav.com`
- An active licence for the product you are downloading
- A Linux or macOS host with `curl` installed

## Step 1: Obtain your licence token

Log in to `software.pointsav.com` and navigate to **Licences**. Each active
licence displays an Ed25519-signed token in the format
`psv1_<product>_<ulid>.<signature>`. Copy the full token string.

The token encodes the product identifier, expiry date, and a cryptographic
binding to your account key. The distribution endpoint returns `401` for an
expired token and `403` if the token does not cover the requested product.

## Step 2: Download the release archive

Pass the licence token as a bearer credential in the download request:

```shell
curl -fsSL \
  -H "Authorization: Bearer <your-licence-token>" \
  "https://software.pointsav.com/releases/<product>/<version>/linux-x86_64.tar.gz" \
  -o release.tar.gz
```

Replace `<product>` and `<version>` with the values shown on the **Releases**
page for your licence. Available platforms appear alongside each release.

## Step 3: Fetch the detached signature

Each release archive has an accompanying `.sig` file signed with the
publisher's Ed25519 private key:

```shell
curl -fsSL \
  -H "Authorization: Bearer <your-licence-token>" \
  "https://software.pointsav.com/releases/<product>/<version>/linux-x86_64.tar.gz.sig" \
  -o release.tar.gz.sig
```

## Step 4: Import the publisher's public key

The signing key is pinned at a well-known path on the distribution endpoint:

```shell
curl -fsSL \
  "https://software.pointsav.com/.well-known/pointsav-signing-key.pub" \
  -o pointsav-signing-key.pub
```

Confirm the key fingerprint matches the value listed in the release notes
for the version you are downloading before proceeding to verification.

## Step 5: Verify the Ed25519 signature

Create an allowed-signers file and run `ssh-keygen -Y verify`:

```shell
echo "releases@pointsav.com $(cat pointsav-signing-key.pub)" > allowed_signers

ssh-keygen -Y verify \
  -f allowed_signers \
  -I releases@pointsav.com \
  -n release \
  -s release.tar.gz.sig \
  < release.tar.gz
```

A successful verification prints:
`Good "release" signature for releases@pointsav.com`

If the command prints `Signature verification failed`, the archive has been
modified in transit or the signature file does not match the archive. Do not
proceed — re-download both files and verify again before use.

## Step 6: Extract and run the binary

```shell
tar -xzf release.tar.gz
chmod +x <product>
./<product> --version
```

The binary validates its licence token at startup. If the token has expired
since the download, the process exits with a message indicating the specific
expiry date. Renew the token at `software.pointsav.com` and restart.

## See also

- [[private-git-paid-customer-endpoint]] — the paid customer endpoint architecture
- [[software-distribution-substrate]] — the software distribution substrate
- [[machine-based-auth]] — how access to the distribution endpoint is authorized
