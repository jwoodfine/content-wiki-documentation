---
schema: foundry-doc-v1
title: "Cómo leer y escribir en archivos Totebox"
slug: read-write-totebox-archives
short_description: "Lee el estado de un archivo Totebox al inicio de sesión — bandeja de entrada, contexto de sesión, git status, NEXT.md — y registra cambios mediante el flujo de commit de nivel staging."
category: how-to
index_group: records-storage
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
language_protocol: TRANSLATE-ES
paired_with: read-write-totebox-archives.md
research_trail:
  sources: [pointsav-monorepo .agent/ mailbox and drafts-outbound conventions, bin/commit-as-next.sh]
  verification_method: "verified against the same staging-tier commit flow and mailbox protocol already source-verified in install-toolchain.md and this wiki's sibling how-to guides"
---

Un Archivo Totebox es un entorno de trabajo delimitado: un repositorio git clonado de una fuente aguas arriba, configurado con reglas de sesión, buzones de entrada y salida, y un pipeline de borradores. Leer un archivo significa entender su estado actual — la bandeja de entrada, el trabajo activo y el contexto de sesión. Escribir en un archivo significa confirmar cambios en su historial git usando el flujo de confirmación por nivel de preparación. Esta guía cubre ambas operaciones.

Para el modelo de sesión que rige el acceso a archivos, véase [[totebox-session]] y [[totebox-orchestration-development]].

## Requisitos previos

- Un dispositivo emparejado con el espacio de trabajo, con acceso de escritura al archivo (véase [[pair-a-new-device]])
- Un Archivo Totebox abierto en su directorio de trabajo
- Una sesión activa (véase [[open-first-totebox-session]])

## Propósito

Leer el estado actual de un Archivo Totebox al inicio de sesión, escribir cambios mediante el flujo de confirmación por nivel de preparación, preparar borradores editoriales correctamente, y comunicarse entre archivos mediante el protocolo de buzón en lugar de editar los archivos de estado de otra sesión.

## Procedimiento

1. **Lea el estado del archivo al inicio de sesión**, en este orden:
   - Abra `.agent/inbox.md` y revise los mensajes pendientes — representan trabajo o información retransmitida de otras sesiones.
   - Abra `.agent/session-start.md` si está presente — contiene notas de orientación de la última sesión que se cerró en este archivo.
   - Abra `.agent/memory/session-context.md` para un resumen continuo de 5 sesiones que incluye elementos pendientes y preferencias del operador.
   - Ejecute `git status` para ver cambios sin confirmar. Si hay archivos preparados o modificados sin una confirmación, léalos antes de comenzar nuevo trabajo.
   - Lea `NEXT.md` — la cola de elementos abiertos del archivo; qué está en progreso y qué está bloqueado.

2. **Escriba en el archivo mediante el flujo por nivel de preparación.** No use `git commit` directamente — use el asistente `commit-as-next.sh`, que establece la identidad de autor correcta y firma la confirmación:
   - Haga sus cambios.
   - Prepare archivos específicos: `git add <archivo> <archivo>` — nunca `git add .` o `git add -A`.
   - Confirme: `~/Foundry/bin/commit-as-next.sh "<mensaje>"`.
   - Verifique: `git status` debe mostrar un árbol limpio.

   Las confirmaciones en un archivo permanecen en la rama de características local hasta la promoción de Etapa 6 por la Sesión de Comando.

3. **Prepare borradores editoriales para transferencia, si corresponde.** Si su trabajo produce un borrador de artículo, prepárelo en `.agent/drafts-outbound/` con el frontmatter correcto `foundry-draft-v1` antes de cerrar la sesión. No confirme contenido borrador directamente en los repositorios wiki desde un archivo — el borrador fluye primero a través del pipeline editorial. Un borrador preparado lleva frontmatter con `artifact`, `schema: foundry-draft-v1`, `status: staged`, `route-to:`, más contenido de cuerpo adecuado para el artículo wiki de destino.

4. **Comuníquese entre archivos mediante el buzón, nunca editando los archivos de estado de otra sesión.** Los mensajes llegan a `.agent/inbox.md` desde otras sesiones y se leen al inicio de sesión; los mensajes salientes nuevos se anteponen a `.agent/outbox.md`, que la Sesión de Comando revisa periódicamente. Escriba en la bandeja de entrada de otro archivo solo a través de la Sesión de Comando o una herramienta MCP aprobada (`send_mailbox_message`) — nunca edite directamente la bandeja de entrada de otra sesión.

## Resultado esperado

El estado del archivo (bandeja de entrada, contexto de sesión, estado de git, NEXT.md) se comprende antes de comenzar nuevo trabajo; cualquier confirmación se realiza mediante `commit-as-next.sh` con un árbol de trabajo limpio después; cualquier borrador se prepara en `.agent/drafts-outbound/` en lugar de confirmarse directamente en un repositorio wiki.

## Verificación

`git status` muestra un árbol limpio después de cada confirmación. El frontmatter de un borrador preparado valida contra el esquema `foundry-draft-v1`. No aparecen ediciones directas en el `.agent/inbox.md` o `.agent/outbox.md` de otra sesión.

## Reversión

Un cambio sin confirmar puede descartarse con `git checkout -- <archivo>` o `git restore <archivo>` antes de prepararlo. Un cambio ya confirmado en la rama de características local todavía no se ha promovido a canónico (la Etapa 6 es un paso posterior separado), por lo que revertirlo es una operación git local normal, no una reversión de producción.

## Próximos pasos

- [[open-first-totebox-session]] — abrir una sesión desde cero en un dispositivo recién emparejado
- [[pair-a-new-device]] — cómo el emparejamiento otorga acceso de escritura a un archivo en primer lugar

## Véase también

- [[totebox-session]] — el modelo de entorno de trabajo delimitado
- [[totebox-orchestration-development]] — el modelo de orquestación que rige cómo interoperan los archivos
- [[machine-based-auth]] — cómo el emparejamiento otorga acceso de escritura a los archivos
- [[worm-ledger-architecture]] — el libro mayor de solo anexar que registra todos los eventos de la plataforma
