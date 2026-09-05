---
schema: foundry-doc-v1
type: topic
content_type: topic
title: "PointSav encyclopedia — glossary and lexicon"
slug: glossary-documentation
short_description: "A canonical A-to-Z lexicon bridging standard industry terminology with PointSav platform concepts, with authoritative definitions across technical and financial domains."
category: reference
index_group: platform-orientation
status: complete
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
csv_source: glossary-documentation.csv
---



This lexicon provides canonical definitions for PointSav platform terms, bridging standard industry vocabulary with the platform's architectural concepts. Each entry defines a term as used in platform documentation, with disambiguation notes and cross-references where relevant. For the [[language-protocol-substrate|language protocol]] that governs which terms are canonical across all three wikis, and for [[editorial-language-registers|register rules]] that govern how terms are translated between audiences, see those articles.

<div class="wiki-toc" style="padding: 10px; background: #f9f9f9; border: 1px solid #ccc; text-align: center; font-weight: bold; margin-bottom: 2em;">
 <a href="#h-a">A</a> | <a href="#h-b">B</a> | <a href="#h-c">C</a> | <a href="#h-d">D</a> | <a href="#h-e">E</a> | <a href="#h-f">F</a> | <a href="#h-g">G</a> | <a href="#h-h">H</a> | <a href="#h-i">I</a> | <a href="#h-j">J</a> | <a href="#h-k">K</a> | <a href="#h-l">L</a> | <a href="#h-m">M</a> | <a href="#h-n">N</a> | <a href="#h-o">O</a> | <a href="#h-p">P</a> | Q | <a href="#h-r">R</a> | <a href="#h-s">S</a> | <a href="#h-t">T</a> | <a href="#h-u">U</a> | <a href="#h-v">V</a> | <a href="#h-w">W</a> | X | Y | <a href="#h-z">Z</a>
</div>

---

## A
<hr>

### Administration Panel or System Administrator or Control Panel or System Preferences
In PointSav, system administration is performed through the os-console command ledger and MBA-authenticated web interfaces; no single-point administration panel exists — every privileged action is a signed, auditable transaction.

### AEC Community
*Comunidad AEC*

Architecture, Engineering, and Construction community, a key target audience for PointSav's digital twin and building management technologies.

### Artificial Intelligence or AI
*Inteligencia Artificial (IA)*

The theory and development of computer systems able to perform tasks that normally require human intelligence, such as visual perception, speech recognition, decision-making, and translation between languages.

### Audience Data
Audience data describes the characteristics and preferences of a communication's intended recipients; in PointSav, it is derived from service-people identity records and service-content gravity scores, never from external data brokers.


## B
<hr>

### Blockchain
*Cadena de Bloques*

A system in which a record of transactions made in bitcoin or another cryptocurrency are maintained across several computers that are linked in a peer-to-peer network.

### Book-Entry
*Anotación en Cuenta*

Electronic registration.

### Building Connectivity
*Conectividad del Edificio*

Future-focused tech integration.

### Business Administration
*Administración de Empresas*

The process of managing a business or non-profit organization, so that it remains stable and continues to grow. It includes all aspects of overseeing and supervising business operations.


## C
<hr>

### Cascading Style Sheet or CSS
*Hojas de Estilo en Cascada*

A style sheet language used for describing the presentation of a document written in a markup language such as HTML. CSS is a cornerstone technology of the World Wide Web, alongside HTML and JavaScript.

### CCTV Data Collection
CCTV data collection refers to the ingestion of video surveillance feeds; in a PointSav deployment, such streams enter through the os-totebox secure ingestion boundary under the [[six-tier-sovereignty-matrix|six-tier sovereignty matrix]] and are never routed through the public internet.

### Cloud Computing
*Computación en la Nube*

The delivery of computing services—including servers, storage, databases, networking, software, analytics, and intelligence—over the Internet ("the cloud") to offer faster innovation, flexible resources, and economies of scale.

