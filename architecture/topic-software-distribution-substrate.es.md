---
schema: foundry-doc-v1
content_type: topic
title: "Sustrato de Distribución de Software"
slug: topic-software-distribution-substrate
aliases:
  - topic-software-distribution-substrate
short_description: "La ruta completa desde el pago del cliente en el marketplace PointSav hasta la entrega autenticada de binarios, implementada mediante tres servicios cooperativos desplegados."
category: architecture
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: TRANSLATE-ES
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: topic-software-distribution-substrate.md
cites: []
---

# Sustrato de Distribución de Software

El sustrato de distribución de software cubre la ruta completa desde el pago del
cliente en el marketplace PointSav, pasando por la emisión del token de licencia, hasta
la entrega autenticada del binario. Tres servicios desplegados forman el sustrato: un
monitor de pagos, una tienda con catálogo de productos y emisión de licencias, y un
servidor de versiones binarias con verificación de tokens.

## Componentes

### Monitor de Pagos (`tool-wallet`)

`tool-wallet` supervisa una dirección en cadena en busca de transferencias entrantes de
USDC en la red Polygon. Para cada transferencia confirmada:

1. Deriva una dirección HD por cliente a partir de un mnemónico BIP-39 mediante BIP-32
   (`m/44'/60'/0'/0/index`).
2. Genera un par de claves Ed25519 para usar como credencial de licencia.
3. Escribe un recibo de pago en el almacén de solo escritura local.

El monedero no tiene estado con respecto a la blockchain: lee transacciones confirmadas
y escribe recibos; no envía transacciones.

### Marketplace (`app-privategit-marketplace`)

`app-privategit-marketplace`, desplegado en `vault-privategit-source-1`, proporciona la
tienda orientada al cliente en `software.pointsav.com`. Sus funciones son:

- Presentar un catálogo de productos de versiones binarias disponibles.
- Aceptar la creación de pedidos y vincular cada pedido a la dirección de pago derivada
  por `tool-wallet` para ese cliente.
- Emitir tokens de licencia firmados al confirmar el pago.
- Verificar los recibos de pago contra el almacén de solo escritura antes de emitir.

El marketplace no retiene material de clave privada para firmar binarios; emite tokens
de licencia que el endpoint binario verifica de forma independiente.

### Servidor de Versiones Binarias (`app-privategit-source`)

`app-privategit-source`, desplegado en `vault-privategit-source-1`, sirve versiones
binarias compiladas a clientes autenticados. Cada solicitud de descarga debe llevar un
token de licencia válido. El servidor:

1. Decodifica el token de licencia Ed25519 del encabezado `Authorization`.
2. Verifica la firma del token contra la clave pública correspondiente almacenada en el
   momento de la emisión.
3. Comprueba los campos de producto y versión del token frente al binario solicitado.
4. Sirve el binario si todas las comprobaciones son correctas; devuelve 403 en caso
   contrario.

El servidor no contacta al marketplace en el momento de la verificación — la
verificación del token es local y puede funcionar sin conexión.

## Formato del Token de Licencia

Los tokens de licencia son cargas útiles firmadas con Ed25519 en un sobre binario
compacto. El cuerpo firmado lleva:

| Campo | Tipo | Propósito |
|---|---|---|
| `product_id` | cadena | Identifica el binario licenciado |
| `version_constraint` | cadena | Rango SemVer o versión exacta |
| `customer_id` | cadena | Identificador opaco del cliente |
| `issued_at` | u64 | Marca de tiempo Unix de emisión |
| `expires_at` | u64 | Marca de tiempo Unix de expiración (0 = perpetuo) |

La revocación de tokens mediante una lista de denegación de IDs de tokens en el servidor
de versiones binarias está prevista para una fase futura; los tokens no son revocables
tras su emisión en la fase actual.

## Modelo de Confianza

El sustrato no asume que el marketplace y el servidor binario compartan un límite de
confianza de red. El token de licencia es el único portador de confianza: un token
emitido por el marketplace es suficiente para el acceso binario sin mayor intervención
del marketplace. Esto permite mover el servidor binario a un host o segmento de red
diferente sin cambios en el marketplace.

## Véase También

- [[topic-crypto-license-sales-architecture|Arquitectura de Ventas de Licencias Cripto]] —
  descripción detallada del flujo de pago a entrega
- [[topic-private-git-paid-customer-endpoint|Endpoint de Cliente de Pago en Git Privado]] —
  el endpoint binario desde la perspectiva del cliente
- [[topic-ppn-small-business-compute|Cómputo PPN para Pequeñas Empresas]] — capacidad
  de cómputo vendida a través del mismo sustrato

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™ y Capability Geometry™ son marcas comerciales de Woodfine Capital Projects Inc., utilizadas en Canadá, los Estados Unidos, América Latina y Europa. Todas las demás marcas comerciales son propiedad de sus respectivos propietarios.*
