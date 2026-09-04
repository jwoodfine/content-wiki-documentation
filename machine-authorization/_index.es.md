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
last_edited: 2026-09-04
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
- [[pair-a-new-device|Emparejar un dispositivo nuevo]] — Empareja un dispositivo os-console todavía sin emparejar con la malla PPN: leer el código de emparejamiento en la pantalla de arranque, conseguir que un administrador lo apruebe y confirmar la admisión en la red.
- [[issue-capability-token|Emitir un token de capacidad]] — Emite desde service-content un token de emparejamiento firmado con Ed25519 sobre HTTP plano, lo registra en el par receptor y explica la cabecera X-Foundry-Capability, que es una credencial aparte.
- [[rotate-keys|Rotar claves y tokens de capacidad]] — Sustituye una credencial de service-content dentro de los límites reales del sistema: los tokens caducan según un reloj fijo de 24 horas, el solapamiento es inevitable y ningún mecanismo acorta la vida de un token en vigor.
<!-- END AUTO-GENERATED -->

## Inscripción de flota

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: fleet-enrollment -->
- [[enroll-ppn-node|Inscribir un nodo PPN]] — Inscribe una máquina en una flota de cómputo PPN estableciendo las tres variables de entorno obligatorias de service-vm-host, ejecutándolo bajo systemd y confirmando el nodo en el listado del controlador.
<!-- END AUTO-GENERATED -->

## Distribución de software

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: software-distribution -->
- [[authenticate-binary-downloads|Autenticar descargas de binarios]] — Autentica una versión de software.pointsav.com: confirmar el pedido en cadena, seguir el enlace de descarga que acuña un token Ed25519 y entender en qué punto ocurre realmente la verificación.
<!-- END AUTO-GENERATED -->

Cada guía tiene sus propios prerrequisitos, pasos de verificación y procedimiento de
reversión; esta página no los repite. La operación cotidiana de un despliegue en marcha
está en [Cómo lo opera](/category/how-to).

## Véase también

- [Cómo lo opera](/category/how-to) — las guías operativas cotidianas restantes
- [Seguridad y confianza](/category/security) — el modelo de identidad y permisos en el que participan estos mecanismos
- [Autoalojamiento](/category/self-hosting) — desplegar los aparatos contra los que se autentican estas credenciales
