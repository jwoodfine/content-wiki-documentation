---
schema: foundry-doc-v1
content_type: topic
title: "Arquitectura de Ventas de Licencias Cripto"
slug: topic-crypto-license-sales-architecture
aliases:
  - topic-crypto-license-sales-architecture
short_description: "Cómo PointSav conduce a un cliente desde la intención de pago, a través de la liquidación en cadena, hasta un token de licencia criptográfico que otorga acceso binario, sin procesadores de pago tradicionales."
category: architecture
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: topic-crypto-license-sales-architecture.md
cites: []
---

# Arquitectura de Ventas de Licencias Cripto

La arquitectura de ventas de licencias cripto describe cómo un cliente avanza desde la
expresión de intención de compra, a través del pago en cadena, hasta la recepción de un
token de licencia que otorga acceso binario, sin que un procesador de pago tradicional
ni un proveedor de identidad intervengan en la ruta crítica.

## Principios de Diseño

Tres principios dan forma a la arquitectura:

1. **Pago e identidad están separados.** La dirección de pago en cadena se deriva
   determinísticamente de un índice de cliente; no se requiere información de identidad
   antes de que llegue el pago.
2. **El token de licencia es el único portador de confianza.** Una vez emitido, el token
   de licencia puede ser verificado por el servidor binario sin contactar ningún otro
   servicio.
3. **La custodia de claves permanece con el cliente.** El marketplace nunca retiene una
   clave privada en nombre del cliente. El par de claves Ed25519 derivado en el momento
   de la emisión es la credencial del cliente.

## Flujo Completo

### Paso 1 — Derivación de Dirección

Cuando un cliente crea un pedido en `app-privategit-marketplace`, el marketplace solicita
una dirección de pago a `tool-wallet`. El monedero deriva una dirección HD usando la ruta
BIP-32 `m/44'/60'/0'/0/<customer_index>` a partir de un mnemónico BIP-39 almacenado en
su almacén de claves. La dirección Polygon derivada es única para ese espacio de cliente
y se devuelve al marketplace para su presentación.

### Paso 2 — Pago en Cadena

El cliente envía USDC en la red Polygon a la dirección mostrada. `tool-wallet` consulta
el endpoint RPC de Polygon a intervalos configurables. Cuando una transferencia a la
dirección del cliente se confirma con la profundidad de bloque requerida, el monedero
escribe un recibo de pago en su almacén de solo escritura y notifica al marketplace.

El monedero no envía transacciones; únicamente las lee.

### Paso 3 — Emisión de Licencia

Al recibir la confirmación de pago, `app-privategit-marketplace` solicita a `tool-wallet`
que genere un par de claves Ed25519 para esta licencia. La clave pública se almacena en
el registro de licencias del marketplace. El token de licencia firmado se construye con:

| Campo | Valor en la emisión |
|---|---|
| `product_id` | Identificador del producto pedido |
| `version_constraint` | Rango de versiones adquiridas |
| `customer_id` | ID opaco del cliente en el marketplace |
| `issued_at` | Marca de tiempo Unix actual |
| `expires_at` | 0 (perpetuo) o expiración configurada |

El token se firma con la clave privada Ed25519 generada en este paso. La clave privada se
entrega al cliente y no es retenida por el marketplace. El marketplace únicamente retiene
la clave pública para consultas de verificación posteriores.

### Paso 4 — Entrega del Token

El token de licencia firmado se entrega al cliente mediante HTTPS. El cliente almacena
el token y lo presenta en el encabezado `Authorization: Bearer <token>` en todas las
solicitudes de descarga posteriores a `app-privategit-source`.

### Paso 5 — Acceso Binario

`app-privategit-source` recibe la solicitud de descarga con el token incluido. Decodifica
el token, recupera la clave pública de su registro de licencias local y verifica la firma
Ed25519 de forma local. Si los campos de producto y versión del token coinciden con el
binario solicitado, el binario se sirve. El servidor binario no contacta ningún servicio
externo durante este paso.

La sincronización del registro entre el marketplace y el servidor binario está prevista
para una fase futura; en la fase actual, el registro se alimenta por escritura directa en
el momento de la emisión.

## Modos de Fallo

| Fallo | Comportamiento |
|---|---|
| RPC de Polygon no disponible | El monedero acumula verificaciones pendientes; sin impacto en tokens existentes |
| Marketplace no disponible | Nuevos pedidos bloqueados; los tokens de licencia existentes siguen funcionando |
| Servidor binario no disponible | Descargas bloqueadas; los tokens de licencia permanecen válidos |
| Token expirado | El servidor binario devuelve 403; el cliente debe renovar a través del marketplace |

## Custodia de Claves

La arquitectura garantiza que ningún servicio único tenga a la vez la capacidad de
confirmar un pago y la de emitir una licencia válida. `tool-wallet` retiene el mnemónico
BIP-39 (derivación de dirección y generación de claves Ed25519) pero no tiene acceso al
catálogo de productos ni a los registros de clientes. `app-privategit-marketplace` retiene
el catálogo de productos y los registros de clientes, pero únicamente llama al monedero
para la generación de claves y la confirmación de pago; no retiene el mnemónico BIP-39
directamente.

## Véase También

- [[topic-software-distribution-substrate|Sustrato de Distribución de Software]] —
  inventario de componentes y visión general del despliegue
- [[topic-private-git-paid-customer-endpoint|Endpoint de Cliente de Pago en Git Privado]] —
  el servidor binario desde la perspectiva del cliente
- [[topic-ppn-small-business-compute|Cómputo PPN para Pequeñas Empresas]] —
  capacidad de cómputo vendida a través de esta misma arquitectura

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
