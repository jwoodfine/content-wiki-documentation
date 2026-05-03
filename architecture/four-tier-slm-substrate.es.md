---
schema: foundry-doc-v1
title: "La Escalera de Cuatro Niveles del Sustrato SLM"
slug: four-tier-slm-substrate.es
category: architecture
type: topic
quality: published
short_description: "Un camino gradual hacia la soberanía en IA: cuatro niveles de despliegue para el cliente, desde una pasarela de API sin modelo local hasta un servicio de IA especializado entrenado sobre el corpus agregado del proveedor, donde cada nivel añade capacidad sin romper la garantía del nivel inferior."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: four-tier-slm-substrate.md
---

La plataforma PointSav estructura el despliegue de IA como una escalera de cuatro niveles. Los clientes comienzan en el nivel que corresponde a su hardware, presupuesto y requisitos de soberanía actuales. Cada nivel superior añade capacidad; rebajar a un nivel inferior en cualquier momento no rompe el sustrato que el cliente ya opera.

## Nivel 0 — Miembro Community, sin modelo local

En el Nivel 0, el Doorman opera como pasarela de API pura. Ningún modelo de lenguaje se ejecuta localmente. El Doorman mantiene las claves del cliente para el servicio externo que haya configurado, enruta las solicitudes a través de una lista de permisos por propósito y registra cada llamada en el libro de auditoría local.

Los servicios de los anillos 1 y 2 — todo el procesamiento determinista de conocimiento — funcionan completamente sin inteligencia artificial en el anillo 3. La inteligencia es opcional.

## Nivel 1 — OLMo 7B local más acceso a API externa

En el Nivel 1 el cliente ejecuta OLMo 3 7B Think localmente. El Doorman enruta la mayoría de las solicitudes al modelo local en la Capa A; las solicitudes más exigentes se dirigen a servicios externos de Capa C cuando están configurados, o al modelo de 32B alojado por el proveedor si el cliente ha suscrito el Nivel 2.

El entrenamiento de adaptadores LoRA por inquilino está disponible desde el Nivel 1. Un primer adaptador puede entrenarse con un corpus de aproximadamente 1,000 a 5,000 pares de preferencias de alta calidad extraídos del historial operativo propio del cliente. Ese adaptador permanece en la instancia ToteboxOS del cliente y no sale de ella a menos que el cliente opte explícitamente por el mercado federado.

## Nivel 2 — Modelo de 32B alojado por el proveedor (Yo-Yo)

En el Nivel 2 el proveedor opera un modelo de 32B en una instancia de GPU bajo demanda con disciplina de apagado inactivo. Desde la perspectiva del cliente, es un servicio de Capa C accesible mediante el Doorman local. El modelo es OLMo 3.1 32B Think; se aplica en tiempo de ejecución una composición de adaptadores por solicitud, incluyendo el adaptador constitucional y adaptadores específicos por inquilino.

## Nivel 3 — Servicio especialista PointSav-LLM (planificado)

El Nivel 3 es un servicio de IA autónomo planificado, entrenado mediante preentrenamiento continuo sobre el corpus multi-inquilino acumulado del proveedor. No es un adaptador LoRA aplicado sobre un modelo base — es un nuevo modelo base producido siguiendo la receta publicada de AI2: 100 mil millones de tokens de entrenamiento intermedio, extensión de contexto largo y alineación posterior.

El resultado previsto es un modelo con profunda familiaridad operativa con la plataforma PointSav, accesible como servicio API multi-inquilino a precios por token diseñados para estar al alcance de los contratos SMB. El primer ciclo de preentrenamiento continuo está planificado para iniciarse en 2027, sujeto a la acumulación de corpus y la disponibilidad operativa.

## La regla de custodia de claves API

Una única regla aplica en todos los niveles: las claves API residen exclusivamente en el límite del Doorman. Ningún motor de inferencia, ningún servicio descendente y ningún proceso del anillo 2 posee una clave de proveedor. Esto garantiza que el registro de auditoría sea completo y que la lista de permisos se aplique en un único punto de control.

## Ver también

- [[compounding-doorman]] — la frontera del Doorman que aplica la regla de custodia de claves en todos los niveles
- [[llm-substrate-decision]] — por qué OLMo 3 es el modelo base en todos los niveles
- [[apprenticeship-substrate]] — el ciclo de entrenamiento que hace que los niveles superiores compongan a lo largo del tiempo

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
