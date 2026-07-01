---
schema: foundry-doc-v1
title: "Computación en la Niebla"
slug: fog-computing
category: reference
type: topic
content_type: topic
quality: complete
status: active
audience: customer-woodfine
bcsc_class: current-fact
language_protocol: TRANSLATE-ES
last_edited: 2026-06-30
editor: woodfine-editorial
short_description: "Arquitectura de computación distribuida que sitúa la computación, el almacenamiento y los servicios de red en una capa intermedia entre los dispositivos de borde y los centros de datos en la nube centralizados — reduciendo la latencia y los requisitos de ancho de banda del backbone para aplicaciones IoT y en tiempo real, definida por Cisco en 2012 y estandarizada mediante IEEE 1934-2018 a través del OpenFog Consortium."
paired_with: fog-computing.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - f345f8ea5a699dc244b42a4e8493130ca319a151a5e2a82166115364b99fbda4
thesis_alignment: "La computación en la niebla define la capa de computación distribuida intermedia entre los dispositivos IoT de borde y los centros de datos en la nube — comprender su arquitectura es fundamental para razonar sobre la latencia, el ancho de banda y la topología de implementación para los servicios de plataforma distribuidos."
keynote: false
---

La computación en la niebla — también llamada red de niebla o *fogging* — es una arquitectura de computación distribuida que utiliza dispositivos de borde para realizar una parte sustancial de la computación, el almacenamiento y la comunicación localmente, con datos enrutados a través del backbone de internet solo cuando es necesario. El término fue acuñado por Cisco en 2012 para describir un enfoque de la computación distribuida que aborda las limitaciones de la computación en la nube para aplicaciones IoT en tiempo real, sensibles a la latencia y limitadas por el ancho de banda.

La metáfora de la "niebla" se refiere a propiedades similares a las de la nube llevadas más cerca del "suelo" — a los dispositivos IoT y de borde que generan datos. Donde la computación en la nube centraliza el procesamiento en centros de datos remotos, la computación en la niebla lo distribuye a unidades informáticas co-ubicadas con los dispositivos que generan datos.

## Concepto

El paradigma de la computación en la niebla surgió de un problema específico: la proliferación de dispositivos del Internet de las Cosas que generan voluminosos datos de sensores que, si se enviaran completamente a los centros de datos en la nube para su procesamiento, superarían el ancho de banda disponible del backbone e introducirían latencias incompatibles con las aplicaciones en tiempo real.

La computación en la niebla se caracteriza por: proximidad a los usuarios finales; distribución geográfica densa; conciencia del contexto respecto a los recursos computacionales e IoT; reducción de la latencia y ahorro del ancho de banda del backbone; y redundancia en caso de fallo.

## Arquitectura

Una arquitectura de computación en la niebla consta de un plano de control y un plano de datos. Los nodos de niebla — unidades informáticas intermedias entre los dispositivos de borde y la nube — reciben datos de los dispositivos de borde, los procesan localmente y reenvían solo los resultados relevantes o resúmenes agregados a la nube.

El NIST Special Publication 500-325 (marzo de 2018) define formalmente la computación en la niebla como "un paradigma de recursos físicos o virtuales horizontal, que reside entre los dispositivos inteligentes de extremo y la computación en la nube tradicional o el centro de datos".

## Historia y normas

El término "computación en la niebla" fue desarrollado por primera vez por Cisco en 2012. El 19 de noviembre de 2015, Cisco Systems, ARM Holdings, Dell, Intel, Microsoft y la Universidad de Princeton fundaron el OpenFog Consortium para promover el desarrollo y la adopción de la computación en la niebla. El IEEE adoptó los estándares de computación en la niebla propuestos por el OpenFog Consortium; el estándar principal es IEEE 1934-2018.

Los casos de uso IoT soportados por la computación en la niebla incluyen vehículos conectados, dispositivos de monitoreo de salud portátiles, realidad aumentada y enjambres de drones inteligentes. El Comando de Sistemas Espaciales y de Guerra Naval de la Marina de los EE.UU. (SPAWAR) ha prototipado implementaciones de Red de Malla Tolerante a la Interrupción escalable y segura usando arquitectura de computación en la niebla.

---

*citas: [[edge-computing]], [[application-programming-interface]], [[computer-appliance]], [[virtual-appliance]]*
