---
schema: foundry-doc-v1
title: "Topología de capacidades en seL4"
slug: sel4-capability-topology
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
last_edited: 2026-08-06
editor: pointsav-engineering
short_description: "En un sistema seL4 la política de seguridad es la forma del grafo de capacidades establecido en el arranque, no una capa de política en tiempo de ejecución. El trabajo propio son nueve binarios de prueba sobre hardware desnudo; ningún servicio de la plataforma se ejecuta sobre seL4."
paired_with: sel4-capability-topology.md
---

**Una topología de capacidades** es la disposición de qué componentes poseen referencias a qué objetos
del kernel — el grafo de quién puede alcanzar qué. En un sistema construido sobre el microkernel seL4
ese grafo *es* la política de seguridad. No hay un motor de políticas aparte al que se consulte en
tiempo de ejecución, ni un archivo de configuración que describa las operaciones permitidas, ni una
identidad que se contraste con un conjunto de reglas: un componente puede invocar un objeto del kernel
si y solo si posee una capacidad que nombre ese objeto en su espacio de capacidades, y la única
pregunta del kernel en cada llamada al sistema es si la capacidad presentada existe y permite la
operación solicitada. Dibuje el grafo de qué componentes poseen capacidades sobre qué objetos y habrá
dibujado — exactamente, no de forma aproximada — lo que cada componente puede llegar a alcanzar.

La consecuencia práctica es que la revisión de seguridad de un sistema seL4 es revisión de topología.
No hay una capa de imposición en tiempo de ejecución que inspeccionar en busca de defectos, porque la
imposición es una propiedad del grafo trazado al arrancar el sistema. Si el grafo es correcto, el
aislamiento se sostiene; si a un dominio se le entregó una capacidad que no debería tener, ninguna
comprobación posterior lo detectará, porque no hay comprobación posterior.

## El invariante de la topología

El kernel impone un invariante por encima de todos los demás, la regla clásica de los sistemas de
capacidades según la cual *solo la conectividad engendra conectividad*: un componente puede obtener una
capacidad nueva únicamente si esta le es transferida por un canal sobre el que ya posee una capacidad.
La autoridad nunca se conjura; solo fluye por aristas existentes. Si el componente A no tiene ninguna
ruta hacia el componente B — ni directa ni transitivamente a través de cualquier cadena de
intermediarios —, entonces A no puede obtener información de B, no puede modificar el estado de B y no
puede hacer que B actúe.

De ello se siguen dos consecuencias. Un arquitecto que dibuja la topología de capacidades de un sistema
ha *especificado* su política de seguridad — dos componentes que no comparten ninguna ruta no tienen
canal, sea cual sea el código que se ejecute dentro de ellos, y un componente comprometido no puede
escapar de su partición porque escapar exigiría una arista que no tiene. Y el modelo disuelve el
problema del delegado confundido (*confused deputy*) que sufren los sistemas basados en listas de
control de acceso: puesto que quien llama debe transmitir la capacidad concreta que autoriza cada
operación, un intermediario privilegiado no puede sustituir la concesión más estrecha de su llamante
por su propia autoridad más amplia. Esto es fundamentalmente distinto de los indicadores gruesos de
privilegio que los kernels convencionales también llaman «capabilities», que son de estilo ACL y
conservan la debilidad del delegado confundido.

## Cómo llega a existir la topología

seL4 arranca una única tarea inicial y le entrega capacidades sobre prácticamente todo — la memoria sin
tipar (*untyped*) que cubre la RAM física, el controlador de interrupciones, los puertos de
entrada/salida y el espacio de capacidades raíz. Ninguna otra cosa tiene autoridad alguna. Esa tarea
inicial realiza entonces la distribución: retipifica la memoria sin tipar hacia los objetos del kernel
concretos que cada dominio necesita — bloques de control de hilo, tablas de páginas, endpoints para la
comunicación — y concede a cada dominio exactamente las capacidades que su función requiere, sin
quedarse ninguna que no necesite. Una vez completada la distribución, la tarea inicial puede revocar su
propia autoridad restante.

La autoridad es por tanto monótonamente no creciente durante la operación normal — un dominio no puede
fabricar una capacidad que no le fue dada — y la delegación es explícita y trazable: toda referencia
que un dominio posee sobre los recursos de otro fue transmitida por una ruta que puede enumerarse a
partir de la descripción de arranque. Como los dominios no comparten memoria por defecto, la
comunicación ocurre a través de objetos endpoint, y una capacidad de endpoint es en sí misma el permiso
para comunicarse — un dominio que no posea ninguna hacia otro no tiene canal alguno hacia él, no un
canal bloqueado. Restringir quién puede hablar con quién no requiere ninguna regla de cortafuegos; se
expresa sencillamente no concediendo nunca la capacidad.

