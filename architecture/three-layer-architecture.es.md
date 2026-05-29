---
schema: foundry-doc-v1
title: "La arquitectura de tres capas — Software, escaparate, instancias"
slug: three-layer-architecture
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: three-layer-architecture.md
short_description: "Los entregables de PointSav se mueven a través de tres capas arquitectónicas — SOFTWARE (monorepo del proveedor), ESCAPARATE (catálogo de implementación del cliente) e INSTANCIAS (implementaciones en ejecución privadas) — con un flujo estrictamente unidireccional del proveedor al cliente al operador que separa la demostración pública de la realidad operacional."
cites: []
---

Los entregables de [[pointsav-overview|PointSav]] se mueven a través de tres capas arquitectónicas, cada una con un propósito distinto, una audiencia distinta y una postura de propiedad distinta. La primera capa es el monorepo del proveedor — el hogar canónico de cada línea de código de la familia. La segunda es el catálogo público del cliente de patrones de implementación — guías operacionales y manifiestos que muestran cómo se usa el sustrato del proveedor en la práctica. La tercera es la capa privada de implementaciones en ejecución reales, local al operador y nunca comprometida en ningún repositorio compartido.

## Las tres capas

| Capa | Nombre | Vive en | Visibilidad | Propietario |
|---|---|---|---|---|
| 1 | SOFTWARE | `pointsav/pointsav-monorepo` | Público | [[pointsav-overview|PointSav Digital Systems]] (proveedor) |
| 2 | ESCAPARATE | `woodfine/woodfine-fleet-deployment` | Público | Woodfine Management Corp. (catálogo de referencia del cliente) |
| 3 | INSTANCIAS | Almacenamiento local en hardware del operador | Privado — no rastreado en ningún repositorio compartido | Cada operador individual |

La direccionalidad es estricta: el proveedor construye → el cliente adopta → los operadores implementan. No hay camino inverso. Los ajustes del lado del cliente no fluyen de vuelta al monorepo del proveedor. Las configuraciones específicas del operador no fluyen de vuelta al catálogo del cliente.

## Capa 1 — SOFTWARE

El monorepo del proveedor es el hogar canónico de cada línea de código de la familia [[pointsav-overview|PointSav]]. Todos los sistemas operativos [[os-family-overview|`os-*`]], todas las superficies de usuario `app-*`, todos los daemons `service-*` y todos los crates de infraestructura `system-*` viven aquí.

| Propiedad | Valor |
|---|---|
| Repositorio | `github.com/pointsav/pointsav-monorepo` |
| Diseño | [[six-tier-sovereignty-matrix|Matriz de seis niveles de soberanía]] (`app-*`, `asset-*`, `moonshot-*`, `os-*`, `service-*`, `system-*`) |
| Acceso de escritura | Solo `ps-administrator` |
| Acceso de lectura | Público |
| Atribución de commits | Identidad del administrador del proveedor, firmada con SSH |
| Cadencia de lanzamiento | Basada en tags, semver |

Los contribuyentes no envían directamente a este repositorio. Envían a bifurcaciones personales y abren pull requests. El administrador hace squash-merge; nace el commit corporativo; la transferencia de PI está completa.

## Capa 2 — ESCAPARATE

La Capa Escaparate es el catálogo público del cliente de patrones de implementación. Es un conjunto curado de guías operacionales y manifiestos de implementación que muestran cómo un cliente de [[pointsav-overview|PointSav]] usa el sustrato del proveedor para operar negocios reales.

| Propiedad | Valor |
|---|---|
| Repositorio | `github.com/woodfine/woodfine-fleet-deployment` |
| Diseño | Un subdirectorio por implementación nombrada |
| Acceso de escritura | Solo `mcorp-administrator` |
| Acceso de lectura | Público |
| Tipo de contenido | Guías operacionales `GUIDE-*`; `MANIFEST.md` por implementación |

La Capa Escaparate no es un registro de implementación privado. Es la demostración publicada del cliente de cómo se usa el sustrato del proveedor en la práctica — visible para otros clientes potenciales, inversores y reguladores. Funciona como un showroom viviente.

## Capa 3 — INSTANCIAS

La Capa 3 contiene las implementaciones en ejecución reales. Cada implementación es una instancia numerada de una plantilla nombrada de la Capa Escaparate. Estas instancias son privadas para el operador y nunca aparecen en ningún repositorio de GitHub.

| Propiedad | Valor |
|---|---|
| Ubicación | Almacenamiento local en hardware del operador |
| Estado en GitHub | No comprometido en ningún repositorio compartido |
| Archivos requeridos | `MANIFEST.md`, `README.md` + `README.es.md` |
| Personalización por implementación | Variables de entorno, claves específicas del cliente, anulaciones locales |

La regla de privacidad estricta es estructural: una instancia de implementación contiene configuración específica del cliente, material de claves y estado operacional. Nada de esto pertenece a un libro mayor público. La Capa Escaparate publica la receta; la Capa de Instancias es la cocción real — en la cocina del cliente, con los ingredientes del cliente.

## Por qué tres capas, no dos

Una arquitectura más simple colapsaría las Capas 2 y 3: las implementaciones reales del cliente serían el catálogo público del cliente. [[pointsav-overview|PointSav]] las separa deliberadamente:

| Problema con dos capas | Cómo lo resuelve tres capas |
|---|---|
| Las implementaciones públicas exponen claves y configuraciones específicas del cliente | La Capa 3 es privada; solo la plantilla de la Capa 2 es pública |
| El cliente duda en publicar una implementación real | La Capa 2 es un catálogo de plantillas, no entornos reales |
| Otros clientes potenciales no pueden ver cómo se usa el sustrato del proveedor | La Capa 2 proporciona exactamente esa demostración sin exponer el estado operacional |
| Las actualizaciones del operador a una implementación privada ensuciarían el libro mayor público | Las instancias de la Capa 3 nunca aparecen en ningún repositorio compartido |

La separación es la respuesta estructural a una pregunta que enfrenta todo proveedor B2B: cómo demostrar el producto en producción sin filtrar la realidad operacional del cliente.

## El Tétrade

Cada archivo de proyecto de [[pointsav-overview|PointSav]] declara cuatro elementos — proveedor, cliente, implementación y wiki. Las tres capas arquitectónicas anteriores representan tres de los cuatro; el cuarto es el contenido público de documentación que explica el sustrato a los lectores humanos. El Tétrade garantiza que cada proyecto tenga simultáneamente código fuente en la capa SOFTWARE, una plantilla de implementación en la capa ESCAPARATE, una instancia real en la capa INSTANCIAS y artículos explicativos en la wiki de documentación — y que ninguno de los cuatro falte.

## Véase también

- [[five-stage-supply-chain]] — cómo el código se mueve entre las tres capas
- [[six-tier-sovereignty-matrix]] — la taxonomía de directorios que organiza la capa SOFTWARE
- [[deployment-patterns]] — los patrones de implementación nombrados que pueblan la capa ESCAPARATE
