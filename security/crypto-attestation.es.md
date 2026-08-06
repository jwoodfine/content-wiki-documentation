---
schema: foundry-doc-v1
title: "Atestación criptográfica de la carga publicada"
slug: crypto-attestation
category: security
index_group: cryptographic-verification
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: forward-looking
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
short_description: "La atestación criptográfica permite a un lector recalcular el hash del contenido publicado y compararlo con un valor publicado. Existen prototipos cosméticos y sin conectar en unas pocas plantillas de publicación; el wiki de conocimiento no ofrece esta función."
paired_with: crypto-attestation.md
---

La **atestación criptográfica de la carga publicada** consiste en publicar un resumen criptográfico
de un documento junto al documento mismo, de modo que cualquier lector pueda recalcular el resumen
a partir de lo que realmente recibió y detectar una discrepancia sin confiar en el servidor que se
lo envió. La garantía es estrecha y conviene enunciarla con precisión: un resumen coincidente
demuestra que los bytes representados en el navegador del lector se corresponden con un valor al
que el editor se comprometió. Por sí solo no demuestra *cuándo* se adquirió ese compromiso, ni
quién lo adquirió, salvo que el resumen se firme por separado o se ancle en un registro con marca
de tiempo.

La técnica resulta atractiva para material corporativo y técnico publicado porque el lector puede
inspeccionarla sin herramientas especiales. Un navegador puede calcular un resumen SHA-256 de un
bloque de texto mediante la Web Crypto API en unas pocas líneas de script, y el lector puede
comparar el resultado con un valor impreso en la página o custodiado en otro lugar.

## Lo que existe hoy

Ninguna superficie publicada de PointSav ofrece atestación verificable por el lector. Lo que existe
es, en cambio, un patrón pequeño, cosmético y sin conectar que reaparece en un puñado de archivos
sin llegar nunca a ser funcionalmente decisivo.

Cuatro archivos del árbol de fuentes canónico contienen un cálculo SHA-256 en el cliente con la
misma forma: `service-content/templates/pointsav-monolith.html` y su hermano
`woodfine-brutalist.html`, más dos maquetas propuestas de sitio público bajo `proposed/pointsav.com/`
y `proposed/woodfinegroup.com/`. Cada uno representa un campo "SHA-256 Checksum" en una barra
lateral de metadatos, calcula un resumen del texto de la página tal como está representada en ese
momento mediante `crypto.subtle.digest('SHA-256', ...)` y escribe el resultado en ese campo — una
visualización en vivo de "aquí tienes un hash de lo que estás mirando", no un valor que el editor
fijara en tiempo de compilación. Cada uno va acompañado de una llamada de telemetría
`navigator.sendBeacon` disparada al descargar la página, ajena al hash en sí. Una búsqueda directa
en el árbol canónico no encontró código Rust, configuración ni cableado de compilación que haga
referencia por nombre a ninguno de los cuatro archivos — ninguno de ellos es servido hoy por nada.
Es el mismo código ya señalado en otro punto de este wiki ([[zero-execution-routing]]) por
contradecir una afirmación distinta de "cero JavaScript en el cliente"; aquí lo pertinente es más
estrecho: se trata de una visualización de integridad de página que un lector podría confundir con
una atestación, no de un mecanismo de rastro de auditoría ni de autoría, y nunca ha estado conectado
para servir ninguna página en vivo.

Existe una quinta implementación, no relacionada, en la aplicación de hoja de cálculo de trabajo,
que calcula un resumen SHA-256 de su propio estado documental canonicalizado y lo almacena en un
campo de auditoría de integridad de guardado — un propósito distinto (detectar corrupción local
accidental) del que daría un lector de una página publicada.

## Lo que el wiki de conocimiento ofrece realmente

El motor del wiki de conocimiento, `app-mediakit-knowledge`, no expone ninguna prestación de
atestación al lector. Esto se comprobó leyendo íntegramente su script de cliente y su código de
maquetación, y buscando en todo ese componente términos de hashing, firma, punto de control y
verificación.

Su script de cliente implementa un conmutador de tema, un cajón de navegación móvil, botones para
copiar bloques de código, ajuste de tablas y dos esbozos etiquetados explícitamente para una fase
futura. No hay cálculo de resumen de ninguna clase. Su barra lateral representa un enlace a la
página principal, una lista de categorías, una sección condicional de guías y un índice construido
a partir de los propios encabezados del artículo — sin hash, sin enlace de firma y sin control de
verificación.

En ese componente sí aparecen dos cosas con forma de "hash", y ninguna es una función de
atestación. Una es un `ETag` HTTP derivado del resumen de un activo estático, utilizado para la
validación de caché de hojas de estilo y tipografías. La otra es una línea de procedencia en el pie
que afirma que cada revisión está direccionada por su contenido mediante su hash de commit, lo que
remite al identificador de commit de Git del artículo.

Esa línea de procedencia apunta al mecanismo del que el wiki realmente depende. El montaje de
contenido es, en sí mismo, un repositorio Git, y el módulo de historial del motor recorre el
registro del repositorio para producir una lista de revisiones por artículo — identificador de
commit, autor, fecha ISO y mensaje. El lector dispone, por tanto, de un *historial de revisiones*
en el sentido ordinario de Git, en el que la manipulación deja rastro: un registro significativo,
pero no un resumen publicado que pueda recalcular de forma independiente contra la página que está
leyendo.

