---
schema: foundry-doc-v1
title: "MCP como Protocolo Substrato"
slug: mcp-substrate-protocol.es
category: architecture
type: topic
quality: published
short_description: "Cada servicio Foundry del Anillo 1 y Anillo 2 expone una interfaz de servidor MCP como su contrato externo primario, con el Portero actuando como la puerta de enlace MCP."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: mcp-substrate-protocol.md
---

**MCP como Protocolo Substrato** designa el Protocolo de Contexto de Modelo (MCP) como el contrato de cable para toda la composición de servicios en la plataforma Foundry. Cada servicio del Anillo 1 y Anillo 2 expone una interfaz de servidor MCP como su contrato externo primario. El Portero (`service-slm`) es la puerta de enlace MCP. Las extensiones del cliente se conectan como servidores MCP adicionales. Esta decisión es estructural y está codificada en la reclamación doctrinal #46.

## Por qué MCP es a nivel de substrato

El Protocolo de Contexto de Modelo se ha convertido en el estándar de la industria para la composición de aplicaciones nativas de IA. Define una interfaz estable y legible por máquinas entre clientes, servidores y procesos anfitriones. Foundry lo adopta a nivel de substrato porque la alternativa — formatos de cable personalizados por servicio — acumula deuda de versionado, costos de prueba por par de contratos e implementaciones de clientes personalizados en cada consumidor.

El resultado práctico: un agente construido por el cliente, una extensión de IDE y la TUI del operador de Foundry interactúan con las mismas interfaces de servicio usando el mismo protocolo. No existe una "API para desarrolladores" distinta de la "API para usuarios." El contrato de cable está unificado.

## Cómo la arquitectura de tres anillos se mapea a los roles MCP

MCP define tres roles. La arquitectura de Foundry se mapea directamente sobre ellos: **Servidor MCP** — cada servicio del Anillo 1 y Anillo 2; **Cliente MCP** — el Portero (consumiendo servicios de los Anillos 1 y 2 como herramientas), la TUI del operador, agentes construidos por el cliente, extensiones de IDE; **Anfitrión MCP** — el Portero para flujos de inferencia, la TUI para flujos del operador.

El Portero es tanto Cliente MCP (llamando a `service-content` para la fundamentación del grafo) como Anfitrión MCP (presentando la interfaz de inferencia unificada a los llamadores externos). Esta dualidad es deliberada: el mismo proceso que custodia las credenciales de inferencia también media la composición de herramientas.

## Extensiones del cliente

Un cliente con una fuente de datos específica de su vertical puede escribir un servidor MCP que exponga ese sistema de datos como herramientas. El Portero descubre y usa esas herramientas en llamadas de inferencia posteriores junto con las herramientas integradas. Este es el mecanismo estructural para los [[vertical-seed-packs-marketplace]] planificados: se pretende que cada paquete incluya un servidor MCP de referencia para las fuentes de datos típicas de esa vertical.

## Compatibilidad HTTP preservada

La interfaz HTTP compatible con OpenAI del Portero se preserva junto a MCP. Los clientes de terceros que usan el SDK de OpenAI continúan funcionando sin modificación. MCP se añade como el estándar de composición a nivel de substrato, no como un reemplazo de la compatibilidad existente.

## Véase También

- [[single-boundary-compute-discipline]] — el Portero como única puerta de enlace MCP para inferencia
- [[knowledge-graph-grounded-apprenticeship]] — la consulta y mutación del grafo son llamadas de herramientas MCP
- [[code-for-machines-first]] — MCP como realización estructural de los contratos de servicio primero-para-máquinas
- [[vertical-seed-packs-marketplace]] — los paquetes planificados incluyen extensiones de servidor MCP específicas de vertical

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-mcp-substrate-protocol.md` (refinado el 30 de abril de 2026). Las referencias a la implementación de Fase 5 llevan encuadre "planificado" e "intencional" conforme a la postura de divulgación continua BCSC.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
