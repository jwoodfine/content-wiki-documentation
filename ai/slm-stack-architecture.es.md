---
schema: foundry-doc-v1
title: "Arquitectura del stack Rust de service-slm"
slug: slm-stack-architecture
category: ai
type: topic
content_type: topic
quality: complete
index_group: the-doorman-boundary
short_description: "El stack real de service-slm: cinco crates de Rust con dos binarios reales — no el binario único que versiones anteriores afirmaban — con la inferencia en llama-server/vLLM externos, no Rust, y varios crates de procesamiento de documentos que no existen en el código."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites: []
paired_with: slm-stack-architecture.md

---

**Qué cambió en esta revisión.** Versiones anteriores de este artículo describían con confianza un stack que no coincide con el código real de `service-slm`. Esta revisión está verificada directamente contra el código fuente, no solo suavizada, y encontró un binario único inventado, un motor de inferencia en Rust que no existe, un marco "We Own It" fabricado, un tercer servicio externo sin respaldo en el código, y varios crates de procesamiento de documentos que no existen en ninguna parte del `Cargo.lock`.

[[service-slm|`service-slm`]] se distribuye como un workspace Cargo de cinco crates reales (`slm-core`, `slm-doorman`, `slm-doorman-server`, `adapter-hub`, `slm-mcp-server`) con dos binarios `[[bin]]` reales (`slm-doorman-server`, `slm-mcp-server`) — no el binario único enlazado estáticamente que afirmaba texto anterior; no existe ninguna configuración de enlace estático (musl o similar) en la configuración del toolchain. El propio `ARCHITECTURE.md` del workspace lo llama una "arquitectura plana" por binario, no un binario único para todo el sistema.

## Por qué importa la elección de Rust

La elección no es una preferencia de lenguaje. Es una restricción de ingeniería impuesta por el destino de despliegue previsto: hardware [[totebox-os|ToteboxOS]], donde un intérprete CPython más un marco de ML de gran tamaño no caben en el presupuesto de memoria disponible. La ausencia de recolector de basura, el arranque predecible y el paralelismo real sobre múltiples núcleos sin bloqueo global de intérprete son requisitos operativos, no mejoras opcionales.

## El marco real "We Own It" — no la taxonomía de dependencias Rust que inventaba texto anterior

Versiones anteriores describían una tabla de tres niveles "L1/L2/L3 de Rust" que clasificaba cuánto del árbol de dependencias es Rust frente a FFI, y llamaba a eso la prueba "We Own It". **Esa tabla no corresponde a ningún marco real de este código base.** El concepto real de "We Own It", documentado en `substrate/llm-substrate-decision.md` y `service-slm/docs/yoyo-training-substrate-and-service-content-integration.md`, clasifica la **apertura del LLM**, no la composición del grafo de dependencias: L1 es pesos abiertos, L2 añade una licencia permisiva, L3 exige que todo el linaje — pesos, datos de entrenamiento y código — esté abiertamente licenciado. OLMo 3 se cita en la documentación real como cumplidor de L3 bajo *este* marco, una afirmación sobre el modelo, no sobre cuánto del propio árbol de dependencias Cargo de `service-slm` está escrito en Rust. La propiedad de higiene de licencias que texto anterior buscaba describir (sin licencias copyleft en ningún punto del grafo de dependencias, por lo que PointSav conserva el derecho irrestricto de bifurcar, modificar y redistribuir) es real y la aplica `cargo-deny` — simplemente no es lo que "We Own It" significa en el vocabulario propio de este código base, y confundir ambos conceptos inventa un marco que no existe.

## Capas clave del stack

**Inferencia**: no es un binario Rust. El Nivel A ejecuta **llama-server (llama.cpp)** y el Nivel B ejecuta **vLLM** — ambos procesos externos, no Rust, invocados por HTTP (`service-slm/ARCHITECTURE.md`). `mistral.rs` y `candle` no están desplegados en ninguna parte del stack actual; `candle` aparece solo como una ruta futura hipotética en la documentación, no como infraestructura de producción. La afirmación de texto anterior de que vLLM era "el motor de inferencia de prueba de la Fase 1, reemplazado por mistral.rs en la Fase 2" se contradice con el resto del propio historial de correcciones de este artículo — vLLM es el motor real y actual del Nivel B, sin reemplazo planificado ni en curso.

El modelo base de producción es la familia **OLMo 3**, cuya totalidad — pesos, datos de entrenamiento y código — está bajo licencias permisivas (Apache 2.0 + Open Data Commons). Esta es la condición necesaria para la ruta de preentrenamiento continuo del [[apprenticeship-substrate]].