## La relación con el registro de solo anexado

La plataforma sí opera un mecanismo de transparencia real y verificable de forma independiente,
descrito en [[cryptographic-ledgers]]: un registro de solo anexado encadenado por hashes con puntos
de control firmados con Ed25519, cuyo resumen de punto de control se envía mensualmente al registro
público de transparencia Sigstore Rekor. Ese mecanismo entrega exactamente lo que el hashing
ingenuo en el cliente no puede: evidencia de un tercero de que un estado dado existía en un momento
dado.

La salvedad importante es que **el contenido de los artículos del wiki no fluye hacia ese
registro**. El motor de conocimiento no contiene ningún cliente del servicio de archivos ni realiza
ninguna llamada de anexado; quienes escriben en el registro son la consola de ingesta, el vigilante
de flota de la administración de red, el servicio de correo, el servicio de personas y el propio
emisor de anclaje. Presentar la propiedad de marcado temporal del registro como si cubriera los
artículos publicados del wiki sería inexacto.

## Verificar una atestación a mano

Detallar cómo sería una comprobación independiente, una vez que tal función exista, aclara por qué
el diseño es creíble en principio aunque hoy nada lo implemente. El lector seleccionaría y copiaría
el texto visible de un bloque de idioma exactamente tal como se representa, calcularía un resumen
SHA-256 de ese texto en su propia máquina con cualquier herramienta estándar y compararía el
resultado con el hash mostrado en la página — una comparación exacta de cadenas, en la que
cualquier diferencia en cualquier dígito hexadecimal significa que el contenido difiere del que
produjo el valor mostrado.

Dos propiedades de SHA-256 sostendrían la garantía. La resistencia a preimagen implica que un
atacante no puede construir un texto alternativo que coincida con un hash dado, de modo que un
contenido manipulado no puede conservar el hash original y seguir siendo consistente. El efecto
avalancha implica que incluso una alteración de un solo carácter cambia el resumen por completo, de
modo que la manipulación nunca sería *casi* indetectable: sería llamativa o inexistente. Una
versión funcional de esta característica tendría que ser estricta sobre qué se somete a hash — qué
bloque, qué normalización de espacios en blanco, qué codificación —, porque un verificador que no
puede reproducir exactamente los bytes de entrada no puede reproducir el hash. Ninguno de los
cuatro archivos prototipo anteriores resuelve esto: cada uno recalcula a partir de lo que la página
representa en ese momento, lo que significa que un intermediario que altere el texto antes de que
llegue al navegador altera también el hash que el script muestra, anulando justamente la garantía
que esta técnica pretende ofrecer.

## Lo que exigiría una implementación completa

Una atestación verificable por el lector para artículos publicados necesitaría, como mínimo: una
regla de canonicalización que fije exactamente qué bytes se someten a hash y cómo se normalizan los
espacios en blanco y el marcado, para que editor y lector calculen sobre la misma entrada; una ruta
de publicación que registre el resumen en tiempo de compilación en lugar de recalcularlo en el
navegador a partir de lo que se haya servido; una firma sobre ese resumen con una clave que el
lector pueda obtener de forma independiente; y, para el marcado temporal, el envío del resumen
firmado a la ruta de anclaje ya descrita. Ninguno de estos cuatro pasos está implementado hoy para
el contenido del wiki, ni para ninguno de los cuatro archivos prototipo.

## Lo que esto no es

**Esta no es una función que el wiki de conocimiento ofrezca actualmente.** Ninguna página de
artículo calcula, muestra ni verifica un resumen de contenido. Un lector que visite hoy el wiki no
dispone de ningún control de atestación.

**Un hash de página calculado por la propia página no es, por sí solo, protección frente a
manipulación.** En los archivos prototipo, el resumen lo calcula un script servido desde la misma
página que el contenido. Un atacante capaz de alterar el contenido suele ser capaz de alterar el
script. Tal visualización es, como mucho, una ayuda cosmética de integridad frente a la corrupción
accidental, no una defensa frente a una ruta de publicación comprometida, salvo que el valor
esperado se obtenga de una fuente independiente.

**La atestación no es autenticación de autoría.** Un resumen sin firmar no dice nada sobre quién
publicó el contenido. Nada en los prototipos descritos arriba firma el resumen con una clave del
editor.

**La atestación no es una marca de tiempo.** Solo la ruta de anclaje independiente establece que un
estado existía en un momento determinado, y esa ruta no cubre actualmente los artículos del wiki ni
ninguno de los archivos prototipo.

**El historial de revisiones de Git no es la misma garantía.** Registra lo que el repositorio
contiene y quién lo confirmó, lo cual es una procedencia valiosa, pero se verifica confiando en el
repositorio y no recalculando un resumen de la página entregada.

## Véase también

- [[cryptographic-ledgers]] — el registro de solo anexado encadenado por hashes y sus puntos de control firmados
- [[doctrine-invention-7-rekor-anchoring]] — el envío mensual de puntos de control a un registro público de transparencia
- [[verify-worm-ledger]] — el procedimiento del operador para comprobar directamente la integridad del registro
- [[merkle-proofs-as-substrate-primitive]] — la estructura de prueba que adoptaría una mejora futura
- [[app-mediakit-knowledge]] — el motor del wiki cuyas capacidades actuales se describen arriba
- [[zero-execution-routing]] — el artículo de patrón donde este mismo código prototipo se señala por separado por una afirmación excesiva no relacionada
