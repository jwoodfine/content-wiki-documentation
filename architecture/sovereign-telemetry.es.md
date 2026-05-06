---
schema: foundry-doc-v1
title: "Arquitectura de Telemetría de Estado Cero"
slug: sovereign-telemetry
category: architecture
type: topic
quality: stub
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: sovereign-telemetry.md
cites: []
---

La arquitectura de telemetría de estado cero recopila señales de comportamiento y hardware de los clientes perimetrales sin cookies, identificadores de sesión ni agregadores de análisis de terceros. Utiliza la compilación del lado del cliente y la transmisión de balizas asíncrona en el cierre de la pestaña.

## Principio de diseño

La implementación actual, denominada internamente V4 Intent Beacon, aplica una postura estricta de sin cookies y sin ID de sesión. Los datos se compilan completamente del lado del cliente usando APIs nativas del navegador y se transmiten de forma asíncrona mediante `navigator.sendBeacon` en el evento `visibilitychange`. No intervienen píxeles de seguimiento, identificadores de sesión ni proveedores de análisis de terceros.

## Señales capturadas

La carga del V4 Intent Beacon captura señales distintas, cada una extraída de una API nativa del navegador:

- `user_agent` — identificación de dispositivo y navegador
- `viewport` — geometría de renderización
- `timezone` — mapeo regional sin geolocalización de IP
- `device_memory` — rango estimado de RAM del dispositivo
- `hardware_cores` — número de hilos de CPU
- `dwell_seconds` — tiempo en la página
- `scroll_depth` — profundidad máxima de desplazamiento vertical
- `intent_clicks` — eventos de clic de alto valor

Ningún campo captura información personalmente identificable. El campo `timezone` proporciona resolución regional sin requerir geolocalización de IP.

## Independencia operativa

La arquitectura es operacionalmente independiente de plataformas de análisis externas. La señal de telemetría existe en la infraestructura del cliente, no en sistemas de terceros.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
