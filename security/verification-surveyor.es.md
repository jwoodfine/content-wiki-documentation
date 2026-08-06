---
schema: foundry-doc-v1
title: "Inspector de verificación"
slug: verification-surveyor
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
short_description: "Una herramienta de línea de comandos que exige a una persona confirmar cada identidad extraída contra evidencia externa antes de que ascienda de una cola a un registro verificado, con un tope de diez confirmaciones al día."
paired_with: verification-surveyor.md
---

**El inspector de verificación** (*verification surveyor*) es una herramienta de línea de comandos que
exige a una persona confirmar contra evidencia externa cada identidad extraída por máquina antes de
que se convierta en un registro duradero. Se sitúa entre una cola de descubrimiento de fragmentos sin
verificar, producida por extracción automatizada, y un registro verificado, y nada cruza esa frontera
sin una decisión humana consignada en el momento en que se toma — bajo un tope estricto de diez
verificaciones por operador y día.

Su propósito es mantener fuera del registro una clase concreta de error. La extracción automatizada
produce identidades plausibles — un nombre y una dirección de correo que aparecen cerca de una empresa
y un puesto en el mismo documento — y plausible no es lo mismo que correcto: una tubería automatizada
que procesa grandes volúmenes de texto acabará inevitablemente interpretando un enlace de
«Unsubscribe» como un nombre, o tomando un título de puesto de un pie de página en lugar de una
biografía. Una vez que una identidad errónea entra en un registro de solo anexado (*append-only*), no
puede retirarse discretamente; hay que sustituirla, y todo lo derivado de ella hay que revisarlo. El
inspector hace que el coste de ese error recaiga durante unos segundos sobre la atención de una
persona, en lugar de recaer para siempre sobre el registro.

## Cómo funciona

La herramienta es un script de Python de unas 140 líneas, invocado a través de un pequeño envoltorio de
shell. Lee de un directorio de cola de descubrimiento, escribe en un directorio de registro verificado
y consulta un catálogo de arquetipos, todo ello bajo una ruta base que por defecto apunta a una
ubicación de despliegue y puede anularse mediante una variable de entorno.

Para cada fragmento en cola se le muestra al operador la identidad extraída y se le hace una única
pregunta, planteada literalmente así: *Paste Verified LinkedIn URL (or type 'reject' / 'skip')* —
«pegue la URL verificada de LinkedIn, o escriba 'reject' / 'skip'». Es esencial que el operador busque
a la persona usando *su propio* navegador y *su propia* cuenta en el directorio externo — la plataforma
nunca inicia la búsqueda por sí misma, de modo que no necesita existir en ningún punto de la plataforma
un token persistente de una API ajena, no se devenga coste por consulta, y la plataforma nunca queda
expuesta a limitaciones de tasa ni a bloqueos de dirección por parte del servicio de directorio, porque
desde la perspectiva de ese servicio el tráfico es el de un ser humano usando su propia cuenta. La
respuesta del operador determina uno de tres desenlaces.

**Skip** (omitir) deja el fragmento intacto en la cola y pasa al siguiente. Es la respuesta correcta
cuando el operador no puede decidir.

**Reject** (rechazar) borra el fragmento de la cola sin más. No se conserva nada — ni registro del
rechazo, ni lápida. El fragmento se trata como ruido que nunca debió encolarse, lo que aun así da a la
tubería de extracción anterior una señal implícita sobre los modos de fallo que producen sus patrones,
incluso sin una traza de auditoría conservada del rechazo en sí.

**Una URL pegada** avanza a una segunda pregunta que solicita un identificador de arquetipo tomado de un
catálogo fijo de once arquetipos profesionales (The Executive, The Guardian, The Fiduciary y otros
ocho), cargado de nuevo desde la ontología de contenido de la plataforma en cada sesión, para que las
clasificaciones se mantengan consistentes entre operadores y a lo largo del tiempo en lugar de
escribirse libremente. Un identificador que no esté presente en el catálogo detiene el procesamiento de
inmediato en lugar de aceptar un registro sin clasificar. Una selección válida marca el registro como
verificado, adjunta a su procedencia la URL aportada, el arquetipo elegido y una marca de tiempo de
verificación, escribe el registro enriquecido en el registro verificado con el mismo nombre de archivo,
elimina el original de la cola e incrementa el contador diario.

