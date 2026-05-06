---
schema: foundry-doc-v1
title: "Substrato de Cómputo Yo-Yo"
slug: yoyo-compute-substrate.es
category: architecture
type: topic
quality: published
short_description: "El substrato de cómputo de tres anillos que permite a service-slm activar y desactivar cómputo GPU mientras retiene estado, acumula habilidad y produce un ledger de auditoría de cada evento de inferencia."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: yoyo-compute-substrate.md
---

El Substrato de Cómputo Yo-Yo es la arquitectura mediante la cual `service-slm` gestiona la inferencia GPU a lo largo de ciclos de encendido y apagado. Un nodo GPU inactivo es costoso. Pero un nodo que descarta todo el estado al apagarse obliga a una recomputación completa en cada nuevo arranque — lenta, costosa e inviable a escala comercial. El substrato Yo-Yo resuelve esta tensión descomponiendo el estado de cómputo en tres anillos, cada uno con una estrategia de persistencia diferente.

El nombre es literal: el nivel de cómputo baja y vuelve a subir, repetidamente, sin perder lo que importa.

## Los tres anillos

**Anillo 1 — Bootstrap**: el estado necesario para arrancar el nodo en menos de treinta segundos sin coste de inactividad. Se logra pre-almacenando cuatro capas en almacenamiento frío de bajo coste: imagen de contenedor precompilada en un registro de artefactos regional, pesos del modelo en almacenamiento en la nube (evita descargas repetidas de decenas de gigabytes), instancias GPU de Cloud Run con drivers preinstalados (arranque en aproximadamente cinco segundos), y warm pool activado únicamente durante ventanas de carga sostenida predecibles — no de forma permanente.

El resultado es un arranque en caliente con peor caso de aproximadamente quince segundos, a coste de inactividad cero en operación normal.

**Anillo 2 — Memoria de trabajo (caché KV)**: el estado de prefill que sobrevive al apagado del nodo mediante LMCache y Mooncake Store. LMCache divide los tokens en bloques hash y los recupera desde una tienda escalonada: memoria GPU → DRAM CPU → almacenamiento en la nube. El campo `moduleId` del sobre RF2 aísla los bloques de caché por cliente: los bloques del Cliente A no colisionan nunca con los del Cliente B, aunque ambos compartan el mismo pool físico.

Para cargas de trabajo con estructura de prefijo repetido — cada documento procesado contra el mismo grafo de conocimiento comparte miles de tokens de contexto — las tasas de acierto de caché por encima del sesenta por ciento son alcanzables desde el segundo run completo del corpus. Esto se traduce directamente en reducción del coste de GPU.

**Anillo 3a — Memoria semántica a largo plazo**: el grafo de conocimiento en LadybugDB, dentro de `service-content`. `service-slm` lo lee en tiempo de ensamblado de contexto. Nunca escribe directamente en él; todas las escrituras fluyen a través de la ruta validada de aplicación de deltas. Este anillo es el registro autoritativo de cada proyecto; su alcance está delimitado por `moduleId`.

**Anillo 3b — Habilidad a largo plazo (adaptadores LoRA)**: la capa que hace compoundar el substrato. Cada proyecto nuevo deja tras de sí un adaptador LoRA afinado — un módulo pequeño y versionado que codifica comportamiento específico de la tarea (clasificación, resolución de entidades, detección de arquetipos, síntesis terminológica). Los adaptadores se almacenan como OCI Artifacts firmados con Sigstore y se activan en el arranque del motor de inferencia.

La arquitectura distingue entre **adaptadores compartidos** (prefijo `dka-*`) que acumulan habilidad general entre proyectos, y **adaptadores por proyecto** (`{cliente}-*`) que retienen conocimiento específico del cliente. Los primeros mejoran con cada proyecto; los segundos permanecen con su propietario.

**Este es el activo que compone.** El modelo base es una materia prima accesible para cualquier despliegue en la industria. La biblioteca de adaptadores es específica del historial operativo del operador. Crece con cada proyecto. No se puede adquirir de un tercero.

## El ledger de auditoría

Cada evento Yo-Yo — arranque, trabajo, apagado, precarga de adaptador, sincronización de caché — se registra en un CSV de solo-apendizaje. El esquema incluye identificador de evento, `moduleId`, versiones de adaptadores activos, tasa de acierto de caché KV, tokens procesados, segundos GPU consumidos, coste estimado, estado de finalización e identidad del operador.

Este ledger vincula cada output — cada página generada, cada registro exportado, cada análisis producido — con el evento de cómputo exacto, las versiones exactas de adaptadores y el material fuente exacto que lo produjo. Es un artefacto de integridad de procesamiento que los servicios de inferencia gestionados no pueden producir, porque operan en una capa por encima de los eventos que el ledger Yo-Yo captura.

## Hoja de ruta (planificada)

La Fase 1 (actual) construye completamente el Anillo 1 y el ledger. Los Anillos 2 y 3b están intencionalmente diferidos hasta que el ensayo de arquitectura complete su validación. La Fase 2 (planificada) añade LMCache y Mooncake Store, con objetivo de sesenta por ciento de tasa de acierto de caché en el segundo run completo. La Fase 3 (planificada) introduce los primeros adaptadores LoRA y el pipeline de entrenamiento. La Fase 4 (prevista a largo plazo) incorporará mejoras en checkpoint/restore de GPU y gestión de adaptadores a escala multi-proyecto.

## Véase también

- [[compounding-doorman]] — el patrón del Doorman que service-slm implementa; el substrato Yo-Yo es su ruta de cómputo Tier B
- [[slm-stack-architecture]] — el grafo de dependencias Rust y la arquitectura binaria de service-slm
- [[apprenticeship-substrate]] — cómo el ledger de auditoría Yo-Yo genera señal de entrenamiento para adaptadores LoRA

---

## Provenance

Fuente: `YOYO-COMPUTE.md` (workspace, v1, 2026-04-20). Adaptación estratégica al español: resumen orientado a comprensión arquitectónica; no traducción literal. Correcciones de nomenclatura aplicadas: `cognitive-forge` → `service-slm` / Doorman; `Data Vault` → `service-content` / grafo de conocimiento; `phi3-mini` → OLMo 3; `ArchiveOS` → ToteboxOS. Posicionamiento estructural: análisis estructural del mercado retenido sin nombrar plataformas competidoras por contraste.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™ y Totebox Archive™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos titulares.*
