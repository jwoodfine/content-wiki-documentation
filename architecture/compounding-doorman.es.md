---
schema: foundry-doc-v1
title: "El Doorman Compuesto"
slug: compounding-doorman.es
category: architecture
type: topic
quality: complete
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: compounding-doorman.md
---

## Adaptación estratégica — El Doorman Compuesto

El **Doorman Compuesto** es el patrón operativo que define los sustratos de IA soberanos. Un único servicio media cada llamada de cómputo externo. Aplica la disciplina de saneamiento y rehidratación en ambos extremos de la llamada. Registra cada evento en un libro mayor de auditoría inmutable. Y acumula señal de entrenamiento que compone el sustrato con el tiempo: cada interacción hace más precisa la siguiente, sin que ningún dato bruto abandone la infraestructura del cliente.

En la plataforma PointSav, `service-slm` es el Doorman Compuesto. Es el único servicio del Anillo 3 de la [[three-ring-architecture]]. Toda solicitud que toque un modelo de inferencia de IA pasa por este límite, y solo por este límite.

## Cuatro disciplinas simultáneas

El Doorman aplica cuatro disciplinas en cada llamada:

**Sanear los datos salientes, rehidratar los entrantes.** SYS-ADR-07 prohíbe que los datos estructurados se enruten a través de IA. Antes de que cualquier solicitud cruce el límite del Doorman, los identificadores, las claves foráneas y los campos estructurados se sustituyen por tokens opacos. Tras recibir la respuesta, los tokens se resuelven de vuelta a sus valores originales. El modelo de IA recibe y devuelve solo prosa y tokens opacos; nunca ve ni devuelve registros estructurados. Esto hace que la ruta de auditoría sea reversible y verificable.

**Enrutamiento de cómputo en tres niveles.** El Doorman selecciona entre tres niveles de cómputo según la forma de la solicitud y la política de presupuesto: Nivel A (OLMo 3 7B local en el hardware propio del cliente, coste marginal cero), Nivel B (OLMo 3.1 32B Think en una instancia de GPU efímera), y Nivel C (APIs de proveedores externos con lista de permitidos explícita por solicitud). La configuración del cliente determina la selección; no se requiere elección manual por solicitud.

**Libro mayor de auditoría.** Cada llamada externa produce una entrada que registra el recuento de tokens, el coste estimado, el `moduleId` y el estado de la respuesta. El registro es de solo adición y reside en la infraestructura del cliente.

**Custodia de claves.** Todas las claves de API para los servicios del Nivel C se custodian exclusivamente en el límite del Doorman. Ningún servicio descendente ni proceso del Anillo 2 posee una clave de proveedor.

## Por qué se compone con el tiempo

Un despliegue del Doorman Compuesto mejora con el uso a través del sustrato de aprendizaje. Tras el primer ciclo de entrenamiento, se entrena el primer adaptador LoRA por tenant con la señal de corpus acumulada. Las tareas que el modelo local antes delegaba al Nivel B pueden pasar a resolverse en el Nivel A, reduciendo el coste por solicitud. Con múltiples ciclos, el modelo se vuelve progresivamente más preciso en los patrones operativos específicos del cliente — los estados de error reales que encuentra, las formas de comando que prefiere, la terminología que utiliza.

La clave del patrón es que el libro mayor de auditoría que registra lo que hizo el Doorman es el mismo sustrato que alimenta los datos de entrenamiento. Cada interacción es a la vez un evento operativo y una señal de entrenamiento. El bucle se cierra estructuralmente, no por configuración.

## Estado de implementación

El Doorman (`service-slm`) está operativo en el servidor del espacio de trabajo. La integración del Nivel B (ráfaga de GPU Yo-Yo) está en desarrollo activo. El entrenamiento de adaptadores LoRA — el mecanismo que hace que el Doorman se componga — depende del Sustrato de Cola de Briefs para la captura del corpus y del sustrato de aprendizaje para la cadena de entrenamiento. La especificación técnica completa está disponible en inglés en el artículo principal.

## Véase también

- [[three-ring-architecture]] — la estructura de anillos que el Doorman Compuesto ocupa (Anillo 3)
- [[service-slm]] — el servicio específico que implementa el Doorman Compuesto
- [[compounding-substrate]] — las cinco propiedades estructurales a las que contribuye el Doorman
- [[brief-queue-substrate]] — la cola durable que mantiene continua la captura del corpus
- [[apprenticeship-substrate]] — cómo los eventos del Doorman generan señal de entrenamiento para adaptadores LoRA

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
