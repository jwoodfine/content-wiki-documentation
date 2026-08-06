---
schema: foundry-doc-v1
title: "Registros criptográficos"
slug: cryptographic-ledgers
category: security
index_group: cryptographic-verification
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-06
editor: pointsav-engineering
short_description: "Un registro de solo anexado en el que el hash de cada entrada cubre a la anterior, cerrado con puntos de control firmados con Ed25519 y anclado mensualmente en un registro público de transparencia. Implementado como cadena lineal, con un archivo plano por inquilino."
paired_with: cryptographic-ledgers.md
---

Un **registro criptográfico** es un registro de solo anexado en el que el hash de cada entrada
incorpora el hash de la entrada anterior, de modo que alterar o eliminar cualquier entrada pasada
invalida todos los hashes que la siguen. La cadena no impide la manipulación — nada almacenado en
un soporte ordinario puede impedirla —, pero la hace detectable por cualquiera que posea un hash
posterior, sin exigir confianza en el sistema que produjo el registro. En una base de datos
tradicional, un administrador con suficiente privilegio puede editar en silencio un registro
almacenado, y nada en los propios datos delata el cambio. Un registro criptográfico elimina esa
ruta mutable privilegiada.

Otros dos mecanismos convierten una propiedad de manipulación detectable en una propiedad
verificable desde fuera. Un punto de control firmado compromete al operador del registro con un
estado raíz concreto para un tamaño concreto, de modo que un lector puede confirmar que está
mirando el registro que el operador publicó y no una versión paralela. Anclar ese punto de control
en un registro público independiente establece que el estado existía antes de un momento que el
operador no controla. La implementación de esta plataforma está en producción en [[service-fs]], el
servicio de registro WORM (escribir una vez, leer muchas) por inquilino, y la descripción que sigue
refleja el código tal como se ejecuta hoy.

## La implementación

### Forma de almacenamiento

Un archivo JSON delimitado por saltos de línea por inquilino, en `<root>/<moduleId>/log.jsonl`.
Cada línea es un registro con cuatro campos: un `cursor` monótono, un `payload_id`, el `payload` en
sí como JSON arbitrario y `this_hash`.

La cadena es una **cadena de hashes SHA-256 lineal, no un árbol de Merkle**. El hash de cada
entrada se calcula sobre el hash anterior, el cursor en forma big-endian y el identificador y los
bytes de la carga precedidos de su longitud. El predecesor de la primera entrada es un hash de
origen fijo derivado de una cadena constante etiquetada con versión, de modo que la cadena tiene un
inicio bien definido y no una semilla arbitraria. Como una prueba de inclusión sobre una cadena
lineal es un recorrido de la cadena y no una ruta logarítmica, el tamaño de la prueba crece con la
distancia al punto de control; una mejora a árbol de Merkle que reduciría las pruebas dejando la
interfaz intacta figura en los comentarios del propio código como refinamiento posterior, no como
una estructura que exista hoy.

La disciplina de escritura es deliberada y conviene enunciarla, porque es de donde procede en la
práctica la inmutabilidad. Un anexado escribe el registro completo en un archivo temporal, lo
sincroniza a disco, lo renombra atómicamente a su sitio y deja el resultado en solo lectura. Al
reabrirlo, el hash de cada registro se recalcula y se contrasta con lo almacenado; una discrepancia
se rechaza como condición de manipulación en lugar de aceptarse en silencio. El indicador de
inmutabilidad más fuerte, a nivel de sistema de archivos, requiere un privilegio que el servicio no
posee y queda diferido a la configuración de la unidad de servicio. El coste de este diseño está
reconocido en el propio código: reescribir todo el registro en cada anexado es lineal respecto al
tamaño del registro — una disposición en mosaicos por segmentos agrupados (segmentos sellados de
256 entradas, al estilo de la infraestructura de transparencia de certificados) es la mejora de
rendimiento planificada, no una estructura que exista hoy en disco. El esquema de registro y la
interfaz del servicio están diseñados para sobrevivir intactos a esa mejora.

### Puntos de control

