---
schema: foundry-doc-v1
title: "Personal y permisos"
slug: personnel-permissions.es
category: architecture
type: topic
quality: complete
short_description: "La identidad y los permisos de los colaboradores en la orquestación Totebox se expresan mediante emparejamientos criptográficos — no mediante roles almacenados en una base de datos ni verificados en tiempo de solicitud — y un colaborador puede alcanzar un recurso únicamente si su os-console está emparejado con el nodo de orquestación que lo gestiona."
status: active
bcsc_class: forward-looking
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: personnel-permissions.md
---

En la orquestación Totebox, la identidad y los permisos de los colaboradores se expresan mediante emparejamientos criptográficos — no mediante roles almacenados en una base de datos ni verificados en tiempo de solicitud. El modelo de permisos es PairingAsPermission: un colaborador puede alcanzar un recurso únicamente si su instancia `os-console` está emparejada con el nodo de orquestación que gestiona ese recurso. Los cuatro niveles de permiso (P1 a P4) describen cómo es el conjunto de emparejamientos de un colaborador; la aplicación se realiza siempre a través de la topología de emparejamientos.

Este artículo describe la identidad del colaborador, los cuatro niveles, cómo se otorgan los permisos y la relación con el agregador planificado `app-orchestration-command`.

## Identidad del colaborador

Cada colaborador tiene:

- Una **identidad de máquina** — una instancia `os-console` con un certificado criptográfico vinculado a ese hardware específico. El certificado es la identidad; no hay autenticación de nombre de usuario y contraseña.
- Un **registro de personal** — una entrada en la capa de datos que contiene el nombre visible del colaborador, su rol, la clave pública SSH y el nivel de permiso.
- Un **conjunto de emparejamientos** — la lista de nodos con los que su `os-console` está emparejado, estableciendo qué archivos, nodos `os-mediakit` e instancias `os-privategit` puede alcanzar.

El almacén de personal es en sí mismo un archivo Totebox — no utiliza un servicio de identidad separado.

## Niveles de permiso

Cuatro niveles describen cómo es el conjunto de emparejamientos de un colaborador. El nivel no es una verificación en tiempo de ejecución; es una descripción humana de los emparejamientos. La aplicación se realiza siempre a través de la topología de emparejamientos.

**P1 — Administrador del sistema**
Conjunto de emparejamientos: Comando, cada archivo Totebox, ambos nodos `os-privategit`, ambos nodos `os-mediakit`, infraestructura de la máquina virtual.
Puede: aprovisionar archivos, actualizar la documentación del espacio de trabajo, ejecutar promociones de la etapa 6, añadir nuevos emparejamientos, gestionar el almacén de identidades, realizar la administración del sistema de la máquina virtual.

**P2 — Gerente de paquetes**
Conjunto de emparejamientos: archivos específicos más rutas de promoción de la etapa 6.
Puede: confirmar y promover dentro de los archivos asignados. No puede aprovisionar nuevos archivos ni modificar documentos a nivel de espacio de trabajo.

**P3 — Usuario**
Conjunto de emparejamientos: archivos específicos únicamente. Sin emparejamiento con el Comando.
Puede: trabajar dentro de los archivos asignados — escribir código, confirmar en staging, redactar contenido del wiki. No puede: acceder a recursos entre archivos directamente, modificar otros archivos ni realizar promociones de la etapa 6. Las solicitudes entre archivos se envían como mensajes para que la sesión de Comando los procese.

**P4 — Interfaz**
Conjunto de emparejamientos: solo superficie de API de solo lectura.
Puede: consultar puntos finales de solo lectura expuestos por archivos del conjunto de emparejamientos.
No puede: escribir ni confirmar nada.

## Cómo se otorgan los permisos

Un nuevo emparejamiento de colaborador es una acción del operador P1:

1. El colaborador genera un par de claves en su `os-console`.
2. El operador P1 añade la clave pública del colaborador a la lista de pares aceptados del nodo correspondiente y al `pairings.yaml` del Comando.
3. Se establece el saludo criptográfico.
4. El emparejamiento se registra como una entrada inmutable en el libro mayor.

No hay flujo de aprobación en un sistema separado. El emparejamiento es la aprobación. La entrada del libro mayor es el rastro de auditoría.

## Ejemplos de alcance del colaborador

**Un administrador del sistema (P1):**
Emparejado con el Comando, cada archivo Totebox activo, ambos nodos `os-privategit`, ambos nodos `os-mediakit` y el archivo de personal. Alcance: todo el espacio de trabajo. Puede ratificar hitos de la tétrada, gestionar el almacén de identidades, aprovisionar nuevos archivos, realizar promociones de la etapa 6.

**Un usuario P3:**
Emparejado con un archivo de proyecto específico — por ejemplo, `project-bookkeeping` — y con un `os-mediakit` de staging local para revisión. Alcance: solo trabajo del archivo y revisión de staging. Sin emparejamiento con el Comando. No puede acceder al almacén de identidades, otros archivos ni los árboles canónicos `vendor/` o `customer/`.

## Relación con app-orchestration-command

El agregador planificado `app-orchestration-command` (CommandCentre) está previsto para exponer un punto final `GET /personnel/<unix-user>` que devuelve el nivel de permiso y el conjunto de emparejamientos de un colaborador, derivado del registro del archivo de personal en la capa de datos. CommandCentre está previsto a utilizarlo para aplicar el alcance del solicitante en el enrutamiento de mensajes entre archivos — la defensa contra el adjunto confuso. El punto final es parte del alcance de implementación de la siguiente fase.

## Véase también

- [[pairing-as-permission]]
- [[totebox-orchestration-development]]
- [[totebox-session]]
- [[doorman-protocol]]

## Referencias

- **`DOCTRINE.md`** — carta constitucional de Foundry; modelo de permisos.
- **`conventions/three-ring-architecture.md`** — referencia de composición de sustrato de tres niveles.
