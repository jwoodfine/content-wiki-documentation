---
schema: foundry-doc-v1
title: "Cadena de suministro de cinco etapas"
slug: five-stage-supply-chain
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
last_edited: 2026-08-06
editor: pointsav-engineering
short_description: "El camino que va del commit de un colaborador al despliegue de un cliente atraviesa tres niveles de repositorio y dos organizaciones, controlado por un script de promoción fuertemente resguardado. No hay solicitud de extracción (pull request) ni revisión por un segundo interviniente."
paired_with: five-stage-supply-chain.md
---

**La cadena de suministro** es el camino que recorre un cambio desde la máquina donde se escribió
hasta el despliegue donde se ejecuta, junto con los controles aplicados en cada traspaso. Su valor
de seguridad procede de los traspasos mismos: cada frontera es un lugar donde un cambio puede
inspeccionarse, filtrarse o rechazarse, y donde queda registrada la identidad de lo que la cruzó. La
cadena de esta plataforma atraviesa tres niveles de repositorio en manos de dos organizaciones y una
capa intermedia de espejos, con el control sustantivo concentrado en un único script de promoción.
Aquí se describe como cinco etapas — una descripción del camino que este artículo organiza para
mayor claridad, no la cita de un marco preexistente con nombre propio (más abajo se explica por qué
importa la distinción).

Dos hechos estructurales condicionan todo lo demás. Primero, colaboradores y clientes nunca
comparten repositorio: un colaborador escribe en un espejo de staging personal y un cliente lee del
catálogo de otra organización distinta, con el repositorio del proveedor entre ambos. Segundo, los
controles automatizados son filtros de contenido y de forma, no revisión humana.

## Las cinco etapas

| Etapa | Actor | Acción actual |
|---|---|---|
| 1 — Respaldo | Colaborador | Envía el trabajo en curso a un espejo de staging personal |
| 2 — Oferta | Colaborador → Proveedor | Confirma mediante el asistente de commit del espacio de trabajo, directamente visible para el administrador |
| 3 — Auditoría | Administrador del proveedor | La herramienta de promoción reproduce los commits verificados sobre la rama canónica y los envía |
| 4 — Transferencia | Proveedor → Cliente | La propagación de gobernanza replica el estado verificado a la organización cliente |
| 5 — Despliegue | Cliente → Producción | Extracción solo de avance rápido sobre los hosts de producción |
| (Bucle) — Reinicio | Proveedor → Colaborador | Se obtiene el canónico y se rebasa sobre él el trabajo del siguiente ciclo |

**Etapa 1 — Respaldo.** El colaborador envía el trabajo en curso a su propio espejo de staging. Es
una red de seguridad privada; nada del registro canónico del proveedor se ve afectado.

**Etapa 2 — Oferta.** Hoy, la oferta *es* el commit: no existe paso de solicitud de extracción ni
compuerta de revisión en las herramientas actuales. El asistente de commit del espacio de trabajo
produce el commit en la rama de trabajo con una identidad de colaborador verificada como autor, una
firma SSH y tráileres identificativos, y ese trabajo confirmado queda directamente visible para el
administrador del proveedor una vez enviado a staging.

**Etapa 3 — Auditoría.** El script de promoción del proveedor lleva el trabajo verificado a la rama
canónica. No fusiona en el sentido habitual: para una rama de trabajo, extrae una rama temporal a
partir de la cabeza canónica y reproduce sobre ella cada commit que cualifica, uno a uno, filtrando
las rutas de estado de sesión e internas del espacio de trabajo, de modo que solo llegue al registro
canónico código revisable.

**Etapa 4 — Transferencia.** Un paso independiente de propagación de gobernanza replica la versión
verificada desde la organización proveedora al catálogo de despliegue de la organización cliente. El
cliente recibe estado terminado y verificado, y nunca ve commits de colaborador en tránsito.

**Etapa 5 — Despliegue.** El cliente extrae el estado verificado sobre los hosts de producción bajo
una restricción de solo avance rápido, de modo que producción no pueda divergir en silencio del
propio catálogo del cliente.

**El bucle.** El colaborador obtiene el resultado canónico y rebasa sobre él el trabajo del
siguiente ciclo, de modo que cada participante comienza cada ciclo desde el mismo punto verificado
en lugar de construir durante semanas sobre una rama divergente.

## Niveles de repositorio y la separación de doble ciego

