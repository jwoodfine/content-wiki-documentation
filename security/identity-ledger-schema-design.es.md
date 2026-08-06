---
schema: foundry-doc-v1
title: "Diseño del esquema del libro de identidad"
slug: identity-ledger-schema-design
category: security
index_group: identity-and-permissions
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
short_description: "Tres tipos de registro — Person, Anchor y Claim — separan quién es conocido de cómo fue observado y de qué se afirmó sobre él. La identidad es un UUIDv5 de un correo en minúsculas, de modo que la misma entrada produce siempre el mismo identificador."
paired_with: identity-ledger-schema-design.md
---

**El esquema del libro de identidad** es el modelo de tres registros con el que esta plataforma
consigna quién le es conocido: un registro **Person** que establece que una identidad existe, un
registro **Anchor** que consigna dónde y cuándo se observó esa identidad, y un registro **Claim** que
afirma un atributo sobre ella con una confianza y una fuente declaradas. Separar los tres evita que
una identidad duradera se sobrescriba cada vez que un documento nuevo la menciona, y evita que un
atributo en disputa contamine la identidad que describe. Su decisión de diseño definitoria es que la
resolución de identidad no implica inferencia de ningún tipo: el identificador primario se deriva
aritméticamente de una dirección de correo, y las observaciones se extraen mediante una expresión
regular fija, nunca mediante un modelo.

La separación resuelve un problema concreto. Una sola fila mutable por persona obliga a que cada
observación nueva se fusione con el registro existente o se descarte, y la fusión es el punto donde
los sistemas de identidad acumulan error silencioso e inatribuible. Bajo este modelo, una
observación añade un Anchor, una afirmación añade un Claim, y ninguno de los dos altera el Person.
El desacuerdo entre fuentes se convierte en dos Claims con fuentes distintas, en lugar de en un
valor previo perdido. Cada afirmación estructural de este artículo se ha verificado directamente
contra el código canónico actual del servicio que lo implementa, [[service-people|service-people]].

## Los tres registros

**Person** lleva siete campos: el `id` derivado, un `name` para mostrar, el `primary_email`
normalizado a minúsculas, una lista de `email_aliases` (también normalizados al entrar), una
`organisation` opcional y las marcas de tiempo de creación y actualización. El identificador nunca lo
asigna quien llama: el único constructor lo deriva del correo, de modo que no puede construirse un
Person cuyo `id` no concuerde con su dirección.

**Anchor** lleva tres campos: el `target_uuid` al que apunta, la dirección observada como
`anchor_source` y una marca de tiempo. Un Anchor deliberadamente no afirma que la dirección
pertenezca a ninguna persona concreta: consigna únicamente que la dirección fue observada y qué
identificador le corresponde. Los Anchors son de solo adición; el sistema nunca modifica ni retira
ninguno.

**Claim** lleva siete campos: un `claim_id` (un UUIDv4 aleatorio, único por observación — a
diferencia del UUID de identidad, que es derivado), el `target_uuid` que anota, un nombre de
`attribute` y el `value` observado, un `confidence_score`, un `source_id` que registra de dónde
procede la observación y una marca de tiempo. En la vía de extracción sancionada, la puntuación de
confianza es `1.0` para todos los Claims sin excepción, porque el único método de extracción
conectado a ella es una expresión regular determinista que busca direcciones de correo; el campo
existe para posibles métodos de extracción futuros, que seguirían sujetos al límite de no inferencia
descrito más abajo.

La asimetría es el diseño. Person es el objeto estable; Anchor y Claim apuntan ambos *hacia* un
identificador de persona y ninguno puede modificarlo. La confianza vive en el Claim, que es donde
corresponde a una afirmación discutible, y nunca en el Person.

### Identidad determinista

El identificador de persona es un UUID de versión 5 derivado de la dirección de correo primaria en
minúsculas, bajo el espacio de nombres DNS estándar:

```
id = UUIDv5(NAMESPACE_DNS, lowercase(primary_email))
```

El constructor pasa a minúsculas antes de calcular el hash, y una prueba unitaria comprueba
explícitamente la insensibilidad a mayúsculas. La propiedad que esto compra es reproducibilidad sin
coordinación: la misma dirección de correo produce el mismo identificador en cualquier máquina, en
cualquier momento, sin contador compartido, sin servicio de asignación y sin emparejamiento
probabilístico — dos componentes que jamás se han comunicado llegarán de forma independiente al
mismo identificador para la misma persona, porque *la derivación es el registro*, no una consulta
contra él.