> **2030 Platform Context:** PointSav's planned architecture is intended to eliminate vendor lock-in and the structural dependency on hyperscaler infrastructure sometimes described as Technofeudalism.

### Console OS
*SO de Consola*

A lightweight, terminal-based operating system for managing and interacting with PointSav services and infrastructure.

- **Console OS – F*Keys**
### Console OS – Systems Administrator
The ConsoleOS systems administrator is the Tier A operator who manages network policy, package signing, and identity provisioning on the os-console layer, working exclusively through the F12-gated command terminal.

### Container
*Contenedor*

A standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. A Docker container image is a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.

### Content Management System (CMS)
A CMS manages creation and publication of digital content; in PointSav, this function is performed by the combination of service-content (gravity engine) and app-mediakit-knowledge (wiki renderer), eliminating a traditional CMS dependency.


## D
<hr>

### Data Entry
Data entry is the manual input of structured information into a system; in PointSav, all data writes by AI components are prohibited — only deterministic, human-verified writes reach the knowledge graph per [[adr-07-zero-ai-in-ring-1|SYS-ADR-07]].

### Data Migration
Data migration is the transfer of data between storage systems or formats; in PointSav, migrations are handled by service-content's deterministic ingestion pipeline and subject to the [[worm-ledger-design|worm-ledger-design]] append-only guarantee.

### Decentralized Network
A decentralized network distributes functions and data across multiple nodes without a single controlling authority; PointSav implements this as a [[sovereign-mesh|sovereign mesh]] topology with deterministic routing and cryptographic anchoring in os-infrastructure.

### Design System
A design system is a collection of reusable components, tokens, and documented patterns that standardize a product's visual and interactive language; PointSav's implementation is pointsav-design-system, a DTCG-format vault delivered as a Git repository.

### Design System Components
Design system components are the individual reusable UI building blocks — buttons, navigation bars, form inputs — documented in pointsav-design-system/components/ with HTML+CSS+ARIA recipes and token references.

### DevOps
*DevOps*

A set of practices that combines software development (Dev) and IT operations (Ops). It aims to shorten the systems development life cycle and provide continuous delivery with high software quality. DevOps is complementary with Agile software development; several DevOps aspects came from Agile methodology.

### Digital Transformation
*Transformación Digital*

The process of using digital technologies to create new — or modify existing — business processes, culture, and customer experiences to meet changing business and market requirements.

### Digital Twin
*Gemelo Digital*

A virtual model designed to accurately reflect a physical object. In the context of PointSav, it refers to a digital replica of a building or other physical asset.

### Distributed Network
A distributed network spreads computation and storage across many nodes, each capable of independent operation; PointSav's fleet implements this through [[os-orchestration|os-orchestration]] coordinating multiple ToteboxOS archives.

### Docker
*Docker*

A set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers. Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels.


## E
<hr>


## F
<hr>

### File System
A file system organizes and stores files on a storage medium; in PointSav, the file system is managed by os-totebox under WORM-ledger constraints, with os-mediakit providing the public-facing document store.

### First-party Data
First-party data is information collected directly from users by the organization that will use it; in PointSav, it enters through service-content's authenticated ingestion endpoints and is stored in the ToteboxOS archive.


## G
<hr>

### GitHub
*GitHub*

A provider of Internet hosting for software development and version control using Git. It offers the distributed version control and source code management (SCM) functionality of Git, plus its own features.


## H
<hr>

### HTML
*HTML*

HyperText Markup Language, a standardized system for tagging text files to achieve font, color, graphic, and hyperlink effects on World Wide Web pages.


## I
<hr>

### Information Technology
*Information Technology*

Required for reliable operations.

### Infrastructure OS
*SO de Infraestructura*

The underlying operating system for managing hardware and network resources, providing a stable foundation for other PointSav services.

### IoT Devices
*Dispositivos de IoT*

