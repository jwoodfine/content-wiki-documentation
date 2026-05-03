---
schema: foundry-doc-v1
title: "Modelo Económico — Niveles Community y Cliente PYME"
slug: economic-model.es
category: architecture
type: topic
quality: published
short_description: "La estructura comercial de dos niveles de PointSav: un nivel Community gratuito como embudo de adopción, y un nivel de Cliente PYME de pago orientado a pequeñas y medianas empresas reguladas que las grandes plataformas no pueden atender económicamente."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: economic-model.md
---

El modelo comercial de PointSav opera en dos niveles: Community (gratuito) y Cliente PYME (de pago). No existe un nivel Enterprise. Esta decisión no responde a un posicionamiento de mercado, sino a una realidad estructural: las pequeñas y medianas empresas reguladas ocupan un segmento que las grandes plataformas de computación en la nube no pueden atender de forma económicamente viable.

## El segmento objetivo

Las PYME reguladas comparten tres características que definen el mercado:

1. Son demasiado pequeñas para los ciclos de venta empresarial que exigen las grandes plataformas (contratos anuales superiores a $500,000 USD).
2. Están demasiado reguladas para los productos de IA de consumo masivo — aplican marcos normativos como HIPAA, PIPEDA, GDPR y equivalentes canadienses.
3. Requieren que sus datos y su infraestructura de IA permanezcan bajo su propio control.

Clínicas pequeñas, despachos jurídicos regionales, asesores financieros de tamaño mediano y operadoras inmobiliarias con archivos corporativos son ejemplos representativos de este segmento. No son casos excepcionales; conforman la economía regulada por debajo del umbral empresarial.

## Los dos niveles

**Community** es el nivel gratuito, licenciado bajo AGPL-3.0-or-later. Incluye un archivo ToteboxOS y una terminal ConsoleOS, con inferencia local de modelos como componente opcional. Su función es el embudo de adopción: genera contribuidores, expone casos de uso reales y hace visible la plataforma para futuros clientes.

**Cliente PYME** es el nivel de ingresos, con un contrato de Orden de Servicio por cliente. Incorpora agregación de múltiples archivos, capacidad de cómputo en GPU bajo demanda, participación en el mercado federado de adaptadores LoRA y acceso prioritario a las actualizaciones del modelo base.

## La asimetría de costos

El ajuste fino LoRA de un modelo de siete mil millones de parámetros cuesta entre $30 y $100 por adaptador. El preentrenamiento continuo del mismo modelo cuesta entre $30,000 y $100,000. Las PYME pueden hacer ajuste fino LoRA con sus propios datos; no pueden costear el preentrenamiento continuo. PointSav realiza el preentrenamiento continuo y distribuye el modelo mejorado — bajo la denominación planificada PointSav-OLMo-N — a toda la base de clientes en cada actualización de la plataforma. Esta asimetría es estructural y no depende de ningún resultado competitivo particular.

## Federación

Las capacidades de federación — el mercado de adaptadores LoRA, el pool Mooncake KV y las actualizaciones del modelo base — están incluidas en la licencia de Cliente PYME. No existe un nivel de federación separado. La privacidad de los datos de cada cliente se preserva mediante técnicas de aprendizaje federado con privacidad diferencial que son maduras en 2026.

## Ver también

- [[compounding-substrate]] — las cinco propiedades estructurales que este modelo económico financia
- [[sovereign-ai-commons]] — el posicionamiento del sustrato como un bien común soberano

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
