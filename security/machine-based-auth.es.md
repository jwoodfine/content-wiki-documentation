---
schema: foundry-doc-v1
title: "Autorización basada en máquina"
slug: machine-based-auth
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
short_description: "El acceso se concede a la clave de un dispositivo, no a la contraseña de una persona. Una ceremonia de emparejamiento con código corto liga la huella de una clave SSH a un registro de usuario tras la aprobación del operador, sin almacenar ninguna contraseña en ningún sitio."
paired_with: machine-based-auth.md
---

**La autorización basada en máquina** (MBA, por sus siglas en inglés) concede acceso a la clave
criptográfica de un dispositivo concreto en lugar de al secreto memorizado de una persona. No hay
contraseña que almacenar, transmitir, adivinar, reutilizar ni suplantar por phishing; lo que posee
el usuario es una clave privada que nunca abandona su máquina, y lo que registra el sistema es la
huella de la clave pública correspondiente. El acceso se revoca eliminando esa huella, no forzando
un restablecimiento de credenciales.

Toda contraseña es un secreto que una persona debe recordar y, por tanto, un secreto que un atacante
puede obtener por phishing, adivinación, relleno de credenciales o ingeniería social — la categoría
entera del robo remoto de credenciales existe porque la credencial es algo que un humano sabe. La
autorización basada en claves traslada el ataque al acceso físico o persistente a una máquina
concreta, algo mucho más difícil de conseguir a escala y mucho más visible cuando ocurre.

## La ceremonia de emparejamiento

La implementación en producción es el componente `system-gateway-mba`, y funciona como una secuencia
de petición, aprobación y vinculación, no como un inicio de sesión.

Un dispositivo envía una petición de emparejamiento que porta un nombre de usuario, una
organización, su clave pública y la huella de esa clave. El servidor registra la petición con un
identificador generado, un código corto de emparejamiento, un contador de intentos, una hora de
creación y una hora de caducidad, y la sitúa en el estado `pending`. Un operador la aprueba o la
deniega después fuera de banda, tras comparar el código corto mostrado en el dispositivo con el
mostrado en la interfaz de aprobación — el paso que impide aprobar por error la petición de una
máquina desconocida.

La aprobación lleva la petición a `approved` y crea el registro de usuario que liga nombre de
usuario, organización y huella de clave. La denegación la lleva a `denied`. Un barrido marca como
`expired` las peticiones cuya caducidad ha vencido. Cinco rutas HTTP cubren la ceremonia: petición,
aprobación, denegación, listado de peticiones pendientes y consulta de estado por petición.

La forma del registro es deliberadamente pequeña. La tabla de peticiones guarda identificador,
código, nombre de usuario, organización, huella, clave pública, rol, estado, número de intentos,
hora de creación y caducidad. La tabla de usuarios guarda huella, nombre de usuario, organización,
rol, un indicador de actividad y la hora de creación, con la huella como valor único y la
organización restringida a uno de dos valores permitidos. **No existe campo de contraseña en ninguna
de las dos tablas** — comprobable leyendo el esquema.

### Qué es la huella

El módulo de autorización tiene diez líneas y hace exactamente una cosa: calcula una huella SHA-256
en formato OpenSSH de una clave pública presentada. Las dependencias del componente son una
biblioteca SSH usada para el análisis de claves y el cálculo de huellas, una base de datos SQLite
embebida, una fuente de números aleatorios y crates ordinarios de serialización y HTTP. El código de
emparejamiento en sí se genera a partir de una fuente aleatoria no criptográfica, en un alfabeto
transcribible por una persona — apropiado para un código que un operador lee en voz alta o vuelve a
teclear, y que no es un secreto por sí mismo, ya que resulta inútil sin la aprobación del operador.

## Dos capas independientes: pertenencia a la red y emparejamiento de aplicación

La MBA opera en la capa de aplicación, deliberadamente independiente de la infraestructura de red.
En los despliegues que usan la [[ppn-mesh-architecture|red privada en malla]] de la plataforma,
alcanzar siquiera una máquina exige ser un par registrado de la malla cifrada: eso es la pertenencia
a la red, una capa. La MBA es la otra: incluso una máquina capaz de alcanzar el destino por red es
rechazada en la frontera de la aplicación si su huella de clave no coincide con un emparejamiento
aprobado. Una parte que opere la infraestructura de red — incluido el proveedor — no obtiene por
ello acceso de capa de aplicación a los datos que circulan sobre ella: la accesibilidad de red y el
acceso a los datos los conceden mecanismos distintos, en manos de partes distintas.