Physical devices that connect to the internet to collect and share data. In the PointSav ecosystem, this includes sensors and other devices used to monitor and control building systems.


## J
<hr>


## K
<hr>


## L
<hr>


## M
<hr>

### MediaKit OS
*SO de MediaKit*

An operating system designed for managing and distributing media assets, including the PointSav design system, marketing materials, and documentation.

### MediaKit OS – Design System
The MediaKit OS design system integration provides the visual component vocabulary and token layer used by os-mediakit's document and asset generation pipeline.

### MediaKit OS – System Administration
MediaKit OS system administration covers the Tier A operator functions for managing os-mediakit's document pipeline configuration, ingestion rules, and storage allocation.

### Microkernel Operating System
*Microkernel*

An operating system architecture where the kernel is as small as possible, with most services running in user space. This can improve security and stability.


## N
<hr>

### Network Admin OS
*SO de Administración de Red*

A specialized operating system for network administrators to manage and monitor network infrastructure, including routers, switches, and firewalls.


## O
<hr>

### Operating System
*Sistema Operativo*

The software that supports a computer's basic functions, such as scheduling tasks, executing applications, and controlling peripherals.

### OrchestrationOS
*SO de Orquestación*

The stateless logic and compute layer. Holds no data. Connects ConsoleOS terminals to one or more ToteboxOS archives and provides extended compute capacity for BIM rendering, GIS spatial analysis, SLM inference, and data warehouse operations. Required for multi-archive use cases — the monetisation boundary between free and proprietary tiers.

### OrchestrationOS – BIM Server
*Servidor BIM de OrchestrationOS*

A component of OrchestrationOS responsible for managing and processing Building Information Modeling (BIM) data.

### OrchestrationOS – Command Centre
*Centro de Comando de OrchestrationOS*

The central management interface for OrchestrationOS, providing a single point of control for all orchestrated services.

### OrchestrationOS – Data Engine
*Motor de Datos de OrchestrationOS*

The data processing and storage component of OrchestrationOS, responsible for managing large datasets and providing data analytics capabilities.

### OrchestrationOS – GIS Engine
*Motor GIS de OrchestrationOS*

A component of OrchestrationOS that provides Geospatial Information System (GIS) capabilities, including mapping, spatial analysis, and data visualization.


## P
<hr>

### P2 – System Administration / Package Manager
The Tier 2 system administration and package management layer manages software installation, update verification, and signing for PointSav OS deployments below the ConsoleOS root level.

### PointSav Design System
The PointSav design system is a tokenized, DTCG-format component library and token vault delivered as a Git-tracked repository, providing the visual and interactive vocabulary for all PointSav product surfaces.

### PointSav Digital Systems
PointSav Digital Systems is the software vendor entity that builds and maintains the PointSav platform, publishing canonical engineering repositories at github.com/pointsav under a per-directory license scheme (the ratified root `LICENSE`, v1.2). Most `os-*`/`service-*`/`app-console-*` directories are AGPL-3.0-or-later; a handful (`os-infrastructure`, `os-mediakit`, `app-mediakit-*`, `os-totebox`) are FSL-1.1-ALv2, with `os-totebox` auto-converting to Apache-2.0 on each dated release; `os-orchestration` is fully proprietary under the PointSav-ARR terms.

### PointSav Private Network
The PointSav private network is the on-premises sovereign mesh that connects os-console terminals, os-orchestration compute, and os-totebox archives within a customer deployment, isolated from the public internet by the os-infrastructure layer.

### PrivateGit OS
*SO de PrivateGit*

An operating system for managing private Git repositories, providing a secure, self-hosted alternative to public Git hosting services.

### Private Network
A private network restricts access to authorized users and devices; in PointSav, the six-tier sovereignty matrix defines which network segments are accessible at each trust tier, enforced by os-infrastructure.

### PropertyArchive
*PropertyArchive*

