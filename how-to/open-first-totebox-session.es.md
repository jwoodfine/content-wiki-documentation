---
schema: foundry-doc-v1
title: "Cómo abrir tu primera sesión Totebox"
slug: open-first-totebox-session
category: how-to
content_type: how-to
type: how-to
status: active
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: open-first-totebox-session.md
---

Una sesión Totebox es el entorno de trabajo delimitado para un único archivo — el ámbito dentro del cual lees registros, confirmas cambios y enrutas solicitudes a otros archivos. Cada tarea de desarrollo comienza abriendo una sesión en el archivo propietario del trabajo.

Esta guía cubre la configuración inicial desde un dispositivo recién vinculado. Si tu dispositivo aún no está vinculado, completa primero [[pair-a-new-device|Vincular un nuevo dispositivo]].

Para detalles de arquitectura, consulta [[totebox-session]] y [[totebox-orchestration-development]].

## Requisitos previos

- Un dispositivo vinculado en nivel INPUT o superior (consulta [[pair-a-new-device]])
- `os-console` instalado y autenticado
- Al menos un archivo provisionado en tu cuenta

## Pasos

### 1. Inicia os-console

Abre `os-console` en tu dispositivo vinculado. La pantalla principal muestra los archivos de tu cuenta. Si no aparece ningún archivo, tu cuenta aún no tiene acceso asignado a archivos — contacta al administrador del sistema.

### 2. Selecciona un archivo

Toca o haz clic en el archivo en el que quieres trabajar. La consola lee el manifiesto del archivo y muestra:

- Nombre del archivo e identificador de módulo
- Estado del Tétrada — cuáles de las cuatro ramas de entrega (vendor, customer, deployment, wiki) están activas
- Recuento de mensajes pendientes en la bandeja de entrada — mensajes de otros archivos o sesiones que requieren tu atención
- El punto de conexión del gateway de IA que usará la sesión para inferencia

### 3. Revisa tu bandeja de entrada

Si el recuento de mensajes pendientes es distinto de cero, revisa los mensajes antes de comenzar a trabajar. Los mensajes pueden contener decisiones, bloqueos o contexto que debe orientar tu trabajo en esta sesión. Marca cada mensaje como procesado cuando lo hayas atendido.

### 4. Inicia una tarea

En la vista de sesión, las tareas aparecen como tarjetas BRIEF — artefactos de proyecto duraderos que sobreviven al cierre de la sesión. Cada BRIEF muestra su estado (activo, referencia, archivado), los elementos pendientes y los tipos de artefactos que produce el trabajo.

Selecciona un BRIEF para ver su registro de trabajo y los elementos abiertos. Si este es un archivo nuevo sin BRIEFs, la sesión está en estado de arranque — tu primera tarea suele ser escribir el BRIEF del archivo.

### 5. Guarda tu trabajo antes de cerrar

Antes de finalizar una sesión, la consola solicita una revisión de cierre:

1. Actualiza o crea BRIEFs para el trabajo en progreso
2. Prepara mensajes salientes en la bandeja de salida para otros archivos o el hub
3. Confirma cualquier cambio no confirmado en la rama de preparación del archivo

Cerrar sin completar la revisión de cierre deja el trabajo en un estado sin preparar que puede entrar en conflicto con la siguiente sesión.

## Qué puede hacer una sesión

Una sesión Totebox escribe únicamente en los repositorios declarados de su propio archivo. No puede escribir configuración del espacio de trabajo, claves de identidad ni ningún archivo de un archivo hermano. Las solicitudes entre archivos se enrutan como mensajes a través de la bandeja de salida — la sesión hub las entrega.

| Permitido | No permitido |
|---|---|
| Editar archivos en los repositorios de este archivo | Escribir en archivos de otro archivo |
| Confirmar en la rama de preparación del archivo | Publicar en canónico sin la Etapa 6 |
| Enviar mensajes a través de la bandeja de salida | Escribir configuración a nivel de espacio de trabajo |
| Preparar borradores wiki en drafts-outbound | Escribir en el almacén de identidad |

## Puntos clave

- Cada sesión se abre dentro de un único archivo — el ámbito se aplica estructuralmente, no por política
- Lee tu bandeja de entrada antes de comenzar; los mensajes pueden cambiar tus prioridades de tarea
- Los BRIEFs son el registro duradero del trabajo en progreso — sobreviven al cierre de la sesión
- Completa la revisión de cierre para evitar pérdida de trabajo y conflictos de preparación

## Véase también

- [[totebox-session]] — qué es una sesión y su modelo de capacidad completo
- [[pair-a-new-device]] — registra el dispositivo en el que corre esta sesión
- [[pairing-as-permission]] — cómo se aplican los límites de acceso de la sesión
- [[totebox-orchestration-development]] — la arquitectura de desarrollo en la que participa una sesión
