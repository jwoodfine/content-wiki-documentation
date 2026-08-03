---
title: "Diode standard"
slug: diode-standard
category: security
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "The Diode Standard is the design rule that command and data flow in one direction only, from authority to subject. Several real mechanisms follow it; no component enforces it as a named standard."
paired_with: diode-standard.es.md
---

**The Diode Standard** is this platform's design rule that command and data move in one direction
only — from an authoritative side to a subordinate side — with no return path capable of carrying
instructions. It borrows its name from the electrical component that conducts current one way and
blocks it the other, and from the "data diode" appliances used in industrial and defence networks
to let telemetry leave a protected segment while making it physically impossible for anything to
enter. Under the standard, a subject system is not merely *forbidden* from commanding its peers or
its authority — the design goal is that it holds no code capable of expressing such a command in
the first place: no shell client toward the authority, no peer-to-peer routing table, no
administrative request path.

The security argument for the rule is about lateral movement rather than confidentiality. Most
serious intrusions are not a single breach but a chain: an attacker reaches a low-value endpoint,
then uses the connection that endpoint already has back toward a management server to reach
something more valuable. A strictly one-directional link removes the second half of that chain
structurally. There is no reverse channel to abuse, so a compromised subject cannot escalate toward
the authority through the link that connects them, regardless of what credentials it holds. The
audit economics matter as much as the breach economics: in a fleet where connections may run in any
direction, reviewing the topology means reasoning about every pair of systems separately. Under a
Diode-conformant fleet, every legitimate connection has the same shape — control down, sanitized
telemetry up, nothing else — and a reviewer checks one rule everywhere.

## Where the rule is stated

The standard is a documented design principle across this platform's internal engineering
material — a user guide section, a corporate glossary entry defining it as "a universal one-way
command flow from source to endpoint," internal architecture notes, and public positioning copy
that names it among the platform's differentiating protocols. It also governs the topology of the
[[os-family-overview|operating-system family]]: an authority side (the operator console and
orchestration systems) issues commands and receives telemetry, while a subject side (the archive,
media delivery, source-control, infrastructure, and network administration systems) executes
commands and emits telemetry, never originating one.

It is important to be exact about what that means. The Diode Standard is real *as a stated design
rule*. What has not been established is that any single named component enforces it as a standard,
checks conformance to it, or refuses traffic on the grounds of violating it.

## Mechanisms that follow the rule today

Several implemented mechanisms genuinely move data in one direction. They were built for their own
purposes and each satisfies the rule in its own domain; none of them is a general-purpose diode
enforcer.

### Pull-and-wipe egress

The clearest case is the egress pair. `tool-egress-pull` — which names itself "the asymmetric
diode" in its own documentation — pulls data chunks from a relay host to local storage over SSH,
reassembles and decompresses them, and only after computing a local SHA-256 checksum to verify
fidelity sends a single authorisation back to the relay: a "WIPE" marker instructing it to delete
its copy. A daemon on the relay side consumes those markers and removes the source files. Data
therefore moves only outward-to-inward; the sole reverse signal is a delete authorisation, which
carries no payload and cannot instruct the relay to do anything else.

### Telemetry pull rather than push

The measurement pipeline described in [[data-sovereignty-telemetry]] is retrieved by scheduled pull
scripts rather than pushed from a central controller into deployments, which keeps the control
direction consistent with the rule.

### Ingestion described as a diode

The email service's harvesting component (`service-email/master-harvester-rs`) names its own
micro-batching logic "the ingress diode" directly in source comments and startup logging. Its role
is consistent with the framing: it draws messages inward into the extraction pipeline and produces
queued fragments for downstream processing, with no path by which the pipeline instructs the
mailbox it read from. This is the one place in the tree where a component adopts the vocabulary of
the standard for itself, though it does so descriptively — nothing in it checks or enforces
directionality as a rule.

### Directional code promotion