Un punto de control lleva la cadena de origen del registro, su número actual de entradas, un hash
raíz, el nombre del algoritmo, una marca de tiempo y, opcionalmente, una firma. Cuando hay una
clave de firma configurada — suministrada como una semilla Ed25519 en bruto de 32 bytes cuya ruta
se indica mediante una variable de entorno —, el cuerpo del punto de control se firma en la forma
de nota firmada C2SP: origen, tamaño y hash raíz codificado en base64, cada uno en su propia línea.
La verificación de firma se expone como una función independiente que toma un punto de control y
una clave pública, de modo que un tercero puede verificar sin ejecutar el servicio. Omitir la clave
hace que el registro funcione sin firma: encadenado, pero sin un compromiso del operador que un
verificador pueda comprobar.

### Pruebas

Ambos tipos de prueba están implementados, no esbozados. Una prueba de inclusión toma el cursor de
una entrada y un punto de control, y devuelve el segmento de hashes encadenados que enlaza esa
entrada con la punta del punto de control. Una prueba de consistencia toma dos puntos de control y
devuelve el segmento que demuestra que el posterior extiende al anterior por solo anexado. Ambas se
ejercitan con pruebas que reinician el servicio y confirman que la cadena continúa correctamente a
través del reinicio.

El flujo de verificación para un auditor que examina un registro histórico es mecánico: recalcular
el hash de cadena del registro a partir de sus campos almacenados y confirmar que coincide;
verificar la inclusión del registro en la cadena contra un punto de control; verificar la firma del
punto de control contra la clave pública del inquilino; y, cuando se requiera garantía externa,
verificar la consistencia del punto de control frente al anclado. Cada paso emplea algoritmos
públicos y la clave pública del inquilino — nada en el flujo requiere la cooperación de PointSav,
la buena voluntad del operador ni acceso a ningún sistema más allá de los datos del registro y el
registro público.

## Anclaje

La detectabilidad dentro de un registro no establece *cuándo* existió un estado. Eso es lo que
aporta el paso de anclaje.

Un emisor dedicado obtiene el punto de control actual del servicio de archivos a través de su
interfaz HTTP local, lo serializa, calcula un resumen SHA-256 de esa serialización y envía el
resumen al registro público de transparencia Sigstore Rekor como una petición de registro con hash
en versión 2 (`hashedRekordRequestV002`), acompañada de una firma Ed25519 y la clave pública
correspondiente. La clave se genera de nuevo en cada ejecución — lo que se busca es la marca de
tiempo y la prueba de inclusión de Rekor, no la continuidad de la identidad de la clave. La entrada
del registro de transparencia devuelta se anexa después al propio registro bajo un identificador
con marca de tiempo, de modo que el evento de anclaje pasa a formar parte del registro que ancla.

El punto de envío es un fragmento anual concreto de Rekor, reemplazable mediante variable de
entorno porque Sigstore rota los fragmentos cada año y advierte contra fijar uno en el código. El
emisor no realiza reintentos: cada fallo de etapa termina con un código distinto, y la recuperación
es la siguiente ejecución del temporizador. La cadencia es mensual — el primer día del mes a las
02:30 UTC, con recuperación activada si la máquina estuvo apagada y un retardo aleatorio de hasta
quince minutos.

El comentario de la propia unidad de servicio systemd desplegada describe la carga de anclaje como
envoltorio de una entrada "Sigstore hashedrekord v0.0.1". El código real del emisor implementa la
forma de petición v0.0.2 de principio a fin: el envoltorio de nivel superior `kind`/`apiVersion` de
la v0.0.1 se elimina explícitamente, el resumen se envía como bytes en bruto y no en la forma
base64-de-PEM de la v0.0.1, y las pruebas comprueban que los campos del envoltorio antiguo están
ausentes. El comentario está desactualizado respecto del código que se publica; el código es la
autoridad, y el mecanismo de anclaje funciona como v0.0.2 con independencia de lo que diga el
archivo de unidad.

## Quién escribe en él

El registro es una instalación compartida a la que se accede por una interfaz HTTP local en el
puerto 9100, y cada escritor identifica a su inquilino mediante una cabecera obligatoria
`X-Foundry-Module-ID` que el servicio contrasta con su propio identificador de módulo configurado
antes de aceptar una escritura. Los escritores confirmados son la consola de ingesta, el servicio
de correo, el servicio de personas, el vigilante de flota de la administración de red y el emisor
de anclaje, que escribe de vuelta su propio resultado.

En esa lista existe un defecto: el anexado de eventos de topología del vigilante de flota
(`write_worm_event`, en `app-network-admin`) publica en el punto de anexado del registro sin
establecer la cabecera de identificador de módulo que el servicio exige, y ninguna ruta
compensatoria la suministra en otro punto de esa llamada. Tal como está escrito, la propia
comprobación de cabecera del servicio rechazaría esa escritura. Se recoge aquí como un hallazgo
verificado, no se describe como funcional.

