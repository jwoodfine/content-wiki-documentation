---
schema: foundry-doc-v1
title: "Cómo ejecutar su primera consulta SLM"
slug: run-first-slm-query
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: run-first-slm-query.md
---

El Cartucho SLM en F9 enruta solicitudes de inferencia a través de Doorman hacia el modelo de lenguaje local. No se transmiten datos del prompt a un proveedor externo — el modelo se ejecuta localmente. Esta guía cubre cómo abrir la ranura SLM, verificar que Doorman tiene un circuito activo y enviar su primer prompt.

Para la arquitectura de inferencia, véase [[app-console-slm]] y [[slm-stack-architecture]]. Para configurar la pila de inferencia en un nuevo despliegue, véase [[run-local-slm-inference]].

## Requisitos previos

- Una sesión Totebox activa con F9 disponible
- El servicio SLM local ejecutándose en la instancia anfitriona
- Doorman ejecutándose y accesible en el puerto local

## Pasos

### 1. Abrir el Cartucho SLM

Presione **F9**. El panel de estado de Doorman llena el área de ranura. Muestra tres filas:

| Fila | Lo que muestra |
|---|---|
| Nivel A | Disponibilidad del DataGraph (service-content) |
| Nivel B | Disponibilidad del modelo SLM |
| Nivel C | Disponibilidad del respaldo local |

Un indicador verde significa que el nivel está disponible; un indicador rojo o `OPEN` significa que el interruptor de circuito se ha activado y ese nivel se omite temporalmente.

### 2. Confirmar que la inferencia está disponible

Para que la inferencia funcione, al menos el Nivel B debe mostrar un circuito activo. Si el Nivel B muestra `OPEN`, presione **R** para actualizar. Si permanece abierto, el servicio SLM local puede no estar ejecutándose — véase [[run-local-slm-inference]] para los pasos de inicio.

### 3. Enviar un prompt

Navegue a la línea de entrada del prompt (mostrada en la parte inferior del área de ranura). Escriba su prompt y presione **Enter**. La respuesta se transmite al área de ranura sobre la línea de entrada.

Los prompts son procesados únicamente por el modelo local. El contexto proviene de la sesión Totebox y las entidades del DataGraph conectado, no de fuentes externas.

### 4. Leer la respuesta

La respuesta se transmite token por token. Al completarse, el cursor regresa a la línea de entrada. Para comenzar un nuevo prompt, escriba y presione Enter nuevamente. Las respuestas anteriores permanecen visibles al desplazarse hacia arriba.

Presione **Esc** para borrar el prompt actual sin enviarlo.

## Verificar el nivel de inferencia en la barra de estado

La barra de estado muestra el nivel SLM actual como una sola letra (`A`, `B` o `C`) junto a la etiqueta de ranura activa. Esto se actualiza en tiempo real conforme cambian los estados del circuito. Si el nivel cae durante un prompt de larga ejecución, la respuesta puede truncarse — reenvíe cuando el circuito se recupere.

## Puntos clave

- Doorman es la puerta de enlace — el Cartucho nunca se conecta directamente al modelo
- Se necesita al menos el Nivel B para inferencia; se necesita el Nivel A para contexto de entidades del DataGraph
- Presione R en F9 para actualizar el estado del circuito sin cambiar de ranura
- Toda la inferencia es local; ningún dato sale del equipo anfitrión

## Véase también

- [[app-console-slm]] — el Cartucho SLM y el panel de estado de Doorman
- [[slm-stack-architecture]] — la pila de inferencia completa y definiciones de niveles
- [[doorman-protocol]] — el modelo de interruptor de circuito de Doorman y reglas de enrutamiento
- [[run-local-slm-inference]] — iniciar el servicio SLM y Doorman en una nueva instancia
- [[navigate-console-tui]] — fundamentos de navegación de la consola