The strongest enforcement in the platform is over source code rather than runtime data. Promotion
(`bin/promote.sh`) runs in one direction only — from staging mirrors, to the canonical repository,
to local service mirrors — and the script actively refuses the reverse case: it permits only
fast-forward pushes or explicit commit-by-commit replays onto the canonical branch, blocks true
history divergence, blocks mass deletions above a threshold, blocks patterns that would silently
revert canonical content, and enforces a strict path allowlist against unlisted top-level
directories. This is a real, hardened, one-directional flow, and it is the platform's best evidence
that the rule is operationally taken seriously — though it governs a build pipeline rather than the
runtime command path the standard describes.

## What was expected and is not present

Earlier descriptions of this standard named a specific enforcing component — a small,
hot-pluggable link service, absent by default and installable by the operator, that would be the
only code translating authority commands into subject-executable operations. Direct search of the
canonical source tree confirms that no package of that name, under either of the two names
previously used, exists anywhere. A corpus-wide search for both strings, and for "Diode" or
"DiodeStandard" in Rust source, returns nothing outside documentation about this article's own
subject.

The one package with a similar-sounding name is a seven-line placeholder whose single function
returns a scaffold-verification string and whose dependency list is empty. It contains no
directional logic of any kind.

**What this means is genuinely unresolved rather than resolved-negative.** The adapter may be a
planned component not yet built, or a design that was renamed or superseded — prior internal
planning material lists it with a status of "conceptual," consistent with a design that was scoped
and named but not built. The question has been flagged for confirmation by the owning engineering
group, and this article does not guess at an answer. Until that answer lands, the accurate
statement is: the Diode Standard is a published design rule for the platform's topology, and no
code currently in the monorepo can be identified as implementing it as a general enforcement
mechanism.

## Enforcement by absence versus enforcement by mechanism

The stronger claim sometimes made for this design — that a subject system is *structurally
incapable* of issuing commands back to its authority because no client capability is compiled into
it — is a different and much more demanding claim than one-directional data movement.

That claim is not verifiable from source alone. What is observable is the absence of
reverse-command code in the relevant daemons, which is consistent with the design but is weaker
evidence than a positive mechanism would be. Absence of a capability in today's build is a property
that any future commit can silently remove; a mechanism that refuses reverse traffic is a property
that survives. A reader assessing this platform's isolation posture should treat the directional
guarantee as an architectural intention supported by the current shape of the code, not as a
checked invariant.

## What this is not

**This is not a hardware data diode.** Nothing described here involves an optical isolator, a
one-way physical link, or any device that makes reverse transmission electrically impossible. The
directionality is a property of software design and process, and it is defeated by a
misconfiguration in a way that a physical diode is not.

**No component enforces the Diode Standard by name.** No conformance check, policy file, or runtime
gate refers to it. The mechanisms listed above follow the rule; none of them polices it.

**The previously named enforcing adapter does not exist.** Neither of the package names used in
earlier descriptions is present anywhere in canonical source — a confirmed absence, not merely an
unsearched gap — and whether it was abandoned, renamed, or deferred remains an open question this
article does not resolve.

**The code-promotion controls are not the runtime diode.** They are the platform's most complete
directional enforcement, but they govern how source code reaches production, not how commands flow
between a running authority and a running subject. Conflating the two overstates the runtime
guarantee.

**One-directional flow is not confidentiality, and it is not an authentication scheme.** The rule
limits what an attacker can do after reaching a subject system; it says nothing about whether the
data crossing the link is encrypted, and it governs *direction* of control, not *identity* of the
parties. Identity and access are the province of [[machine-based-auth|machine-based
authorization]], which decides whether two machines may form a connection at all — the Diode then
constrains what may flow across a connection that authorization has permitted.

## See also

- [[os-family-overview]]
- [[machine-based-auth]]
- [[capability-based-security]]
- [[sel4-capability-topology]]
- [[five-stage-supply-chain]] — the promotion path whose directionality is enforced in script
- [[data-sovereignty-telemetry]] — the pull-based measurement pipeline
- [[reverse-flow-substrate]] — the wider treatment of directional data movement across the platform
