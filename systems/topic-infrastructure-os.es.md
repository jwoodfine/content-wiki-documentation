---
schema: foundry-doc-v1
title: "Infrastructure OS"
slug: topic-infrastructure-os
category: systems
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: topic-infrastructure-os.md
cites: []
---

Infrastructure OS es la columna vertebral de virtualización y redes del ecosistema de PointSav. Opera como la capa de host fundacional que permite la ejecución de múltiples instancias de Totebox Archive aisladas en una sola máquina física o virtual.

## Virtualización y orquestación

La función principal de Infrastructure OS es virtualizar los recursos de hardware para el sustrato de PointSav. Actúa como el host subyacente para las **Micro Máquinas Virtuales** que ejecutan los Toteboxes individuales.

A través de su integración con la orquestación Totebox, Infrastructure OS gestiona el ciclo de vida de estos archivos, garantizando que permanezcan aislados a nivel de kernel mientras proporciona los recursos de cómputo necesarios para sus servicios internos (extracción, indexación, búsqueda).

## Red Privada de PointSav

Infrastructure OS crea y mantiene la **Red Privada de PointSav**. Esta es una red de superposición cifrada de igual a igual que permite la comunicación segura entre los dispositivos distribuidos de PointSav.

Cada nodo que ejecuta Infrastructure OS se convierte en un miembro verificado de esta red, permitiendo:
- **Transferencia de datos cifrada:** Mover imágenes de disco arrancables de Totebox Archive entre ubicaciones de forma segura.
- **Comunicación entre dispositivos:** Sincronización segura de estado entre instancias distribuidas de PointSav.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
