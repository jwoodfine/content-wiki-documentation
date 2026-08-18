---
schema: foundry-doc-v1
title: "Enrutamiento de IA y la esclusa lingüística"
slug: sovereign-ai-routing
short_description: "El enrutamiento de IA mantiene cada credencial de modelo externo y audita cada solicitud en una única frontera. No depura PII de los prompts, y el enrutamiento de Nivel C hacia modelos externos todavía no está en producción."
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

**El enrutamiento de IA**, tal como existe hoy, es el mecanismo por el cual [[service-slm|`service-slm`]] — el [[doorman-protocol|Doorman]] — media cada solicitud que involucra un modelo de lenguaje, a través de tres niveles de cómputo. `service-slm` es la única frontera que posee credenciales de modelos externos y registra cada llamada en el libro contable de auditoría por inquilino; ningún otro componente del sistema posee credenciales de IA externa ni realiza llamadas salientes directas a modelos de lenguaje externos.

Esta plataforma no depura información personal identificable ni datos de ubicación de un prompt antes de una llamada externa. El único código de sanitización en la plataforma hoy es un redactor de credenciales: elimina secretos — claves privadas, tokens de API, patrones genéricos de bearer/secreto/contraseña — y se ejecuta únicamente en la ruta que escribe ejemplos de entrenamiento en el corpus de aprendizaje, nunca en la ruta hacia un modelo externo.

Esta es una brecha relevante para el cumplimiento normativo, no un detalle cosmético, para lectores de sectores regulados — inmobiliario, asesoramiento financiero, clínicas, despachos jurídicos — que evalúan las protecciones de privacidad de la plataforma. La respuesta honesta hoy: cuando el Nivel C entre en producción, el texto crudo del cliente llegará a un modelo externo a menos que se construya primero un mecanismo de depuración de PII. El redactor de credenciales protege secretos, no datos del cliente.

## Lo que es real hoy

- **Tres niveles de cómputo**: Nivel A (local), Nivel B (ráfaga Yo-Yo/GPU), Nivel C (API externa).
- **Nombres de modelos**: el Nivel A ejecuta `olmo-3-7b-instruct` localmente; el Nivel B (Yo-Yo) usa por defecto `Olmo-3-1125-32B-Think`.
- **El Nivel C no está en producción.** El cliente solo está conectado a un simulador de pruebas, y cada llamada está bloqueada tras una lista de permitidos fija, fijada en tiempo de compilación.
- **Cada llamada intermediada se registra en auditoría**, con el costo y la respuesta guardados en el libro contable de auditoría.
- **Cada solicitud lleva una etiqueta de inquilino obligatoria.**
- **Ningún límite de presupuesto por inquilino determina todavía las decisiones de enrutamiento.** Existe seguimiento de costos y configuración de precios, pero nada vincula aún el gasto de un inquilino con una decisión de enrutamiento.

## Lo que no está construido

La depuración de PII, la eliminación de identificadores de ubicación, la sustitución por tokens seudónimos, y cualquier forma de mecanismo de rehidratación no están construidos.

## Aplicaciones — lo que la plataforma puede prometer honestamente hoy

- **Flujo editorial**: los borradores TOPIC y GUIDE que llegan al Nivel C hoy lo hacen a través de las tareas de precisión acotada de la lista de permitidos fija (véase [[learning-datagraph-architecture]] para el comportamiento de `draft_generate`) — no a través de ningún paso de sanitización, porque no existe ninguno para esta ruta.
- **Uso del Nivel C por firmas de asesoría financiera / inmobiliarias / clínicas / despachos jurídicos** todavía no es una afirmación segura. Cualquiera de estos casos de uso que envíe registros del libro contable, nombres de clientes, o registros de propiedades/propietarios a través del Nivel C hoy llegaría al modelo externo con la PII sin redactar. Un mecanismo real de depuración de PII, verificado de forma independiente, debe existir antes de que eso cambie.

## Véase también

- [[compounding-substrate]]
- [[worm-ledger-architecture]]
- [[decode-time-constraints]]
- [[machine-based-auth]]
- [[3-layer-stack]]
