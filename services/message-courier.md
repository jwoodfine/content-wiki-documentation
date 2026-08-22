---
schema: foundry-doc-v1
title: "Message courier service"
slug: message-courier
category: services
type: topic
content_type: topic
quality: stub
index_group: specialist-and-domain-services
short_description: "A deliberately thin engine that dynamically loads a customer's private adapter script and hands it execution control — keeping every operational detail of a client's web-automation logic out of the open-source codebase entirely."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
paired_with: message-courier.es.md
---

`service-message-courier` is intentionally small. Its entire job is to load a piece of code the engine itself has never seen — a private adapter — and hand it control. Everything a specific web-automation task actually does lives in that adapter, not in the engine.

## What the engine does

The command-line entry point takes two arguments: which adapter to run, and an operational limit (defaulting to 10) to cap how much work one execution cycle does. It then:

1. Dynamically imports the named adapter from `private-adapters/<name>.py`.
2. Calls the adapter's `execute_payload(limit=...)` function.
3. Reports success or failure — the adapter's own exception, if it raises one, is caught and logged.

That's the whole engine. It has no built-in knowledge of any ledger, any portal, or any browser-automation library — those are choices the adapter makes, entirely outside this codebase.

## Why the adapter lives outside version control

`private-adapters/` is excluded from Git by the repository's own `.gitignore`, alongside local credentials and any local execution-tracking database. A customer's operational logic — which portal to reach, what to do there, and how to authenticate — never enters the public monorepo's history. The engine fails loudly and exits if the requested adapter file isn't present, rather than silently doing nothing.

This keeps the open-source engine genuinely tenant-agnostic: the same 56-line script runs unmodified for any deployment, and everything specific to one customer's operation is an external file the engine loads at runtime, never a fork of the engine itself.

## See also

- [[service-people]] — a plausible source of records an adapter might act on, though the engine itself has no direct connection to it
