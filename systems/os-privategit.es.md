---
schema: foundry-doc-v1
type: topic
content_type: topic
index_group: network-control-and-infrastructure
slug: os-privategit
short_description: "La capa de sistema operativo que aloja la infraestructura Git privada que sustenta el espacio de trabajo de desarrollo, flujo de commit de nivel de staging y repositorios de fuente canónica para todos los repos de ingeniería de PointSav."
title: "Private Git OS"
category: systems
language: es
paired_with: os-privategit.md
status: stub
last_edited: 2026-08-22
editor: pointsav-engineering
---

`os-privategit` es la capa del sistema operativo que ejecuta la infraestructura soberana de control de versiones de la plataforma — repositorios Git privados y alojamiento del [[design-system-substrate|sistema de diseño]] — en hardware propiedad del operador, sin enrutar el código fuente a través de un proveedor externo de alojamiento Git. El propio binario del SO es una puerta de verificación de licencia; la lógica de alojamiento Git y del sistema de diseño reside en las aplicaciones hermanas `app-privategit-*` que aloja (`app-privategit-source`, `app-privategit-design`, `app-privategit-marketplace`, `app-privategit-workbench`), siguiendo la misma división SO/aplicación que el resto de la familia. Pertenece a la [[os-family-overview|familia de ocho SO]] y se empareja con el [[app-privategit-workbench|banco de trabajo de navegador]] para la autoría y revisión de archivos.

El entorno de escritorio [[os-workplace|os-workplace]] y el archivo [[totebox-os|Totebox]] son los consumidores principales del software alojado en `os-privategit`. El código fuente fluye desde `os-privategit` hacia el modelo de despliegue [[customer-first-ordering|cliente-primero]].

## Estado actual de construcción y despliegue

A diferencia de un resumen genérico de "lista de aplicaciones", cada una de las cuatro
aplicaciones alojadas tiene su propio estado de construcción confirmado, en lugar de una
descripción única y uniforme:

| Aplicación | Versión | Estado | Qué hace |
|---|---|---|---|
| `app-privategit-source` | v0.1.0 | Activa | Servidor de publicación de binarios con verificación de token de licencia Ed25519 |
| `app-privategit-marketplace` | v0.1.0 | Activa | Tienda de software — catálogo de productos, emisión de licencias, verificación de pagos |
| `app-privategit-workbench` | v0.0.1 | Activa | El editor de archivos de tres columnas basado en navegador (árbol / visor / editor) mencionado arriba |
| `app-privategit-design` | v0.3.0 | Sin confirmar | Existe una base de código sustancial en disco; el propio README del crate se autodescribe como un andamiaje arquitectónico temprano pendiente de un ciclo de ingeniería dedicado — ambas señales están en conflicto y no se concilian aquí |

`app-privategit-source` y `app-privategit-marketplace` están desplegadas y activas en el host
`vault-privategit-source-1` hoy. `app-privategit-workbench` está activa como la superficie de
edición de archivos descrita arriba. El estado real de `app-privategit-design` no pudo
confirmarse en un sentido u otro a partir de las fuentes disponibles al momento de escribir
esto — se menciona aquí en lugar de omitirse silenciosamente, con su estado señalado como sin
confirmar en lugar de afirmado.

## Véase también

- [[app-privategit-workbench]] — el editor de archivos basado en navegador en os-privategit
- [[os-family-overview]] — la familia de ocho SO y dónde encaja os-privategit
- [[machine-based-auth]] — el modelo de autorización que rige el acceso a los repositorios privados
- [[deployment-patterns]] — cómo os-privategit aparece en las configuraciones de flota canónicas