A ToteboxOS archive for a physical property. Anchored to a Land Title PIN or legal address. Contains permits, lifecycle records, BIM drawings, IoT data, lease register, and maintenance history. Replaces legacy term RealPropertyArchive.

### Property Management
*Administración de Propiedades*

Function of proprietary software.

### Public Browser Delivery – Data Marketplace
Public browser delivery for the data marketplace provides browser-accessible endpoints through which external consumers purchase and retrieve licensed data assets curated by service-content.

### Public Cloud
Traditional off-premise infrastructure. In the 2030 platform vision, this represents a structural dependency that PointSav's planned architecture is intended to mitigate.


## R
<hr>

### Real-Time Operating System
A real-time operating system guarantees bounded response times for time-sensitive tasks; PointSav's IoT ingestion path relies on os-totebox to receive real-time streams from RTOS-equipped field devices.

### Record Keeping
*Mantenimiento de Registros*

Function of proprietary software.


## S
<hr>

### Second-party Data
Second-party data is first-party data obtained through a direct partnership agreement; in PointSav, it enters through controlled service-content endpoints with explicit data-sharing contracts recorded in the ledger.

### service-extraction
*service-extraction*

The deterministic parser service. Strips proprietary formatting from inbound payloads and routes structured data to deterministic services and unstructured text to service-slm. Assigns transaction IDs for chain-of-custody tracing. Canonical long-term name replacing the legacy working name service-parser.

### service-materials
*Catálogo de materiales*

A planned, archive-resident service intended to hold the shared catalog of material and building-element identity for use by domain engines such as [[tool-construction|tool-construction]] — classification against the published Uniclass tables, native unit of measure, an optional buildingSMART data dictionary reference, and a content-hash-verified specification citation. `service-materials` never holds cost, price, or productivity data — a citing project's own records reference a catalog row by its content hash, so a later edit to the shared definition is detectable rather than silent, while what a material costs or how productively it installs stays local, contractor-owned data. Proposed; not yet built.

### service-search
*service-search*

The planned inverted-index service for full-text retrieval across the files in a Totebox Archive using Tantivy, designed to operate without a running database engine and to remain searchable on an air-gapped machine. Not yet built — the directory holds a README describing the design, with no crate implementing it.

### Smart Building
*Edificio Inteligente*

A building that uses technology to automatically control its operations, including heating, ventilation, air conditioning, lighting, security, and other systems.

### Surveillance
Monitoring of user activity or system behaviour for security or analytical purposes. PointSav replaces third-party surveillance dependencies with zero-cookie first-party telemetry pipelines.

### System Design
System design is the process of defining the architecture, components, and interfaces of a system to satisfy specified requirements; PointSav's platform design is governed by the [[three-ring-architecture|three-ring-architecture]] and the six-tier sovereignty matrix.


## T
<hr>

### Technofeudalism
A term describing structural dependency on platform providers who control access to data and services. Cited as context for the vendor lock-in problem that PointSav is designed to resolve.

### Third-party Data
Third-party data is collected by an entity with no direct relationship to the end user and sold commercially; PointSav evaluates all third-party data through SYS-ADR-07 and ingests approved datasets via the service-content deterministic pipeline.

### tool-accounting
A flat-file, owner-held domain engine providing double-entry accounting — journals, ledgers, financial statements, and multi-entity consolidation — computed deterministically from plain-text records with no hosted database and git as the audit trail. The platform's original domain engine, and the design pattern sibling `tool-*` engines (including `tool-construction`) are modeled against. Licensed under FSL-1.1-ALv2. See [[tool-accounting|tool-accounting]] for the full article.

### tool-construction
A flat-file, owner-held domain engine providing construction cost, schedule, and quality accountability, built on the same double-entry design discipline as `tool-accounting`. Its central mechanism: installed material quantity, reported once from the field, both earns a labour-hours budget and draws down a material balance in the same transaction — making the relationship between materials and labour structural to the ledger rather than a convention applied on top of it. Licensed under FSL-1.1-ALv2. See [[tool-construction|tool-construction]] for the full article.

