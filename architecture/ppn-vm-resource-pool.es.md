---
schema: foundry-doc-v1
title: "Arquitectura del Pool de Recursos VM PPN"
slug: ppn-vm-resource-pool
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
paired_with: ppn-vm-resource-pool.md
short_description: "El pool de recursos VM de la PPN es una pila de tres servicios que aprovisiona, coloca y contabiliza máquinas virtuales en una malla WireGuard heterogénea que combina nodos en la nube y hardware físico."
cites: []
---

El pool de recursos de máquinas virtuales de la Red Privada de PointSav (PPN) es una pila de tres servicios que aprovisiona, coloca y contabiliza máquinas virtuales en una malla WireGuard heterogénea. El pool combina nodos en la nube con hardware físico, formando un sustrato de cómputo distribuido que abarca distintos perfiles de capacidad.

Tres servicios dividen la superficie de responsabilidad. El controlador de flota mantiene una visión global de la capacidad de los nodos y gestiona las decisiones de colocación. El agente de host se ejecuta por nodo como la autoridad de creación de VMs, comunicándose con el hipervisor y conservando el estado local de cada máquina virtual. El proxy de inquilino se sitúa en el límite del cliente, aplicando autenticación, aislamiento del espacio de nombres del inquilino, límites de cuota y un registro de auditoría inmutable. Por encima de esta pila, un broker de inferencia comercial gestiona cargas de trabajo medidas para el nivel SLM local.

Todos los procesos de servicio se comunican a través de la capa subyacente WireGuard de la PPN. Ningún servicio expone una interfaz pública; todo el tráfico dirigido al cliente entra a través del proxy de inquilino.

## Controlador de flota

El controlador de flota mantiene un registro en memoria del estado de los nodos: capacidad disponible, disponibilidad de virtualización por hardware, recuento actual de VMs y estado de reserva.

La colocación utiliza un algoritmo de selección en dos pasadas. La primera pasada considera únicamente los nodos no reservados, satisfaciendo el límite de capacidad solicitado. Si la primera pasada no arroja ningún candidato, la segunda amplía la búsqueda para incluir los nodos reservados. Esta separación permite a los operadores designar nodos para cargas de trabajo sensibles a la latencia, manteniendo al mismo tiempo la posibilidad de colocación por desbordamiento bajo carga.

Los endpoints de estado de flota proporcionan una visión global del estado de los nodos y listados de VMs por inquilino. La ingestión de latidos de corazón (*heartbeats*) procedentes de los agentes de host está delimitada por la capa subyacente WireGuard y la identidad del nodo, no por credenciales separadas.

## Agente de host

El agente de host es la autoridad de creación por nodo. Cada nodo del pool ejecuta una instancia que acepta solicitudes de creación y destrucción reenviadas por el controlador de flota tras la colocación.

Al recibir una solicitud de creación, el agente ensambla la configuración de inicialización necesaria, invoca al hipervisor con los parámetros apropiados y escribe metadatos de estado junto a la imagen de disco. Este archivo auxiliar almacena el identificador de la VM y permite la recuperación del latido de corazón tras un reinicio del proceso o del nodo, sin necesidad de consultar al controlador de flota.

Los nodos señalan su estado de reserva e identidad estable al controlador de flota en el arranque. En los nodos donde la virtualización por hardware (KVM) no está disponible — como instancias en la nube sin virtualización anidada — este indicador de capacidad se informa en el latido de corazón; el hipervisor recurre a la emulación por software en esos nodos.

## Proxy de inquilino

El proxy de inquilino es la capa orientada al cliente. Acepta solicitudes de creación, destrucción y consulta de estado de llamantes autenticados, y aplica el contrato de inquilino antes de reenviarlas al controlador de flota.

La autenticación utiliza tokens portadores emitidos en el momento del aprovisionamiento del inquilino. Cada token lleva un identificador de inquilino que el proxy utiliza para delimitar todos los registros de VM en un espacio de nombres. Un inquilino no puede consultar, modificar ni destruir las VMs de otro inquilino; el proxy aplica esta restricción en cada endpoint antes de cualquier interacción con la flota.

