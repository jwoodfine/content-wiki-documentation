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
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: service-slm.md
cites: []
---

`service-slm`, también llamado el Portero (Doorman), es el límite del Anillo 3 de inteligencia opcional en la arquitectura de tres anillos de PointSav. Es el único servicio que posee claves de API para proveedores de IA externos. Cada solicitud de inferencia de IA de cualquier otro servicio se enruta a través del Portero.

## Los tres niveles de cómputo

| Nivel | Cómputo | Cuándo se usa |
|---|---|---|
| Nivel A — Local | OLMo 3 7B Q4 en la VM del espacio de trabajo (CPU) | Solicitudes de alto volumen, baja latencia, sensibles al presupuesto |
| Nivel B — Yo-Yo | OLMo 3.1 32B Think en GPU de múltiples nubes | Solicitudes que requieren mayor capacidad de modelo |
| Nivel C — API externa | Anthropic Claude / Google Gemini / OpenAI | Tareas de precisión limitada: anclaje de citas, construcción inicial del grafo |

Los clientes no eligen el nivel. La forma de la solicitud y los límites de presupuesto del inquilino determinan el enrutamiento automáticamente.

## La disciplina de la esclusa

El Portero actúa como la esclusa de aire para el texto no estructurado que ingresa al pipeline de conocimiento. Aplica disciplina de sanitizar-salida / rehidratar-entrada: los detalles de identificación del cliente no llegan a los proveedores externos en forma cruda. Escribe una entrada de auditoría firmada al libro contable por inquilino en cada llamada, ya sea interna o externa.

## SYS-ADR-07

La implementación de `service-slm` satisface SYS-ADR-07: los datos estructurados nunca se enrutan a través de IA. El texto sin procesar que llega de los servicios del Anillo 1 pasa por `service-slm` antes de que cualquier hecho estructurado se escriba en el grafo de conocimiento.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
