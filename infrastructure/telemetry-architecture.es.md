---
schema: foundry-doc-v1
title: "Arquitectura de telemetría"
slug: telemetry-architecture
short_description: "La plataforma recopila análisis de tráfico web de nodos perimetrales de producción y los enruta a un entorno de procesamiento controlado localmente a través de una ruta cifrada sin pasar por servicios de análisis de terceros en la nube."
category: infrastructure
index_group: network-and-telemetry
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-28
editor: pointsav-engineering
paired_with: telemetry-architecture.md
---

El sistema de telemetría de la plataforma recopila analítica de tráfico web desde los [[edge-deployment|nodos de borde]] en producción y la enruta a través de la [[sovereign-mesh|malla WireGuard]] hacia un entorno de procesamiento local, coherente con los principios de [[customer-hostability|custodia de datos del cliente]], sin pasar por ningún servicio de agregación en la nube de terceros.

## Puntos clave

- La telemetría sigue una ruta de cuatro niveles: captura en el borde → tránsito cifrado WireGuard → nodo de procesamiento local → extracción al nodo de control. Ningún payload pasa por un servicio de agregación en la nube de terceros en ningún paso.
- Todo el tráfico se escribe en un único registro compartido en el nodo de procesamiento local (`assets/ledger_telemetry.csv`) — no existe separación por inquilino en el registro hoy.
- El nodo de control extrae únicamente informes Markdown compilados desde el directorio `outbox/` del nodo de procesamiento — no los datos CSV en bruto, que permanecen en el nodo de procesamiento. Esto limita el alcance de un posible compromiso del nodo de control a los datos de resumen, no al registro de tráfico completo.
- La telemetría local es una condición previa del modelo de aislamiento por inquilino y de la propiedad de [[customer-hostability|custodia de datos del cliente]]. El operador conserva la custodia completa de la analítica de tráfico; ningún tercero almacena ni procesa los datos en bruto.

## Ruta de enrutamiento en cuatro niveles

**Nivel 1 — Captura en el borde.** Los relays Nginx en los nodos de borde capturan payloads JSON del tráfico web orgánico y los enrutan a la red local a través de puertos designados: `10.50.0.2:8081` para el inquilino PointSav y `10.50.0.2:8082` para el inquilino Woodfine.

**Nivel 2 — Tránsito cifrado.** Los payloads atraviesan una malla WireGuard (`wg0`) entre el borde en la nube y el nodo de procesamiento local. El túnel termina en el firewall local; los datos están cifrados en tránsito y no pasan por ningún servicio intermediario.

**Nivel 3 — Procesamiento local.** Un daemon de telemetría en Rust, ejecutándose en el nodo de procesamiento local, recibe los payloads descifrados y los añade a un único registro CSV compartido. Un binario de generación de informes independiente lee ese registro, consulta una base de datos local GeoLite2 City para resolver cada IP registrada a una región geográfica, y escribe un informe Markdown estructurado en el directorio de salida.

**Nivel 4 — Extracción para análisis.** El nodo de control ejecuta un script de extracción que obtiene los informes compilados del nodo de procesamiento sin tocar los datos en bruto del registro CSV.

## Justificación del diseño

Enrutar la telemetría hacia un nodo bajo control local significa que el operador conserva la custodia completa de los datos de tráfico. Ningún tercero almacena ni procesa la analítica en bruto.

## Véase también

- [[sovereign-telemetry]] — la carga de la baliza del lado del cliente que transporta el enrutamiento de este artículo
- [[worm-ledger-architecture]] — el diseño del registro WORM que comparte el modelo de escritura de solo adición
- [[edge-deployment]] — la arquitectura de ingesta en el perímetro
- [[compounding-substrate]] — el contexto más amplio del sustrato para la custodia de datos local
