---
schema: foundry-doc-v1
title: "Enrutamiento de IA y la esclusa lingüística"
slug: sovereign-ai-routing
short_description: "El enrutamiento de IA mantiene cada credencial de modelo externo y audita cada solicitud en una única frontera — pero el mecanismo de sanitizar-salida/rehidratar-entrada de PII que versiones anteriores de este artículo describían no existe en el código, y el enrutamiento de Nivel C hacia modelos externos tampoco está en producción todavía."
category: ai
type: topic
content_type: topic
quality: complete
index_group: the-doorman-boundary
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-17
editor: pointsav-engineering
paired_with: sovereign-ai-routing.md
cites: []

---

**Lo que este artículo afirmaba antes, y lo que realmente es cierto.** Versiones anteriores describían un mecanismo de "sanitizar-salida / rehidratar-entrada": una pasada local que eliminaría PII e identificadores de ubicación antes de que cualquier texto saliera de la red del cliente, los reemplazaría con tokens seudónimos, y revertiría la sustitución al recibir la respuesta del modelo externo — una "esclusa lingüística". **Ninguna parte de ese mecanismo existe.** El único código real de sanitización, `service-slm/crates/slm-doorman/src/redact.rs`, es un redactor de **secretos/credenciales** basado en expresiones regulares simples — claves privadas PEM, tokens de AWS/GitHub/Slack, patrones genéricos de bearer/clave-API/secreto/contraseña — y su propio comentario de documentación indica que es "la única superficie de redacción en el pipeline de aprendizaje", invocado exclusivamente al escribir tuplas del corpus de entrenamiento. Nunca se ejecuta en la ruta hacia un modelo externo. Una búsqueda en todo el código de "PII", "pseudónimo", "identificador de ubicación", o cualquier tabla de rehidratación no arroja ningún resultado en ninguna parte de `service-slm`. Por separado, el cliente real de Nivel C (`crates/slm-doorman/src/tier/external.rs`) documenta "sin llamadas API en vivo en v0.1.x" y bloquea cada llamada mediante una lista de permitidos fijada en tiempo de compilación que no puede ampliarse en producción — así que el enrutamiento que este artículo describe como vigente hoy no está en producción en absoluto, además de nunca haber tenido el paso de sanitización que afirmaba.

Esta es una brecha relevante para el cumplimiento normativo, no un detalle cosmético. Este artículo se dirige explícitamente a lectores de sectores regulados — inmobiliario, asesoramiento financiero, clínicas, despachos jurídicos — que evalúan las protecciones de privacidad reales de la plataforma. La respuesta honesta hoy: **cuando el Nivel C entre en producción, el texto crudo del cliente llegará a un modelo externo a menos que se construya primero un mecanismo real de depuración de PII** — el redactor de credenciales protege secretos, no datos del cliente. Lo que sigue describe lo que es real hoy, no el mecanismo retractado.

**El enrutamiento de IA**, tal como realmente existe, es el mecanismo por el cual [[service-slm|`service-slm`]] — el [[doorman-protocol|Doorman]] — media cada solicitud que involucra un modelo de lenguaje, a través de tres niveles de cómputo reales. Se confirma que [[service-slm|`service-slm`]] es la única frontera que posee credenciales de modelos externos y registra cada llamada en el libro contable de auditoría por inquilino; ningún otro componente del sistema posee credenciales de IA externa ni realiza llamadas salientes directas a modelos de lenguaje externos. Esta parte de la arquitectura es real y cumple lo que afirma — la brecha está específicamente en la capa de sanitización/rehidratación, no en el diseño de frontera única.

## Lo que es real hoy

- **Tres niveles de cómputo reales**, confirmados en `crates/slm-doorman/src/flow_policy.rs` y `lib.rs`: Nivel A (local), Nivel B (ráfaga Yo-Yo/GPU), Nivel C (API externa).
- **Nombres de modelos**: el Nivel A ejecuta `olmo-3-7b-instruct` localmente; el Nivel B (Yo-Yo) usa por defecto `Olmo-3-1125-32B-Think`.
- **El Nivel C no está en producción.** `tier/external.rs` documenta que no hay llamadas API externas en vivo en esta versión; el cliente solo está conectado a un simulador de pruebas, y cada llamada está bloqueada tras una lista de permitidos fija, fijada en tiempo de compilación.
- **Cada llamada intermediada se registra en auditoría** — confirmado en `audit_proxy.rs`, `lib.rs` y `cost_ledger.rs` — con el costo y la respuesta guardados en un libro contable de auditoría real.
- **Cada solicitud lleva una etiqueta de inquilino obligatoria** (`ModuleId` en `slm-core`), confirmado real.
- **No encontrado en el código**: un "límite de presupuesto configurado del inquilino" que determine las decisiones de enrutamiento — existe seguimiento de costos y configuración de precios, pero no se localizó ninguna restricción explícita de presupuesto por inquilino sobre la decisión de enrutamiento en sí.

## Lo que no es real (retractado, no simplemente suavizado)

La pasada de sanitizar-salida / rehidratar-entrada; la detección de PII; la eliminación de identificadores de ubicación; la sustitución por tokens seudónimos; cualquier tipo de tabla de rehidratación. Nada de esto existe en `service-slm`. Cualquier versión futura de este artículo que reincorpore lenguaje como "sanitiza información sensible" o "enmascara PII" para la ruta de enrutamiento de Nivel C necesita una cita de código nueva, no una restauración de este texto.

## Aplicaciones — replanteadas según lo que la plataforma puede prometer honestamente hoy

- **Flujo editorial**: los borradores TOPIC y GUIDE que llegan al Nivel C hoy lo hacen a través de las tareas de precisión acotada de la lista de permitidos fija (véase [[learning-datagraph-architecture]] para el comportamiento real de `draft_generate`) — no a través de ningún paso de sanitización, porque no existe ninguno para esta ruta.
- **Uso del Nivel C por firmas de asesoría financiera / inmobiliarias / clínicas / despachos jurídicos**: todavía no es una afirmación segura en los propios términos de este artículo, dada la retractación anterior. Cualquiera de estos casos de uso que envíe registros del libro contable, nombres de clientes, o registros de propiedades/propietarios a través del Nivel C hoy llegaría al modelo externo sin redactar la PII. Esto debe permanecer señalado hasta que se construya un mecanismo real y se verifique de forma independiente, no implicarse como ya resuelto.

## Véase también

- [[compounding-substrate]]
- [[worm-ledger-architecture]]
- [[decode-time-constraints]]
- [[machine-based-auth]]
- [[3-layer-stack]]
