---
schema: foundry-doc-v1
title: "Cómo ejecutar inferencia SLM local"
slug: run-local-slm-inference
category: how-to
content_type: how-to
type: how-to
status: stub
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: run-local-slm-inference.md
---

La pila de inferencia de PointSav ejecuta un modelo de lenguaje pequeño localmente a través del gateway Doorman. Toda la inferencia permanece en el hardware del operador — ningún dato de solicitud se envía a un proveedor externo. Esta guía cubre el inicio del servicio SLM local, la verificación del punto de conexión de salud del Doorman y el envío de tu primera solicitud de inferencia desde os-console.

Para la arquitectura de la pila de inferencia, consulta [[slm-stack-architecture]] y [[doorman-protocol]]. Para el cartucho de consola que expone la inferencia local en la TUI, consulta [[app-console-slm]].

## Véase también

- [[slm-stack-architecture]] — arquitectura de la pila SLM local y niveles de modelo compatibles
- [[doorman-protocol]] — el protocolo del gateway Doorman; salud, enrutamiento y comportamiento del interruptor de circuito
- [[app-console-slm]] — el cartucho SLM de os-console y el panel de salud del Doorman
- [[open-first-totebox-session]] — el contexto de operador en el que la inferencia está disponible
- [[self-host-a-deployment]] — provisiona la instancia que aloja la pila de inferencia
