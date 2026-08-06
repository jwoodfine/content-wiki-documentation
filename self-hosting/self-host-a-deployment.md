---
schema: foundry-doc-v1
title: "Self-host a deployment"
slug: self-host-a-deployment
short_description: "Boots the published os-totebox and app-orchestration-slm seL4 appliance images under QEMU, with configuration baked in at build time via device-tree bootargs, and verifies both come up healthy."
category: self-hosting
index_group: getting-the-platform-running
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: self-host-a-deployment.es.md
research_trail:
  sources: [GUIDE-deploying-os-totebox-orchestration-appliances.draft.md (project-totebox, 2026-08-03), BRIEF-os-totebox-platform.md, .agent/binary-targets.yaml]
  verification_method: "independently confirmed by project-totebox 2026-08-06 against real source (build-guest-rootfs.sh + deploy-loader-img.sh present for both os-totebox and app-orchestration-slm; vendor-libvmm/ confirmed genuine upstream seL4 Microkit VMM) after this archive raised a direct contradiction question against capability-based-security.md and os-totebox's Cargo.toml; app-orchestration-command's separate, not-yet-built seL4 packaging status was confirmed at the same time and does not apply to this guide, which never references that product"
---

## Prerequisites

- A host that can run QEMU for `aarch64` (the appliance images target this architecture regardless of your host's own CPU)
- The published `os-totebox-loader.img` and, optionally, `app-orchestration-slm-loader.img` from `software.pointsav.com`
- A persistent disk image, created once and kept — an ext4-formatted raw file the guest mounts at `/data`
- If you need non-default configuration (a specific orchestration endpoint, a Tier B license): the source repo, the Microkit SDK, and an `aarch64` cross-compilation toolchain — the published images alone don't let you change configuration after the fact (see Step 3)

## Purpose

Self-hosting a deployment means booting one or both of two independent, self-contained seL4/Microkit appliance images on operator-controlled infrastructure: `os-totebox` (the Sovereign WORM Data Vault — local DataGraph, corpus ingestion, Tier A operations) and `app-orchestration-slm` (the Yo-Yo broker chassis — health, fleet, and discovery endpoints; Tier B brokering requires a license). Each runs standalone by default; neither needs the other present to start.

## Procedure

1. Create your persistent disk, once:

   ```
   qemu-img create -f raw persistent.raw 2G
   ```

   This is where DataGraph state, adapter weights, and cached identity survive across restarts. Losing this file means losing everything the appliance has accumulated — it is not regenerated from the image.

2. Boot the image via QEMU's `-device loader` mechanism (this is Microkit's own loader path, not the `-kernel`/`-append` path a general-purpose Linux VM would use):

   ```
   qemu-system-aarch64 \
     -machine virt,virtualization=on,secure=off -cpu cortex-a53 \
     -device loader,file=os-totebox-loader.img,addr=0x70000000,cpu-num=0 \
     -m size=2G -nographic -global virtio-mmio.force-legacy=false \
     -drive file=persistent.raw,format=raw,if=none,id=hd \
     -device virtio-blk-device,drive=hd,bus=virtio-mmio-bus.1 \
     -device virtio-net-device,netdev=netdev0,bus=virtio-mmio-bus.0 \
     -netdev user,id=netdev0,hostfwd=tcp::<host-port>-:<guest-port>
   ```

3. If the published, generic image's default configuration is sufficient, skip to Step 4. Otherwise, understand this before you try to change anything: **runtime configuration is baked into the image at build time**, in the device tree's `bootargs`. There is no post-boot config file and no `-append` equivalent on this boot path. Changing configuration means rebuilding the image yourself, with your own `foundry.*` bootarg values, and replacing the published one — see the relevant keys below and the full rebuild procedure in the internal dogfood development guide (`GUIDE-live-flow-doorman-orchestration-yoyo.draft.md`, project-totebox).

   | Key | Appliance | Purpose |
   |---|---|---|
   | `foundry.orchestration_endpoint` | os-totebox | Chassis URL for Tier B brokering |
   | `foundry.tier_b_subscribed` | os-totebox | `true` to claim a paid subscription at registration |
   | `foundry.yoyo_default_endpoint` | app-orchestration-slm | Default Yo-Yo compute backend URL |
   | `foundry.license_token` / `foundry.license_pubkey_hex` | app-orchestration-slm | Ed25519-signed Tier B license |

4. Repeat Step 2 for `app-orchestration-slm-loader.img` if you want the Yo-Yo broker chassis too — it's an independent image with its own boot invocation, not a component started from inside `os-totebox`.

## Expected outcome

`os-totebox` reaches a healthy, standalone state within seconds of boot, with or without `app-orchestration-slm` present — this degrade-not-refuse behavior is the intended design, not a sign of misconfiguration. `app-orchestration-slm`, if booted, answers health/fleet/discovery requests standalone; Tier B brokering itself stays disabled until a valid license is baked into a rebuilt image.

## Verification

```
curl http://<host>:<totebox-port>/healthz       # os-totebox
curl http://<host>:<orchestration-port>/healthz  # app-orchestration-slm
curl http://<host>:<orchestration-port>/readyz   # license / fleet / circuit status
```

## Rollback

Stop the QEMU process. The persistent disk (`persistent.raw`) is untouched by stopping the guest — restarting the same boot command resumes from the same accumulated state. To discard accumulated state entirely, discard the persistent disk file itself and create a fresh one (Step 1); there is no partial-reset mechanism short of that.

## Next steps

- [[deploy-knowledge-instance]] — deploy the wiki-serving engine, a separate concern from these appliance images
- [[configure-doorman]] — configure the inference gateway once your deployment is running
- [[authenticate-binary-downloads]] — verify a downloaded image's signature before booting it

## Known limitations, as shipped (2026-08-03)

- No automated update mechanism — a configuration change means a rebuild and a full image replacement, not a live edit.
- The published images have not been through a customer-scale security review; treat as an early release.
- Real GPU-scale training requires your own Yo-Yo compute backend — the images themselves don't include one.

## See also

- [[deployment-patterns]] — gateway configuration patterns and deployment topologies
- [[edge-deployment]] — edge instance architecture and connectivity model
- [[software-distribution-substrate]] — how signed binary releases are delivered
- [[authenticate-binary-downloads]] — verify a release before running it
- [[configure-doorman]] — wire up the inference gateway after the deployment is running
