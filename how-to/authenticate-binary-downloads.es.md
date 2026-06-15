---
schema: foundry-doc-v1
title: "Cómo autenticar descargas de binarios"
slug: authenticate-binary-downloads
category: how-to
content_type: how-to
type: how-to
status: stub
language_protocol: TRANSLATE-ES
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: authenticate-binary-downloads.md
---

El punto de distribución privado de PointSav en `software.pointsav.com` emite versiones de binarios firmadas con Ed25519. Cada descarga se verifica contra la clave pública del editor antes de ejecutar el binario. Esta guía cubre la solicitud de un token de licencia, la descarga de una versión y la verificación de la firma.

Para la arquitectura detrás del sistema de distribución, consulta [[private-git-paid-customer-endpoint]] y [[software-distribution-substrate]].

## Véase también

- [[private-git-paid-customer-endpoint]] — la arquitectura del punto de conexión para clientes de pago
- [[software-distribution-substrate]] — el sustrato de distribución de software
- [[machine-based-auth]] — cómo se autoriza el acceso al punto de distribución
