---
schema: foundry-doc-v1
title: "Cómo emitir un token de capacidad"
slug: issue-capability-token
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
language: es
language_protocol: TRANSLATE-ES
paired_with: issue-capability-token.md
---

Un token de capacidad es una credencial firmada que otorga a un dispositivo, servicio o sesión acceso a una capacidad específica de la plataforma. Los tokens están firmados con Ed25519, son autodescriptivos y tienen un límite de tiempo. Emitir un token significa generar una credencial firmada usando el material de clave de la plataforma y entregarla al destinatario. Esta guía cubre la emisión de un solo token para un dispositivo o servicio.

Para el modelo de autorización en el que operan los tokens de capacidad, véase [[machine-based-auth]]. Para el flujo completo de emparejamiento que culmina en un token, véase [[pair-a-new-device]].

## Requisitos previos

- Acceso de administrador al servicio de emisión de claves de la plataforma (o el binario `tool-wallet` si se emite a través de integración de cartera)
- La clave pública del destinatario o la identidad del dispositivo verificada
- Conocimiento del alcance de capacidad que se está otorgando (INPUT, USER, READ o un alcance de servicio nombrado)

## Paso 1: Identificar el alcance de capacidad

Los tokens de capacidad llevan un campo de alcance que restringe lo que el portador puede hacer. Antes de emitir, decida el alcance:

| Alcance | Otorga |
|---|---|
| `READ` | Acceso de solo lectura a datos de acceso público; sin escrituras en el libro mayor |
| `USER` | Acceso de sesión estándar; puede leer datos de entidades, enviar consultas |
| `INPUT` | Acceso completo de operador; puede escribir en el libro mayor WORM, activar la Máquina de Entrada F12 |
| `service:<nombre>` | Alcance de servicio a servicio nombrado; restringe el token a una API de servicio específica |

Otorgue el alcance mínimo que satisfaga el caso de uso. Los tokens no pueden reducirse después de la emisión — emita un nuevo token con un alcance más reducido si el original es demasiado amplio.

## Paso 2: Obtener la clave pública del destinatario

El destinatario genera un par de claves Ed25519 en su dispositivo y proporciona la clave pública. La clave pública es un valor de 32 bytes, típicamente codificado como base64 o hex.

Para un nodo PPN, la clave pública se genera durante la inicialización del dispositivo y está disponible a través de:

```
service-vm-host --print-pubkey
```

Para una sesión de aplicación, la clave pública es generada por la herramienta de emparejamiento de la plataforma en el momento del emparejamiento y almacenada en el almacén de claves local del dispositivo.

## Paso 3: Emitir el token

Llame al endpoint de emisión de tokens con la clave pública del destinatario y el alcance previsto:

```
curl -X POST http://<host-servicio-emisión>:<puerto>/v1/tokens \
  -H "Authorization: Bearer <token-admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_pubkey": "<clave-publica-base64-destinatario>",
    "scope": "INPUT",
    "expires_in_seconds": 86400
  }'
```

El servicio devuelve una carga útil de token firmada. El token es una estructura JSON autocontenida firmada sobre sus campos con la clave de firma Ed25519 de la plataforma. Copie el valor completo del token — no se almacena del lado del servidor después de la emisión.

## Paso 4: Entregar el token al destinatario

Entregue la carga útil del token firmado al destinatario a través de un canal de confianza. El destinatario carga el token en el almacén de claves local de su dispositivo:

```
os-console --load-token <carga-útil-token>
```

O para un servicio:

```
export PLATFORM_TOKEN=<carga-útil-token>
```

El token se verifica en cada llamada a la API comprobando la firma Ed25519 contra la clave pública publicada de la plataforma.

## Paso 5: Verificar que el token está activo

Después de que el destinatario cargue el token, confirme el acceso verificando la barra de estado de la consola (el alcance debe mostrar el nivel esperado) o consultando el endpoint de verificación de tokens:

```
curl -X POST http://<host-servicio-emisión>:<puerto>/v1/tokens/verify \
  -H "Content-Type: application/json" \
  -d '{"token": "<carga-útil-token>"}'
```

Un token válido devuelve el alcance, la fecha de vencimiento y la clave pública del sujeto. Una firma inválida o un token vencido devuelve una respuesta 401 con un motivo de rechazo.

## Puntos clave

- Los tokens están firmados con Ed25519 y son autocontenidos — el emisor no necesita almacenarlos después de la entrega
- Otorgue el alcance mínimo; los tokens no pueden reducirse después de la emisión
- La entrega del token debe usar un canal de confianza — el token en sí mismo demuestra que el portador tiene la clave privada, pero la entrega determina quién lo recibe
- El endpoint de verificación de tokens de la plataforma puede confirmar la validez de un token sin una sesión activa

## Véase también

- [[machine-based-auth]] — el modelo de autorización del que forman parte los tokens de capacidad
- [[pair-a-new-device]] — el flujo completo de emparejamiento de dispositivos que produce un token como último paso
- [[rotate-keys]] — cómo reemplazar un token y su par de claves subyacente al vencer o comprometerse
- [[crypto-license-sales-architecture]] — el modelo de licencia criptográfica utilizado para tokens de distribución de software
- [[service-vm-tenant]] — el servicio proxy de tenant que valida los tokens en las llamadas a la API