La aplicación de cuota opera a nivel de capacidad. Cada inquilino tiene asignado un techo en el momento del aprovisionamiento. El proxy comprueba la capacidad asignada actualmente frente al techo antes de reenviar una solicitud de creación; las solicitudes que superarían la cuota son rechazadas. Las creaciones concurrentes del mismo inquilino se serializan mediante una compuerta por inquilino para impedir que dos solicitudes simultáneas superen ambas la comprobación de cuota contra el mismo total previo a la creación.

Todas las operaciones de escritura se añaden a un registro de auditoría inmutable. Cada entrada registra el identificador del inquilino, el identificador de la VM, el tipo de operación, la marca de tiempo y el origen de la solicitud. El registro es de solo adición; ninguna ruta modifica las entradas existentes.

## Broker de inferencia

El broker de inferencia gestiona el tráfico medido hacia el nivel SLM local, posicionado por encima de la pila de VMs como la superficie de intermediación comercial. No crea ni gestiona VMs directamente; intermedia solicitudes de inferencia y contabiliza el consumo por inquilino.

El broker implementa un disyuntor con umbrales configurables. Cuando el disyuntor está abierto o la compuerta de admisión está cerrada, las solicitudes de inferencia entrantes reciben una respuesta de servicio no disponible en lugar de encolarse indefinidamente. Esto protege al SLM local de picos de carga que de otro modo degradarían la latencia de respuesta para todos los inquilinos.

La medición por inquilino registra los recuentos de tokens de cada inferencia completada. Un endpoint de conciliación de facturación agrega los registros de medición por inquilino. El estado de la licencia se comprueba en el arranque y periódicamente a partir de entonces; un fallo de licencia cierra la compuerta de admisión sin interrumpir las solicitudes en vuelo.

## Malla WireGuard

La capa subyacente de la PPN utiliza una malla WireGuard. Todos los procesos de servicio se vinculan a sus direcciones de interfaz WireGuard, no a interfaces públicas. La configuración de pares es estática; cada nodo conserva las claves públicas de sus pares y los rangos de enrutamiento de cada túnel.

Un nodo de retransmisión en la nube reenvía el tráfico entre nodos físicos que se encuentran en redes separadas sin una ruta directa, aunque WireGuard utiliza rutas directas entre pares cuando están disponibles. El rol de retransmisión no exige que el nodo en la nube participe en la colocación de VMs — opera únicamente en la capa de red.

La heterogeneidad de nodos es una propiedad deliberada del pool. Cada tipo de nodo aporta un perfil de capacidad diferente: los nodos en la nube ofrecen tiempo de actividad confiable y almacenamiento elástico; los nodos físicos ofrecen virtualización acelerada por hardware. Las decisiones de colocación reflejan estas diferencias mediante el indicador de capacidad y el algoritmo de selección reservados/no reservados en dos pasadas.

## Extensiones planificadas

Tres extensiones al sustrato de cómputo están previstas para despliegue futuro; ninguna está operativa en la actualidad.

**Aislamiento por microkernel (planificado/previsto):** La ruta de creación de VMs en hardware AArch64 está prevista para utilizar un modelo de componente de microkernel formalmente verificado. El diseño previsto reemplazaría el kernel del host como límite de confianza para el aislamiento de VMs, proporcionando verificación formal del planificador y los canales de comunicación entre procesos entre VMs.

**MicroVM ligero (planificado/previsto):** Se está evaluando un backend de hipervisor alternativo para cargas de trabajo donde el tiempo de arranque inferior a un segundo y la reducción de la sobrecarga de memoria son prioritarios. El punto de integración previsto es el agente de host, que seleccionaría el backend del hipervisor en función del tipo de carga de trabajo especificado en la solicitud de creación.

**ISO de aprovisionamiento de metal desnudo (planificado/previsto):** Está prevista una imagen de arranque firmada y reproducible como sustrato de aprovisionamiento para nuevos nodos de la PPN. El diseño planificado pretende instalar la pila completa del nodo desde un único arranque, sin necesidad de una instalación previa del sistema operativo ni configuración manual.

## Véase también

- [[ppn-small-business-compute|Cómputo PPN para pequeñas empresas]] — el producto de pequeñas empresas construido sobre el pool de recursos PPN
- [[ppn-tenant-vm-isolation|Aislamiento de VMs por Inquilino en PPN]] — modelo de aislamiento detallado e isolamiento planificado a nivel de red
- [[software-distribution-substrate|Sustrato de Distribución de Software]] — distribución binaria y verificación de licencias

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
