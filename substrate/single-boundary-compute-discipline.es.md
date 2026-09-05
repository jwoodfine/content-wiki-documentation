---
schema: foundry-doc-v1
title: "Disciplina de cómputo de límite único"
slug: single-boundary-compute-discipline
category: substrate
type: topic
content_type: topic
quality: complete
index_group: the-compounding-doorman-and-ai-boundary
short_description: "Todo el tráfico de inferencia de IA en un despliegue de la plataforma pasa exclusivamente por el Portero, con la omisión estructuralmente impedida a nivel de kernel."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: single-boundary-compute-discipline.md
---


La **Disciplina de Cómputo de Límite Único** establece que todo el tráfico de inferencia de IA en un despliegue de la plataforma pasa por un único punto de frontera: el [[compounding-doorman|Portero]] (`service-slm`). Ningún proceso, sesión ni servicio accede a un nivel de inferencia —local, [[yoyo-compute-substrate|GPU en ráfaga]] o API externa— excepto a través de esta frontera.

## Por qué un solo límite

Un único punto de frontera garantiza estructuralmente cuatro propiedades clave:

**Integridad del registro de auditoría.** El [[worm-ledger-architecture|registro de auditoría]] captura cada llamada de inferencia. Un operador que necesite saber si la IA tocó un registro específico obtiene una respuesta definitiva al consultar el registro. Si existiera una ruta alternativa, el registro tendría lagunas, lo que lo haría inadmisible como evidencia de cumplimiento.

**Integridad del corpus de entrenamiento.** El [[apprenticeship-substrate|substrato de aprendizaje]] captura cada llamada mediada por el Portero como una tupla de entrenamiento. Las llamadas que evaden el Portero no producen ningún ejemplo de aprendizaje; las lagunas en el corpus degradan permanentemente la calidad del [[adapter-composition|adaptador]] por inquilino.

**Control de costos.** Los límites de presupuesto y los interruptores de emergencia operan en la frontera del Portero. Las llamadas que evaden esa frontera también evaden los controles de gasto.

**Soberanía.** Las claves de API y los tokens de autenticación para el cómputo externo residen exclusivamente en el entorno del Portero. Ningún otro proceso los posee. Cuando se rota una clave, el cambio ocurre en un único lugar.

## Qué aplica la frontera realmente hoy

Los secretos de inferencia viven únicamente en el archivo de entorno del Portero. La dirección de enlace por defecto del Portero es `127.0.0.1`, no una interfaz alcanzable por red — un proceso en la misma máquina puede alcanzarlo, pero nada fuera de ella, sin un proxy inverso o reenvío de puerto configurado deliberadamente.

Dos mecanismos que este artículo describía antes como ya aplicados no cuentan hoy con respaldo de código: una regla de iptables a nivel de kernel que restrinja el servidor de inferencia local a conexiones solo del proceso del Portero, y una verificación de arranque que rechace iniciar sin un token de autenticación de ráfaga GPU. El comportamiento real de arranque asigna una cadena vacía cuando el token no está definido, en lugar de negarse a arrancar — una brecha real entre la disciplina prevista y lo que se aplica hoy, no una decisión de diseño. Restringir la instancia de GPU en ráfaga a la IP del Portero es un control real y estándar a nivel de redes en la nube, independiente del código de la aplicación.

## Relación con la arquitectura de tres anillos

El [[compounding-doorman|Portero]] es el único punto de entrada al Anillo 3. La [[three-ring-architecture|arquitectura de tres anillos]] hace que el Anillo 3 sea estructuralmente opcional; la disciplina de límite único garantiza que deshabilitar ese punto produce un estado degradado limpio en lugar de un estado parcialmente comprometido. Para operaciones determinísticas en los Anillos 1 y 2, el substrato funciona completamente sin el Portero activo en modo de inferencia.

## Composición con otras reclamaciones

Esta disciplina compone con varios otros patrones de substrato. [[knowledge-graph-grounded-apprenticeship]] depende de ella: el contexto del grafo se ensambla en el Portero antes del despacho; evitarla implica inferencia sin fundamentación. [[mcp-substrate-protocol]] designa al Portero como la puerta de enlace MCP; evitarla rompe el grafo MCP. El substrato soberano aplica la soberanía del cliente en la frontera del Portero; evitarla es una fuga de soberanía.

## Véase También

- [[knowledge-graph-grounded-apprenticeship]] — fundamentación del grafo ensamblada en la frontera del Portero
- [[mcp-substrate-protocol]] — el Portero como puerta de enlace MCP
- [[substrate-without-inference-base-case]] — operación determinística cuando los niveles de inferencia no están disponibles
