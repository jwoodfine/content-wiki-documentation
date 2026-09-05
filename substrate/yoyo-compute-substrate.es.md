---
schema: foundry-doc-v1
title: "Substrato de Cómputo Yo-Yo"
slug: yoyo-compute-substrate
category: substrate
type: topic
content_type: topic
quality: complete
index_group: small-language-model-stack
short_description: "El substrato de cómputo de tres anillos que permite a service-slm activar y desactivar cómputo GPU mientras retiene estado, acumula habilidad y produce un ledger de auditoría de cada evento de inferencia."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Open Source Security Foundation. 'SLSA: Supply chain Levels for Software Artifacts v1.0.' SLSA.dev, 2023."
    url: "https://slsa.dev/spec/v1.0/"
paired_with: yoyo-compute-substrate.md
---

El Substrato de Cómputo Yo-Yo es la arquitectura mediante la cual [[service-slm]] gestiona la inferencia GPU a lo largo de ciclos de encendido y apagado. Un nodo GPU inactivo es costoso. Pero un nodo que descarta todo el estado al apagarse obliga a una recomputación completa en cada nuevo arranque — lenta, costosa e inviable a escala comercial. El substrato Yo-Yo resuelve esta tensión descomponiendo el estado de cómputo en tres anillos, cada uno con una estrategia de persistencia diferente.

El nombre es literal: el nivel de cómputo baja y vuelve a subir, repetidamente, sin perder lo que importa.

## Los tres anillos

**Anillo 1 — Bootstrap**: el nodo Yo-Yo #1 real es una VM de GCE convencional (`google_compute_instance`) con GPU L4, activada según una programación (`google_compute_resource_policy`) para la ventana de entrenamiento nocturna — no un servicio Cloud Run que escala a cero entre solicitudes. El arranque real espera hasta noventa minutos a que el servidor de inferencia señale que está listo, no los segundos que sugeriría un arranque serverless. El patrón de carga de trabajo que este anillo realmente sirve es trabajo por lotes programado, no ráfagas oportunistas de sub-segundo en tiempo de consulta. Los pesos del modelo se mantienen en un disco persistente (`google_compute_disk`) en lugar de descargarse en cada ciclo, lo que sí evita descargas repetidas de decenas de gigabytes desde el repositorio de modelos de origen en cada ciclo nocturno.

El checkpoint/restore de CUDA, la migración de adaptador único enrutado y las demás primitivas prospectivas descritas más adelante en este artículo siguen siendo direcciones de investigación genuinamente planificadas, independientes de esta corrección — el ajuste de esta sección trata sobre qué producto de GCP ejecuta realmente el Anillo 1 y cuánto dura su arranque real, no sobre si vale la pena perseguir esas primitivas.

**Anillo 2 — Memoria de trabajo (caché KV)**: el estado de prefill que sobrevive al apagado del nodo mediante LMCache y Mooncake Store. LMCache divide los tokens en bloques hash y los recupera desde una tienda escalonada: memoria GPU → DRAM CPU → almacenamiento en la nube. El campo `moduleId` del sobre RF2 aísla los bloques de caché por cliente: los bloques del Cliente A no colisionan nunca con los del Cliente B, aunque ambos compartan el mismo pool físico.

Para cargas de trabajo con estructura de prefijo repetido — cada documento procesado contra el mismo grafo de conocimiento comparte miles de tokens de contexto — las tasas de acierto de caché por encima del sesenta por ciento son alcanzables desde el segundo run completo del corpus. Esto se traduce directamente en reducción del coste de GPU.

**Anillo 3a — Memoria semántica a largo plazo**: el grafo de conocimiento en LadybugDB, dentro de [[service-content]]. `service-slm` lo lee en tiempo de ensamblado de contexto. Nunca escribe directamente en él; todas las escrituras fluyen a través del pipeline de propuesta con verificación humana documentado en otra parte de esta wiki, no un ciclo automatizado dentro del propio `service-slm`.

El Anillo 3a está delimitado por proyecto, por diseño. La partición del grafo de un inquilino es inaccesible para otro sin una exportación explícita a través del canal de datos autorizado. Este es el comportamiento correcto para los datos. Es el comportamiento incorrecto para la habilidad — por eso existe el Anillo 3b como una capa separada.

**Anillo 3b — Habilidad a largo plazo (adaptadores LoRA)**: la capa que hace compoundar el substrato. Cada proyecto nuevo deja tras de sí un [[adapter-composition|adaptador LoRA]] afinado — un módulo pequeño y versionado que codifica comportamiento específico de la tarea (clasificación, resolución de entidades, detección de arquetipos, síntesis terminológica). Los adaptadores se almacenan como OCI Artifacts firmados con Sigstore y se activan en el arranque del motor de inferencia. [^1]

