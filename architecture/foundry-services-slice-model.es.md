---
schema: foundry-doc-v1
title: "Partición cgroup para entornos de múltiples desarrolladores — la capa de servicios"
slug: foundry-services-slice-model
short_description: "Particionado de cgroups de systemd que da a los servicios de producción el doble de peso de CPU frente a sesiones interactivas — aislamiento de un solo nodo sin Kubernetes."
language: es
category: architecture
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

- `foundry-services.slice` otorga a los servicios de producción el doble de peso en el planificador de CPU frente a una shell interactiva de usuario. Bajo contención, los servicios tienen prioridad sobre los trabajos de compilación.
- Los techos de memoria (`MemoryHigh=11G`) impiden que cualquier servicio fije toda la memoria de 16 GiB de la VM. La ordenación `OOMScoreAdjust` — sshd en −1000, local-fs en −500, local-doorman en −300, local-slm en +500 — hace que el kernel elimine primero los servicios más fáciles de reiniciar.
- Este esquema no es Kubernetes. No hay planificador, ni controlador de réplicas, ni malla de servicios — solo partición cgroup de systemd. Apropiado para un despliegue de nodo único con hasta aproximadamente 12 servicios.
- La disciplina cgroup se mantiene cuando aumenta la escala. El patrón de drop-in `Slice=` por servicio es compatible con una orquestación multinodo más compleja.

## Contención de recursos en un servidor compartido

El entorno de desarrollo de [[pointsav-overview|PointSav]] ejecuta servicios de producción y sesiones de ingeniería interactivas en el mismo servidor Linux. Los servicios de la plataforma (el SLM local, [[doorman-protocol|Doorman]], el [[service-content|grafo de contenido]], el escritor del ledger y el corrector) comparten CPU y memoria con sesiones de compilación de múltiples operadores. Sin aislamiento de recursos, una compilación `cargo build` pesada en la sesión de un operador puede privar al servicio de inferencia justo cuando otro operador depende de él.

## Pesos de CPU, techos de memoria y ordenación OOM

Una pasada inicial de endurecimiento introdujo `foundry-services.slice` — una partición cgroup de systemd con `CPUWeight=200` y `MemoryHigh=11G` que contiene todos los `local-*.service`. Los slices de usuario predeterminados de systemd se sitúan en `CPUWeight=100`, por lo que bajo contención de CPU el grupo de servicios recibe el doble de peso del planificador en comparación con una shell interactiva. Los techos de memoria impiden que cualquier servicio fije más de aproximadamente 11 GiB en una VM de 16 GiB; con la ordenación `OOMScoreAdjust` (sshd −1000, local-fs −500, local-doorman −300, local-slm +500), el último recurso del kernel para liberar memoria prefiere matar servicios fáciles de reiniciar antes que el escritor del ledger WORM o la conexión SSH del operador.

**Corrección (2026-07-18):** el `foundry-services.slice` real en el monorepo
(`infrastructure/systemd/foundry-services.slice`) no coincide con esta descripción.
Establece `MemoryMin=12G` (una garantía de reserva de memoria contra desalojo bajo presión
del host, dimensionada para un host de 31G, no un techo de 11G en una VM de 16G) — no
aparece ningún ajuste `CPUWeight` en el archivo del slice, y una búsqueda en todo el
monorepo no encuentra `CPUWeight` en ningún lugar. El mecanismo descrito en los propios
comentarios del archivo es de otra naturaleza: presupuesto por servicio vía `MemoryMin`
(local-content/LadybugDB recibe una garantía de 2G; local-slm y local-doorman no tienen
ninguna establecida), no un esquema de peso de CPU/OOMScoreAdjust. El único ajuste
`OOMScoreAdjust` encontrado en todo el monorepo está en `local-content` (`-200`,
"moderadamente protegido") — no la ordenación de cuatro servicios sshd/local-fs/
local-doorman/local-slm que describe este artículo. **Señalado, no reescrito
silenciosamente** — esto se lee como un diseño anterior sustituido por un mecanismo más
simple basado solo en reserva de memoria, pero necesita confirmación de project-totebox
antes de corregir o eliminar las afirmaciones sobre peso de CPU y ordenación OOM.

## Alcance de nodo único sin Kubernetes

Este esquema no es orquestación en el sentido de Kubernetes — no hay planificador, ni controlador de réplicas, ni malla de servicios. systemd es suficiente. El patrón escala a aproximadamente una docena de servicios en una sola VM de GCE, la configuración de nodo único compacta que caracteriza un despliegue soberano mínimo. Más allá de esa escala, la arquitectura cambia — pero la disciplina cgroup se mantiene.

Ubicación en disco: `/etc/systemd/system/services.slice`, más drop-ins `Slice=` bajo `/etc/systemd/system/local-*.service.d/slice.conf`. Los espejos del código fuente bajo control de versiones viven en el directorio `infrastructure/` del monorepo.

**Corrección (2026-07-18):** los nombres del código fuente bajo control de versiones no
coinciden con esas rutas. El archivo del slice es
`infrastructure/systemd/foundry-services.slice` (no `services.slice`), y los únicos
drop-ins encontrados son `local-content-memory.conf` y `local-content-oom.conf` (no un
`slice.conf` genérico por servicio). Señalado junto con la corrección de peso de CPU/
ordenación OOM anterior — la misma desactualización subyacente.

## Véase también

- [[multi-engine-session-coordination]] — cómo las sesiones concurrentes de codificación asistida por IA coordinan el acceso al espacio de trabajo para prevenir corrupción del índice
- [[cargo-target-per-user-discipline]] — separación de la caché de compilación por usuario para el mismo escenario de múltiples desarrolladores
- [[totebox-session]] — el modelo de sesión que siguen los flujos de trabajo individuales de los desarrolladores
- [[totebox-orchestration-development]] — el patrón de orquestación en la capa de entorno de desarrollo
