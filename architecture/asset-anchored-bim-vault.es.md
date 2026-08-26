---
schema: foundry-doc-v1
title: "Bóveda BIM anclada al activo"
slug: asset-anchored-bim-vault
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
short_description: "El registro digital autoritativo de un edificio, estructurado como archivos de texto plano y binario estandarizado en un directorio versionado con git, que califica como un Entorno de Datos Común conforme a la norma ISO 19650 y que viaja con la escritura de la propiedad."
cites: [ifc-4-3, iso-19650, ids-1-0]
paired_with: asset-anchored-bim-vault.md
---

El registro digital autoritativo de un edificio es un directorio de archivos de texto plano y binario estandarizado que reside en el almacenamiento del propietario, viaja con la escritura de la propiedad cuando cambia de dueño, y permanece legible sin una licencia de software propietaria mientras se mantengan los estándares abiertos subyacentes. Este artículo describe la disposición de la bóveda, la capa de versionado que le da al archivo trazabilidad de grado git, y la calificación bajo ISO 19650 que hace de un repositorio git de archivos planos un Entorno de Datos Común conforme.

**Por qué importa:** el registro se posee de la misma manera en que se posee el edificio mismo — de forma permanente, transferible, y sin pagar a un proveedor por acceso continuado.

## La disposición de la bóveda

La bóveda canónica para un archivo de propiedad se estructura así:

```
vault/
├── ifc/             # Archivos IFC-SPF autoritativos (ISO 16739-1:2024)
├── elements/        # Sidecars YAML por elemento (Pset_* + sensor + orden de trabajo)
├── bcf/             # Directorios BCF 3.0 por tema (XML + PNG; sin comprimir)
├── ids/             # Contratos de validación IDS 1.0 (superposición por jurisdicción)
├── materials/       # Base de datos de materiales (archivos planos; entrada de service-materials)
├── codes/           # Códigos de construcción como superposiciones geométricas componibles
│                    #   (bsdd-*.json + *.ids + fragmentos *.ifc por jurisdicción)
├── geometry/        # glTF 2.0 + CityJSONSeq (cachés regenerables; no canónicos)
├── drawings/        # Dibujos 2D en SVG (regenerables; GUID de IFC en los IDs de elemento SVG)
├── objects/<hash>.json  # Almacén de objetos direccionado por hash
└── refs/            # Punteros de referencia estilo git (ramas, etiquetas, HEADs)
```

Los archivos `.ifc` son el único estado espacial y semántico autoritativo del edificio. Cada uno de los demás directorios valida el estado IFC, lo enriquece con datos no geométricos, o almacena en caché una representación derivada que puede regenerarse desde la fuente canónica.

## El archivo IFC-SPF como archivo canónico

IFC-SPF es la codificación STEP Physical File de IFC, especificada en ISO 10303-21. Es un formato de texto claro orientado a líneas: una persona con un editor de texto puede leer un archivo IFC-SPF. Un diff de Unix entre dos archivos IFC-SPF muestra exactamente qué entidades cambiaron entre versiones del modelo.

El formato está en producción desde IFC 1.0 en 1996. IFC 4.3, publicado como ISO 16739-1:2024, es la revisión vigente. El modelo de gobernanza del estándar — mantenido por buildingSMART International, ratificado por ISO — ofrece la vida útil más creíble de cualquier formato de datos de construcción en uso hoy.

## Sidecars YAML por elemento

Cada elemento IFC que porta datos operativos no geométricos tiene un sidecar YAML correspondiente en `vault/elements/`. El nombre de archivo del sidecar es el GUID de IFC del elemento, que es estable entre revisiones del modelo.

El sidecar puede portar:

- **Anulaciones de Pset** — valores de propiedad no geométricos no capturados en la sesión de autoría IFC
- **Lecturas de sensores** — registros con marca de tiempo desde un broker MQTT (temperatura, CO₂, ocupación) escritos como entradas de registro de solo adición
- **Órdenes de trabajo** — referencias a tareas de mantenimiento, registros de inspección e historial de reparación por ID de orden de trabajo
- **Referencias de arrendamiento** — identificador de inquilino y plazo de arrendamiento, vinculando el elemento espacial con el registro de arrendamientos

Debido a que el sidecar es un archivo YAML plano en el mismo repositorio git que el archivo IFC, cada cambio a los datos de sensores o al historial de órdenes de trabajo es un commit de git. El historial operativo del edificio queda versionado junto con su geometría.

**Por qué importa:** los datos de sensores y de arrendamiento suelen ser la primera baja de una migración de proveedor — un archivo sidecar plano sobrevive a una porque nada en él depende de la herramienta que lo escribió.

## El almacén de objetos direccionado por hash y su estructura de tokens

