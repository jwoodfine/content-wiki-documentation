---
schema: foundry-doc-v1
title: "Cómo configurar el gateway Doorman"
slug: configure-doorman
short_description: "Configura un gateway Doorman de instancia única mediante variables de entorno — endpoint local de Tier A, cómputo de ráfaga Yo-Yo opcional de Tier B, proveedores externos opcionales de Tier C — y verifica el estado de cada nivel a través de /readyz."
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
paired_with: configure-doorman.md
---

## Requisitos previos

- El binario `slm-doorman-server` (o la unidad systemd `slm-doorman`) disponible en el host de despliegue
- El binario del modelo SLM local presente en la ruta que espera el Tier A (véase `local-slm.service`)
- Una sesión de terminal en el host donde se ejecutará Doorman
- Acceso de red a un endpoint Yo-Yo en GCE, si se desea cómputo de ráfaga de Tier B (opcional)
- Claves de API de Anthropic, Gemini u OpenAI, si se desea el respaldo externo de Tier C (opcional)

## Propósito

El gateway Doorman enruta las solicitudes de inferencia y de audit-proxy hacia uno de tres niveles: Tier A (un modelo pequeño local), Tier B (cómputo de ráfaga Yo-Yo en GCE, opcional) o Tier C (APIs de proveedores externos, opcional). Doorman se configura íntegramente mediante variables de entorno — no existe ningún archivo de configuración. Un Doorman con solo el Tier A configurado es un despliegue completo y válido (el "modo community-tier"); los Tiers B y C son aditivos, no obligatorios.

## Procedimiento

1. Defina la dirección de escucha. Doorman escucha en `SLM_BIND_ADDR` (por defecto `127.0.0.1:9080` — solo loopback; coloque delante un proxy inverso con terminación TLS para cualquier tráfico que no sea del mismo host).

2. Defina el endpoint y el modelo del Tier A (local). `SLM_LOCAL_ENDPOINT` debe coincidir con la dirección a la que se vincula `local-slm.service` (por defecto `http://127.0.0.1:8080`). `SLM_LOCAL_MODEL` debe coincidir con el nombre de archivo del modelo que ese servicio cargó al arrancar (por ejemplo `Olmo-3-1125-7B-Think-Q4_K_M.gguf`). Estas dos variables son las únicas necesarias para que Doorman arranque y atienda solicitudes.

3. Opcional: defina las variables del Tier B (Yo-Yo). Deje todas las variables `SLM_YOYO_*` vacías o sin definir para permanecer en modo community-tier (solo Tier A) — Doorman arranca sin problemas en cualquiera de los dos casos. Para habilitar el Tier B, defina como mínimo `SLM_YOYO_ENDPOINT` (la URL de inferencia Yo-Yo en GCE) y `SLM_YOYO_BEARER` (un token bearer estático para la ruta de desarrollo/staging; un despliegue real con GCP Workload Identity lo sustituye por un token específico del proveedor). `SLM_YOYO_MODEL` nombra el modelo servido en ese endpoint.

4. Opcional: defina las variables del Tier C (externo). Cada proveedor (`SLM_TIER_C_ANTHROPIC_*`, `SLM_TIER_C_GEMINI_*`, `SLM_TIER_C_OPENAI_*`) necesita su propio endpoint, clave de API y tarifas de entrada/salida por millón de tokens. Todo proveedor sin definir permanece deshabilitado; la ruta de audit-proxy (`POST /v1/audit/proxy`) devuelve `503` con un mensaje explicativo de "unconfigured" hasta que al menos uno esté configurado — este es el comportamiento correcto y esperado, no un estado de error.

5. Coloque las variables ya definidas en un `EnvironmentFile` (por ejemplo `/etc/local-doorman/local-doorman.env`) y apunte la directiva `EnvironmentFile=` de la unidad systemd hacia él, o añada los valores como líneas `Environment=` en línea dentro de un drop-in de la unidad. Los valores del `EnvironmentFile` tienen prioridad sobre cualquier línea `Environment=` en línea que ya exista en la unidad.

6. Inicie el servicio:

   ```
   sudo systemctl start slm-doorman
   ```

## Resultado esperado

Doorman arranca y comienza a aceptar solicitudes en `SLM_BIND_ADDR`, con independencia de si el Tier B o el Tier C están configurados. `GET /healthz` devuelve `200` de inmediato como comprobación de vida. `GET /readyz` devuelve el estado de preparación junto con el estado de los niveles una vez que Doorman ha terminado de construir su enrutador interno.

## Verificación

Compruebe la preparación y el estado de los niveles:

```
curl http://127.0.0.1:9080/readyz
```

Una respuesta sana con solo el Tier A ("community-tier") incluye:

```json
{
  "tier_a": true,
  "tier_b": false,
  "tier_c": false,
  "has_local": true,
  "has_yoyo": false,
  "has_external": false,
  "ai_available": true
}
```

`tier_a`/`tier_b`/`tier_c` (y sus equivalentes `has_local`/`has_yoyo`/`has_external`) son booleanos, no una cadena de estado de circuito — un nivel marca `true` cuando su dependencia es alcanzable, `false` en caso contrario. `ai_available` es `true` siempre que cualquiera de los niveles esté operativo. El Tier B expone además su propio detalle de circuit-breaker en `GET /v1/status/yoyo` (estados de circuito de los nodos Yo-Yo) — una solicitud de Tier B que encuentre un circuito Yo-Yo abierto recurre automáticamente al Tier A en lugar de fallar.

Confirme el enrutamiento, no solo la preparación, enviando una solicitud real:

```
curl -X POST http://127.0.0.1:9080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Say hello in one word."}]}'
```

## Reversión

Detenga el servicio y elimine o comente las variables que haya cambiado:

```
sudo systemctl stop slm-doorman
```

Los Tiers B y C son aditivos y pueden deshabilitarse de forma independiente — vaciar `SLM_YOYO_ENDPOINT` o la clave de un proveedor `SLM_TIER_C_*` devuelve Doorman al modo community-tier en el siguiente reinicio sin afectar al Tier A.

## Próximos pasos

- [[run-local-slm-inference]] — envíe solicitudes de inferencia una vez que Doorman esté en ejecución
- [[doorman-protocol]] — el modelo completo de enrutamiento y circuit-breaker
- [[navigate-console-tui]] — lea el estado de los niveles desde el panel F9 de la consola

## Véase también

- [[doorman-protocol]] — el modelo de circuit-breaker y la lógica de enrutamiento entre niveles
- [[slm-stack-architecture]] — cómo está estructurado el modelo SLM del que depende el Tier A
- [[run-local-slm-inference]] — verificar que el servicio SLM esté saludable antes de que inicie Doorman
- [[navigate-console-tui]] — leer el estado del nivel en la barra de estado de la consola
- [[run-first-slm-query]] — enviar su primera solicitud de inferencia una vez que Doorman esté configurado
