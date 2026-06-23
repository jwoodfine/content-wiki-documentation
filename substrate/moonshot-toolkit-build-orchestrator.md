---
schema: foundry-doc-v1
content_type: topic
title: "The moonshot-toolkit Build Orchestrator"
slug: moonshot-toolkit-build-orchestrator
category: substrate
last_edited: 2026-06-23
editor: pointsav-engineering
status: stable
bcsc_class: no-disclosure-implication
---

moonshot-toolkit is a Rust-only build orchestrator for seL4 unikernel images,
replacing the Python and CMake toolchain provided by the seL4 Microkit framework. It
reads a TOML system specification, derives a deterministic content-addressed build
manifest, and orchestrates the cross-compilation and image assembly pipeline through to
a bootable elfloader binary for the AArch64 target.

## 1. Why Rust-Only

The seL4 Microkit framework ships a Python image-assembly script and a CMake build
system. These tools are adequate for general embedded development but present three
problems for a reproducible-build discipline.

First, determinism. Python dictionary ordering is implementation-defined; CMake
dependency discovery varies across versions. A Rust binary built from a fixed source
revision with vendored dependencies produces bit-identical plan bytes across machines
and over time.

Second, auditability. A single Rust binary is an auditable end-to-end artefact.
Python scripts, CMake modules, Makefiles, and shell wrappers compose a multi-language
audit surface that is difficult to reason about formally.

Third, network isolation. The Reproducible-Verification-On-Customer-Metal
convention requires that build steps run without network access. Python's `pip install`
and CMake's `find_package` are live network surfaces. A Rust binary with vendored
dependencies eliminates them.

## 2. SystemSpec — The Input

A system specification is a TOML file that describes a seL4 Microkit system. It is
the Rust-native equivalent of Microkit 2.2.0's system-description XML schema.

The specification declares four collections:

**Protection domains** are isolated, single-threaded software components scheduled by
the seL4 kernel. Each domain has a name, a path to its source binary, a scheduling
priority (0 is highest, matching seL4 and Microkit conventions), and a stack size in
bytes (defaulting to 4 KiB per Microkit). The system may contain at most 63 protection
domains, the hard limit imposed by the Microkit framework.

**Channels** are point-to-point communication links between protection domains, using
seL4's Protected Procedure Call or notification mechanisms. Each protection domain
may have at most 63 channels.

**Memory regions** declare physical memory mappings with caching and permission
attributes and an optional prefill from a binary blob. Overlapping regions are
rejected at parse time.

**IRQ delivery** entries bind hardware interrupt lines to specific protection domains.

Validation rules are enforced during parsing: no duplicate domain names, all channel
endpoints and IRQ targets must reference declared domains, and memory regions must
not overlap.

A minimal hello-world specification looks like:

```toml
[[protection_domains]]
name     = "hello"
binary   = "moonshot-toolkit/examples/hello.c"
priority = 100
stack_bytes = 65536
```

## 3. BuildPlan — The Manifest

Given a parsed SystemSpec, moonshot-toolkit generates a BuildPlan: a deterministic,
content-addressed build manifest.

The plan contains three fields. The `spec_hash` is the SHA-256 digest of the canonical
TOML rendering of the SystemSpec — it identifies the input. The `steps` field is an
ordered list of build steps: one CompilePd step per protection domain followed by a
single AssembleImage step. The `plan_hash` is the SHA-256 digest of the canonical
JSON rendering of `(spec_hash, steps)` — it is the value the customer-apex cosignature
commits to.

The determinism guarantee is strict: the same SystemSpec always produces the same
`plan_hash`. This property is covered by tests and is foundational to the
Reproducible-Verification-On-Customer-Metal convention: a customer can verify that a
delivered binary corresponds to a known specification by recomputing the plan_hash and
comparing it against a cosigned value.

## 4. Build Commands

A BuildPlan contains two kinds of steps.

**CompilePd** cross-compiles a protection domain's source file to a bare-metal AArch64
ELF binary. The invocation uses the `aarch64-linux-gnu-gcc` cross-compiler with flags
appropriate for seL4 Microkit protection domains:

- `-nostdlib -nostartfiles`: no C standard library or startup files; the protection
  domain provides its own `_start` entry point.
- `-ffreestanding`: no hosted-environment assumptions; no implicit includes.
- `-static -no-pie`: Microkit loads PD binaries at fixed virtual addresses; dynamic
  linking is not available.
- `-march=armv8-a`: target AArch64 ISA.
- `-mgeneral-regs-only`: exclude FPU and SIMD registers; the seL4 kernel does not
  save FPU state by default.

The output is a statically linked ELF executable targeting the AArch64 architecture.

**AssembleImage** produces the bootable system image. It executes in pure Rust without
invoking Python, CMake, or shell scripts, in five stages:

1. **CPIO archive**: the protection-domain binaries, the seL4 kernel ELF, and the
   kernel device tree binary are packed into a CPIO "newc" archive using a Rust-native
   writer (`src/cpio.rs`). The writer implements the exact 110-byte ASCII header format
   and 4-byte-aligned padding that the seL4 elfloader's CPIO parser requires.

2. **Archive embedding**: the CPIO archive is embedded into an assembly stub
   (`archive.S`) using `.incbin`. This file is compiled as one object in the final link.

3. **Elfloader compilation**: the 44 C and ASM source files of the seL4 elfloader
   (from `vendor-sel4-tools/elfloader-tool/`) are compiled with AArch64 bare-metal
   flags, together with the seL4 libcpio helper library. All include paths — elfloader
   headers, CMake-generated configuration headers, kernel autoconf — are resolved from
   the vendor trees present in the repository.

4. **Link**: all objects are linked with `-nostdlib -static -lgcc` using a preprocessed
   version of the elfloader's linker script. The result is a bare-metal AArch64 ELF
   with entry point `0x40400000`.

5. **Output**: the linked ELF is copied to the specified output path (default:
   `build/system-image.bin`).

## 5. Reproducibility and Cosignature

The plan_hash ties together the input specification and the full ordered build procedure.
A customer receiving a binary artefact can verify its provenance by:

1. Reconstructing the SystemSpec from the shipped TOML.
2. Running `moonshot-toolkit plan` to derive the BuildPlan.
3. Comparing the computed plan_hash against the value in the vendor's cosigned manifest.
4. Optionally rerunning `moonshot-toolkit build` on their own infrastructure to verify
   the binary byte-for-byte.

This chain satisfies the Capability Ledger Substrate property: cryptographically auditable
access-control decisions anchored to logs the customer controls. The plan_hash is the
point at which the cosignature (Sigstore Cosign with customer-apex key) attaches.

## 6. Phase 1C Status

moonshot-toolkit v0.3.0, released 2026-05-29, completes the Phase 1C milestone:

- **Phase 1C.a** (v0.2.0, 2026-05-27): CompilePd invokes the real AArch64
  cross-compiler and produces a verified bare-metal ELF. Confirmed: `build/hello.elf`,
  entry point `0x40010c`.

- **Phase 1C.b** (2026-05-27): seL4 AArch64 kernel built from source with
  `KernelPlatform=qemu-arm-virt`. The `kernel.elf` at `vendor-sel4-kernel/build/aarch64-qemu/`
  is a valid AArch64 ELF, entry point `0xffffff8040000000`.

- **Phase 1C.c** (2026-05-28): full QEMU boot confirmed. elfloader → seL4 kernel →
  rootserver chain produces output: "Booting all finished, dropped to user space".

- **Phase 1C.d** (v0.3.0, 2026-05-29): AssembleImage fully implemented in Rust.
  `moonshot-toolkit build moonshot-toolkit/examples/hello-world.toml` produces
  `build/system-image.bin`, entry point `0x40400000`. QEMU boots the image using
  `-m 1G -kernel build/system-image.bin`.

The complete build pipeline — from TOML specification to a booting seL4 system — now
runs in a single `cargo run` invocation with no Python, CMake, or shell in the
critical path.

## See Also

- [[sel4-aarch64-qemu-substrate-target]] — the seL4 kernel target that
  moonshot-toolkit's images run on
- [[capability-ledger-substrate]] — what the built images enforce at runtime
