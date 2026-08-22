---
schema: foundry-doc-v1
title: "Punto de acceso privado para descarga binaria de clientes con licencia"
slug: private-git-paid-customer-endpoint
aliases:
  - topic-private-git-paid-customer-endpoint
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
language: es
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: private-git-paid-customer-endpoint.md
short_description: "El servidor de versiones binarias de software.pointsav.com verifica tokens de licencia Ed25519 y transmite binarios compilados — sin estado, sin registros de pago ni claves, con algunos productos servidos abiertamente sin verificación de licencia."
cites: []
---

El servidor de versiones binarias es el componente de `software.pointsav.com` que entrega
binarios compilados a los clientes con licencia. Es una puerta delgada y sin estado: no
almacena registros de pago, datos de clientes ni claves de firma. Su única responsabilidad
es verificar que un token de licencia presentado sea genuino y autorice el producto
solicitado, y luego transmitir el archivo binario.

## Estructura de rutas

**Descubrimiento de productos y versiones.** Un índice de productos sin autenticar
enumera cada producto con versiones en el servidor; un índice por producto lista sus
versiones disponibles. Ambos están diseñados para herramientas — gestores de paquetes,
scripts de instalación, canalizaciones de CI.

**Descarga de binario versionado.** El endpoint principal con restricción sirve un binario
para un producto, versión y plataforma específicos, y requiere un token de licencia
válido — con una excepción: un producto cuyo manifiesto establece `requires_license: false`
se sirve a cualquiera, sin token. Un archivo de firma Ed25519 independiente para cada
binario está disponible en una ruta correspondiente y siempre está sin autenticar — las
firmas independientes son públicas por diseño, lo que permite a cualquier parte verificar
la autenticidad de un binario sin tener licencia.

**Redirección a la última versión.** Un endpoint de conveniencia resuelve la versión más
alta disponible para un producto y plataforma dados, y emite una redirección a la ruta de
descarga versionada, reenviando el token de licencia. Solo redirige a una plataforma para
la que realmente existe una versión.

**Manifiesto de versión y script de instalación.** Un endpoint de manifiesto por versión y
un endpoint `install.sh` por producto están ambos sin autenticar, permitiendo que las
herramientas inspeccionen una versión u obtengan un instalador sin token de licencia.

**Introspección de token.** Un endpoint autenticado verifica un token presentado contra
un producto y devuelve su validez, ID de producto, piso de versión, expiración del canal
y derechos — sin iniciar una descarga. Un endpoint separado sirve la clave pública de
verificación del propio servidor en hexadecimal, para que un cliente pueda verificar una
firma independiente por su cuenta. Un endpoint de sondeo de salud respalda el monitoreo
de disponibilidad.

## Autenticación

El servidor de versiones acepta un token de licencia como encabezado `Authorization:
Bearer` o como parámetro de consulta `token`. La forma de parámetro de consulta existe
específicamente para descargas de un solo clic iniciadas desde el navegador: una tienda
puede generar una URL que lleve el token para que un cliente descargue directamente desde
su navegador sin configurar ningún encabezado. Ambas formas son igual de seguras — ninguna
expone el token a ninguna parte más allá del cliente y el servidor.

## Lógica de verificación

Un token es `base64url(firma[64 bytes] || payload_json)` — una firma Ed25519 sobre los
bytes del payload, antepuesta al propio payload. El servidor divide el token, verifica la
firma contra su clave pública almacenada, y luego comprueba que el campo de producto del
payload coincida con el producto solicitado y que el canal no haya expirado. Una firma
incorrecta o malformada devuelve 401; una firma válida para el producto equivocado, o un
canal expirado, devuelve 403.

## Cadenas de plataforma

Las cadenas de plataforma siguen la convención de tripletas de destino de Rust —
`x86_64-unknown-linux-gnu`, `aarch64-unknown-linux-gnu`, `x86_64-apple-darwin`, entre
otras. El servidor mapea producto, versión y plataforma directamente a una ruta de archivo
en el directorio de versiones; una combinación sin binario construido devuelve 404. La
redirección a la última versión solo apunta a cadenas de plataforma para las que
realmente existe un archivo de versión.

## Gestión de claves y comportamiento a prueba de fallos

El servidor carga su clave pública de verificación Ed25519 al inicio desde la
configuración. Si no hay una clave configurada, no acepta silenciosamente todos los
tokens — los endpoints de descarga e introspección devuelven 503. Una instancia
correctamente configurada solo acepta tokens firmados por la clave privada
correspondiente.

## Lo que el servidor no hace

La ruta del protocolo Git es un stub: devuelve un 503 con un enlace al repositorio
público de GitHub, no un proxy activo ni una redirección HTTP — el acceso Git smart-HTTP
aún no está habilitado.

## Véase también

- [[crypto-license-sales-architecture]] — cómo se procesan los pagos y se emiten los tokens antes de llegar a este servidor
- [[software-distribution-substrate]] — visión general del sistema de tres componentes al que pertenece este servidor
- [[authenticate-binary-downloads]] — guía paso a paso: verificar versiones binarias firmadas con Ed25519 desde el endpoint de distribución privado
- [[issue-capability-token]] — guía paso a paso: generar un token de capacidad Ed25519 con alcance limitado para un dispositivo o servicio
