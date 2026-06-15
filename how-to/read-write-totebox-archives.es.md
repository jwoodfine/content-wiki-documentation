---
schema: foundry-doc-v1
title: "Cómo leer y escribir en archivos Totebox"
slug: read-write-totebox-archives
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: read-write-totebox-archives.md
---

Un Archivo Totebox es un entorno de trabajo delimitado: un repositorio git clonado de una fuente aguas arriba, configurado con reglas de sesión, buzones de entrada y salida, y un pipeline de borradores. Leer un archivo significa entender su estado actual — la bandeja de entrada, el trabajo activo y el contexto de sesión. Escribir en un archivo significa confirmar cambios en su historial git usando el flujo de confirmación por nivel de preparación. Esta guía cubre ambas operaciones.

Para el modelo de sesión que rige el acceso a archivos, véase [[totebox-session]] y [[totebox-orchestration-development]].

## Requisitos previos

- Un dispositivo emparejado con acceso de nivel INPUT (véase [[pair-a-new-device]])
- Un Archivo Totebox abierto en su directorio de trabajo
- Una sesión activa (véase [[open-first-totebox-session]])

## Leer un archivo al inicio de sesión

Antes de hacer cualquier trabajo en un archivo, lea su estado actual en este orden:

1. **Lea la bandeja de entrada** — abra `.agent/inbox.md` y revise los mensajes pendientes. Representan trabajo o información retransmitida de otras sesiones.
2. **Lea el archivo de inicio de sesión** — abra `.agent/session-start.md` si está presente. Contiene notas de orientación de la última sesión que se cerró en este archivo.
3. **Lea el contexto de sesión** — abra `.agent/memory/session-context.md` para un resumen continuo de 5 sesiones que incluye elementos pendientes y preferencias del operador.
4. **Verifique el estado de git** — ejecute `git status` para ver cambios sin confirmar. Si hay archivos preparados o modificados sin una confirmación, léalos antes de comenzar nuevo trabajo.
5. **Lea el NEXT.md** — la cola de elementos abiertos del archivo; qué está en progreso y qué está bloqueado.

## Escribir en un archivo

Todas las confirmaciones usan el flujo por nivel de preparación. No use `git commit` directamente — use el asistente `commit-as-next.sh`, que establece la identidad de autor correcta y firma la confirmación.

La secuencia para cualquier escritura:

1. Haga sus cambios.
2. Prepare archivos específicos: `git add <archivo> <archivo>` — nunca `git add .` o `git add -A`.
3. Confirme: `~/Foundry/bin/commit-as-next.sh "<mensaje>"`.
4. Verifique: `git status` debe mostrar un árbol limpio.

Las confirmaciones en un archivo permanecen en la rama de características local hasta la promoción por el Nivel 6 de la Sesión de Comando.

## Preparar borradores editoriales para transferencia

Si su trabajo produce un borrador de artículo, prepárelo en `.agent/drafts-outbound/` con el frontmatter correcto `foundry-draft-v1` antes de cerrar la sesión. No confirme contenido borrador directamente en los repositorios wiki desde un archivo — el borrador fluye primero a través del pipeline editorial.

Un borrador preparado tiene:
- Frontmatter con `artifact`, `schema: foundry-draft-v1`, `status: staged`, `route-to:`
- Contenido del cuerpo adecuado para el artículo wiki de destino

## Comunicación entre archivos

Use el sistema de buzón para comunicarse con otras sesiones en lugar de editar archivos de estado directamente:

- **Bandeja de entrada** — los mensajes llegan a `.agent/inbox.md` desde otras sesiones; léala al inicio de sesión
- **Bandeja de salida** — anteponga nuevos mensajes a `.agent/outbox.md`; la Sesión de Comando los revisa periódicamente

Escriba en la bandeja de entrada de otro archivo solo a través de la Sesión de Comando o una herramienta MCP aprobada (`send_mailbox_message`). Nunca edite directamente la bandeja de entrada de otra sesión.

## Puntos clave

- Siempre lea bandeja de entrada → inicio de sesión → contexto de sesión → estado de git → NEXT.md antes de comenzar a trabajar
- Use `commit-as-next.sh` para cada confirmación; `git commit` directo está bloqueado por la compuerta pre-confirmación
- Prepare borradores en `.agent/drafts-outbound/`; no confirme contenido borrador en repositorios wiki desde este archivo
- La comunicación entre sesiones usa el protocolo de buzón — nunca escriba directamente los archivos de estado de otra sesión

## Véase también

- [[totebox-session]] — el modelo de entorno de trabajo delimitado
- [[totebox-orchestration-development]] — el modelo de orquestación que rige cómo interoperan los archivos
- [[open-first-totebox-session]] — abrir una sesión desde cero en un dispositivo recién emparejado
- [[machine-based-auth]] — cómo el emparejamiento de nivel INPUT otorga acceso de escritura a los archivos
- [[worm-ledger-architecture]] — el libro mayor de solo anexar que registra todos los eventos de la plataforma