El directorio `vault/objects/` implementa un almacén de objetos direccionado por hash. Cada objeto es un archivo JSON cuyo nombre de archivo es el hash SHA-256 de su contenido — esta es la unidad de datos almacenados del archivo, y cada uno combina tres cosas a la vez, escritas juntas como un registro atómico único: una carga binaria inmutable que es direccionable por contenido y de escritura única; un esqueleto de metadatos que porta campos validados por esquema que describen el tipo, la procedencia y la titularidad del contenido; y una conexión de grafo que enlaza el objeto con su posición en la jerarquía taxonómica que mantiene el servicio de grafo de conocimiento. Ninguno de los tres existe de forma aislada dentro del archivo — una carga sin su esqueleto de metadatos o su posición de grafo no es un objeto resoluble.

`vault/refs/` contiene punteros con nombre — ramas, etiquetas y HEAD — que resuelven a hashes de objeto específicos.

Esta arquitectura le da a la bóveda semántica de direccionamiento por contenido al estilo git, independientemente del repositorio git que la envuelve. El resultado es un DAG de Merkle: el hash raíz de un estado del modelo está criptográficamente ligado a cada elemento que contiene.

La estructura de Merkle ofrece dos beneficios estructurales:

1. **Integridad del rastro de auditoría.** Un estado histórico declarado del modelo puede verificarse contra el hash raíz sin confiar en el servidor que lo almacenó.
2. **Transferencia eficiente de deltas.** Cuando dos partes sincronizan bóvedas, solo necesitan transferirse los objetos cuyos hashes difieren.

## Calificación bajo ISO 19650

ISO 19650 define un Entorno de Datos Común (CDE) como un sistema para recopilar, gestionar y difundir información en contenedores estructurados. El estándar es neutral en cuanto a tecnología.

Un repositorio git que aloja un directorio de bóveda califica como CDE bajo ISO 19650 con el siguiente mapeo:

| Concepto ISO 19650 | Implementación en git + bóveda |
|---|---|
| Contenedor de información | Archivo IFC o sidecar YAML |
| UID del contenedor | Hash de objeto git o GUID de IFC |
| Estado | Nombre de rama (`work-in-progress`, `shared`, `published`) |
| Revisión | Hash de commit de git |
| Clasificación | Ruta de directorio + encabezado YAML |
| Historial de cambios | `git log --follow <archivo>` |
| Estados de flujo del CDE | Flujo de fusión de ramas / pull-request de git |

Un repositorio git local en una estación de trabajo con air-gap satisface ISO 19650 tan plenamente como una plataforma alojada. Esto hace que la arquitectura de bóveda sea apropiada para proyectos de defensa bajo ITAR, jurisdicciones de la Ley de Datos de la UE, e instalaciones de salud gobernadas por HIPAA.

## Supervivencia ante la obsolescencia de proveedores

Los edificios suelen diseñarse para permanecer en pie entre 50 y 100 años. Las herramientas de software usadas para autorar modelos BIM suelen cambiar de formato con cada versión mayor y volverse ilegibles para herramientas competidoras en menos de una década.

La arquitectura de bóveda aborda esta asimetría de dos maneras. Primero, los formatos canónicos — IFC-SPF, BCF 3.0, IDS 1.0, YAML — son estándares abiertos gobernados por ISO o formatos de texto plano ampliamente adoptados. Cualquier ingeniero competente puede escribir un lector para IFC-SPF a partir de la especificación ISO sin acceso a SDKs propietarios. Segundo, los derivados regenerables — cachés de visualización glTF, dibujos 2D en SVG — están marcados explícitamente como no canónicos. Si la herramienta que los generó desaparece, el archivo IFC canónico permanece y cualquier conversor IFC-a-glTF o IFC-a-SVG puede regenerarlos. La arquitectura es consistente con los principios de diseño descritos en [[flat-file-bim-leapfrog]].

**Por qué importa:** la reemplazabilidad es todo el diseño — una herramienta que desaparece cuesta un re-renderizado, no un nuevo levantamiento.

## El archivo viaja con el terreno

Un activo inmobiliario físico se transfiere con una escritura de propiedad. La bóveda está pensada para agruparse con esa transferencia: el mismo repositorio git que aloja el archivo IFC, las referencias al registro de arrendamientos y el historial operativo acompaña a la propiedad cuando cambia de dueño.

Ninguna plataforma en la nube puede ofrecer esta garantía. Una plataforma SaaS multiinquilino aloja el gemelo digital en nombre del inquilino actual; cuando esa suscripción vence o el proveedor descontinúa el producto, los datos requieren una exportación explícita — y los formatos de exportación son invariablemente más pobres que la representación nativa de la plataforma.

Una bóveda de archivos planos es propiedad del dueño en el mismo sentido en que el edificio físico es propiedad del dueño: incondicionalmente, de forma transferible, y sin permiso continuo de ningún proveedor.

## Véase también

- [[flat-file-bim-leapfrog]] — las cinco restricciones arquitectónicas de las que este diseño de bóveda es una expresión
- [[building-design-system]] — la capa de coordinación que organiza las categorías de objetos que almacena esta bóveda
- [[bim-object-specification]] — el esquema de Objeto BIM que porta cada elemento de esta bóveda
