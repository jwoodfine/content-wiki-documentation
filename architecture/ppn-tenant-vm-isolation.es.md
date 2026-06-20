---
schema: foundry-doc-v1
title: "Aislamiento de Máquinas Virtuales por Inquilino en PPN"
slug: ppn-tenant-vm-isolation
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: ppn-tenant-vm-isolation.md
short_description: "El pool de recursos PPN separa las cargas de trabajo por inquilino mediante aislamiento de espacio de nombres, aislamiento de proceso por VM y redes en modo usuario. El aislamiento a nivel de subred de red es un hito planificado."
cites: []
---

El pool de recursos de la Red Privada de PointSav (PPN) permite que múltiples inquilinos ejecuten máquinas virtuales en un conjunto compartido de nodos físicos y en la nube. Este artículo describe el modelo de aislamiento: qué separación se proporciona, qué no, y el camino planificado hacia un aislamiento más sólido a nivel de red.

## La pila

Cada solicitud de máquina virtual atraviesa tres capas antes de que un proceso QEMU se inicie en un nodo físico:

- **Proxy de inquilino** — autentica al llamante, aplica el espacio de nombres y la cuota, y es el único punto de entrada externo
- **Controlador de flota** — gestiona la colocación y delega en el agente de host; acepta conexiones únicamente del proxy de inquilino y de los participantes internos de la malla
- **Agente de host** — inicia el proceso QEMU en el nodo seleccionado; no es accesible por llamantes externos

Un llamante que disponga de la dirección del controlador de flota pero no de una credencial de inquilino válida no puede alcanzar el controlador de flota directamente — la capa de autenticación no puede eludirse.

## Qué proporciona el aislamiento de inquilinos

### Aislamiento de espacio de nombres

Un inquilino autenticado puede crear, listar y destruir únicamente sus propias máquinas virtuales. La identidad del inquilino es inyectada por el proxy de inquilino en cada solicitud reenviada al controlador de flota; un inquilino no puede suministrar una identidad diferente en el cuerpo de una solicitud. El listado de VMs devuelve únicamente los registros pertenecientes al inquilino autenticado. Las solicitudes de destrucción se validan contra la propiedad antes de ser reenviadas.

Este aislamiento sobrevive a los reinicios del controlador de flota: la identidad del inquilino se almacena en el registro de la VM, se repite en cada latido de corazón del nodo y se restaura en el registro en memoria al arrancar. La propiedad no reside únicamente en la memoria del proxy de inquilino.

### Aislamiento de proceso

Cada máquina virtual es un proceso QEMU separado en el nodo físico. Los sistemas operativos invitados se ejecutan en espacios de direcciones aislados por hardware (en nodos con aceleración KVM) o en espacios de direcciones aislados por software (en nodos solo con TCG). La máquina virtual de un inquilino no puede leer la memoria ni el disco de la máquina virtual de otro inquilino a través de rutas de software normales.

### Contención de red por VM

Las máquinas virtuales utilizan redes en modo usuario SLIRP: cada invitado recibe una pila de direcciones NAT privada sin ninguna ruta entrante desde la red del host ni desde otras VMs. Un proceso invitado que abra un socket de servidor no es alcanzable a menos que se haya configurado una regla de reenvío al host en el momento de la creación. La respuesta de creación de la VM incluye la lista de puertos del host reenviados para que los llamantes sepan cómo acceder a su VM.

### Seguridad del token portador

Las credenciales de inquilino son tokens portadores opacos que se asignan a una identidad de inquilino en la configuración del proxy. Conocer la cadena de identidad de un inquilino no es suficiente para autenticarse; el llamante debe presentar el token asociado. Los tokens no se registran en ningún registro de auditoría.

### Registro de auditoría

Cada operación del ciclo de vida de un inquilino — crear VM, destruir VM — queda registrada en dos lugares: un archivo de solo adición local en el proxy de inquilino, y el libro WORM. El registro WORM incluye la identidad del inquilino, el tipo de operación, el identificador de la VM, la marca de tiempo y el resultado. Las entradas WORM no pueden sobrescribirse ni eliminarse.

## Qué no proporciona el aislamiento de inquilinos

### Sin subred de red por inquilino

Todas las máquinas virtuales en un nodo físico dado salen a través de la misma interfaz de red del host. Un observador de red que monitorice el tráfico saliente del nodo no puede distinguir el tráfico de la VM de un inquilino del tráfico de la VM de otro inquilino en la capa de transporte. Los inquilinos están aislados en la capa de aplicación mediante pilas de red separadas, pero no en la capa de red.

### Sin aislamiento del operador del nodo

Cualquier persona con acceso administrativo a la máquina física que aloja una VM puede leer la imagen de disco y la memoria del invitado. Esto es una propiedad del modelo de virtualización basado en QEMU actual, no una limitación del plano de control de la PPN.

La respuesta prevista a ambas limitaciones es la capa de aislamiento seL4, descrita a continuación.

## Aplicación de cuota

Cada inquilino tiene configurado un recuento máximo de VMs en el proxy de inquilino. El proxy aplica las cuotas mediante una compuerta serializada en solicitudes de creación concurrentes: dos solicitudes simultáneas del mismo inquilino superan ambas la comprobación de cuota solo si existe cuota suficiente para las dos.

## Camino hacia el aislamiento a nivel de red

El aislamiento a nivel de red — subredes WireGuard por inquilino de modo que las VMs de los inquilinos sean criptográficamente inaccesibles para otros inquilinos, no solo separadas por API — requiere dos hitos futuros:

**Fase S3 del plano de control de red de la PPN (planificada):** El plano de control adquiere la capacidad de gestionar tablas de pares WireGuard programáticamente. Cuando un nuevo nodo se une a la malla, está previsto que el plano de control actualice automáticamente las configuraciones de enrutamiento de todos los nodos. Esta es la base prevista para asignar a cada inquilino una subred distinta con sus propias claves WireGuard.

**Modo B de seL4 (planificado/previsto):** Está previsto que el propio plano de control de red se ejecute como una VM de primera clase dentro de la PPN, aislada por un microkernel formalmente verificado. En el Modo B, se prevé que incluso un operador de nodo con acceso administrativo a la máquina física no pueda inspeccionar la configuración del plano de control de red ni extraer las claves de los inquilinos.

Hasta que se alcancen estos hitos, el límite de aislamiento se describe con precisión como aislamiento a nivel de API: los inquilinos no pueden acceder a los recursos de los demás a través del plano de control, pero comparten las rutas de red física en la capa de transporte, y los operadores de nodo mantienen el acceso administrativo a las máquinas físicas que administran.

## Véase también

- [[ppn-small-business-compute|Cómputo PPN para pequeñas empresas]] — descripción general del sistema, pila de tres nodos, malla WireGuard
- [[software-distribution-substrate|Sustrato de Distribución de Software]] — distribución binaria y verificación de licencias

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
