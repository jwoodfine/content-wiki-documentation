---
schema: foundry-doc-v1
title: "Cómo rotar claves y tokens de capacidad"
slug: rotate-keys
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: rotate-keys.md
---

La rotación de claves reemplaza un par de claves Ed25519 y su token de capacidad asociado antes de que las credenciales antiguas venzan o después de una posible compromisión. La rotación es una operación planificada con una breve ventana de transición durante la cual tanto el token antiguo como el nuevo son válidos. Esta guía cubre la secuencia completa de rotación: generar un nuevo par de claves, emitir un nuevo token, hacer la transición del destinatario y revocar el token antiguo.

Para el modelo de autorización, véase [[machine-based-auth]]. Para emitir un token desde cero, véase [[issue-capability-token]].

## Requisitos previos

- Acceso al servicio de emisión de tokens con alcance de administrador
- La identidad del titular de las credenciales (la clave pública del par de claves antiguo o el identificador del dispositivo)
- Una ventana de coordinación: tanto el titular como el servicio de emisión deben estar disponibles

## Paso 1: Generar un nuevo par de claves en el dispositivo del destinatario

El titular de las credenciales genera un nuevo par de claves Ed25519 en su dispositivo. La clave privada nunca sale del dispositivo; solo la clave pública se comparte con el emisor.

Para una sesión de consola:

```
os-console --generate-keypair --out new-key
```

Para un nodo PPN:

```
service-vm-host --generate-keypair --out /etc/ppn/new-key
```

Ambos comandos escriben un `new-key.pub` (clave pública, base64) y un `new-key` (clave privada, solo local). Registre el valor de la clave pública para el paso 2.

## Paso 2: Emitir un nuevo token con el nuevo par de claves

Usando la nueva clave pública, solicite un nuevo token de capacidad con el mismo alcance que el anterior:

```
curl -X POST http://<host-servicio-emisión>:<puerto>/v1/tokens \
  -H "Authorization: Bearer <token-admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_pubkey": "<nueva-clave-publica-base64>",
    "scope": "<mismo-alcance-que-token-antiguo>",
    "expires_in_seconds": 86400
  }'
```

La respuesta es una nueva carga útil de token firmado. No la entregue todavía.

## Paso 3: Entregar y cargar el nuevo token

Entregue el nuevo token al titular de las credenciales a través de un canal de confianza. El titular lo carga junto con el token antiguo — durante la ventana de transición, ambos son válidos:

```
os-console --load-token <carga-útil-nuevo-token>
```

Para un servicio:

```
export PLATFORM_TOKEN=<carga-útil-nuevo-token>
```

Verifique que la API acepta el nuevo token antes de continuar. Si el nuevo token es rechazado, no revoque el token antiguo — investigue primero el motivo del rechazo.

## Paso 4: Revocar el token antiguo

Una vez que el titular confirma que el nuevo token funciona, revoque el token antiguo:

```
curl -X DELETE http://<host-servicio-emisión>:<puerto>/v1/tokens/<id-token-antiguo> \
  -H "Authorization: Bearer <token-admin>"
```

El ID del token antiguo es el campo `jti` (JWT ID) de la carga útil del token original, o la clave pública del sujeto si el servicio de emisión usa la clave pública como clave de búsqueda. Después de la revocación, el token antiguo devuelve 401 en cualquier llamada a la API.

## Paso 5: Eliminar el par de claves antiguo del dispositivo

Después de confirmar que el token antiguo está revocado y el nuevo token funciona, elimine el par de claves antiguo:

```
rm -f /etc/ppn/old-key /etc/ppn/old-key.pub
```

Para una sesión de consola, el par de claves antiguo se elimina a través de:

```
os-console --remove-keypair <huella-digital-clave-antigua>
```

No elimine el par de claves antiguo antes de revocar el token antiguo — si el nuevo token falla y necesita revertir, el par de claves antiguo debe seguir presente.

## Puntos clave

- La rotación es un proceso de tres fases: nuevo token emitido → nuevo token verificado → token antiguo revocado
- Nunca elimine el par de claves antiguo antes de que el token antiguo esté revocado y el nuevo token esté confirmado funcionando
- Ambos tokens son válidos durante la ventana de transición — mantenga la ventana corta (minutos, no días)
- Una rotación causada por una posible compromisión debe omitir la ventana de transición: revoque el token antiguo inmediatamente antes de cargar el nuevo

## Véase también

- [[machine-based-auth]] — el modelo de autorización que rige la validez y revocación de tokens
- [[issue-capability-token]] — cómo emitir un token desde cero cuando no existe un token anterior
- [[pair-a-new-device]] — la secuencia de emparejamiento inicial que precede a la primera emisión de token
- [[verify-worm-ledger]] — confirmar que los eventos de rotación están registrados en el libro mayor de auditoría
- [[service-vm-tenant]] — el proxy de tenant que aplica la validación de tokens en las llamadas a la API
