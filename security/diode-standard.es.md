---
schema: foundry-doc-v1
title: "Estándar del diodo"
slug: diode-standard
category: security
index_group: isolation-boundaries
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: forward-looking
language: es
language_protocol: TRANSLATE-ES
last_edited: 2026-08-22
editor: pointsav-engineering
short_description: "El Estándar del Diodo es la regla de diseño según la cual los comandos y los datos circulan en una sola dirección, de la autoridad al sujeto. Varios mecanismos reales la cumplen; ningún componente la aplica como estándar con nombre propio."
paired_with: diode-standard.md
---

**El Estándar del Diodo** es la regla de diseño de esta plataforma según la cual los comandos y los
datos circulan en una sola dirección — desde un lado con autoridad hacia un lado subordinado — sin
ningún camino de retorno capaz de transportar instrucciones. Toma su nombre del componente eléctrico
que conduce corriente en un sentido y la bloquea en el otro, y de los dispositivos de «diodo de
datos» empleados en redes industriales y de defensa para que la telemetría pueda salir de un
segmento protegido mientras se vuelve físicamente imposible que algo entre. Bajo el estándar, a un
sistema sujeto no solo se le *prohíbe* dar órdenes a sus pares o a su autoridad: el objetivo de
diseño es que no albergue código alguno capaz de expresar semejante orden — ningún cliente de shell
dirigido a la autoridad, ninguna tabla de enrutamiento entre pares, ninguna vía de petición
administrativa.

El argumento de seguridad de la regla tiene que ver con el movimiento lateral, no con la
confidencialidad. Las intrusiones graves rara vez son una sola brecha: son una cadena. Un atacante
alcanza un extremo de bajo valor y luego aprovecha la conexión que ese extremo ya mantiene hacia un
servidor de gestión para llegar a algo más valioso. Un enlace estrictamente unidireccional elimina
estructuralmente la segunda mitad de esa cadena. No existe canal inverso del que abusar, de modo que
un sujeto comprometido no puede escalar hacia la autoridad a través del enlace que los une, sean
cuales sean las credenciales que posea. La economía de la auditoría importa tanto como la economía
de la brecha: en una flota donde las conexiones pueden ir en cualquier dirección, revisar la
topología obliga a razonar por separado sobre cada par de sistemas. En una flota conforme al Diodo,
toda conexión legítima tiene la misma forma — control hacia abajo, telemetría saneada hacia arriba,
nada más — y quien revisa comprueba una sola regla en todas partes.

## Dónde está enunciada la regla

El estándar es un principio de diseño documentado en el material de ingeniería interno de esta
plataforma: una sección de guía de usuario, una entrada de glosario corporativo que lo define como
«un flujo universal de comandos en un solo sentido, del origen al extremo», notas internas de
arquitectura y material público de posicionamiento que lo nombra entre los protocolos
diferenciadores de la plataforma. También rige la topología de la [[os-family-overview|familia de
sistemas operativos]]: un lado con autoridad (la consola del operador y los sistemas de
orquestación) emite comandos y recibe telemetría, mientras que un lado sujeto (los sistemas de
archivo, entrega de medios, control de código fuente, infraestructura y administración de red)
ejecuta comandos y emite telemetría, sin originar jamás ninguno.

Conviene ser exactos sobre lo que eso significa. El Estándar del Diodo es real *como regla de diseño
enunciada*. Lo que no se ha establecido es que algún componente concreto lo imponga como estándar,
verifique su cumplimiento o rechace tráfico por vulnerarlo.

## Mecanismos que hoy cumplen la regla

Varios mecanismos ya implementados mueven datos genuinamente en una sola dirección. Se construyeron
cada uno para su propio fin y cada uno satisface la regla en su dominio; ninguno de ellos es un
aplicador de diodo de propósito general.

### Egreso de extracción y borrado

El caso más claro es el par de egreso. `tool-egress-pull` — que en su propia documentación se
autodenomina «el diodo asimétrico» — extrae fragmentos de datos desde un host de relevo hacia
almacenamiento local a través de SSH, los reensambla y descomprime, y solo después de calcular una
suma de verificación SHA-256 local que confirme la fidelidad envía una única autorización de vuelta
al relevo: un marcador «WIPE» que le ordena borrar su copia. Un demonio del lado del relevo consume
esos marcadores y elimina los archivos de origen. Los datos, por tanto, se mueven únicamente de
fuera hacia dentro; la única señal inversa es una autorización de borrado, que no transporta carga
útil alguna y no puede instruir al relevo para que haga ninguna otra cosa.

### Telemetría extraída, no enviada

La canalización de medición descrita en [[data-sovereignty-telemetry]] se recupera mediante scripts
de extracción programados, en lugar de ser empujada desde un controlador central hacia los
despliegues, lo que mantiene la dirección de control coherente con la regla.

### Ingesta descrita como un diodo

El componente de recolección del servicio de correo (`service-email/master-harvester-rs`) denomina
«the ingress diode» («el diodo de ingreso») a su propia lógica de microlotes, directamente en los
comentarios del código fuente y en el registro de arranque. Su función es coherente con ese marco:
atrae mensajes hacia dentro de la canalización de extracción y produce fragmentos en cola para el
procesamiento posterior, sin ninguna vía por la que la canalización pueda dar instrucciones al buzón
del que leyó. Este es el único punto del árbol donde un componente adopta para sí el vocabulario del
estándar, aunque lo hace de forma descriptiva: nada en él comprueba ni impone la direccionalidad
como regla.

### Promoción direccional del código

