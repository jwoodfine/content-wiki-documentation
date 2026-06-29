---
schema: foundry-doc-v1
title: "os-infrastructure and os-network-admin: Distribution Model"
slug: os-products-distribution-model
category: architecture
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: os-products-distribution-model.es.md
short_description: "Two products are planned/intended for software.pointsav.com: os-infrastructure ($19 USDC, bare metal or cloud VM) and os-network-admin ($1 USDC, mesh control plane including Linux daemon mode). Each ships as three signed artifacts per version."
cites: []
---

Two products are planned/intended for distribution at `software.pointsav.com`:

| Product | Price | What it provides |
|---|---|---|
| `os-infrastructure` | $19 USDC | Sovereign OS for PPN infrastructure nodes — runs on bare metal, cloud VMs, or QEMU |
| `os-network-admin` | $1 USDC | Mesh control plane; also available as a Linux daemon for existing systems |

Pricing is denominated in USDC on Polygon PoS. No subscription billing. No customer account required. The on-chain transaction is the receipt.

## Three artifacts per product

Each product ships three signed artifacts per version. The same Ed25519 key signs all three, so artifact authenticity is verifiable independently of the distribution server.

### `.iso` — Bare metal

ISO 9660 image with El Torito and GRUB2 multiboot loader. Writes to USB with standard tools. Boots on any x86-64 machine with hardware virtualisation support (Intel VT-x or AMD-V), or AArch64 when the AArch64 target is published.

Target hardware: retired laptops and desktops, leased servers, decommissioned enterprise kit — any x86-64 machine from approximately 2011 onwards.

### `.qcow2` — Cloud VM import

QCOW2 image (QEMU native format). Importable to major cloud providers as a custom image, then launched as a standard cloud instance. A single `platform=` boot argument selects the runtime behaviour — bare metal and cloud VM use the same kernel image.

### Daemon AppImage / `.deb` — Linux daemon (os-network-admin only)

A standalone Linux binary for `os-network-admin`. No seL4 boot required. Installs on any Linux x86-64 system with WireGuard available, joining the PPN mesh without reimaging the host. This is the primary path for existing Linux workstations — including machines that hold physical key custody for the mesh.

## License model

Payment flow:

1. Operator selects a product at `software.pointsav.com` and initiates a USDC transaction on Polygon PoS.
2. The payment watcher detects the confirmed on-chain transfer and writes a receipt.
3. The operator provides the transaction hash; the storefront issues an Ed25519-signed download token.
4. The download token unlocks all three artifact formats for the purchased version.
5. On subsequent use, the installed binary can re-verify its token against the storefront's public key without contacting the storefront again.

Source code is available on GitHub. The $19 / $1 payment covers the pre-built binary, the Ed25519 signature from the PointSav signing key, and the commercial license token.

## Two-click install principle

The target market is small and medium businesses with limited IT staff. Installation complexity is constrained to three operator decisions or fewer.

For `os-infrastructure` on bare metal: download the `.iso`, write it to USB, boot the machine, and answer three setup questions (node name, genesis endpoint, pairing code). The node appears in the fleet within thirty seconds of completing the pairing sequence.

For `os-network-admin` in daemon mode: download the AppImage, mark it executable, run it, and configure the WireGuard endpoint through the guided terminal interface. The daemon joins the mesh and registers in the fleet without requiring any system reimaging.

Any installation step that adds complexity beyond this model is product scope reduction work, not a feature addition.

## See also

- [[software-distribution-substrate]] — the technical architecture of the payment, license issuance, and binary delivery system
- [[ppn-three-path-architecture]] — the three seL4 architecture options for os-infrastructure nodes
- [[sovereign-mesh]] — the WireGuard mesh the daemon and node join on first boot
- [[genesis-protocol]] — the autonomous first-boot sequence for bare-metal os-infrastructure nodes
