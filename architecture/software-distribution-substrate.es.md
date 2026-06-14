---
schema: foundry-doc-v1
title: "Sustrato de distribución de software de PointSav"
slug: software-distribution-substrate
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
paired_with: software-distribution-substrate.md
short_description: "Un sistema de tres componentes — servidor de versiones, tienda virtual y observador de pagos — que entrega binarios compilados contra pagos USDC en cadena, sin cuentas de cliente ni facturación por suscripción."
cites: []
---

El sustrato de distribución de software de PointSav es un sistema de tres componentes
que gestiona el alojamiento de versiones binarias, la tienda virtual con emisión de
licencias y la verificación de pagos en cadena. Los tres componentes — un servidor de
versiones, una tienda virtual de mercado y un observador de pagos — se ejecutan como
servicios separados accesibles en `software.pointsav.com`. Cada componente tiene una
responsabilidad única y delimitada, y juntos forman una ruta de distribución sin
custodia: no se requieren cuentas de cliente, y un cliente puede pasar del pago a la
descarga de binarios en una sola sesión.

## Los tres componentes

**Servidor de versiones.** El servidor de versiones entrega binarios compilados y
aplica la verificación de tokens de licencia Ed25519 antes de que se realice cualquier
descarga. También expone índices de productos y versiones que permiten a las herramientas
descubrir qué versiones están disponibles, y puede redirigir las solicitudes de la
última versión de un producto a la ruta versionada correspondiente. El servidor no tiene
estado: no almacena registros de pago ni datos de clientes. Su única responsabilidad es
verificar que un token sea genuino y autorice el producto solicitado, y luego transmitir
el archivo.

**Tienda virtual.** La tienda virtual presenta un catálogo de productos en los
navegadores, verifica los pagos entrantes de USDC en Polygon mediante la comparación
cruzada de transferencias confirmadas en cadena con un almacén local de recibos en
archivo plano, y emite tokens de licencia firmados con Ed25519 una vez confirmado el
pago. La tienda virtual es la infraestructura del proveedor — ejecuta la lógica de
negocio de la capa de distribución. Los productos de software que vende llevan claves
de licencia Ed25519 y listados en el mercado; son lo que la tienda distribuye, no lo
que la tienda es.

**Observador de pagos.** El observador de pagos monitorea la red Polygon PoS en busca
de transferencias entrantes de USDC a la dirección de la billetera del proveedor, escribe
un recibo estructurado por cada pago confirmado y proporciona utilidades de gestión de
claves: generación de pares de claves Ed25519, generación de semillas mnemónicas BIP-39
y derivación de direcciones deterministas jerárquicas (HD) por pedido. Los recibos son
el registro de autoridad de la compra; la tienda virtual no emitirá un token de licencia
sin uno.

## Formato del token de licencia

Un token de licencia es una firma Ed25519 sobre una carga útil JSON, codificada en
base64url. Los 64 bytes de la firma se anteponen a los bytes de la carga útil antes de
la codificación, produciendo una cadena opaca única. La carga útil registra el
identificador de producto, una fecha de vencimiento y una lista de autorizaciones que
codifican el nivel de licencia. El servidor de versiones solo tiene la mitad pública
del par de claves de firma. La verificación no requiere ninguna llamada de red ni estado
compartido — el servidor decodifica el token, verifica la firma y comprueba el producto
y el vencimiento íntegramente a partir del propio token.

## Flujo de pago y licencia

Una compra se realiza en cinco etapas:

1. El cliente visita la tienda virtual, selecciona un nivel de licencia y envía USDC
   a la billetera del proveedor en Polygon PoS — ya sea a la dirección estática del
   proveedor o a una dirección derivada por pedido para seguimiento de pedidos.
2. El observador de pagos detecta la transferencia confirmada en cadena y escribe un
   recibo que identifica el producto y el hash de transacción del comprador.
3. El cliente consulta el punto de acceso de licencias de la tienda virtual con el hash
   de transacción; la tienda virtual localiza el recibo y emite un token de descarga
   firmado.
4. El cliente presenta el token al servidor de versiones mediante un encabezado HTTP
   o un parámetro de consulta; el servidor de versiones verifica el token y transmite
   el binario.
5. En usos posteriores, el binario o el instalador puede verificar nuevamente su propio
   token contra el punto de acceso de clave pública del servidor de versiones sin
   contactar a la tienda virtual en tiempo de ejecución.

## Niveles de licencia

Están disponibles dos niveles. El nivel de código abierto tiene licencia Apache 2.0.
El nivel comercial tiene licencia bajo la Functional Source Licence (FSL). Ambos
niveles son compras únicas; no existen suscripciones. El nivel está codificado en el
campo de autorizaciones del token y en el recibo de pago. Los precios actuales se
publican en `software.pointsav.com`.

## Lo que este sistema no es

El sustrato gestiona pagos, emisión de tokens y entrega de binarios. No gestiona
suscripciones — todas las compras son transacciones únicas y perpetuas. No crea cuentas
de cliente. No restringe el acceso al código fuente: el repositorio de GitHub es
públicamente accesible por separado bajo la licencia Apache 2.0. Los clientes que
adquieren el nivel comercial FSL reciben una clave de licencia que desbloquea la
distribución binaria; los términos del código fuente se rigen por la licencia
respectiva, no por este sistema.

## Véase también

- [[crypto-license-sales-architecture]] — arquitectura detallada del componente de pago y emisión de tokens de este sistema
- [[private-git-paid-customer-endpoint]] — arquitectura detallada del servidor de versiones y su punto de acceso de descarga
