---
schema: foundry-doc-v1
title: "Personal y permisos"
slug: personnel-permissions
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
short_description: "Cuatro niveles de permisos, de P1 a P4, implementados como una enumeración tipada y servidos a través de un endpoint HTTP que lee un archivo de configuración del espacio de trabajo. Ese archivo no declara hoy ningún colaborador, de modo que el endpoint no resuelve nada para ningún usuario real."
paired_with: personnel-permissions.md
---

**Un nivel de permisos** es un grado de autoridad con nombre asignado a un colaborador, que determina
en qué archivos de trabajo puede trabajar y qué operaciones privilegiadas puede ejecutar. Esta
plataforma define cuatro — de P1 a P4 — implementados como una enumeración tipada en el componente de
mando de orquestación, servidos a través de un endpoint HTTP y derivados de un archivo de
configuración del espacio de trabajo, no de una base de datos de usuarios.

La decisión de diseño que conviene notar es a *qué* está atado el nivel. No hay tabla de cuentas, ni
asignación de roles por servicio, ni pertenencia a grupos. La autoridad de un colaborador está
pensada como una propiedad de un archivo de configuración que describe con qué archivos de trabajo
está emparejado, y el nivel se deriva de ese emparejamiento — el permiso como consecuencia del
emparejamiento y no como una concesión aparte. Ese diseño es código real hoy; si actualmente gobierna
a alguien es una cuestión distinta, que este artículo responde con precisión más abajo.

## Los cuatro niveles

La enumeración es tipada y no una cadena libre, y sus variantes llevan documentación que enuncia
directamente el alcance de cada nivel:

- **P1 — System Administrator (administrador del sistema).** Acceso completo al espacio de trabajo.
- **P2 — Package Manager (gestor de paquetes).** Archivos de trabajo concretos, más la autoridad para
  ejecutar el paso de promoción canónica.
- **P3 — User (usuario).** Solo archivos de trabajo concretos; sin emparejamiento en la capa de
  mando.
- **P4 — Interface (interfaz).** Solo superficie de API de lectura.

El orden es una jerarquía real de radio de impacto, no de antigüedad. La frontera significativa está
entre P2 y P3: P2 puede mover trabajo al repositorio canónico, que es el punto en el que un cambio se
vuelve visible desde fuera e irreversible en la práctica. P3 puede hacer commit libremente dentro de
sus propios archivos de trabajo, sin ese alcance. P4 no puede escribir en absoluto.

## Cómo se resuelve un nivel

La ruta de resolución es corta y está gobernada íntegramente por un archivo.

Un módulo de personal lee un archivo de configuración del espacio de trabajo — el `pairings.yaml` de
la raíz del espacio de trabajo — buscando una clave `contributors` de primer nivel. Cada entrada ahí
aportaría un nombre de usuario del sistema operativo, una cadena de nivel y una lista de archivos de
trabajo emparejados. El módulo convierte esa forma en bruto en un registro interno de tres campos y
convierte la cadena de nivel en la enumeración tipada; un nivel no reconocido o ausente cae de vuelta
a P3, el más restrictivo de los dos niveles acotados a archivos de trabajo.

Una única ruta, `GET /v1/personnel/{user}`, devuelve el registro resultante como JSON o un error de
no encontrado. Ese endpoint es la respuesta prevista de la plataforma a la pregunta «qué se le permite
hacer a este colaborador».

### El registro son tres campos

El registro lleva un nombre de usuario del sistema operativo, un nivel y el conjunto de archivos de
trabajo emparejados. Eso es todo. **No** lleva un nombre para mostrar, ni una cadena de rol, ni una
clave pública SSH. El material de clave se gestiona por separado en el almacén de identidades del
espacio de trabajo, donde cada identidad tiene su propio directorio y su clave de firma con permisos
restrictivos. Describir un único registro de personal unificado que contuviera nombre, rol, clave y
nivel a la vez tergiversaría el modelo de datos: el almacén de identidades y el registro de nivel son
sistemas separados, unidos únicamente por la convención del nombre de usuario.

## Hoy el archivo de configuración no declara ningún colaborador

La clave `contributors` es opcional para el analizador, de modo que un archivo que carezca de ella por
completo se carga igualmente sin error y produce un conjunto vacío de colaboradores. El
`pairings.yaml` real del espacio de trabajo se leyó directamente para este artículo: contiene una
lista `pairings:` de entradas de topología de archivos de trabajo (nombre del clúster, ID de módulo,
rama, nivel de autoservicio) y **no lleva ninguna clave `contributors:` en ninguna parte**.

La consecuencia es exacta y merece enunciarse sin eufemismos: hoy el endpoint de personal devolvería
no encontrado para todo usuario real. Ningún colaborador tiene actualmente un nivel resuelto por esta
vía. La enumeración, el analizador, el endpoint y su comportamiento de reserva son todos reales, están
construidos y han sido verificados de forma independiente contra la fuente canónica — pero los datos
que darían a todo ello un efecto práctico para un operador real no se han poblado en el archivo que
lee. Es un caso de código construido y correcto situado frente a datos sin poblar, no un caso de una
funcionalidad ficticia — una distinción que importa a cualquiera que evalúe la postura de control de
acceso de esta plataforma, porque la descripción honesta no es ni «no implementado» ni «gobierna hoy
el acceso por completo».

