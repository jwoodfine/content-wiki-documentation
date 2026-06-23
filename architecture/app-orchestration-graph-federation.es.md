---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: app-orchestration-graph-federation
title: "Federación de DataGraph: de app-orchestration-slm a app-orchestration-graph"
short_description: "Cómo la plataforma PointSav federa los DataGraphs soberanos de cada archivo a través de una única puerta de enlace auditable, y las condiciones bajo las cuales esa puerta pasa a ser un servicio dedicado."
audience: vendor-public
bcsc_class: current-fact
language: es
paired_with: app-orchestration-graph-federation.md
category: architecture
status: active
quality: complete
last_edited: 2026-06-23
---

# Federación de DataGraph: de app-orchestration-slm a app-orchestration-graph

Cada archivo Totebox en la plataforma PointSav mantiene un DataGraph soberano: un
grafo de entidades, relaciones y metadatos del corpus específicos a su dominio
operacional. El archivo GIS alberga entidades geográficas y relaciones espaciales.
El archivo editorial alberga entidades de contenido y grafos de autoría. Estos
DataGraphs no se fusionan. No se replican. Cada uno es autoritativo en su propio
dominio e inaccesible para cualquier otro archivo por defecto.

Esta soberanía es un invariante de diseño, no una limitación. La geometría de
capacidades de la plataforma hace imposible el acceso al DataGraph entre archivos
salvo a través de un único camino auditable: la puerta de enlace de federación de
DataGraph.

## Cómo funciona la federación hoy

En la plataforma actual (desde la Fase 2 de os-orchestration), la federación de
DataGraph es gestionada por `app-orchestration-slm` mediante `POST /v1/graph/federated`.
Cuando un proceso descendente requiere una consulta de entidades entre archivos,
la solicitud llega al intermediario. El intermediario llama a
`FleetRegistry.list_full()` — que devuelve todos los miembros de la flota Totebox
registrados con su `doorman_endpoint` completo — y distribuye la consulta a cada
miembro de forma concurrente. Cada Doorman Totebox consulta su propio DataGraph de
`service-content` y devuelve el resultado. El intermediario agrega las respuestas
`FederatedGraphEntry` y devuelve un `FederatedGraphResponse`.

Este diseño tiene tres propiedades:

**Consulta bajo demanda.** El intermediario no mantiene estado del DataGraph. Consulta
los Toteboxes cuando se le solicita, agrega en memoria y descarta. Nada se almacena
en caché entre solicitudes. Esto preserva la soberanía: si el DataGraph de un archivo
se actualiza, la siguiente consulta federada devuelve datos frescos sin ningún paso
de sincronización.

**Solo invocado por el operador.** El endpoint de federación no se llama automáticamente.
Requiere un POST explícito de un llamante autorizado. Ningún proceso en segundo plano
en os-orchestration barre los DataGraphs de los Toteboxes. Esto es intencional: las
lecturas no solicitadas desde un archivo soberano requerirían un permiso de acceso
permanente entre archivos, que la arquitectura no permite.

**Protegido por autenticación.** Cada Doorman Totebox valida la consulta entrante
según sus reglas de capacidad locales antes de exponer datos del DataGraph. El
intermediario no puede extraer datos que el Totebox no haya autorizado para acceso
entre archivos.

## Por qué app-orchestration-slm alberga la federación ahora

`app-orchestration-slm` es el intermediario de inferencia — su función principal es
enrutar solicitudes de inferencia de los Doormen de Nivel 0 al nivel de cómputo
adecuado. La federación está colocada junto a la inferencia por una razón sencilla:
en una flota pequeña, la acción del operador que desencadena una tarea de inferencia
federada (inyectar contexto entre archivos en un prompt) también necesita el resultado
del DataGraph federado para construir ese contexto. Mantener ambos en un mismo proceso
evita un salto de red adicional.

Esta colocación es correcta con flotas de 2 a 10 Toteboxes. A esta escala, las
consultas de distribución al DataGraph son infrecuentes en comparación con las
solicitudes de inferencia, el coste de conexión es trivial y la lógica de agregación
es lo bastante sencilla como para mantenerse inline.

## Cuándo se hace necesaria la separación