## Para qué se usa el registro

La disciplina se aplica allí donde la plataforma consigna hechos que más adelante puede necesitar
demostrar:

- **Registros corporativos y operativos** — las entradas se anexan al registro WORM antes de que
  ningún procesamiento posterior las toque, de modo que el registro conserva el primer estado
  duradero.
- **Observaciones de identidad** — el [[identity-ledger-schema-design|registro de identidad]]
  escribe sus registros de persona, ancla y afirmación por la misma ruta de anexado.
- **Postura de auditoría** — el invariante de solo anexado, la verificación determinista y el
  anclaje externo dan a los revisores de cumplimiento un registro cuya integridad no depende de
  confiar en los controles de acceso del operador. La arquitectura está estructuralmente alineada
  con los regímenes de conservación documental que exigen almacenamiento WORM, si bien la
  alineación con cualquier normativa concreta es materia de evaluación formal y no una propiedad
  automática del diseño.

## Lo que esto no es

**El formato en disco no es C2SP tlog-tiles.** Es un único archivo plano JSON delimitado por saltos
de línea por inquilino. La disposición multiarchivo, codificada en base64 y de 256 entradas por
mosaico aparece en los documentos de arquitectura e investigación del componente como diseño
objetivo, y en el nombre del tipo que la implementa; hoy ningún código crea ni lee un archivo de
mosaico. De C2SP solo está realmente implementada la forma de punto de control en nota firmada.

**La estructura no es un árbol de Merkle.** Es una cadena de hashes lineal. Las pruebas de
inclusión son segmentos de cadena, no rutas logarítmicas, y la mejora a árbol es un paso posterior
declarado sin calendario comprometido.

**Solo anexado no es a prueba de borrado.** La garantía es la detección. Quien tenga acceso de
escritura al almacenamiento puede sustituir el archivo; la respuesta del registro es que al
reabrirlo falla la verificación y que cualquier punto de control anclado previamente deja de
coincidir. Nada impide físicamente la sustitución.

**El anclaje no es continuo.** Entre ejecuciones mensuales, un estado cuenta con la integridad
interna del registro y la firma del operador, pero sin marca de tiempo independiente. La ventana de
exposición es de hasta un mes.

**Un registro sin firmar es una afirmación más débil.** La firma es opcional en el arranque. Sin
clave, las entradas quedan encadenadas pero ningún punto de control porta un compromiso del
operador, y la ruta de anclaje no tiene nada significativo que enviar.

**El registro no es una cadena de bloques.** No hay consenso distribuido, ni criptomoneda, ni
minería, ni red de pares — es un registro de solo anexado, de un único escritor y por inquilino,
cuyo anclaje externo de confianza es un registro público de transparencia, el mismo patrón que
emplea la transparencia de certificados. Tampoco es cifrado: el registro hace que los asientos
tengan manipulación detectable, no que sean secretos; la confidencialidad la manejan capas
separadas.

**El contenido de los artículos del wiki no fluye hacia este registro.** El motor de conocimiento
no tiene cliente del servicio de archivos ni realiza ninguna llamada de anexado. El historial de
revisiones de los artículos es historial ordinario de Git, una propiedad distinta y más débil que
la descrita aquí.

**La completitud no es tarea de esta capa.** El registro no impide que un operador *deje de
consignar* algo: demuestra que lo consignado no ha sido alterado, y que la historia registrada
nunca se reescribió después del anclaje, pero la decisión de qué entra en el registro se toma antes
de él.

## Véase también

- [[worm-ledger-architecture]] — el modelo de registro de escritura única que esto implementa
- [[worm-ledger-storage-architecture]] — la disposición de almacenamiento y su evolución prevista
- [[fs-anchor-emitter]] — el componente que realiza el envío mensual
- [[doctrine-invention-7-rekor-anchoring]] — el diseño de anclaje y su justificación
- [[merkle-proofs-as-substrate-primitive]] — la estructura de prueba que adoptaría la mejora planificada
- [[verify-worm-ledger]] — el procedimiento del operador para comprobar la integridad directamente
- [[identity-ledger-schema-design]] — otro escritor que usa la misma ruta de anexado
- [[crypto-attestation]]
