---
schema: foundry-doc-v1
title: "documentation.pointsav.com"
slug: index.es
lang: es
paired_with: index.md
category: root
status: pre-build
last_edited: 2026-04-29
editor: pointsav-engineering
---

# documentation.pointsav.com

La documentación de la plataforma PointSav abarca la arquitectura, los
servicios, los sistemas operativos y las convenciones de gobernanza del
sustrato PointSav. Los artículos están dirigidos a ingenieros, escritores,
diseñadores y lectores con interés financiero en la plataforma. Todo el
contenido se publica bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Áreas principales

La wiki está organizada en nueve áreas temáticas:

- **Arquitectura** — principios de diseño, patrones de sustrato e invariantes
  transversales que rigen la construcción de la plataforma
- **Servicios** — servicios autónomos de ingestión, procesamiento, búsqueda y
  egreso que implementan el modelo de tres anillos
- **Sistemas** — ToteboxOS y su modelo de capacidades basado en seL4,
  orquestación y aislamiento de inquilinos
- **Aplicaciones** — aplicaciones orientadas al usuario e internas construidas
  sobre el sustrato de la plataforma
- **Gobernanza** — registros de decisiones de arquitectura, postura de licencias
  y convenciones de cumplimiento
- **Infraestructura** — despliegue de flota y topología operacional (en preparación)
- **Empresa** — entidades corporativas, estructura organizativa y divulgaciones
  públicas
- **Referencia** — glosario, matriz de nomenclatura y guías de estilo para
  colaboradores
- **Ayuda** — guías de incorporación para ingenieros, escritores y diseñadores

## Artículo destacado

El motor del sitio lee el archivo `featured-topic.yaml` en la raíz del
repositorio para determinar qué artículo se destaca en la página de inicio.
Si el archivo no está presente, esta sección no se renderiza.

## Contribuir

El contenido se publica bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Las contribuciones siguen el flujo de confirmación por niveles descrito en
[[style-guide-topic]]. La wiki incluye pares bilingües: cada artículo técnico
en inglés tiene un resumen estratégico en español adaptado para lectores
hispanohablantes, no una traducción literal.

El motor que sirve este sitio, [[app-mediakit-knowledge]], está construido
en Rust y consume este repositorio como su única fuente de contenido. Está
previsto que futuras instancias sirvan wikis de clientes bajo el patrón de
hostabilidad del cliente.
