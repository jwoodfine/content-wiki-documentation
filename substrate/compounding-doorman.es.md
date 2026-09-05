---
schema: foundry-doc-v1
title: "Doorman compuesto"
slug: compounding-doorman
short_description: "El patrón operativo en el corazón de sustratos de IA soberana: un único servicio que media cada llamada de cómputo externa, registra cada evento en un libro mayor de auditoría y acumula señal de capacitación que compone el sustrato a lo largo del tiempo."
category: substrate
type: topic
content_type: topic
quality: complete
index_group: the-compounding-doorman-and-ai-boundary
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
paired_with: compounding-doorman.md
---

El **Doorman Compuesto** es el patrón operativo que define los sustratos de IA soberanos. Un único servicio media cada llamada de cómputo externo. Registra cada evento en un libro mayor de auditoría inmutable. Y acumula señal de entrenamiento que compone el sustrato con el tiempo: cada interacción hace más precisa la siguiente, sin que ningún dato bruto abandone la infraestructura del cliente.

En la plataforma PointSav, [[service-slm]] es el Doorman Compuesto. Es el único servicio del Anillo 3 de la [[three-ring-architecture]]. Toda solicitud que toque un modelo de inferencia de IA pasa por este límite, y solo por este límite.

## Cuatro disciplinas simultáneas

El Doorman aplica cuatro disciplinas en cada llamada:

**Saneamiento en la vía de aprendizaje.** SYS-ADR-07 prohíbe que los datos estructurados se enruten a través de IA. La lógica de saneamiento del Doorman elimina credenciales e identificadores de cada brief, intento y veredicto antes de capturarlo en el corpus de aprendizaje — la vía que produce datos de entrenamiento. Un saneamiento general de salida y rehidratación de entrada en cada llamada del Anillo 3 es la intención de diseño, aún no construida más allá de esa vía de captura del corpus.

**Enrutamiento de cómputo en tres niveles.** El Doorman selecciona entre tres niveles de cómputo según la forma de la solicitud y la política de presupuesto (ver [[four-tier-slm-substrate]]):
- **Nivel A — local**: OLMo 3 7B en el hardware propio del cliente. Costo marginal cero, localidad total de los datos. Por defecto para la mayoría de las operaciones.
- **Nivel B — ráfaga de GPU**: OLMo 3.1 32B Think en una instancia de GPU de corta duración. Se usa para solicitudes que el nivel local no puede manejar eficientemente. El cliente controla el inicio y la detención; el apagado por inactividad es el comportamiento por defecto.
- **Nivel C — API externa**: APIs de proveedores externos, usadas solo con una lista de permitidos explícita por solicitud. Registrada en el libro de auditoría del cliente, no en el del proveedor.

La configuración de enrutamiento del cliente — umbrales de forma de solicitud y límites de presupuesto por nivel — determina qué nivel maneja cada solicitud. No se requiere selección manual por solicitud.

**Libro mayor de auditoría.** Cada llamada externa produce una entrada que registra el recuento de tokens, el coste estimado, el `moduleId` y el estado de la respuesta. El registro es de solo adición. Un operador que necesite responder "¿tocó la IA este registro, y cuándo?" puede inspeccionar el libro directamente, sin consultar un sistema de terceros. La superficie de auditoría es propiedad del cliente y permanece en su infraestructura.

**Custodia de claves.** Todas las claves de API para los servicios del Nivel C se custodian exclusivamente en el límite del Doorman. Ningún servicio descendente, ningún proceso del Anillo 2, ningún pipeline editorial posee una clave de proveedor. Si una clave se rota o se revoca, el cambio ocurre en un único lugar.

## Por qué se compone con el tiempo

Un despliegue del Doorman Compuesto mejora con el tiempo a través del [[apprenticeship-substrate|sustrato de aprendizaje]]:

- **Al desplegarse**: el Doorman sirve con la base OLMo 3 actual más cualquier adaptador LoRA ya entrenado para este inquilino.
- **Tras el primer ciclo de entrenamiento**: se entrena el primer adaptador LoRA por inquilino con la señal de corpus acumulada. Las tareas que el modelo local antes delegaba al Nivel B ahora pueden resolverse en el Nivel A. Las llamadas al Nivel B se vuelven menos frecuentes; el costo por solicitud cae.
- **A lo largo de múltiples ciclos**: adaptadores adicionales se acumulan en la biblioteca, intercambiados en caliente por solicitud según el tipo de tarea que identifica el Doorman. El modelo se vuelve progresivamente más preciso en los patrones operativos específicos del cliente — los estados de error reales que encuentra, las formas de comando que prefiere, la terminología que utiliza.
- **A través de la federación** (planificado): los clientes que optan por el [[sovereign-ai-commons|compuesto federado]] contribuyen señal de entrenamiento destilada al curador. El curador integra la señal acumulada de muchos despliegues en un modelo base mejorado. La base mejorada regresa a cada despliegue. Ningún dato bruto del cliente sale del [[totebox-archive|almacenamiento controlado por el cliente]].

El bucle de composición se cierra porque el libro mayor de auditoría que registra lo que hizo el Doorman es el mismo sustrato que alimenta los datos de entrenamiento. Cada interacción es simultáneamente un evento operativo y una señal de entrenamiento.

## La metáfora del Doorman

La metáfora se corresponde con precisión a la disciplina operativa:

- Un portero saluda a cada visitante — cada solicitud entra por esta frontera.
- Un portero verifica la identificación — el Doorman valida el `moduleId`.
- Un portero dirige a los visitantes al destino correcto — enrutamiento al nivel local, a la ráfaga de GPU o a la API externa según la política.
- Un portero lleva un registro de quién entró y salió — el libro de auditoría.
- Un portero nunca entra a las habitaciones — el Doorman nunca escribe en el grafo de conocimiento autoritativo; solo propone, conforme a SYS-ADR-07.

La disciplina es lo que hace que la IA soberana sea auditable, reversible y componible.

## Relación con la arquitectura de tres anillos

El Doorman Compuesto es la totalidad del Anillo 3. Es el único punto en el que la IA toca la plataforma. Su postura de solo lectura frente al Anillo 2 no es una limitación sino una garantía arquitectónica: el pipeline determinista de conocimiento en los Anillos 1 y 2 sigue siendo el registro autoritativo sin importar lo que proponga el Anillo 3.

Esto es lo que permite que un despliegue opere el Anillo 3 en cualquier nivel de confianza — desde operaciones totalmente asistidas por IA hasta una configuración donde el Anillo 3 está presente pero toda propuesta requiere aprobación humana explícita antes de entrar al Anillo 2. El Doorman aplica la regla del punto de control humano (SYS-ADR-10) en el punto donde la salida de la IA de otro modo fluiría silenciosamente hacia el grafo de conocimiento.

## Estado de implementación

El Doorman (`service-slm`) está operativo en el servidor del espacio de trabajo. Se enlaza en `127.0.0.1:9080` y enruta el Nivel A al servicio de modelo local. El libro de auditoría escribe archivos diarios (`<AAAA-MM-DD>.jsonl`) en un directorio establecido por `SLM_AUDIT_DIR` — `/var/lib/local-doorman/audit/` en el despliegue del espacio de trabajo, `$HOME/.service-slm/audit/` por defecto cuando no está establecido.

La integración del Nivel B (ráfaga de GPU Yo-Yo) está en desarrollo activo. El enrutamiento de API externa del Nivel C está disponible para tareas de precisión estrecha donde el operador ha configurado explícitamente una lista de permitidos.

El entrenamiento de adaptadores LoRA — el mecanismo que hace que el Doorman se componga — depende del [[brief-queue-substrate|Sustrato de Cola de Briefs]] para la captura del corpus y del [[apprenticeship-substrate|sustrato de aprendizaje]] para el pipeline de entrenamiento. Ambos están operativos o en desarrollo activo.

## Véase también

- [[three-ring-architecture]] — la estructura de anillos que el Doorman Compuesto ocupa (Anillo 3)
- [[service-slm]] — el servicio específico que implementa el Doorman Compuesto
- [[compounding-substrate]] — las cinco propiedades estructurales a las que contribuye el Doorman
- [[brief-queue-substrate]] — la cola durable que mantiene continua la captura del corpus
- [[apprenticeship-substrate]] — cómo los eventos del Doorman generan señal de entrenamiento para adaptadores LoRA
