---
schema: foundry-doc-v1
title: "Consultar el DataGraph"
slug: query-the-datagraph
short_description: "Consulta el DataGraph para obtener el estado actual de entidades con las herramientas MCP reales query_datagraph y get_entity_context, y maneja la indisponibilidad del DataGraph como su propia señal, separada de los niveles de inferencia de Doorman."
category: how-to
index_group: records-storage
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Ingenieros (con acceso directo al terminal); operadores de cliente"
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: query-the-datagraph.md
---

## Requisitos previos

- Acceso a las herramientas MCP del DataGraph (`query_datagraph`, `get_entity_context`)
- Disponibilidad del DataGraph (verifique la sección DataGraph del panel F9 — véase [[use-f-key-model]])

## Propósito

Consulte el estado actual y verificado de una entidad en lugar de confiar en la memoria de la sesión, que es una instantánea que se desactualiza. Una consulta toma segundos una vez que sabe a qué herramienta recurrir.

## Procedimiento

1. Para una búsqueda amplia o exploratoria, llame a `query_datagraph` con una consulta de texto libre o palabras clave:

   ```
   query_datagraph(q: "estado del archivo project-editorial")
   ```

   Acepta un `limit` opcional (10 resultados por defecto) y un indicador opcional `format_for_prompt` que devuelve un bloque preformateado listo para pegar en otro prompt.

2. Para un perfil completo de una entidad específica ya identificada, llame a `get_entity_context` con su nombre o identificador:

   ```
   get_entity_context(entity: "service-content")
   ```

3. Para seguir una relación de una entidad a otra, tome el identificador de la entidad que le interesa de su primer resultado y llame a `get_entity_context` sobre esa entidad directamente. Navegue desde la entidad que ya conoce hacia la que busca.

4. Reduzca una consulta amplia añadiendo una palabra clave de tipo de entidad — persona, organización, proyecto, servicio, despliegue — al texto de la consulta; la propia taxonomía del DataGraph suele mostrar la entidad correcta en el primer resultado.

## Resultado esperado

Una lista clasificada de entidades coincidentes de `query_datagraph`, o un perfil completo de entidad de `get_entity_context` — estado actual y verificado, no una instantánea de cuando su propio contexto se actualizó por última vez.

## Verificación

Compare la actualidad del resultado con su propia suposición. Si esperaba un dato que no está en el perfil devuelto, o el perfil es más antiguo de lo que esperaba, trate la respuesta del DataGraph como autoritativa y actualice su propia comprensión, no al revés.

> **Nota:** la disponibilidad del DataGraph no es uno de los niveles de inferencia de Doorman. Los niveles A/B/C determinan hacia dónde se enruta una solicitud de inferencia; el DataGraph es un almacén de entidades en vivo separado con su propio estado, mostrado en su propia sección del panel F9. Ambos pueden estar activos o caídos de forma independiente entre sí.

## Reversión

Las consultas son de solo lectura. Nada que deshacer.

## Próximos pasos

- [[export-structured-data]] — exporte registros de entidades una vez que haya encontrado lo que necesita
- [[use-f-key-model]] — dónde se muestra realmente el propio estado del DataGraph

## Véase también

- [[service-content]] — el servicio que mantiene el DataGraph
- [[service-extraction]] — cómo entran las entidades al grafo desde el corpus en bruto
- [[doorman-protocol]] — la pasarela de enrutamiento de inferencia separada y su modelo de niveles
