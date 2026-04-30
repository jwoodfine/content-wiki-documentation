---
schema: foundry-doc-v1
title: "service-people: Personnel Ledger"
slug: topic-service-people
category: services
type: topic
quality: complete
short_description: "service-people is the Ring 1 boundary-ingest service that maintains a deterministic flat-file personnel ledger, storing unique contact identifiers, communication states, and contact histories as a portable, schema-stable JSON flat-file database."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-service-people.es.md
---

# service-people: Personnel Ledger

> service-people is the Ring 1 boundary-ingest service that maintains a deterministic flat-file personnel ledger, storing unique contact identifiers, communication states, and contact histories as a portable, schema-stable JSON flat-file database.

**service-people** is a Ring 1 boundary-ingest service in the PointSav three-ring architecture. It acts as the centralized contact database for the enterprise, storing unique identifiers, contact states, and communication ledgers for every known contact. The service uses a flat-file JSON state machine rather than a centralized database cluster, which keeps the contact data portable across infrastructure changes and makes the ledger natively compatible with future local intelligence model training without schema fracturing.

## Overview

Every communication that enters through Ring 1 carries sender identity. service-people receives sender-identity records from service-extraction and maintains a persistent, queryable ledger of known contacts. Because the ledger is a flat-file JSON structure rather than a relational or document database, it can be copied, audited, and inspected with standard filesystem tools and does not require a running database process to remain readable.

## Ring and Role

service-people occupies **Ring 1 — Boundary Ingest** in the three-ring architecture. Ring 1 services are per-tenant and implement an MCP (Model Context Protocol) server interface. service-people's role within Ring 1 is to maintain identity state: as communications arrive through service-email and other Ring 1 channels, service-people receives the parsed sender records from service-extraction and updates the contact ledger accordingly. Downstream Ring 2 services query service-people to enrich content with known contact context.

## Architecture

The service enforces the DS-ADR-02 flat-file standard, which rejects centralized database clusters in favour of a verifiable JSON flat-file state machine. The design choices that follow from this standard:

- **Portability.** The entire ledger is a directory of JSON files that can be moved to any system with a filesystem. No database migration is required.
- **Schema stability.** JSON flat files do not require schema migrations when fields are added. Existing records remain valid as the schema evolves.
- **Auditability.** The ledger can be inspected, diffed, and versioned with standard tools.
- **Model compatibility.** The flat-file format allows the ledger to feed local intelligence models directly, without an ETL step to extract from a database schema.

The service operates as a CLI tool. It exposes strictly defined query and update operations, processes sub-process calls from authorized execution adapters, and executes read and write operations against the JSON ledger files.

## Configuration

| Parameter | Purpose |
|---|---|
| Ledger path | Filesystem path for the JSON contact database |
| Update adapter | Identity of the authorized process permitted to write contact records |
| Query interface | CLI flags for read operations against the ledger |

## See Also

- [[topic-service-email]]
- [[topic-service-extraction]]
- [[topic-service-search]]
- [[topic-trajectory-substrate]]

## References

- DOCTRINE.md §XI — Ring 1 boundary-ingest architecture and MCP server interface
- `pointsav-monorepo/service-people/` — implementation crate
- DS-ADR-02 — flat-file state machine standard (files over databases)
