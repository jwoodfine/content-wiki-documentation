---
schema: foundry-doc-v1
title: "Arquitectura de telemetría"
slug: telemetry-architecture.es
short_description: "La plataforma recopila análisis de tráfico web de nodos perimetrales de producción y los enruta a un entorno de procesamiento controlado localmente a través de una ruta cifrada sin pasar por servicios de análisis de terceros en la nube."
category: infrastructure
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: telemetry-architecture.md
---

El sistema de telemetría de la plataforma recopila analítica de tráfico web desde los [[edge-deployment|nodos de borde]] en producción y la enruta a través de la [[sovereign-mesh|malla WireGuard]] hacia un entorno de procesamiento local, coherente con los principios de [[customer-hostability|custodia de datos del cliente]], sin pasar por ningún servicio de agregación en la nube de terceros.

## Ruta de enrutamiento en cuatro niveles

**Nivel 1 — Captura en el borde.** Los relays Nginx en los nodos de borde capturan payloads JSON del tráfico web orgánico y los enrutan a la red local a través de puertos designados: `10.50.0.2:8081` para el inquilino PointSav y `10.50.0.2:8082` para el inquilino Woodfine.

**Nivel 2 — Tránsito cifrado.** Los payloads atraviesan una malla WireGuard (`wg0`) entre el borde en la nube y el nodo de procesamiento local. El túnel termina en el firewall local; los datos están cifrados en tránsito y no pasan por ningún servicio intermediario.

**Nivel 3 — Procesamiento local.** Un daemon de telemetría en Rust, ejecutándose en el nodo de procesamiento local, recibe los payloads descifrados, los escribe en registros CSV por inquilino y produce informes Markdown estructurados cruzando los datos con la base de datos GeoLite2 City para resolver direcciones IP a regiones geográficas.

**Nivel 4 — Extracción para análisis.** El nodo de control ejecuta un script de extracción que obtiene los informes compilados del nodo de procesamiento sin tocar los datos en bruto del registro CSV.

## Justificación del diseño

Enrutar la telemetría hacia un nodo bajo control local significa que el operador conserva la custodia completa de los datos de tráfico. Ningún tercero almacena ni procesa la analítica en bruto, lo que es una condición previa del modelo de aislamiento por inquilino de la plataforma.

## Véase también

- [[sovereign-telemetry]] — la arquitectura de telemetría de estado cero que opera sobre esta ruta de enrutamiento
- [[worm-ledger-architecture]] — el diseño del registro WORM que comparte el modelo de escritura de solo adición
- [[edge-deployment]] — la arquitectura de ingesta en el perímetro
- [[compounding-substrate]] — el contexto más amplio del sustrato para la custodia de datos local
