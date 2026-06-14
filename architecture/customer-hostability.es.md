---
schema: foundry-doc-v1
title: "Hospedaje por el cliente"
slug: customer-hostability.es
short_description: "La capacidad de alojamiento del cliente es el compromiso arquitectónico de que cada artefacto de PointSav pueda ejecutarse en el hardware del cliente, contra las claves del cliente, con el libro mayor de auditoría del cliente — haciendo que la implementación autohospedada sea el patrón canónico, no un nivel."
category: architecture
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: customer-hostability.md
---


La disciplina de hospedaje por el cliente es el
compromiso arquitectónico de que cada artefacto que un cliente
adopta puede ejecutarse sobre metal del cliente, con datos del
cliente, contra llaves del cliente, con un libro de auditoría
del cliente. El cliente puede bifurcarlo desde el día uno.

No es un nivel de precios ni una opción de despliegue. Es la
forma del sustrato. Una variante de la plataforma que requiera
infraestructura alojada por el proveedor para funcionar no es
hospedable por el cliente por construcción. Véase también [[customer-first-ordering|orden cliente primero]], [[six-tier-sovereignty-matrix|la matriz de soberanía de seis niveles]] y [[economic-model|el modelo económico]].

## Tres compromisos concretos

1. **Bootstrap auto-hospedable.** Cada servicio de la plataforma envía un
 `bootstrap.sh` que levanta el servicio en la máquina propia
 del cliente — sin dependencia SaaS, sin login con proveedor,
 sin API medida.
2. **Adaptadores por inquilino en el sistema de archivos del
 cliente.** Cuando el adaptador del cliente entrena sobre el
 corpus del cliente, el `.lora` resultante vive en
 `data/adapters/` dentro del sustrato del cliente.
3. **Libro de auditoría anclado en el cliente.** El [[apprenticeship-substrate|corpus de
 aprendizaje]] vive en `data/training-corpus/apprenticeship/`
 dentro del sustrato del cliente. Los registros privados de
 inquilino nunca salen de la infraestructura del cliente.

## Por qué los hiperescaladores no pueden replicar esto

Su economía unitaria depende de entrenamiento central, raíces
de confianza compartidas y atestación anclada en el proveedor.
La pre-formación continuada por cliente no calza a escala PYME
con esa economía. La plataforma está construida para que la postura
regulatoria del cliente no dependa de la del proveedor.

## Qué no es el hospedaje por el cliente

- No es licencia de código abierto permisiva. Una licencia
 permisiva sobre un servicio que requiere plano de control
 alojado no satisface el hospedaje por el cliente.
- No es "el proveedor lo aloja por ti". El alojamiento por
 proveedor es una opción operativa, no la forma canónica.
- No es exportación de datos. El hospedaje por el cliente es
 estructural — los datos ya están en el metal del cliente
 desde el momento en que se escribieron.

## Prueba operativa

Un servicio nuevo de la plataforma es hospedable por el cliente si éste
puede clonar los repositorios, ejecutar `bootstrap.sh` en una
máquina propia, generar y servir adaptadores desde disco local,
operar el servicio sin contactar nunca un endpoint del
proveedor, y auditar cada petición, respuesta y actualización
de adaptador localmente.

## Véase también

- [Documento canónico en inglés](topic-customer-hostability.md)
- [El sustrato de protocolo de lenguaje](topic-language-protocol-substrate.md)
- [Disciplina anti-homogenización](topic-anti-homogenization-discipline.md)