La aplicación más estricta de la plataforma recae sobre el código fuente, no sobre los datos en
ejecución. El paso de promoción discurre en una sola dirección — desde los espejos de
staging, al repositorio canónico, a los espejos de servicio locales — y el script rechaza activamente
el caso inverso: solo permite envíos de avance rápido o reproducciones explícitas commit a commit
sobre la rama canónica, bloquea la divergencia real del historial, bloquea las eliminaciones masivas
por encima de un umbral, bloquea los patrones que revertirían silenciosamente contenido canónico y
aplica una lista blanca estricta de rutas frente a directorios de primer nivel no declarados. Se
trata de un flujo unidireccional real y endurecido, y es la mejor prueba de que la regla se toma en
serio a nivel operativo — aunque gobierna una canalización de construcción, no la vía de comandos en
ejecución que describe el estándar.

## Lo que se esperaba encontrar y no está presente

Descripciones anteriores de este estándar nombraban un componente aplicador concreto: un pequeño
servicio de enlace conectable en caliente, ausente por omisión e instalable por el operador, que
sería el único código encargado de traducir los comandos de la autoridad en operaciones ejecutables
por el sujeto. No existe ningún paquete con ese nombre, bajo ninguno de los dos nombres empleados
anteriormente, en ninguna parte del código de la plataforma, y ni «Diode» ni «DiodeStandard»
aparecen en el código Rust fuera de la documentación referida al propio asunto de este artículo.

El único paquete con un nombre parecido es un marcador de posición de siete líneas cuya única
función devuelve una cadena de verificación de andamiaje y cuya lista de dependencias está vacía. No
contiene lógica direccional de ningún tipo.

**Lo que esto significa está genuinamente sin resolver, no resuelto en negativo.** El adaptador
puede ser un componente previsto y todavía no construido, o un diseño renombrado o sustituido —
material de planificación interna anterior lo enumera con estado «conceptual», coherente con un
diseño que se delimitó y se nombró pero no se construyó. La cuestión se ha señalado para su
confirmación por parte del grupo de ingeniería propietario, y este artículo no aventura una
respuesta. Hasta que llegue esa respuesta, el enunciado exacto es: el Estándar del Diodo es una
regla de diseño publicada para la topología de la plataforma, y no puede identificarse en el
monorepo ningún código que lo implemente como mecanismo general de aplicación.

## Aplicación por ausencia frente a aplicación por mecanismo

La afirmación más fuerte que a veces se hace de este diseño — que un sistema sujeto es
*estructuralmente incapaz* de emitir comandos de vuelta hacia su autoridad porque no se compila en
él ninguna capacidad de cliente — es una afirmación distinta y mucho más exigente que la del
movimiento unidireccional de datos.

Esa afirmación no es verificable solo a partir del código fuente. Lo que sí es observable es la
ausencia de código de comando inverso en los demonios pertinentes, hecho coherente con el diseño
pero de menor fuerza probatoria que un mecanismo positivo. La ausencia de una capacidad en la
compilación de hoy es una propiedad que cualquier commit futuro puede eliminar en silencio; un
mecanismo que rechaza el tráfico inverso es una propiedad que perdura. Quien evalúe la postura de
aislamiento de esta plataforma debe tratar la garantía direccional como una intención arquitectónica
respaldada por la forma actual del código, no como un invariante comprobado.

## Lo que esto no es

**Esto no es un diodo de datos por hardware.** Nada de lo aquí descrito implica un aislador óptico,
un enlace físico unidireccional ni dispositivo alguno que haga eléctricamente imposible la
transmisión inversa. La direccionalidad es una propiedad del diseño de software y del proceso, y
puede quedar anulada por una configuración incorrecta, cosa que no ocurre con un diodo físico.

**Ningún componente aplica el Estándar del Diodo por su nombre.** Ninguna comprobación de
conformidad, archivo de política ni control en tiempo de ejecución lo menciona. Los mecanismos
enumerados arriba cumplen la regla; ninguno de ellos la vigila.

**El adaptador aplicador nombrado anteriormente no existe.** Ninguno de los dos nombres de paquete
usados en descripciones previas aparece en ningún punto del código canónico — es una ausencia
confirmada, no una simple laguna sin examinar — y si fue abandonado, renombrado o aplazado sigue
siendo una pregunta abierta que este artículo no resuelve.

**Los controles de promoción de código no son el diodo en tiempo de ejecución.** Son la aplicación
direccional más completa de la plataforma, pero gobiernan cómo llega el código fuente a producción,
no cómo circulan los comandos entre una autoridad y un sujeto en ejecución. Confundir ambas cosas
exagera la garantía en tiempo de ejecución.

**El flujo unidireccional no es confidencialidad, ni es un esquema de autenticación.** La regla
limita lo que un atacante puede hacer tras alcanzar un sistema sujeto; no dice nada sobre si los
datos que cruzan el enlace están cifrados, y gobierna la *dirección* del control, no la *identidad*
de las partes. La identidad y el acceso son competencia de la [[machine-based-auth|autorización
basada en máquina]], que decide si dos máquinas pueden siquiera establecer una conexión — el Diodo
restringe después qué puede circular por una conexión que la autorización ya ha permitido.

## Véase también

- [[os-family-overview]]
- [[machine-based-auth]]
- [[capability-based-security]]
- [[sel4-capability-topology]]
- [[five-stage-supply-chain]] — la ruta de promoción cuya direccionalidad sí se aplica por script
- [[data-sovereignty-telemetry]] — la canalización de medición basada en extracción
- [[reverse-flow-substrate]] — el tratamiento más amplio del movimiento direccional de datos en la plataforma
