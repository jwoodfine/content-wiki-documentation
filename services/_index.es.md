---
schema: foundry-doc-v1
title: "Servicios"
slug: _index.es
lang: es
category: services
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.md
---

La arquitectura de tres anillos de PointSav asigna cada servicio a una capa con autoridad y dependencias definidas. Los servicios del Anillo 1 gestionan la ingesta por inquilino: cada uno acepta datos brutos de una fuente externa y los escribe en un libro durable. Los servicios del Anillo 2 proporcionan conocimiento y procesamiento determinista: leen del Anillo 1 y producen registros estructurados, grafos de conocimiento e índices de búsqueda. El Anillo 3 es un único servicio, service-slm, que lee del Anillo 2 y nunca escribe en él.

La plataforma funciona completamente a través de los Anillos 1 y 2 sin cómputo de IA. Eliminar el Anillo 3 reduce la superficie de ataque, satisface los requisitos de aislamiento de red y responde a la pregunta de cumplimiento sobre si la IA ha tocado el registro autoritativo. La respuesta es arquitectónica: los Anillos 1 y 2 no tienen ninguna importación, dependencia ni llamada en tiempo de ejecución que alcance el Anillo 3.

## Anillo 1 — Ingesta en el límite

Servicios de límite por inquilino. Cada uno se ejecuta como un proceso separado por inquilino y expone una interfaz de servidor de Protocolo de Contexto de Modelo.

- [[service-fs-architecture]] — El servicio de sistema de archivos: libro WORM de solo anexado, raíz de almacenamiento por inquilino, la base en la que escribe cada otro servicio del Anillo 1.
- [[service-email]] — Ingesta de correo electrónico: SMTP e IMAP, cargas útiles saneadas, Maildir de solo anexado en almacenamiento local en bloque.
- [[service-people]] — Libro de identidad: registros de personas, asignaciones de roles y el modelo de datos Anchor-Claim-Socket que nunca sobreescribe el estado.

## Anillo 2 — Conocimiento y procesamiento

Servicios de procesamiento determinista. Cada uno lee del Anillo 1 y produce registros estructurados — ninguna varianza de IA entra en el registro autoritativo.

- [[service-extraction]] — El controlador central de tráfico del Anillo 2: elimina el formato propietario, construye Paquetes de Entidades, asigna IDs de transacción, enruta a servicios deterministas o a service-slm.
- [[service-content]] — El Motor de Gravedad: lee cargas útiles brutas de un Totebox, las ejecuta contra una taxonomía institucional, genera los documentos estructurados que publica una organización.
- [[service-search]] — Búsqueda de texto completo sobre Tantivy: fragmentación por inquilino, recuperación en microsegundos, sin proceso de base de datos activo.
- [[service-egress]] — Válvula de liberación física: los registros estructurados salen de la plataforma únicamente a través de este servicio.
- [[archetypes-and-chart-of-accounts]] — La taxonomía institucional: once arquetipos y un Plan de Cuentas que clasifican al personal y los documentos por posición estructural y rol funcional.

## Anillo 3 — Puerta de IA

Un servicio abarca el Anillo 3. Lee del Anillo 2 y produce propuestas que un humano revisa; nunca escribe en el grafo de conocimiento ni en el libro.

- [[service-slm]] — El Portero: enrutamiento de IA entre niveles de cómputo local, de ráfaga y externo; libro de auditoría en cada llamada; todas las claves API retenidas en este límite.
- [[service-slm-yoyo-operational]] — Estado operativo de service-slm y la VM de ráfaga GPU Yo-Yo: configuración de Nivel A/B, cola de borradores de aprendizaje, techo de coste por apagado inactivo.
- [[service-slm-totebox-sysadmin]] — Cómo service-slm se convierte en el asistente operativo para despliegues Totebox: diez familias de tareas operativas, pipeline de cuatro etapas desde la captura del corpus hasta los adaptadores LoRA por inquilino.

## Servicios especializados y de dominio

Servicios construidos para capacidades específicas de la plataforma.

- [[service-business-clustering]] — Convierte datos minoristas brutos en clústeres comerciales: esquema espacial padre-hijo, una entidad comercial por sitio.
- [[service-places-filtering]] — Filtra la infraestructura cívica e institucional para retener solo las instalaciones de grado regional en las clasificaciones GIS.
- [[pointsav-gis-engine]] — Inteligencia de ubicación de alto rendimiento en Rust: primero sin conexión, archivos planos, sin instancias de bases de datos centralizadas.
- [[service-wallet-settlement]] — Infraestructura de cartera y liquidación de pagos directos.
- [[message-courier]] — Motor de automatización web sin interfaz que conecta libros de identidad internos con portales web externos.
- [[fs-anchor-emitter]] — Puntos de control firmados del libro WORM a cadencia horaria, anclados a Sigstore Rekor mensualmente para auditabilidad externa.
- [[service-fs-security-compliance]] — Postura de cumplimiento de service-fs para SEC 17a-4(f), eIDAS y SOC 2 por garantía estructural.
- [[service-fs-data-lake]] — Data lake de archivos planos para el pipeline GIS: puntos geoespaciales brutos de fuentes abiertas, sin paso ETL.
- [[template-ledger]] — Distribuye plantillas de correo electrónico aprobadas al entorno de correo del operador; elimina la desviación de versiones entre el diseño de plantillas y la ejecución.

## Véase también

- [Sistemas](/systems/) — los sistemas operativos dentro de los cuales se ejecutan los servicios
- [Arquitectura](/architecture/) — el modelo de tres anillos y los invariantes que rigen la interacción entre anillos
- [Infraestructura](/infrastructure/) — despliegue de flota y la capa física en la que se ejecutan los servicios
