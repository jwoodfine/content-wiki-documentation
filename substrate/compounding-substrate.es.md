---
schema: foundry-doc-v1
title: "El sustrato compuesto"
slug: compounding-substrate.es
category: substrate
type: topic
content_type: topic
quality: complete
short_description: "El sustrato compuesto es el patrón arquitectónico que PointSav construye y administra: código de plataforma abierto, una capa de datos determinista que funciona sin IA, y una capa de inteligencia opcional cuya cada interacción genera señal de entrenamiento que se compone a través de todos los despliegues."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-21
editor: pointsav-engineering
paired_with: compounding-substrate.md
---

Una organización que adopta una plataforma de IA hoy alquila la inteligencia. El modelo mejora según el calendario del proveedor. La señal de entrenamiento que genera el trabajo de la propia organización se acumula para el proveedor, y abandonar la plataforma significa empezar de nuevo.

PointSav se construye sobre un patrón distinto — el **sustrato compuesto**. El código de la plataforma es abierto y bifurcable, la capa de datos determinista funciona con cero cómputo de IA, y cada interacción operativa genera señal de entrenamiento que se compone a través de cada despliegue de inquilino.

Un curador — PointSav — incorpora periódicamente la señal acumulada en un modelo base mejorado que regresa a cada despliegue. Los datos del cliente nunca salen de su infraestructura; solo los pesos de los adaptadores y los bloques de caché clave-valor, despojados de los datos de origen, entran en la federación compartida.

Para un comprador regulado la consecuencia es concreta. La capa de IA mejora con cada mes de uso en producción, y no se cede ningún dato más allá de lo que el comprador eligió al incorporarse. El patrón es duradero por una razón estructural: un proveedor de inteligencia alquilada no puede copiarlo sin desmantelar su propio modelo de facturación.

Este artículo nombra las cinco propiedades estructurales del patrón y explica la inversión de la cadena de valor que lo hace duradero.

## Qué es un sustrato compuesto

Un sustrato compuesto es una arquitectura de sustrato de IA con cinco propiedades definitorias.


1. El código del sustrato es abierto y bifurcable.
2. La capa de datos determinista funciona independientemente de cualquier cómputo de IA.
3. La IA se agrega como una capa de inteligencia opcional que cualquier inquilino puede componer dentro o fuera.
4. Cada interacción operativa genera señal de entrenamiento que se compone a través de los despliegues del sustrato.
5. Un curador incorpora periódicamente la señal acumulada en modelos base mejorados que regresan a todos los despliegues sin interrumpir la propiedad de los datos del cliente.


El patrón aplica un modelo ya probado en la infraestructura de código abierto: el código de la plataforma se convierte en un bien común abierto, y el valor económico migra hacia las operaciones, la integración y un mercado federado construido sobre él.

## Las cinco propiedades estructurales

Cada propiedad es un reclamo estructural sobre la plataforma. Cada una nombra también la razón específica por la que un proveedor de inteligencia alquilada no puede replicarla sin desmantelar su propio modelo de negocio.

### Custodia de la pila del cliente

Cada cliente posee su pila completa: datos, cómputo, adaptadores y composición de despliegue. El sustrato — código de plataforma más modelo base — es abierto bajo una licencia permisiva; los datos y los adaptadores entrenados son propiedad intelectual del cliente.

Un proveedor de inteligencia alquilada monetiza el sustrato mismo como un servicio medido. La propiedad del sustrato erosiona el bloqueo sobre el que descansa ese modelo de facturación.

### Capa de inteligencia desacoplada

El anillo de datos y el anillo de procesamiento determinista funcionan por completo sin el anillo de IA. Un cliente, un miembro de la comunidad, un comprador regulado o un sitio aislado puede ejecutar una plataforma de datos PointSav completa con cero cómputo de IA. La IA es valor agregado, no lo básico.

Un proveedor de inteligencia alquilada acopla el cómputo de IA a sus servicios de datos. Desacoplarlos elimina los ingresos por cómputo de IA de cada despliegue que opta por no participar.

### Enrutamiento dinámico de cómputo

[[service-slm]] es la única puerta de control de acceso de la plataforma — el [[compounding-doorman|Doorman]]. Enruta cada solicitud entre tres niveles de cómputo: un modelo local en la máquina del propio cliente, un nivel de ráfaga multi-nube y una API frontera externa. El cliente no elige el nivel; la forma de la solicitud y los topes presupuestarios lo eligen.

Un proveedor de inteligencia alquilada factura cada nivel como una relación separada y no puede abarcar el modelo frontera de un competidor. No puede abstraer este enrutamiento.

### Federación que preserva la privacidad

Los clientes optan por un [[sovereign-ai-commons|mercado federado de adaptadores]] que agrega mejoras sin mover los datos de origen. Los datos propios de cada cliente permanecen en su lugar; solo los pesos de los adaptadores y los bloques de caché clave-valor, sin datos de origen, fluyen hacia la federación. El método de agregación sigue el linaje de investigación de adaptadores federados que preservan la privacidad.

