---
title: "Cryptographic payload attestation"
slug: crypto-attestation
category: security
index_group: cryptographic-verification
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "Cryptographic payload attestation lets a reader recompute a hash of published content and compare it against a published value. Unwired, cosmetic prototypes exist in a few release templates; the knowledge wiki does not offer it."
paired_with: crypto-attestation.es.md
---

**Cryptographic payload attestation** is the practice of publishing a cryptographic digest of a
document alongside the document itself, so that any reader can recompute the digest from what
they actually received and detect a discrepancy without trusting the server that sent it. The
guarantee is narrow and worth stating precisely: a matching digest shows that the bytes rendered
in the reader's browser correspond to a value the publisher committed to. It does not by itself
prove *when* that commitment was made, nor who made it, unless the digest is separately signed or
anchored in a timestamped log.

The technique is attractive for published corporate and technical material because it is
inspectable by the reader without special tooling. A browser can compute a SHA-256 digest of a
text block using the Web Crypto API in a few lines of script, and the reader can compare the
result against a value printed on the page or held elsewhere.

## What exists today

No shipped PointSav surface offers reader-verifiable attestation. What exists instead is a small,
unwired, cosmetic pattern that recurs in a handful of files without ever being load-bearing.

Four files in the canonical source tree contain a client-side SHA-256 computation of the same
shape: `service-content/templates/pointsav-monolith.html` and its sibling
`woodfine-brutalist.html`, plus two proposed public-site mockups under `proposed/pointsav.com/`
and `proposed/woodfinegroup.com/`. Each renders a "SHA-256 Checksum" field in a metadata sidebar,
computes a digest of the currently-rendered page text via `crypto.subtle.digest('SHA-256', ...)`,
and writes the result into that field — a live display of "here is a hash of what you're looking
at," not a value the publisher fixed at build time. Each is paired with a `navigator.sendBeacon`
telemetry call fired on page unload, unrelated to the hash itself. A direct search of the
canonical tree found no Rust code, configuration, or build wiring that references any of the four
files by name — none of them is currently served by anything. This is the same code already
flagged elsewhere in this wiki ([[zero-execution-routing]]) for contradicting a separate "zero
client-side JavaScript" claim; here the relevant point is narrower: it is a page-integrity display
of the kind a reader might mistake for attestation, not an audit-trail or authorship mechanism, and
it has never been wired to serve any live page.

A fifth, unrelated implementation exists in the workplace spreadsheet application, which computes
a SHA-256 digest of its own canonicalised document state and stores it in a save-integrity audit
field — a different purpose (detecting accidental local corruption) from anything a reader of a
published page would use.

## What the knowledge wiki actually offers

The knowledge wiki engine, `app-mediakit-knowledge`, exposes no attestation affordance to a
reader. This was checked by reading its client script and its layout code in full and by
searching the whole of that component for hashing, signature, checkpoint, and verification terms.

Its client-side script implements a theme toggle, a mobile navigation drawer, code-block copy
buttons, table wrapping, and two explicitly labelled stubs for a future phase. There is no digest
computation of any kind. Its sidebar renders a main-page link, a category list, a conditional
guides section, and a table of contents built from the article's own headings — no hash, no
signature link, and no verify control.

Two "hash"-shaped things do appear in that component and neither is an attestation feature. One is
an HTTP `ETag` derived from a static asset's digest, used for cache validation of stylesheets and
fonts. The other is a footer provenance line stating that each revision is content-addressed by
its commit hash, which refers to the article's Git commit identifier.

That provenance line points at the mechanism the wiki genuinely relies on. The content mount is
itself a Git repository, and the engine's history module walks the repository log to produce a
per-article revision list — commit identifier, author, ISO date, and message. A reader therefore
has a tamper-evident *revision history* in the ordinary Git sense, which is a meaningful record
but is not a published digest they can independently recompute against the page they are reading.

## The relationship to the append-only ledger

