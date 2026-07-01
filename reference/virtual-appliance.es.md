---
schema: foundry-doc-v1
title: "Appliance Virtual"
slug: virtual-appliance
category: reference
type: topic
content_type: topic
quality: complete
status: active
audience: customer-woodfine
bcsc_class: current-fact
language_protocol: TRANSLATE-ES
last_edited: 2026-06-30
editor: woodfine-editorial
short_description: "Imagen de máquina virtual preconfigurada que combina un sistema operativo mínimo con una aplicación específica, distribuida como una unidad de implementación autónoma en formato OVF o similar — que permite a los proveedores de software distribuir configuraciones de software completamente funcionales que se ejecutan de forma consistente en plataformas de hipervisor sin esfuerzo de instalación y configuración por host."
paired_with: virtual-appliance.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - d10cc0e71b298b62123d673a2279ee4a1024b20367effb01db928ecdaa5a829f
thesis_alignment: "El appliance virtual es el formato de distribución principal para los servicios orientados a appliances de software implementados en infraestructura virtualizada — comprenderlo es prerequisito para razonar sobre la topología de implementación para la distribución de servicios basada en hipervisor."
keynote: false
---

Un appliance virtual es una imagen de máquina virtual preconfigurada que combina un sistema operativo mínimo con una aplicación o servicio específico, distribuida como una unidad autónoma lista para su implementación en una plataforma de hipervisor o infraestructura en la nube compatible. La característica definitoria de un appliance virtual es que llega preconfigurado: a diferencia del software convencional que debe instalarse en un entorno de sistema operativo existente y configurarse para la máquina de destino, un appliance virtual se implementa como una imagen que contiene tanto el sistema operativo como la aplicación en una configuración precomprobada y funcional.

## Open Virtualization Format

El Open Virtualization Format (OVF) es el formato estándar para empaquetar y distribuir appliances virtuales. Desarrollado por DMTF (Distributed Management Task Force), OVF define una estructura estándar para describir máquinas virtuales de una manera que es portable entre plataformas de hipervisor — un appliance virtual en formato OVF puede ejecutarse en VMware, VirtualBox, Xen, KVM y otros hipervisores compatibles con OVF sin modificación.

Un paquete OVF (típicamente distribuido como un único archivo `.ova`, un archivo OVF) contiene: una o más imágenes de disco virtual en formato estandarizado; un descriptor OVF (archivo XML `.ovf`) que especifica los requisitos de hardware, la configuración de red, los parámetros de inicio y otras propiedades de implementación; un archivo de manifiesto que enumera las sumas de comprobación para todos los componentes del paquete; y un archivo de certificado opcional para la verificación de firma.

## Características

**Estado preconfigurado.** Un appliance virtual llega con toda la configuración requerida aplicada: cadenas de conexión de bases de datos, cuentas de usuario de servicio, certificados SSL y configuración a nivel de aplicación se establecen durante la construcción del appliance y no requieren configuración por implementación. La organización que lo implementa proporciona solo los parámetros específicos del entorno: dirección de red, proveedor de identidad externo, rutas de almacenamiento.

**Huella mínima del SO.** Los appliances virtuales incorporan típicamente una capa de Sistema Operativo Mínimo Suficiente (JeOS) en lugar de una distribución completa de propósito general. El SO mínimo reduce el tamaño de la imagen, el consumo de memoria, la superficie de ataque y la sobrecarga de parcheo requerida para mantener el appliance durante su vida operativa.

**Modelo de inmutabilidad.** En un appliance virtual bien construido, las capas del sistema operativo y la aplicación se tratan como inmutables: las actualizaciones se aplican reemplazando toda la imagen del appliance en lugar de parchear el sistema en ejecución. Este enfoque elimina la deriva de configuración y hace que el appliance implementado sea idéntico al appliance probado.

**Instantánea y reversión.** Como máquina virtual, un appliance virtual puede ser objeto de instantáneas antes de las operaciones de mantenimiento, lo que permite una reversión instantánea a un estado conocido como correcto si una actualización o cambio de configuración causa un problema.

## Casos de uso

**Distribución por proveedores de software.** Los proveedores de software independientes distribuyen sus productos como appliances virtuales para reducir la fricción en la implementación. El cliente descarga, importa e inicia el appliance en lugar de realizar un procedimiento de instalación.

**Estandarización de infraestructura como servicio.** En entornos IaaS, los appliances virtuales son la unidad estándar de implementación de servicios. En lugar de mantener scripts de configuración por servicio, los operadores mantienen un catálogo de imágenes de appliance precompiladas que pueden implementarse de forma consistente en todos los entornos.

**Entornos de desarrollo y prueba.** Los appliances virtuales proporcionan entornos de desarrollo y prueba reproducibles: un desarrollador puede destruir y recrear una instancia de appliance en segundos, garantizando que el entorno coincida exactamente con la configuración de producción.

---

*citas: [[just-enough-operating-system]], [[computer-appliance]], [[lightweight-linux-distribution]]*
