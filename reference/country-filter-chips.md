---
schema: foundry-doc-v1
type: topic
category: reference
slug: country-filter-chips
title: Country Filter Chips
paired_with: country-filter-chips.es.md
state: authoritative
audience: vendor-public
bcsc_class: current-fact
language_protocol: DESIGN-COMPONENT
authored: 2026-04-30
---

# Country Filter Chips

The Country Filter Chip component is a specialized navigation primitive designed for multi-jurisdictional geographic data sets. It enables users to execute global or country-specific data cuts through an exclusive-selection interface, simultaneously filtering map features and re-centering the viewport on target national boundaries.

## Executive Summary

Foundry map surfaces utilize Country Filter Chips to facilitate rapid geographic segmentation. By providing a horizontal radiogroup of jurisdiction-specific triggers—including a default "ALL" state—the component allows users to navigate complex global datasets with a single interaction. Each selection triggers an automated viewport transition (fly-to) to the respective country's geographic extent, ensuring the relevant data is immediately prioritized and framed.

## Usage Guidelines

### Deployment Scenarios
- **Global Intelligence Maps**: Serves as the primary filter for location-based data spanning multiple countries (e.g., US, CA, MX, ES).
- **Portfolio Dashboards**: Planned for use in customer-specific dashboards to segment assets by operating jurisdiction.
- **Regulatory Disclosure**: Intended for surfaces requiring BCSC or EU-specific jurisdictional views.

### Constraints
The component is optimized for exclusive selection (radiogroup). It should not be used for toggling individual data layers or for switching between entirely different view modes, which are handled by the Checkbox and Content Switcher components respectively.

## Technical Specifications

### Anatomy and Composition
- **Visual Identifier**: Each chip displays an ISO 3166-1 alpha-2 country code, optionally paired with a supplementary flag icon.
- **State Feedback**: Selected states are communicated through a combination of background color, border weight, and semantic ARIA attributes.
- **Container**: A horizontal row that supports overflow scrolling when the number of jurisdictional chips exceeds eight.

### Interaction Model
- **Selection Logic**: Activating a chip deselects all others. Selection triggers a data filter event and a 700ms cubic-bezier viewport animation.
- **Keyboard Navigation**: The group is accessible via Tab, with arrow-key navigation supporting focus movement between individual chips.
- **Touch Optimization**: Each chip maintains a minimum 44px hit target to comply with WCAG 2.2 AAA recommendations for touch interfaces.

## Accessibility and Compliance
The component adheres to WCAG 2.2 AA requirements for interactive controls:
- **Semantic Roles**: Utilizes `role="radiogroup"` and `role="radio"` with `aria-checked` states.
- **Accessible Names**: All icons are supplementary; the rendered ISO code provides the primary accessible name.
- **Visual Contrast**: Selected states maintain a minimum 4.5:1 contrast ratio (AA) with plans to move toward 7:1 (AAA) in future design-system iterations.

## Design Tokens (DTCG)

| Token | Value | Description |
| :--- | :--- | :--- |
| `ps.chip.height` | 36px | Standard chip height |
| `ps.chip.border-radius` | 18px | Full pill radius |
| `ps.chip.bg.selected` | brand-primary | Active selection background |
| `ps.chip.fg.selected` | text-on-brand | Active selection text color |

## Strategic Roadmap
Future enhancements are intended to include:
- **Geographic Grouping**: Research is underway to determine if continental grouping (e.g., "Americas", "Europe") provides better usability for datasets spanning more than ten countries.
- **Multi-Select Variant**: A planned variation that utilizes `role="group"` and `aria-pressed` to allow for cross-country data composition.
