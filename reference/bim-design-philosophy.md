---
schema: foundry-doc-v1
type: topic
slug: bim-design-philosophy
title: BIM Design Philosophy
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: bim-design-philosophy.es.md
---

# BIM Design Philosophy

The Building Design System serves as the AEC-specific extension of Foundry’s design substrate, analogous to the relationship between IBM Carbon and specialized industry modules. It is anchored to the IFC 4.3 entity hierarchy and prioritized for high-fidelity operational environments. The system translates Foundry’s core commitments—flat-file storage, open standards, and offline-first execution—into a professional toolset that addresses the structural weaknesses of legacy cloud-only BIM.

## Structural Differentiators

Foundry’s design philosophy is predicated on five capabilities that are structurally incompatible with multi-tenant SaaS models:

1.  **Asset-Anchored BIM:** The digital twin is a legal artifact signed with the land title, moving with the property deed rather than being tied to a vendor’s tenant model.
2.  **Offline-Capable Operations:** Full BIM functionality is maintained in basements, air-gapped facilities, and remote sites where internet access is unavailable.
3.  **Vendor-Obsolescence Survival:** By utilizing a text-based open-standard stack (IFC-SPF, BCF 3.0, IDS 1.0, COBie), data remains accessible for 50+ years, outlasting specific software vendors.
4.  **Local IoT Integration:** Sensor data is ingested via local brokers into YAML sidecars, ensuring data residency and eliminating usage-based token charges.
5.  **Legal-Financial Convergence:** The Totebox Archive unifies the building’s spatial, operational, and financial identities into a single portable artifact.

## Compositional-First Regulatory Compliance

Foundry introduces a "compositional-first" approach to building codes and jurisdictional rules. Instead of post-design validation, cities are intended to publish codes as composable design tokens (bSDD dictionaries + IDS 1.0 constraints). Designers then assemble models within pre-constrained envelopes where violations become geometrically impossible by construction.

This shift from "check-after-design" to "compliant-by-construction" represents a significant leapfrog in AEC technology (Proposed Doctrine Claim #41).

## Integration with the META-Substrate

The BIM-SEMANTIC layer sits atop project-design’s META-substrate. While project-design owns the baseline Carbon and DTCG vault standards, project-bim manages the BIM-specific extensions:
*   8 BIM token categories anchored to IFC 4.3.
*   18 specialized component recipes.
*   Uniclass 2015 as the universal classification floor.

This architecture ensures that BIM components remain consistent with the broader Foundry design language while meeting the rigorous semantic requirements of ISO-standardized building data.
