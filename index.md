---
schema: foundry-doc-v1
title: "Welcome to Documentation Wiki"
slug: index
category: root
status: pre-build
last_edited: 2026-05-03
editor: pointsav-engineering
---

<!-- ENGINE-SPEC: project-knowledge
     This index.md serves as the definitive Main Page for the wiki.
     The layout must replicate Wikipedia's muscle memory (Portals, Featured Article, Did You Know?) 
     while maintaining a high-contrast, institutional aesthetic suitable for a 65+ demographic.
     The dual-hyperlink architecture (blue links for topics, dashed underlines for glossary) 
     must be active on this page. -->

<div style="display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 1em; border-bottom: 1px solid #a2a9b1; margin-bottom: 1em;">
  <div>
    <h1 style="border: none; margin: 0; padding: 0;">Welcome to Documentation Wiki</h1>
    <p style="margin: 0.5em 0 0 0; font-size: 1.1em;">The definitive reference for PointSav Digital Systems' sovereign infrastructure.</p>
  </div>
  <div>
    <img src="/pointsav-media-assets/logos/PointSav Logo_Earth_Logo_Small.png" alt="PointSav Logo" height="50">
  </div>
</div>

PointSav Digital Systems builds the sovereign infrastructure for 2030. We provide regulated small and mid-size businesses with permanent, portable, and verifiable data ledgers on hardware they explicitly control. This encyclopedia serves as the definitive reference for the platform's architecture, services, operating systems, and regional deployment indices. 

---

## Knowledge portals

<!-- ENGINE-SPEC: Render this section as a prominent 2-column grid. Each portal acts as a 
     macro-category gateway. Use the new {{gli|...}} syntax for hover-definitions if needed. -->

### [[architecture|Architecture & doctrine]]
The foundational laws of the PointSav system. Explores cross-cutting invariants, immutable record-keeping via WORM ledgers, the zero-execution routing discipline, and the structural separation of compute and data. 
→ **[[architecture|Enter the architecture portal]]**

### [[development-regions|Development regions (GIS indices)]]
Interactive indices of the Top 800 commercial nodes across North America and Europe. Fuses proprietary GIS data with curated macroeconomic indicators to establish Michelin-style co-location ratings.
→ **[[development-regions|Enter the regions portal]]**

### [[services|Core services]]
The autonomous functional components implementing the platform's capabilities, including cryptographic extraction, search indexing, linguistic air-locks, and {{gli|Doorman}} compute routing.
→ **[[services|Enter the services portal]]**

### [[governance|Governance & stewardship]]
The administrative models securing the ecosystem for the long term. Details the contributor model, licensing posture, and sovereign replacement initiatives.
→ **[[governance|Enter the governance portal]]**

---

## Featured article

<!-- ENGINE-SPEC: Read `featured-topic.yaml` from the repo root.
     Render as a framed, authoritative panel. Do not use promotional language.
     If the pin file is absent, render a fallback to [[compounding-substrate]]. -->

**[[compounding-substrate|The Compounding Substrate]]**

The **Compounding Substrate** is an AI-substrate architecture where the platform code is open and forkable, the deterministic data layer functions independently of any AI compute, and AI is added as an optional layer that any tenant can compose in or out. Every operational interaction generates a training signal that compounds across deployments. A curator — PointSav — periodically rolls accumulated signal into improved base models that flow back to all deployments without disrupting customer data ownership...

**[[compounding-substrate|Read the full analysis →]]**

---

## Did you know...

<!-- ENGINE-SPEC: This section replaces the standard "Recent Changes". 
     It should pull dynamic telemetry or GIS stats to show immediate, institutional scale.
     Fallback to static bullet points until the telemetry endpoint is wired. -->

*   **Sovereign infrastructure:** The platform enforces strict separation between data and compute, meaning no AI model can spontaneously execute logic over structured records (see [[zero-execution-routing]]).
*   **Regional scale:** The GIS Engine currently tracks over 3,500 active retail nodes in the United States and 400+ in Canada, categorized by our 5-tier co-location methodology.
*   **Immutable audit:** Every transaction on a PointSav appliance is cryptographically anchored to a [[worm-ledger-architecture|Write-Once, Read-Many (WORM) ledger]], ensuring compliance with institutional reporting standards.

---

## Other areas of documentation

For definitions of technical terminology (e.g., *Air-gapped*, *Hypervisor*, *Sovereign airlock*), please consult the central **[[glossary-documentation|Platform glossary]]**. Terms marked with a dashed underline throughout the encyclopedia can be hovered over for instant, inline definitions.

---

<div style="font-size: 0.85em; text-align: center; margin-top: 3em; padding-top: 1em; border-top: 1px solid #eaecf0; color: #54595d;">
  <p>Text is available under the <a href="https://creativecommons.org/licenses/by/4.0/" style="color: #0645ad;">Creative Commons Attribution 4.0 International License</a>; additional terms may apply.</p>
  <p>Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.</p>
</div>