Las dos versiones de UUID del esquema reparten el trabajo de forma deliberada. La identidad usa la
versión 5 — un hash con espacio de nombres — precisamente *porque* es determinista: la identidad
debe ser reproducible solo a partir de la dirección. Los Claims usan la versión 4 — aleatoria —
precisamente porque no deben serlo: cada observación es un evento distinto, y dos observaciones del
mismo atributo desde la misma fuente son dos registros, no uno.

El coste es igual de definido y corresponde enunciarlo junto al beneficio. La identidad queda ligada
a una única dirección de correo. Una persona cuya dirección primaria cambia deriva un identificador
distinto hasta que un operador vincule ambas mediante la lista de alias; el esquema elige ese coste
visible y auditable frente a la inferencia silenciosa.

## La vía de escritura — y una segunda, no sancionada

El componente de personas escribe los registros en el servicio de archivos por HTTP: un POST a un
endpoint `/v1/append` que porta una cabecera `X-Foundry-Module-ID`, verificado leyendo directamente
el cliente y mediante una prueba de extremo a extremo que arranca un demonio real del servicio de
archivos y comprueba que un registro completa el trayecto de ida y vuelta con fidelidad. El
almacenamiento al otro lado es el registro de solo adición encadenado por hash descrito en
[[cryptographic-ledgers]], de modo que los registros de identidad heredan su evidencia de
manipulación y sus propiedades de punto de control y anclaje.

Esa es la vía sancionada, y decirlo con claridad importa porque no es la única vía del árbol. Una
herramienta de minería independiente, `tool-acs-miner`, define estructuras Anchor y Claim propias,
idénticas byte a byte, deriva identificadores con la misma llamada `Uuid::new_v5` (una prueba dentro
del propio `service-people` fija la concordancia entre ambas implementaciones) y los escribe con
llamadas ordinarias del sistema de archivos, directamente en archivos abiertos en modo de adición
bajo su propio directorio de trabajo — sin llamada HTTP, sin servicio de archivos, sin cadena de
hash. También asigna puntuaciones de confianza que varían según el tipo de atributo — `1.0` para
correo, `0.9` para teléfono, `0.6` para una coincidencia de nombre propio — a diferencia del `1.0`
constante de la vía sancionada. Los registros escritos así quedan enteramente fuera de las garantías
de integridad del libro mayor. No se encontró ningún script ni componente del árbol que invoque esta
herramienta, de modo que no pudo establecerse si se ejecuta en algún sitio; se documenta como
presente, no como activa.

La documentación del esquema añade una tercera descripción más: un archivo de esquema JSON y el
README de un componente describen un registro considerablemente más rico — un objeto `addresses`
estructurado que agrupa correos, teléfonos y endpoints, una lista `roles` y un bloque de metadatos —
bajo nombres de campo (`identity_id`, `addresses.emails`, `addresses.phones`) que ningún código del
árbol escribe. Ese documento describe un modelo previsto, no el implementado, que sigue siendo los
siete campos planos de `Person` de arriba.

## Tratamiento de conflictos

El almacén en proceso define un error tipado para la identidad en conflicto, que porta la dirección
de correo, el identificador ya ligado a ella y el recién derivado. Una adición que ligaría un correo
ya conocido a un identificador distinto se rechaza en lugar de fusionarse, y una prueba ejercita ese
rechazo.

El rechazo es real; una expresión que a veces se usa para describirlo merece matizarse. El conflicto
se manifiesta como un error devuelto a quien llama a la operación de adición — en la interfaz de la
herramienta, como una cadena de error en la llamada. No existe en el código ninguna bandeja de
entrada del operador, ninguna cola de revisión ni ninguna interfaz específica de resolución. La
garantía que sí se sostiene es *que no hay fusión silenciosa*: la escritura falla y quien llama sabe
por qué. La garantía que hoy no se sostiene es que se presente sistemáticamente el conflicto a una
persona para que lo dirima — eso sigue siendo propiedad de aquello que llame a la operación de
adición, no del esquema en sí.

## El límite de no inferencia y sus citas de gobernanza

