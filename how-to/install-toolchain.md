---
schema: foundry-doc-v1
title: "How to install the development toolchain"
slug: install-toolchain
short_description: "Installs the pinned Rust toolchain with rustup, runs a baseline build and tests, and verifies the commit helper and SSH signing key needed before working in a monorepo archive."
category: how-to
index_group: getting-started
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); new contributors"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: install-toolchain.es.md
research_trail:
  sources: [pointsav-monorepo rust-toolchain.toml, bin/commit-as-next.sh, identity/ store layout]
  verification_method: "verified against the real rust-toolchain.toml pin and the commit-as-next.sh pre-commit gate already documented in read-write-totebox-archives.md"
---

The platform codebase is a Rust workspace. The development toolchain consists of the Rust compiler and standard Cargo build tools, plus the workspace commit helper that enforces staging-tier identity and SSH commit signing. This guide covers installing both, verifying the installation, and making your first test build.

For the broader workspace architecture, see [[totebox-orchestration-development]]. For opening your first session after toolchain setup, see [[open-first-totebox-session]].

## Prerequisites

- A device paired to the workspace (see [[pair-a-new-device]])
- SSH access to your workspace VM
- A shell session on that VM

## Purpose

Install the pinned Rust toolchain, confirm it builds and tests the workspace cleanly, and verify the commit helper and SSH signing key are ready — the full set of preconditions for making a first commit in a monorepo archive.

## Procedure

1. **Install the Rust toolchain.** The workspace uses a pinned Rust toolchain version specified in `rust-toolchain.toml` at the monorepo root. Install `rustup`, the Rust toolchain manager, if it is not already present:

   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

   After installation, source the environment file or open a new shell session. Rustup reads `rust-toolchain.toml` automatically when you enter a directory with one — no explicit version selection is needed.

2. **Verify the Rust installation.** Run a version check from within the monorepo clone:

   ```bash
   cd ~/Foundry/clones/<your-archive>/pointsav-monorepo
   cargo --version
   rustc --version
   ```

   Both commands should print the pinned version from `rust-toolchain.toml`. If rustup reports that the toolchain is not installed, run `rustup show` to trigger the automatic install of the pinned version.

3. **Run a baseline build.** Build the full workspace to confirm the toolchain is working end to end:

   ```bash
   cargo build
   ```

   A clean build on first run downloads and compiles all dependencies and may take several minutes. Subsequent builds are incremental. If the build fails with a missing dependency, install the named system library via the package manager (`apt-get install <lib>` on Debian/Ubuntu) and re-run.

4. **Verify the commit helper.** The workspace commit helper (`~/Foundry/bin/commit-as-next.sh`) requires a working SSH agent with the staging-tier signing key loaded. Direct `git commit` is blocked by a pre-commit gate — all commits must go through the helper.

   Verify the helper is reachable:

   ```bash
   ls ~/Foundry/bin/commit-as-next.sh
   ```

   Verify an SSH key is loaded:

   ```bash
   ssh-add -l
   ```

   If no keys are listed, add your staging identity's key:

   ```bash
   ssh-add ~/Foundry/identity/<your-identity>/<your-key>
   ```

   Staging-tier teams typically alternate commit authorship across two or more identities automatically — check your workspace's identity store for the exact names in use.

5. **Run tests.** Confirm the test suite passes before starting work:

   ```bash
   cargo test
   ```

## Expected outcome

`cargo build` and `cargo test` both complete cleanly on the pinned toolchain version, the commit helper script is reachable, and an SSH key is loaded in the agent — the workspace is ready for a first commit.

## Verification

All tests should pass on a clean clone. A test failure before any local changes indicates either a stale clone or a build environment issue — check `git status` and compare the HEAD commit against the upstream staging branch.

## Rollback

Toolchain installation has no destructive side effect to roll back. If `rustup` was installed in error, remove it with `rustup self uninstall`; this does not affect the monorepo clone itself.

## Next steps

- [[read-write-totebox-archives]] — the full read/write flow for working in an archive
- [[open-first-totebox-session]] — the full session startup sequence after toolchain setup

## See also

- [[totebox-orchestration-development]] — the session architecture this toolchain supports
- [[pair-a-new-device]] — how a device gets paired to the workspace in the first place
