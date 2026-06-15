---
schema: foundry-doc-v1
title: "Punto de acceso privado para descarga binaria de clientes con licencia"
slug: private-git-paid-customer-endpoint
category: services
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-06-13
editor: pointsav-engineering
paired_with: private-git-paid-customer-endpoint.md
short_description: "El servidor de versiones binarias de software.pointsav.com verifica tokens de licencia Ed25519 y transmite binarios compilados. Diseñado sin estado: no almacena registros de pago, datos de clientes ni claves de firma."
cites: []
---

El servidor de versiones binarias es el componente de `software.pointsav.com` que entrega
binarios compilados a los clientes con licencia. Es una puerta delgada y sin estado: no
almacena registros de pago, datos de clientes ni claves de firma. Su única responsabilidad
es verificar que el token de licencia presentado sea genuino y autorice el producto
solicitado, y luego transmitir el archivo binario. Un cliente que ha completado una compra
y posee un token válido puede descargar el binario correspondiente sin ninguna interacción
adicional con la infraestructura de pagos.

## Estructura de rutas

El servidor de versiones organiza sus puntos de acceso en cuatro categorías.

**Descubrimiento de productos y versiones.** Un índice de productos sin autenticación
lista todos los productos cuyas versiones están disponibles en el servidor, y un índice
de versiones lista todas las versiones disponibles para un producto determinado. Estos
puntos de acceso no requieren token de licencia y están diseñados para ser consumidos por
herramientas como gestores de paquetes, scripts de instalación y pipelines de CI.

**Descarga de binarios versionados.** El punto de acceso principal protegido sirve un
binario para un producto, versión y plataforma específicos. Las solicitudes a este punto
de acceso requieren un token de licencia válido. Un archivo de firma Ed25519 separada
para cada binario está disponible en una ruta correspondiente y siempre está sin
autenticación — las firmas separadas son públicas por diseño, lo que permite a cualquier
parte verificar la autenticidad de un binario sin tener una licencia.

**Redirección a la última versión.** Un punto de acceso de conveniencia resuelve la
versión más alta disponible para un producto y plataforma dados, y emite una redirección
a la ruta de descarga versionada. El token de licencia se reenvía a través de la
redirección. La redirección solo apunta a combinaciones de plataforma y versión para las
que realmente existe una versión; no redirigirá a una versión que carezca de un binario
para la plataforma solicitada.

**Manifiesto de versión.** Un punto de acceso de metadatos por versión sirve un manifiesto
estructurado que describe el contenido de una versión. No se requiere autenticación. Este
punto de acceso es útil para herramientas que necesitan inspeccionar el contenido de una
versión antes de iniciar una descarga.

## Autenticación

El servidor de versiones acepta un token de licencia en dos formas.

**Encabezado HTTP de autorización.** El token se pasa como credencial Bearer en el
encabezado `Authorization`. Esta es la forma estándar para clientes programáticos,
instaladores automatizados y herramientas de línea de comandos que pueden establecer
encabezados de solicitud arbitrarios.

**Parámetro de consulta.** El token se pasa como parámetro `token` añadido a la URL.
Esta forma existe específicamente para habilitar enlaces de descarga con un solo clic
iniciados desde el navegador: una tienda virtual puede generar una URL que incluya el
token, lo que permite al cliente descargar un binario directamente desde su navegador
sin configurar ningún encabezado HTTP. Ambas formas son igualmente seguras — ninguna
expone el token a partes adicionales más allá del cliente y el servidor.

## Lógica de verificación

El servidor decodifica la cadena del token en base64url, separa los primeros 64 bytes
como una firma Ed25519 y verifica la firma sobre los bytes restantes utilizando la clave
pública de verificación almacenada en el servidor. Luego analiza la carga útil y
comprueba dos cosas: que el campo de producto en la carga útil coincida con el producto
solicitado, y que la fecha de vencimiento no haya pasado. Un token para un producto
diferente devuelve 403. Un token cuya firma no se verifica devuelve 401. Un token vencido
devuelve 403 con un motivo que indica que el canal ha vencido. El formato del token se
describe en detalle en [[crypto-license-sales-architecture]].

## Cadenas de plataforma

Las cadenas de plataforma siguen la convención de triple objetivo de Rust. Entre los
ejemplos se incluyen `x86_64-unknown-linux-gnu` para Linux de 64 bits en x86,
`aarch64-unknown-linux-gnu` para Linux ARM de 64 bits y `x86_64-apple-darwin` para macOS
en Intel. El servidor mapea el nombre del producto, la cadena de versión y el triple de
plataforma directamente a una ruta de archivo en el directorio de versiones. Si no se ha
compilado ningún binario para la combinación solicitada, el servidor devuelve 404 con una
nota indicando que el pipeline de compilación aún no ha producido esa versión. El punto
de acceso de redirección a la última versión solo redirige a cadenas de plataforma para
las que realmente existe un archivo de versión.

## Gestión de claves y comportamiento de seguridad ante fallos

El servidor carga la clave pública de verificación Ed25519 al iniciar desde una fuente
de configuración. Si no se configura ninguna clave, el servidor no acepta silenciosamente
todos los tokens: los puntos de acceso de descarga y verificación devuelven una respuesta
de servicio no disponible. Este comportamiento de seguridad ante fallos significa que una
instancia mal configurada o recién desplegada que aún no ha recibido una clave de
verificación rechazará todas las solicitudes en lugar de conceder accidentalmente acceso.
Una instancia correctamente configurada con una clave válida aceptará los tokens firmados
por la clave privada correspondiente y rechazará todos los demás.

## Lo que el servidor no hace

El servidor de versiones no registra las descargas individuales ni mantiene ningún
historial de descargas. No implementa la revocación de tokens: una vez emitido un token,
sigue siendo válido hasta su fecha de vencimiento, y no existe ninguna lista de revocación.
Los clientes que necesiten evitar que se use un token comprometido deben esperar a que
el token venza; la rotación de claves por parte de la tienda virtual invalida todos los
tokens emitidos anteriormente, con el coste de requerir que los clientes existentes
vuelvan a emitir sus tokens.

El servidor no sirve código fuente y no actúa como servidor Git. Un punto de acceso
provisional en la ruta del protocolo Git devuelve una redirección al repositorio público
de GitHub en lugar de enviar operaciones Git. Esta ruta está reservada para una versión
futura que pueda ofrecer acceso Git autenticado a repositorios privados.

## Véase también

- [[crypto-license-sales-architecture]] — cómo se procesan los pagos y se emiten los tokens antes de llegar a este servidor
- [[software-distribution-substrate]] — descripción general del sistema de tres componentes al que pertenece este servidor
- [[authenticate-binary-downloads]] — guía paso a paso: verificar versiones de binarios firmados con Ed25519 desde el punto de distribución privado
- [[issue-capability-token]] — guía paso a paso: generar un token de capacidad Ed25519 con alcance para un dispositivo o servicio
