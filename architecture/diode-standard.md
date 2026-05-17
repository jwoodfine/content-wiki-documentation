---
schema: foundry-doc-v1
title: "The Diode Standard"
slug: diode-standard
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: diode-standard.es.md
short_description: "The Diode Standard is the foundational security topology of the PointSav family — a unidirectional command flow discipline where traffic moves from authority to subject and never the reverse, structurally removing lateral movement attacks by eliminating the routing logic that would allow them."
cites: []
references:
 - id: 1
 text: "Rose, S. et al. 'Zero Trust Architecture.' NIST SP 800-207, 2020."
 url: "https://doi.org/10.6028/NIST.SP.800-207"
 - id: 2
 text: "MITRE. 'ATT&CK Tactic: Lateral Movement (TA0008).' MITRE Corporation, 2023."
 url: "https://attack.mitre.org/tactics/TA0008/"
---

In electrical engineering, a diode conducts current in one direction and blocks it in the other. The Diode Standard applies the same principle to commands across the PointSav operating system family: traffic flows from authority to subject, and never the reverse. [^1] It is the foundational security topology of the entire family — not a feature of a single operating system, but the law governing how all operating systems communicate with each other. This article covers the authority hierarchy, the three traffic categories, the structural removal of lateral movement, and the adapter that enforces the standard.

## The hierarchy

| Position | Operating system | Privilege |
|---|---|---|
| Authority | `os-console` and `os-orchestration` | Issues commands; receives telemetry |
| Subject | `os-totebox`, `os-mediakit`, `os-privategit`, `os-infrastructure`, `os-network-admin` | Executes commands; emits telemetry; never originates a command |

A Totebox cannot command a MediaKit. A MediaKit cannot reach into a Totebox. A compromised Subject cannot move laterally to another Subject because the protocol stack contains no routing logic to do so.

## The three traffic categories

| Traffic | Direction | Status |
|---|---|---|
| Downstream control | Authority → Subject | Permitted: configuration, content, commands, updates |
| Upstream telemetry | Subject → Authority | Permitted but strictly sanitised: logs, heartbeats, status |
| Upstream control | Subject → Authority | Structurally blocked: no shell access, no RPC, no admin requests |

Upstream control is not blocked by a firewall rule. It is blocked because the code to express it does not exist on the Subject. There is no `ssh` client. There is no peer-to-peer routing table. The Subject is structurally incapable of initiating an authority relationship.

## Why this matters

The category of attacks called lateral movement — where an attacker compromises one node and uses it to reach more valuable nodes — is the dominant pattern in modern breach reports. [^2] The Diode Standard removes it structurally.

| Scenario | Without the Diode | With the Diode |
|---|---|---|
| A plugin on `os-mediakit` is compromised | Attacker rides the management tunnel back to the corporate `os-totebox` | The adapter has no upstream route; the attacker is contained on the public-facing host |
| A Totebox kiosk is physically compromised | Attacker scans the local network and pivots to the MediaKit | The kiosk Totebox cannot route to other Subjects; it is a dead end |
| `os-orchestration` is compromised | Attacker holds the keys to every Totebox in the fleet | `os-orchestration` holds no Totebox keys; it requests signed capabilities per query; a full Orchestration compromise yields no Totebox decryption material |

## The adapter

The Diode is enforced by a small, hot-pluggable service called `service-pointsav-link` (the `pointsav-protocol` package). This adapter is the only code that knows how to translate authority commands into Subject-executable operations.

| Property | Behaviour |
|---|---|
| Default state | Not installed; the Subject has no concept of phoning home |
| Activated state | Hot-plugged by the operator with a single command; brings the Subject under fleet management |
| Failure mode | If the adapter crashes, the link severs cleanly; the Subject continues running standalone; the fleet management surface goes dark |
| Code path | Diode policy lives inside the adapter, not the OS kernel — the policy can be updated without touching the rest of the system |

## The Universal Standard

The Diode is not a MediaKit feature or a Totebox feature. It applies identically to every `os-*` operating system. The same `service-pointsav-link` package, with different policy bindings, sits between any pair of nodes that need to communicate. This single, uniform standard is the reason a complex fleet remains auditable: every connection looks the same and obeys the same rules.

## See also

- [[os-family-overview]] — the eight operating systems the Diode topology governs
- [[machine-based-auth]] — the machine-based authorisation system that the Diode works alongside
- [[deployment-patterns]] — the fleet deployment patterns that apply the Diode discipline
