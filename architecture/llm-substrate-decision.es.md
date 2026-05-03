---
schema: foundry-doc-v1
title: "Decisión de Sustrato LLM — Familia OLMo 3"
slug: llm-substrate-decision.es
category: architecture
type: topic
quality: published
short_description: "La justificación para seleccionar OLMo 3 como sustrato de inferencia local y en GPU: la única familia de modelos completamente abierta — datos, código de entrenamiento y puntos de control incluidos — que permite el preentrenamiento continuo y satisface la postura de adquisición de una empresa pública canadiense."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: llm-substrate-decision.md
---

La plataforma PointSav utiliza la familia de modelos OLMo 3 como sustrato de inferencia de lenguaje. OLMo 3 7B se ejecuta localmente en el hardware del cliente. OLMo 3.1 32B Think se ejecuta en instancias de GPU bajo demanda para tareas de inferencia más exigentes. La selección no responde principalmente al desempeño en benchmarks, sino a la profundidad de propiedad que cada modelo permite.

## Los tres niveles de apertura

El mercado de modelos de lenguaje en 2026 ofrece tres niveles distintos de apertura, y la diferencia es crítica para cualquier organización que planifique una trayectoria de composición a cinco años.

**Nivel 1 — Pesos abiertos.** Se publican los archivos de parámetros entrenados. Es posible ejecutar inferencia y ajuste fino LoRA, pero no se pueden inspeccionar los datos de entrenamiento ni continuar el preentrenamiento desde un punto de control conocido.

**Nivel 2 — Pesos abiertos con licencia permisiva.** Igual que el Nivel 1, con una licencia suficientemente permisiva para incluir el modelo en un producto comercial sin exposición legal.

**Nivel 3 — Modelo completamente abierto.** Se publican los datos de entrenamiento, el código de entrenamiento y los puntos de control en cada etapa, junto con los pesos y una licencia permisiva. A este nivel es posible continuar el preentrenamiento: partiendo de un punto de control conocido, sobre un corpus propio, para producir un modelo derivado que la organización posee de forma efectiva.

OLMo 3 es el único modelo en el panorama abierto no chino de 2026 que opera en el Nivel 3. Sus datos de entrenamiento son el corpus Dolma 3 (9.3 billones de tokens, publicado bajo Open Data Commons). Su código de entrenamiento es Apache 2.0. Los puntos de control intermedios están disponibles públicamente.

## Por qué se descartaron las alternativas

Los modelos de origen chino — independientemente de su calidad técnica y sus licencias permisivas — fueron descartados por las restricciones de adquisición aplicables a una empresa pública canadiense, derivadas del precedente legislativo estadounidense de 2026 sobre infraestructuras de IA de origen chino.

Los modelos Phi-4, Granite 4 y otros con licencias permisivas fueron descartados porque sus datos de entrenamiento son cerrados y de propiedad del fabricante: permiten ajuste fino LoRA pero no preentrenamiento continuo, por lo que no habilitan el camino hacia un modelo base propio.

## Las tres capas de cómputo

El Doorman enruta las solicitudes entre tres capas:

- **Capa A — local:** OLMo 3 7B en el hardware del cliente. Costo marginal aproximadamente cero.
- **Capa B — ráfaga GPU:** OLMo 3.1 32B Think en instancias de GPU de corta duración. Utilizado para razonamiento extendido. Disciplina de apagado inactivo por defecto.
- **Capa C — API externa:** servicios de terceros bajo lista de permitidos explícita, registrados en el libro de auditoría del cliente.

## Trayectoria de preentrenamiento continuo (planificada)

La trayectoria prevista para la plataforma contempla, a partir del segundo año, el inicio del preentrenamiento continuo del modelo base OLMo 3 7B sobre el corpus acumulado de Foundry, con el objetivo de producir PointSav-OLMo-N — un modelo derivado que incorpora los patrones de uso reales de los clientes. Esta trayectoria es una intención declarada y está sujeta a las condiciones técnicas y económicas del momento.

## Ver también

- [[four-tier-slm-substrate]] — los cuatro niveles de despliegue construidos sobre este sustrato
- [[compounding-doorman]] — el servicio que enruta todas las llamadas de inferencia

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
