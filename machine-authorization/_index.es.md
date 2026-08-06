---
schema: foundry-doc-v1
title: "Autorización de Máquinas"
slug: machine-authorization-index
category: machine-authorization
type: topic
content_type: topic
index_type: thematic
index_scope: machine-authorization
quality: complete
short_description: "Emparejar dispositivos y nodos en la red, emitir y rotar tokens de capacidad servicio a servicio, y autenticar descargas de binarios."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: _index.md
---

**La autorización de máquinas** cubre los mecanismos de credenciales y admisión que determinan quién y qué puede actuar sobre la plataforma — emparejar un dispositivo a la malla WireGuard, emitir y rotar los tokens de capacidad Ed25519 que los servicios usan para autenticarse entre sí, inscribir un nodo de cómputo en una flota, y autenticar una descarga de binario firmada. Son mecanismos genuinamente distintos, no un solo sistema con nombres diferentes; cada guía indica con claridad dónde están los límites reales de su propio mecanismo, incluyendo los casos en los que hoy no existe ningún comando de revocación o desemparejamiento.

<!-- START-HERE-HIGHLIGHT: el motor lee este bloque para la tarjeta "empezar aquí"
     (reutiliza el componente cluster-card--start-here existente). No añadir más de una. -->

**Empiece aquí:** [[pair-a-new-device|Emparejar un dispositivo nuevo]] — registra un dispositivo con el servidor de emparejamiento y recorre la aprobación del administrador, el punto de entrada más común a esta categoría.

<!-- END-START-HERE-HIGHLIGHT -->

## Emparejamiento y tokens

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: pairing-and-tokens -->
- [[pair-a-new-device|Emparejar un dispositivo nuevo]] — registre un dispositivo os-console y logre que se apruebe en la malla WireGuard
- [[issue-capability-token|Emitir un token de capacidad]] — genere un token firmado con Ed25519 y regístrelo con un servicio par
- [[rotate-keys|Rotar claves y tokens de capacidad]] — reemplace una credencial dentro de los límites reales de expiración de 24 horas del sistema
<!-- END AUTO-GENERATED -->

## Inscripción de flota

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: fleet-enrollment -->
- [[enroll-ppn-node|Inscribir un nodo PPN]] — inicie el agente de latido por nodo y confírmelo en el controlador de la flota
<!-- END AUTO-GENERATED -->

## Distribución de software

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: software-distribution -->
- [[authenticate-binary-downloads|Autenticar descargas de binarios]] — confirme un pedido y siga la ruta de descarga firmada de una versión
<!-- END AUTO-GENERATED -->

Cada guía tiene sus propios prerrequisitos, pasos de verificación y procedimiento de
reversión; esta página no los repite. La operación cotidiana de un despliegue en marcha
está en [Cómo lo opera](/category/how-to).

## Véase también

- [Cómo lo opera](/category/how-to) — las guías operativas cotidianas restantes
- [Seguridad y confianza](/category/security) — el modelo de identidad y permisos en el que participan estos mecanismos
- [Autoalojamiento](/category/self-hosting) — desplegar los aparatos contra los que se autentican estas credenciales
