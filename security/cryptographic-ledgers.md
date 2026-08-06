---
schema: foundry-doc-v1
title: "Cryptographic ledgers"
slug: cryptographic-ledgers
category: security
index_group: cryptographic-verification
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "An append-only log where each entry's hash covers the one before it, closed by Ed25519-signed checkpoints and anchored monthly in a public transparency log. Implemented as a linear chain, one flat file per tenant."
paired_with: cryptographic-ledgers.es.md
---

**A cryptographic ledger** is an append-only record in which each entry's hash incorporates the
hash of the entry before it, so that altering or removing any past entry invalidates every hash
that follows. The chain does not prevent tampering — nothing stored on ordinary storage can — but
it makes tampering detectable by anyone holding a later hash, without requiring trust in the
system that produced the record. In a traditional database, an administrator with sufficient
privilege can silently edit a stored record; nothing in the data itself betrays the change. A
cryptographic ledger removes that privileged mutable path.

Two further mechanisms turn a detectable-tampering property into an externally verifiable one. A
signed checkpoint commits the log's operator to a specific root state at a specific size, so a
reader can confirm they are looking at the log the operator published rather than a parallel
version. Anchoring that checkpoint in an independent public log establishes that the state existed
before a time the operator does not control. This platform's implementation is live in
[[service-fs]], the per-tenant WORM (write-once-read-many) ledger service,
and the description below reflects the code as it runs today.

## The implementation

### Storage shape

One newline-delimited JSON file per tenant, at `<root>/<moduleId>/log.jsonl`. Each line is a
record with four fields: a monotonic `cursor`, a `payload_id`, the `payload` itself as arbitrary
JSON, and `this_hash`.

The chain is a **linear SHA-256 hash chain, not a Merkle tree**. Each entry's hash is computed over
the previous hash, the cursor in big-endian form, and the length-prefixed payload identifier and
payload bytes. The first entry's predecessor is a fixed origin hash derived from a version-tagged
constant string, so the chain has a well-defined start rather than an arbitrary seed. Because an
inclusion proof over a linear chain is a walk of the chain rather than a logarithmic path, proof
size grows with distance from the checkpoint; a Merkle-tree upgrade that would shrink proofs while
leaving the interface unchanged is described in the code's own comments as a follow-up refinement,
not a structure that exists today.

Write discipline is deliberate and worth stating because it is where immutability actually comes
from in practice. An append writes the whole log to a temporary file, synchronises it to disk,
atomically renames it into place, and sets the result read-only. On reopening, every record's hash
is recomputed and checked against what is stored; a mismatch is refused as a tamper condition
rather than silently accepted. The stronger filesystem-level immutability flag requires a
privilege the service does not hold and is deferred to service-unit configuration. The cost of
this design is acknowledged in the code itself: rewriting the entire log on every append is linear
in the log's size — a segment-batched tile layout (sealed segments of 256 entries, in the style
used by certificate-transparency infrastructure) is the planned performance upgrade, not a
structure that exists on disk today. The record schema and the service's interface are designed to
survive that upgrade unchanged.

### Checkpoints

A checkpoint carries the log's origin string, its current entry count, a root hash, the algorithm
name, a timestamp, and optionally a signature. When a signing key is configured — supplied as a
raw 32-byte Ed25519 seed whose path is given by an environment variable — the checkpoint body is
signed in the C2SP signed-note form: origin, size, and base64-encoded root hash on separate lines.
Signature verification is exposed as an independent function taking a checkpoint and a public key,
so a third party can verify without running the service. Omitting the key runs the ledger unsigned,
chained but without an operator commitment a verifier can check.

### Proofs

Both proof types are implemented rather than stubbed. An inclusion proof takes an entry cursor and
a checkpoint and returns the segment of chained hashes linking that entry to the checkpoint's tip.
A consistency proof takes two checkpoints and returns the segment demonstrating that the later one
extends the earlier append-only. Both are exercised by tests that restart the service and confirm
the chain continues correctly across the restart boundary.

The verification workflow for an auditor examining a historical record is mechanical: recompute
the record's chain hash from its stored fields and confirm it matches; verify the record's
inclusion in the chain against a checkpoint; verify the checkpoint's signature against the
tenant's public key; and, where external assurance is required, verify the checkpoint's
consistency against the anchored one. Every step uses public algorithms and the tenant's public
key — nothing in the workflow requires PointSav's cooperation, the operator's goodwill, or access
to any system beyond the ledger data and the public log.

## Anchoring

Detectability within a log does not establish *when* a state existed. That is what the anchoring
step provides.

A dedicated emitter fetches the current checkpoint from the file service over its local HTTP
interface, serialises it, computes a SHA-256 digest of that serialisation, and submits the digest
to the public Sigstore Rekor transparency log as a version 2 hashed-record request
(`hashedRekordRequestV002`), with an Ed25519 signature and the corresponding public key attached.
The key is generated fresh for each run — the value being sought is Rekor's timestamp and
inclusion proof, not continuity of key identity. The returned transparency-log entry is then
appended back into the ledger itself under a timestamped identifier, so the anchoring event becomes
part of the record it anchors.

