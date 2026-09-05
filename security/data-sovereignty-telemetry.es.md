---
schema: foundry-doc-v1
title: "Soberanía de datos y telemetría de estado cero"
slug: data-sovereignty-telemetry
category: security
index_group: data-handling-and-privacy
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
short_description: "La telemetría de estado cero es la postura prevista: medir el uso de un sitio sin conservar datos identificativos. La canalización que se ejecuta hoy escribe direcciones IP completas y sin enmascarar en un archivo de texto plano durante hasta un año; el enmascaramiento no está implementado."
paired_with: data-sovereignty-telemetry.md
---

La **telemetría de estado cero** es el objetivo de diseño que rige cómo la plataforma PointSav
pretende medir el uso de sus superficies públicas: sin conservar información personal
identificable, sin cookies de rastreo, sin estado de sesión — señal agregada sin registros
individuales. Junto a él va el principio más amplio de la **soberanía de datos**: que los registros
operativos que genera un despliegue pertenecen al cliente, se ejecutan sobre infraestructura que
este controla y no se exportan a un proveedor ni a un tercero de medición. El estado cero es tanto
una postura de seguridad como de privacidad: un almacén de telemetría que nunca contuvo la
identidad de un lector es un almacén cuya brecha no revela nada sobre los lectores, que es la
respuesta a incidentes más barata que existe.

Ese objetivo no se cumple hoy, y la primera tarea de este artículo es decirlo con claridad. La
canalización de ingesta real de la plataforma registra actualmente la dirección IP completa y sin
enmascarar de quien realiza la petición, junto con la marca de tiempo, el URI solicitado y la
cadena de agente de usuario, para cada petición que registra, y conserva el registro en bruto
durante hasta un año. La distancia entre el diseño declarado y el código en ejecución se detectó
mediante inspección directa del código de ingesta y se ha escalado internamente como una
discrepancia relevante para el cumplimiento; sigue abierta a fecha de redacción de este texto. Lo
que sigue describe la arquitectura prevista, el comportamiento real de la canalización — verificado
directamente contra el código canónico — y el trabajo concreto que haría falta para cerrar la
distancia entre ambos.

## Lo que hace hoy la canalización

La canalización de medición consta de dos programas en `app-mediakit-telemetry`, ambos leídos
directamente del código canónico para este artículo.

El recolector (`telemetry-daemon`) acepta un cuerpo JSON que contiene un URI solicitado, una marca
de tiempo y una cadena completa de agente de usuario. Obtiene la dirección del cliente de la
cabecera de petición `x-forwarded-for`, tomando el primer valor separado por comas, y recurre a una
dirección de marcador de posición cuando la cabecera no está presente. A continuación escribe una
única línea con valores entrecomillados y separados por comas — dirección, marca de tiempo, URI y
agente de usuario — en un archivo de registro de texto plano abierto en modo anexado.
La dirección se escribe literalmente: **en ningún punto del
recolector se produce enmascaramiento, truncamiento, hashing ni generalización de la dirección del
cliente.**

El segundo programa, `omni-matrix-engine`, lee ese archivo, omite las filas que llevan la dirección
de marcador de posición y realiza una búsqueda geográfica de cada dirección restante contra una
base de datos MaxMind GeoLite2 City alojada localmente, de la que extrae país, primera subdivisión,
ciudad y zona horaria. Agrupa los eventos en ventanas móviles y escribe un informe de resumen.
También opera sobre la cadena de dirección en bruto, y no le queda otra: una dirección enmascarada
no resuelve a un resultado útil a nivel de ciudad, de modo que el diseño actual depende activamente
de conservar el valor completo en ese paso.

### La exposición del recolector

Otras dos propiedades del recolector son relevantes para una lectura de seguridad. El recolector
acepta envíos de cualquier llamante que pueda alcanzarlo, sin autenticación — su propio comentario
en el código atribuye esto a la aceptación de tráfico de malla sobre la red WireGuard de la
plataforma — y su configuración CORS permite cualquier origen.

En conjunto, el punto de acceso admite un registro de cualquier llamante capaz de alcanzarlo, y los
valores que almacena los suministra el llamante: el URI, la marca de tiempo y el agente de usuario
se leen de un cuerpo JSON enviado, no los observa el servidor, y solo la dirección se deriva de una
cabecera. Un registro del archivo acredita, por tanto, que algo lo publicó, no que una página fuera
realmente vista. Quien construya análisis sobre estos datos, o valore su sensibilidad, debe
tratarlos como afirmados por el llamante y no como observados por el servidor.

Las descripciones públicas de la telemetría de esta plataforma como una arquitectura de estado
cero, enmascarada o preservadora de la privacidad describen la postura prevista, no el
comportamiento actual. Esta brecha se ha escalado a la gobernanza de la plataforma en lugar de
resolverse en la documentación, y la remediación — enmascarar antes de persistir, o reestructurar
el paso geográfico para que trabaje a partir de un valor ya generalizado — no está implementada a
fecha de redacción de este texto. Es un cambio de sistema que debe realizar el equipo propietario
del componente de telemetría, no un cambio de redacción.

## Retención y rotación

Un script de despliegue rota el archivo activo hacia un histórico con fecha, reinicia el recolector,
regenera los informes y después elimina los archivos en bruto históricos de más de **365 días** y
los informes generados de más de **30 días**.

De ahí se siguen dos cosas. La primera: las filas en bruto que contienen direcciones de cliente
completas persisten hasta un año; se trata de una política de retención acotada, no de retención
cero. La segunda: la rotación no realiza anonimización alguna — es únicamente borrado por tiempo,
de modo que una dirección está o bien íntegramente presente o bien íntegramente ausente, sin que se
conserve ninguna forma generalizada intermedia para análisis de largo plazo.

