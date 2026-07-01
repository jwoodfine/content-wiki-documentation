---
schema: foundry-doc-v1
title: "User Interface Design"
slug: user-interface-design
category: reference
type: topic
content_type: topic
quality: complete
status: active
audience: customer-woodfine
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-06-30
editor: woodfine-editorial
short_description: "The discipline of designing interfaces between humans and machines or software — concerned primarily with maximizing usability and user experience through information architecture, visual presentation, and interaction flow — encompassing graphical, voice, and gesture-based interfaces, governed by the ISO 9241 standard's dialogue principles and presentation attributes."
paired_with: user-interface-design.es.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - d0b2cb64c72cd131b0df59af533bb8518674d08582dfc19a6b4df94231036804
thesis_alignment: "User interface design is the discipline that governs how users interact with applications; understanding its principles and standards is prerequisite to reasoning about console, workplace, and public-facing application surfaces."
keynote: false
---

User interface design, also called user interface engineering, is the design of interfaces for machines and software applications with the principal goal of maximizing usability and user experience. In the context of computer software, user interface design focuses on information architecture — the organization and structure of information presented to the user — and the construction of interfaces that communicate clearly and enable users to accomplish tasks with appropriate efficiency and minimal frustration.

User interface design is involved in a wide range of projects, from computer systems and aircraft cockpits to consumer electronics and industrial control panels. In all contexts, the goal is to facilitate the completion of the task at hand without drawing unnecessary attention to the interface itself. Effective UI design combines graphic design, typography, and information architecture in service of usability; it balances technical functionality with the visual and interactive elements that make software accessible and comprehensible to its intended users.

## Relationship to user experience design

User interface design is often discussed alongside user experience design, but the two disciplines are distinct. The distinction was articulated by Don Norman and Jakob Nielsen: UI design refers to the surface and overall look of a design — the visual and interactive elements a user encounters when using a product. UX design refers to the entire process of creating the user experience — the full range of factors that affect how a user perceives and interacts with a product, including but not limited to the visual interface. UI design is one component of UX design; UX design encompasses UI design plus user research, information architecture, content strategy, and post-deployment analysis.

## Types of user interface

Three primary interface types are in widespread use in contemporary computing:

**Graphical user interfaces (GUIs)** — desktop and web applications presented through visual metaphors: windows, icons, menus, and pointers. The GUI paradigm, developed at Xerox PARC and commercialized by Apple and Microsoft, is the dominant interface model for personal computing and enterprise software.

**Voice interfaces** — interfaces controlled through speech, including intelligent personal assistants (Siri, Alexa, Google Assistant) and voice-controlled applications. Voice interfaces face unique design challenges: without a visual display, the interface must communicate status, options, and errors through audio alone.

**Gesture-based interfaces** — interfaces controlled through physical motion, including touchscreen interfaces, touchpads, and the three-dimensional gesture interfaces used in virtual reality, augmented reality, and interactive gaming environments.

## Design process

A systematic UI design process follows several phases:

**Functionality requirements gathering** — establishing what the interface must enable the user to do, informed by user research and business requirements analysis.

**User and task analysis** — understanding who the users are, what tasks they need to perform, what contexts they work in, and what constraints (technical ability, available time, hardware) they face.

**Information architecture** — organizing the structure and hierarchy of information to support user goals. Information architecture determines the navigation model, the grouping of related functions, and the labelling of interface elements.

**Prototyping** — creating low-fidelity wireframes and interactive prototypes that represent the interface structure without the visual design detail. Prototypes are tested with users before significant development investment is made.

**Usability inspection** — structured expert review of the interface against established criteria. Common inspection methods include cognitive walkthrough (following the user's thought process step by step), heuristic evaluation (assessing the interface against a set of established usability principles), and pluralistic walkthrough (a structured group review involving developers, users, and usability specialists together).

**Usability testing** — observation of real users attempting to complete defined tasks with the interface. The think-aloud protocol, in which participants narrate their thoughts while using the interface, is the most widely used method.

**GUI design** — applying visual design to the interface structure, establishing the visual hierarchy, colour palette, typography, and iconography that constitute the interface's look and feel.

## ISO 9241 standards

ISO 9241, the international standard for ergonomics of human-system interaction, provides the principal international framework for UI design requirements.

**Seven dialogue principles (ISO 9241 Part 10/110)** address the dynamic qualities of an interface:

1. **Suitability for the task** — the interface supports the user in completing the task without imposing unnecessary burden.
2. **Self-descriptiveness** — the interface provides sufficient feedback and explanatory cues that users can understand their current state and available options without external documentation.
3. **Controllability** — users can control the pace and sequence of interaction.
4. **Conformity with user expectations** — the interface behaves consistently with what users expect based on their prior knowledge and the cues provided by the interface.
5. **Error tolerance** — despite erroneous inputs or actions, the interface allows the user to recover with minimal corrective effort.
6. **Suitability for individualization** — the interface can be adapted to the skills, abilities, and preferences of individual users.
7. **Suitability for learning** — the interface supports users in learning how to use it.

**Usability (ISO 9241 Part 11)** defines usability as a product of three components: effectiveness (users can achieve their goals), efficiency (users can achieve their goals with appropriate expenditure of resources), and satisfaction (users find the interaction acceptable).

**Seven presentation attributes (ISO 9241 Part 12)** address the static visual qualities of an interface:

1. **Clarity** — information is distinguishable and legible.
2. **Discriminability** — displayed information can be differentiated from other information.
3. **Conciseness** — users are not overloaded with extraneous information.
4. **Consistency** — the same design language is applied throughout.
5. **Detectability** — the user's attention is directed toward required information.
6. **Legibility** — characters are easy to read.
7. **Comprehensibility** — the meaning of displayed information is clear and unambiguous.

**User guidance (ISO 9241 Part 13)** addresses five means by which an interface guides users: prompts, feedback, status information, error management, and online help.

---

*cites: [[user-experience-design]], [[application-programming-interface]]*
