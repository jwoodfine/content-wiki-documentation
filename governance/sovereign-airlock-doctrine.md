---
schema: foundry-doc-v1
type: topic
slug: sovereign-airlock-doctrine
title: The Sovereign Airlock Doctrine
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: sovereign-airlock-doctrine.es.md
---

# The Sovereign Airlock Doctrine

The Sovereign Airlock Doctrine establishes the mandatory security and identity protocols for all data transmission and code deployment within the Foundry ecosystem. By enforcing strict isolation between Vendor (PointSav) and Customer (Woodfine) identities, Foundry guarantees absolute operational integrity and sovereign control over digital assets.

## 1. Sovereign Asset Isolation

Foundry’s infrastructure is organized into four structurally isolated silos, each corresponding to a specific identity and organizational role:

*   **`factory-pointsav/`**: The Vendor Source. Contains the primary codebase and infrastructure blueprints owned by PointSav AG.
*   **`fleet-woodfine/`**: The Customer Operations. Contains the proprietary operational data and fleet configurations for Woodfine Management Corp.
*   **`stage-pwoodfine/`**: Engineering Airlock. The staging environment for the engineering identity.
*   **`stage-jwoodfine/`**: Operations Airlock. The staging environment for the operations identity.

## 2. Deterministic Staging and Verification

Direct modification of data within the `stage-*` airlocks is strictly prohibited. Information flow must follow a deterministic path:

1.  **Development:** Edits occur exclusively within the primary `factory-` or `fleet-` silos.
2.  **Synchronization:** Payloads are synchronized to the Airlock via `rsync`, deliberately stripping `.git` metadata to ensure a clean state transfer.
3.  **Verification:** Files are audited for correctness within the Airlock environment.
4.  **Transmission:** Data is pushed to staging identities using specific, isolated SSH keys.
5.  **Finalization:** A final merge is executed from staging to the Organization repositories using authoritative Administrator keys.

## 3. Cryptographic Identity Isolation

Operational security is maintained through a mapping of specific SSH keys to organizational silos:

| Silo | Identity | SSH Key |
| :--- | :--- | :--- |
| **PointSav Factory** | `ps-administrator` | `id_ps-administrator` |
| **Woodfine Fleet** | `mcorp-administrator` | `id_mcorp-administrator` |
| **Staging (pwoodfine)** | `pwoodfine` | `id_pwoodfine` |
| **Staging (jwoodfine)** | `jwoodfine` | `id_jwoodfine` |

## 4. Immutable Registry Operations

The fundamental physics of 2030 hyperscaler infrastructure dictate the deployment of infrastructure (GCP/On-Prem), network admin routes, and per-tenant Totebox clusters (Corporate, Personnel, Real Property).

This "{{gli|Sovereign Airlock}}" ensures that no single point of failure or identity compromise can bridge the gap between Vendor infrastructure and Customer data.
