---
schema: foundry-doc-v1
title: "Registry-driven releases: one source of truth for tokens, components, and counts"
slug: registry-driven-releases
short_description: "Explains the registry-driven architecture behind the design-system site's releases: navigation, homepage statistics, the machine-readable registry endpoint, MCP responses, and release packaging all resolve against one registry file, so they cannot drift apart — illustrated with two real defects from the system's own history rather than hypotheticals."
category: design-system
type: topic
content_type: topic
quality: complete
index_group: token-concepts-and-tooling
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: registry-driven-releases.es.md
cites: []
---

A design-system site makes small factual claims everywhere: the navigation
lists eight sections, the homepage says 146 tokens and 37 components, the
releases page says a bundle contains what it contains, the machine endpoint
returns counts to whatever agent asked. Each claim is easy to state and easy
to get wrong, because each usually lives in a different file, maintained by
a different hand, on a different day.

The v3 architecture of design.pointsav.com takes one position on this: every
one of those claims must resolve against a single registry file. Navigation,
homepage statistics, the machine-readable registry endpoint
(`/registry.json`), MCP tool responses, and the packaging that cuts release
downloads all read the same registered records. A component that is not
registered cannot appear in the nav; a count on the homepage cannot differ
from what a release contains, because there is exactly one place either
number comes from. Releases stop being hand-assembled artifacts and become
cuts of the registry.

That is the thesis. What makes it worth an article is that this system has
already violated it twice, in small and instructive ways, in its own working
history — and both defects are better teachers than any hypothetical.

## The failure mode: parallel copies maintained by hand

The general pattern is well documented in software engineering practice.
The docs-as-code movement exists because documentation maintained beside
code, rather than in the same pipeline as code, reliably drifts: the code
changes continuously, the parallel description changes sporadically, and the
gap compounds. The remedy is structural rather than disciplinary — keep one
source and generate the rest, so that the parallel copy that could drift
does not exist.

Design tooling reached the same conclusion for token values. Style
Dictionary's entire model is a single source of token JSON transformed into
per-platform outputs — CSS custom properties, iOS and Android formats —
precisely so that no platform maintains its own hand-edited copy of a color.
Tokens Studio applies the same logic to the design-to-code boundary, using a
git repository as the source of truth that both the design tool and the
build pipeline synchronize against. The registry architecture described here
extends that established principle one level up: not just token *values*,
but the site's claims *about* its tokens and components — what exists, what
it is called, how many there are, what ships in a release.

## A worked example from our own review

During the 2026-07-10 review of the v3 homepage mockup, the page carried an
illustrative `curl` response showing what `/registry.json` would return —
including a `nav` array listing the site's sections. The visible navigation
on the same page had eight entries. The registry JSON's `nav` array had
seven: it omitted "Running at PointSav," an entry the rendered nav plainly
included.

On a page whose central diagram argues that the nav and the registry cannot
disagree because both read the same file, the nav and the registry
disagreed. The reason is exactly the failure mode above: in a static mockup,
both the visible nav and the "registry" are hand-typed HTML, so the
structural guarantee the page describes did not yet protect the page
describing it. The defect was found in review and fixed the same day, and it
is recorded here deliberately: it is a genuine, verified instance of how
easy the principle is to violate by accident — one edit applied to one copy
and not the other — and therefore of why the guarantee has to be built,
not resolved to.

## A second example: two token bundles

The same week supplied a larger instance. The design-system repository
carried two files named `dtcg-bundle.json` — one at the repository's
`tokens/` root, one inside the vault — with overlapping content and no
declared relationship. A full reconciliation diff, resolving every token
alias to its final literal value on both sides rather than comparing raw
strings, found 107 token paths present in both files. Forty of the fifty
apparent value conflicts were false alarms — one side referenced an alias
where the other hardcoded the literal the alias resolves to — but ten were
real conflicts, and five primitive colors existed only in the copy that was
no longer maintained.

Two details make this example useful. First, neither copy actually fed the
site: the tokens design.pointsav.com serves resolve through one pipeline —
the vault's source files (`primitive.json`, `pointsav-brand.json`, plus the
`paper` and `writing` pillars) compiled into a single resolved export,
`dtcg-vault/exports/tokens.full.json` — so the divergence was invisible in
production while remaining a live hazard for any tool that picked the wrong
file. That export has grown well past the two-pillar shape this section
first measured; the current published bundle spans four pillars and several
hundred leaves total, and the file itself is the current count, not a
number fixed to this article's writing date. Second, the resolution was
registry-shaped: declare
one copy canonical, fold the five genuinely-new values into it, and replace
the other with a deprecation stub that points at the canonical file. Not a
cleanup of two copies into two better copies — the elimination of the second
copy as a thing that can drift.

## What the registry drives

In the v3 architecture, the registry file is the single source for five
consumers: the navigation; the homepage statistics; the `/registry.json`
endpoint that returns the same records to machines; the [[design-system-substrate|MCP tools]] that
answer agent queries about tokens and components; and release packaging,
where a versioned download — token bundle, asset archive, manifest — is cut
from registered entries, so nothing ships that is not registered and nothing
registered can be silently omitted from what ships. The property being
bought is not tidiness. It is that the site's factual claims become
verifiable against one file, by anyone, including the site's own build.

## Which license applies to what

Three licenses are in play, and they do not substitute for one another. The
registry describes token and component **data**, which is Apache-2.0. The
**server** that serves `/registry.json` and the MCP endpoint
(`app-privategit-design` in the PointSav monorepo) is AGPL-3.0-or-later.
**This article** is CC BY 4.0, the license of the documentation wiki it is
published in. A release download built from the registry carries the data
license, Apache-2.0, not the server's.

## Scope and limits

Stated plainly: as of this writing, the registry-driven site is a design
mockup under review, not the live production site, and the mockup's registry
JSON is itself hand-maintained — which is precisely how the nav defect
described above was possible. The drift-impossibility claim is a property of
the target architecture, in which the registry is generated from the vault
and every consumer reads it at build or request time; it is not yet a
property the mockup can enforce, and a build-time consistency check that
fails when rendered claims differ from the registry is designed but not
implemented. Both worked examples in this article are real and were verified
against the repository's own history before publication; no external case
studies or adoption figures are claimed, because none exist yet.

---

*This article is background for readers of the PointSav Design System
documentation, ahead of the releases page and the machine-surface reference.
It explains why the site's counts, navigation, endpoints, and downloads are
designed to resolve against one registry file, using the system's own
recorded defects as evidence rather than hypotheticals.*
