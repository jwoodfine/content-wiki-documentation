---
schema: foundry-doc-v1
title: "Totebox Archive"
slug: totebox-archive
short_description: "Un Totebox Archive es una bóveda soberana de datos asignada a una única entidad — empaquetada como una imagen de disco de arranque libremente transferible, almacenando datos como archivos planos WORM, y aceptando consultas solo a través del Diode Standard y el PointSav Protocol."
category: systems
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
language: es
language_protocol: TRANSLATE-ES
paired_with: totebox-archive.md
last_edited: 2026-05-30
editor: editorial
---

Un Totebox Archive es una bóveda soberana de datos asignada a una única entidad — un edificio, una empresa, una persona, o cualquier otra unidad que el operador defina. Es la unidad fundamental de almacenamiento e identidad de la pila PointSav. El archivo se empaqueta como una imagen de disco de arranque y se ejecuta como una máquina virtual en la capa de hipervisor PPN. Se publica bajo Apache 2.0 y está disponible de forma gratuita: un operador, un archivo, es un despliegue gratuito.

## La imagen de disco es el archivo

La propiedad más importante de un Totebox Archive es que la imagen de disco de arranque y el archivo son la misma cosa. No existe una base de datos externa, ni un bucket de almacenamiento en la nube, ni un registro central que contenga los datos del archivo. La imagen de disco contiene todo: los datos, el par de claves de identidad y el sistema operativo que sirve las consultas.

Esto significa que un archivo puede ser:

- **Detenido** — la VM se apaga; no se pierden datos; nada caduca
- **Copiado** — la imagen de disco es un archivo que puede duplicarse como cualquier otro archivo
- **Reubicado** — la copia se inicia en un nodo PPN diferente; el hipervisor del nodo de destino asigna recursos de su propio pool para la nueva VM
- **Reanudado** — el archivo continúa exactamente desde el estado en que se encontraba cuando fue detenido

El hipervisor del nodo receptor no sabe nada sobre los datos dentro de la VM. Asigna CPU y RAM de su pool por nodo para alojar la VM. La identidad, las claves y los datos del archivo viajan con la imagen de disco sin cambios. Esta es la propiedad de transferencia libre.

## Modelo de almacenamiento: archivos planos WORM

Un Totebox Archive almacena datos como archivos planos inmutables:

| Formato | Contenido |
|---|---|
| JSONL | Registros estructurados (entradas de libro mayor, registros de eventos, metadatos de entidades) |
| GeoParquet | Datos geoespaciales (límites de sitios, registros de ubicación) |
| Markdown | Documentos legibles por humanos (memorandos, notas, informes) |

Cada escritura añade datos; ningún registro se modifica ni elimina jamás. Este es un libro mayor de Escritura Única, Lectura Múltiple (WORM). El archivo acumula un historial completo e inalterable de cada entrada registrada. No existe operación `DELETE` ni operación `UPDATE` — solo anexado. Una entrada que debe ser reemplazada es seguida por una entrada de corrección; la entrada original permanece permanentemente visible en el registro.

Este diseño es intencional: el archivo es un registro de calidad legal de lo que una entidad sabía y cuándo lo sabía. La garantía de inmutabilidad es estructural, no una opción de configuración.

## Modelo de acceso: solo Diodo + PSP

Un Totebox Archive no expone una API de propósito general. Responde solo a consultas entregadas a través del [[diode-standard|Diode Standard]] — el flujo de comandos unidireccional que gobierna la pila PointSav:

```
os-console  ──┐
               ├──▶  os-orchestration  ──▶  os-totebox (dentro de la VM del archivo)
               │         (PSP)
               └──▶  os-totebox (directo, archivo único)
```

Las consultas llegan como objetos de capacidad firmados entregados a través del PointSav Protocol (PSP), un protocolo binario basado en capacidades que tuneliza sobre TLS. Un objeto de capacidad otorga permiso para leer una fila específica o un conjunto de filas — nada más. El archivo verifica la firma del objeto contra su par de claves MBA, ejecuta la consulta y devuelve solo las filas de resultados coincidentes. Nunca devuelve registros sin procesar en bloque. Nunca acepta comandos desde una dirección fuera del flujo del Diodo.

