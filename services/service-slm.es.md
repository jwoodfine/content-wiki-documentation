---
schema: foundry-doc-v1
title: "Modelo de lenguaje pequeño institucional"
slug: service-slm
category: services
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-22
editor: pointsav-engineering
paired_with: service-slm.md
short_description: "service-slm es el servicio de modelo de lenguaje de la familia PointSav — un Modelo de Lenguaje Pequeño cuantizado y estrecho que traduce la intención institucional en salidas deterministas y enruta cada llamada de inferencia de IA a través del límite de auditoría del Portero."
cites:
 - olmo3-allenai
references:
 - id: 1
 text: "ISO/IEC 42001:2023 — Tecnología de la información — Inteligencia artificial — Sistema de gestión."
 url: "https://www.iso.org/standard/81230.html"
 - id: 2
 text: "Groeneveld, D. et al. 'OLMo: Accelerating the Science of Language Models.' arXiv:2402.00838, 2024."
 url: "https://arxiv.org/abs/2402.00838"
---

Una solicitud de IA que sale del edificio no puede auditarse ni revocarse. En el momento en que la intención institucional llega a un modelo de frontera en la nube de otra empresa, la organización ha cedido tanto el registro de la decisión como el control sobre ella.

<!--claim id=small-by-design confidence=structural cites=[]-->`service-slm` es el servicio de modelo de lenguaje de la familia PointSav. Es deliberadamente un Modelo de Lenguaje Pequeño — cuantizado, estrecho, rápido — y su trabajo no es la conversación sino la traducción semántica: convertir la intención institucional en salidas deterministas.<!--/claim-->

<!--claim id=doorman-transit confidence=structural cites=[]-->El servicio se ejecuta en tres niveles de cómputo. Cada llamada de inferencia — local, de ráfaga o externa — transita el límite de auditoría del [[doorman-protocol|Portero]], donde cada prompt y cada respuesta se capturan en el [[worm-ledger-design|libro mayor]] por inquilino antes de que la respuesta regrese.<!--/claim-->

Para un comprador regulado la consecuencia es concreta. Ninguna decisión de IA queda sin registrar, y ninguna solicitud llega a una API de terceros sin cruzar un límite que el operador controla. Este artículo cubre las cuatro operaciones, los tres niveles de cómputo, el límite del Portero y por qué un modelo pequeño es una elección estructural y no un compromiso de costo.

## Qué hace service-slm

El servicio es invisible — no hay ventana de chat, y el operador nunca escribe directamente en `service-slm`. La superficie por encima de él presenta un flujo de trabajo estructurado; `service-slm` es el intermediario silencioso. Realiza cuatro operaciones, en orden de peso institucional creciente.

| Operación | Entradas | Salida |
|---|---|---|
| Análisis de comandos semánticos | Intención en inglés desde el Terminal F8 | Comando UDP binario para `service-udp` |
| Verificación de gravedad | Vector de Gravedad de 50 palabras de [[service-content]] | Token único `VALID` o `REJECT` |
| Asignación de enchufe | Paquete de entidades de [[service-extraction]] + [[archetypes-and-chart-of-accounts|Plan de Cuentas]] | Sovereign-ID con enchufe del Plan de Cuentas |
| Sugerencia de temas | Patrones recurrentes que señala el Motor de Gravedad | Entradas propuestas a la Bóveda de Semillas de Temas, para aprobación del operador |

<!--claim id=no-autonomous-publish confidence=structural cites=[]-->El modelo nunca publica datos estructurados de forma autónoma. Cada salida transita un paso de verificación con intervención humana antes de poder escribirse en un libro mayor verificado.<!--/claim-->

## Los tres niveles de cómputo

La misma interfaz de `service-slm` se adapta al hardware del anfitrión a través de tres modos de ejecución.

| Nivel | Dónde se ejecuta | Tamaño del modelo | Caso de uso |
|---|---|---|---|
| Local | Estación de trabajo del operador u [[totebox-os|`os-totebox`]] con al menos 16 GB de RAM | Modelo cuantizado de 1B–7B parámetros cargado localmente | Bóveda de Hierro Soberano — clientes institucionales; sin egreso a la nube |
| Ráfaga elástica | Nodo GPU efímero aprovisionado por el operador | Modelo más grande en hardware arrendado; datos tunelizados por un enlace cifrado | Procesamiento por lotes pesado optimizado en costo; el nodo se desmonta tras la ejecución |
| API externa | Endpoint de API de terceros con licencia | Modelo de frontera | Enrutamiento de último recurso para tareas donde la capacidad local es insuficiente |

<!--claim id=no-tier-bypass confidence=structural cites=[]-->Los tres niveles transitan el límite de auditoría del Portero. Ningún nivel lo elude.<!--/claim-->

## El límite del Portero

El Portero es el punto de control de auditoría y enrutamiento entre `service-slm` y el resto del sistema. Cada prompt y cada respuesta se capturan antes de que la respuesta regrese al solicitante. El registro de auditoría vive en el libro mayor local por inquilino y forma el registro institucional de cada decisión de IA.

El Portero existe por tres razones.

1. **Regulatoria.** ISO/IEC 42001, el estándar de sistema de gestión de IA [^1], exige un registro inmutable de las decisiones asistidas por IA.
2. **Operativa.** Un sistema auto-reparable necesita un corpus de su propio comportamiento pasado; el Portero lo captura.
3. **Soberana.** Ninguna solicitud llega a una API de terceros sin pasar por un límite local que controla el operador.

## Selección del modelo

<!--claim id=olmo-canonical cites=[olmo3-allenai] confidence=established-->El modelo local canónico es de la familia OLMo, que se distribuye con pesos completamente abiertos y documentación de los datos de entrenamiento [^2].<!--/claim--> Los pesos abiertos y los datos documentados son un prerrequisito para el preentrenamiento continuo sobre el corpus propio del operador — el camino a largo plazo hacia un modelo institucional especializado en el dominio.

| Perfil | Modelo | RAM objetivo |
|---|---|---|
| Edge | OLMo-2-0425-1B-Instruct | ~2 GB |
| Standard | OLMo-3-1125-7B-Think-Q4_K_M | ~6 GB |

## Por qué un modelo pequeño

<!--claim id=small-model-rationale confidence=structural cites=[]-->Un modelo de escala de frontera impone tres costos que `service-slm` no puede aceptar: exige egreso a la nube, consume decenas de gigabytes de RAM y no puede auditarse de ninguna manera significativa. Un modelo cuantizado de 1B parámetros es suficiente para la única tarea estrecha — traducir el inglés institucional en salidas deterministas — y encaja dentro del presupuesto de un nodo en la nube de bajo costo junto con un Totebox.<!--/claim-->

La especialización, no la escala, es el principio de diseño.

## Véase también

- [[service-content]] — el Motor de Gravedad ascendente; principal solicitante de service-slm para la verificación de gravedad
- [[os-network-admin]] — el Terminal F8 donde se origina el análisis de comandos semánticos
- [[totebox-os]] — el Totebox que aloja service-slm en modo Hierro Soberano
- [[architecture-decisions|SYS-ADR-07]] — los datos estructurados nunca se enrutan a través de IA; service-slm implementa este límite
- [[doorman-protocol]] — el protocolo de auditoría y enrutamiento del Portero en detalle
