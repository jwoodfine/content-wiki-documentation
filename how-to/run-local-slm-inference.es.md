---
schema: foundry-doc-v1
title: "Cómo ejecutar inferencia SLM local"
slug: run-local-slm-inference
category: how-to
content_type: how-to
type: how-to
status: active
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: run-local-slm-inference.md
---

La pila de inferencia de PointSav ejecuta un modelo de lenguaje pequeño localmente a través del gateway Doorman. Toda la inferencia permanece en el hardware del operador — ningún dato de solicitud sale del despliegue. Esta guía cubre el inicio del servicio SLM local, la verificación del endpoint de salud del Doorman y el envío de una solicitud de inferencia — tanto desde la TUI de la consola como directamente a través de la API.

Para la arquitectura de la pila de inferencia, véase [[slm-stack-architecture]] y [[doorman-protocol]]. Para el cartucho de consola que expone la inferencia local en la TUI, véase [[app-console-slm]].

## Requisitos previos

- Un despliegue con el binario del modelo OLMo instalado en la ruta esperada (véase [[self-host-a-deployment]])
- El servicio `slm-doorman-server` en ejecución y saludable
- Una sesión con acceso de nivel USER como mínimo (véase [[pair-a-new-device]])

## Paso 1: Iniciar el servicio SLM

Si el servicio SLM no está ya en ejecución, inícielo:

```
sudo systemctl start slm-doorman-server
```

Verifique que se inició correctamente:

```
systemctl is-active slm-doorman-server
journalctl -u slm-doorman-server --since "1 minute ago"
```

Un inicio saludable produce una línea de registro indicando que el modelo se cargó y que el Doorman está escuchando en su puerto configurado. Si el servicio no se inicia, verifique la ruta del binario del modelo en la configuración del servicio — el binario OLMo debe estar presente en la ruta que el servicio espera.

## Paso 2: Verificar la salud del Doorman desde la consola

Presione **F9** en la consola para abrir el Cartucho SLM. El panel de salud del Doorman muestra:

- `A — DataGraph`: disponibilidad del almacén de entidades (no requerida para inferencia pura)
- `B — SLM`: debe mostrar verde una vez que el modelo esté cargado y el Doorman sea accesible
- `C — Respaldo local`: siempre disponible; se usa cuando el Nivel B está degradado

El Nivel B debe estar verde antes de que las solicitudes de inferencia tengan éxito. Presione **R** para actualizar el estado de salud.

## Paso 3: Enviar una solicitud de inferencia desde la consola

Con el Nivel B activo, envíe un prompt en la línea de entrada de F9. Escriba el texto de su prompt y presione Enter. La respuesta del modelo se transmite token por token al área de salida. La barra de estado muestra el nivel de inferencia activo (`B`) durante la generación.

Las solicitudes de inferencia a través de la consola son seguras conforme a SYS-ADR-07 — ningún dato estructurado de la plataforma pasa por la capa del modelo. El modelo recibe solo texto de prompt plano.

## Paso 4: Enviar una solicitud de inferencia directamente a través de la API

Para uso programático, llame al endpoint de inferencia del Doorman:

```
curl -X POST http://127.0.0.1:<puerto-doorman>/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token-de-sesión>" \
  -d '{
    "prompt": "Resumir el papel del gateway Doorman:",
    "max_tokens": 200
  }'
```

La respuesta es un objeto JSON con una matriz `choices`. Cada elección contiene el texto generado. El campo `model` en la respuesta confirma qué nivel atendió la solicitud.

## Paso 5: Verificar el estado del interruptor de circuito

El interruptor de circuito del Doorman se abre automáticamente si el servicio SLM no responde. Cuando está abierto, todas las solicitudes de inferencia caen al Nivel C (respaldo local). Para verificar el estado del circuito:

```
curl http://127.0.0.1:<puerto-doorman>/health
```

La respuesta incluye `tier_b_state`: `CLOSED` (saludable) u `OPEN` (activado). Un circuito activado se restablece después del período de enfriamiento configurado, o inmediatamente después de que el servicio SLM se recupere.

## Puntos clave

- Toda la inferencia se ejecuta en las instalaciones; ningún dato de prompt sale del despliegue
- El Nivel B (SLM) debe mostrar verde en el panel de salud F9 antes de que las solicitudes de inferencia tengan éxito
- El interruptor de circuito del Doorman cae automáticamente al Nivel C cuando el modelo no responde
- Se aplica SYS-ADR-07: no pase datos estructurados de la plataforma (registros de entidades, entradas WORM) por la capa del modelo

## Véase también

- [[slm-stack-architecture]] — arquitectura de la pila SLM local y niveles de modelo compatibles
- [[doorman-protocol]] — el protocolo del gateway Doorman; salud, enrutamiento y comportamiento del interruptor de circuito
- [[app-console-slm]] — el cartucho SLM de os-console y el panel de salud del Doorman
- [[run-first-slm-query]] — enviar una consulta desde la consola una vez que el modelo esté en ejecución
- [[self-host-a-deployment]] — provisionar la instancia que aloja la pila de inferencia
