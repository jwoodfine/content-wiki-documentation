---
schema: foundry-doc-v1
title: "Computación en el Borde"
slug: edge-computing
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
short_description: "Paradigma de computación distribuida que acerca la computación y el almacenamiento de datos a las fuentes de datos — reduciendo los tiempos de respuesta y ahorrando ancho de banda al realizar el procesamiento en nodos de borde de red próximos a los dispositivos que generan datos en lugar de en centros de datos en la nube centralizados — con orígenes en las redes de distribución de contenidos de finales de los años 1990 y aplicaciones que van desde IoT hasta vehículos autónomos e inteligencia artificial en el borde."
paired_with: edge-computing.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - fb6311089e5a0200771a827bd28ebdf0cd293cbc3ac5e50321fb7efec93dc0ed
thesis_alignment: "La computación en el borde define la arquitectura distribuida que traslada el procesamiento desde los centros de datos centralizados al perímetro de la red, directamente relevante para la topología de implementación de la plataforma, el diseño de sistemas IoT y la entrega de servicios sensibles a la latencia."
keynote: false
---

La computación en el borde es un paradigma de computación distribuida que acerca la computación y el almacenamiento de datos a las fuentes de datos. Las motivaciones principales son la mejora de los tiempos de respuesta y la reducción del consumo de ancho de banda: al realizar el procesamiento en nodos próximos a los dispositivos que generan datos en lugar de en centros de datos en la nube centralizados, la computación en el borde reduce la latencia de ida y vuelta entre la entrada y la respuesta y elimina la necesidad de transmitir datos brutos a través de redes de área amplia.

La computación en el borde es una arquitectura más que una tecnología específica. Es una forma de computación distribuida sensible a la topología y a la ubicación — el atributo clave es la proximidad física a las fuentes de datos, no una implementación concreta.

## Orígenes

Los orígenes de la computación en el borde se remontan a las redes de distribución de contenidos (CDN) creadas a finales de los años 1990 para servir contenido web y de vídeo desde servidores de borde desplegados cerca de los usuarios, reduciendo la latencia de entrega de contenido desde los servidores de origen. A principios de los años 2000, estas redes evolucionaron para alojar aplicaciones en servidores de borde, dando lugar a los primeros servicios comerciales de computación en el borde.

Los sistemas del Internet de las Cosas (IoT) son un motor contemporáneo importante de la computación en el borde. Un concepto erróneo común es que la computación en el borde y el IoT son sinónimos; la computación en el borde es el paradigma más amplio y el IoT es una aplicación de él.

Una definición ampliamente citada, propuesta por Karim Arabi en un discurso inaugural de la IEEE DAC de 2014, define la computación en el borde como "toda la computación fuera de la nube que ocurre en el borde de la red, y más específicamente en aplicaciones donde se requiere procesamiento de datos en tiempo real."

## Concepto y volúmenes de datos

La motivación comercial de la computación en el borde descansa en proyecciones sobre el crecimiento del volumen de datos. Se espera que los datos del mundo crezcan un 61 por ciento hasta llegar a 175 zettabytes para 2025 (IDC). Según la firma de investigación Gartner, aproximadamente el 10 por ciento de los datos generados por empresas se procesa fuera de un centro de datos o nube tradicional; Gartner proyectó que esta cifra alcanzaría el 75 por ciento para 2025.

El objetivo de la computación en el borde es trasladar la computación desde los centros de datos hacia el borde de la red, aprovechando objetos inteligentes, teléfonos móviles y pasarelas de red para realizar tareas y proporcionar servicios en nombre de la nube.

## Propiedades

**Privacidad y seguridad.** La naturaleza distribuida de la computación en el borde introduce un cambio en los esquemas de seguridad. Los datos que viajan entre nodos distribuidos requieren mecanismos de cifrado independientes de los modelos de seguridad en la nube. La propiedad de los datos se transfiere de los proveedores de servicios a los usuarios finales.

**Velocidad.** La computación en el borde acerca los recursos analíticos a los usuarios finales, aumentando la capacidad de respuesta. Las aplicaciones que dependen de tiempos de respuesta cortos — sistemas IoT, conducción autónoma, reconocimiento facial (que tarda a un ser humano de 370 a 620 ms en realizar) — se benefician sustancialmente del procesamiento en el borde. La inteligencia artificial en el borde (Edge AI) implementa inteligencia artificial en el entorno de computación en el borde, cerca de donde se recopilan los datos.

**Eficiencia.** Al usar servidores en una red de borde local para realizar el procesamiento computacionalmente intensivo, los datos solo necesitan transmitirse a través de la red local; evitar la transmisión por internet resulta en ahorros significativos de ancho de banda. El reconocimiento de voz es un ejemplo representativo: realizarlo localmente permite enviar el texto reconocido a la nube en lugar de grabaciones de audio bruto.

## Aplicaciones

Las aplicaciones incluyen: gestión de dispositivos IoT; vehículos autónomos y conectados; ciudades inteligentes e Industria 4.0; juegos en la nube/transmisión de píxeles; automatización del hogar; e inteligencia artificial en el borde (Edge AI).

---

*citas: [[fog-computing]], [[application-programming-interface]], [[computer-appliance]]*