The platform does operate a real, independently verifiable transparency mechanism, described in
[[cryptographic-ledgers]]: an append-only hash-chained log with Ed25519-signed checkpoints, whose
checkpoint digest is submitted monthly to the public Sigstore Rekor transparency log. That
mechanism delivers exactly what naive client-side hashing cannot — third-party evidence that a
given state existed at a given time.

The important qualification is that **wiki article content does not flow into that ledger**. The
knowledge engine contains no client for the file service and makes no append call; the ledger's
writers are the ingest console, the network administration fleet watcher, the email service, the
people service, and the anchoring emitter itself. Presenting the ledger's timestamping property as
though it covered published wiki articles would be inaccurate.

## Verifying an attestation by hand

Spelling out what an independent check would look like, once such a feature exists, clarifies why
the design is credible in principle even though nothing implements it today. A reader would select
and copy the visible text of a language block exactly as rendered, compute a SHA-256 digest of
that text on their own machine using any standard tool, and compare the result against the hash
displayed on the page — an exact string comparison, where any difference in any hex digit means
the content differs from what produced the displayed value.

Two properties of SHA-256 would carry the guarantee. Preimage resistance means an attacker cannot
construct alternative text that matches a given hash, so tampered content cannot keep the original
hash and remain consistent. The avalanche property means even a one-character alteration changes
the digest completely, so tampering would never be *nearly* undetectable — it would be conspicuous
or absent. A working version of this feature would need to be strict about what gets hashed —
which block, which whitespace normalisation, which encoding — because a verifier who cannot
reproduce the exact input bytes cannot reproduce the hash. None of the four prototype files above
solve this: each recomputes from whatever the page currently renders, which means a
man-in-the-middle who alters the text before it reaches the browser also alters the hash the
script displays, defeating the guarantee this technique is meant to provide.

## What a complete implementation would require

A reader-verifiable attestation for published articles would need, at minimum: a canonicalisation
rule fixing exactly which bytes are hashed and how whitespace and markup are normalised, so
publisher and reader compute over the same input; a publication path that records the digest at
build time rather than recomputing it in the browser from whatever was served; a signature over
that digest under a key the reader can obtain independently; and, for timestamping, submission of
the signed digest to the existing anchoring path described above. None of these four steps is
implemented for wiki content, or for any of the four prototype files, today.

## What this is not

**This is not a feature the knowledge wiki currently provides.** No article page computes,
displays, or verifies a content digest. A reader visiting the wiki today has no attestation
control available to them.

**A self-computed page hash is not tamper protection on its own.** In the prototype files, the
digest is computed by script served from the same page as the content. An attacker able to alter
the content is generally able to alter the script. Such a display is at most a cosmetic integrity
aid against accidental corruption, not a defence against a compromised publication path, unless
the expected value is obtained from an independent source.

**Attestation is not authentication of authorship.** An unsigned digest says nothing about who
published the content. Nothing in the prototypes described above signs the digest with a
publisher key.

**Attestation is not a timestamp.** Only the separate anchoring path establishes that a state
existed at a point in time, and it does not currently cover wiki articles or any of the prototype
files.

**Git revision history is not the same guarantee.** It records what the repository holds and who
committed it, which is valuable provenance, but it is verified by trusting the repository rather
than by recomputing a digest of the delivered page.

## See also

- [[cryptographic-ledgers]] — the append-only hash-chained log and its signed checkpoints
- [[doctrine-invention-7-rekor-anchoring]] — the monthly submission of checkpoints to a public transparency log
- [[verify-worm-ledger]] — the operator procedure for checking ledger integrity directly
- [[merkle-proofs-as-substrate-primitive]] — the proof structure a future upgrade would adopt
- [[app-mediakit-knowledge]] — the wiki engine whose current capabilities are described above
- [[zero-execution-routing]] — the pattern article where this same prototype code is separately flagged for an unrelated overclaim