La facturación por inquilino y la postura de cumplimiento de un proveedor de inteligencia alquilada hacen que el agrupamiento cruzado entre inquilinos sea estructuralmente inadmisible. No puede operar una verdadera federación.

### Avance curado del sustrato

Un modelo base abierto fluye hacia una variante de preentrenamiento continuo de PointSav, lanzada como el sustrato para despliegues posteriores. El bien común curado de cada año alimenta el modelo base del año siguiente. Para 2030 se pretende que el modelo base entrenado por la federación sea competitivo con los modelos propietarios de frontera en los dominios de la federación.

Un proveedor de inteligencia alquilada no puede permitir que los datos del cliente entrenen un modelo base que el cliente luego posea. Eso destruye el bloqueo del que dependen sus márgenes.

## La inversión de la cadena de valor

La cadena de valor de la inteligencia alquilada depende de que el cliente permanezca en el sustrato del proveedor. La cadena de valor del sustrato compuesto depende de que el cliente componga su propia pila. Los dos modelos son opuestos; uno no puede adoptar el otro sin desmantelarse.

Un proveedor que copiara la propiedad de propiedad del sustrato erosionaría su propio bloqueo. Un proveedor que copiara la propiedad de inteligencia opcional perdería ingresos por cómputo de IA en cada despliegue que optara por no participar. Un proveedor que copiara la propiedad de composición federada violaría sus propios contratos de cumplimiento por inquilino.

Esta asimetría es lo que hace duradero al patrón.

## El papel de PointSav — administrador, no proveedor

PointSav no es un proveedor del sustrato ni un portero hacia él. Es el administrador.

- **Administrador del protocolo** — gobierna la especificación del Doorman y ejecuta el proceso de convención que la versiona.
- **Administrador del modelo base** — publica la variante de preentrenamiento continuo y contribuye aguas arriba cuando es relevante.
- **Administrador del mercado** — opera el grupo federado de adaptadores.
- **Operador de registro** — vende dispositivos, integración y soporte.
- **Cliente de referencia** — el entorno de desarrollo de PointSav y MCorp son prueba de que el patrón funciona.

El sustrato es un bien común abierto; el valor migra hacia las operaciones, la integración y el mercado de adaptadores.

## El bucle compuesto

Cada acción produce datos; los datos producen conocimiento estructurado; el conocimiento mejora las acciones futuras. El bucle se ejecuta continuamente, en cada despliegue de inquilino, federado a través de los bienes comunes.

Para un operador que evalúa la plataforma, la consecuencia es medible: cada mes de uso en producción hace que la capa de IA sea materialmente mejor, sin inversión ni intercambio de datos más allá de lo que el operador eligió al incorporarse.

```
operador + asistente hace el trabajo
  ↓ produce
commits de git + ediciones de archivos + registros de sesión + turnos de conversación
  ↓ ingerido por
service-fs[inquilino] ← registro WORM
  ↓ analizado por
service-extraction[inquilino] ← determinista
  ↓ escribe estructurado en
service-content[inquilino] ← grafo de conocimiento
  ↓ indexado por
service-search[inquilino] ← índice de texto completo
  ↓ consultado por (cuando la IA está activa)
service-slm ← Doorman; enruta entre 3 niveles de cómputo
  ↓ entrena (periódicamente)
adaptadores LoRA ← paquetes de habilidades por inquilino
  ↓ contribuye (con opción de participar, federado)
grupo federado de adaptadores ← beneficio común
  ↓ se incorpora a (anualmente)
preentrenamiento continuo del modelo base ← curado por PointSav
  ↓ se envía en
actualización del dispositivo ← cada cliente se beneficia
  ↓ usado por
operador + asistente en la siguiente sesión ← el bucle se cierra, compuesto
```

## Trayectoria operativa

La trayectoria descrita a continuación es `planeada` e `intencionada`, enmarcada según el [[disclosure-substrate|lenguaje de divulgación continua]] de `[ni-51-102]` y la disciplina prospectiva de `[osc-sn-51-721]`. La forma arquitectónica está establecida; la capacidad operativa madura con el tiempo.

Para 2030, el sustrato compuesto pretende producir:

- un modelo base competitivo con los modelos de frontera en tareas reguladas de pequeñas empresas;
- una federación de más de cien clientes, cada uno poseyendo su pila completa;
- una pila de protocolos versionada dos veces a través del proceso de convención y validada en producción;
- una posición de mercado en la que los sectores regulados de pequeñas empresas — clínicas, firmas de abogados medianas, asesores financieros regionales, operadores inmobiliarios — se han estandarizado en el patrón porque su postura de cumplimiento lo requiere.

El patrón no pretende desplazar por volumen a los grandes proveedores de IA en la nube. Apunta al mercado regulado de pequeñas empresas que la IA en la nube medida no puede alcanzar económicamente.

## Véase también

- [[apprenticeship-substrate]]
- [[3-layer-stack]]
- [[worm-ledger-architecture]]
- [[sovereign-ai-routing]]
- [[language-protocol-substrate]]