Existen tres niveles de contenido, y el flujo entre ellos es unidireccional por diseño.

**Fuente.** La organización proveedora custodia los repositorios canónicos — la copia autoritativa
del código y el único nivel sobre el que escribe una promoción.

**Catálogo.** La organización cliente custodia el catálogo de despliegue — las descripciones
empaquetadas y versionadas a partir de las cuales se aprovisiona una instancia. El contenido llega a
él por el paso independiente de propagación de gobernanza nombrado arriba como Etapa 4.

**Instancias.** Los despliegues aprovisionados viven enteramente fuera del control de versiones, son
locales a la máquina que los ejecuta y están excluidos de todos los repositorios.

Junto a estos niveles existen dos cuentas personales de staging usadas exclusivamente como espejos.
Cada clon de trabajo lleva tres remotos: el repositorio canónico, alcanzado mediante un alias de
acceso administrativo, y un espejo de staging por identidad de colaborador. El trabajo se envía
libremente a los espejos de staging; solo el script de promoción escribe en el remoto canónico, y
únicamente desde una sesión que posea la clave canónica.

Esta disposición produce la propiedad de seguridad que define la cadena: quién no puede ver a quién.
Un colaborador que envía a su propio espejo no tiene ninguna vía hacia el catálogo del cliente, y un
cliente que lee el catálogo no tiene visibilidad del espejo — ninguno puede observar la actividad
del otro a través de los repositorios a los que llega, y el proveedor es la única parte con
visibilidad de ambos extremos. Esto escala con el número de colaboradores: añadir colaboradores
añade actividad de las etapas 1 y 2, no nuevas vías hacia el entorno del cliente.

## Confirmar cambios

Todo commit se crea a través de un único script asistente en lugar de invocar Git directamente — una
regla aplicada por la compuerta de tiempo de commit descrita en [[pre-commit-defense-in-depth]].

El asistente alterna entre dos identidades de colaborador en cada commit, mediante un archivo de
conmutación bajo el almacén de identidades protegido por un bloqueo de archivo, de modo que las
sesiones concurrentes no puedan competir por él; la conmutación se escribe de forma atómica, con un
archivo temporal y un renombrado. Firma cada commit con la clave SSH propia de esa identidad y
repara en el primer uso la configuración de verificación de firmas del repositorio local, para que
la inspección posterior del historial verifique sin configuración adicional. Añade tres tráileres
que registran el archivo, el motor y la sesión; los fallos de detección degradan a un valor
«unknown» en lugar de bloquear el commit.

El asistente no prepara archivos ni envía nada. Ambas cosas son deliberadas: la preparación es
explícita para que ningún cambio se arrastre de forma involuntaria, y el envío es una decisión
aparte que se toma más tarde.

## Promoción al canónico

El script de promoción es donde reside el control real de la cadena, y buena parte de su extensión
es código de guarda. Para una rama de trabajo reproduce individualmente cada commit que cualifica
sobre una rama temporal tomada de la cabeza canónica, tratando los commits de fusión contra su
primer padre, regenerando el archivo de bloqueo de dependencias cuando ese es el único conflicto y
deteniéndose para resolución manual ante un conflicto de código genuino. Para los repositorios
administrativos realiza únicamente un envío de avance rápido, tras confirmar que la cabeza canónica
es antecesora de la cabeza local.

Los archivos de estado de sesión nunca cruzan: un filtro identifica el directorio de estado del
agente, los archivos de instrucciones del motor, la configuración de sesión, los archivos de notas
de trabajo y de registro de cambios, y los directorios de staging, los elimina de cualquier commit
que aterrice durante la promoción, y una compuerta final vuelve a revisar el árbol a punto de
enviarse y rechaza de plano si alguna de esas rutas ha sobrevivido.

Las guardas restantes, cada una de las cuales puede detener una promoción: un directorio de bloqueo
que impide ejecuciones concurrentes; una comprobación de alcance que confirma que la sesión está
autorizada a promover; una compuerta de formato, análisis estático y pruebas; una comprobación de
remotos requeridos; una comprobación de correspondencia de rama; una comprobación de árbol de
trabajo limpio; una comprobación de sincronización con el espejo de staging; una comprobación de
avance rápido posible que bloquea la divergencia real; un filtro de rutas de datos de negocio que
termina la ejecución sin autocertificarse; una guarda de eliminación masiva por encima de un
umbral configurado; una guarda de reversión silenciosa por encima del mismo umbral para contenido
revertido discretamente a un estado canónico anterior; una comprobación de patrones de contenido en busca de
nombres de entidades reales en el repositorio de diseño; una lista blanca de rutas de primer nivel
para el repositorio canónico; confirmación interactiva forzada para los repositorios visibles
públicamente incluso en modo no interactivo; y una petición final de confirmación. Las excepciones
de eliminación y de reversión quedan a su vez registradas en un archivo de omisiones.

