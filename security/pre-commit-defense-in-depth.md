---
title: "Pre-commit defense in depth"
slug: pre-commit-defense-in-depth
category: security
index_group: supply-chain-controls
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "Three independent git hooks run before a commit is recorded: a helper-only gate, a data-path block, a staged-content secret and size scan, and an author-identity check. Every bypass is logged."
paired_with: pre-commit-defense-in-depth.es.md
---

**Pre-commit defense in depth** is the practice of stacking several independent checks at the
moment a commit is created, each catching a different class of mistake, so that no single failure
lets a secret, an oversized artefact, or a mis-attributed change enter history. It is the cheapest
point in the lifecycle to intervene: a rejected commit costs seconds, whereas a credential that
reaches a published repository must be treated as compromised and rotated regardless of how
quickly the commit is reverted.

The controls described here operate on the *staged* content — what the commit is about to record —
rather than on the working directory. That distinction is what makes them meaningful: a scan of
files on disk can be defeated by staging a different version, whereas reading the staged blob
through Git's own object store sees exactly what is about to be written.

## The layers

Four separate checks run at commit time, in a deliberate order: cheapest and broadest first, most
expensive last.

### Helper-only commit gate

The first check refuses a direct `git commit` unless the environment variable
`FOUNDRY_COMMIT_HELPER` is set, which the sanctioned commit helper sets for its own invocation. It
needs no file inspection at all, only an environment check, so it fails fast with an instruction
pointing at the helper rather than a mystery. The effect is that every ordinary commit is routed
through one script, which is where identity alternation, trailers, and signing are applied
consistently — the helper-only gate is what makes the [[five-stage-supply-chain|supply chain]]'s
attribution guarantees trustworthy at their origin.

The gate makes a deliberate exception for Git's own internal commits: if `GIT_REFLOG_ACTION`
indicates a merge, rebase, or cherry-pick, the commit proceeds without the helper variable. Without
that carve-out, every conflict resolution during a rebase would be blocked. A separate emergency
bypass variable exists for an operator with a legitimate reason; using it is logged rather than
silent.

### Data-path block

A second check inspects staged file *paths* — not their contents — against a catalogue of path
shapes known to carry business records and personal information: specific engine directories, a
named personnel ledger file, transaction-queue prefixes, particular document patterns, and the
input and output working directories. A small allowlist covers legitimate exceptions. This layer
exists because the most costly category of accidental commit is not a credential but a real
business record, and such a file is often indistinguishable from ordinary project content by its
extension alone. It runs before the content scan so that a business-admin file is refused on its
path alone, cheaply, rather than being pumped through pattern matching first.

### Secret-pattern and size scan

The largest layer reads a pattern catalogue from `conventions/secret-patterns.yaml` and scans the
staged content of each added, copied, modified, or renamed file. Content is retrieved through Git
plumbing rather than from disk. Binary files are skipped by a heuristic examining null bytes and the
printable-character ratio of the first four kilobytes of each file — checked before the expensive
full-content decode, after a real commit of roughly 150 business-admin files (several large PDFs and
a zip) once took over 25 minutes because that ordering was reversed.

Reading the live catalogue directly, it currently carries **23 pattern entries**: private keys in
six forms (OpenSSH, RSA, EC, DSA, PGP, and encrypted PEM), a dedicated bare WireGuard
`PrivateKey =` line pattern — added after a real, live finding of an untracked WireGuard private
key in a business-admin configuration file that the PEM-armored patterns would have missed
entirely — cloud and platform credentials (a major cloud provider's access keys, another's
service-account and API keys, and three shapes of source-forge token), three model-provider API
keys and one chat-platform token, generic password assignments and bearer tokens, a hardcoded
workspace identity path, and four patterns matching personal-information shapes — telephone
numbers, email addresses, national identity numbers, and street addresses. The catalogue has grown
twice since it was last measured at 18 entries: the WireGuard pattern and the four
personal-information patterns were both added afterward, for the reasons above.

Severity determines the outcome. Critical and high matches block the commit outright. Lower
severities print a warning and allow it to proceed. A path allowlist exempts the catalogue file
itself, `identity/*.pub` and `allowed_signers`, and two named test fixtures whose unit tests
necessarily contain secret-shaped strings.

