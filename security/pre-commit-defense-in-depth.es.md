---
schema: foundry-doc-v1
title: "Defensa en profundidad previa al commit"
slug: pre-commit-defense-in-depth
category: security
index_group: supply-chain-controls
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-22
editor: pointsav-engineering
short_description: "Cuatro hooks de git independientes se ejecutan antes de que un commit quede registrado: una compuerta de solo-helper, un bloqueo por ruta de datos, un escaneo de secretos y tamaño sobre el contenido preparado, y una comprobación de identidad del autor. Toda elusión queda registrada."
paired_with: pre-commit-defense-in-depth.md
---

**La defensa en profundidad previa al commit** es la práctica de apilar varias comprobaciones
independientes en el momento en que se crea un commit, cada una destinada a atrapar una clase distinta
de error, de modo que ningún fallo aislado permita que un secreto, un artefacto sobredimensionado o un
cambio mal atribuido entren en el historial. Es el punto más barato del ciclo de vida para intervenir:
un commit rechazado cuesta segundos, mientras que una credencial que llega a un repositorio publicado
debe tratarse como comprometida y rotarse con independencia de la rapidez con que se revierta el
commit.

Los controles descritos aquí operan sobre el contenido *preparado* (*staged*) — lo que el commit está
a punto de registrar — y no sobre el directorio de trabajo. Esa distinción es lo que los hace
significativos: un escaneo de los archivos en disco puede burlarse preparando una versión distinta,
mientras que leer el blob preparado a través del propio almacén de objetos de Git muestra exactamente
lo que está a punto de escribirse.

## Las capas

Cuatro comprobaciones separadas se ejecutan en el momento del commit, en un orden deliberado: primero
las más baratas y amplias, al final la más costosa.

### Compuerta de commit solo a través del helper

La primera comprobación rechaza un `git commit` directo salvo que esté definida la variable de entorno
`FOUNDRY_COMMIT_HELPER`, que el helper de commit sancionado define para su propia invocación. No
necesita inspeccionar ningún archivo, solo comprobar el entorno, de modo que falla rápido y con una
instrucción que apunta al helper en vez de con un misterio. El efecto es que todo commit ordinario se
encauza por un único script, que es donde se aplican de forma consistente la alternancia de identidad,
los trailers y la firma — la compuerta de solo-helper es lo que hace fiables desde su origen las
garantías de atribución de la [[five-stage-supply-chain|cadena de suministro]].

La compuerta hace una excepción deliberada para los commits internos del propio Git: si
`GIT_REFLOG_ACTION` indica un merge, un rebase o un cherry-pick, el commit procede sin la variable del
helper. Sin esa salvedad, toda resolución de conflictos durante un rebase quedaría bloqueada. Existe
además una variable de elusión de emergencia para el operador que tenga un motivo legítimo; su uso
queda registrado en lugar de pasar en silencio.

### Bloqueo por ruta de datos

Una segunda comprobación inspecciona las *rutas* de los archivos preparados — no su contenido — contra
un catálogo de formas de ruta que se sabe que llevan registros de negocio e información personal:
directorios de motor concretos, un archivo de libro de personal con nombre propio, prefijos de colas
de transacciones, patrones documentales particulares y los directorios de trabajo de entrada y salida.
Una pequeña lista de permitidos cubre las excepciones legítimas. Esta capa existe porque la categoría
más costosa de commit accidental no es una credencial sino un registro de negocio real, y un archivo
así suele ser indistinguible del contenido ordinario del proyecto solo por su extensión. Se ejecuta
antes del escaneo de contenido para que un archivo de administración de negocio sea rechazado por su
ruta, de forma barata, en lugar de pasar primero por la comparación de patrones.

### Escaneo de patrones de secretos y de tamaño

La capa más grande lee un catálogo de patrones mantenido y escanea el
contenido preparado de cada archivo añadido, copiado, modificado o renombrado. El contenido se obtiene
mediante las órdenes de fontanería (*plumbing*) de Git y no desde el disco. Los archivos binarios se
omiten mediante una heurística que examina los bytes nulos y la proporción de caracteres imprimibles de
los primeros cuatro kilobytes de cada archivo — comprobación que se hace antes de la costosa
decodificación del contenido completo, después de que un commit real grande de archivos de
administración de negocio (varios PDF grandes y un zip) llegara a tardar un tiempo inaceptablemente
largo en escanearse porque ese orden estaba invertido.

Leyendo el catálogo vivo directamente, hoy contiene varias decenas de entradas de patrón: claves
privadas en varios formatos, credenciales de nube y de plataforma, tokens de API de varios
proveedores de modelos y de una plataforma de chat, asignaciones genéricas de contraseña y tokens
bearer, una ruta de identidad del espacio de trabajo escrita en duro, y varios patrones que
corresponden a formas de información personal — números de teléfono, direcciones de correo
electrónico, números de identidad nacional y direcciones postales. El catálogo ha crecido con el
tiempo, más recientemente para cubrir un formato de clave privada que un hallazgo real y en vivo
mostró que los patrones existentes no detectaban.

La severidad determina el desenlace. Las coincidencias críticas y altas bloquean el commit sin más.
Las severidades menores imprimen una advertencia y lo dejan proceder. Una lista de rutas permitidas
exime al propio archivo del catálogo, a `identity/*.pub` y `allowed_signers`, y a dos fixtures de
prueba con nombre propio cuyas pruebas unitarias contienen necesariamente cadenas con forma de secreto.

La misma capa impone un techo de tamaño configurado sobre el tamaño del blob preparado, comprobado
antes del escaneo de secretos para que un blob sobredimensionado se rechace solo por su tamaño en
lugar de escanearse primero. Una lista de
rutas permitidas aparte cubre los directorios donde los artefactos grandes son legítimamente esperables
— el registro de binarios, los repositorios de activos multimedia y las raíces web de despliegue.

