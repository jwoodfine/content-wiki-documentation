---
schema: foundry-doc-v1
title: "Arquitectura del stack Rust de service-slm"
slug: slm-stack-architecture
category: ai
type: topic
content_type: topic
quality: complete
index_group: the-doorman-boundary
short_description: "El grafo de dependencias Rust y la arquitectura de binarios de service-slm, el servicio Doorman que media cada llamada de inferencia en la plataforma PointSav."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites: []
paired_with: slm-stack-architecture.md

---

[[service-slm|`service-slm`]] se distribuye como un workspace Cargo de cinco crates (`slm-core`, `slm-doorman`, `slm-doorman-server`, `adapter-hub`, `slm-mcp-server`) con dos binarios `[[bin]]` (`slm-doorman-server`, `slm-mcp-server`) — una arquitectura plana por binario, no un binario único enlazado estáticamente para todo el sistema.

## Por qué importa la elección de Rust

La elección no es una preferencia de lenguaje. Es una restricción de ingeniería impuesta por el destino de despliegue previsto: hardware [[totebox-os|ToteboxOS]], donde un intérprete CPython más un marco de ML de gran tamaño no caben en el presupuesto de memoria disponible. La ausencia de recolector de basura, el arranque predecible y el paralelismo real sobre múltiples núcleos sin bloqueo global de intérprete son requisitos operativos, no mejoras opcionales.

## El marco "We Own It"

"We Own It" clasifica la **apertura del LLM**, no la composición del grafo de dependencias: L1 es pesos abiertos, L2 añade una licencia permisiva, L3 exige que todo el linaje — pesos, datos de entrenamiento y código — esté abiertamente licenciado. OLMo 3 cumple L3 bajo este marco.

Por separado, el propio grafo de dependencias no tiene ninguna licencia copyleft en ningún punto, por lo que PointSav conserva el derecho irrestricto de bifurcar, modificar y redistribuir — una propiedad que aplica `cargo-deny`, distinta de la clasificación "We Own It" anterior.

## Capas clave del stack

**Inferencia**: no es un binario Rust. El Nivel A ejecuta **llama-server (llama.cpp)** y el Nivel B ejecuta **vLLM** — ambos procesos externos, no Rust, invocados por HTTP. `mistral.rs` y `candle` no están desplegados en ninguna parte del stack actual; `candle` aparece solo como una ruta futura hipotética, no como infraestructura de producción. vLLM es el motor real y actual del Nivel B, sin reemplazo planificado.

El modelo base de producción es la familia **OLMo 3**, cuya totalidad — pesos, datos de entrenamiento y código — está bajo licencias permisivas (Apache 2.0 + Open Data Commons). Esta es la condición necesaria para la ruta de preentrenamiento continuo del [[apprenticeship-substrate]].

**HTTP y runtime**: `axum` + `tower` + `tokio` (todos MIT). Las llamadas HTTP salientes usan `reqwest`.

**Almacenamiento y estado**: el ledger de auditoría usa **rusqlite** con SQLite. El grafo de conocimiento a largo plazo (en [[service-content]]) es LadybugDB. No existe hoy en el stack ninguna dependencia para el almacenamiento en la nube de pesos/adaptadores.

**Procesamiento de documentos, orquestación y observabilidad.** Ninguno de estos forma parte del stack hoy: no existen bibliotecas de ingesta de PDF/DOCX, ningún marco de orquestación de trabajos, ningún exportador de trazas, ni ninguna dependencia de firma de artefactos en este workspace.

**Higiene de licencias.** `cargo-deny` se ejecuta en CI. La lista de licencias permitidas es `MIT`, `Apache-2.0`, `Apache-2.0 WITH LLVM-exception`, `BSD-2-Clause`, `BSD-3-Clause`, `CC0-1.0`, `ISC`, `MPL-2.0` (a nivel de archivo), `Unicode-DFS-2016`, `Unicode-3.0`, y `Zlib`.

## Integración con ToteboxOS

La arquitectura está motivada en parte por las restricciones de despliegue de ToteboxOS. Un stack CPython más un marco de inferencia GPU no cabe en el presupuesto de memoria disponible en hardware de appliance restringido. Un binario Rust con un runtime de inferencia cuantizado operando en modo CPU sí cabe.

**La restricción vinculante en los hosts Laptop-A es un presupuesto de 4 GB de RAM.**

- Binario estático por cada objetivo `[[bin]]`, sin arranque de intérprete — segundos, no minutos, hasta la primera inferencia
- Sin recolector de basura, sin heap de intérprete
- Paralelismo real entre núcleos sin bloqueo global de intérprete
- Compilación cruzada vía `cargo build --target aarch64-unknown-linux-gnu` para objetivos ARM de ToteboxOS

## Dos servicios externos que no son Rust

El sustrato de cómputo Yo-Yo depende de dos servicios externos no-Rust:

**LMCache + Mooncake Store** (plano de control en Python + Mooncake Transfer Engine en C++): el nivel de caché KV que persiste el estado de prefill a través de los reinicios de nodos GPU. service-slm mantiene un cliente Rust que se comunica con Mooncake vía HTTP y TCP. Sin acoplamiento FFI. Ambos tienen licencia Apache-2.0.

**vLLM** (Python): el motor de inferencia real y actual del Nivel B (véase Capa de inferencia, arriba). Apache-2.0.

Ambos están detrás de protocolos de red estables; service-slm depende del protocolo de comunicación, no de la implementación. Sustituir cualquiera de ellos requiere cambiar un único módulo cliente.

## Véase también

- [[compounding-doorman]] — el patrón operativo que service-slm implementa
- [[yoyo-compute-substrate]] — el substrato de cómputo multi-anillo que service-slm dirige
- [[apprenticeship-substrate]] — cómo el ledger de auditoría alimenta el entrenamiento de adaptadores LoRA
