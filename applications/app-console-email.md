---
schema: foundry-doc-v1
title: "app-console-email — communications cartridge"
slug: app-console-email
category: applications
type: app
content_type: topic
quality: complete
index_group: input-and-developer-surfaces
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: app-console-email.es.md
short_description: "app-console-email is the F3 communications cartridge for os-console, providing inbox listing, message reading, and compose-and-send via service-email."
cites: []
---

`app-console-email` is the F3 communications cartridge for [[os-console|os-console]]. It connects to [[service-email|service-email]] and provides an operator-facing interface for three communication tasks: reading an inbox, reading a message, and composing and sending a message. The cartridge is keyboard-driven throughout; no pointer interaction is required.

The cartridge implements the `Cartridge` trait defined by [[app-console-keys|app-console-keys]], occupying the F3 slot in the console's navigation strip.

## The Comm Diode model

`app-console-email` is not a general-purpose email client. Outbound messages flow through `service-email` — a service that acts as a Comm Diode between the operator's [[totebox-os|Totebox]] and external correspondents. The diode analogy reflects a design constraint: `service-email` controls the egress path and applies the tenant's communication policies before any message leaves the platform boundary.

This means the cartridge does not speak directly to an external mail server. It composes a message, submits it to `service-email`, and the service handles routing, queuing, and delivery. The cartridge receives a delivery confirmation or an error; it does not manage SMTP or IMAP sessions itself.

## Inbox view

The inbox view lists received messages in reverse chronological order. Each row displays the sender, subject, and received timestamp. The list refreshes when the cartridge is focused and on demand via keyboard shortcut.

Messages are sourced from `service-email`'s message store. The cartridge does not maintain its own local copy; all state lives in the service.

## Message reading

Selecting a message from the inbox opens the message reading view, which fetches and displays the full message body alongside the sender, subject, and timestamp already shown in the inbox row. The cartridge carries no attachment support — a message's body is plain text or an HTML fallback, with nothing to download or open separately.

Plain-text mode is available via the `--plain` flag at console startup. In plain mode, HTML-only message bodies are rendered as their plaintext fallback. Terminals without unicode support receive ASCII approximations of any unicode symbols in subject lines and sender names.

## Compose and send

The compose view provides fields for recipient, subject, and body. The interface is structured: the operator fills each field in sequence using keyboard navigation. Sending submits the composed message to `service-email` for egress processing.

Draft saving is not implemented. An abandoned compose session is discarded; no partial message persists in the service store.

## Authorization dependency

The cartridge's connection to `service-email` is brokered through the [[machine-based-auth|machine-based authorization]] client managed by [[app-console-keys|app-console-keys]]. That authorization link is chassis-wide, not per-cartridge: when it goes inactive, the chassis replaces the entire content area with a full-screen pairing prompt, and `app-console-email` — like every other cartridge — is not rendered at all until the link is restored.

## See also

- [[service-email]] — the email service that handles routing, queuing, and egress
- [[os-console]] — the os-console product overview and F-key surface
- [[os-console]] — cartridge architecture and the full F-key map
- [[app-console-keys]] — the chassis that hosts this cartridge; defines the Cartridge trait
- [[app-console-input]] — the F12 mandatory gate for inbound file ingestion
- [[machine-based-auth]] — the authorization layer the cartridge connects through
