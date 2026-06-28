---
artifact: topic
schema: foundry-draft-v1
status: draft
language_protocol: TOPIC
route: project-editorial
target_wiki: documentation.pointsav.com
created: 2026-06-20
session: Session 111 (Command@claude-code)
research_trail:
  source_briefs: [command-10x-dev-environment]
  cross_checks: [BRIEF-10x-dev-environment.md, pairings.yaml, AGENT.md]
  forbidden_terms_cleared: false
---

# El modelo de ramas por archivo en app-orchestration-command

Cada Totebox Archive en la topología de `app-orchestration-command` opera en su propia rama aislada, separada del `main` canónico que gestiona el coordinador. Este artículo explica por qué existe ese aislamiento, qué protege y cómo el coordinador hace cumplir el límite durante la publicación.

## Por qué existen ramas aisladas

La rama aislada de un Totebox Archive funciona como una superficie de desarrollo privada. Contiene el historial de trabajo completo del archivo: commits de código, commits de estado operativo y cualquier punto intermedio. El `main` canónico, en cambio, contiene únicamente lo que ha sido publicado —código que superó la puerta de pre-publicación, está firmado y figura de forma permanente en el registro.

Las ramas aisladas existen por dos razones:

1. **Prevención de contaminación.** Sin aislamiento, cada commit de sesión —incluidas notas operativas, borradores y actualizaciones de memoria de sesión— correría el riesgo de entrar en el historial canónico. La rama aislada es la capa de contención. Solo el filtro de publicación del coordinador decide qué cruza hacia el historial canónico.
2. **Ritmo independiente.** Veintiún archivos ejecutándose en una única rama compartida se bloquearían constantemente entre sí. Cada rama aislada se desarrolla a su propio ritmo. Los commits en la rama de un archivo no tienen efecto sobre la de otro.

## Qué llega al historial canónico

Cuando el coordinador publica el trabajo de un archivo, selecciona únicamente los commits que modifican código fuente:

- Archivos fuente (`.rs`, `.ts`, `.html`, `.css` y similares)
- Manifiestos de compilación (`Cargo.toml`, `Cargo.lock`, archivos de paquete)
- Pruebas y datos de prueba
- Documentación incluida con el código (en línea, archivos `README.md` dentro del paquete)

Estos commits se aplican a `origin/main` como una integración de avance rápido (*fast-forward*) o, cuando la rama del archivo ha divergido, como una secuencia de selección filtrada (*cherry-pick*).

## Qué permanece en la rama del archivo

Los archivos de estado operativo son duraderos y valiosos para el archivo, pero no son adecuados para el historial canónico:

- Memoria de sesión y resúmenes de preferencias del operador
- Documentos en borrador que esperan revisión editorial
- Notas operativas y mensajes entre archivos
- Borradores de informes en curso

Estos commits permanecen indefinidamente en la rama aislada del archivo. Para garantizar su durabilidad, el coordinador envía la rama del archivo al espejo de preparación (el repositorio remoto `jwoodfine` o `pwoodfine`), de modo que quede preservada fuera de la máquina. Nunca llega a `origin/main`.

## El filtro de publicación del coordinador

Durante la publicación, `app-orchestration-command` recorre la lista de commits entre el extremo de la rama del archivo y el HEAD actual de `origin/main`. Para cada commit aplica el filtro:

- **Commit de código** → se selecciona para `origin/main` (*cherry-pick*).
- **Commit exclusivamente de estado operativo** → se omite; permanece en la rama del archivo.
- **Commit mixto** (código + estado operativo) → se resuelve a favor de los cambios de código entrantes; los archivos de estado operativo quedan excluidos del resultado de la selección.

El filtro se ejecuta de forma idéntica independientemente de si el archivo inició la publicación por sí mismo o delegó la solicitud al coordinador.

## Relación con el historial WORM

El `origin/main` canónico se comporta como un registro de escritura única y lectura múltiple (*WORM*): cada commit publicado está firmado criptográficamente por la identidad administradora y es permanente. La rama del archivo, en cambio, es mutable —los archivos realizan un rebasado contra `origin/main` antes de publicar para resolver cualquier divergencia, lo que reescribe el historial de su rama local. Esta reescritura nunca toca el registro canónico.

## Velocidad en paralelo

Dado que cada archivo dispone de su propia rama aislada, el desarrollo en 21 archivos es concurrente. Los 50 commits que el Archivo A realice esta semana no bloquean al Archivo B para publicar sus 3 commits, y la publicación del Archivo B no interfiere con el trabajo pendiente del Archivo A. El único paso serializado es la publicación canónica en sí misma —y esa serialización es deliberada, para mantener la integridad de la auditoría.

## Temas relacionados

- [Cómo app-orchestration-command publica los cambios de un archivo](TOPIC-app-orchestration-command-publication-flow.es.draft.md) — criterios, modelo de elegibilidad y comportamiento sin conexión
- [Escalar el desarrollo coordinado en múltiples archivos soberanos](TOPIC-scaling-coordinated-development-sovereign-archives.es.draft.md) — el desafío de coordinación a escala
