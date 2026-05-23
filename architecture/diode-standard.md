---
schema: foundry-doc-v1
title: "The diode standard"
slug: diode-standard
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-22
editor: pointsav-engineering
paired_with: diode-standard.es.md
short_description: "The Diode Standard is the foundational security topology of the PointSav operating-system family — a unidirectional command flow where traffic moves from authority to subject and never the reverse, removing lateral-movement attacks by eliminating the routing logic that would allow them."
cites: []
references:
 - id: 1
 text: "Rose, S. et al. 'Zero Trust Architecture.' NIST SP 800-207, 2020."
 url: "https://doi.org/10.6028/NIST.SP.800-207"
 - id: 2
 text: "MITRE. 'ATT&CK Tactic: Lateral Movement (TA0008).' MITRE Corporation, 2023."
 url: "https://attack.mitre.org/tactics/TA0008/"
---

An attacker who breaches one machine rarely wants that machine. They want the next one. Lateral movement — pivoting from a first compromised node to more valuable nodes — is the dominant pattern in modern breach reports [^2].

The Diode Standard removes the pivot. <!--claim id=diode-principle confidence=structural cites=[]-->In electrical engineering a diode conducts current one way and blocks the other; the Diode Standard applies the same rule to commands across the PointSav operating-system family — traffic flows from authority to subject, and never the reverse [^1].<!--/claim-->

<!--claim id=upstream-absent confidence=structural cites=[]-->A Subject operating system has no code to initiate an authority relationship: no shell client, no peer-to-peer routing table. Upstream control is not blocked by a firewall rule — the code to express it does not exist on the Subject.<!--/claim-->

For a regulated buyer the consequence is concrete. An entire breach category is removed by structure, and a complex fleet stays auditable because every connection obeys one uniform rule. This article covers the authority hierarchy, the three traffic categories, the structural removal of lateral movement, and the adapter that enforces the standard.

## The hierarchy

The Diode is the foundational topology of the whole operating-system family — not a feature of one operating system, but the law governing how all of them communicate.

| Position | Operating system | Privilege |
|---|---|---|
| Authority | `os-console` and `os-orchestration` | Issues commands; receives telemetry |
| Subject | `os-totebox`, `os-mediakit`, `os-privategit`, `os-infrastructure`, `os-network-admin` | Executes commands; emits telemetry; never originates a command |

<!--claim id=no-lateral-route confidence=structural cites=[]-->A Totebox cannot command a MediaKit; a MediaKit cannot reach into a Totebox. A compromised Subject cannot move laterally to another Subject, because the protocol stack contains no routing logic to do so.<!--/claim-->

## The three traffic categories

| Traffic | Direction | Status |
|---|---|---|
| Downstream control | Authority → Subject | Permitted: configuration, content, commands, updates |
| Upstream telemetry | Subject → Authority | Permitted but strictly sanitised: logs, heartbeats, status |
| Upstream control | Subject → Authority | Structurally blocked: no shell access, no RPC, no admin requests |

Upstream control is blocked because the Subject is structurally incapable of initiating an authority relationship. The absence is the control.

## Why this matters

Lateral movement — an attacker compromising one node and using it to reach more valuable nodes — is the dominant pattern in modern breach reports [^2]. The Diode Standard removes it structurally.

| Scenario | Without the Diode | With the Diode |
|---|---|---|
| A plugin on `os-mediakit` is compromised | The attacker rides the management tunnel back to the corporate `os-totebox` | The adapter has no upstream route; the attacker is contained on the public-facing host |
| A Totebox kiosk is physically compromised | The attacker scans the local network and pivots to the MediaKit | The kiosk Totebox cannot route to other Subjects; it is a dead end |
| `os-orchestration` is compromised | The attacker holds the keys to every Totebox in the fleet | `os-orchestration` holds no Totebox keys; it requests signed capabilities per query, so a full Orchestration compromise yields no Totebox decryption material |

## The adapter

<!--claim id=hot-pluggable-adapter confidence=structural cites=[]-->The Diode is enforced by a small, hot-pluggable service, `service-pointsav-link` (the `pointsav-protocol` package). It is the only code that translates authority commands into Subject-executable operations.<!--/claim-->

| Property | Behaviour |
|---|---|
| Default state | Not installed; the Subject has no concept of phoning home |
| Activated state | Hot-plugged by the operator with a single command; brings the Subject under fleet management |
| Failure mode | If the adapter crashes, the link severs cleanly; the Subject keeps running standalone; the fleet-management surface goes dark |
| Code path | Diode policy lives inside the adapter, not the OS kernel — the policy can be updated without touching the rest of the system |

## The universal standard

<!--claim id=universal-standard confidence=structural cites=[]-->The Diode is not a MediaKit feature or a Totebox feature; it applies identically to every `os-*` operating system. The same `service-pointsav-link` package, with different policy bindings, sits between any pair of nodes that communicate.<!--/claim-->

This single uniform standard is why a complex fleet stays auditable: every connection looks the same and obeys the same rules.

## See also

- [[os-family-overview]] — the eight operating systems the Diode topology governs
- [[machine-based-auth]] — the machine-based authorization system the Diode works alongside
- [[deployment-patterns]] — the fleet deployment patterns that apply the Diode discipline