La arquitectura distingue entre **adaptadores compartidos** (prefijo `dka-*`) que acumulan habilidad general entre proyectos, y **adaptadores por proyecto** (`{cliente}-*`) que retienen conocimiento específico del cliente. Los primeros mejoran con cada proyecto; los segundos permanecen con su propietario.

**Este es el activo que compone.** El modelo base es una materia prima accesible para cualquier despliegue en la industria. La biblioteca de adaptadores es específica del historial operativo del operador. Crece con cada proyecto. No se puede adquirir de un tercero.

## El ledger de auditoría

Cada evento Yo-Yo — arranque, trabajo, apagado, precarga de adaptador, sincronización de caché — se registra en un CSV de solo-apendizaje. El esquema incluye identificador de evento, `moduleId`, versiones de adaptadores activos, tasa de acierto de caché KV, tokens procesados, segundos GPU consumidos, coste estimado, estado de finalización e identidad del operador.

Este [[worm-ledger-architecture|ledger]] vincula cada output — cada página generada, cada registro exportado, cada análisis producido — con el evento de cómputo exacto, las versiones exactas de adaptadores y el material fuente exacto que lo produjo. Es un artefacto de integridad de procesamiento que los servicios de inferencia gestionados no pueden producir, porque operan en una capa por encima de los eventos que el ledger Yo-Yo captura.

## La disciplina de `moduleId`

El sobre RF2 ya lleva un campo `moduleId` en cada mensaje. El substrato Yo-Yo extiende su alcance hacia el cómputo:

- **Anillo 1**: selecciona la variante de contenedor a arrancar (rara vez varía por proyecto)
- **Anillo 2**: aísla los hashes de bloque de Mooncake (el Proyecto A y el Proyecto B comparten un pool; nunca comparten bloques de caché)
- **Anillo 3a**: delimita el recorrido del grafo LadybugDB a la partición correcta
- **Anillo 3b**: selecciona la pila de adaptadores LoRA a activar — la [[four-tier-slm-substrate|selección de nivel]] propaga `moduleId` hacia cada carga de adaptador
- **Ledger**: etiqueta cada entrada para la contabilidad de costos por proyecto

Un solo campo, cinco funciones. La propiedad de aislamiento multi-inquilino no fue una idea posterior; es una consecuencia estructural de que `moduleId` se propaga por cada anillo.

## Horizonte 2030

El substrato está diseñado para que las primitivas de investigación que están planificadas o en etapa de RFC en 2026 puedan integrarse sin cambio arquitectónico:

| Primitiva | Estado (2026) | Punto de integración |
|---|---|---|
| Checkpoint/restore de CUDA | Etapa de RFC; ganancia de diez veces en arranque en frío demostrada en entornos controlados | Anillo 1: entrada opcional de paquete de checkpoint |
| Adaptador único enrutado (C-LoRA) | Publicado en 2025 | Anillo 3b: migración del esquema del registro |
| Pool de KV multi-nube | Dirección de investigación de largo horizonte; no existe capa de orquestación para ello en el despliegue actual | Anillo 2: maestro de Mooncake en pool multi-nube |
| Cuantización FP8 de la caché KV | Disponible como bandera de configuración del motor de inferencia | Anillo 2: bandera de configuración, reducción de memoria de aproximadamente el doble |
| Reentrenamiento de adaptador en tiempo de reposo | Etapa de investigación | Anillo 3b: reentrenamiento por lotes nocturno en cómputo de costo reducido |

Cada una de estas puede integrarse como una adición de configuración o un nuevo subdirectorio. Ninguna requiere reescribir `service-slm`.

## Hoja de ruta (planificada)

La Fase 1 (actual) construye completamente el Anillo 1 (como VM de GCE programada, no como el diseño de Cloud Run descrito antes) y el ledger. Los Anillos 2 y 3b están intencionalmente diferidos hasta que el ensayo de arquitectura complete su validación. El nivel Yo-Yo está actualmente inactivo según el [[service-slm-yoyo-operational|artículo de estado operativo]] de esta wiki — conviene verificarlo antes de asumir que la Fase 1 sirve tráfico en vivo. La Fase 2 (planificada) añade LMCache y Mooncake Store, con objetivo de sesenta por ciento de tasa de acierto de caché en el segundo run completo. La Fase 3 (planificada) introduce los primeros adaptadores LoRA y el pipeline de entrenamiento. La Fase 4 (prevista a largo plazo) incorporará mejoras en checkpoint/restore de GPU y gestión de adaptadores a escala multi-proyecto.

## Véase también

- [[compounding-doorman]] — el patrón del Doorman que service-slm implementa; el substrato Yo-Yo es su ruta de cómputo Tier B
- [[slm-stack-architecture]] — el grafo de dependencias Rust y la arquitectura binaria de service-slm
- [[apprenticeship-substrate]] — cómo el ledger de auditoría Yo-Yo genera señal de entrenamiento para adaptadores LoRA