### Qué contiene un fragmento en cola

El registro que juzga el operador es deliberadamente delgado: un campo identificador, un nombre para
mostrar, un objeto de afirmaciones que contiene una dirección de correo, una empresa y un puesto, y un
objeto de procedencia que nombra el archivo de origen del que se extrajo el fragmento. Nada en él es
autoritativo — cada campo es la lectura que una máquina hizo de un documento, y la entrada de
procedencia existe para que el operador pueda volver a ese documento si los valores extraídos parecen
mal encajados entre sí.

La verificación añade, no sustituye. La URL confirmada, el arquetipo elegido y una marca de tiempo de
verificación se adjuntan junto a lo que ya estaba, y el campo de estado pasa a verificado. Los valores
extraídos originales no se sobrescriben ni se descartan, de modo que un revisor posterior puede ver
tanto lo que se extrajo como lo que una persona concluyó al respecto. El archivo conserva su nombre
original al moverse entre directorios, que es lo que permite leer los dos directorios como una única
tubería y no como dos almacenes sin relación.

### El tope diario como mecanismo de calidad

Se impone un límite estricto de **diez verificaciones por operador y día**, llevado en un archivo de
control de una sola línea en el directorio personal del operador, que contiene una fecha y un recuento;
una fecha almacenada que ya no coincide con la de hoy reinicia el recuento automáticamente. No hay
bloqueo, porque se trata de un archivo local de un solo operador y no de un recurso compartido.

El límite es un control de calidad deliberado, no una restricción de capacidad, dirigido a un modo de
fallo bien conocido de la revisión humana: la aprobación de alto volumen y a velocidad degenera en
confirmación habitual, donde el clic del revisor se vuelve un reflejo en lugar de un juicio. Limitar el
día a diez mantiene cada verificación como un acto deliberado, e invierte la economía habitual de las
tuberías de datos, donde el rendimiento es la métrica y la revisión es el coste a minimizar — aquí la
revisión *es* el producto, y el tope es lo que hace creíble y no meramente nominal la afirmación de
calidad del registro verificado. Diez confirmaciones cuidadosas al día se acumulan hasta unas 3.650
relaciones verificadas por operador y año, con una tasa de error que el diseño sostiene que debería
aproximarse a cero, porque cada registro pasó una comprobación humana fresca y sin prisa contra una
fuente externa primaria.

**El propio README del componente de personas declara una cifra distinta y contradictoria.** Describe
el flujo del inspector como «restringido a 40-60 verificaciones humanas diarias». La comparación
directa con el código que se impone (`MAX_DAILY_VERIFICATIONS = 10`) y con la guía de usuario de la
plataforma, que de forma independiente indica diez tanto en su prosa como en su diagrama de tubería,
confirma que la cifra del README es errónea y que el código es la autoridad — una inconsistencia entre
documentos que merece nombrarse con precisión en lugar de conciliarse en silencio, dado que el README
sigue describiendo un mecanismo que no coincide con lo que se ejecuta.

## Dónde vive, y dónde no

El script forma parte del componente de consola de contenido (`app-console-content`), no del componente
de personas (`service-people`) — una pequeña corrección con consecuencias reales para quien intente
localizarlo o razonar sobre sus dependencias. Describir el servicio de identidad como «propietario» del
inspector exagera el acoplamiento.

Los directorios de la cola de descubrimiento y del registro verificado están situados bajo una *ruta*
del componente de personas en una disposición de despliegue, que es el origen de la confusión, pero el
código propio del componente de personas nunca los toca — buscar en el fuente de ese componente
cualquiera de los dos nombres de directorio no devuelve nada. Los fragmentos los colocan en la cola dos
programas divisores pertenecientes al servicio de correo (`email-splitter` y `sovereign-splinter`), que
escriben archivos planos directamente; el inspector los lee; nada más en la plataforma participa. Una
búsqueda sobre el árbol completo confirmó una única copia del script y una única definición de su
límite diario — no hay ningún duplicado derivado en otro lugar.

