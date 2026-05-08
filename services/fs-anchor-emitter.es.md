---
schema: foundry-doc-v1
title: "fs-anchor-emitter"
slug: fs-anchor-emitter.es
category: services
type: topic
quality: complete
short_description: "fs-anchor-emitter genera puntos de control firmados del libro mayor inmutable Write-Once-Read-Many a cadencia horaria y los prepara para el anclaje externo al registro público de transparencia Sigstore Rekor con cadencia mensual — el mecanismo que hace que el estado del libro mayor de la plataforma sea criptográficamente auditable desde fuera de la plataforma misma."
status: active
audience: vendor-public
bcsc_class: current-fact
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: fs-anchor-emitter.md
---

`fs-anchor-emitter` es el componente que genera puntos de control firmados del libro mayor inmutable Write-Once-Read-Many a cadencia horaria y los prepara para el anclaje externo al registro público de transparencia Sigstore Rekor con cadencia mensual — el mecanismo que hace que el estado del libro mayor de la plataforma sea criptográficamente auditable desde fuera de la plataforma. El emisor opera en la Capa 4 de la pila WORM, lee el estado actual del árbol de mosaicos por inquilino, genera un punto de control en formato `signed-note` y lo almacena en la ruta autoritativa bajo `$FS_LEDGER_ROOT/<moduleId>/checkpoint`. El proceso mensual de anclaje del espacio de trabajo consume esos puntos de control y los publica en el registro público de transparencia.

## Requisitos de Configuración

El emisor requiere las siguientes variables de entorno:
- **FS_LEDGER_ROOT:** Ubicación de los datos del cliente.
- **FS_SIGNING_KEY:** Ruta a la clave privada del cliente (Ed25519).
- **FS_ANCHOR_INTERVAL:** Frecuencia de generación (se recomienda 1 hora).

## Funcionamiento

1. **Generación de Firma:** El emisor lee el estado actual del ledger y genera un archivo de texto con el tamaño del árbol y el hash raíz.
2. **Formato Estándar:** Utiliza el formato `signed-note` de C2SP, compatible con el ecosistema Sigstore Rekor.
3. **Prueba de Consistencia:** Se prevé que el sistema verifique que el nuevo estado sea una continuación válida del anterior antes de firmar, detectando cualquier intento de manipulación accidental o malintencionada.

## Anclaje Externo

Aunque los puntos de control se generan cada hora, su publicación en la red de transparencia Rekor está programada actualmente para realizarse de forma mensual, proporcionando una prueba de existencia externa e irrefutable de los datos de la empresa.

## Véase también

- [[service-fs-architecture]]
- [[service-fs-security-compliance]]
- [[worm-ledger-design]]