Un servicio independiente de incorporación de nodos ejecuta la misma forma de
petición-aprobación-denegación-caducidad para admitir nodos de cómputo en la propia red privada. Sus
registros portan un identificador de nodo, una clave pública de malla, una capa inferior declarada y
una arquitectura; los nodos aprobados se añaden a un archivo de registro que lee la herramienta de
aprovisionamiento de la malla. Una pequeña biblioteca compartida aporta la generación del código
corto, la normalización y el código escaneable renderizado en terminal que ambas ceremonias
utilizan. La clave pública de malla merece una precisión: se almacena y se transfiere como una
cadena opaca. Ninguno de los dos servicios realiza un intercambio de claves de malla; el
aprovisionamiento lo lleva a cabo herramienta externa invocada desde scripts de shell, y el
directorio reservado nominalmente para esa herramienta contiene únicamente un README.

## Los roles, y lo que no son

El rol adjunto al registro de usuario de emparejamiento es una cadena simple, no un conjunto tipado
de valores, y la vía de aprobación escribe en él un único valor por defecto fijado en el código. La
base de datos no aplica restricción alguna sobre su contenido. No existe en el código fuente del
componente ninguna implementación de protocolo de saludo del tipo que a veces se asocia a este
diseño — un intercambio de claves al estilo Noise o al estilo de una VPN en malla —; una búsqueda en
todo el árbol no halló ninguna implementación de Noise ni biblioteca correspondiente en ningún punto
del código canónico.

Sí existe un rol de emparejamiento tipado en otro lugar de la plataforma: `PairingRole`, en el
componente de comandos de orquestación (`app-orchestration-command`), un enum de tres valores —
`User` (lectura/escritura, operador diario), `Admin` (acceso completo) e `Interface` (solo
metadatos, para el agregador de orquestación). No es el mismo campo, no reside en este componente y
no incluye un cuarto valor. Las descripciones de cuatro niveles de autorización con nombre
implementados como construcciones de código en este sistema de emparejamiento no están respaldadas
por el código fuente; el modelo independiente de cuatro niveles `PermissionTier` que sí existe
(`P1`–`P4`) se describe en [[personnel-permissions]] y pertenece a otro componente y a otra vía de
datos — los dos enums viven en el mismo crate, pero gobiernan asuntos sin relación entre sí y no
deben confundirse.

El componente ha crecido desde la última vez que se midió: ahora ronda las 870 líneas repartidas
entre sus archivos fuente, no la cifra menor que a veces se cita — aunque su forma (tabla de
peticiones, tabla de usuarios, cinco rutas HTTP, módulo de huella de diez líneas) no ha cambiado.

## La brecha en el transporte

Una limitación honesta corresponde al cuerpo del artículo, no a una nota al pie. El acceso nativo al
host a través de la internet pública discurre actualmente por un túnel SSH con reenvío de puertos
que **no** verifica la identidad del servidor remoto. La propiedad prevista — que el proveedor no
pueda leer los datos del operador en tránsito — no se entrega, por tanto, en ese salto hoy. Pasará a
ser cierta cuando llegue a esa vía un TLS mutuo verificado; hasta entonces, la ceremonia de
emparejamiento autentica el dispositivo ante el servicio, pero el servicio no queda autenticado
criptográficamente ante el dispositivo a través de ese túnel concreto.

## Por qué emparejamiento en lugar de cuentas

De ligar la autoridad a un dispositivo en vez de a una persona se derivan tres propiedades.

**La revocación es exacta.** Eliminar una huella retira el acceso de una sola máquina. Un portátil
comprometido se resuelve sin perturbar los demás dispositivos de esa misma persona ni forzar un
restablecimiento de credenciales en toda la organización. Las copias de software que conserve un
colaborador que se marcha quedan inertes sin material de clave aprobado, y los registros de petición
del flujo de aprobación sirven además como rastro de auditoría de a quién se le concedió qué, y
cuándo.

