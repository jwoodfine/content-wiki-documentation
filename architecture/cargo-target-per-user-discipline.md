---
schema: foundry-doc-v1
title: "Per-User Build Cache Discipline — Preventing Cross-User Cargo Races"
slug: cargo-target-per-user-discipline
language: en
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-18
editor: pointsav-engineering
cites: []
paired_with: cargo-target-per-user-discipline.es.md
---

Cargo's incremental build cache lives under `target/`. By default that is a per-crate directory inside each crate. The workspace overrides this via `CARGO_TARGET_DIR=/srv/foundry/cargo-target/` so the build cache is shared across all crates in the monorepo — saving disk space and rebuild time.

This works for a single developer. With two developers in the workspace group it becomes a race. Cargo's `target/.cargo-lock` serialises full-tree builds, so two `cargo build` invocations on different crates block one another. Worse, mixed file ownership — build artefacts written by one user interleaved with another user's — causes sporadic `Permission denied` errors during incremental rebuild, even when the crates appear to be unrelated.

The fix: `/etc/profile.d/foundry-cargo.sh` exports `CARGO_TARGET_DIR=/srv/foundry/cargo-target/$USER/`. Each user gets a private subdirectory. The build cache stays shared within a user — the original optimisation is preserved — but no longer crosses users. The environment variable takes precedence over `~/.cargo/config.toml`'s `target-dir` setting, so the change takes effect on any new shell without per-user dotfile edits.

The migration involved moving the existing 3.3 GiB cache from `/srv/foundry/cargo-target/{release,debug,cxxbridge,tmp}` into one user's subdirectory. That user's incremental state is preserved; the other developer starts with an empty cache that fills on first build.

Service accounts in the workspace group (local-doorman, local-design, and similar) do not run Cargo and do not receive a per-user cache directory. The profile.d script only exports when `/srv/foundry/cargo-target/` exists, so non-workspace contexts are unaffected.

The lesson generalises: any group-writable shared workspace path needs explicit design around which operations are safe to share (reads, content appends) and which require per-user partition (build state, lock files, temp). Cargo is the prominent example; the same logic applies to anything with mutable state under a shared root.

## See also

- [[foundry-services-slice-model]] — the cgroup partitioning that protects shared service resources in the same multi-developer environment
- [[multi-engine-session-coordination]] — the session-lock protocol that prevents a related class of same-repo conflicts
- [[totebox-session]] — the session model that the multi-operator workspace is built around
