---
schema: foundry-doc-v1
title: "Cómo consultar el DataGraph"
slug: query-the-datagraph
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: query-the-datagraph.md
---

El DataGraph es el almacén de entidades activo en el centro de `service-content`. Contiene cada persona, organización, proyecto y servicio que el Motor de Gravedad ha identificado y verificado del corpus — la fuente de verdad para el estado de entidades en cualquier momento. Consultar el DataGraph permite buscar el estado actual de entidades, navegar relaciones entre ellas y verificar hechos antes de confirmar contenido.

Para el lugar del DataGraph en el Motor de Gravedad, véase [[service-content]]. Para cómo se extraen las entidades al grafo, véase [[service-extraction]].

## Requisitos previos

- Acceso a la puerta de enlace Doorman (véase [[doorman-protocol]])
- Circuito Nivel A de Doorman en estado activo (verifique la barra de estado del Cartucho SLM)
- Una llamada `query_datagraph` enrutada a través de la interfaz MCP

## Realizar una búsqueda básica de entidad

Llame a `query_datagraph` con una pregunta en texto plano sobre la entidad que busca:

```
query_datagraph("estado del archivo project-editorial")
```

El DataGraph realiza una búsqueda semántica sobre el almacén de entidades y devuelve una lista clasificada de entidades coincidentes. Cada resultado incluye el identificador de la entidad, su tipo y los campos verificados más recientes.

Para un perfil completo de entidad con todos los campos registrados, use `get_entity_context`:

```
get_entity_context("service-content")
```

## Navegar entidades relacionadas

Los resultados de entidades incluyen un campo `related_to` que lista entidades vinculadas por tipo. Para seguir una relación:

1. Lea el resultado de la entidad y anote el identificador de la entidad relacionada.
2. Llame a `get_entity_context("<identificador>")` para recuperar el perfil de la entidad relacionada.

Las relaciones son direccionales — una entidad de proyecto enlaza a los servicios de los que depende, pero una entidad de servicio no lista automáticamente todos los proyectos que la usan. Navegue desde la entidad que conoce hacia la entidad que busca.

## Filtrar resultados por tipo

Agregue una palabra clave de tipo de entidad a la consulta para reducir los resultados:

```
query_datagraph("servicio pipeline de extracción")
query_datagraph("proyecto estado editorial")
```

El DataGraph entiende la taxonomía de entidades de la plataforma: personas, organizaciones, proyectos, servicios, despliegues. Calificar la consulta con el tipo generalmente muestra la entidad correcta en el primer resultado.

## Manejar un circuito Nivel A cerrado

Si el circuito Nivel A de Doorman está `OPEN`, el DataGraph no está disponible. La pila de inferencia cae de vuelta al Nivel B (solo SLM) o Nivel C (respaldo local), pero las llamadas `query_datagraph` fallarán.

Proceda con la siguiente advertencia en el contenido que esté redactando: *"DataGraph no disponible — verificado desde memoria de sesión; compruebe el estado actual antes de confirmar."* No confirme contenido dependiente de entidades durante una interrupción del Nivel A sin la advertencia.

## Puntos clave

- El DataGraph es la autoridad activa para el estado de entidades; la memoria de sesión es una instantánea y puede quedar desactualizada
- Use `get_entity_context` cuando necesite el perfil completo, `query_datagraph` para búsqueda
- Un circuito Nivel A OPEN significa que el DataGraph no está disponible — anote la advertencia y verifique antes de confirmar
- Las entidades relacionadas se recorren llamando a `get_entity_context` con el identificador del primer resultado

## Véase también

- [[service-content]] — el Motor de Gravedad que mantiene el DataGraph
- [[service-extraction]] — cómo las entidades entran al grafo desde documentos del corpus en bruto
- [[doorman-protocol]] — la puerta de enlace que enruta las llamadas al DataGraph y su modelo de interruptor de circuito
- [[app-console-slm]] — el panel de estado de Doorman mostrando los estados del Nivel A/B/C
- [[run-first-slm-query]] — enviar consultas de inferencia una vez que el Nivel A/B está activo