Ninguna VM puede emitir comandos de regreso al plano de control. Ningún archivo puede instruir a la malla PPN para añadir o eliminar un nodo. El flujo es estructuralmente unidireccional.

## Par de claves de autorización basada en máquina

Cada Totebox Archive contiene un par de claves Ed25519. Este par de claves es la identidad del archivo en la malla PointSav. Está registrado en `pairings.yaml`, el archivo que gobierna qué operadores y orquestadores están autorizados para consultar el archivo.

Los tipos de emparejamiento son:

| Tipo | Nivel de acceso |
|---|---|
| ADMIN | Autoridad administrativa total sobre este archivo |
| INPUT | Lectura-escritura; emparejamiento predeterminado para entrada de datos activa |
| USER | Solo lectura |
| INTERFACE | Solo metadatos; sin contenido de registros |

Un operador sin entrada en `pairings.yaml` no puede consultar el archivo, independientemente de si está en la misma malla PPN. La accesibilidad de red y el acceso a datos son planos separados sin autoridad compartida.

## Convención de nomenclatura del clúster

Los archivos se nombran con el prefijo `cluster-totebox-` seguido del dominio de datos y un número de instancia:

| Nombre de instancia | Dominio |
|---|---|
| `cluster-totebox-corporate-1` | Registros de entidades corporativas |
| `cluster-totebox-personnel-1` | Registros de personal |
| `cluster-totebox-property-1` | Registros de bienes inmuebles |

El prefijo `cluster-` indica una instancia de VM gestionada por la capa de hipervisor PPN. El sufijo numérico permite que múltiples archivos del mismo dominio coexistan en la misma flota.

## Relación con la familia de SO

| Componente | Rol |
|---|---|
| `os-totebox` | El sistema operativo que se ejecuta dentro de la VM del archivo; gestiona el libro mayor WORM y la superficie de consulta PSP |
| `os-console` | Un terminal nativo de teclado que se conecta a un archivo a la vez; nivel gratuito |
| `os-orchestration` | Un agregador sin estado de múltiples archivos que distribuye consultas a través de muchos archivos mediante PSP; nivel de pago |
| `os-infrastructure` | El hipervisor Tipo I que aloja VMs de archivo y gestiona el pool de recursos por nodo |

`os-totebox` y `os-console` son Apache 2.0 — gratuitos. `os-orchestration` introduce el límite comercial: consultar un único archivo directamente a través de `os-console` es gratuito; enrutar consultas a través de múltiples archivos mediante `os-orchestration` es el nivel de pago.

## Lo que un Totebox Archive no es

- **No es una base de datos.** No existe planificador de consultas, índice ni registro de transacciones en el sentido de bases de datos relacionales. El archivo es un libro mayor de solo anexado que devuelve filas que coinciden con un objeto de capacidad firmado.
- **No es almacenamiento en la nube.** No hay bucket S3, API de almacenamiento de objetos ni URL prefirmada. Los datos salen del archivo solo a través de la ruta Diodo + PSP.
- **No es un recurso compartido de archivos.** No hay recurso compartido SMB, montaje NFS ni punto final SFTP. Los operadores acceden a los datos a través de `os-console` o `os-orchestration`, no a través de protocolos de sistema de archivos.
- **No es una VM en el sentido general.** La VM es el medio de empaquetado. El archivo son los datos, la identidad y la historia que contiene. Cuando alguien se refiere al "Totebox Archive", se refiere a la imagen de disco y su contenido — no a la instancia del hipervisor que en este momento la ejecuta.

## Temas relacionados

- [[infrastructure-os]] — el hipervisor Tipo I que aloja VMs de archivo y gestiona el pool de recursos
- [[ppn-hypervisor-resource-pool]] — cómo el hipervisor otorga y recupera CPU/RAM de cada VM
- [[machine-based-auth]] — el modelo de par de claves Ed25519 que gobierna el acceso al archivo
- [[diode-standard]] — el flujo de comandos unidireccional que atraviesa cada consulta al archivo