En el marco de componentes recomendado por seL4, el Microkit, la arquitectura de un sistema es
estática: los dominios de protección, sus canales de comunicación y sus regiones de memoria compartida
se declaran en una descripción de sistema en tiempo de compilación, y la cadena de herramientas del
marco traduce esa descripción a objetos del kernel y genera código de arranque que lleva de forma
demostrable el sistema arrancado al estado descrito — señalando el propio proyecto seL4 que partes de
las demostraciones a nivel del marco todavía se están completando.

## Qué demuestra la verificación formal

La afirmación distintiva de seL4 es que la imposición de este modelo está comprobada por máquina, no
simplemente aseverada. Estos son resultados de terceros sobre el kernel como artefacto, publicados por
el proyecto seL4 y citados aquí como afirmaciones propias de ese proyecto y no reverificadas de forma
independiente para este artículo; establecen, en secuencia:

- **Corrección funcional** — la implementación en C es un refinamiento de la especificación matemática
  abstracta del kernel: el código no puede hacer nada que la especificación no permita, lo que descarta
  los ataques estándar a nivel de implementación (violaciones de seguridad de memoria, inyección de
  código, secuestro del flujo de control) como comportamientos que el kernel pueda exhibir.
- **Validación de la traducción** — se demuestra, mediante una cadena de herramientas automatizada, que
  el binario compilado implementa correctamente el C verificado, lo que saca al compilador de la base
  de confianza.
- **Imposición de la seguridad** — demostraciones que conectan la especificación abstracta con las
  propiedades clásicas de confidencialidad, integridad y disponibilidad: en un sistema correctamente
  configurado, el kernel no permitirá que una entidad lea datos sin acceso de lectura ni modifique
  datos sin acceso de escritura.

Las demostraciones descansan sobre supuestos declarados — que el hardware se comporta como está
especificado, que la especificación captura las propiedades pretendidas, que el pequeño núcleo del
comprobador de demostraciones es sólido, y que la distribución inicial de capacidades es ella misma
correcta — y llevan un límite reconocido: todavía no cubren el comportamiento temporal, de modo que los
canales encubiertos por temporización quedan fuera de las garantías actuales. La completitud varía
además según la arquitectura; las propias páginas de estado del proyecto seL4, y no este artículo, son
el registro autorizado de qué propiedad está demostrada dónde. La escala forma parte de la
credibilidad: la demostración original de corrección funcional alcanzó unas doscientas mil líneas de
guion de demostración comprobado por máquina, hoy ya por encima del millón, contrastadas contra un
núcleo de confianza de solo unas pocas decenas de miles de líneas. Todas ellas siguen siendo
propiedades del microkernel como artefacto y no se transfieren hacia arriba: una demostración sobre el
kernel no dice nada sobre el software que se ejecuta por encima de él, y esta plataforma no ha
publicado ninguna demostración formal propia.

## El estado del trabajo propio

Existe código seL4 real y funcional en el árbol de fuentes de esta plataforma, y es experimentación
sobre hardware desnudo, no un entorno de ejecución de servicios. El paquete `moonshot-sel4-vmm` es un
componente propio en Rust compilado como `no_std` y `no_main` para un objetivo AArch64 sobre hardware
desnudo, que contiene nueve binarios independientes, cada uno correspondiente a un hito numerado y
condicionado a una cadena literal de éxito impresa en un registro serie bajo emulación. Cubren: un
banner de consola a través de la llamada de salida de depuración del kernel; dos hilos intercambiando
un mensaje por un endpoint; un dominio de protección de serie y otro de consola comunicándose por paso
de mensajes; una escritura directa mapeada en memoria a un controlador serie PL011; un panel de estado
renderizado a través del dominio de serie; y una secuencia de cuatro pasos que pone en marcha un
dispositivo de red paravirtualizado — sondearlo e inicializarlo, llevar sus anillos de descriptores al
estado listo, transmitir tramas Ethernet, ARP y de petición de eco en bruto mediante acceso directo a
memoria, y finalmente completar una petición TCP en bruto a un endpoint de salud en el anfitrión.

Ese último hito es un resultado genuino: un programa Rust `no_std` ejecutándose sobre seL4 bajo
emulación, manejando un dispositivo de red virtual sin ningún sistema operativo por debajo, y
completando un intercambio HTTP. También son nueve binarios de demostración, no un hipervisor ni un
entorno de ejecución de plataforma. El kernel en sí, sus herramientas de compilación y un pequeño
andamiaje de proyecto están presentes como fuente de terceros vendorizada en directorios separados, con
su licencia original, y con parte de la salida de compilación versionada junto a ellos.

