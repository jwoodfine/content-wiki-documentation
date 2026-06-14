---
schema: foundry-doc-v1
title: "Pre-commit defense in depth — secret scan, size guard, helper-only gate"
slug: pre-commit-defense-in-depth
language: en
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: pre-commit-defense-in-depth.es.md
---

Three commit-pipeline incidents in 2026 — an SSH key landing in a public monorepo, a `.git/config` author override that mis-attributed hundreds of commits, and chmod-revert races against the identity store — share a structural cause: there was no gate between a workspace participant and `git commit`. Any agent, any operator, could write any content and commit any way.

The Phase 1 hardening closes this with a single pre-commit hook symlinked into `.git/hooks/pre-commit` at the workspace root and every archive clone. It runs three checks against every commit.

**Helper-only commits.** The hook refuses unless a helper environment variable is set by the authorised commit helper script. Direct `git commit` invocations — by an operator, an agent, or automation — receive a clear error message pointing at the helper. Merge commits and rebases are allowed via `GIT_REFLOG_ACTION` detection; emergencies can bypass with `--no-verify`. The cost of the rule is one redirected commit; the benefit is the end of the entire "wrong author" class.

**Secret-pattern scan.** The hook reads a pattern catalogue and scans staged content against 17 regex patterns: SSH/PGP private keys (OPENSSH, RSA, EC, DSA, PGP), cloud credentials (AWS, GCP, GitHub PAT, OAuth tokens), API keys (Anthropic, OpenAI, Slack), and generic password assignments. Critical and high-severity matches block the commit; medium and low produce a warning and proceed. A path allowlist exempts the pattern catalogue itself and public-key files.

**Size guard.** Blobs over 2 MiB are refused unless the path is on the size allowlist (`data/binary-ledger/`, media-asset repos, fleet-deployment `www/`). This catches the accidental binary commit — large images, copied build artefacts, vendored databases — before history pollution.

The Python implementation is approximately 150 lines; PyYAML is the only external dependency. For a typical commit of 5–20 files, the hook adds under a second. For unusually large commits, the size guard catches the bloat before the secret scan has to read it.

What this does not solve: bypass via `--no-verify`, or a commit on a workspace clone without the hook installed. The first is intentional — an operator with a legitimate reason can bypass with a full audit log entry. The second is closed by the archive-provisioning script, which installs the hook symlink whenever an archive is provisioned.

## See also

- [[multi-engine-session-coordination]] — the session-lock protocol that closes a complementary class of coordination defects
- [[identity-ledger-schema-design]] — the identity architecture whose integrity the helper-only gate protects
- [[totebox-session]] — the session model that the helper commit path serves
- [[learning-datagraph-architecture]] — the learning loop whose trajectory-capture hooks run in the same pre-commit pipeline