Tres condiciones indican que la federación de DataGraph debería extraerse en un
servicio dedicado `app-orchestration-graph`:

**Independencia de carga de trabajo.** Cuando las consultas al DataGraph llegan a
tasas, volúmenes o presupuestos de latencia sustancialmente diferentes de las
solicitudes de inferencia, ambas cargas compiten por recursos dentro del mismo proceso.
Una distribución federada lenta (esperando a 15 Toteboxes) bloquea el enrutamiento
de inferencia; una ráfaga de solicitudes de inferencia se encola detrás de la
agregación de federación. La extracción elimina este acoplamiento.

**Múltiples consumidores.** Mientras solo el camino de inferencia necesite acceso
al DataGraph entre archivos, la colocación es defendible. Si surge un segundo
consumidor — un pipeline de informes, una superficie de búsqueda entre archivos,
o un coordinador de programación de entrenamiento que necesite recuentos de entidades
en todos los archivos — la lógica de distribución no debería duplicarse. Un servicio
dedicado con una API estable sirve a todos los consumidores.

**Requisitos del pool de conexiones.** `app-orchestration-graph` mantendría conexiones
HTTP persistentes con el endpoint `service-content` de cada Totebox registrado. Para
una flota de más de 20 Toteboxes, este pool de conexiones es un recurso no trivial.
Gestionarlo dentro de `app-orchestration-slm` — diseñado para ser un proceso de
enrutamiento sin estado — introduce una complejidad operacional que un servicio
dedicado maneja de forma natural.

El umbral de activación previsto es aproximadamente 10 archivos Totebox activos con
DataGraphs no triviales, o la aparición de un segundo consumidor.

## Lo que app-orchestration-graph está previsto que asuma

Cuando se extraiga, `app-orchestration-graph` está previsto que asuma:

- El endpoint `POST /v1/graph/federated` y toda la lógica de distribución (transferido
  desde `app-orchestration-slm`)
- Un pool de conexiones persistente a todos los endpoints `service-content` de los
  Toteboxes registrados
- Tolerancia a fallos parciales: un DataGraph Totebox inaccesible devuelve una
  bandera `partial: true` en la respuesta, y los resultados restantes se devuelven
  en lugar de fallar toda la consulta
- Normalización de resultados: los resultados de entidades entre archivos usarían
  un formato canónico común independientemente de las variaciones de esquema del
  DataGraph por archivo
- Caché de resultados (TTL corto, configurable por tipo de consulta): la federación
  es costosa a escala; una caché de 30 segundos sobre consultas de entidades estables
  está prevista para evitar distribuciones redundantes

Puerto planificado: `:9181` (`:9180` corresponde a `app-orchestration-slm`).

## Lo que app-orchestration-graph NO asumirá

`app-orchestration-graph` no mantendrá datos de entidades, no replicará DataGraphs
y no enviará nada a los Toteboxes. Es una puerta de enlace de solo lectura. La
fuente de verdad de cada entidad permanece en la instancia de `service-content` del
Totebox que la generó.

El nombre `app-orchestration-content` fue considerado y explícitamente descartado.
Introduciría confusión con `service-content` — el almacén DataGraph por Totebox.
La denominación de grafo (`app-orchestration-graph`) señala la función (puerta de
enlace de federación de grafos) sin implicar propiedad de datos.

## Relación con la arquitectura de separación de niveles

`app-orchestration-graph` es una consideración de la Fase 3 o posterior en la
arquitectura de separación de niveles SLM. Las implantaciones de la Fase 1 y la
Fase 2 — que utilizan el endpoint `POST /v1/graph/federated` integrado en
`app-orchestration-slm` — permanecen en funcionamiento a lo largo de todo el proceso.
El directorio reservado existe para capturar la intención arquitectónica y evitar que
el diseño se pierda a medida que la flota crece de forma incremental.

Cuando la extracción se lleve a cabo, la transición está prevista para ser aditiva:
desplegar `app-orchestration-graph` junto a `app-orchestration-slm`, migrar el
endpoint de grafo federado, verificar la paridad y luego eliminar el endpoint de
`app-orchestration-slm`. No se requieren cambios en ningún archivo Totebox — el
destino de la distribución cambia en la capa del intermediario, de forma invisible
para los archivos individuales.
