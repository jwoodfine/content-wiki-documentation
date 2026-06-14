---
schema: foundry-doc-v1
title: "Catálogo de Guías Operacionales"
slug: guide-catalog
category: reference
type: topic
content_type: topic
status: stable
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: guide-catalog.md
---

El Catálogo de Guías Operacionales enumera todas las guías operacionales del despliegue de flota Woodfine, organizadas por propósito. Cada guía cubre una tarea operacional específica en un nodo de despliegue designado. Utilice este catálogo para localizar la guía correcta cuando sepa lo que necesita hacer, pero no cuál sistema es el responsable de la tarea. Para la arquitectura de despliegue que sustenta cada tipo de nodo, véase [[totebox-archive|Archivo Totebox]] y [[totebox-orchestration-development]].

## Aprovisionamiento y Despliegue

Esta sección reúne las guías para aprovisionar nuevos nodos y desplegar servicios en toda la flota. Consulte estas guías al poner en marcha un nuevo nodo, realizar un despliegue desde cero o recuperar un despliegue a un estado conocido y válido.

- **guide-deployment** (cluster-totebox-corporate) — despliega el nodo Totebox del archivo corporativo
- **guide-provision-node** (cluster-totebox-corporate) — aprovisiona un nuevo nodo del archivo corporativo
- **guide-deployment** (cluster-totebox-property) — despliega el nodo Totebox del archivo de propiedad
- **guide-provision-node** (cluster-totebox-property) — aprovisiona un nuevo nodo del archivo de propiedad
- **guide-deployment** (fleet-infrastructure-cloud) — despliega un nodo de retransmisión en la nube (GCP)
- **guide-provision-node** (fleet-infrastructure-cloud) — aprovisiona un nodo de retransmisión en la nube
- **guide-deployment** (fleet-infrastructure-onprem) — despliega un nodo de hardware en instalaciones propias
- **guide-provision-node** (fleet-infrastructure-onprem) — aprovisiona un nodo en instalaciones propias
- **guide-deployment** (gateway-interface-command) — despliega la pasarela de interfaz de comando
- **guide-provision-node** (gateway-interface-command) — aprovisiona un nodo de interfaz de comando
- **guide-deployment** (cluster-totebox-personnel) — despliega el nodo del archivo de personal
- **guide-provision-node** (cluster-totebox-personnel) — aprovisiona un nodo del archivo de personal
- **guide-provision-standalone** (fleet-infrastructure-leased) — aprovisiona un nodo de servidor dedicado en arrendamiento
- **guide-provision-relay** (fleet-infrastructure-cloud) — aprovisiona el retransmisor PPN en la nube
- **guide-provision-onprem** (fleet-infrastructure-onprem) — aprovisiona la pila de hardware en instalaciones propias
- **guide-deployment** (route-network-admin) — despliega el nodo de enrutamiento de administración de red
- **guide-provision-node** (route-network-admin) — aprovisiona el nodo de enrutamiento de administración de red
- **guide-provision-node** (vault-privategit-source) — aprovisiona el nodo de bóveda git privada

## BIM y Propiedad

Esta sección reúne las guías para operar la pasarela de orquestación BIM y el archivo de propiedad. Consulte estas guías cuando cree o gestione objetos BIM, publique superposiciones regulatorias o realice operaciones cotidianas en el archivo de propiedad.

- **guide-bim-object-authoring** (gateway-orchestration-bim) — crea y modifica objetos BIM dentro del archivo IFC
- **guide-bim-token-authoring** (gateway-orchestration-bim) — crea tokens BIM para el registro de tokens BIM de Woodfine
- **guide-climate-zone-objects** (gateway-orchestration-bim) — asigna y gestiona clasificaciones de zonas climáticas en objetos BIM
- **guide-climate-zone-tokens** (gateway-orchestration-bim) — publica conjuntos de tokens de zonas climáticas en el registro de tokens BIM
- **guide-deploy-bim-substrate** (gateway-orchestration-bim) — despliega el sustrato BIM en un nodo gateway-orchestration-bim
- **guide-deployment** (gateway-orchestration-bim) — despliega la pasarela de orquestación BIM
- **guide-provision-node** (gateway-orchestration-bim) — aprovisiona un nodo de pasarela de orquestación BIM
- **guide-regulation-overlay-publishing** (gateway-orchestration-bim) — publica superposiciones regulatorias (zonificación, código de construcción) sobre capas del modelo BIM
- **guide-bim-archive-operations** (cluster-totebox-property) — operaciones cotidianas del archivo BIM de propiedad (ingesta IFC, validación y mantenimiento)

## SIG y Geoespacial

Esta sección reúne las guías para operar el proceso de co-localización SIG y la pasarela de orquestación geoespacial. Consulte estas guías cuando incorpore nuevas cadenas minoristas, amplíe la cobertura a nuevos países, reconstruya el proceso SIG o despliegue la pasarela SIG.