No se encontró en el código canónico ningún temporizador ni unidad programada que invoque este
script de rotación, por lo que aquí no ha podido establecerse su cadencia real de ejecución en un
despliegue dado. El archivo en sí no está confirmado en el repositorio, y la base de datos
geográfica tampoco; ambos son artefactos de tiempo de ejecución o aprovisionados por el operador,
de modo que no puede informarse de ningún tamaño ni recuento de filas.

## Lo que sí sostiene la afirmación de soberanía

Varias propiedades estructurales del diseño son exactas tal como se enuncian y conviene separarlas
de la brecha de enmascaramiento, porque son la sustancia de la afirmación de soberanía de datos.

**La medición se ejecuta sobre la propia infraestructura del operador.** El recolector, el programa
de análisis y el archivo de salida son componentes del propio despliegue. No hay llamada a ningún
proveedor de analítica externo, ni script de terceros incrustado en una página servida con fines de
medición, ni exportación del registro a un servicio operado por un proveedor.

**La resolución geográfica es fuera de línea.** La búsqueda se realiza contra un archivo de base de
datos alojado localmente en la misma máquina. No se envía ninguna dirección a un servicio remoto de
geolocalización para resolverla. El operador aprovisiona la base de datos por su cuenta y bajo su
propia licencia, y esta no se redistribuye dentro del repositorio de forma deliberada.

**No se establecen cookies.** Una búsqueda en todo el árbol de código canónico encontró cero
apariciones de una cabecera `Set-Cookie` en cualquier punto de la plataforma, y ningún componente
de banner de consentimiento de ninguna clase. Una página de privacidad publicada para una de las
superficies de marketing afirma que el sitio no establece cookies, no ejecuta analítica de
terceros, publicidad ni scripts de rastreo, y no muestra banner de consentimiento porque no hay
nada que consentir. La afirmación de ausencia de cookies es coherente con lo que muestra el código
— lo que resuelve un punto que una revisión anterior había dejado marcado como abierto.

Dicho esto, dos salvedades acompañan a lo anterior. Una superficie separada de marketplace sí
utiliza un token de sesión funcional para el estado de licencia de quien ha iniciado sesión, que es
un mecanismo de sesión y no de rastreo, pero no es "ningún estado en absoluto". Y un conjunto de
maquetas propuestas de sitio público alojadas en el árbol contiene una baliza de cliente mucho más
detallada — referente, ventana gráfica, zona horaria, memoria del dispositivo, número de
procesadores, profundidad de desplazamiento, tiempo de permanencia, objetivos de clic, tipo de red
—, enviada a un punto de telemetría sin ninguna solicitud de consentimiento, junto a texto de
marketing en la misma página que proclama una "Zero-Cookie and Zero-State Telemetry architecture"
(arquitectura de telemetría sin cookies y de estado cero). Si esas maquetas están desplegadas en
alguna superficie viva no pudo determinarse a partir del código, y se señalan aquí en lugar de
darse por inactivas.

## Lo que esto no es

**Esta no es una canalización de telemetría enmascarada ni anonimizada.** Se escriben direcciones
de cliente completas en un archivo de texto plano y se conservan hasta un año. Cualquier afirmación
de que se descarta el último octeto, o de que las direcciones se someten a hash antes de
persistirse, es inexacta como descripción del código en ejecución.

**Esto no describe una posición de cumplimiento.** La intención de diseño está alineada con los
principios de minimización de datos, pero una canalización que almacena direcciones sin enmascarar
junto a marcas de tiempo, rutas solicitadas y cadenas completas de agente de usuario trata datos
personales, y este artículo no debe leerse como afirmación de que se satisface ninguna obligación
regulatoria concreta — RGPD, PIPEDA u otra. Esa evaluación corresponde al operador y a sus
asesores.

**La ausencia de cookies no es la ausencia de identificadores.** Una dirección emparejada con una
cadena de agente de usuario y una ruta de petición es un registro reidentificable en muchos
contextos. La medición sin cookies reduce la vinculación entre sitios; no convierte un registro en
anónimo.

**El borrado por tiempo no es anonimización.** La retención limita la duración de la exposición.
Dentro de la ventana de retención, el registro identifica plenamente.

**El estado cero no es el estado actual.** Es el objetivo hacia el que está escrito el diseño. Si
el comportamiento presente de la canalización es coherente con algún régimen concreto de protección
de datos es una determinación jurídica fuera del alcance de este artículo; lo que este artículo
afirma a partir de la inspección directa del código es más estrecho y verificable: hoy se están
escribiendo direcciones IP completas en almacenamiento persistente, y la arquitectura de estado
cero es un objetivo, no una descripción. Tampoco es este un informe de incidente — aquí no se
constata ningún acceso no autorizado ni uso indebido de los datos registrados, únicamente una
divergencia entre diseño e implementación — y no se adjunta ningún plazo a la remediación anterior,
porque no se ha comprometido ninguno.

## Véase también

- [[sovereign-telemetry]] — la posición arquitectónica más amplia sobre la medición en manos del operador
- [[telemetry-architecture]] — la estructura de la canalización de recolección y análisis
- [[app-mediakit-marketing]] — la superficie servida cuya página de privacidad publicada se cita arriba
- [[cryptographic-ledgers]] — el registro de solo anexado usado para eventos auditables, distinto de esta canalización
- [[customer-owned-graph-ip]] — el principio de propiedad aplicado a los datos derivados
- [[machine-based-auth]]
