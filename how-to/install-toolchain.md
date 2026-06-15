---
schema: foundry-doc-v1
title: "How to install the development toolchain"
slug: install-toolchain
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: install-toolchain.es.md
---

The platform codebase is a Rust workspace. The development toolchain consists of the Rust compiler and standard Cargo build tools, plus the workspace commit helper that enforces staging-tier identity and SSH commit signing. This guide covers installing both, verifying the installation, and making your first test build.

For the broader workspace architecture, see [[totebox-orchestration-development]]. For opening your first session after toolchain setup, see [[open-first-totebox-session]].

## Prerequisites

- A paired device with INPUT-level access (see [[pair-a-new-device]])
- SSH access to the workspace VM (`foundry-workspace`)
- A shell session on the workspace VM

## Step 1: Install the Rust toolchain

The workspace uses a pinned Rust toolchain version specified in `rust-toolchain.toml` at the monorepo root. Install `rustup`, the Rust toolchain manager, if it is not already present:

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

After installation, source the environment file or open a new shell session. Rustup reads `rust-toolchain.toml` automatically when you enter a directory with one — no explicit version selection is needed.

## Step 2: Verify the Rust installation

Run a version check from within the monorepo clone:

```
cd ~/Foundry/clones/<your-archive>/pointsav-monorepo
cargo --version
rustc --version
```

Both commands should print the pinned version from `rust-toolchain.toml`. If rustup reports that the toolchain is not installed, run `rustup show` to trigger the automatic install of the pinned version.

## Step 3: Run a baseline build

Build the full workspace to confirm the toolchain is working end to end:

```
cargo build
```

A clean build on first run downloads and compiles all dependencies and may take several minutes. Subsequent builds are incremental. If the build fails with a missing dependency, install the named system library via the package manager (`apt-get install <lib>` on Debian/Ubuntu) and re-run.

## Step 4: Verify the commit helper

The workspace commit helper (`~/Foundry/bin/commit-as-next.sh`) requires a working SSH agent with the staging-tier signing key loaded. Direct `git commit` is blocked by a pre-commit gate — all commits must go through the helper.

Verify the helper is reachable:

```
ls ~/Foundry/bin/commit-as-next.sh
```

Verify an SSH key is loaded:

```
ssh-add -l
```

If no keys are listed, add the staging key:

```
ssh-add ~/Foundry/identity/jwoodfine/id_jwoodfine
```

The commit helper alternates author identity between `jwoodfine` and `pwoodfine` automatically — no manual selection is needed.

## Step 5: Run tests

Confirm the test suite passes before starting work:

```
cargo test
```

All tests should pass on a clean clone. A test failure before any local changes indicates either a stale clone or a build environment issue — check `git status` and compare the HEAD commit against the upstream staging branch.

## Key takeaways

- The toolchain version is pinned in `rust-toolchain.toml`; rustup reads it automatically
- `cargo build` / `cargo test` / `cargo clippy` / `cargo fmt` are always allowed without approval
- All commits use `commit-as-next.sh`; direct `git commit` is blocked at the pre-commit gate
- An SSH key must be loaded in the agent before the commit helper can sign commits

## See also

- [[totebox-orchestration-development]] — the session architecture this toolchain supports
- [[open-first-totebox-session]] — the full session startup sequence after toolchain setup
- [[pair-a-new-device]] — how a device acquires the INPUT-level access that allows commits
- [[read-write-totebox-archives]] — the full read/write flow for working in an archive
