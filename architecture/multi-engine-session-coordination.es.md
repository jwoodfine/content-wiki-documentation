---
schema: foundry-doc-v1
title: "Coordinación de sesiones multi-motor — bloqueos de sesión, boot_id y guardias de rol"
slug: multi-engine-session-coordination
language: es
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: multi-engine-session-coordination.md
---

La orquestación Totebox admite múltiples motores de IA y operadores humanos trabajando concurrentemente en el mismo anfitrión. El problema de coordinación no es teórico — cuando dos sesiones tocan el mismo `.git/index`, el árbol de trabajo se corrompe de formas costosas de diagnosticar.

## Puntos clave

- Cada motor escribe `.agent/engines/<id-motor>/session.lock` al inicio, con el id del motor, rol, PID, hora de inicio ISO-8601 y el `boot_id` de `/proc/sys/kernel/random/boot_id`. Un `boot_id` diferente en un archivo de bloqueo significa que el anfitrión se reinició entre sesiones — el bloqueo está definitivamente muerto y puede eliminarse automáticamente.
- La sesión concentradora escribe `role.lock` en la raíz del espacio de trabajo; un segundo intento de inicio produce un error en lugar de competir. Las sesiones de archivo delimitan sus bloqueos a su propio directorio `.agent/`, no a la raíz del espacio de trabajo.
- El protocolo advierte sobre conflictos en el mismo archivo pero no impide físicamente una segunda escritura en `.git/index`. Un hook PreToolUse planificado añadirá aplicación en tiempo de escritura. Hasta entonces, la única salvaguarda estructural contra corrupción del índice es el `flock` a nivel OS en `.git/index`.
- Las sesiones concentradoras deben ejecutar la herramienta de verificación del espacio de trabajo al inicio para detectar y limpiar bloqueos obsoletos antes de abrir cualquier archivo — los bloqueos obsoletos de arranques anteriores o PIDs muertos requieren eliminación automática o manual.

El protocolo es intencionalmente minimal: cada motor escribe `.agent/engines/<id-motor>/session.lock` al inicio. El bloqueo contiene el identificador del motor, el rol de sesión, el PID del proceso padre, la hora de inicio en ISO-8601 y el ID de arranque de `/proc/sys/kernel/random/boot_id`. El ID de arranque es la clave — permite que una sesión futura determine si un bloqueo está obsoleto (un ID de arranque diferente significa que el anfitrión se reinició entre sesiones, haciendo que el bloqueo esté definitivamente muerto) o potencialmente vivo (mismo ID de arranque, verificar `kill -0 <pid>` para la actividad del proceso).

El modelo [[totebox-session]] asigna exactamente una sesión concentradora a la raíz del espacio de trabajo. Esa sesión escribe `role.lock` en `.agent/role.lock`; un segundo intento produce un error a menos que el operador borre manualmente el bloqueo. Las sesiones de archivo quedan delimitadas a archivos individuales y escriben sus bloqueos bajo el directorio `.agent/engines/<id-motor>/session.lock` de cada archivo.

Lo que esto no resuelve: dos motores abiertos en el mismo archivo. El protocolo de bloqueo de sesión detecta el conflicto y advierte, pero no lo impide físicamente — para eso está `flock` en `.git/index`. Un hook PreToolUse planificado añadirá una verificación que rechazará cualquier llamada de escritura en un archivo cuyo `session.lock` muestre un motor diferente activo. La herramienta de verificación del espacio de trabajo incluye un detector de `index.lock` entre usuarios que identifica bloqueos en el mismo archivo mantenidos por operadores distintos.

La limpieza de bloqueos obsoletos es automática cuando los IDs de arranque difieren, y manual en los demás casos. Una pasada de limpieza el 2026-05-18 eliminó 8 bloqueos de este tipo — 3 de un arranque anterior y 5 de PIDs muertos en el arranque actual. Las sesiones concentradoras deben ejecutar la herramienta de verificación al inicio y limpiar los bloqueos obsoletos antes de abrir cualquier archivo.

## Véase también

- [[totebox-session]] — el modelo de sesión cuyas garantías de concurrencia protege este protocolo
- [[mailbox-atomicity]] — la disciplina de escritura atómica complementaria para la comunicación entre sesiones
- [[foundry-services-slice-model]] — la partición cgroup que aísla el consumo de recursos en el mismo entorno multi-desarrollador
- [[totebox-orchestration-development]] — la capa de orquestación dentro de la cual operan estas sesiones
