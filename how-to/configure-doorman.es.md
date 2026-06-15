---
schema: foundry-doc-v1
title: "Cómo configurar el gateway Doorman"
slug: configure-doorman
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: configure-doorman.md
---

El gateway Doorman enruta todas las solicitudes de inferencia y búsqueda de entidades al nivel apropiado: Nivel A (DataGraph), Nivel B (SLM local) o Nivel C (respaldo local). Configurar Doorman significa establecer las direcciones de nivel superior para cada nivel, definir los umbrales del interruptor de circuito y verificar el endpoint de salud después del inicio. Esta guía cubre un despliegue de Doorman en una sola instancia.

Para el protocolo de Doorman y el modelo de interruptor de circuito, véase [[doorman-protocol]]. Para iniciar el modelo SLM del que depende el Nivel B, véase [[run-local-slm-inference]].

## Requisitos previos

- El binario `slm-doorman-server` disponible en el host de despliegue
- Acceso de red al endpoint del DataGraph (`service-content`) si el Nivel A está previsto
- El binario del modelo OLMo presente en la ruta configurada para el Nivel B
- Una sesión de terminal en el host donde se ejecutará Doorman

## Paso 1: Crear el archivo de configuración de Doorman

Doorman lee su configuración desde un archivo TOML. Cree `doorman.toml`:

```toml
[server]
port = 9080
bind = "127.0.0.1"

[tier_a]
enabled = true
service_content_url = "http://127.0.0.1:9090"
circuit_breaker_threshold = 5
circuit_breaker_timeout_secs = 30

[tier_b]
enabled = true
model_path = "/opt/pointsav/models/olmoe-1b-7b-instruct.gguf"
context_window = 4096
max_tokens = 512

[tier_c]
enabled = true
fallback_message = "Inferencia no disponible — solo respaldo local"
```

Ajuste `service_content_url` para que coincida con la dirección del servicio DataGraph en su despliegue. Si el DataGraph está en el mismo host, `127.0.0.1:9090` es típico. Si está en un nodo separado, use su dirección de red.

## Paso 2: Iniciar el servicio Doorman

Inicie el servicio con el archivo de configuración:

```
slm-doorman-server --config doorman.toml
```

O como un servicio systemd:

```
sudo systemctl start slm-doorman-server
```

Doorman registra su secuencia de inicio: intenta contactar el DataGraph (Nivel A), carga el modelo SLM (Nivel B) y confirma que el Nivel C siempre está disponible. Cualquier fallo al contactar el Nivel A en el inicio no impide que Doorman inicie — marca el circuito del Nivel A como `OPEN` y enruta al Nivel B en su lugar.

## Paso 3: Verificar el endpoint de salud

Doorman expone un endpoint de salud en `/health`:

```
curl http://127.0.0.1:9080/health
```

Una respuesta saludable:

```json
{
  "tier_a_state": "CLOSED",
  "tier_b_state": "CLOSED",
  "tier_c_state": "AVAILABLE",
  "active_tier": "A"
}
```

`CLOSED` significa que el circuito está saludable y enrutando solicitudes. `OPEN` significa que el circuito se ha activado y Doorman no está enrutando a ese nivel. `active_tier` muestra qué nivel está recibiendo solicitudes actualmente.

## Paso 4: Verificar desde la consola

Abra la consola y presione **F9** para ver el panel de salud de Doorman. El panel lee desde el mismo endpoint `/health`. Los Niveles A, B y C deben mostrar verde bajo operación normal.

Si el Nivel A muestra `OPEN` pero el servicio DataGraph está en ejecución, verifique `service_content_url` en la configuración. Un fallo de resolución DNS o un puerto incorrecto es la causa más común.

## Paso 5: Ajustar los umbrales del interruptor de circuito (opcional)

El `circuit_breaker_threshold` en `[tier_a]` establece cuántos fallos consecutivos activan el circuito. Un umbral más bajo (p.ej., 3) hace que el circuito se active más rápido ante fallos transitorios; un umbral más alto (p.ej., 10) tolera más errores antes de hacer el respaldo. El valor predeterminado de 5 es apropiado para la mayoría de los despliegues.

Después de cambiar el umbral, reinicie Doorman para que el cambio surta efecto:

```
sudo systemctl restart slm-doorman-server
```

## Puntos clave

- Doorman inicia independientemente de si el Nivel A (DataGraph) es accesible — marca los niveles no disponibles como `OPEN` y enruta al siguiente
- El endpoint `/health` es la fuente autorizada del estado del circuito — léalo directamente o a través de F9 en la consola
- Los ajustes del interruptor de circuito están en `doorman.toml` bajo `[tier_a]`; los cambios requieren un reinicio del servicio
- El Nivel C siempre está disponible; nunca se activa

## Véase también

- [[doorman-protocol]] — el modelo de interruptor de circuito y la lógica de enrutamiento entre niveles
- [[slm-stack-architecture]] — cómo está estructurado el modelo SLM del que depende el Nivel B
- [[run-local-slm-inference]] — verificar que el servicio SLM esté saludable antes de que inicie Doorman
- [[navigate-console-tui]] — leer el estado del Nivel en la barra de estado de la consola
- [[run-first-slm-query]] — enviar su primera solicitud de inferencia una vez que Doorman esté configurado
