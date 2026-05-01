# El sustrato de protocolo de lenguaje (resumen)

El sustrato que convierte el trabajo editorial en Foundry en
una práctica auditada, por inquilino y bifurcable. Lleva cuatro
familias, dieciocho plantillas de género y una división en
cuatro servicios que permite al cliente intercambiar cualquier
componente sin tocar los demás.

## Qué hace

El sustrato provee cuatro artefactos:

1. **Una taxonomía de adaptadores en cuatro familias.** PROSE
   para texto largo en inglés, COMMS para mensajería corta,
   LEGAL para documentos formales con volumen gatillado,
   TRANSLATE como meta-protocolo sobre las demás familias.
2. **Un registro de plantillas de género.** Dieciocho plantillas;
   cada una con sus secciones requeridas, parámetros de registro,
   convención bilingüe, esquema de portada y andamiaje de
   indicaciones (*prompt scaffolding*).
3. **Un validador de portada.** Devuelve todas las violaciones
   por género en una sola pasada, no la primera falla.
4. **Una lista de vocabulario prohibido.** Ocho términos
   transversales que sobreviven en prosa de marketing y no
   tienen lugar en escritura precisa.

Estos cuatro artefactos viajan en un crate de Rust
(`service-disclosure`) que cualquier componente Foundry puede
consumir. El Doorman compone las plantillas en indicaciones al
momento del pedido; el asistente de escritura por inquilino
valida texto entrante y saliente contra el esquema; la línea de
aprendizaje produce tuplas de entrenamiento firmadas por el
revisor en cada acción editorial.

## Por qué existe

Los asistentes de escritura de los hiperescaladores — Grammarly
Business, Microsoft 365 Copilot, Google Workspace, Apple
Intelligence — son nube-por-defecto con cadenas de atestación
ancladas en el proveedor. El texto del cliente cruza la red del
proveedor; los pesos del modelo viven con el proveedor; el
cliente no puede bifurcar pesos ni operar sobre metal propio.

La táctica de Foundry es composición, no invención. Reclamos
existentes (#15, #21, #22, #25, #31, #32) componen para producir:
**tus datos, tus pesos, tu adaptador, auditado, en tu metal.**
Los hiperescaladores estructuralmente no pueden ofrecer esto a
economía PYME porque su economía unitaria requiere entrenamiento
central y raíces de confianza compartidas.

## Las cuatro familias

| Familia | Responsabilidad | Plantillas |
|---|---|---|
| **PROSE** | Prosa larga en inglés | README, TOPIC, GUIDE, MEMO, ARCHITECTURE, INVENTORY, license-explainer, CHANGELOG |
| **COMMS** | Comunicación corta | correo, chat, comentario de ticket, notas de reunión |
| **LEGAL** | Formal con volumen gatillado | contrato, CLA, política, términos (rutea a Tier C por defecto) |
| **TRANSLATE** | Meta-protocolo | Opera sobre las otras familias |

Tres adaptadores se componen al momento del pedido:
`base ⊕ adaptador-inquilino ⊕ adaptador-protocolo`. Cinco o
más cruzan a interferencia multi-tarea según la literatura LoRA
de 2025; Foundry se mantiene en tres.

## La división en cuatro servicios

| Servicio | Forma | Cluster propietario |
|---|---|---|
| `service-content` | Datos — grafo de conocimiento | project-slm |
| `service-slm` | Inferencia — Doorman + ruteo de niveles | project-slm |
| `service-disclosure` | Esquema — tipos, validadores, CFG, plantillas | project-language |
| `service-proofreader` | Operativo — asistente HTTP por petición | project-proofreader |

Un cliente puede sustituir cualquiera sin tocar los demás. Es
el significado de *forkable on day one*.

## Véase también

- [Documento canónico en inglés](topic-language-protocol-substrate.md)
- [Hospedaje por el cliente](topic-customer-hostability.md)
- [Disciplina anti-homogenización](topic-anti-homogenization-discipline.md)

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.