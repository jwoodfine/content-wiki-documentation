---
schema: foundry-topic-v1
title: "Arquitectura de Telemetría"
slug: topic-telemetry-architecture
category: infrastructure
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

El sistema de telemetría de la plataforma recopila analítica de tráfico web desde los nodos de borde en producción y la enruta hacia un entorno de procesamiento local, sin pasar por ningún servicio de agregación en la nube de terceros. Todo el análisis se ejecuta en hardware bajo control del operador.

## Ruta de enrutamiento en cuatro niveles

**Nivel 1 — Captura en el borde.** Los relays Nginx en los nodos de borde capturan payloads JSON del tráfico web orgánico y los enrutan a la red local a través de puertos designados: `10.50.0.2:8081` para el inquilino PointSav y `10.50.0.2:8082` para el inquilino Woodfine.

**Nivel 2 — Tránsito cifrado.** Los payloads atraviesan una malla WireGuard (`wg0`) entre el borde en la nube y el nodo de procesamiento local. El túnel termina en el firewall local; los datos están cifrados en tránsito y no pasan por ningún servicio intermediario.

**Nivel 3 — Procesamiento local.** Un daemon de telemetría en Rust, ejecutándose en el nodo de procesamiento local, recibe los payloads descifrados, los escribe en registros CSV por inquilino y produce informes Markdown estructurados cruzando los datos con la base de datos GeoLite2 City para resolver direcciones IP a regiones geográficas.

**Nivel 4 — Extracción para análisis.** El nodo de control ejecuta un script de extracción que obtiene los informes compilados del nodo de procesamiento sin tocar los datos en bruto del registro CSV.

## Justificación del diseño

Enrutar la telemetría hacia un nodo bajo control local significa que el operador conserva la custodia completa de los datos de tráfico. Ningún tercero almacena ni procesa la analítica en bruto, lo que es una condición previa del modelo de aislamiento por inquilino de la plataforma.

## Véase también

- [[topic-worm-ledger-architecture]] — el diseño del registro WORM que comparte el modelo de escritura de solo adición
- [[topic-edge-deployment]] — la arquitectura de ingesta en el perímetro
- [[compounding-substrate]] — el contexto más amplio del sustrato para la custodia de datos local

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
