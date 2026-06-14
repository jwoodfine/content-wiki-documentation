---
schema: foundry-doc-v1
title: "service-pointsav-link"
slug: service-pointsav-link
short_description: "service-pointsav-link is the hot-pluggable adapter that connects an os-* Subject node to a PointSav fleet, with a default state of not installed and a clean-severance failure mode."
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
language: en
paired_with: service-pointsav-link.es.md
last_edited: 2026-05-30
editor: editorial
---

`service-pointsav-link` is the hot-pluggable adapter that connects an `os-*` Subject node to a PointSav fleet. It is the sole code responsible for translating authority commands — issued by `os-network-admin` and delivered via the [[ppn-command-protocol|PPN Command Protocol]] — into Subject-executable operations. The adapter ships as the `pointsav-protocol` package. Its most important property is its default state: it is not installed. A Subject with no `service-pointsav-link` has no concept of phoning home, receiving commands, or participating in fleet management.

## The four properties

| Property | Behaviour |
|---|---|
| Default state | Not installed; the Subject has no concept of phoning home |
| Activated state | Hot-plugged by the operator with a single command; brings the Subject under fleet management |
| Failure mode | If the adapter crashes, the link severs cleanly; the Subject continues running standalone; the fleet management surface goes dark |
| Code path | Diode policy lives inside the adapter, not the OS kernel — the policy can be updated without touching the rest of the system |

## Default state: no phone-home capability

A freshly booted `os-infrastructure` node does not have `service-pointsav-link` installed. This is not a configuration choice — it is an architectural invariant. The Subject OS contains no code that would allow it to initiate contact with any authority. There is no `ssh` client, no peer-to-peer routing table, and no RPC initiator. The Subject is structurally incapable of phoning home.

This property holds across the entire `os-*` family. Every Subject — `os-totebox`, `os-mediakit`, `os-privategit`, `os-infrastructure`, and `os-network-admin` when acting as a Subject — begins in a state where fleet management is absent. Bringing a node under management is always an explicit operator action, never an automatic one.

## Activation: hot-plugging the adapter

An operator activates `service-pointsav-link` on a Subject with a single command issued from `os-network-admin`. The activation sequence installs the `pointsav-protocol` package, registers the node's fiduciary keypair with the fleet's pairing registry as a Subject entry, and opens the adapter's single inbound command channel.

After activation, the Subject becomes addressable by the fleet's command broadcast. The adapter's inbound channel listens on the PPN mesh and accepts only packets whose operation code is within the permitted set defined by the fleet's [[diode-standard|Diode Standard]] policy. All other traffic is discarded at the adapter boundary.

## Failure mode: clean severance

If `service-pointsav-link` crashes or is deliberately uninstalled, the Subject does not fail. It continues running its workloads — serving content, executing computations, maintaining its local state — as if fleet management had never been present. The fleet management surface goes dark: `os-network-admin` loses visibility of the Subject and cannot issue commands to it. But the Subject's own services are unaffected.

This failure mode is by design. A Subject that depends on the adapter for normal operation would be permanently coupled to the control plane — any control-plane outage would cascade to the Subject's workloads. By decoupling Subject operation from adapter presence, `service-pointsav-link` ensures that a control-plane failure is an observability loss, not a service outage.

## Policy in the adapter, not the kernel

The [[diode-standard|Diode Standard]] policy — which command flows are permitted, what operations are allowed from which authorities, what telemetry is emitted — lives inside `service-pointsav-link`, not in the Subject OS kernel. This separation has a practical consequence: updating fleet policy requires updating the adapter, not rebuilding or rebooting the operating system.

A Subject OS release and a Diode policy update are independent deployments. An operator can tighten or loosen fleet policy by pushing a new `pointsav-protocol` package version to active Subjects without touching any kernel code.

## The Universal Standard

`service-pointsav-link` is not a feature of a specific operating system. The same `pointsav-protocol` package, with different policy bindings, is the adapter between any pair of PointSav OS instances that need to communicate. An `os-totebox` Subject connected to an `os-console` Authority uses the same adapter code path as an `os-infrastructure` Subject connected to `os-network-admin`.

This uniform standard is what makes a complex fleet auditable. Every connection looks the same at the protocol layer. An auditor examining any pair of connected nodes sees the same adapter shape — the same default-off behaviour, the same activation sequence, the same clean-severance guarantee.

## See also

- [[diode-standard]] — the authority hierarchy and traffic rules the adapter enforces
- [[os-network-admin]] — the Authority that activates and commands Subjects via the adapter
- [[infrastructure-os]] — an os-infrastructure Subject that uses this adapter to join a fleet
- [[ppn-command-protocol]] — the 16-byte binary wire format the adapter receives
- [[machine-based-auth]] — the fiduciary keypairs that authenticate the adapter's command channel