**La incorporación es observada.** Un dispositivo pasa a ser conocido mediante una decisión de
aprobación tomada por una persona que comparó un código, no mediante un formulario de autoservicio.
No existe vía por la que un dispositivo se dé de alta a sí mismo, y no hay superficie de phishing:
un emparejamiento nunca se teclea, de modo que no se puede engañar a un operador para que lo
introduzca en un formulario falsificado.

**El valor almacenado no es un secreto.** Una huella no revela nada aprovechable. Una brecha de la
base de datos de emparejamientos entrega una lista de qué claves eran de confianza — reconocimiento
útil, pero no credenciales, lo que supone una exposición materialmente distinta de la de un almacén
de contraseñas filtrado. De ahí se sigue una ventaja más discreta y acumulativa: el modelo carece de
toda la liturgia de higiene de credenciales — sin calendarios de rotación, sin políticas de
complejidad, sin contraseñas que caducan y generan restablecimientos en el servicio de asistencia.
Lo que queda es una lista corta e inspeccionable de claves de máquina aprobadas por inquilino, que
es una postura de seguridad que un revisor puede auditar de principio a fin.

## Lo que esto no es

**No hay saludo del Noise Protocol ni intercambio de claves en este componente.** La criptografía
presente es el cálculo de huellas de clave pública SSH; las claves de malla que manejan los
servicios de emparejamiento son cadenas opacas que se pasan a herramienta externa.

**El componente no se llama `service-pairing`.** No existe ningún componente con ese nombre. La
implementación en producción es `system-gateway-mba`, y la ceremonia de incorporación de nodos es,
de nuevo, un servicio aparte.

**El campo de rol no es un nivel aplicado.** Es una cadena sin restricciones con un valor por
defecto fijado en el código en el momento de la aprobación; no es una enumeración tipada ni un nivel
de autorización comprobado. Sí existe un rol tipado de tres valores, pero en otro componente y para
otro propósito, y no es la taxonomía de cuatro niveles que a veces se describe para este.

**La MBA no es autenticación multifactor superpuesta a contraseñas.** No hay contraseña alguna a la
que añadir factores; el modelo sustituye la categoría entera. Tampoco es biométrica: no se mide ni
se almacena nada del cuerpo humano, y la entidad ligada es una máquina, no una persona — lo que
significa también que la MBA por sí sola no indica *qué ser humano* estaba ante el teclado de una
máquina aprobada; la identidad a nivel de personal y su escalonamiento son la capa aparte de
[[personnel-permissions|personal y permisos]].

**El emparejamiento no es una sesión de inicio de sesión.** Establece que un dispositivo es
conocido. Lo que ese dispositivo pueda hacer a continuación lo rige el modelo de permisos descrito
en otro lugar, que se apoya en una fuente de datos enteramente distinta, las reglas direccionales
del [[diode-standard|Estándar del Diodo]] y el [[worm-ledger-design|libro de auditoría de solo
adición]] donde aterriza cada evento de acceso. El emparejamiento es el requisito previo; las reglas
de dirección y el libro mayor son las compuertas.

**Un código de emparejamiento no es una credencial.** Es un valor corto y transcribible por una
persona, procedente de una fuente aleatoria no criptográfica, con sentido únicamente durante la
ventana de aprobación y únicamente junto a una decisión del operador.

**La confidencialidad de transporte de extremo a extremo no se entrega actualmente sobre el túnel de
acceso remoto.** Véase la brecha en el transporte más arriba; esto se enuncia como previsto, no como
logrado.

## Véase también

- [[pairing-as-permission]] — el principio de que el registro de emparejamiento es en sí mismo la autorización
- [[pair-a-new-device]] — el procedimiento del operador para ejecutar la ceremonia
- [[personnel-permissions]] — el modelo de permisos de cuatro niveles y dónde reside realmente
- [[enroll-ppn-node]] — la variante de incorporación de nodos de la misma ceremonia
- [[app-console-keys]] — la interfaz del lado del dispositivo que presenta el código de emparejamiento
- [[capability-based-security]] — el modelo de autoridad por encima de la autenticación de dispositivos
- [[diode-standard]]
- [[ppn-mesh-architecture]]