**HTTP y runtime**: `axum` + `tower` + `tokio` (todos MIT), confirmados en el `Cargo.toml` real. Las llamadas HTTP salientes usan `reqwest`.

**Almacenamiento y estado**: el ledger de auditoría usa **rusqlite** con SQLite, no `sqlx` como afirmaba texto anterior — `Cargo.lock` no tiene ninguna coincidencia de `sqlx` entre los 286 paquetes del workspace. El grafo de conocimiento a largo plazo (en [[service-content]]) es LadybugDB. No se encontró ninguna dependencia `object_store` para el almacenamiento en la nube de pesos/adaptadores; la afirmación de texto anterior al respecto no está confirmada.

**Procesamiento de documentos, orquestación y observabilidad — no son dependencias reales.** Texto anterior nombraba un stack sustancial de procesamiento de documentos y orquestación — `oxidize-pdf`, `docx-rust`, `calamine`, `pulldown-cmark` para la ingesta de documentos; `apalis` para orquestación de trabajos; `opentelemetry-rust` para exportación de trazas; `sigstore-rs` para firma de artefactos; `mupdf-rs` como dependencia AGPL explícitamente excluida. **Ninguno de estos aparece en ninguna parte del `Cargo.lock` del workspace.** Esta sección completa de texto anterior fue inventada, no simplemente imprecisa — no hay evidencia real de que este stack de procesamiento de documentos/orquestación/observabilidad exista en `service-slm` hoy.

**Higiene de licencias — confirmada real, con correcciones menores.** `cargo-deny` realmente se ejecuta en CI con un `deny.toml` real, confirmado por lectura directa. La lista de licencias permitidas coincide en gran parte con lo descrito antes (`MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `MPL-2.0` a nivel de archivo, `Zlib`), con dos correcciones: el archivo real también permite `Apache-2.0 WITH LLVM-exception` y `CC0-1.0`, ambas omitidas antes; y las entradas de licencia Unicode son `Unicode-DFS-2016`/`Unicode-3.0` en el archivo real, no el `Unicode-DFS` genérico que usaba texto anterior.

## Integración con ToteboxOS

La arquitectura está motivada en parte por las restricciones de despliegue de ToteboxOS. Un stack CPython más un marco de inferencia GPU no cabe en el presupuesto de memoria disponible en hardware de appliance restringido. Un binario Rust con un runtime de inferencia cuantizado operando en modo CPU sí cabe.

**La restricción vinculante en los hosts Laptop-A es el presupuesto de 4 GB de RAM** — no la cifra de "~550 MB de margen disponible" que citaba texto anterior, la cual no tiene fuente en ninguna parte del código base; el `ARCHITECTURE.md` real indica directamente la cifra de 4 GB.

- Binario estático por cada objetivo `[[bin]]`, sin arranque de intérprete — segundos, no minutos, hasta la primera inferencia
- Sin recolector de basura, sin heap de intérprete
- Paralelismo real entre núcleos sin bloqueo global de intérprete
- Compilación cruzada vía `cargo build --target aarch64-unknown-linux-gnu` para objetivos ARM de ToteboxOS

## Dos servicios externos que no son Rust — no tres

Versiones anteriores de este artículo enumeraban tres servicios externos no-Rust en el sustrato de cómputo Yo-Yo, incluyendo "SkyPilot" para orquestación de GPU multi-nube. **SkyPilot no tiene ninguna referencia en ninguna parte del monorepo** y se elimina aquí en lugar de mantenerse sin verificar. Los dos reales:

**LMCache + Mooncake Store** (plano de control en Python + Mooncake Transfer Engine en C++): el nivel de caché KV que persiste el estado de prefill a través de los reinicios de nodos GPU. service-slm mantiene un cliente Rust que se comunica con Mooncake vía HTTP y TCP. Sin acoplamiento FFI. Ambos tienen licencia Apache-2.0.

**vLLM** (Python): el motor de inferencia real y actual del Nivel B (véase Capa de inferencia, arriba) — no una prueba superada, como afirmaba texto anterior. Apache-2.0.

Ambos están detrás de protocolos de red estables; service-slm depende del protocolo de comunicación, no de la implementación. Sustituir cualquiera de ellos requiere cambiar un único módulo cliente.

## Véase también

- [[compounding-doorman]] — el patrón operativo que service-slm implementa
- [[yoyo-compute-substrate]] — el substrato de cómputo multi-anillo que service-slm dirige
- [[apprenticeship-substrate]] — cómo el ledger de auditoría alimenta el entrenamiento de adaptadores LoRA