- **guide-gis-adding-a-chain** (gateway-orchestration-gis) — incorpora una nueva cadena minorista al proceso de co-localización SIG
- **guide-gis-adding-a-country** (gateway-orchestration-gis) — agrega un nuevo país al área de cobertura SIG y reconstruye las capas de datos afectadas
- **guide-gis-pipeline-rebuild** (gateway-orchestration-gis) — realiza una reconstrucción completa del proceso SIG a partir de los datos fuente
- **guide-totebox-orchestration-gis** (gateway-orchestration-gis) — ejecuta el flujo de trabajo de orquestación Totebox SIG de principio a fin
- **guide-deployment** (gateway-orchestration-gis) — despliega la pasarela de orquestación SIG
- **guide-provision-node** (gateway-orchestration-gis) — aprovisiona un nodo de pasarela de orquestación SIG

## Personal e Identidad

Esta sección reúne las guías para operar el archivo de personal. Consulte estas guías cuando gestione registros de personal, ejecute integraciones de identidad, opere la superficie de búsqueda soberana o ejecute inferencia del modelo de lenguaje reducido en el clúster de personal.

- **guide-cold-storage-sync** (cluster-totebox-personnel) — sincroniza registros de personal con almacenamiento en frío cifrado
- **guide-ingress-operations** (cluster-totebox-personnel) — gestiona la ingesta y verificación de datos entrantes de personal
- **guide-linkedin-adapter** (cluster-totebox-personnel) — opera el adaptador de datos profesionales de LinkedIn
- **guide-msft-entra-id** (cluster-totebox-personnel) — configura y opera la integración de identidad con Microsoft Entra ID
- **guide-personnel-ledger** (cluster-totebox-personnel) — gestiona el libro mayor de personal: creación, actualización y auditoría de registros
- **guide-slm-execution** (cluster-totebox-personnel) — ejecuta la capa de inferencia del modelo de lenguaje reducido en el clúster de personal
- **guide-sovereign-search** (cluster-totebox-personnel) — opera la superficie de búsqueda de texto completo soberana para datos de personal
- **guide-totebox-orchestration** (cluster-totebox-personnel) — ejecuta el flujo de trabajo de orquestación Totebox del archivo de personal

## Redes e Infraestructura

Esta sección reúne las guías para operar superposiciones de red en la flota, la inscripción de equipos terminales y la capa de enrutamiento de malla de la Red Privada Pointsav. Consulte estas guías cuando despliegue superposiciones VPN, configure equipos macOS, administre redes de contenedores u orqueste la malla PPN.

- **guide-deploy-vpn** (fleet-infrastructure-leased) — despliega la superposición VPN WireGuard en nodos de servidores arrendados
- **guide-endpoint-macbook** (fleet-infrastructure-leased) — aprovisiona un equipo terminal macOS en el nivel de infraestructura arrendada
- **guide-macos-endpoints** (fleet-infrastructure-leased) — gestiona la configuración e inscripción de equipos terminales macOS
- **guide-lxc-network-admin** (fleet-infrastructure-onprem) — administra las redes de contenedores LXC en hardware en instalaciones propias
- **guide-mesh-orchestration** (route-network-admin) — orquesta la capa de enrutamiento de malla de la Red Privada Pointsav
- **guide-mesh-execution** (root) — ejecuta una operación de malla PPN desde el terminal F8
- **guide-physical-egress** (root) — gestiona el egreso físico y los flujos de trabajo de impresión regulatoria

## Consola y Operaciones

Esta sección reúne las guías para operar la consola unificada de gestión de activos. Consulte estas guías cuando realice operaciones diarias de consola, gestione el libro mayor de comandos, empareje dispositivos o supervise la telemetría de la flota.

- **guide-console-operations** (node-console-operator) — operaciones diarias de la consola unificada de gestión de activos
- **guide-command-ledger** (node-console-operator) — gestiona el libro mayor de comandos: registro, reproducción y auditoría de comandos de consola
- **guide-mba-pairing-ceremony** (node-console-operator) — realiza la ceremonia de emparejamiento del dispositivo MBA para la autenticación de consola
- **guide-os-console-operator** (node-console-operator) — instala y opera la plataforma os-console para el nodo de consola Woodfine
- **guide-telemetry-operations** (root) — supervisa y gestiona la telemetría operacional en toda la flota Woodfine

## Contenido y Medios

Esta sección reúne las guías para operar la wiki de documentación, la wiki corporativa, la wiki de proyectos y el sitio de marketing. Consulte estas guías cuando ejecute revisiones editoriales, gestione hojas de ruta de sprints, configure tokens de diseño u opere despliegues de nodos de medios.

