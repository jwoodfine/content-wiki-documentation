---
schema: foundry-doc-v1
title: "Modelo económico — niveles Community y Cliente PYME"
slug: economic-model.es
category: architecture
type: topic
quality: complete
short_description: "La estructura comercial de dos niveles de PointSav: un nivel Community gratuito como embudo de adopción, y un nivel de Cliente PYME de pago orientado a pequeñas y medianas empresas reguladas que los modelos de facturación a hiperescala no pueden atender económicamente."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-22
editor: pointsav-engineering
cites: []
paired_with: economic-model.md
---

Una pequeña empresa regulada se sitúa en una brecha. Es demasiado pequeña para un contrato de IA empresarial — esos empiezan en cientos de miles de dólares al año — y está demasiado regulada para pasar sus datos por un producto de IA de consumo. Ningún ciclo de venta la alcanza.

La estructura comercial de PointSav se construye enteramente en torno a esa brecha. <!--claim id=two-tiers-no-enterprise confidence=structural cites=[]-->Hay dos niveles y ningún nivel Enterprise: un nivel Community gratuito que es el embudo de adopción, y un nivel de Cliente PYME de pago para pequeñas y medianas empresas reguladas.<!--/claim-->

<!--claim id=structural-not-positional confidence=structural cites=[]-->La decisión es estructural, no de posicionamiento. El segmento objetivo maneja contratos de herramientas de IA de entre 5.000 y 50.000 dólares al año: demasiado pequeño para un ciclo de venta empresarial, demasiado regulado para un producto de consumo. La estructura de costos de la plataforma está diseñada para atenderlo de forma rentable.<!--/claim-->

Para un comprador de ese segmento, la economía de la plataforma está alineada con la suya. Este artículo cubre los dos niveles, por qué no hay nivel Enterprise, el segmento objetivo, la federación y la asimetría de costos que protege la posición.

## El segmento objetivo

Las PYME reguladas comparten tres características que definen el mercado.

1. Son demasiado pequeñas para los ciclos de venta empresarial que exigen los mínimos de la hiperescala.
2. Están demasiado reguladas para la IA de consumo o sin gestión — aplican HIPAA, PIPEDA, GDPR, FINRA y marcos provinciales canadienses equivalentes.
3. Requieren que sus datos y su IA permanezcan en infraestructura que controlan.

Clínicas pequeñas bajo legislación de privacidad sanitaria, despachos jurídicos regionales con obligaciones de confidencialidad, asesores financieros medianos con requisitos de reporte regulatorio y operadoras inmobiliarias con archivos corporativos son ejemplos representativos. No son casos excepcionales; conforman la economía regulada por debajo del umbral empresarial.

## Los dos niveles

<!--claim id=community-tier confidence=structural cites=[]-->**Community** es el nivel gratuito, bajo licencia AGPL-3.0-or-later. Un despliegue Community es un archivo ToteboxOS y una terminal ConsoleOS, con inferencia local de modelos como componente opcional. Community es el embudo de adopción — genera contribuidores y expone casos límite — y PointSav no obtiene ingresos de él.<!--/claim-->

<!--claim id=smb-tier confidence=structural cites=[]-->**Cliente PYME** es el nivel de ingresos, con un contrato de Orden de Servicio por cliente. Incorpora agregación de múltiples archivos, capacidad de cómputo en GPU bajo demanda, participación en el mercado federado de adaptadores y acceso prioritario a las actualizaciones del modelo base.<!--/claim-->

## Por qué no hay nivel Enterprise

El cliente direccionable de una plataforma de IA de nivel Enterprise suele manejar valores de contrato anuales superiores a 500.000 dólares. Los proveedores de hiperescala están estructurados para ese segmento. PointSav no está equipado para competir allí y no lo intenta.

<!--claim id=the-gap confidence=structural cites=[]-->El segmento que PointSav atiende maneja valores de contrato anuales de herramientas de IA de 5.000 a 50.000 dólares. Esa brecha — demasiado pequeña para un ciclo empresarial, demasiado regulada para un producto de consumo — es estructuralmente inaccesible para una plataforma construida en torno a un modelo de facturación a hiperescala.<!--/claim-->

## La asimetría de costos

El ajuste fino de adaptadores de un modelo de siete mil millones de parámetros cuesta entre 30 y 100 dólares por adaptador. El preentrenamiento continuo del mismo modelo cuesta entre 30.000 y 100.000 dólares. El preentrenamiento desde cero a esa escala cuesta entre 500.000 y 2.000.000 de dólares.

<!--claim id=cost-asymmetry confidence=structural cites=[]-->Una pequeña empresa puede ajustar adaptadores con sus propios datos; no puede costear el preentrenamiento continuo. PointSav financia el preentrenamiento continuo, y la federación agrupa el aprendizaje de adaptadores por cliente en un bien común que mejora el modelo base para todos. La asimetría no depende de ningún resultado competitivo particular — depende de la economía del cómputo a escala.<!--/claim-->

## Federación

<!--claim id=federation-included confidence=structural cites=[]-->Las capacidades de federación — el mercado federado de adaptadores, el pool compartido de caché clave-valor y las actualizaciones del modelo base — están incluidas en la licencia de Cliente PYME. No hay un nivel de federación separado; todo cliente de pago puede participar.<!--/claim-->

## El preentrenamiento continuo como inversión curatorial

<!--claim id=linux-distro-model confidence=structural cites=[]-->La inversión de PointSav en el preentrenamiento continuo del modelo base se financia con los ingresos por licencias de Cliente PYME, y el modelo base mejorado beneficia a cada cliente cuando se distribuye en la siguiente versión de la plataforma. La estructura económica se asemeja a una distribución de Linux: la curación se financia con el negocio de suscripción, los clientes ejecutan sus propias instalaciones, y el modelo base mejorado regresa a toda la base de suscriptores.<!--/claim-->

## Véase también

- [[compounding-substrate]] — las cinco propiedades estructurales que este modelo económico financia
- [[sovereign-ai-commons]] — el posicionamiento del sustrato como un bien común soberano
- [[llm-substrate-decision]] — cómo la elección del modelo se corresponde con los niveles de capacidad
- [[four-tier-slm-substrate]] — los cuatro niveles de despliegue dentro del modelo de Cliente PYME
