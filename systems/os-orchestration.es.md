---
schema: foundry-doc-v1
title: "OrchestrationOS"
slug: os-orchestration.es
category: systems
type: os
quality: complete
short_description: "OrchestrationOS es la capa del sistema operativo que administra un clúster de archivos Totebox — agregando archivos, exponiendo una interfaz unificada para operadores y enrutando los mensajes de coordinación entre sesiones de IA entre los archivos."
status: active
bcsc_class: forward-looking
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: os-orchestration.md
---

OrchestrationOS (`os-orchestration`) es la capa del sistema operativo que administra un clúster de archivos Totebox. Agrega los archivos que supervisa, expone una interfaz unificada para los operadores y otros nodos de orquestación, y enruta los mensajes de coordinación entre sesiones de IA entre los archivos. Tres instancias por proyecto están operativamente activas en el espacio de trabajo hoy; el agregador planificado `app-orchestration-command` que expone la interfaz unificada es el siguiente hito de implementación.

Este artículo describe los dos roles que puede ocupar una instancia de orquestación, las instancias por proyecto activas y cómo la coordinación entre archivos preserva el invariante [[pairing-as-permission]].

## Roles

**Comando** — Una única instancia de Comando está emparejada con cada archivo Totebox, ambos nodos os-mediakit y ambos nodos os-privategit. El Comando es el concentrador de la topología de orquestación Totebox. Es el único nodo con visibilidad completa entre archivos; su lista de emparejamientos es el registro topológico operativo.

**Instancias por proyecto** — Cada clúster de proyecto activo ejecuta su propia instancia de orquestación con alcance a los archivos de ese clúster. Una instancia por proyecto está emparejada únicamente con sus propios archivos. No tiene emparejamiento con el Comando (la comunicación fluye por mensaje, no por conexión directa) y no tiene emparejamiento con instancias por proyecto hermanas.

## Instancias por proyecto activas

Las siguientes instancias de orquestación por proyecto están actualmente activas en el espacio de trabajo Foundry:

| Instancia | Clúster | Alcance |
|---|---|---|
| `gateway-orch-bim-1` | `project-bim` | Archivos de información de construcción |
| `gateway-orch-gis-1` | `project-gis` | Archivos de información geográfica |
| `gateway-orch-proofreader` | `project-proofreader` | Archivos de la aplicación de corrección |

Se planifican instancias adicionales por proyecto a medida que los clústeres restantes completen las patas de su tétrada.

## CommandCentre

`app-orchestration-command` — denominado CommandCentre — es la aplicación agregadora concentradora prevista que se ejecutará en la instancia de orquestación de Comando. Está planificada para exponer:

- `GET /archives` — salud y estado de la tétrada de todos los archivos Totebox emparejados
- `POST /message` — acepta un mensaje de coordinación entre archivos, valida el alcance del solicitante (la defensa contra el adjunto confuso) y enruta al archivo objetivo
- `GET /personnel/<user>` — devuelve el nivel de permiso y el conjunto de emparejamientos de un colaborador

CommandCentre es la implementación prevista del concentrador de Comando. El clúster (`project-command`) está provisionado; la aplicación está pendiente de implementación.

## Relación con os-mediakit

La orquestación y os-mediakit se ejecutan en nodos físicos separados por diseño. El nodo de orquestación gestiona el desarrollo, el staging y todo el trabajo de archivo. El nodo os-mediakit gestiona la entrega de sitios web públicos. Se comunican a través de un puente rsync con compuerta humana — una compuerta de despliegue deliberada coherente con `SYS-ADR-19` (sin publicación automatizada de IA a libros mayores verificados).

## Coordinación entre archivos

Las instancias de orquestación por proyecto no se conectan directamente entre sí. Cuando `project-bim` necesita información de `project-editorial`, envía un mensaje al Comando. El Comando, emparejado con ambos, recupera los datos y los devuelve, o reenvía el mensaje. No se crea ninguna conexión lateral. La topología no cambia. PairingAsPermission se preserva.

El patrón — procesos aislados más un concentrador de paso de mensajes — implica que una instancia por proyecto comprometida no puede alcanzar archivos hermanos. La conexión literalmente no existe. Véase [[pairing-as-permission]] para la base formal de seguridad.

## Véase también

- [[totebox-orchestration-development]]
- [[pairing-as-permission]]
- [[totebox-session]]
- [[doorman-protocol]]

## Referencias

- **`DOCTRINE.md`** — carta constitucional de Foundry; topología de orquestación Totebox.
- **`MANIFEST.md`** — pasaporte del espacio de trabajo; declaración de identidad de la instancia de Comando.
