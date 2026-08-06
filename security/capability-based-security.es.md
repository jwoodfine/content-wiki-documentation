---
schema: foundry-doc-v1
title: "Seguridad basada en capacidades"
slug: capability-based-security
category: security
index_group: identity-and-permissions
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
short_description: "La seguridad basada en capacidades entrega a cada componente un token infalsificable y acotado que debe presentar para actuar, en lugar del privilegio ambiental. Hoy la implementa una única capa de software; la aplicación a nivel de kernel está planificada."
paired_with: capability-based-security.md
---

La **seguridad basada en capacidades** es un modelo de control de acceso en el que un componente
solo puede realizar una operación presentando un token infalsificable que nombra tanto la operación
como su alcance. No existe privilegio ambiental — es decir, autoridad heredada del contexto de
ejecución: poseer una capacidad *es* el permiso, y un componente que no posee ninguna no puede
hacer nada, sea cual sea la cuenta de usuario bajo la que se ejecuta o la máquina en la que reside.
El modelo se remonta a la matriz de protección de Lampson de 1974 y alcanzó su expresión moderna
más conocida en el microkernel seL4, donde todo objeto del kernel — marcos de memoria, hilos,
puntos de comunicación — solo es alcanzable a través de una capacidad explícita alojada en una
tabla por proceso.

La diferencia respecto de las listas de control de acceso (ACL) que emplean la mayoría de los
sistemas es estructural, no cosmética. Bajo una ACL se comprueba la *identidad* del sujeto contra
una política en el momento de uso, y un proceso comprometido hereda todo lo que esa identidad tiene
permitido hacer. Bajo un modelo de capacidades lo que importa es la *posesión* del sujeto, y un
proceso comprometido solo alcanza los objetos concretos cuyas capacidades le fueron entregadas. El
privilegio queda así acotado en el momento de la delegación y no en el momento de uso.

## Lo que se aplica hoy

Hay un mecanismo de capacidades implementado, probado y en ejecución dentro del código de la
plataforma: la compuerta de peticiones de `service-content`. Es una capa de software, no de
hardware ni de kernel, y su alcance es la autorización entre instancias, no el aislamiento entre
procesos.

La compuerta lee una cabecera `X-Foundry-Capability`, resuelve la clave pública registrada del par
que llama, verifica una firma Ed25519 sobre una carga codificada en base64url, contrasta el nonce
de la carga con una caché de repetición y confirma que el alcance de archivo nombrado en la
capacidad permite la petición que se está haciendo. Los tokens caducados, los alcances que no
coinciden, los nonces repetidos y los pares no registrados se rechazan cada uno con códigos de
estado distintos, y los resultados se anexan a un registro de auditoría de interfaz. Diez pruebas
de integración ejercitan la compuerta directamente — cubren el caso de paso libre, la coincidencia
exacta y con comodín del alcance, los alcances discordantes, los pares no registrados, los tokens
caducados y la repetición de nonce — y cada una comprueba el código de estado concreto que devuelve
la compuerta.

Dos propiedades de esta compuerta importan para una lectura exacta. La primera: la capacidad va
*firmada*, no simplemente presentada — nadie puede acuñar un token salvo quien posea una clave
privada registrada. La segunda, y más importante: una petición que llega **sin** cabecera de
capacidad pasa sin alteración, por diseño, para preservar la ruta de llamada local ya existente y
considerada de confianza. La compuerta es, por tanto, un caso real y probado de control de acceso
basado en capacidades — un token firmado e infalsificable sustituye a la identidad —, pero es
aditiva y opcional, no un punto de paso obligatorio por el que deba atravesar todo el tráfico.

Existe una segunda capa de aplicación adyacente en `service-vm-tenant`, que extrae un token
portador, aplica comprobaciones de cuota por inquilino y serializa la creación de máquinas
virtuales tras un cerrojo documentado explícitamente como protección frente a condiciones de
carrera de tiempo-de-comprobación/tiempo-de-uso (TOCTOU). Esto es autorización por token
convencional, no un modelo de capacidades propiamente dicho — el token nombra a un inquilino, no a
un objeto y una operación —, pero es el otro punto de la plataforma donde la autoridad se comprueba
contra una credencial presentada en lugar de suponerse a partir del contexto.

## La arquitectura prevista

El diseño que describe la mayor parte de la literatura de seguridad de esta plataforma es más
amplio que la compuerta anterior: una capa de capacidades asentada sobre una
[[sel4-microkernel-substrate|base de microkernel]], con cada controlador, interfaz de red y
servicio de plataforma ejecutándose como un componente aislado que no posee derechos
administrativos generales. Para comunicarse con otro componente, un proceso invocaría una
capacidad, que el kernel — y no un middleware de nivel de aplicación — valida antes de permitir la
operación.

Por encima del kernel, el diseño contempla una capa de gestión de capacidades: en el momento del
despliegue, una declaración de política establecería qué componentes pueden comunicarse con cuáles
y qué operaciones tiene permitida cada uno, y las concesiones de capacidad resultantes se
distribuirían al arrancar el sistema. El plan aplica este modelo a toda la pila de despliegue
prevista — el sistema operativo de archivo seguro que custodia los datos en reposo, el entorno de
entrega en el borde que sirve contenido público y el
[[worm-ledger-architecture|registro de solo anexado]], cuya ruta de escritura solo sería alcanzable
por componentes que posean una concesión explícita de anexado.

Nada de esta capa de política en tiempo de despliegue existe hoy en código en ejecución. Verificado
mediante una búsqueda en todo el árbol de fuentes canónico, y no en un único componente: no hay
gestor de capacidades, ni envoltorio de aislamiento, ni componente puente de hipervisor en ninguna
parte. El paquete `moonshot-hypervisor` que albergaría una capa de mediación es un marcador de
posición de cuatro archivos cuya lista de dependencias está vacía y cuya única función devuelve una
cadena de verificación de andamiaje.

