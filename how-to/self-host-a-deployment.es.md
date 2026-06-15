---
schema: foundry-doc-v1
title: "Cómo autoalojar un despliegue"
slug: self-host-a-deployment
category: how-to
content_type: how-to
type: how-to
status: stub
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: self-host-a-deployment.md
---

Un despliegue de PointSav es una instancia nombrada y numerada de una configuración de gateway provisionada en infraestructura controlada por el operador. Cada despliegue ejecuta el mismo sustrato de distribución de software que el servicio alojado, con todos los datos y claves almacenados localmente. Esta guía cubre el provisionamiento de una nueva instancia de despliegue, la verificación de que el gateway inicia correctamente y su conexión a la plataforma central.

Para la arquitectura de despliegue, consulta [[deployment-patterns]] y [[edge-deployment]]. Para el modelo de distribución de software que suministra binarios firmados a tu instancia, consulta [[software-distribution-substrate]].

## Véase también

- [[deployment-patterns]] — patrones de configuración de gateway y topologías de despliegue
- [[edge-deployment]] — arquitectura de instancia edge y modelo de conectividad
- [[software-distribution-substrate]] — cómo se entregan las versiones de binarios firmados
- [[authenticate-binary-downloads]] — verifica el binario antes de ejecutarlo
- [[configure-doorman]] — configura el gateway de inferencia después de que el despliegue esté en funcionamiento