### Comprobación de identidad del autor

Un hook `commit-msg` verifica de forma independiente el autor del commit contra las dos identidades de
colaborador permitidas y rechaza los trailers `Co-Authored-By` o `Signed-off-by` que nombren a
cualquier otro. Esto cierra una brecha distinta de las anteriores: no le importa qué contiene el
commit, solo que la atribución sea correcta y que ninguna herramienta automatizada se haya insertado en
el registro de autoría. Es lo que cerró la clase de incidentes de atribución errónea de 2026, en la que
una anulación local de configuración perdida podía cambiar en silencio el autor de una serie de
commits.

## Por qué importan el orden y la graduación de severidad

Los falsos positivos son el impuesto que paga todo escáner de secretos, y una compuerta que da falsas
alarmas se elude culturalmente mucho antes de que se eluda técnicamente. Los patrones cuyas
coincidencias son casi siempre secretos reales — una cabecera de clave privada, una clave de acceso de
proveedor — bloquean sin más. Los patrones que aparecen legítimamente en fixtures de prueba y en
documentación — asignaciones genéricas de contraseña, cadenas con aspecto de token — advierten y dejan
proceder el commit, manteniendo informado al operador sin acostumbrarlo a recurrir a la elusión. Las
listas de permitidos siguen la misma filosofía: el catálogo de patrones tiene que poder committearse
aunque esté hecho de las mismas cadenas que persigue, y las claves públicas tienen que poder
committearse aunque compartan territorio en el sistema de archivos con las privadas, así que ambas se
eximen por ruta en lugar de debilitar los patrones.

## Comportamiento ante fallos y elusión

Cada capa puede eludirse mediante su propia variable de entorno, y cada elusión se añade a un registro
`data/bypass-ledger.jsonl`. El registro es de mejor esfuerzo y nunca bloquea el commit en sí. Esta es
la postura buscada: un operador con un motivo legítimo puede proceder, y la decisión deja una traza
duradera en lugar de ser invisible.

Dos vías de degradación merecen enunciarse con claridad. Si falta el catálogo de patrones, el escaneo
de secretos y de tamaño se omite con una advertencia en lugar de fallar en cerrado. Si PyYAML — la
única dependencia externa del escaneo, siendo todo lo demás biblioteca estándar — no está instalado,
ocurre lo mismo. En ambos casos el commit procede sin escanear. La propia opción `--no-verify` de Git
omite todos los hooks por completo, y un clon sin los hooks instalados no impone ninguno de estos
controles; esa brecha se cierra operativamente, instalando el hook automáticamente en el momento de
aprovisionar un archivo de trabajo, y no por ninguna imposibilidad técnica.

## Relación con la compuerta de promoción

Estas comprobaciones son la primera de dos líneas. El script de promoción que lleva el trabajo a la
rama canónica vuelve a aplicar un filtro de ruta de datos comparable contra el árbol que está a punto
de empujarse, bloquea los borrados masivos y las reversiones silenciosas por encima de un umbral,
impone una lista de rutas de primer nivel permitidas para el repositorio canónico y exige confirmación
explícita para los repositorios que son públicamente visibles. Un secreto que sobreviva al momento del
commit todavía tiene que pasar ese segundo filtro antes de volverse observable desde fuera. La
estratificación es deliberada: las comprobaciones del momento del commit son rápidas y locales, las del
momento de la promoción son más lentas y consideran el árbol entero.

## Lo que esto no es

**Esto no es una garantía de que ningún secreto pueda committearse.** El escaneo es comparación de
expresiones regulares contra formas conocidas de credencial. Una credencial en un formato no
reconocido, partida en varias líneas o codificada, pasa. La cobertura de detección es un catálogo, no
una demostración — y el número de patrones aquí indicado es una medición, no una constante; el catálogo
ha crecido dos veces en el historial documentado de este artículo, y cualquier reenunciado de la cifra
debería recontarse contra el catálogo vivo en lugar de citarse desde esta página.

**Esto no es un control obligatorio.** Existen tres escapes distintos — las variables de entorno por
capa, el `--no-verify` de Git y un clon sin hooks instalados. El primero queda registrado; los otros
dos, no.

**Una dependencia ausente no hace fallar el commit.** La ausencia de PyYAML o la ausencia del archivo
de catálogo reduce en silencio el escaneo a nada y permite el commit. Es un diseño que falla en abierto
(*fail-open*), elegido para que un problema de herramientas no detenga el trabajo, y debe entenderse
como tal.

**Esto no escanea el historial.** Las comprobaciones se aplican al commit que se está creando. El
contenido que ya está en el historial no se ve afectado, y un secreto introducido antes de que
existieran estos controles sigue ahí.

**Los patrones de información personal no son un control de protección de datos.** Corresponden a
cuatro formas comunes, con severidad de advertencia en la mayoría de los casos. Reducen la exposición
accidental; no constituyen una revisión de si los datos personales se tratan de manera apropiada.

## Véase también

- [[five-stage-supply-chain]] — la ruta de promoción cuyas compuertas forman la segunda línea
- [[contributor-model]] — el modelo de identidad que impone la comprobación de autor
- [[api-key-boundary-discipline]] — las reglas más amplias de manejo del material de credenciales
- [[root-files-discipline]] — las convenciones de ruta de las que se nutre el bloqueo por ruta de datos
- [[machine-based-auth]]
- [[cryptographic-ledgers]]
- [[rotate-keys]] — el procedimiento que sigue a una exposición de credenciales
