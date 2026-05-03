---
schema: foundry-doc-v1
title: "Tiempo de Ejecución Sin Contenedores"
slug: zero-container-runtime.es
category: reference
type: topic
quality: published
short_description: El compromiso estructural de que todo despliegue de PointSav se ejecuta como un binario Linux bajo systemd en una máquina virtual simple o hardware bare-metal, sin tiempo de ejecución de contenedores ni orquestador.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: zero-container-runtime.md
---

Todo despliegue de PointSav — en todos los anillos de servicio, todos los niveles de cómputo y todos los contextos de despliegue desde la implementación de referencia hasta un futuro despliegue en appliance — se ejecuta como un binario ELF de Linux supervisado por systemd en una máquina virtual simple o un host bare-metal. Sin tiempo de ejecución de contenedores. Sin orquestador. Sin plataforma de tiempo de ejecución gestionada.

Este es un compromiso estructural, no una elección pragmática de primera fase.

## Por qué es estructural

**Inspectabilidad en texto plano.** Las imágenes de contenedores son artefactos binarios procesados por tiempos de ejecución de contenedores. Ambos añaden opacidad sobre el sistema de archivos. Un archivo de unidad systemd y un binario Linux en un sistema de archivos son completamente inspeccionables con herramientas estándar: la tabla de procesos muestra qué está ejecutándose, el journal muestra qué ocurrió, el archivo de unidad muestra cómo está configurado el proceso.

**Soberanía del cliente.** Un cliente que ejecuta software dentro de un contenedor que no construyó, en un tiempo de ejecución que no controla, está a una decisión de plataforma de una interrupción. Las plataformas de tiempo de ejecución de contenedores pueden cambiar precios, políticas o disponibilidad sin la participación del cliente. Un binario gestionado por systemd en una máquina virtual Linux es portable a cualquier host Linux — cualquier proveedor de nube, infraestructura local del cliente o appliance — sin modificación.

**Legibilidad a largo plazo.** Los binarios ELF y los archivos de unidad systemd han sido el estándar en Linux desde los años 1990 y 2010 respectivamente. Los ecosistemas de tiempo de ejecución de contenedores dependen de especificaciones de formato de imagen e infraestructura de registro que han sufrido cambios sustanciales incluso en una década.

**Economía para PYMEs.** Las pequeñas y medianas empresas — el cliente objetivo de los despliegues de PointSav — no pueden mantener razonablemente infraestructura de contenedores. Un operador puede ejecutar `systemctl status` y leer la respuesta en texto plano.

## Lo que se usa en su lugar

La supervisión de procesos se maneja con unidades systemd. Los binarios Linux ELF se empaquetan para distribución como binarios nativos. La configuración vive en archivos de texto plano bajo `/etc/` o en archivos de entorno systemd. Los secretos se obtienen del gestor de secretos en la nube al arranque y se conservan en un sistema de archivos respaldado por memoria. El registro se enruta a través de journald.

## La compensación declarada

El compromiso acepta un tiempo de inicio en frío más largo para el cómputo de ráfaga en comparación con las plataformas de contenedores gestionadas. A cambio: cada proceso en ejecución en cada despliegue es visible para el cliente con herramientas estándar de administración del sistema, y el mismo binario y archivo de unidad se ejecuta en cualquier host Linux sin modificación.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Con licencia [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