El resultado son dos sistemas paralelos que comparten la palabra «identidad» y un prefijo de directorio
sin compartir código alguno. Uno es la cola basada en archivos descrita aquí. El otro es el modelo de
registro descrito en [[identity-ledger-schema-design|el diseño del esquema del registro de identidad]],
al que se llega por una interfaz HTTP y que se persiste a través del servicio de archivos. Tratarlos
como un mismo sistema lleva a conclusiones incorrectas sobre ambos.

Una revisión anterior sobre este asunto concluyó erróneamente que el mecanismo del inspector no
existía, habiendo buscado únicamente en el fuente del propio servicio de identidad; aquel hallazgo fue
retractado en cuanto se localizó la implementación real en la consola de contenido. La lección
permanente: una búsqueda en un solo crate no es prueba suficiente de que un mecanismo descrito no
exista en ninguna parte del monorepo.

## Ninguna inferencia en toda la ruta

El paso de verificación no contiene ningún componente de inteligencia artificial de ningún tipo. El
script no hace llamadas de red, no importa ninguna biblioteca de modelos ni de inferencia, y su paso de
clasificación es una elección manual sobre un catálogo fijo. El propio fuente del componente de
personas enuncia la misma regla para los registros que construye — la extracción es solo comparación de
patrones, sin inferencia en ninguna ruta de construcción. Esto importa porque la plataforma
circundante sí contiene herramientas asistivas: la misma consola de contenido aloja una funcionalidad
de redacción, no relacionada, que llama a un endpoint de modelo de lenguaje. Ambas comparten componente
pero no ruta de código, y el flujo de verificación se mantiene deliberadamente al margen de aquella.

## Lo que esto no es

**Esto no forma parte del componente de personas.** El script vive en la consola de contenido. El
componente de personas es dueño de un modelo de identidad distinto, basado en HTTP y en un registro, y
no lee ni escribe en absoluto los directorios de la cola.

**Esto no es un servicio de verificación automatizada.** Ninguna clave de API, ningún scraper y ninguna
integración conectan la plataforma con ningún directorio externo — si el operador no busca
personalmente un registro, no se produce ninguna búsqueda.

**Esto no es un flujo de aprobación.** No hay un segundo revisor, ni ruta de escalado, ni registro de
los rechazos. Un solo operador decide, y un fragmento rechazado se borra en lugar de conservarse para
auditoría.

**Un registro verificado no es un registro autenticado.** La confirmación establece que una persona
contrastó un fragmento extraído contra un perfil profesional público que juzgó corresponder al mismo
individuo. Es un juicio humano meditado, no una prueba de identidad, y hereda la exactitud que tenga
ese perfil externo.

**El tope diario no es una frontera de seguridad.** Es un contador simple en un archivo del propio
directorio personal del operador, reiniciable con solo borrarlo. Existe para proteger la calidad de la
decisión, no para resistir a un adversario.

**Diez al día no es un plan de escalado.** Al ritmo impuesto, el mecanismo verifica como mucho unos
pocos miles de identidades al año por operador. Cualquier corpus mayor requiere más operadores, no un
tope más alto — quien imagine miles de verificaciones por semana y operador ha imaginado un sistema
distinto y, según el propio argumento de este diseño, de menor calidad.

## Véase también

- [[identity-ledger-schema-design]] — el modelo de registro aparte al que se llega a través del servicio de archivos
- [[service-people]] — el componente dueño de ese modelo, y el que no es dueño de esta herramienta
- [[adr-07-zero-ai-in-ring-1]] — la regla que prohíbe la inferencia en la ruta de extracción del nivel de archivo
- [[archetypes-and-chart-of-accounts]] — el catálogo de clasificación del que se nutre la segunda pregunta
- [[tiered-entity-extraction-architecture]] — las etapas de extracción que llenan la cola
- [[service-email]] — el componente cuyos divisores escriben los fragmentos en cola
- [[machine-based-auth]]
