---
schema: foundry-doc-v1
title: "La orquestación Totebox como entorno de desarrollo"
slug: totebox-orchestration-development.es
category: architecture
type: topic
quality: complete
short_description: "El entorno de desarrollo de PointSav está desplegado como una instancia de orquestación Totebox — el espacio de trabajo que construye la plataforma se ejecuta sobre la misma arquitectura que la plataforma entrega a los clientes."
status: active
bcsc_class: forward-looking
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: totebox-orchestration-development.md
---

El entorno de desarrollo de PointSav está desplegado como una instancia de orquestación Totebox — la misma arquitectura que la plataforma entrega a los clientes. El espacio de trabajo de desarrollo, donde se escribe y publica la plataforma, opera como un concentrador que coordina trece archivos Totebox a través de una única pasarela compartida de control de acceso `service-slm`. El flujo de trabajo de desarrollo es el flujo de trabajo del cliente. No existe un entorno de pruebas que se aparte de la arquitectura de producción; el entorno que produce el código es la arquitectura que el código describe.

Este artículo documenta cómo el espacio de trabajo se asigna a la orquestación Totebox, qué responsabilidades tienen la sesión de Comando y las sesiones Totebox, y qué componentes están operativos frente a los planificados.

## Qué es la orquestación Totebox

La orquestación Totebox organiza el trabajo en archivos Totebox — unidades autocontenidas, cada una con código fuente, guías operativas, un despliegue activo y una contribución al wiki. Una sesión de Comando actúa como concentrador: mantiene los emparejamientos con cada archivo y coordina el trabajo entre archivos. Una sesión Totebox se abre dentro de un único archivo y opera solo dentro del alcance declarado de ese archivo.

El espacio de trabajo de desarrollo se asigna directamente a esta topología:

| Espacio de trabajo de desarrollo | Equivalente en orquestación Totebox |
|---|---|
| El espacio de trabajo | Sesión de Comando — concentrador, almacén de identidades, coordinación entre archivos |
| Cada directorio `clones/project-*/` | Un archivo Totebox |
| Una sesión abierta en un clon de cluster | Una sesión Totebox |
| Pasarela de control de acceso `service-slm` | La capa compartida de enrutamiento de IA de la orquestación |
| `vault-privategit-source-1` (declarado en `MANIFEST.md`) | La identidad de la instancia de Comando |

Trece archivos Totebox están actualmente activos en el espacio de trabajo, cubriendo las áreas de información de construcción, información geográfica, edición editorial, diseño, conocimiento, marketing, contabilidad, corrección de pruebas e infraestructura de plataforma. Se planifican dos archivos de desarrollo adicionales para completar la topología — `project-source` para el trabajo del nivel canónico de PointSav y `project-woodfine` para el trabajo del nivel de cliente de Woodfine.

## La sesión de Comando

La sesión de Comando se inicia en la raíz del espacio de trabajo. Su alcance:

- Documentación del espacio de trabajo y convenciones
- El almacén de identidades en `identity/` — claves criptográficas para cada identidad de contribuyente
- La cadena de herramientas `bin/` — scripts para confirmar, promover y abrir archivos
- Gobernanza entre archivos: ratificación de hitos, enrutamiento de mensajes, barrido de buzones de salida
- Administración del sistema de la máquina virtual
- `pairings.yaml` — el registro topológico operativo (ver [[pairing-as-permission]])

La sesión de Comando es la única sesión que puede escribir archivos a nivel de espacio de trabajo. Las sesiones Totebox individuales enrutan las solicitudes entre archivos como mensajes a la sesión de Comando, en lugar de cruzar archivos directamente.

## Sesiones Totebox

Una sesión Totebox se abre dentro de un archivo específico. Opera dentro de ese archivo — escribiendo código, confirmando en ramas de staging, redactando contenido del wiki, actualizando el despliegue. No escribe en otros archivos, no modifica archivos del espacio de trabajo y no tiene acceso directo al almacén de identidades.

El punto de entrada planificado es `bin/open-archive.sh <archive-name>`, previsto para leer el manifiesto del archivo, mostrar el estado de la tétrada y los mensajes pendientes, establecer las variables de entorno con alcance al archivo y abrir una sesión en el directorio raíz del archivo. Esto está pensado para reflejar cómo un cliente o miembro de la comunidad abre un archivo Totebox a través de `os-console`: el flujo de trabajo de desarrollo es idéntico al flujo del cliente.

## La sesión raíz retirada

Las versiones anteriores del flujo incluían una sesión raíz que se abría directamente dentro de los repositorios de ingeniería (`vendor/content-wiki-*`, `vendor/pointsav-design-system`). Los clientes nunca tuvieron un equivalente — no existe modo raíz en el modelo Totebox — por lo que el rol carecía de justificación arquitectónica.