Los archivos a los que se ha concedido permiso de autoservicio pueden, en su lugar, enviar su propia
rama a los espejos de staging y añadir un registro a un archivo de cola de promoción, lo que antepone
una notificación en la bandeja de entrada de la sesión coordinadora. Ese script nunca escribe en el
remoto canónico — es una cola de trabajo asíncrona para una ejecución de promoción privilegiada
posterior, no una promoción en sí misma.

## Lo que la cadena no incluye

En esta canalización no hay solicitud de extracción en ningún punto. Una búsqueda en todo el árbol
del código canónico y de los scripts del espacio de trabajo, en busca de clientes de API de forjas de
código, de órdenes de creación y fusión de solicitudes de extracción y de herramientas de revisión,
devolvió coincidencias únicamente dentro de la configuración de integración continua original de
proyectos de terceros incorporados — ninguna perteneciente a esta plataforma.

La consecuencia es que la transferencia de propiedad en la frontera del proveedor se consuma
mediante un único commit reproducido bajo las guardas del script de promoción, no mediante una
solicitud de extracción revisada y aplastada. El resultado — que el cambio pase a formar parte del
historial canónico del proveedor, con la propiedad transfiriéndose a PointSav Digital Systems — es
el mismo en ambos casos; el mecanismo no lo es, y describirlo como una fusión con revisión previa
tergiversaría qué es lo que protege esa frontera.

## Lo que esto no es

**Esto no es una secuencia de cinco etapas definida por la documentación propia de la plataforma.**
Una búsqueda en todos los documentos de gobernanza de primer nivel y en el directorio de convenciones
no halló ninguna definición de una «Etapa 1» a «Etapa 4» como término establecido y referenciado.
Existen exactamente dos etapas numeradas nombradas en el material existente: un paso de propagación
de gobernanza hacia el catálogo del cliente, y el paso de promoción al canónico. El encuadre en
cinco partes de arriba es la organización descriptiva propia de este artículo sobre los pasos reales
de la canalización, no la cita de un término canónico preexistente.

**No hay solicitud de extracción ni compuerta de revisión de código.** El único paso humano de la
promoción es una petición de confirmación respondida por el operador que ejecuta el script — la
misma parte que realiza la promoción. Ningún segundo interviniente aprueba un cambio antes de que
llegue al canónico.

**La promoción no es una fusión aplastada.** Para las ramas de trabajo es una reproducción commit a
commit sobre una rama tomada de la cabeza canónica; para los repositorios administrativos es un
envío de avance rápido. El administrador no colapsa el historial de commits del colaborador.

**Las guardas son filtros de forma, no criterio.** Comparan rutas, cuentan archivos eliminados y
detectan contenido revertido. No evalúan si un cambio es correcto, seguro o deseable.

**Tres niveles no son tres organizaciones.** Dos organizaciones custodian repositorios; el tercer
nivel son instancias de despliegue locales y no versionadas. Los espejos de staging son cuentas
personales, no organizaciones.

**La cadena no es el plano de datos de la plataforma.** Los datos del cliente nunca recorren este
camino en ninguna dirección — sus protecciones son las capas de [[cryptographic-ledgers|libro
mayor]] y de [[machine-based-auth|autorización]], no la cadena de suministro.

## Véase también

- [[pre-commit-defense-in-depth]] — las comprobaciones de tiempo de commit que preceden a toda promoción
- [[contributor-model]] — el esquema de contribución con dos identidades y su razón de ser
- [[registry-driven-releases]] — cómo un cambio promovido se convierte en una versión publicada
- [[legal-and-ip-structure]] — el acuerdo de propiedad que implementa la frontera del proveedor
- [[software-distribution-substrate]] — cómo llegan los artefactos publicados a los clientes
- [[authenticate-binary-downloads]] — la verificación disponible para quien recibe un artefacto compilado
- [[machine-based-auth]]
