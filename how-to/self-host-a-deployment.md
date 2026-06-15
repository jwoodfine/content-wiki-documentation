---
schema: foundry-doc-v1
title: "How to self-host a deployment"
slug: self-host-a-deployment
category: how-to
content_type: how-to
type: how-to
status: stable
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: self-host-a-deployment.es.md
---

A PointSav deployment is a named, numbered instance of a gateway configuration provisioned on operator-controlled infrastructure. Each deployment runs the same software distribution substrate as the hosted service, with all data and keys held locally. This guide covers provisioning a new deployment instance, verifying the gateway starts correctly, and connecting it to the upstream platform.

For the deployment architecture, see [[deployment-patterns]] and [[edge-deployment]]. For the software distribution model that supplies signed binaries to your instance, see [[software-distribution-substrate]].

## Before you begin

You need:

- A Linux server with at least 4 GB RAM and 20 GB available disk
- A verified account at `software.pointsav.com` with an active deployment licence
- A domain name or static IP address for the gateway endpoint
- A TLS certificate and private key for the gateway bind address

## Step 1: Download and verify the gateway binary

Follow [[authenticate-binary-downloads]] to download and verify the gateway
release for your platform. Once verified, install the binary:

```shell
sudo mv pointsav-gateway /usr/local/bin/
sudo chmod +x /usr/local/bin/pointsav-gateway
pointsav-gateway --version
```

The `--version` flag prints the build SHA alongside the version number.
Confirm this matches the release notes entry for the version you downloaded.

## Step 2: Create the deployment directories

```shell
sudo mkdir -p /etc/pointsav/gateway
sudo mkdir -p /var/lib/pointsav/data
```

All configuration lives in `/etc/pointsav/gateway/`. Runtime data — the WORM
ledger, local cache, and key store — writes to `/var/lib/pointsav/data/`.
Both paths should be owned by the process user the gateway will run as.

## Step 3: Write the deployment manifest

Create `/etc/pointsav/gateway/manifest.toml`:

```toml
[deployment]
name          = "<your-deployment-name>"
instance      = 1
licence_token = "<your-licence-token>"

[gateway]
bind     = "0.0.0.0:443"
tls_cert = "/etc/pointsav/gateway/tls.crt"
tls_key  = "/etc/pointsav/gateway/tls.key"

[data]
root = "/var/lib/pointsav/data"
```

`name` must match the deployment name registered at `software.pointsav.com`.
`instance` is an integer that distinguishes multiple deployments of the same
named configuration. Place your TLS certificate and private key at the paths
declared under `[gateway]`.

## Step 4: Start the gateway

```shell
sudo -u <process-user> pointsav-gateway \
  --manifest /etc/pointsav/gateway/manifest.toml
```

For production, register this as a systemd service with `Restart=on-failure`.
The gateway logs to stderr; redirect to your preferred log target in the unit
file.

## Step 5: Verify the gateway is healthy

```shell
curl -sk https://localhost/healthz
# expected: {"status":"ok","deployment":"<your-deployment-name>-1"}
```

If the response is `{"status":"licence_error"}`, the licence token has expired
or the `name` field does not match the registered deployment name. Renew the
token at `software.pointsav.com` and restart. If the response is a connection
refusal, confirm the gateway is running and the bind port is open in the host
firewall.

## Step 6: Provision downstream modules

With the gateway healthy, provision the modules relevant to your deployment
pattern — see [[deployment-patterns]] for the catalogue of available
configurations. To add local inference capability, configure the Doorman
service next: see [[configure-doorman]].

## See also

- [[deployment-patterns]] — gateway configuration patterns and deployment topologies
- [[edge-deployment]] — edge instance architecture and connectivity model
- [[software-distribution-substrate]] — how signed binary releases are delivered
- [[authenticate-binary-downloads]] — verify the binary before running it
- [[configure-doorman]] — wire up the inference gateway after the deployment is running
