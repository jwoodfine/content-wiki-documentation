---
schema: foundry-doc-v1
title: "Disciplina de Cómputo de Límite Único"
slug: single-boundary-compute-discipline.es
category: architecture
type: topic
quality: published
short_description: "Todo el tráfico de inferencia de IA en un despliegue Foundry pasa exclusivamente por el Portero, con la omisión estructuralmente impedida a nivel de kernel."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: single-boundary-compute-discipline.md
---

La **Disciplina de Cómputo de Límite Único** establece que todo el tráfico de inferencia de IA en un despliegue Foundry pasa por un único punto de frontera: el Portero (`service-slm`). Ningún proceso, sesión ni servicio accede a un nivel de inferencia —local, GPU en ráfaga o API externa— excepto a través de esta frontera. Esta disciplina codifica la reclamación doctrinal #43.

## Por qué un solo límite

Un único punto de frontera garantiza estructuralmente cuatro propiedades clave:

**Integridad del registro de auditoría.** El registro de auditoría captura cada llamada de inferencia. Un operador que necesite saber si la IA tocó un registro específico obtiene una respuesta definitiva al consultar el registro. Si existiera una ruta alternativa, el registro tendría lagunas, lo que lo haría inadmisible como evidencia de cumplimiento.

**Integridad del corpus de entrenamiento.** El substrato de aprendizaje captura cada llamada mediada por el Portero como una tupla de entrenamiento. Las llamadas que evaden el Portero no producen ningún ejemplo de aprendizaje; las lagunas en el corpus degradan permanentemente la calidad del adaptador por inquilino.

**Control de costos.** Los límites de presupuesto y los interruptores de emergencia operan en la frontera del Portero. Las llamadas que evaden esa frontera también evaden los controles de gasto.

**Soberanía.** Las claves de API y los tokens de autenticación para el cómputo externo residen exclusivamente en el entorno del Portero. Ningún otro proceso los posee. Cuando se rota una clave, el cambio ocurre en un único lugar.

## Cuatro mecanismos de cumplimiento

La disciplina se hace cumplir a nivel estructural, no como política:

Los secretos de inferencia viven únicamente en el archivo de entorno del Portero. Las reglas de cortafuegos restringen las instancias de GPU en ráfaga para aceptar conexiones únicamente desde el IP del Portero. El servidor de inferencia local acepta conexiones únicamente desde el UID del proceso del Portero, aplicado mediante reglas de iptables a nivel de kernel. Y el Portero verifica la presencia del token de autenticación en el inicio y se niega a arrancar si falta.

## Relación con la arquitectura de tres anillos

El Portero es el único punto de entrada al Anillo 3. La arquitectura de tres anillos hace que el Anillo 3 sea estructuralmente opcional; la disciplina de límite único garantiza que deshabilitar ese punto produce un estado degradado limpio en lugar de un estado parcialmente comprometido. Para operaciones determinísticas en los Anillos 1 y 2, el substrato funciona completamente sin el Portero activo en modo de inferencia.

## Composición con otras reclamaciones

Esta disciplina es un requisito previo estructural para el Aprendizaje Fundamentado en Grafos de Conocimiento (#44): el contexto del grafo se ensambla en el Portero antes del despacho; evitar el Portero produce inferencia sin contexto. También es un requisito previo para el Protocolo Substrato MCP (#46): el Portero es la puerta de enlace MCP; la evasión rompe la integración del grafo. Y es la forma operativa de la soberanía del cliente en el Substrato Soberano de Dos Fondos (#34).

## Véase También

- [[knowledge-graph-grounded-apprenticeship]] — fundamentación del grafo ensamblada en la frontera del Portero
- [[mcp-substrate-protocol]] — el Portero como puerta de enlace MCP
- [[substrate-without-inference-base-case]] — operación determinística cuando los niveles de inferencia no están disponibles

---

## Procedencia

Resumen de adaptación estratégica del archivo fuente `convention-single-boundary-compute-discipline.md` (refinado el 30 de abril de 2026). El cuerpo en español es una síntesis orientada estratégicamente, no una traducción literal.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
