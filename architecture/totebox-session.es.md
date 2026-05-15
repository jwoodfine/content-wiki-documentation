---
schema: foundry-doc-v1
title: "Sesión Totebox"
slug: totebox-session.es
category: architecture
type: topic
quality: complete
short_description: "Una sesión Totebox es una sesión de colaborador asistida por IA abierta dentro de un único archivo Totebox — con alcance a los repositorios declarados del archivo, sin capacidad de escribir fuera de ellos, y es el punto de entrada estándar para todo trabajo de desarrollo en la orquestación Totebox."
status: active
bcsc_class: forward-looking
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: totebox-session.md
---

Una sesión Totebox es una sesión de colaborador asistida por IA abierta dentro de un único archivo Totebox. Tiene alcance a los repositorios declarados del archivo y no puede escribir fuera de ellos. Desde la perspectiva del colaborador, abrir una sesión Totebox es como comienza cada tarea de desarrollo en la orquestación Totebox. El protocolo de la sesión refleja la experiencia del cliente: el punto de entrada del colaborador en el espacio de trabajo y el punto de entrada del cliente a través de `os-console` realizan la misma función.

Este artículo describe cómo se abre una sesión, qué puede y no puede hacer, los cuatro niveles de permiso, y el protocolo de buzones de entrada y salida que coordina el trabajo entre archivos.

## Cómo abrir una sesión

El punto de entrada previsto es `bin/open-archive.sh <archive-name>`, planificado para invocarse desde la sesión de Comando. Cuando se invoque, está previsto que:

1. Lea el manifiesto del archivo en `clones/<archive>/.agent/manifest.md`
2. Imprima el nombre del archivo, el estado de la tétrada, el punto final de la pasarela de IA y el recuento de mensajes pendientes en el buzón de entrada
3. Verifique el nivel de permiso del colaborador contra el registro de personal (véase [[personnel-permissions]])
4. Establezca las variables de entorno `FOUNDRY_ARCHIVE` y `FOUNDRY_MODULE_ID`
5. Abra una sesión de IA en el directorio raíz del archivo

Esto refleja la experiencia del cliente: un miembro de la comunidad o un cliente abre un archivo Totebox a través de `os-console`. El flujo de trabajo de desarrollo utiliza el mismo punto de entrada, adaptado al espacio de trabajo.

## Alcance de la sesión

Una sesión Totebox:

- Escribe en cualquier repositorio declarado en el manifiesto del archivo
- Confirma en la rama de staging del archivo (nunca directamente en `main` canónica)
- Enruta la inferencia a través de la pasarela compartida de control de acceso `service-slm` usando el identificador de módulo del archivo
- Envía solicitudes entre archivos como mensajes a la sesión de Comando (nunca escribe en otros archivos)
- Almacena borradores del wiki en `.agent/drafts-outbound/` para la canalización editorial

Una sesión Totebox no:

- Escribe archivos del espacio de trabajo (`CLAUDE.md`, `AGENT.md`, `bin/`, `pairings.yaml`)
- Escribe en el almacén de identidades
- Accede directamente a los árboles canónicos `vendor/` o `customer/` (esos reciben contenido por promoción, no por escritura directa)
- Abre conexiones con sesiones de archivo hermanas

## La tétrada del proyecto

Cada archivo Totebox declara cuatro patas de la tétrada del proyecto. El trabajo de una sesión contribuye a las cuatro:

| Pata | La sesión escribe en |
|---|---|
| vendor | Código de característica en el clon `pointsav-monorepo` del archivo |
| customer | Guías operativas en el clon `woodfine-fleet-deployment` del archivo |
| deployment | Provisión de la instancia en ejecución en el directorio de despliegue |
| wiki | Archivos de borrador TOPIC almacenados en `.agent/drafts-outbound/` |

La sesión de Comando ratifica la completitud de la tétrada cuando las cuatro patas están presentes.

## El protocolo de coordinación entre sesiones de IA

Las sesiones se comunican mediante el protocolo de archivos de buzones de entrada y salida:

- Cada archivo contiene los archivos `.agent/inbox.md` y `.agent/outbox.md`
- Una sesión Totebox lee su buzón de entrada al iniciar la sesión y archiva los mensajes accionados
- Las solicitudes salientes a otros archivos o a la sesión de Comando se anteponen en `.agent/outbox.md` (más reciente arriba)
- La sesión de Comando barre los buzones de salida del clúster durante la revisión del espacio de trabajo y enruta los mensajes

En la siguiente fase planificada, `app-orchestration-command` (CommandCentre) está previsto para intermediar todos los mensajes entre archivos por HTTP, con cada mensaje transitando automáticamente la pasarela de control de acceso y el libro mayor inmutable. El protocolo basado en archivos está previsto para permanecer como respaldo y como mecanismo en modo de desarrollo.

## Niveles de permiso

Cuatro niveles rigen lo que un colaborador — y la sesión que abre — pueden hacer:

| Nivel | Etiqueta | Conjunto de emparejamientos |
|---|---|---|
| P1 | Administrador del sistema | Comando + cada archivo + cada nodo de infraestructura |
| P2 | Gerente de paquetes | Archivos específicos más rutas de promoción de la etapa 6 |
| P3 | Usuario | Archivos específicos; sin emparejamiento con Comando; solo lectura entre archivos |
| P4 | Interfaz | Solo superficie de API de solo lectura |

Los niveles se aplican mediante emparejamientos, no comparaciones de cadenas. El `os-console` de un colaborador P3 no está emparejado con el Comando — la conexión no existe. Véase [[pairing-as-permission]] para el mecanismo formal.

## Relación con os-console

`os-console` es el punto de entrada orientado al cliente para abrir un archivo Totebox. En el espacio de trabajo, `bin/open-archive.sh` es el equivalente. Ambos están previstos para realizar la misma función: leer el manifiesto del archivo, validar el alcance del permiso del colaborador, establecer el contexto de la sesión y abrir una sesión de trabajo dentro del archivo. El entorno de desarrollo utiliza el mismo patrón que el cliente está previsto a utilizar.

## Véase también

- [[totebox-orchestration-development]]
- [[pairing-as-permission]]
- [[personnel-permissions]]
- [[doorman-protocol]]

## Referencias

- **`DOCTRINE.md`** — carta constitucional de la plataforma.
