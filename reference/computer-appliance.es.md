---
schema: foundry-doc-v1
title: "Appliance Informático"
slug: computer-appliance
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
short_description: "Dispositivo informático que combina hardware y software diseñados para realizar una función específica y bien definida — implementado como una unidad cerrada y sellada que no requiere configuración por instalación y no puede reutilizarse para computación general — incluyendo appliances de red, de almacenamiento, de copia de seguridad, de seguridad y dispositivos gateway IoT industriales."
paired_with: computer-appliance.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - cfe9a4fcee0f1fa23212792ac352fb57dccf96133acff2d08124be467915d06a
thesis_alignment: "El appliance informático es el patrón de codiseño hardware-software para la computación de función única — comprenderlo establece la arquitectura de referencia para las unidades de implementación inmutables y de propósito específico en los dominios de red, seguridad e informática industrial."
keynote: false
---

Un appliance informático es un dispositivo informático en el que el hardware y el software han sido diseñados e ingenieriados conjuntamente para realizar una función informática específica y bien definida. A diferencia de un ordenador de propósito general — que puede configurarse, reconfigurarse y reutilizarse para muchas funciones — un appliance informático está diseñado para una tarea, se entrega con el software para esa tarea preinstalado, y normalmente no puede reutilizarse para otras funciones sin reemplazarlo por completo.

El appliance informático se describe como "cerrado y sellado": el software no es instalable ni modificable por el usuario de la manera en que lo son los sistemas operativos de propósito general. El usuario de un appliance informático interactúa con él a través de la interfaz específica que proporciona su fabricante — una interfaz de gestión basada en web, un panel de hardware dedicado o un protocolo de red definido — en lugar de hacerlo a través de una línea de comandos o un entorno gráfico de propósito general.

El concepto de appliance informático es el análogo en hardware del appliance de software o virtual — la misma filosofía de diseño aplicada a infraestructura física en lugar de virtualizada.

## Tipos

**Appliances de red** — hardware dedicado para funciones de red: enrutamiento, conmutación, cortafuegos, equilibrio de carga y análisis de tráfico. Los appliances de red están construidos específicamente para manejar el tráfico de red a velocidad de línea, un requisito de rendimiento que los servidores de propósito general con implementaciones de software no pueden satisfacer de manera confiable.

**Appliances de almacenamiento** — hardware construido específicamente para almacenamiento y recuperación de datos: dispositivos de almacenamiento conectado en red (NAS), cabinas de área de almacenamiento (SAN), appliances de copia de seguridad y appliances de deduplicación de datos.

**Appliances de copia de seguridad** — hardware dedicado para copia de seguridad, deduplicación y recuperación de datos. Los appliances de copia de seguridad combinan alta capacidad de almacenamiento con motores de deduplicación y software de replicación.

**Appliances de seguridad** — hardware para funciones de seguridad: sistemas de detección y prevención de intrusiones (IDS/IPS), pasarelas de seguridad de correo electrónico, pasarelas de seguridad web y dispositivos de gestión unificada de amenazas (UTM).

**Appliances gateway IoT industriales y MES** — dispositivos informáticos robustizados para entornos industriales: pasarelas de sistemas de ejecución de fabricación (MES), dispositivos de comunicación SCADA y nodos de computación en el borde para sistemas de control industrial. Estos dispositivos conectan las redes de tecnología operativa (OT) — los sistemas de control que gestionan el equipo industrial — con las redes de tecnología de la información (TI).

**Appliances de consumo** — dispositivos informáticos de consumo de propósito específico: grabadores de vídeo en red, decodificadores, equipos de red doméstica y reproductores de medios digitales.

## Pila de software

El software en un appliance informático se construye típicamente sobre una distribución Linux mínima que sirve como capa del sistema operativo — equivalente al concepto de Sistema Operativo Mínimo Suficiente (JeOS). Las actualizaciones se entregan como imágenes de firmware validadas que reemplazan toda la pila de software en una única operación atómica, garantizando que el estado posterior a la actualización coincida con la configuración probada por el proveedor.

---

*citas: [[virtual-appliance]], [[just-enough-operating-system]], [[lightweight-linux-distribution]]*