## Qué ejecuta la plataforma en su lugar

Los servicios que llevan tráfico en vivo en la red privada de cómputo son servicios Rust
convencionales. Leyendo directamente sus manifiestos de dependencias, el controlador de flota, el
agente anfitrión por nodo y el proxy de cara al inquilino dependen cada uno de `axum`, `tokio`,
`reqwest`, `serde`, `chrono` y crates de trazado, más un paquete compartido de tipos de cable.
**Ninguno de los tres lleva dependencia alguna de seL4.** Son servicios HTTP ordinarios escuchando en
puertos ordinarios.

Esto importa porque contradice una descripción que apareció en textos anteriores sobre esta plataforma:
que la interfaz de red de malla, el servidor de la ceremonia de emparejamiento y el servicio de gestión
de flota ocupan cada uno dominios de protección seL4 distintos. Como afirmación en presente, eso es
falso. Esas tres funciones existen y están separadas entre sí, pero lo están como procesos y servicios
sobre un sistema operativo de propósito general, no como dominios aislados por capacidades bajo un
microkernel verificado. El componente que albergaría una capa de mediación de hipervisor,
`moonshot-hypervisor`, es un marcador de posición de cuatro archivos con una lista de dependencias
vacía.

El interés de la plataforma en seL4 es directo: una flota construida sobre una topología de capacidades
impuesta por el kernel convertiría las reglas unidireccionales del [[diode-standard|Diode Standard]] y
los valores por defecto de mínimo privilegio del
[[capability-based-security|modelo de capacidades]] en propiedades del kernel y no en disciplina de
aplicación. Ese sigue siendo el motivo de la inversión descrita arriba, no una afirmación de que ya
haya llegado.

## Lo que esto no es

**Ningún servicio de la plataforma se ejecuta hoy sobre seL4.** Los servicios de flota, anfitrión e
inquilino son servicios Rust y `axum` corrientes, sin dependencia de seL4 en ningún manifiesto.
Cualquier afirmación de que los servicios de la plataforma ocupan dominios de protección seL4 distintos
describe únicamente arquitectura prevista.

**El trabajo propio sobre seL4 no es un hipervisor.** Son nueve binarios de demostración condicionados
por emulador que establecen que las primitivas básicas del kernel — salida de depuración, hilos,
endpoints, acceso a dispositivos mapeados en memoria y acceso directo a memoria a una tarjeta de red
virtual — pueden manejarse desde Rust `no_std`. No se aloja ningún sistema operativo invitado y ninguna
carga de trabajo de producción se ejecuta sobre él.

**Una topología de capacidades no es una lista de control de acceso.** No se consulta, ni se evalúa, ni
se contrasta con una identidad en tiempo de ejecución. Revisarla significa revisar la distribución
hecha en el arranque, porque un error ahí no se detecta después.

**La verificación formal de seL4 no es verificación de esta plataforma.** Las demostraciones son
propiedades del kernel bajo supuestos declarados, el más importante de los cuales es que la
distribución inicial de capacidades sea ella misma correcta — que es precisamente la parte que todo
sistema adoptante debe acertar por su cuenta. Tampoco es una constante universal entre plataformas de
hardware: las propiedades formales son por arquitectura, con completitud variable, y un despliegue
hereda únicamente lo que esté demostrado para su familia de procesadores.

**Una topología correcta no es confidencialidad frente a todo canal.** Los resultados publicados sobre
confidencialidad abordan flujos de información especificados bajo supuestos especificados; los canales
laterales de temporización y otros canales físicos quedan fuera de lo que aborda una demostración de
corrección funcional, según la declaración del propio proyecto seL4, y los ataques físicos y los
defectos de hardware quedan fuera de las garantías de cualquier kernel.

**Tampoco es una afirmación de que el software dentro de un dominio de protección sea correcto.** Un
componente puede tener tantos errores como cualquier otro programa; lo demostrado es que su alcance
está acotado por las capacidades que posee, no que se comporte bien dentro de ellas.

## Véase también

- [[sel4-microkernel-substrate]] — el kernel en sí y por qué se seleccionó
- [[sel4-aarch64-qemu-substrate-target]] — el objetivo emulado contra el que se ejecutan los binarios de demostración
- [[sel4-unikernel-substrate]] — la dirección de espacio de direcciones único que se está considerando
- [[capability-based-security]] — el modelo de control de acceso en su forma general
- [[diode-standard]]
- [[ppn-tenant-vm-isolation]] — la frontera de aislamiento que soporta hoy la carga comercial
- [[os-totebox-service-pd-model]] — la disposición de dominios de protección prevista para el sistema operativo de archivo
