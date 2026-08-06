---
schema: foundry-doc-v1
title: "Figma and Tokens Studio: consuming the design system's tokens in a design tool"
slug: figma-tokens-studio-integration
short_description: "Explains how designers bring the PointSav Design System's published DTCG token export into Figma with the Tokens Studio plugin's URL sync — a read-only pull from the system's own hosted JSON, with no export/import step — and why the read-only direction is a governance feature, with an honest comparison to Penpot's native token support."
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
paired_with: figma-tokens-studio-integration.es.md
cites: []
---

The PointSav Design System publishes its complete token set as a single file
in the Design Tokens Community Group (DTCG) interchange format, the W3C
community group specification whose Format Module reached its first stable
version in October 2025. That file is not a build artifact buried in a
repository; it is served by the design-system site itself, at a stable URL,
regenerated from the same registry that renders the documentation pages.
Because the export uses the community interchange format rather than a
proprietary one, any tool that reads DTCG JSON can consume it — and the most
practical consequence of that, for a design team, is that the tokens can be
brought directly into Figma.

This is a working, documented path today, not a roadmap item. The design
system's own get-started guide for designers records it in one line: point
the Tokens Studio plugin at the published token file. This article explains
what that line means, why the integration is shaped the way it is, and where
its edges are.

## The path, concretely

Tokens Studio is a widely used plugin for Figma, available in the Figma
Community plugin directory, that manages design tokens inside a Figma file
and applies them to design elements. Two of its documented capabilities carry
this integration:

- **DTCG format support.** The plugin can operate on tokens in W3C DTCG
  format — the dollar-prefixed `$value` / `$type` / `$description` structure
  this design system publishes — selectable in the plugin's settings. The
  plugin's documentation presents this format option without a paid-plan
  requirement.
- **URL sync.** The plugin can be pointed at a hosted JSON file and pull
  tokens from it. Its documentation describes this provider as read-only: the
  plugin fetches the tokens and lets the designer apply them to Figma
  elements, but does not write changes back to the URL. As the design
  system's tokens change upstream, the plugin surfaces pull indicators so the
  Figma file can be brought current. The documentation states no paid-plan
  restriction on this provider.

Connecting the two: a designer installs the plugin, adds the design system's
published token export as a URL sync source, and pulls. This release's token
values are then available inside the Figma file — no export/import ceremony,
no manual re-entry of values, no copy of the token set maintained by hand.
That is the same framing the design-system site itself uses, and this article
is the background behind it.

The plugin itself is free to install, and the two capabilities this path
depends on are documented without a paid tier attached. Tokens Studio does
sell pro features — multi-file remote sync and branch switching among them —
but this integration does not require them. That distinction is stated
carefully on purpose: the vendor's pricing is the vendor's to change, and the
claim made here is about what its documentation says at the time of writing.

## Why read-only is the right direction

It would be natural to read "read-only" as a limitation. For this design
system it is the correct behavior, and worth defending explicitly.

The token set is governed in one place: the design system's repository, where
changes are proposed, reviewed, versioned, and released. The published DTCG
file is an output of that governance, generated from the same registry that
drives the documentation site and the machine API. If a design tool could
write token values back, there would be two sources of truth — the repository
and whichever Figma file most recently pushed — and every downstream consumer
would inherit the ambiguity.

The read-only pull gives designers exactly the relationship code consumers
already have: subscribe to the released values, work with them, and route
proposed changes through the system's contribution process rather than
around it. A designer who needs a token changed files the change against the
design system; when it lands and a release publishes, every subscribed Figma
file pulls the same corrected value that every stylesheet build does. One
change, at the token, everywhere — which is the entire argument for tokens.

## Penpot, for comparison

The same get-started guide names a second design tool: Penpot, the
open-source design platform, which supports design tokens natively — no
plugin required. Penpot's implementation adheres to the DTCG Format Module
and imports token JSON directly, and for teams selecting a design tool on
open-standards grounds that native support is a genuine point in its favor.
One honest caveat belongs next to it: as of this writing, Penpot community
discussion records that its token export emits Tokens-Studio-style JSON
rather than strict current-revision DTCG output, so round-tripping tokens out
of Penpot is not yet as clean as importing them into it. For the consumption
direction this article describes — system publishes, tool subscribes — that
caveat does not bite: the design system's export is the source, and both
tools read it.

Sketch users are covered by the same plugin route: Tokens Studio also ships
for Sketch, and the same published file serves it.

## Licensing

Two licenses apply here, and they attach to different things. The token data
— the DTCG JSON file a designer points Tokens Studio at — is published under
Apache-2.0, the convention shared by major open design systems, so consuming
it in a design tool, a build pipeline, or a derived product carries
Apache-2.0's permissive terms. This article's text, as part of the
documentation wiki, is licensed CC BY 4.0 — a content license requiring
attribution, distinct from the data license. Pulling the tokens into Figma
engages the former; quoting or republishing this article engages the latter.

## Scope and limits

Stated plainly: what is demonstrated is the publication side — the DTCG
export exists, is served by the design-system site, and is the documented
designer path — and the plugin capabilities cited are taken from Tokens
Studio's own current documentation, read directly rather than assumed. This
article does not claim a measured adoption result, does not speak for Tokens
Studio's or Penpot's roadmaps, and flags rather than hides the one remaining
soft edge: third-party pricing and feature boundaries are checked as of
2026-07-10, not guaranteed forward. (The export's short-form public URL now
resolves via a permanent redirect to the server's bundle route — verified
2026-07-30 — so that earlier open question is closed.)

---

*This article is background for designers encountering the design system's
token export for the first time, ahead of the step-by-step guide to
configuring Tokens Studio against a specific instance.*