El esquema está construido para que toda operación sea verificable sin estado de modelo. La
extracción de correos es una única expresión regular fija e insensible a mayúsculas. La derivación
del identificador es el algoritmo UUIDv5 — un hash con espacio de nombres fijo, determinista por
definición. La detección de conflictos es igualdad de UUID: sin coincidencia difusa, sin similitud
de embeddings, sin umbral ajustado. No hay pesos de modelo en el servicio de identidad ni llamadas a
ningún endpoint de inferencia en la vía de ingesta; el propio código del componente lo declara
directamente.

Aquí se citan con frecuencia juntas dos reglas de gobernanza distintas, y conviene separarlas, ya
que confundirlas tergiversa ambas. **SYS-ADR-07** prohíbe hacer pasar datos estructurados por un
modelo de inferencia — es la regla que hay detrás de esta vía de extracción sin inferencia.
**SYS-ADR-10** es la regla independiente que exige un punto de control humano obligatorio en el
momento del commit; gobierna el compromiso humano con una escritura, no la ausencia de un modelo en
la canalización. Son dos reglas que gobiernan dos mecanismos diferentes, no una sola regla compuesta.

Las extensiones previstas quedan fuera del límite de no inferencia por diseño: una interfaz de
consulta de identidad entre inquilinos y una capa opcional de similitud que podría *sugerir*
candidatos de fusión para revisión del operador. Ambas están destinadas al segundo anillo de la
plataforma; ninguna existe en la implementación actual, y bajo las reglas de la plataforma cualquier
sugerencia derivada de inferencia exigiría una acción explícita del operador antes de que nada
llegara al libro mayor del primer anillo.

## Lo que esto no es

**Esto no es el flujo de verificación basado en colas.** La herramienta con intervención humana
descrita en [[verification-surveyor]] opera sobre archivos JSON por transacción en una cola de
descubrimiento y nunca toca estos tipos de registro ni el servicio de archivos. Dos sistemas
comparten la palabra «identidad» y un prefijo de directorio, y no comparten código alguno.

**El registro Person implementado no es el documentado.** El esquema JSON y el README del componente
describen un registro más rico, con direcciones estructuradas, roles y metadatos, bajo nombres de
campo que nada escribe. El registro implementado son siete campos planos.

**No todo el que escribe estas formas de registro pasa por el servicio de archivos.** La herramienta
de minería independiente escribe estructuras idénticas directamente en archivos locales de solo
adición, fuera de la cadena de hash. Cualquier afirmación de que todos los registros de identidad
están cubiertos por las propiedades de integridad del libro mayor es cierta para la vía sancionada y
no para esa otra.

**La identidad determinista no es resolución de identidad.** La derivación garantiza que el mismo
correo produce el mismo identificador. No decide si dos direcciones de correo distintas pertenecen a
la misma persona, y no concluirá que dos direcciones distintas corresponden al mismo ser humano —
unirlas exige un acto deliberado del operador sobre la lista de alias, nunca una fusión automática.
Tratar el volumen de anchors como un hecho sobre un individuo también sería leer mal el esquema: un
Anchor no es en absoluto una afirmación sobre una persona, solo sobre la aparición de una dirección.

**Los conflictos no se enrutan hacia una persona.** Se rechazan y se devuelven como error a quien
llama. La propiedad entregada es la ausencia de fusión silenciosa; la adjudicación sistemática por
parte de un revisor no está implementada.

**La inmutabilidad no es una propiedad de estos registros en sí.** Procede del almacenamiento del
servicio de archivos: encadenado, con puntos de control y de solo lectura tras la escritura. Los
registros escritos fuera de esa vía — como los de la herramienta de minería — no tienen nada de eso.

## Véase también

- [[cryptographic-ledgers]] — el almacenamiento encadenado de solo adición que usa la vía de escritura sancionada
- [[worm-ledger-design]] — el modelo de registro de escritura única y sus garantías
- [[service-people]] — el componente propietario de los tipos Person, Anchor y Claim
- [[verification-surveyor]] — el paso independiente de confirmación humana para fragmentos en cola
- [[machine-based-auth]]
- [[three-ring-architecture]] — la disposición en capas en la que se sitúa el nivel de archivo
- [[tiered-entity-extraction-architecture]] — las etapas de extracción que producen anchors y claims