The same layer enforces a size ceiling, set in the catalogue as `size_cap_mb: 2` and applied as a
2 MiB limit against the staged blob size, checked ahead of the secret scan so an oversized blob is
refused on size alone rather than scanned first. A separate path allowlist covers directories where
large artefacts are legitimately expected — the binary ledger, media-asset repositories, and
deployment web roots.

### Author-identity check

A `commit-msg` hook independently verifies the commit author against the two permitted contributor
identities and rejects `Co-Authored-By` or `Signed-off-by` trailers naming anyone else. This closes
a different gap from the others: it does not care what the commit contains, only that attribution
is correct and that no automated tooling has inserted itself into the authorship record. It is what
closed the 2026 mis-attribution incident class, where a stray local configuration override could
silently change the author on a run of commits.

## Why the order and the severity grading matter

False positives are the tax every secret scanner pays, and a gate that cries wolf gets bypassed
culturally long before it gets bypassed technically. Patterns whose matches are almost always real
secrets — a private-key header, a provider access key — block outright. Patterns that legitimately
appear in test fixtures and documentation — generic password assignments, token-like strings — warn
and let the commit proceed, keeping the operator informed without training them to reach for the
bypass. The allowlists follow the same philosophy: the pattern catalogue must be committable even
though it is made of the very strings it hunts, and public keys must be committable even though
they share filesystem real estate with private ones, so both are exempted by path rather than by
weakening the patterns.

## Failure behaviour and bypass

Each layer can be bypassed by its own environment variable, and each bypass is appended to a
`data/bypass-ledger.jsonl` record. The logging is best-effort and never blocks the commit itself.
This is the intended posture: an operator with a legitimate reason can proceed, and the decision
leaves a durable trace rather than being invisible.

Two degradation paths are worth stating plainly. If the pattern catalogue is missing, the secret and
size scan is skipped with a warning rather than failing closed. If PyYAML — the scan's only external
dependency, everything else being standard library — is not installed, the same thing happens. In
both cases the commit proceeds unscanned. Git's own `--no-verify` flag skips every hook entirely,
and a clone without the hooks installed enforces none of these controls; that gap is closed
operationally, by installing the hook automatically at archive-provisioning time, rather than by any
technical impossibility.

## Relationship to the promotion gate

These checks are the first of two lines. The promotion script that moves work onto the canonical
branch re-applies a comparable data-path filter against the tree about to be pushed, blocks mass
deletions and silent reverts above a threshold, enforces a top-level path allowlist for the
canonical repository, and requires explicit confirmation for the repositories that are publicly
visible. A secret that survives commit time still has to pass that second filter before it becomes
externally observable. The layering is deliberate: commit-time checks are fast and local,
promotion-time checks are slower and consider the whole tree.

## What this is not

**This is not a guarantee that no secret can be committed.** The scan is regular-expression matching
against known credential shapes. A credential in an unrecognised format, split across lines, or
encoded passes through. Detection coverage is a catalogue, not a proof — and the pattern count
stated here is a measurement, not a constant; the catalogue has grown twice in this article's
documented history, and any restatement of the number should be re-counted against the live
catalogue rather than quoted from this page.

**This is not a mandatory control.** Three separate escapes exist — per-layer environment
variables, Git's `--no-verify`, and a clone without hooks installed. The first is logged; the other
two are not.

**A missing dependency does not fail the commit.** Absent PyYAML or an absent catalogue file
silently reduces the scan to nothing while allowing the commit. This is a fail-open design, chosen
so a tooling problem does not halt work, and it should be understood as such.

**This does not scan history.** The checks apply to the commit being created. Content already in
history is unaffected, and a secret introduced before these controls existed remains there.

**The personal-information patterns are not a data-protection control.** They match four common
shapes at warning severity in most cases. They reduce accidental exposure; they do not constitute a
review of whether personal data is handled appropriately.

## See also

- [[five-stage-supply-chain]] — the promotion path whose gates form the second line
- [[contributor-model]] — the identity model the author check enforces
- [[api-key-boundary-discipline]] — the wider handling rules for credential material
- [[root-files-discipline]] — the path conventions the data-path block draws on
- [[machine-based-auth]]
- [[cryptographic-ledgers]]
- [[rotate-keys]] — the procedure that follows a credential exposure
