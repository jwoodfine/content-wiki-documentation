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
last_edited: 2026-07-31
editor: woodfine-editorial
short_description: "Arquitectura distribuida que sitúa cómputo, almacenamiento y servicios de red entre dispositivos de borde y la nube, definida por Cisco en 2012 y estandarizada en IEEE 1934-2018."
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

Una arquitectura de computación en la niebla consta de un plano de control y un plano de datos. En el plano de datos, la computación en la niebla permite que los servicios de cómputo residan en el borde de la red, en lugar de en servidores de un centro de datos. Los nodos de niebla — unidades informáticas intermedias entre los dispositivos de borde y la nube — reciben datos de los dispositivos de borde, los procesan localmente y reenvían solo los resultados relevantes o resúmenes agregados a la nube.

### Definición del NIST y el límite con la computación de borde

El NIST Special Publication 500-325 (marzo de 2018) define formalmente la computación en la niebla como "un paradigma de recursos físicos o virtuales horizontal, que reside entre los dispositivos inteligentes de extremo y la computación en la nube tradicional o el centro de datos" y afirma que este paradigma "soporta aplicaciones verticalmente aisladas y sensibles a la latencia mediante la provisión de computación, almacenamiento y conectividad de red ubicua, escalable, en capas y federada".

El NIST distingue además la computación en la niebla de la computación de borde: en el modelo teórico, los nodos de computación en la niebla operan física y funcionalmente entre los nodos de borde y la nube centralizada. "La computación en la niebla se distingue principalmente por su distancia respecto al borde." Para despliegues más pequeños, niebla y borde suelen usarse indistintamente; para despliegues de ciudades inteligentes a gran escala, la computación en la niebla constituye una capa intermedia diferenciada.

## Comparación con la computación en la nube y de borde

Tanto la computación en la nube como la computación en la niebla proporcionan almacenamiento, aplicaciones y datos a los usuarios finales. La computación en la niebla está más cerca de los usuarios finales que la computación en la nube y ofrece una distribución geográfica más amplia. La computación en la niebla implica la distribución de recursos y servicios de comunicación, cómputo y almacenamiento sobre — o cerca de — los dispositivos y sistemas bajo el control de los usuarios finales.

La computación en la niebla es un nivel intermedio de potencia de cómputo, de peso medio. En lugar de sustituir a la computación en la nube, la computación en la niebla actúa como complemento: descarga localmente el procesamiento sensible a la latencia o intensivo en ancho de banda, mientras se apoya en la infraestructura en la nube para el almacenamiento, la analítica y el procesamiento no urgente. La computación en la niebla es más eficiente energéticamente que la computación en la nube cuando se agrega a gran escala en despliegues IoT, porque la eliminación del tránsito de datos innecesario reduce tanto los costos de ancho de banda como la energía consumida por el procesamiento en el centro de datos de datos brutos irrelevantes.

## Historia y normas

El término "computación en la niebla" fue desarrollado por primera vez por Cisco en 2012. El 19 de noviembre de 2015, Cisco Systems, ARM Holdings, Dell, Intel, Microsoft y la Universidad de Princeton fundaron el OpenFog Consortium para promover el desarrollo y la adopción de la computación en la niebla. El IEEE adoptó los estándares de computación en la niebla propuestos por el OpenFog Consortium; el estándar principal es IEEE 1934-2018.

Los casos de uso IoT soportados por la computación en la niebla incluyen vehículos conectados, dispositivos de monitoreo de salud portátiles, realidad aumentada y enjambres de drones inteligentes. El Comando de Sistemas Espaciales y de Guerra Naval de la Marina de los EE.UU. (SPAWAR) ha prototipado implementaciones de Red de Malla Tolerante a la Interrupción escalable y segura usando arquitectura de computación en la niebla, con el fin de proteger activos militares estratégicos, incluidos sistemas IoT fijos y móviles.

La norma ISO/IEC 20248 establece un método mediante el cual los datos de objetos identificados por computación de borde utilizando Portadores de Datos de Identificación Automática (AIDC) — códigos de barras y etiquetas RFID — pueden leerse, interpretarse, verificarse y ponerse a disposición en la niebla y en el borde, incluso después de que la etiqueta AIDC se haya desplazado.

---

*citas: [[edge-computing]], [[application-programming-interface]], [[computer-appliance]], [[virtual-appliance]]*
