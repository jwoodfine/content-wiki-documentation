---
schema: foundry-doc-v1
title: "service-slm — Esclusa Lingüística"
slug: service-slm
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-slm.md
cites: []
---

Cada llamada de inferencia de IA en la plataforma PointSav se enruta a través de un único servicio — **service-slm** (el Portero) — que posee todas las claves de API de proveedores, selecciona el nivel de cómputo más económico que satisface el plazo de la solicitud y escribe un registro de auditoría inmutable antes de devolver el resultado. Una solicitud que se resuelve en el modelo local nunca abandona la infraestructura del cliente y nunca aparece en una factura de la nube. La lógica de enrutamiento, los umbrales de nivel y el registro de auditoría son todos controlados por el operador.

## Los tres niveles de cómputo

| Nivel | Cómputo | Cuándo se usa |
|---|---|---|
| Nivel A — Local | OLMo 3 7B Q4 en la VM del espacio de trabajo (CPU) | Solicitudes de alto volumen, baja latencia, sensibles al presupuesto |
| Nivel B — GPU por demanda | OLMo 3.1 32B Think en GPU de múltiples nubes | Solicitudes que requieren mayor capacidad de modelo |
| Nivel C — API externa | Anthropic Claude / Google Gemini / OpenAI | Tareas de precisión limitada: anclaje de citas, construcción inicial del grafo |

Los clientes no eligen el nivel. La forma de la solicitud y los límites de presupuesto del inquilino determinan el enrutamiento automáticamente.

## La disciplina de la esclusa

El Portero es el único límite de IA de la plataforma: ninguna llamada de inferencia entra o sale del pipeline de conocimiento sin pasar por él. Aplica disciplina de sanitizar-salida / rehidratar-entrada: los detalles de identificación del cliente no llegan a los proveedores externos en forma cruda. Escribe una entrada de auditoría firmada al libro contable por inquilino en cada llamada, ya sea interna o externa.

## SYS-ADR-07

La implementación de `service-slm` satisface SYS-ADR-07: los datos estructurados nunca se enrutan a través de IA. El texto sin procesar que llega de los servicios del Anillo 1 pasa por `service-slm` antes de que cualquier hecho estructurado se escriba en el grafo de conocimiento.

## Véase también

- [[service-extraction]]
- [[service-search]]
- [[apprenticeship-substrate]]
- [[language-protocol-substrate]]
- [[trajectory-substrate]]