Sí existe trabajo genuino sobre seL4, pero es experimentación sobre hardware desnudo, no un tiempo
de ejecución de plataforma. El código fuente del kernel seL4 está incorporado al árbol de fuentes
de la plataforma, y un espacio de trabajo de desarrollo independiente, `moonshot-sel4-vmm`,
contiene código temprano de tiempo de ejecución de dominios de protección con una serie de binarios
de prueba que ejercitan la salida por consola, la comunicación entre procesos, el manejo de serie y
UART, y la red VirtIO bajo emulación. Ningún componente de PointSav publicado se ejecuta hoy sobre
seL4; los servicios vivos de la plataforma, incluidos los servicios de flota, de anfitrión y de
inquilino de la red de cómputo privada, son procesos Rust ordinarios construidos sobre `axum` y
`tokio`, sin ninguna dependencia de seL4 en ninguno de sus manifiestos. Este trabajo se describe
con más detalle en [[sel4-capability-topology]] y [[sel4-microkernel-substrate]].

El material publicado por el propio proyecto seL4 cuantifica por qué esta base resulta atractiva
como objetivo. Un microkernel bien diseñado ronda las diez mil líneas de código, frente a unos
veinte millones en un kernel monolítico convencional — una base de cómputo confiable tres órdenes
de magnitud menor. El análisis del proyecto sobre compromisos críticos del kernel de Linux concluyó
que un diseño de microkernel habría eliminado por completo alrededor del 29 por ciento de ellos y
habría mitigado otro 55 por ciento por debajo de la severidad crítica. Esas cifras describen la
arquitectura seL4 en general, tal como las publica el proyecto seL4, y no ningún despliegue de
PointSav; se recogen aquí como la justificación de la base que la plataforma pretende adoptar, no
como una afirmación sobre trabajo ya realizado.

## Por qué las dos capas no son intercambiables

Resulta tentador tratar la compuerta de capacidades de software como un primer incremento del
modelo de kernel planificado. Defienden cosas distintas, y una no se convierte en la otra con el
tiempo.

### Fronteras de amenaza distintas

La compuerta de software presupone un sistema operativo correcto, un tiempo de ejecución de
lenguaje correcto y una frontera de proceso correcta; protege los datos de un servicio frente al
llamante de otra organización. La aplicación de capacidades en el kernel presupone mucho menos —
está pensada para sostenerse incluso cuando un servicio está completamente comprometido, porque
quien rechaza la operación no autorizada es el kernel, no el servicio.

### Modos de fallo distintos

Un defecto en la compuerta de software es una comprobación de autorización eludida en la superficie
HTTP de un servicio. Un defecto en una distribución de capacidades del kernel es una frontera de
aislamiento vulnerada entre todos los dominios de la máquina. Esta asimetría es la razón por la que
las demostraciones formales de seL4 se dirigen al kernel y no a las aplicaciones que corren sobre
él.

### Historias de verificación distintas

La garantía de la compuerta de software son pruebas de integración. La garantía del modelo
planificado descansaría sobre las demostraciones verificadas por máquina del propio seL4 —
establecidas en el asistente de demostración Isabelle/HOL, que muestran que su implementación se
corresponde con su especificación y que un sistema correctamente configurado hace cumplir la
confidencialidad, la integridad y la disponibilidad — más los resultados de integridad y
confidencialidad publicados para arquitecturas concretas. Son resultados de terceros sobre el
kernel en sí, y se sostienen adopte o no esta plataforma dicho kernel algún día.

## Lo que esto no es

**Esto no describe un sistema de capacidades en ejecución y obligatorio.** Con la única excepción
de la compuerta de peticiones probada que se describe arriba, el control de acceso basado en
capacidades en esta plataforma es arquitectura prevista. Las afirmaciones sobre capacidades
ancladas en hardware, dominios de protección por servicio y distribución de capacidades dirigida
por política describen lo que está planificado, no lo que está desplegado.

**seL4 no se ejecuta hoy en ninguna parte de la plataforma.** La única aplicación de capacidades
que existe dentro del propio seL4 es una propiedad formalmente verificada de ese kernel — real,
pero aún no llevada a producción por esta plataforma.

**La compuerta de capacidades de software no es un punto de paso obligatorio.** Una petición sin
cabecera de capacidad no se rechaza. Cualquier caracterización de la plataforma como un sistema en
el que "toda petición porta una capacidad" sería hoy inexacta.

**La verificación formal de seL4 no es la verificación formal de esta plataforma.** Las
demostraciones en Isabelle/HOL son propiedades del microkernel como artefacto por derecho propio.
No dicen nada sobre la corrección del software construido encima, y esta plataforma no ha publicado
ninguna demostración formal propia.

**Las capacidades no sustituyen a los demás controles descritos en esta categoría.** Incluso bajo
el modelo planificado, el escaneo de secretos en el momento del commit, la inmutabilidad del
registro y la autorización de dispositivos basada en emparejamiento abordan cada uno una clase de
riesgo que las capacidades sobre objetos no tocan. Tampoco este artículo afirma que hagan falta
capacidades en hardware ni procesadores exóticos — el diseño previsto emplea un modelo de
capacidades por software aplicado por un microkernel sobre hardware convencional.

## Véase también

- [[sel4-capability-topology]]
- [[sel4-microkernel-substrate]]
- [[machine-based-auth]]
- [[cryptographic-ledgers]]
- [[worm-ledger-architecture]]
- [[pre-commit-defense-in-depth]]
