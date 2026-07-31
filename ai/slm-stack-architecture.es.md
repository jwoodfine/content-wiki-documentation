---
schema: foundry-doc-v1
title: "Arquitectura del stack Rust de service-slm"
slug: slm-stack-architecture
category: ai
type: topic
content_type: topic
quality: complete
short_description: "Visión estratégica del stack Rust de service-slm: un binario único, licencias permisivas de extremo a extremo, y la disciplina de construcción que mantiene la soberanía técnica sobre cada dependencia."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-31
editor: pointsav-engineering
cites: []
paired_with: slm-stack-architecture.md
---

[[service-slm|`service-slm`]] — el [[doorman-protocol|Doorman]] de la plataforma [[pointsav-overview|PointSav]] — se construye como un único binario de Rust enlazado estáticamente. Cada dependencia directa en el stack es Rust puro o bindings Rust sobre una biblioteca nativa con licencia permisiva. No hay licencias copyleft en ningún punto del grafo de dependencias. Esta propiedad, denominada criterio "We Own It", garantiza que PointSav conserva el derecho irrestricto de bifurcar, modificar y redistribuir la totalidad del código base en cualquier momento.

## Por qué importa la elección de Rust

La elección no es una preferencia de lenguaje. Es una restricción de ingeniería impuesta por el destino de despliegue previsto: hardware [[totebox-os|ToteboxOS]], donde un intérprete CPython más un marco de ML de gran tamaño no caben en el presupuesto de memoria disponible. La ausencia de recolector de basura, el arranque predecible y el paralelismo real sobre múltiples núcleos sin bloqueo global de intérprete son requisitos operativos, no mejoras opcionales.

El objetivo técnico es lo que la industria denomina "Rust de nivel L2": todo el código escrito por PointSav es Rust, y cada crate de dependencia directa es un crate Rust — aunque internamente pueda usar FFI hacia C/C++ para kernels CUDA o motores de almacenamiento columnares. El nivel L3 (Rust transitive completo hasta el metal) no es alcanzable en 2026 para los motores de inferencia GPU, y tampoco es el objetivo correcto. La prueba "We Own It" es una cuestión de licencias, no de lenguaje: `MIT + Apache-2.0 = lo poseemos`.

## Capas clave del stack

**Inferencia**: `mistral.rs` (MIT) — binario Rust enlazado estáticamente, con FlashAttention V2/V3, PagedAttention y carga en caliente de adaptadores LoRA por token. El modelo base de producción es la familia **OLMo 3**, el único modelo de pesos abiertos cuya totalidad — pesos, datos de entrenamiento y código — está bajo licencias permisivas (Apache 2.0 + Open Data Commons). Esta es la condición necesaria para la ruta de preentrenamiento continuo del [[apprenticeship-substrate]].

**HTTP y runtime**: `axum` + `tower` + `tokio` (todos MIT). Un único loop de eventos asíncrono atiende las peticiones entrantes del [[doorman-protocol|Doorman]] y despacha las llamadas salientes a Cloud Run GPU ([[yoyo-compute-substrate|Yo-Yo]]) y a las APIs externas.

**Almacenamiento y estado**: `sqlx` con SQLite para el ledger de auditoría de solo-lectura-apendizaje; LadybugDB via bindings Rust (en [[service-content]]) para el grafo de conocimiento; `object_store` (Apache-2.0) para pesos y adaptadores LoRA en almacenamiento en la nube.

**Procesamiento de documentos**: `oxidize-pdf` (Rust puro, cero dependencias C, 3.000–4.000 páginas/seg), `docx-rust`, `calamine` y `pulldown-cmark`. **mupdf-rs está explícitamente excluido** por su licencia AGPL-3.0, y la política `cargo-deny` en CI lo hace cumplir automáticamente en cada commit.

**Orquestación**: `apalis` (MIT) — procesamiento de trabajos con composición de pasos y middleware `tower`. Sin dependencias Python, sin bucles de mensajería externos. El modelo de trabajo de service-slm es: saneamiento → envío → espera → recepción → rehidratación. apalis encaja de forma nativa en ese modelo.

## Arquitectura plana: un binario, sin malla de servicios

El workspace Cargo produce un único binario: `slm-cli`. Los módulos lógicos se comunican mediante llamadas a funciones Rust, no mediante RPC. Las llamadas externas — a Cloud Run, al sidecar Mooncake, a las APIs externas permitidas, a LadybugDB — son los únicos límites de red.

Este es el perfil que requiere un componente de ToteboxOS: un proceso, un flujo de logs, un conjunto de métricas, un binario para firmar con Sigstore, un archivo de configuración.

## Integración con ToteboxOS

La arquitectura de binario único está motivada en parte por las restricciones de despliegue de ToteboxOS. Un stack CPython más un marco de inferencia GPU no cabe en el presupuesto de memoria disponible en hardware de appliance restringido. Un binario Rust con un runtime de inferencia cuantizado operando en modo CPU sí cabe.

Las restricciones relevantes según el perfil de hardware ToteboxOS Laptop-A (~550 MB de margen disponible tras los servicios centrales):

- Binario estático, sin arranque de intérprete — segundos, no minutos, hasta la primera inferencia
- Sin recolector de basura, sin heap de intérprete
- Paralelismo real entre núcleos sin bloqueo global de intérprete
- Compilación cruzada vía `cargo build --target aarch64-unknown-linux-gnu` para objetivos ARM de ToteboxOS

## Tres servicios externos que no son Rust

Tres servicios del sustrato de cómputo Yo-Yo se sitúan fuera del binario Rust, todos detrás de protocolos de red estables:

**LMCache + Mooncake Store** (plano de control en Python + Mooncake Transfer Engine en C++): el nivel de caché KV que persiste el estado de prefill a través de los reinicios de nodos GPU. service-slm mantiene un cliente Rust que se comunica con Mooncake vía HTTP y TCP. Sin acoplamiento FFI. Ambos tienen licencia Apache-2.0.

**vLLM** (Python): el motor de inferencia de prueba de la Fase 1. Reemplazado por mistral.rs en la Fase 2. Apache-2.0.

**SkyPilot** (Python): orquestación de GPU multi-nube. Se usa cuando Cloud Run GPU por sí solo resulta insuficiente. Apache-2.0.

Los tres están detrás de protocolos de red estables. service-slm depende del protocolo de comunicación, no de la implementación. Sustituir cualquiera de ellos requiere cambiar un único módulo cliente.

## Soberanía de licencias en producción

`cargo-deny` impone la política de licencias sobre el grafo completo de dependencias transitivas en cada ejecución de CI. Cualquier dependencia nueva que introduzca AGPL, GPL, LGPL, BSL o licencias comunitarias personalizadas falla la compilación de forma automática. La política está registrada en `deny.toml` en el repositorio y se revisa con cada adición de dependencia.

## Camino de apertura futura

Si en el futuro PointSav decidiera publicar `service-slm` como código abierto, la publicación sería mecánica: todas las dependencias ya son Apache-2.0 o MIT. La decisión de licencia para el código propio de PointSav se prevé Apache-2.0 (por la concesión explícita de patentes, ventajosa en mercados institucionales), con sign-off de Developer Certificate of Origin en lugar de CLA. No hay modificaciones técnicas necesarias en la base de código.

## Véase también

- [[compounding-doorman]] — el patrón operativo que service-slm implementa
- [[yoyo-compute-substrate]] — el substrato de cómputo multi-anillo que service-slm dirige
- [[apprenticeship-substrate]] — cómo el ledger de auditoría alimenta el entrenamiento de adaptadores LoRA
