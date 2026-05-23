---
schema: foundry-doc-v1
title: "El sustrato de protocolo de lenguaje"
slug: language-protocol-substrate.es
lang: es
paired_with: language-protocol-substrate.md
category: substrate
type: topic
quality: complete
short_description: "La infraestructura editorial que codifica el registro, la voz de marca, el subtipo de documento y el público objetivo como andamiaje de indicaciones reutilizable — cuatro familias de adaptadores, dieciocho plantillas de género, un validador de portada, y una división en cuatro servicios que permite al cliente sustituir cualquier componente sin tocar los demás."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
---

Cada acción editorial que pasa por la plataforma PointSav — generación de documentos, validación de esquemas, captura de tuplas de entrenamiento — está modelada por un sustrato que codifica el registro, la voz de marca, el subtipo de documento y el público objetivo como andamiaje de indicaciones reutilizable, no como instrucción ad-hoc. El resultado es trabajo editorial auditado, por inquilino y sustituible en cualquier capa sin reconstruir el resto.

El sustrato provee cuatro familias de artefactos, dieciocho plantillas de género, un validador de portada que devuelve todas las violaciones de esquema en una sola pasada, y una lista de vocabulario prohibido de ocho términos transversales. Estos viajan en un crate de Rust (`service-disclosure`) dividido entre cuatro servicios — `service-content` (grafo de conocimiento), `service-slm` (Doorman e inferencia), `service-disclosure` (esquema y plantillas), `service-proofreader` (asistente HTTP) — donde cualquier servicio puede ser sustituido por uno del cliente sin afectar a los demás.

Tres adaptadores se componen al momento del pedido: modelo base, adaptador de inquilino (voz de marca) y adaptador de protocolo (PROSE | COMMS | LEGAL | TRANSLATE). El registro, la voz de marca y el público objetivo viven como andamiaje de indicaciones, no como adaptadores adicionales — cinco o más adaptadores por pedido cruzan a interferencia multi-tarea según la literatura LoRA de 2025; la plataforma se mantiene en tres. Cada acción editorial produce una tupla de entrenamiento firmada por el revisor a través de la línea de [[apprenticeship-substrate|aprendizaje]], alimentando el pre-entrenamiento continuo del adaptador del cliente sin que el texto salga de su infraestructura.

Para compradores regulados, la división en cuatro servicios importa porque cada acción editorial queda auditada en el libro por inquilino antes de salir de la red del cliente. El cliente puede bifurcar cualquier adaptador, inspeccionar el andamiaje de indicaciones y verificar que su voz de marca no se agrupa con los datos de entrenamiento de otro inquilino. Por `[ni-51-102]` y `[osc-sn-51-721]`, la línea de entrenamiento se describe en términos prospectivos; la arquitectura del sustrato está operativa hoy.

## Qué provee

**Una taxonomía de adaptadores en cuatro familias.** PROSE para texto largo en inglés, COMMS para mensajería corta interpersonal, LEGAL para documentos formales con volumen gatillado, TRANSLATE como meta-protocolo sobre las demás familias.

**Un registro de plantillas de género.** Dieciocho plantillas; cada una con sus secciones requeridas, parámetros de registro, convención bilingüe, esquema de portada y andamiaje de indicaciones.

**Un validador de portada.** Devuelve todas las violaciones por género en una sola pasada, no la primera falla.

**Una lista de vocabulario prohibido.** Ocho términos transversales que sobreviven en prosa de marketing y no tienen lugar en escritura precisa.

## Las cuatro familias

| Familia | Responsabilidad | Plantillas |
|---|---|---|
| **PROSE** | Prosa larga en inglés | README, TOPIC, GUIDE, MEMO, ARCHITECTURE, INVENTORY, license-explainer, CHANGELOG |
| **COMMS** | Comunicación corta | correo, chat, comentario de ticket, notas de reunión |
| **LEGAL** | Formal con volumen gatillado | contrato, CLA, política, términos (rutea a Tier C por defecto) |
| **TRANSLATE** | Meta-protocolo | Opera sobre las otras familias |

Tres adaptadores se componen al momento del pedido: `base ⊕ adaptador-inquilino ⊕ adaptador-protocolo`. Cinco o más cruzan a interferencia multi-tarea según la literatura LoRA de 2025; la plataforma se mantiene en tres.

## La división en cuatro servicios

| Servicio | Forma | Cluster propietario |
|---|---|---|
| `service-content` | Datos — grafo de conocimiento | project-slm |
| `service-slm` | Inferencia — Doorman + ruteo de niveles | project-slm |
| `service-disclosure` | Esquema — tipos, validadores, CFG, plantillas | project-language |
| `service-proofreader` | Operativo — asistente HTTP por petición | project-proofreader |

Un cliente puede sustituir cualquiera sin tocar los demás. La contribución de la plataforma es el libro de auditoría por inquilino que hace que cada sustitución sea composable a través de contextos regulatorios.

## Véase también

- [[style-guide-topic]]
- [[customer-hostability]]
- [[anti-homogenization-discipline]]
- [[apprenticeship-substrate]]
- [[citation-substrate]]
