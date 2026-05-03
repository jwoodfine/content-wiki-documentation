---
schema: foundry-doc-v1
title: "Arquitectura del Stack Rust de service-slm"
slug: slm-stack-architecture.es
category: architecture
type: topic
quality: published
short_description: "Visión estratégica del stack Rust de service-slm: un binario único, licencias permisivas de extremo a extremo, y la disciplina de construcción que mantiene la soberanía técnica sobre cada dependencia."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: slm-stack-architecture.md
---

`service-slm` — el Doorman de la plataforma PointSav — se construye como un único binario de Rust enlazado estáticamente. Cada dependencia directa en el stack es Rust puro o bindings Rust sobre una biblioteca nativa con licencia permisiva. No hay licencias copyleft en ningún punto del grafo de dependencias. Esta propiedad, denominada criterio "We Own It", garantiza que PointSav conserva el derecho irrestricto de bifurcar, modificar y redistribuir la totalidad del código base en cualquier momento.

## Por qué importa la elección de Rust

La elección no es una preferencia de lenguaje. Es una restricción de ingeniería impuesta por el destino de despliegue previsto: hardware ToteboxOS, donde un intérprete CPython más un marco de ML de gran tamaño no caben en el presupuesto de memoria disponible. La ausencia de recolector de basura, el arranque predecible y el paralelismo real sobre múltiples núcleos sin bloqueo global de intérprete son requisitos operativos, no mejoras opcionales.

El objetivo técnico es lo que la industria denomina "Rust de nivel L2": todo el código escrito por PointSav es Rust, y cada crate de dependencia directa es un crate Rust — aunque internamente pueda usar FFI hacia C/C++ para kernels CUDA o motores de almacenamiento columnares. El nivel L3 (Rust transitive completo hasta el metal) no es alcanzable en 2026 para los motores de inferencia GPU, y tampoco es el objetivo correcto. La prueba "We Own It" es una cuestión de licencias, no de lenguaje: `MIT + Apache-2.0 = lo poseemos`.

## Capas clave del stack

**Inferencia**: `mistral.rs` (MIT) — binario Rust enlazado estáticamente, con FlashAttention V2/V3, PagedAttention y carga en caliente de adaptadores LoRA por token. El modelo base de producción es la familia **OLMo 3**, el único modelo de pesos abiertos cuya totalidad — pesos, datos de entrenamiento y código — está bajo licencias permisivas (Apache 2.0 + Open Data Commons). Esta es la condición necesaria para la ruta de preentrenamiento continuo del [[apprenticeship-substrate]].

**HTTP y runtime**: `axum` + `tower` + `tokio` (todos MIT). Un único loop de eventos asíncrono atiende las peticiones entrantes del Doorman y despacha las llamadas salientes a Cloud Run GPU y a las APIs externas.

**Almacenamiento y estado**: `sqlx` con SQLite para el ledger de auditoría de solo-lectura-apendizaje; LadybugDB via bindings Rust para el grafo de conocimiento; `object_store` (Apache-2.0) para pesos y adaptadores LoRA en almacenamiento en la nube.

**Procesamiento de documentos**: `oxidize-pdf` (Rust puro, cero dependencias C, 3.000–4.000 páginas/seg), `docx-rust`, `calamine` y `pulldown-cmark`. **mupdf-rs está explícitamente excluido** por su licencia AGPL-3.0, y la política `cargo-deny` en CI lo hace cumplir automáticamente en cada commit.

**Orquestación**: `apalis` (MIT) — procesamiento de trabajos con composición de pasos y middleware `tower`. Sin dependencias Python, sin bucles de mensajería externos. El modelo de trabajo de service-slm es: saneamiento → envío → espera → recepción → rehidratación. apalis encaja de forma nativa en ese modelo.

## Arquitectura plana: un binario, sin malla de servicios

El workspace Cargo produce un único binario: `slm-cli`. Los módulos lógicos se comunican mediante llamadas a funciones Rust, no mediante RPC. Las llamadas externas — a Cloud Run, al sidecar Mooncake, a las APIs externas permitidas, a LadybugDB — son los únicos límites de red.

Este es el perfil que requiere un componente de ToteboxOS: un proceso, un flujo de logs, un conjunto de métricas, un binario para firmar con Sigstore, un archivo de configuración.

## Soberanía de licencias en producción

`cargo-deny` impone la política de licencias sobre el grafo completo de dependencias transitivas en cada ejecución de CI. Cualquier dependencia nueva que introduzca AGPL, GPL, LGPL, BSL o licencias comunitarias personalizadas falla la compilación de forma automática. La política está registrada en `deny.toml` en el repositorio y se revisa con cada adición de dependencia.

## Camino de apertura futura

Si en el futuro PointSav decidiera publicar `service-slm` como código abierto, la publicación sería mecánica: todas las dependencias ya son Apache-2.0 o MIT. La decisión de licencia para el código propio de PointSav se prevé Apache-2.0 (por la concesión explícita de patentes, ventajosa en mercados institucionales), con sign-off de Developer Certificate of Origin en lugar de CLA. No hay modificaciones técnicas necesarias en la base de código.

## Véase también

- [[compounding-doorman]] — el patrón operativo que service-slm implementa
- [[yoyo-compute-substrate]] — el substrato de cómputo multi-anillo que service-slm dirige
- [[apprenticeship-substrate]] — cómo el ledger de auditoría alimenta el entrenamiento de adaptadores LoRA

---

## Provenance

Fuente: `SLM-STACK.md` (workspace, v1, 2026-04-20). Adaptación estratégica al español: resumen orientado a comprensión arquitectónica; no traducción literal. Correcciones de nomenclatura aplicadas: `phi3-mini` → OLMo 3; `ArchiveOS` → ToteboxOS. Posicionamiento estructural: ningún proveedor externo mencionado por contraste competitivo.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
