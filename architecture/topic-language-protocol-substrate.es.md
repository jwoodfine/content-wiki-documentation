---
schema: foundry-doc-v1
title: "El Sustrato del Protocolo de Lenguaje"
slug: topic-language-protocol-substrate.es
category: architecture
type: topic
quality: published
short_description: La infraestructura editorial que hace del trabajo de escritura en un despliegue de PointSav una práctica auditada, por inquilino y bifurcable, con una taxonomía de adaptadores y un ciclo de entrenamiento que mejora con el tiempo.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - constitutional-ai-2212-08073
  - lorax-predibase
  - olmo3-allenai
paired_with: topic-language-protocol-substrate.md
---

El **Sustrato del Protocolo de Lenguaje** es la arquitectura que hace del trabajo editorial en un despliegue de PointSav algo estructurado, por inquilino y auditable. Define una taxonomía de adaptadores de cuatro familias para la generación de texto, un conjunto de plantillas de género entregadas como andamiaje de prompts en tiempo de solicitud, una división de servicios que mantiene los datos, la inferencia y las preocupaciones operativas en componentes separados, y un ciclo de entrenamiento cuyo resultado se acumula con cada acción editorial que realiza el inquilino.

## La inversión del modelo tradicional

Los asistentes de escritura en la nube típicamente enrutan el texto del cliente a través de la infraestructura del proveedor, entrenan en modelos del proveedor y almacenan los perfiles de voz por cliente en el proveedor. El Sustrato del Protocolo de Lenguaje invierte estas propiedades: los adaptadores LoRA por inquilino se entrenan en el corpus propio del cliente, se alojan en el hardware propio del cliente y son portables si el cliente se va. El registro de auditoría de cada llamada editorial de IA es propiedad del cliente.

## Taxonomía de cuatro familias

La producción de infraestructura multi-LoRA soporta hasta tres adaptadores por solicitud antes de que la interferencia multitarea degrade la calidad. La taxonomía del sustrato está diseñada alrededor de esta restricción:

- **PROSE** — Prosa larga en inglés: READMEs, TOPICs, GUIDEs, memorandos, documentos de arquitectura.
- **COMMS** — Texto interpersonal corto: correo electrónico, chat, comentarios de tickets, notas de reuniones.
- **LEGAL** — Volumen limitado; se enruta a través de la API externa (Tier C) salvo que el corpus legal del inquilino justifique un adaptador dedicado.
- **TRANSLATE** — Meta-protocolo; transforma la salida de cualquier otra familia a través de un par de idiomas o un cambio de registro.

En tiempo de solicitud, el Doorman compone tres capas de adaptadores: modelo base + adaptador de inquilino + adaptador de protocolo. El registro, la voz de marca, el subtipo de documento, la formalidad del canal y el público objetivo se expresan como **andamiaje de prompt** en lugar de adaptadores adicionales.

## División de servicios y portabilidad del cliente

Cuatro servicios componen el sustrato con contratos distintos y pueden desplegarse, intercambiarse o reemplazarse de forma independiente: `service-content` (datos), `service-slm` (inferencia), `service-disclosure` (esquemas y restricciones), y `service-proofreader` (asistente de escritura operativo). El cliente puede reemplazar el backend de inferencia sin tocar los otros tres componentes.

## El rol de puerta de enlace editorial

En la versión v0.1.31 del espacio de trabajo, `service-language` se convirtió en la puerta de enlace editorial para toda la producción de wiki y documentación de Foundry. Los borradores de las sesiones de Task, Root y Master se publican en directorios `drafts-outbound/`. `project-language` barre esos borradores, aplica las restricciones del sustrato (gramática de vocabulario prohibido, resolución del registro de citas, generación de pares bilingües, disciplina BCSC de información prospectiva) y entrega el resultado refinado al repositorio de destino correspondiente.

Un ciclo DPO de dos etapas se cierra con el tiempo: la Etapa 1 captura la corrección estructural del sustrato de aprendizaje; la Etapa 2 captura el arte editorial de las ediciones del Contribuidor Creativo al final del ciclo. El preentrenamiento continuo trimestral en el corpus combinado hace que la línea base generada por el sustrato converja hacia el estándar combinado de estructura y arte.

## Véase también

- [[compounding-doorman]] — el límite de inferencia a través del cual enruta el sustrato
- [[apprenticeship-substrate]] — el mecanismo de entrenamiento que el sustrato extiende al trabajo editorial
- [[topic-adapter-composition]] — el álgebra que hace funcionar la composición de tres adaptadores

## Referencias

1. IA Constitucional: Inofensividad a partir de la Retroalimentación de IA, Bai et al., arXiv 2212.08073.
2. OLMo 3 — Allen Institute for AI, Apache 2.0.
3. LoRAX — servidor de inferencia multi-LoRA de Predibase.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Atribución 4.0 Internacional](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.