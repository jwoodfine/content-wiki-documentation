---
schema: foundry-doc-v1
title: "service-slm — El Modelo de Lenguaje Pequeño Institucional"
slug: service-slm
category: services
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: service-slm.md
short_description: "service-slm es el servicio de modelo de lenguaje de la familia PointSav — un Modelo de Lenguaje Pequeño cuantizado y estrecho que traduce la intención institucional en salidas deterministas y enruta cada llamada de inferencia de IA a través del límite de auditoría del Portero."
cites: []
references:
  - id: 1
    text: "ISO/IEC 42001:2023 — Tecnología de la información — Inteligencia artificial — Sistema de gestión."
    url: "https://www.iso.org/standard/81230.html"
  - id: 2
    text: "Groeneveld, D. et al. 'OLMo: Accelerating the Science of Language Models.' arXiv:2402.00838, 2024."
    url: "https://arxiv.org/abs/2402.00838"
---

`service-slm` es el servicio de modelo de lenguaje de la familia PointSav. Es intencionalmente un Modelo de Lenguaje Pequeño — cuantizado, estrecho, rápido — en lugar de un modelo de escala de frontera. Su trabajo no es la conversación. Su trabajo es la traducción semántica: convertir la intención institucional (comandos en inglés, contenido de documentos, consultas de taxonomía) en salidas deterministas (comandos binarios, decisiones `VALID`/`REJECT`, asignaciones de enchufe del Plan de Cuentas). Es invisible — no hay ventana de chat, y el operador nunca escribe directamente en `service-slm`. La superficie por encima de él presenta un flujo de trabajo estructurado; `service-slm` es el intermediario silencioso. Este artículo cubre las cuatro operaciones, los tres niveles de cómputo, el límite de auditoría del Portero y por qué un modelo pequeño es una elección estructural, no un compromiso de costo.

## Qué hace service-slm

El servicio realiza cuatro operaciones en orden de peso institucional creciente:

| Operación | Entradas | Salida |
|---|---|---|
| Análisis de comandos semánticos | Intención en inglés desde el Terminal F8 | Comando UDP binario para `service-udp` |
| Verificación de gravedad | Vector de Gravedad de 50 palabras de `service-content` | Token único `VALID` o `REJECT` |
| Asignación de enchufe | Paquete de entidades de `service-extraction` + Plan de Cuentas | Sovereign-ID con enchufe del Plan de Cuentas |
| Sugerencia de temas | Patrones recurrentes que señala el Motor de Gravedad | Entradas propuestas a la Bóveda de Semillas de Temas (para aprobación del operador) |

El modelo nunca publica datos estructurados de forma autónoma. Cada salida transita un paso de verificación con intervención humana antes de que pueda escribirse en un libro mayor verificado.

## Los tres niveles de cómputo

La misma interfaz de `service-slm` se adapta al hardware del anfitrión a través de tres modos de ejecución:

| Nivel | Dónde se ejecuta | Tamaño del modelo | Caso de uso |
|---|---|---|---|
| Local | Estación de trabajo del operador o `os-totebox` con ≥16 GB RAM | Modelo cuantizado de 1B–7B parámetros cargado localmente | Bóveda de Hierro Soberano — clientes institucionales; sin egreso a la nube |
| Yo-Yo | Nodo GPU elástico aprovisionado por el operador | Modelo más grande en hardware arrendado; datos tunelizados via WireGuard | Procesamiento por lotes pesado optimizado en costo; el nodo se desmonta después de la ejecución |
| API Externa | Endpoint de API de terceros con licencia | Modelo de frontera | Enrutamiento de último recurso para tareas donde la capacidad local es insuficiente |

Los tres niveles transitan el límite de auditoría del Portero. Ningún nivel lo elude.

## El límite del Portero

El Portero es el punto de control de auditoría y enrutamiento entre `service-slm` y el resto del sistema. Cada prompt y cada respuesta son capturados antes de que la respuesta regrese al solicitante. El registro de auditoría vive en el libro mayor local por inquilino y forma el registro institucional de cada decisión de IA.

El Portero existe por tres razones:

1. **Regulatoria.** ISO/IEC 42001 (Sistema de Gestión de IA) [^1] requiere un registro inmutable de decisiones asistidas por IA.
2. **Operativa.** Un sistema auto-reparable necesita un corpus de su propio comportamiento pasado. El Portero lo captura.
3. **Soberana.** Ninguna solicitud llega a una API de terceros sin pasar por un límite local que controla el operador.

## Selección del modelo

El modelo local canónico es de la familia OLMo (Apache 2.0 + Open Data Commons) [^2]. Hay dos perfiles disponibles:

| Perfil | Modelo | RAM objetivo |
|---|---|---|
| Edge | OLMo-2-0425-1B-Instruct | ~2 GB |
| Standard | OLMo-3-1125-7B-Think-Q4_K_M | ~6 GB |

OLMo es preferido porque se distribuye con pesos completamente abiertos y documentación de datos de entrenamiento — un prerrequisito para el pre-entrenamiento continuo en el corpus propio del operador, que es el camino a largo plazo hacia un modelo institucional especializado en el dominio.

## Por qué un modelo pequeño

Los modelos de escala de frontera imponen tres costos que `service-slm` no puede aceptar: requieren egreso a la nube, consumen decenas de gigabytes de RAM y no pueden auditarse de ninguna manera significativa. Un modelo cuantizado de 1B parámetros es suficiente para su única tarea estrecha — traducir el inglés institucional en salidas deterministas — y encaja dentro del presupuesto de un nodo en la nube de $7 junto con un Totebox.

La especialización, no la escala, es el principio de diseño.

## Véase también

- [[service-content]] — el Motor de Gravedad ascendente; principal solicitante de service-slm para la verificación de gravedad
- [[os-network-admin]] — el Terminal F8 donde se origina el análisis de comandos semánticos
- [[totebox-os]] — el Totebox que aloja service-slm en modo Hierro Soberano
- [[sys-adr-07]] — los datos estructurados nunca se enrutan a través de IA; service-slm es la implementación de este límite
- [[doorman-protocol]] — el protocolo de auditoría y enrutamiento del Portero en detalle
