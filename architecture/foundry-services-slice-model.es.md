---
schema: foundry-doc-v1
title: "Partición cgroup para entornos de múltiples desarrolladores — la capa de servicios"
slug: foundry-services-slice-model
short_description: "Una reserva de memoria cgroup de systemd que protege los servicios de producción de ser desalojados por procesos pesados de compilación o investigación en el mismo host — aislamiento de un solo nodo sin Kubernetes."
language: es
category: architecture
index_group: customer-ownership-and-deployment
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-18
editor: pointsav-engineering
cites: []
paired_with: foundry-services-slice-model.md
---

El entorno de desarrollo de [[pointsav-overview|PointSav]] ejecuta servicios de producción y sesiones de ingeniería interactivas en el mismo servidor Linux. El patrón de capa de servicios del espacio de trabajo garantiza que los picos de recursos de las sesiones de compilación no priven a los servicios de inferencia y libro mayor de los que dependen otros operadores durante la misma sesión.

## Puntos clave

- `foundry-services.slice` reserva 12G de RAM (`MemoryMin=12G`, en un host de 31G) que el kernel no reclamará de los servicios de la plataforma ni siquiera bajo presión severa de memoria del host — una garantía, no un techo.
- Un servicio, `local-content` (el grafo de entidades), lleva protección adicional: su propio `MemoryMin` de 2G más `OOMScoreAdjust=-200`, lo que lo convierte en un candidato tardío para el último recurso de eliminación del kernel. Ningún otro servicio lleva esta protección hoy.
- Este esquema no es Kubernetes. No hay planificador, ni controlador de réplicas, ni malla de servicios, ni planificación por peso de CPU — solo una reserva de memoria más la protección OOM de un servicio. Apropiado para un despliegue de nodo único con hasta aproximadamente 12 servicios.
- La disciplina cgroup se mantiene cuando aumenta la escala. El patrón de drop-in `Slice=` por servicio es compatible con una orquestación multinodo más compleja.

## Contención de recursos en un servidor compartido

El entorno de desarrollo de [[pointsav-overview|PointSav]] ejecuta servicios de producción y sesiones de ingeniería interactivas en el mismo servidor Linux. Los servicios de la plataforma (el SLM local, [[doorman-protocol|Doorman]], el [[service-content|grafo de contenido]], el escritor del ledger y el corrector) comparten memoria con sesiones de compilación de múltiples operadores y procesos por lotes de investigación/GIS. Sin protección, un proceso pesado en memoria fuera del slice puede desalojar el conjunto de trabajo de un servicio de la plataforma bajo presión del host — `service-content` sufrió esto exactamente, quedando sin responder cuando un proceso Python externo agotó la RAM del host.

## Una reserva de memoria, no un esquema de CPU u ordenación OOM

`foundry-services.slice` establece `MemoryMin=12G` en un host de 31G: un piso que el kernel no reclamará para ningún servicio del slice, incluso bajo presión severa — dimensionado como el conjunto de trabajo de ~7G del SLM local, la propia reserva de 2G de `local-content`, y un búfer de 3G para el resto de servicios de la plataforma. No existe ningún ajuste `CPUWeight` en este slice ni en ningún otro lugar del monorepo; la planificación de CPU no forma parte de este mecanismo.

Solo `local-content` lleva protección adicional más allá del piso a nivel de slice: su propio `MemoryMin=2G` (más `MemoryHigh=5500M`, `MemoryMax=6G`, y `MemorySwapMax=0` — nunca se intercambia a disco, ya que un grafo de entidades parcialmente en swap no puede servir consultas en tiempo real), y `OOMScoreAdjust=-200`. Ese puntaje negativo indica al eliminador OOM del kernel que trate a `local-content` como candidato tardío — el grafo tarda minutos en reconstruirse si se elimina. Ningún otro servicio de la plataforma (`local-doorman`, el SLM local) lleva su propio ajuste `OOMScoreAdjust` hoy; una jerarquía de tres niveles se describe en los comentarios de configuración de `local-content` como justificación de su valor, pero solo se aplica realmente el puntaje propio de `local-content`.

## Alcance de nodo único sin Kubernetes

Este esquema no es orquestación en el sentido de Kubernetes — no hay planificador, ni controlador de réplicas, ni malla de servicios. systemd es suficiente. El patrón escala a aproximadamente una docena de servicios en una sola VM de GCE, la configuración de nodo único compacta que caracteriza un despliegue soberano mínimo. Más allá de esa escala, la arquitectura cambia — pero la disciplina cgroup se mantiene.

Instalado como `/etc/systemd/system/foundry-services.slice`, más drop-ins de memoria y protección OOM por servicio bajo el propio directorio `.service.d/` de cada servicio protegido.

## Véase también

- [[multi-engine-session-coordination]] — cómo las sesiones concurrentes de codificación asistida por IA coordinan el acceso al espacio de trabajo para prevenir corrupción del índice
- [[cargo-target-per-user-discipline]] — separación de la caché de compilación por usuario para el mismo escenario de múltiples desarrolladores
- [[totebox-session]] — el modelo de sesión que siguen los flujos de trabajo individuales de los desarrolladores
- [[totebox-orchestration-development]] — el patrón de orquestación en la capa de entorno de desarrollo