- **guide-editorial-content-sweep** (media-knowledge-documentation) — ejecuta un pase de revisión editorial en la wiki de documentación
- **guide-knowledge-wiki-sprint-roadmap** (media-knowledge-documentation) — gestiona la planificación de sprints y la hoja de ruta de la wiki de conocimiento
- **guide-wiki-dark-mode-toggle** (media-knowledge-documentation) — configura y prueba el interruptor de modo oscuro de la wiki
- **guide-wiki-design-tokens** (media-knowledge-documentation) — aplica y audita las actualizaciones de tokens de diseño en la superficie de la wiki
- **guide-deployment** (media-knowledge-corporate) — despliega el nodo de medios de la wiki corporativa
- **guide-provision-node** (media-knowledge-corporate) — aprovisiona un nodo de la wiki corporativa
- **guide-deployment** (media-knowledge-projects) — despliega el nodo de medios de la wiki de proyectos
- **guide-provision-node** (media-knowledge-projects) — aprovisiona un nodo de la wiki de proyectos
- **guide-deployment-marketing-site** (media-marketing-landing) — despliega el sitio de marketing y páginas de aterrizaje de Woodfine
- **guide-operate-marketing-landing** (media-marketing-landing) — operaciones diarias de la página de aterrizaje de marketing
- **guide-provision-marketing-site** (media-marketing-landing) — aprovisiona la infraestructura del sitio de marketing
- **guide-telemetry-governance** (media-marketing-landing) — gestiona la política de gobernanza de telemetría para el sitio de marketing
- **guide-telemetry-operations** (media-marketing-landing) — opera la pila de telemetría del sitio de marketing

## Control de Fuentes y Distribución

Esta sección reúne las guías para operar la bóveda git privada. Consulte estas guías cuando gestione la distribución de software, abra sesiones de desarrollo, opere el servicio de control de acceso Doorman, administre el nodo de bóveda o configure un entorno de trabajo para desarrolladores.

- **guide-command-session** (vault-privategit-source) — abre y opera una Sesión de Comando contra la bóveda git privada
- **guide-deployment** (vault-privategit-source) — despliega el nodo vault-privategit-source
- **guide-doorman-deployment** (vault-privategit-source) — despliega el servicio de control de acceso Doorman en el nodo de bóveda
- **guide-doorman** (vault-privategit-source) — opera el Doorman de service-slm: control de acceso, registro de autenticación y gestión de sesiones
- **guide-open-archive** (vault-privategit-source) — abre un Archivo Totebox para una nueva sesión de desarrollo
- **guide-operating-yoyo** (vault-privategit-source) — opera la capa de programación de Cómputo Elástico (Yo-Yo) dentro del entorno de bóveda
- **guide-software-distribution-operations** (vault-privategit-source) — gestiona las operaciones de distribución de software: paquetes de versión, binarios y publicación de artefactos
- **guide-tier-a-sysadmin-tui** (vault-privategit-source) — opera la interfaz TUI de administración de sistemas de Nivel A para la administración a nivel de bóveda
- **guide-workbench-setup** (vault-privategit-source) — configura el entorno de trabajo del desarrollador en el nodo de bóveda

## Inteligencia Artificial y Aprendizaje Automático

Esta sección reúne las guías para operar el clúster de inteligencia y el [[service-slm|servicio de inferencia del modelo de lenguaje reducido]]. Consulte estas guías cuando ejecute el proceso de [[yoyo-compute-substrate|cómputo elástico]] nocturno o despliegue el servicio de inferencia dentro del clúster de personal.

- **guide-elastic-compute-nightly-pipeline** (cluster-intelligence) — ejecuta el proceso nocturno de cómputo elástico (ajuste fino LoRA)
- **guide-01-deployment** (cluster-totebox-personnel/service-slm) — despliega el servicio de inferencia del modelo de lenguaje reducido dentro del clúster de personal

## Entorno de Desarrollo

Esta sección reúne las guías para operar el propio entorno de trabajo Foundry. Consulte estas guías cuando aprovisione nuevos Archivos Totebox, gestione ganchos de pre-confirmación, recupere recursos de la máquina virtual o verifique las herramientas de Claude Code.

- **guide-claude-code-hooks-installed** (foundry-workspace) — verifica y opera los ganchos de pre-herramienta de Claude Code en el entorno de trabajo Foundry
- **guide-foundry-vm-resource-recovery** (foundry-workspace) — recupera recursos de disco y memoria en la máquina virtual GCE de Foundry
- **guide-onboarding-new-archive** (foundry-workspace) — aprovisiona un nuevo Archivo Totebox desde cero dentro del entorno de trabajo Foundry
- **guide-pre-commit-gate-operator-flow** (foundry-workspace) — opera la puerta de pre-confirmación: cómo gestionar fallos de ganchos, procedimientos de omisión y auditorías de la puerta

## Véase También

- [[totebox-orchestration-development]] — el modelo de desarrollo de orquestación Totebox que sustenta el aprovisionamiento y la operación de los nodos de despliegue de flota
- [[totebox-archive]] — el patrón de Archivo Totebox que organiza el trabajo en sesiones a través de todos los clústeres de despliegue de flota
