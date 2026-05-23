---
schema: foundry-doc-v1
title: "PointSav — Visión general de la empresa y estructura de tres organizaciones"
slug: pointsav-overview
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: pointsav-overview.md
short_description: "PointSav Digital Systems es un proveedor de tecnología que construye sistemas operativos soberanos y con capacidad de instalación local para gestión de registros y administración empresarial. Se encuentra dentro de una estructura de tres organizaciones establecida por Woodfine Capital Projects Inc."
cites: []
---

PointSav Digital Systems es un proveedor de tecnología que construye y licencia sistemas operativos soberanos y con capacidad de instalación local, junto con servicios de gestión de registros, administración empresarial e integración de sistemas ciberfísicos. La empresa existe para diseñar el sustrato que opera las operaciones inmobiliarias de su grupo matriz, y luego licencia ese sustrato a clientes institucionales con estructuras similares. PointSav se encuentra dentro de una topología de gobernanza de tres organizaciones establecida por Woodfine Capital Projects Inc., una firma inmobiliaria enfocada en la adquisición, desarrollo y gestión de propiedades inmobiliarias. Este artículo cubre la estructura de tres organizaciones, las ventajas estructurales que produce y el modelo de licenciamiento y contribuidores.

## La estructura de tres organizaciones

| Organización | Rol | Relación |
|---|---|---|
| **Woodfine Capital Projects Inc.** | Matriz al 100% | Firma inmobiliaria; posee ambas subsidiarias íntegramente |
| **PointSav Digital Systems** | Proveedor | Titular de PI; diseña y construye la plataforma tecnológica |
| **Woodfine Management Corp.** | Cliente | Primer cliente y cliente de referencia; opera activos inmobiliarios |

El flujo de relaciones es estrictamente unidireccional: el proveedor construye, el cliente adopta, los despliegues funcionan. No hay escrituras inversas — el cliente nunca edita el código fuente del proveedor, y el proveedor nunca gestiona los registros del cliente.

## Por qué esta estructura importa

Tres ventajas estructurales emergen de la separación:

**Custodia limpia de PI.** PointSav posee la propiedad intelectual. Woodfine Management Corp. licencia el producto como cualquier otro cliente. No hay mezcla de registros corporativos y código fuente.

**Despliegue de referencia.** Dado que Woodfine Management Corp. es un operador real — no un entorno de prueba — cada función del producto debe sobrevivir el contacto con operaciones empresariales reales antes de poder venderse en otro lugar. El cliente de referencia es la puerta de calidad.

**Claridad para inversores.** El proveedor (PointSav) es el activo que escala. El cliente (Woodfine Management Corp.) es el activo que opera. Cada uno puede medirse, auditarse y valorarse en sus propios términos.

## Modelo de licenciamiento

La estrategia de productos sigue un patrón de núcleo abierto. Los sistemas operativos principales (`os-totebox`, `os-console`, `os-workplace`) están previstos para su lanzamiento bajo Apache 2.0 con un Addendum Soberano previsto que garantice que las instancias en ejecución permanezcan libremente transferibles por el operador independientemente de dónde estén alojadas. El producto agregador de flota (`os-orchestration`) está previsto para permanecer como propietario en calidad de impulsor de ingresos comerciales.

PointSav tiene previsto asociarse con la Sovereign Data Foundation para supervisar la integridad de los componentes de código abierto. Los términos y la estructura de cualquier acuerdo de este tipo están previstos y sujetos a finalización.

## Modelo de contribuidores

El trabajo de ingeniería fluye a través de identidades de contribuidores de nivel de staging: `jwoodfine` y `pwoodfine` son los dos contribuidores de staging establecidos, ambos empleados de Woodfine Management Corp. que envían cambios a sus propias bifurcaciones de GitHub. La función de administración del proveedor acepta contribuciones mediante fusión-aplastada — el momento en que la propiedad intelectual se transfiere formalmente del contribuidor al proveedor. La organización cliente extrae etiquetas de versión del proveedor. Se aplica una compartimentación de doble cara: los contribuidores nunca envían directamente a los repositorios del cliente; la organización cliente nunca tiene visibilidad de las bifurcaciones de los contribuidores.

## Véase también

- [[legal-and-ip-structure]] — entidades corporativas, mecánicas de transferencia de PI, estrategia de patentes y licencias
- [[deployment-patterns]] — las seis configuraciones canónicas para despliegues de PointSav
- [[os-family-overview]] — los ocho sistemas operativos que construye PointSav
- [[machine-based-auth]] — el modelo de seguridad que subyace a la plataforma
- [[compliance-and-continuous-disclosure]] — postura BCSC y obligaciones de divulgación continua
