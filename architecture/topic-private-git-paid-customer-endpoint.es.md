---
schema: foundry-doc-v1
content_type: topic
title: "Endpoint de Cliente de Pago en Git Privado"
slug: topic-private-git-paid-customer-endpoint
aliases:
  - topic-private-git-paid-customer-endpoint
short_description: "El servidor de versiones binarias que entrega software PointSav compilado a clientes con tokens de licencia Ed25519 válidos, realizando toda la verificación localmente sin llamadas a servicios externos."
category: architecture
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: topic-private-git-paid-customer-endpoint.md
cites: []
---

# Endpoint de Cliente de Pago en Git Privado

El endpoint de cliente de pago en git privado es el servidor de versiones binarias que
entrega software PointSav compilado a clientes que poseen tokens de licencia válidos. A
pesar del término "git" en el nombre, el endpoint sirve artefactos binarios precompilados
en lugar de repositorios git; el nombre refleja su posición en la infraestructura
PointSav como sucesor de una superficie prevista de alojamiento git privado.

El servicio es `app-privategit-source`, desplegado en `vault-privategit-source-1`.

## Qué Sirve el Endpoint

El endpoint sirve artefactos de versión binaria: ejecutables compilados, archivos
comprimidos y metadatos asociados. Cada artefacto se asocia con un `product_id` y una
cadena de versión. El catálogo de productos es alimentado por el marketplace
(`app-privategit-marketplace`) en el momento de la publicación del binario.

No se sirve código fuente. No se habla protocolo git. La API HTTP es la única superficie
de acceso.

## Autenticación

Cada solicitud de descarga debe llevar un token de licencia Ed25519 en el encabezado
`Authorization`:

```
Authorization: Bearer <token-codificado-en-base64url>
```

El token es emitido por `app-privategit-marketplace` en el momento de la compra y
entregado al cliente. El servidor binario verifica el token localmente:

1. Decodifica el sobre del token y recupera la referencia a la clave pública.
2. Busca la clave pública correspondiente en su registro de licencias local.
3. Verifica la firma Ed25519 sobre el cuerpo del token.
4. Comprueba que los campos `product_id` y `version_constraint` del token cubren el
   binario solicitado.

El paso 4 es la decisión de autorización: un token comprado para el producto A no otorga
acceso al producto B, y un token para la versión 1.x no otorga acceso a la versión 2.0.

## API

| Endpoint | Método | Auth requerida | Descripción |
|---|---|---|---|
| `/v1/binaries/:product_id/:version` | GET | Token Bearer | Descargar binario |
| `/v1/catalog` | GET | Token Bearer | Listar productos y versiones disponibles |
| `/v1/token/info` | GET | Token Bearer | Devolver metadatos del token (producto, expiración) |
| `/healthz` | GET | Ninguna | Sonda de salud |

## Verificación Sin Conexión

El servidor binario realiza toda la verificación sin contactar al marketplace ni a
ningún servicio externo en el momento de la solicitud. El registro de licencias (un
almacén de claves local alimentado desde el marketplace en el momento de la publicación)
es la única dependencia para la verificación de tokens. Esto significa que el servidor
binario puede servir descargas durante una interrupción del marketplace, y puede
desplegarse en un entorno aislado de red.

## Sincronización del Registro de Licencias

El registro de licencias local se alimenta cuando el marketplace publica un nuevo
binario o cuando se emite un token de licencia. La sincronización del registro entre el
marketplace y el servidor binario está prevista para una fase futura; en la fase actual,
el registro se alimenta por escritura directa en el momento de la emisión por parte del
marketplace.

## Ciclo de Vida del Token

Los tokens pueden ser perpetuos (`expires_at = 0`) o con límite de tiempo. El servidor
binario aplica la expiración en el momento de cada solicitud. La revocación de tokens
mediante una lista de denegación de IDs de tokens está prevista para una fase futura; en
la fase actual el servidor binario no mantiene una lista de revocación, por lo que un
token permanece utilizable hasta su marca de tiempo de expiración.

Los clientes con tokens expirados deben renovarlos a través de `app-privategit-marketplace`.
La renovación emite un nuevo token.

## Véase También

- [[topic-software-distribution-substrate|Sustrato de Distribución de Software]] —
  inventario completo de componentes, incluidos el marketplace y el monitor de pagos
- [[topic-crypto-license-sales-architecture|Arquitectura de Ventas de Licencias Cripto]] —
  cómo se genera y entrega un token de licencia antes de llegar a este endpoint

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
