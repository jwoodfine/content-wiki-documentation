---
schema: foundry-doc-v1
title: "Interfaz de Programación de Aplicaciones"
slug: application-programming-interface
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
short_description: "Una interfaz definida que permite la comunicación entre dos o más sistemas de software — especificando las llamadas o solicitudes que pueden realizarse, cómo realizarlas y los formatos de datos utilizados — con orígenes en la informática británica de los años 1940, definición formal en un artículo de la AFIPS de 1968 y dominio contemporáneo a través de las API web basadas en REST que constituyen el mecanismo de integración principal de la internet moderna."
paired_with: application-programming-interface.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - 4b97263b79ad51000cb9daf66b6f154ef8ea80cc64d9fe220be227e1699ddc99
thesis_alignment: "La API es la primitiva de integración fundamental de los sistemas informáticos distribuidos; comprender sus definiciones, historia y principios de diseño es prerequisito para razonar sobre la arquitectura del sistema, la comunicación entre servicios y el diseño de plataformas."
keynote: false
---

Una interfaz de programación de aplicaciones (API, por sus siglas en inglés) es una forma en que dos o más programas informáticos se comunican entre sí. Es un tipo de interfaz de software que ofrece servicios a otras piezas de software. Un documento o estándar que describe cómo construir o usar dicha conexión se denomina especificación de API; se dice que un sistema informático que cumple el estándar implementa o expone una API.

Una API se distingue de una interfaz de usuario por su consumidor previsto: una interfaz de usuario conecta al usuario humano con el sistema; una API conecta programas de software entre sí. Una API no está destinada a ser utilizada directamente por una persona sino por un programador que la incorpora en un software más grande. Las llamadas que componen una API se conocen como subrutinas, métodos, solicitudes o puntos de conexión, dependiendo del estilo arquitectónico.

## Historia

**Años 1940–1950.** La base conceptual de la API fue establecida por los científicos informáticos británicos Maurice Wilkes y David Wheeler en su trabajo desarrollando una biblioteca de software modular para EDSAC, un ordenador primitivo, en la década de 1940. Su libro de 1951 *The Preparation of Programs for an Electronic Digital Computer* contiene la primera especificación de API publicada.

**Años 1960–1970.** El término "application program interface" (interfaz de programa de aplicación) apareció por primera vez en un artículo de 1968 titulado *Data structures and techniques for remote computer graphics*, presentado en una conferencia de la Association for Information Processing Societies (AFIPS). El término fue introducido en el campo de las bases de datos por C.J. Date en un artículo de 1974; se convirtió en parte del marco ANSI/SPARC para sistemas de gestión de bases de datos.

**Años 1990.** Para 1990, la API era definida por el tecnólogo Carl Malamud simplemente como "un conjunto de servicios disponibles para un programador para realizar ciertas tareas". El concepto se amplió con el surgimiento de las llamadas a procedimientos remotos y las API web. En la década de 1990, con la difusión de internet, estándares como CORBA, COM y DCOM compitieron para convertirse en el mecanismo dominante para exponer servicios API a través de redes.

**Años 2000 hasta el presente.** La disertación de Roy Fielding de 2000 en la Universidad de California en Irvine definió la Transferencia de Estado Representacional (REST) y describió la idea de una "interfaz de programación de aplicaciones basada en red". Las API web XML y JSON vieron una adopción comercial generalizada a partir del año 2000. La reciente proliferación de arquitecturas de microservicios ha convertido el diseño de API en un aspecto central de la arquitectura de software empresarial.

## Tipos

**API de bibliotecas.** La interfaz de una biblioteca de software es un tipo de API. La API describe y prescribe el "comportamiento esperado" (especificación) mientras que la biblioteca es una "implementación real" de ese conjunto de reglas. Una única API puede tener múltiples implementaciones.

**API de sistemas operativos.** POSIX, por ejemplo, proporciona un conjunto de especificaciones de API comunes diseñadas para permitir que las aplicaciones escritas para un SO compatible con POSIX se compilen para otro. Linux y la Berkeley Software Distribution (BSD) implementan ambos las API POSIX.

**API remotas.** Las API remotas permiten a los desarrolladores manipular recursos remotos a través de protocolos — estándares específicos para la comunicación que permiten que diferentes tecnologías funcionen juntas independientemente del lenguaje o plataforma.

**API web.** Las API web son servicios a los que acceden los dispositivos cliente a un servidor web usando el Protocolo de Transferencia de Hipertexto (HTTP). Los dispositivos cliente envían una solicitud en forma de solicitud HTTP y reciben un mensaje de respuesta típicamente en formato JSON o XML.

## Políticas de publicación

Las API se clasifican típicamente por su política de acceso: las API *privadas* son solo para uso interno de la empresa; las API de *socio* están disponibles solo para socios comerciales específicos bajo acuerdo contractual; las API *públicas* están disponibles para uso general del público, sujetas a autenticación y límites de velocidad.

---

*citas: [[user-interface-design]], [[user-experience-design]], [[fog-computing]], [[edge-computing]]*
