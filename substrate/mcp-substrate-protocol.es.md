---
schema: foundry-doc-v1
title: "MCP como protocolo substrato"
slug: mcp-substrate-protocol
category: substrate
type: topic
content_type: topic
quality: complete
index_group: the-compounding-doorman-and-ai-boundary
short_description: "Cada servicio del Anillo 1 y Anillo 2 expone una interfaz de servidor MCP como su contrato externo primario, con el Portero actuando como la puerta de enlace MCP."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Anthropic. 'Model Context Protocol Specification.' modelcontextprotocol.io, 2025."
    url: "https://modelcontextprotocol.io/specification/2025-11-25"
paired_with: mcp-substrate-protocol.md
---


**MCP como Protocolo Substrato** designa el Protocolo de Contexto de Modelo (MCP) como el contrato de cable para toda la composición de servicios en la plataforma. Cada servicio del Anillo 1 y Anillo 2 expone una interfaz de servidor MCP como su contrato externo primario. El [[compounding-doorman|Portero]] ([[service-slm]]) es la puerta de enlace MCP. Las extensiones del cliente se conectan como servidores MCP adicionales. Esta decisión es estructural.

## Por qué MCP es a nivel de substrato

El Protocolo de Contexto de Modelo se ha convertido en el estándar de la industria para la composición de aplicaciones nativas de IA. Define una interfaz estable y legible por máquinas entre clientes, servidores y procesos anfitriones. [^1] La plataforma lo adopta a nivel de substrato porque la alternativa — formatos de cable personalizados por servicio — acumula deuda de versionado, costos de prueba por par de contratos e implementaciones de clientes personalizados en cada consumidor.

El resultado práctico: un agente construido por el cliente, una extensión de IDE y la TUI del operador interactúan con las mismas interfaces de servicio usando el mismo protocolo. No existe una "API para desarrolladores" distinta de la "API para usuarios." El contrato de cable está unificado.

## Cómo la arquitectura de tres anillos se mapea a los roles MCP

MCP define tres roles. La arquitectura de la plataforma se mapea directamente sobre ellos: **Servidor MCP** — cada servicio del Anillo 1 y Anillo 2; **Cliente MCP** — el Portero (consumiendo servicios de los Anillos 1 y 2 como herramientas), la TUI del operador, agentes construidos por el cliente, extensiones de IDE; **Anfitrión MCP** — el Portero para flujos de inferencia, la TUI para flujos del operador.

El [[compounding-doorman|Portero]] es tanto Cliente MCP (llamando a [[service-content]] para la [[knowledge-graph-grounded-apprenticeship|fundamentación del grafo]]) como Anfitrión MCP (presentando la interfaz de inferencia unificada a los llamadores externos). Esta dualidad es deliberada: el mismo proceso que custodia las credenciales de inferencia también media la composición de herramientas.

## Semántica de herramientas

Cada servicio expone un pequeño conjunto de herramientas MCP con nombre. `service-content` expone consulta y mutación del grafo; la búsqueda vectorial y la consulta temporal aún no están implementadas — la propia arquitectura del servicio enumera la clasificación por palabras clave, no la búsqueda vectorial, como el mecanismo de recuperación actual. El servicio de registro de archivos expone exactamente una herramienta MCP, `ledger.append`; existe además un recurso MCP de solo lectura, "Entradas del Registro", para leer el historial — un primitivo distinto de una herramienta de consulta — y no hay una herramienta de checkpoint dedicada. El servicio de extracción expone extracción y clasificación de entidades. El servicio de personas expone búsqueda, upsert y consulta de relaciones de personas.

Se pretende que el servicio de mercado (planificado para la Fase 5) exponga creación de listados, consulta de listados e inicio de transacciones como herramientas MCP. Los clientes que extienden la plataforma añaden nuevos servidores MCP que exponen sus propias herramientas específicas de vertical. El [[compounding-doorman|Portero]] descubre nuevas herramientas al inicio de la sesión mediante el método `tools/list` de MCP; no se requiere ningún cambio en el código central para acomodar una nueva extensión.

## El Portero como puerta de enlace MCP

Cuando cualquier llamador — sesión de tarea, TUI del operador o agente del cliente — envía una solicitud de inferencia al Portero, el Portero es simultáneamente cliente (llamando a [[service-content]] para el contexto del grafo según [[knowledge-graph-grounded-apprenticeship]]) y puerta de enlace (enrutando la solicitud al nivel de cómputo apropiado). Este punto de mediación es donde convergen la fundamentación del grafo, el registro de auditoría, la selección de nivel y la aplicación de la frontera de cómputo.

## Extensiones del cliente

Un cliente con una fuente de datos específica de su vertical puede escribir un servidor MCP que exponga ese sistema de datos como herramientas. El Portero descubre y usa esas herramientas en llamadas de inferencia posteriores junto con las herramientas integradas. Este es el mecanismo estructural para los [[vertical-seed-packs-marketplace]] planificados: se pretende que cada paquete incluya un servidor MCP de referencia para las fuentes de datos típicas de esa vertical.

## Composición con Código para Máquinas Primero

MCP es la realización estructural del principio [[code-for-machines-first]]. Cada contrato de servicio es legible por máquinas e introspectable en tiempo de ejecución. Las superficies orientadas al ser humano — la TUI, las interfaces web — son clientes de las mismas interfaces MCP que usaría cualquier otro agente. No existe ninguna superficie de datos exclusiva para humanos en la plataforma.

## Compatibilidad HTTP preservada

La interfaz HTTP compatible con OpenAI del Portero se preserva junto a MCP. Los clientes de terceros que usan el SDK de OpenAI continúan funcionando sin modificación. MCP se añade como el estándar de composición a nivel de substrato, no como un reemplazo de la compatibilidad existente.

## Véase También

- [[single-boundary-compute-discipline]] — el Portero como única puerta de enlace MCP para inferencia
- [[knowledge-graph-grounded-apprenticeship]] — la consulta y mutación del grafo son llamadas de herramientas MCP
- [[code-for-machines-first]] — MCP como realización estructural de los contratos de servicio primero-para-máquinas
- [[vertical-seed-packs-marketplace]] — los paquetes planificados incluyen extensiones de servidor MCP específicas de vertical