Una advertencia histórica acompaña a lo anterior, porque el propio historial de verificación de este
artículo ha estado en ambos lados de ella. Una revisión anterior de este asunto concluyó que el modelo
P1–P4 describía un sistema que no existía en absoluto — una conclusión apoyada en una búsqueda acotada
a un solo componente y un solo archivo de configuración. Una búsqueda más amplia localizó la
implementación real descrita arriba, y aquel hallazgo anterior fue retractado. La lección permanente
es de procedimiento: una búsqueda acotada a un solo componente no es prueba suficiente de que algo no
exista en ninguna parte del monorepo, y la misma cautela se aplica al hallazgo de esta sección — el
archivo se leyó directamente, íntegro, para este borrador, en lugar de inferirse de su ausencia en una
búsqueda más estrecha.

## Por qué un archivo de configuración y no una base de datos

La decisión de derivar la autoridad de un archivo de configuración versionado en lugar de una tabla de
usuarios tiene consecuencias en ambos sentidos, y conviene nombrarlas.

A su favor: el archivo está bajo control de versiones, de modo que un cambio de autoridad es un commit
con autor, marca de tiempo y firma, revisable en el historial como cualquier otro cambio. No hay una
interfaz administrativa aparte que asegurar, ni sesión que secuestrar, ni ruta de escritura en vivo
por la que un nivel pudiera escalarse en tiempo de ejecución. El mismo archivo lleva además la
topología de archivos de trabajo y las concesiones de autoservicio por archivo, de modo que la
descripción de quién puede trabajar dónde y la descripción de qué puede hacer cada archivo de trabajo
residen en un único lugar auditable.

En su contra: el archivo es el control entero. Cualquiera capaz de hacer commit de un cambio en él, y
de llevar ese cambio a la máquina que sirve el endpoint, cambia la respuesta. No hay segundo factor ni
paso de aprobación específico para los cambios de autoridad — la protección es el mismo control de
commit y de promoción que protege cualquier otro archivo, descrito en
[[five-stage-supply-chain|la cadena de suministro de cinco etapas]]. El comportamiento de reserva del
analizador se eligió con eso en mente: un nivel no reconocido o ausente se resuelve como P3, de modo
que una entrada malformada concede menos, no más.

## Qué gobierna realmente el acceso hoy

Dado que el endpoint de niveles no tiene datos detrás, conviene ser explícito sobre qué sí acota en la
práctica la autoridad de los colaboradores, porque la respuesta no es este componente.

La autoridad la imponen los mecanismos descritos en
[[five-stage-supply-chain|la cadena de suministro de cinco etapas]] y en
[[pre-commit-defense-in-depth|la defensa en profundidad previa al commit]]: la posesión de la clave de
acceso del remoto canónico, que solo tiene una sesión privilegiada; una comprobación de alcance dentro
del script de promoción que confirma que la sesión tiene derecho a promover; un permiso de autoservicio
registrado por archivo de trabajo en el mismo archivo de configuración, que determina si un archivo
puede empujar su propia rama a los espejos de staging; y una comprobación del mensaje de commit que
restringe la identidad del autor. Estos son controles reales y activos. El modelo de niveles es la
descripción declarativa de esa misma intención, hoy por delante de sus datos.

## Lo que esto no es

**Ningún colaborador tiene hoy un nivel asignado por esta vía.** El archivo de configuración no declara
colaboradores, de modo que el endpoint no resuelve nada. La implementación existe; la población de
datos, no.

**Un registro de personal no es un registro de identidad.** Contiene un nombre de usuario, un nivel y
los archivos de trabajo emparejados. Los nombres, los roles y las claves viven en otro sitio, y ningún
código los une en un solo objeto.

**Los niveles no los impone el componente de niveles.** La enumeración y el endpoint describen
autoridad; no acotan ninguna operación. El rechazo ocurre en el script de promoción, en los hooks de
commit y en quién tiene cada clave de acceso.

**Este no es el sistema de emparejamiento descrito en
[[machine-based-auth|la autorización basada en máquina]].** Aquel componente vincula una clave de
dispositivo a un registro de usuario y lleva una cadena de rol sin restricciones con un valor por
defecto codificado. Es un componente distinto, un modelo de datos distinto, y no un nivel P1–P4. En el
componente de orquestación existe además un rol de emparejamiento de tres valores — usuario,
administrador, interfaz — que tampoco es esta enumeración.

**Un nivel no es una cuenta.** No hay inicio de sesión, ni sesión, ni credencial asociada a él. Es una
declaración leída de un archivo, y su integridad depende enteramente de la integridad de ese archivo y
del proceso que lo edita.

## Véase también

- [[app-orchestration-command-branch-model]] — el componente que aloja el modelo de niveles y el endpoint
- [[contributor-model]] — el esquema de contribución que describen los niveles
- [[pairing-as-permission]] — el principio de que la autoridad la confiere el emparejamiento, no una concesión de rol
- [[machine-based-auth]] — autorización a nivel de dispositivo, un mecanismo aparte
- [[five-stage-supply-chain]] — donde se impone realmente la autoridad de promoción
- [[identity-ledger-schema-design]]
- [[scale-user-tiers]] — cómo se prevé que la asignación de niveles escale con el número de colaboradores