The submission endpoint is a specific yearly Rekor shard, overridable by environment variable
because Sigstore rotates shards annually and warns against hardcoding one. The emitter performs no
retries: each stage failure exits with a distinct code, and recovery is the timer's next run. The
schedule is monthly — the first of the month at 02:30 UTC, with catch-up enabled if the machine was
off and a randomised delay of up to fifteen minutes.

The deployed systemd service unit's own comment describes the anchoring payload as wrapping "a
Sigstore hashedrekord v0.0.1" entry. The emitter's actual code implements the v0.0.2 request shape
throughout — the v0.0.1 top-level `kind`/`apiVersion` envelope is explicitly removed, the digest is
sent as raw bytes rather than the v0.0.1 base64-of-PEM form, and tests assert the older envelope
fields are absent. The comment is stale relative to the code that ships; the code is authoritative,
and the anchoring mechanism itself functions as v0.0.2 regardless of what the unit file says.

## Who writes to it

The ledger is a shared facility reached over a local HTTP interface on port 9100, with each writer
identifying its tenant through a required `X-Foundry-Module-ID` header that the service checks
against its own configured module ID before accepting a write. Confirmed writers are the ingest
console, the email service, the people service, the network-administration fleet watcher, and the
anchoring emitter writing back its own result.

One defect exists in that list: the fleet watcher's topology-event append (`write_worm_event` in
`app-network-admin`) posts to the ledger's append endpoint without setting the module-ID header the
service requires, and no compensating path supplies it elsewhere in that call. As written, the
service's own header-enforcement check would reject that write. It is recorded here as a verified
finding, not described as working.

## What the ledger is used for

The discipline applies wherever the platform records facts it may later need to prove:

- **Corporate and operational records** — entries are appended to the WORM ledger before any
  downstream processing touches them, so the ledger holds the earliest durable state.
- **Identity observations** — the [[identity-ledger-schema-design|identity ledger]] writes its
  person, anchor, and claim records through the same append path.
- **Audit posture** — the append-only invariant, deterministic verification, and external anchoring
  give compliance reviewers a record whose integrity does not depend on trusting the operator's
  access controls. The architecture is aligned in structure with recordkeeping regimes that require
  WORM storage, though alignment with any specific regulation is a matter for formal assessment
  rather than an automatic property of the design.

## What this is not

**The on-disk format is not C2SP tlog-tiles.** It is a single flat newline-delimited JSON file per
tenant. The multi-file, base64-encoded, 256-entries-per-tile layout appears in the component's
architecture and research documents as a target design and in the implementing type's name; no
code creates or reads a tile file today. Only the signed-note checkpoint form of C2SP is actually
implemented.

**The structure is not a Merkle tree.** It is a linear hash chain. Inclusion proofs are chain
segments, not logarithmic paths, and the tree upgrade is a stated follow-up without a committed
schedule.

**Append-only is not deletion-proof.** The guarantee is detection. Someone with write access to the
storage can replace the file; the ledger's response is that reopening it fails verification and
that any previously anchored checkpoint no longer matches. Nothing physically prevents the
substitution.

**Anchoring is not continuous.** Between monthly runs, a state has the ledger's internal integrity
and the operator's signature, but no independent timestamp. The exposure window is up to a month.

**An unsigned ledger is a weaker claim.** Signing is optional at startup. Without a key, entries are
chained but no checkpoint carries an operator commitment, and the anchoring path has nothing
meaningful to submit.

**The ledger is not a blockchain.** There is no distributed consensus, no cryptocurrency, no
mining, and no peer network — it is a single-writer, per-tenant append-only log whose external
trust anchor is a public transparency log, the same pattern used by certificate transparency. Nor
is it encryption: the ledger makes records *tamper-evident*, not secret; confidentiality is handled
by separate layers.

**Wiki article content does not flow into this ledger.** The knowledge engine has no client for the
file service and makes no append call. Article revision history is ordinary Git history, which is a
different and weaker property than the one described here.

**Completeness is not this layer's job.** The ledger does not prevent an operator from *failing to
record* something: it proves that what was recorded has not been altered, and that recorded
history was never rewritten after anchoring, but the decision of what enters the ledger sits
upstream of it.

## See also

- [[worm-ledger-architecture]] — the write-once record model this implements
- [[worm-ledger-storage-architecture]] — the storage layout and its planned evolution
- [[fs-anchor-emitter]] — the component performing the monthly submission
- [[doctrine-invention-7-rekor-anchoring]] — the anchoring design and its rationale
- [[merkle-proofs-as-substrate-primitive]] — the proof structure the planned upgrade would adopt
- [[verify-worm-ledger]] — the operator procedure for checking integrity directly
- [[identity-ledger-schema-design]] — another writer using the same append path
- [[crypto-attestation]]