### tool-payroll
A proposed, jurisdiction-aware domain engine for gross-to-net pay and statutory remittance timing, designed as a sibling product to `tool-accounting` and fed one-way by `tool-construction` timecards. 100% design as of this writing — no code written, no crate scaffolded. Licensed under FSL-1.1-ALv2. See [[tool-payroll|tool-payroll]] for the full article.

### `tool-*` distribution governance
*(Cross-reference note, not a full entry)*

The platform's distribution governance classifies every `tool-*` directory as internal operator tooling by default, not distributed as a standalone catalog product, with exceptions granted individually — `tool-wallet` is the one existing precedent. No such exception is currently recorded for `tool-accounting`, `tool-construction`, or `tool-payroll`.

### Totebox Archive
*Archivo Totebox*

A self-contained, portable, and encrypted repository for data and applications, designed for long-term storage and secure access. Each Totebox Archive is a single file that can be stored on any storage medium.

### Totebox OS
*SO Totebox*

The operating system that runs within a Totebox Archive, providing a secure environment for applications and services. It is designed to be lightweight and portable.

### Totebox OS – IoT Data
ToteboxOS IoT data handling receives telemetry streams from connected physical devices and writes them to the WORM-secured archive, available for service-content gravity classification and os-mediakit report generation.

### Totebox Services
*Servicios Totebox*

A suite of applications and services that run within the Totebox OS, providing functionality such as data storage, communication, and collaboration tools.


## U
<hr>

### Unikernel
*Unikernel*

A specialized, single-address-space machine image constructed by using library operating systems. Unikernels are often smaller and more secure than traditional operating systems.

### User Experience or Service Design or UX
*Experiencia de Usuario (UX)*

The overall experience of a person using a product such as a website or computer application, especially in terms of how easy or pleasing it is to use.

### User Interface or Product Design or UI
*Interfaz de Usuario (UI)*

The means by which the user and a computer system interact, in particular the use of input devices and software.


## V
<hr>

### Virtual Machine or VM
*Máquina Virtual (VM)*

A software-based emulation of a physical computer. It has its own operating system and can run applications independently from the host machine.


## W
<hr>

### Windows Operating System
Microsoft Windows is used by PointSav for os-workplace deployments on managed desktop hardware, with the os-workplace sovereign desktop layer providing the management and security boundary above it.

### Workplace OS
*SO de Workplace*

A user-friendly, graphical operating system designed for everyday business-related tasks, providing a suite of productivity applications and a secure environment for users.

### Workplace OS – Browser
*Navegador de Workplace OS*

The web browser integrated into Workplace OS, providing secure and controlled access to the internet and internal web applications.

### Workplace OS – Calculator
*Calculadora de Workplace OS*

A basic calculator application included in Workplace OS for performing simple mathematical calculations.

### Workplace OS – File Manager
*Gestor de Archivos de Workplace OS*

The file management application in Workplace OS, used for organizing, browsing, and managing files and folders.

### Workplace OS – PDF Viewer
*Visor de PDF de Workplace OS*

An application for viewing PDF documents within the Workplace OS environment.

### Workplace OS – Spreadsheet
*Hoja de Cálculo de Workplace OS*

A spreadsheet application in Workplace OS for creating and editing spreadsheets, performing calculations, and analyzing data.

### Workplace OS – Word Processor
*Procesador de Textos de Workplace OS*

A word processing application in Workplace OS for creating, editing, and formatting text documents.


## Z
<hr>

### Zero-party Data
Zero-party data is information that users intentionally and proactively share with an organization; in PointSav, it is the highest-trust input class for service-content, requiring no inference and carrying explicit user consent.

## See also

- [[editorial-language-registers]]
