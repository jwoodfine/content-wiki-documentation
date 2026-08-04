---
schema: foundry-doc-v1
title: "Cómo ejecutar inferencia SLM local"
slug: run-local-slm-inference
short_description: "Inicia el servicio local de Tier A, verifica que Doorman lo reconoce como listo y envía una solicitud de inferencia desde la consola o la API, manteniendo todos los datos del prompt en el despliegue."
category: self-hosting
index_group: wiring-up-inference
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: run-local-slm-inference.md
---

## Requisitos previos

- Un despliegue con el binario del modelo SLM local instalado en la ruta que `local-slm.service` espera (véase [[self-host-a-deployment]])
- El servicio `slm-doorman` en ejecución y en buen estado (véase [[configure-doorman]])
- Una sesión con acceso de nivel User (véase [[pair-a-new-device]])

## Propósito

La pila de inferencia de la plataforma ejecuta un modelo de lenguaje pequeño de forma local, en el Tier A, al que se accede a través del gateway Doorman. Toda la inferencia de Tier A permanece en el hardware del propio operador — ningún dato de prompt sale del despliegue. Esta guía inicia el modelo local, confirma que Doorman lo ve como listo y envía una solicitud, tanto desde la TUI de consola como directamente contra la API.

## Procedimiento

1. Inicie el servicio SLM local, si no está ya en ejecución:

   ```
   sudo systemctl start local-slm
   ```

2. Confirme que arrancó correctamente:

   ```
   systemctl is-active local-slm
   journalctl -u local-slm --since "1 minute ago"
   ```

   Un arranque saludable registra en el log la carga del modelo y el enlace del servicio a su puerto (por defecto `127.0.0.1:8080`). Si falla, verifique que el archivo del modelo indicado en la configuración de la unidad exista realmente en la ruta que el servicio espera.

3. Confirme que Doorman ve el Tier A como listo. En la consola, pulse **F9** para abrir el panel de salud del SLM Cartridge, que lee el `/readyz` de Doorman. `tier_a` (mostrado también como `A — Local`) debe estar en `true`/verde antes de que una solicitud tenga éxito. Pulse **R** para actualizar.

4. Envíe un prompt desde la consola. Con el Tier A activo, escriba un prompt en la línea de entrada de F9 y pulse Enter — la respuesta se transmite token a token en el área de salida, y la barra de estado muestra el nivel activo durante la generación.

5. O envíe un prompt directamente vía la API:

   ```
   curl -X POST http://127.0.0.1:9080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"Summarise the role of the Doorman gateway."}]}'
   ```

   La respuesta es un objeto JSON compatible con OpenAI con un arreglo `choices`; cada elección contiene el texto generado.

## Resultado esperado

Un prompt enviado mientras el Tier A está listo devuelve una respuesta generada sin que ningún dato salga del host — la línea F9 de la consola y la llamada a `/v1/chat/completions` recorren la misma ruta de solicitud subyacente, simplemente desde dos clientes distintos.

## Verificación

Las solicitudes de inferencia desde la consola son seguras conforme a SYS-ADR-07 por construcción: por la capa del modelo solo pasa texto plano de prompt, nunca datos estructurados de la plataforma (registros de entidades, entradas WORM). Confirme que el Tier A siguió siendo el nivel que sirvió la solicitud, en lugar de haber caído silenciosamente a otro, consultando `/readyz` de nuevo tras la solicitud:

```
curl http://127.0.0.1:9080/readyz
```

`tier_a: true` y `ai_available: true` confirman que el Tier A sirvió la solicitud. Si el Tier B (Yo-Yo) está configurado y el Tier A deja de estar disponible a mitad de sesión, Doorman enruta automáticamente al Tier B en lugar de fallar — véase [[doorman-protocol]] para el orden completo de fallback.

## Reversión

Detenga el servicio del modelo local; Doorman sigue en ejecución e informa `tier_a: false` en su siguiente comprobación de `/readyz`, en lugar de fallar:

```
sudo systemctl stop local-slm
```

## Próximos pasos

- [[run-first-slm-query]] — un primer recorrido guiado de consulta desde la consola
- [[query-the-datagraph]] — otra capacidad enrutada por Doorman, búsqueda de entidades en vez de inferencia
- [[doorman-protocol]] — el modelo completo de fallback entre niveles, para cuando el Tier A solo no basta

## Véase también

- [[slm-stack-architecture]] — arquitectura de la pila SLM local y los niveles de modelo compatibles
- [[doorman-protocol]] — el protocolo del gateway Doorman; preparación, enrutamiento y comportamiento de fallback entre niveles
- [[app-console-slm]] — el cartucho SLM de os-console y el panel de salud del Doorman
- [[run-first-slm-query]] — enviar una consulta desde la consola una vez que el modelo esté en ejecución
- [[self-host-a-deployment]] — provisionar la instancia que aloja la pila de inferencia
- [[configure-doorman]] — configurar el Tier A/B/C antes de ejecutar una solicitud de inferencia