El reemplazo utiliza dos archivos Totebox de desarrollo dedicados: `project-source` para el trabajo del nivel canónico de PointSav y `project-woodfine` para el trabajo del nivel de cliente de Woodfine, ambos planificados. Todo el trabajo del repositorio se prevé que fluya a través de estos archivos y luego se promueva al libro mayor canónico mediante la etapa 6 (`bin/promote.sh`). Los directorios `vendor/` y `customer/` son destinos del libro mayor canónico — el trabajo se envía hacia ellos, nunca se abre en ellos para sesiones de IA.

## La tétrada del proyecto

Cada archivo Totebox declara una tétrada del proyecto: cuatro patas que en conjunto representan su contribución completa a la plataforma.

| Pata | Qué contiene |
|---|---|
| vendor | Código fuente en `pointsav-monorepo` — la implementación |
| customer | Guías operativas en `woodfine-fleet-deployment` — cómo usarla |
| deployment | Instancia activa en el directorio de despliegue — el servicio en ejecución |
| wiki | Artículos en `content-wiki-documentation` o `content-wiki-projects` — la contribución de conocimiento |

Un archivo con las cuatro patas ratificadas está completo. Los archivos con patas pendientes llevan el estado `leg-pending` con un plan. La sesión de Comando ratifica la completitud de la tétrada como parte de la revisión del hito.

## La pasarela compartida de control de acceso

Cada archivo Totebox enruta la inferencia a través de la misma instancia de la pasarela `service-slm`. La pasarela es multi-inquilino: acepta solicitudes etiquetadas con un encabezado `X-Module-ID` que identifica qué archivo está realizando la solicitud, enruta al nivel de cómputo apropiado y aplica los límites por inquilino en cada llamada.

Una sola instancia de `service-slm` actualmente sirve a los trece archivos activos. El manifiesto de cada archivo declara `slm_endpoint: http://localhost:8011`, apuntando a esta instancia compartida. Cuando los archivos finalmente se trasladen a máquinas virtuales separadas, cada máquina está prevista para ejecutar su propia instancia de pasarela — el campo del manifiesto se actualiza sin que el código que llama requiera otros cambios.

## La arquitectura de dos nodos

El espacio de trabajo está previsto para ejecutarse en dos nodos de cómputo separados:

**Nodo os-orchestration** — el entorno de desarrollo. Aloja la sesión de Comando, todos los archivos Totebox, la pasarela `service-slm`, el código fuente y las herramientas del espacio de trabajo. El trabajo de inteligencia, el desarrollo de código y el staging están previstos para suceder aquí. No accesible desde la internet pública.

**Nodo os-mediakit** — la capa de entrega. Aloja los sitios web públicos activos, nginx y las instancias de servicio en producción. Recibe despliegues desde el nodo os-orchestration a través de un puente rsync deliberadamente con compuerta humana. Sin código fuente, sin trabajo de desarrollo, sin conexión directa con el nodo os-orchestration.

La separación está diseñada para que un incidente de desarrollo — una prueba fallida, un evento de disco lleno, una característica inacabada — no pueda afectar a los sitios web públicos activos. El puente rsync está concebido como la compuerta humana deliberada entre desarrollo y producción, coherente con la disciplina SYS-ADR-19 de no publicación automatizada a entornos activos.

## "Construimos PointSav sobre PointSav"

La afirmación arquitectónica es demostrable a partir de artefactos ya en su lugar:

- El espacio de trabajo está declarado como `vault-privategit-source-1` en `MANIFEST.md` — una instancia Totebox en sentido canónico.
- Trece archivos Totebox están activos, cada uno siguiendo la disciplina de la tétrada del proyecto.
- La pasarela compartida `service-slm` está operativamente activa (177 de 177 pruebas aprobadas) y sirve como capa de enrutamiento de IA de la orquestación.
- El flujo de confirmaciones — ramas de staging promovidas mediante `bin/promote.sh` al libro mayor canónico — es la canalización de promoción Totebox.
- El protocolo de archivos buzón-de-entrada-y-salida es el protocolo de coordinación entre sesiones de IA — el mismo patrón que los clientes están previstos a usar para la comunicación entre archivos.

El siguiente paso previsto es la aplicación planificada `app-orchestration-command`: un agregador concentrador que expone una interfaz HTTP activa para la salud de los archivos, el enrutamiento de mensajes y las verificaciones de permisos del personal. El cluster (`project-command`) está provisionado; la aplicación es el siguiente hito de implementación.

## Véase también

- [[pairing-as-permission]]
- [[doorman-protocol]]
- [[compounding-substrate]]
- [[apprenticeship-substrate]]

## Referencias

- **`DOCTRINE.md`** — carta constitucional de la plataforma; disciplina de composición de sustratos.
- **`MANIFEST.md`** — pasaporte del espacio de trabajo que declara la identidad de la instancia `vault-privategit-source-1`.
- [[three-ring-architecture]] — referencia de composición de sustrato del Anillo 1/2/3.
