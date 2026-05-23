---
schema: foundry-doc-v1
title: "Defensa en profundidad pre-commit — Análisis de secretos, límite de tamaño y puerta de ayudante"
slug: pre-commit-defense-in-depth
language: es
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-18
editor: pointsav-engineering
cites: []
paired_with: pre-commit-defense-in-depth.md
---

Tres incidentes en la canalización de confirmaciones en 2026 — una clave SSH que llegó a un monorepo público, una anulación de autor en `.git/config` que atribuyó incorrectamente cientos de confirmaciones, y carreras de reversión de chmod contra el almacén de identidad — comparten una causa estructural: no existía ninguna barrera entre un participante del espacio de trabajo y `git commit`. Cualquier agente, cualquier operador, podía escribir cualquier contenido y confirmar de cualquier manera.

El endurecimiento de la Fase 1 cierra esta brecha con un único hook pre-commit: `bin/pre-commit-foundry-gate.sh`, enlazado simbólicamente en `.git/hooks/pre-commit` en la raíz del espacio de trabajo y en cada clon de archivo. Ejecuta tres verificaciones en cada confirmación.

**Confirmaciones solo mediante ayudante.** El hook rechaza a menos que `FOUNDRY_COMMIT_HELPER=1` esté configurado en el entorno. `bin/commit-as-next.sh` establece esta variable antes de invocar `git commit`. Las invocaciones directas de `git commit` — por un operador, un agente o automatización — reciben un mensaje de error claro que apunta al ayudante. Las confirmaciones de fusión y los rebases se permiten mediante la detección de `GIT_REFLOG_ACTION`; las emergencias pueden omitir con `--no-verify`. El costo de la regla es una confirmación redirigida; el beneficio es el fin de toda la clase de errores de "autor incorrecto".

**Análisis de patrones de secretos.** El hook lee `conventions/secret-patterns.yaml` y analiza el contenido preparado contra 17 patrones de expresión regular: claves privadas SSH/PGP (OPENSSH, RSA, EC, DSA, PGP), credenciales en la nube (AWS, GCP, GitHub PAT, tokens OAuth), claves API (Anthropic, OpenAI, Slack) y asignaciones genéricas de contraseñas. Las coincidencias de severidad crítica y alta bloquean la confirmación; las de severidad media y baja producen una advertencia y continúan. Una lista de rutas permitidas exime el catálogo de patrones en sí y los archivos de clave pública.

**Guardia de tamaño.** Los blobs de más de 2 MiB se rechazan a menos que la ruta esté en la lista de tamaños permitidos (`data/binary-ledger/`, repositorios de activos multimedia, `www/` de fleet-deployment). Esto detecta la confirmación accidental de binarios — imágenes grandes, artefactos de compilación copiados, bases de datos integradas — antes de la contaminación del historial.

La implementación en Python es de aproximadamente 150 líneas; PyYAML es la única dependencia externa. Para una confirmación típica de 5 a 20 archivos, el hook agrega menos de un segundo. Para confirmaciones inusualmente grandes, la guardia de tamaño detecta la sobrecarga antes de que el análisis de secretos tenga que leerla.

Lo que esto no resuelve: la omisión mediante `--no-verify`, o una confirmación en un clon del espacio de trabajo sin el hook instalado. Lo primero es intencional — un operador con una razón legítima puede omitir con una entrada completa en el registro de auditoría. Lo segundo lo cierra `bin/onboarding/new-archive.sh`, que instala el enlace simbólico del hook cada vez que se aprovisiona un archivo.

## Véase también

- [[multi-engine-session-coordination]] — el protocolo de bloqueo de sesión que cierra una clase complementaria de defectos de coordinación
- [[identity-ledger-schema-design]] — la arquitectura de identidad cuya integridad protege la puerta de solo ayudante
- [[totebox-session]] — el modelo de sesión al que sirve la ruta de confirmación del ayudante
- [[learning-datagraph-architecture]] — el bucle de aprendizaje cuyos hooks de captura de trayectorias se ejecutan en la misma canalización pre-commit
