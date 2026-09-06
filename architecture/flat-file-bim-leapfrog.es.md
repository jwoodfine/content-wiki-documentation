---
schema: foundry-doc-v1
title: "El salto del BIM en archivos planos"
slug: flat-file-bim-leapfrog
language: es
category: architecture
index_group: location-intelligence-and-domain
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "El Sistema de Diseño de Edificios se construye sobre cinco restricciones — archivos planos, estándares abiertos, Rust y Tauri, funcionamiento sin conexión y licencia Apache 2.0. La propiedad anclada al activo, el uso en campo sin red, la ingesta de sensores y la convergencia del modelo con los registros de arrendamiento y financieros se derivan de la arquitectura, no se añaden encima."
cites: [ifc-4-3, iso-19650]
paired_with: flat-file-bim-leapfrog.md
---

El Sistema de Diseño de Edificios de PointSav se apoya en cinco restricciones arquitectónicas: almacenamiento en archivos planos, estándares abiertos, Rust y Tauri, funcionamiento sin conexión y licencia Apache 2.0. Por separado, cada una es un inconveniente menor en una comparación de funcionalidades. Juntas definen una categoría de producto que un hiperescalador no puede ocupar sin canibalizar su propio modelo de ingresos.

**Por qué importa:** un registro digital construido así se posee como se posee el edificio — de forma permanente, transferible y sin pagar a un proveedor por seguir accediendo a él.

Este artículo explica qué es el BIM en archivos planos, qué no es, y por qué cinco capacidades concretas se derivan de la arquitectura en lugar de añadirse encima.

## Los estándares alcanzaron madurez de producción en 2024

La premisa sobre la que se apoya la arquitectura es que los estándares ya existen, especifican codificaciones de texto plano y están dentro de la ISO. IFC 4.3 se publicó como ISO 16739-1:2024 en abril de 2024 y extendió IFC de los edificios a puentes, carreteras, ferrocarril, puertos y vías navegables. Su serialización canónica, IFC-SPF, es texto claro ISO 10303-21, legible en cualquier editor de texto. IDS 1.0 pasó a ser estándar oficial de buildingSMART el 1 de junio de 2024. BCF 3.0 es un ZIP de marcado XML con capturas PNG: descomprimido, su árbol de directorios por tema es prosa comparable línea a línea. CityJSON 2.0 es un estándar comunitario de OGC, y CityJSONSeq se usa a escala nacional en el conjunto 3DBAG de la TU Delft, con más de diez millones de edificios neerlandeses.

Importa igual lo que **no** está listo para producción. ifcJSON sigue siendo un borrador comunitario. IFC 5 está en fase alfa, con una serialización IFCX basada en JSON que toma la composición de OpenUSD de Pixar; se esperan cambios incompatibles. La conclusión práctica: canonizar hoy sobre IFC-SPF, replicar a ifcJSON de forma oportunista y diseñar el modelo de objetos para que una migración a IFC 5 / IFCX sea un cambio de serialización y no una reescritura.

**Por qué importa:** la arquitectura no depende de ningún estándar que PointSav haya redactado o controle. La afirmación de durabilidad es una afirmación sobre la ISO, no sobre PointSav.

## Qué significa "archivo plano"

Un directorio de archivos de texto plano y binarios estandarizados que un editor de texto o un visor SVG corriente puede abrir sin un SDK propietario, décadas después de que desaparezca el proveedor que los produjo.

| Formato | ISO / editor | Función |
|---|---|---|
| IFC-SPF (`.ifc`) | ISO 16739-1:2024 | Geometría y semántica autoritativas |
| IDS 1.0 | buildingSMART (junio 2024) | Contrato de validación |
| BCF 3.0 | buildingSMART | Historial de colaboración por tema |
| COBie vía ifccsv | NIST | Entrega de activos |
| Sidecars YAML por elemento | convención local | `Pset_*`, sensores y órdenes de trabajo |
| Almacén de objetos por hash | convención local; inspirado en Speckle | DAG de Merkle versionado |
| glTF 2.0 | ISO/IEC 12113:2022 | Caché de visualización (regenerable) |
| SVG | Recomendación W3C (sin número ISO/IEC) | Planos 2D (regenerables) |
| CityJSONSeq | OGC | Contexto de cartera y urbano |

El archivo `.ifc` es el estado espacial y semántico autoritativo del edificio. Los sidecars llevan los datos no geométricos — clasificaciones, cantidades, lecturas de sensores, órdenes de trabajo, referencias de arrendamiento. La capa de almacén de objetos da al conjunto una semántica de versionado equivalente a la de git. Las derivadas de visualización son cachés que se regeneran a voluntad desde la fuente autoritativa. Cualquier visor o herramienta de autoría BIM concreta es sustituible; el archivo no lo es.

**Por qué importa:** la sustituibilidad es todo el diseño. Un visor que desaparece cuesta un renderizado, no un levantamiento nuevo.

## Cinco capacidades que se derivan de la arquitectura

### 1. BIM anclado al activo

El registro digital se firma junto al título de propiedad y acompaña a la escritura cuando cambia de manos. Una plataforma SaaS multiinquilino no puede ofrecer esto sin romper su modelo de arrendamiento de servicio: el nuevo propietario debe incorporarse al inquilino del proveedor, migrar el modelo, reconstruir los permisos y renegociar la suscripción. Un registro en archivos planos se posee como se posee el edificio — de forma indefinida, transferible, sin permiso del proveedor.

