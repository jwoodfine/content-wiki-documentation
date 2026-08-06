---
schema: foundry-doc-v1
title: "Personnel and permissions"
slug: personnel-permissions
category: security
index_group: identity-and-permissions
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "Four permission tiers, P1 through P4, are implemented as a typed enumeration and served over an HTTP endpoint that reads a workspace configuration file. That file currently declares no contributors, so the endpoint resolves nothing for any real user."
paired_with: personnel-permissions.es.md
---

**A permission tier** is a named level of authority assigned to a contributor, determining which
archives they may work in and which privileged operations they may perform. This platform defines
four — P1 through P4 — implemented as a typed enumeration in the orchestration command component,
served over an HTTP endpoint, and derived from a workspace configuration file rather than from a
user database.

The design choice worth noticing is what the tier is *attached to*. There is no accounts table, no
per-service role assignment, and no group membership. A contributor's authority is meant to be a
property of a configuration file describing which archives they are paired with, and the tier is
derived from that pairing — permission as a consequence of pairing rather than a separate grant.
That design is real code today; whether it currently governs anyone is a separate question this
article answers precisely below.

## The four tiers

The enumeration is typed rather than a free string, and its variants carry documentation that
states each tier's scope directly:

- **P1 — System Administrator.** Full workspace access.
- **P2 — Package Manager.** Specific archives, plus authority to run the canonical promotion step.
- **P3 — User.** Specific archives only; no command-layer pairing.
- **P4 — Interface.** Read-only API surface only.

The ordering is a genuine hierarchy of blast radius rather than seniority. The meaningful boundary
sits between P2 and P3: P2 can move work into the canonical repository, which is the point at which
a change becomes externally visible and irreversible in practice. P3 can commit freely within its
own archives without that reach. P4 cannot write at all.

## How a tier is resolved

The resolution path is short and entirely file-driven.

A personnel module reads a workspace configuration file — the workspace-root `pairings.yaml` —
looking for a top-level `contributors` key. Each entry there would supply an operating-system
username, a tier string, and a list of paired archives. The module maps that raw shape into an
internal three-field record and parses the tier string into the typed enumeration; an unrecognised
or missing tier falls back to P3, the more restrictive of the two archive-scoped tiers.

A single route, `GET /v1/personnel/{user}`, returns the resulting record as JSON or a not-found
error. That endpoint is the platform's intended answer to "what is this contributor allowed to do."

### The record is three fields

The record carries an operating-system username, a tier, and the set of paired archives. That is
all. It does **not** carry a display name, a role string, or an SSH public key. Key material is
managed separately in the workspace identity store, where each identity has its own directory and
signing key with restrictive permissions. Describing a single unified personnel record holding
name, role, key, and tier together would misstate the data model: the identity store and the tier
record are separate systems joined only by convention on the username.

## The configuration file declares no contributors today

The `contributors` key is optional in the parser, so a file lacking it entirely still loads without
error and yields an empty contributor set. The real workspace `pairings.yaml` was read directly for
this article: it contains a `pairings:` list of archive-topology entries (cluster name, module ID,
branch, self-service level) and carries **no `contributors:` key anywhere in it**.

The consequence is exact and worth stating without euphemism: the personnel endpoint would return
not-found for every real user today. No contributor currently holds a resolved tier through this
path. The enumeration, the parser, the endpoint, and its fallback behaviour are all real, built, and
independently verified against canonical source — but the data that would give any of it a
practical effect for a real operator has not been populated into the file it reads. This is a case
of code that is built and correct sitting in front of data that is unpopulated, not a case of a
fictitious feature — a distinction that matters for anyone assessing this platform's access-control
posture, because the honest description is neither "not implemented" nor "fully governs access
today."

One historical caution belongs alongside this, because this article's own verification record has
been on both sides of it. An earlier review of this subject concluded the P1–P4 model described a
system that did not exist at all — a conclusion that rested on a search scoped to one component and
one configuration file. A broader search located the real implementation described above, and that
earlier finding was retracted. The standing lesson is procedural: a search scoped to one component
is not sufficient evidence that something does not exist anywhere in the monorepo, and the same
caution applies to the finding in this section — the file was read directly, in full, for this
draft, rather than inferred from its absence in a narrower search.

## Why a configuration file rather than a database

The choice to derive authority from a checked-in configuration file rather than from a user table
has consequences in both directions, and they are worth naming.

In its favour: the file is version-controlled, so a change of authority is a commit with an author,
a timestamp, and a signature, reviewable in history like any other change. There is no separate
administrative interface to secure, no session to hijack, and no live write path by which a tier
could be escalated at runtime. The same file also carries the archive topology and the per-archive
self-service grants, so the description of who may work where and the description of what each
archive may do sit in one auditable place.

Against it: the file is the entire control. Anyone able to commit a change to it, and to get that
change onto the machine serving the endpoint, changes the answer. There is no second factor and no
approval step specific to authority changes — the protection is the same commit and promotion
gating that protects any other file, described in [[five-stage-supply-chain]]. The parser's
fallback behaviour is chosen with that in mind: an unrecognised or absent tier resolves to P3, so a
malformed entry grants less rather than more.

## What actually governs access today

Since the tier endpoint has no data behind it, it is worth being explicit about what does gate
contributor authority in practice, because the answer is not this component.

Authority is enforced by the mechanisms described in [[five-stage-supply-chain]] and
[[pre-commit-defense-in-depth]]: possession of the canonical remote's access key, which only a
privileged session holds; a scope check inside the promotion script confirming the session is
entitled to promote; a self-service permission recorded per archive in the same configuration file,
which determines whether an archive may push its own branch to the staging mirrors; and a
commit-message check restricting the author identity. These are real, active controls. The tier
model is the declarative description of the same intent, currently ahead of its data.

## What this is not

**No contributor currently has a tier assigned through this path.** The configuration file declares
no contributors, so the endpoint resolves nothing. The implementation exists; the population does
not.

**A personnel record is not an identity record.** It holds a username, a tier, and paired archives.
Names, roles, and keys live elsewhere, and no code joins them into a single object.

**Tiers are not enforced by the tier component.** The enumeration and endpoint describe authority;
they do not gate any operation. Refusal happens in the promotion script, in the commit hooks, and
in who holds which access key.

**This is not the pairing system described in [[machine-based-auth]].** That component binds a
device key to a user record and carries an unconstrained role string with a hardcoded default. It
is a different component, a different data model, and not a P1–P4 tier. A separate three-value
pairing role — user, administrator, interface — also exists in the orchestration component and is
likewise not this enumeration.

**A tier is not an account.** There is no login, no session, and no credential associated with it.
It is a declaration read from a file, and its integrity depends entirely on the integrity of that
file and of the process that edits it.

## See also

- [[totebox-session]] — the four-tier permission model referenced above
- [[contributor-model]] — the contribution arrangement the tiers describe
- [[pairing-as-permission]] — the principle that pairing, not a role grant, confers authority
- [[machine-based-auth]] — device-level authorisation, a separate mechanism
- [[five-stage-supply-chain]] — where promotion authority is actually enforced
- [[identity-ledger-schema-design]]
- [[scale-user-tiers]] — how tier assignment is intended to scale with contributor count
