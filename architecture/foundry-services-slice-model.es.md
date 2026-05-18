---
schema: foundry-doc-v1
title: "Partición cgroup para Entornos de Múltiples Desarrolladores — la Capa de Servicios"
slug: foundry-services-slice-model
language: es
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-18
editor: pointsav-engineering
cites: []
paired_with: foundry-services-slice-model.md
---

El entorno de desarrollo funciona como una plataforma multi-inquilino: los servicios de producción (local-slm, local-doorman, local-content, local-fs, local-proofreader) comparten el mismo servidor Linux con sesiones interactivas de codificación asistida por IA (Claude Code, Gemini CLI) y shells de operadores humanos. Sin aislamiento de recursos, una compilación `cargo build` pesada en la sesión de un operador puede privar al SLM OLMo del acceso a CPU justo cuando otro operador depende de él para inferencia.

Una pasada inicial de endurecimiento introdujo `foundry-services.slice` — una partición cgroup de systemd con `CPUWeight=200` y `MemoryHigh=11G` que contiene todos los `local-*.service`. Los slices de usuario predeterminados de systemd se sitúan en `CPUWeight=100`, por lo que bajo contención de CPU el grupo de servicios recibe el doble de peso del planificador en comparación con una shell interactiva. Los techos de memoria impiden que cualquier servicio fije más de aproximadamente 11 GiB en una VM de 16 GiB; con la ordenación `OOMScoreAdjust` (sshd −1000, local-fs −500, local-doorman −300, local-slm +500), el último recurso del kernel para liberar memoria prefiere matar servicios fáciles de reiniciar antes que el escritor del ledger WORM o la conexión SSH del operador.

Este esquema no es orquestación en el sentido de Kubernetes — no hay planificador, ni controlador de réplicas, ni malla de servicios. systemd es suficiente. El patrón escala a aproximadamente una docena de servicios en una sola VM de GCE, la configuración de nodo único compacta que caracteriza un despliegue soberano mínimo. Más allá de esa escala, la arquitectura cambia — pero la disciplina cgroup se mantiene.

Ubicación en disco: `/etc/systemd/system/foundry-services.slice`, más drop-ins `Slice=foundry-services.slice` en `/etc/systemd/system/local-*.service.d/slice.conf`. Los espejos del código fuente bajo control de versiones viven en `infrastructure/`.

## Véase también

- [[multi-engine-session-coordination]] — cómo las sesiones concurrentes de codificación asistida por IA coordinan el acceso al espacio de trabajo para prevenir corrupción del índice
- [[cargo-target-per-user-discipline]] — separación de la caché de compilación por usuario para el mismo escenario de múltiples desarrolladores
- [[totebox-session]] — el modelo de sesión que siguen los flujos de trabajo individuales de los desarrolladores
- [[totebox-orchestration-development]] — el patrón de orquestación en la capa de entorno de desarrollo