Las condiciones de suscripción del BIM en la nube lo dejan explícito: un plazo vencido obliga al propietario a firmar un nuevo contrato para seguir accediendo a los datos del proyecto. El registro digital se alquila; no se vende.

### 2. BIM sin conexión para trabajo de campo

Sótanos, cubiertas, obras remotas, instalaciones de defensa aisladas de red, campus sanitarios con residencia de datos estricta, regiones de baja conectividad — en todos ellos un modelo cuya autoridad reside en la nube es estructuralmente imposible, porque el BIM con autoridad en la nube exige acceso de red en vivo durante la construcción. Un contenedor Tauri y Rust que aloja un archivo IFC local en un portátil o tableta conserva toda la funcionalidad sin dependencia alguna de la red.

### 3. BIM que sobrevive a la obsolescencia del proveedor

Los edificios duran cincuenta años o más; los formatos propietarios de autoría BIM mantienen compatibilidad durante tres a cinco años. Un sustrato en archivos planos sigue siendo legible décadas después de que desaparezca un proveedor concreto. Esto importa sobre todo a los programas BIM del sector público (UK Government Level 2, GSA, DoD y VA en Estados Unidos), a los custodios de patrimonio cultural y a los propietarios de horizonte largo — los compradores más expuestos al riesgo de discontinuación.

### 4. Ingesta de sensores directamente en el archivo

Un archivo en archivos planos con sidecars YAML por elemento admite lecturas de un broker MQTT local, escritas como registros JSON con marca temporal en el sidecar del propio elemento, sin que los datos salgan de las instalaciones del propietario. Importa en lo económico (sin tarificación por sensor), en lo legal (residencia GDPR, HIPAA en sanidad, control de exportación en defensa) y en lo arquitectónico: el historial de sensores queda versionado junto a la geometría en lugar de derivar en un sistema aparte.

### 5. Modelo, registro de arrendamientos y libro financiero en un solo archivo portátil

Para un propietario, el edificio, el arrendamiento, la renta y la financiación son el mismo activo: el edificio es donde se aplica el arrendamiento, el arrendamiento es de donde procede la renta, la renta atiende el préstamo y el préstamo justificó el edificio. La nube multiinquilino no puede reunir modelo, registro de arrendamientos y renta en un único archivo bajo control del propietario: la confidencialidad comercial, la residencia de datos, las pistas de auditoría financiera y el aislamiento entre inquilinos lo impiden cada una por separado.

La familia de aplicaciones de puesto de trabajo — `app-workplace-memo`, `app-workplace-presentation`, `app-workplace-proforma` y `app-workplace-bim` — está prevista para converger en ese archivo único, de modo que la identidad legal, financiera, espacial y operativa de un edificio sea un solo artefacto que viaja con el activo.

**Por qué importa:** ninguna de las cinco es una funcionalidad de hoja de ruta que pudiera retirarse. Cada una se deriva de elegir archivos planos, estándares abiertos y funcionamiento sin conexión — que es también la razón por la que un competidor nativo de nube no puede ofrecerlas sin cambiar lo que vende.

## La aceptación regulatoria es estructuralmente favorable

La pila de formatos — IFC-SPF, IDS 1.0, BCF 3.0 y COBie — satisface los requisitos obligatorios de entrega en estándar abierto de las agencias federales estadounidenses (GSA, USACE, VA, NAVFAC), de los Estados miembros de la UE (Alemania, Italia, España, Dinamarca, Noruega, Países Bajos, Polonia), del UK BIM Framework, de CORENET X en Singapur (obligatorio desde octubre de 2026), de Dubái (obligatorio desde enero de 2024) y del programa openBIM de buildingSMART.

Una arquitectura sin conexión y en archivos planos es la única que satisface de forma nativa el aislamiento de red exigido por ITAR en defensa, la soberanía del Reglamento de Datos de la UE, las salvaguardas técnicas de HIPAA y la residencia de datos del GDPR, sin depender de las garantías contractuales de un proveedor de nube. La licencia Apache 2.0 que rige los archivos de datos de Objetos BIM está aprobada por la OSI, es compatible con FAR 12.212 y admite tanto la contratación pública como el uso derivado comercial.

**Por qué importa:** la postura de cumplimiento es una propiedad de los formatos de archivo, no de una certificación que PointSav deba mantener.

## Qué no hace bien todavía el BIM en archivos planos

Un balance honesto de las concesiones:

- La edición simultánea en tiempo real es más lenta que en un SaaS síncrono para talleres de diseño tipo *charette*. Para sesiones síncronas, el SaaS en la nube es genuinamente mejor.
- La federación a escala de ciudad, con un millón o más de edificios, requiere una arquitectura de transmisión distinta a la de un archivo de una sola propiedad.
- Las herramientas generativas de autoría BIM de los grandes proveedores son propietarias hoy. El sustrato está preparado para la participación de la IA — el [[compounding-doorman|Doorman]] despacha las solicitudes generativas a través de un libro de auditoría — pero no hay una herramienta de autoría generativa prevista para la versión v0.0.1.

Son concesiones deliberadas de una postura sin conexión y resistente a la obsolescencia, no descuidos pendientes de parche.

## Véase también

- [[city-code-as-composable-geometry]] — codificar los requisitos normativos en la propia especificación del elemento
- [[worm-ledger-design]] — el patrón de libro de solo anexado que sigue el versionado del archivo
- [[sel4-microkernel-substrate]] — el sustrato de aislamiento bajo los despliegues sin conexión
