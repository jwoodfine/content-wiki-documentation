---
schema: foundry-doc-v1
title: "Arquitectura de pagos con criptomonedas y emisión de licencias"
slug: crypto-license-sales-architecture
category: architecture
type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-06-13
editor: pointsav-engineering
paired_with: crypto-license-sales-architecture.md
short_description: "La arquitectura de pagos y licencias de software.pointsav.com: un flujo sin custodia que va desde una transferencia USDC en cadena hasta un token de descarga firmado con Ed25519, sin cuentas de cliente ni intermediarios de pago."
cites: []
---

Una compra de licencia de software en `software.pointsav.com` fluye desde una transferencia
de USDC en Polygon en cadena hasta un token firmado con Ed25519 que autoriza las descargas
de binarios. El diseño no requiere custodia: el cliente nunca crea una cuenta, el proveedor
nunca retiene fondos del cliente más allá del momento de liquidación, y no se necesita ningún
intermediario para enrutar el pago. La arquitectura tiene tres componentes principales —
un observador de pagos, una tienda virtual y un servidor de versiones — descritos aquí
en el nivel de sus interacciones.

## Por qué USDC en Polygon

USDC es una moneda estable vinculada al dólar estadounidense emitida por Circle. Su valor
está anclado al dólar, lo que la hace práctica para compras de software a precio fijo sin
exponer a ninguna de las partes a la volatilidad del tipo de cambio. Polygon PoS es una
cadena compatible con EVM de prueba de participación con comisiones de transacción más
bajas que la red principal de Ethereum, lo que resulta económico para compras en el rango
de pocos dólares. El sistema de pago opera como un observador de solo lectura del estado
público de la cadena de bloques: observa eventos de registro de transferencia ERC-20 en
el contrato USDC dirigidos a la billetera del proveedor. No se requiere ningún contrato
inteligente en el lado del proveedor. Cualquier explorador de cadena de bloques puede
verificar de forma independiente un pago utilizando el hash de la transacción.

## Mecánica del observador de pagos

El observador de pagos consulta el punto de acceso JSON-RPC de Polygon en un intervalo
configurable, avanzando por los bloques confirmados e inspeccionando las entradas de
registro de transferencia ERC-20. Cuando encuentra una transferencia hacia la dirección
de la billetera del proveedor, inspecciona el monto transferido para determinar a qué
nivel de licencia corresponde el pago — los dos niveles corresponden cada uno a un monto
distinto de USDC. Ante cada coincidencia confirmada, escribe un recibo en archivo plano
estructurado que contiene el hash de la transacción, la dirección del remitente, el número
de bloque, la marca de tiempo de confirmación y el identificador de producto derivado.
También añade una entrada a un registro de transacciones JSONL con fines contables y
de auditoría.

Los recibos son la fuente de autoridad. La tienda virtual no emitirá un token de licencia
sin un recibo coincidente en disco. El diseño en dos etapas — el observador escribe el
recibo, la tienda lo lee — significa que la tienda nunca consulta la cadena directamente;
delega esa responsabilidad enteramente en el observador. El observador también admite
una URL de RPC alternativa para resiliencia: si el punto de acceso RPC principal no está
disponible, reintenta contra la alternativa antes de fallar.

## Derivación de dirección por pedido

Por defecto, todos los pagos se dirigen a una única dirección estática de billetera del
proveedor, y el hash de la transacción sirve como identificador de pedido. Para los
clientes que prefieren una dirección de recepción dedicada para el seguimiento de pedidos
o fines contables, la tienda virtual puede derivar una a partir de la semilla maestra
BIP-39 del proveedor utilizando la derivación de clave determinista jerárquica BIP-32
a lo largo de la ruta de derivación estándar de Ethereum. Cada pedido recibe un índice
único, y el mapeo del identificador de pedido al índice de derivación se almacena
localmente. Los pagos a direcciones derivadas son observados y registrados por el mismo
observador que monitorea la dirección estática. El flujo de dirección derivada es
opcional; el flujo estándar de dirección única sigue siendo el predeterminado.

## Emisión de tokens de licencia

Una vez que existe un recibo para un hash de transacción, la tienda virtual emite un
token de licencia firmado con Ed25519. La clave de firma la tiene exclusivamente la tienda
virtual y nunca la abandona. La clave pública de verificación correspondiente la tiene
exclusivamente el servidor de versiones. Ningún componente tiene el material de clave del
otro, y ningún material de clave se transmite al cliente.

La carga útil del token registra el identificador de producto, una fecha de vencimiento
(un año desde el momento de emisión en la configuración actual) y el nivel de licencia
como una lista de autorizaciones. El token se forma anteponiendo la firma Ed25519 de
64 bytes a los bytes de la carga útil sin procesar y codificando el resultado como una
cadena en base64url. El resultado es una cadena opaca única que el cliente almacena y
presenta al servidor de versiones.

## Verificación en el servidor de versiones

La verificación no tiene estado y no requiere ninguna llamada de red. Cuando llega una
solicitud de descarga con un token, el servidor de versiones decodifica la cadena en
base64url, separa los primeros 64 bytes como la firma Ed25519, verifica la firma sobre
los bytes restantes utilizando la clave pública almacenada, analiza la carga útil y
comprueba que el producto coincida con el producto solicitado y que la fecha de
vencimiento no haya pasado. Un producto que no coincide devuelve 403; una firma no
válida devuelve 401; un token vencido devuelve 403 con una cadena de motivo que
indica que el canal ha vencido. Dado que el servidor de versiones no tiene clave de
firma, una vulneración del servidor de versiones no permite a un atacante acuñar nuevos
tokens.

El servidor de versiones expone la clave pública de verificación en un punto de acceso
conocido. Las herramientas externas — como el script de instalación propio del cliente —
pueden descargar la clave pública una vez y posteriormente verificar los tokens sin
conexión sin contactar al servidor de versiones en tiempo de ejecución.

## Idempotencia del recibo y el flujo de reclamación

El punto de acceso de emisión de licencias de la tienda virtual es idempotente: consultar
el mismo hash de transacción varias veces siempre devuelve el mismo token. Si ya existe
un recibo en disco, el token se emite inmediatamente. Si no, la tienda virtual delega una
consulta en cadena al subcomando de verificación del observador de pagos y, al confirmar,
escribe el recibo antes de emitir el token. La primera llamada para una nueva transacción
puede implicar un ciclo de ida y vuelta en cadena; cada llamada posterior se sirve desde
el disco sin latencia adicional más allá de la E/S local.

Un punto de acceso de reclamación separado registra una asociación fuera de cadena entre
un hash SHA-256 de binario y la dirección de billetera del comprador. Esto constituye la
base para una futura atestación de propiedad en cadena. La capacidad de acuñación en
cadena está prevista para una versión futura del sistema; el registro de reclamación se
escribe ahora para que los datos estén disponibles cuando se añada esa capacidad.

## Véase también

- [[software-distribution-substrate]] — descripción general del sistema de distribución de tres componentes del que esta arquitectura es el componente de pago
- [[private-git-paid-customer-endpoint]] — cómo el servidor de versiones gestiona la verificación de tokens y la entrega de binarios en el punto de acceso de descarga
