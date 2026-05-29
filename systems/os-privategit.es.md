---
schema: foundry-doc-v1
type: topic
slug: os-privategit
short_description: "La capa de sistema operativo que aloja la infraestructura Git privada que sustenta el espacio de trabajo de desarrollo, flujo de commit de nivel de staging y repositorios de fuente canónica para todos los repos de ingeniería de PointSav."
title: "Private Git OS"
category: systems
language: es
paired_with: os-privategit.md
status: stub
last_edited: 2026-05-25
editor: pointsav-engineering
---

`os-privategit` es la capa del sistema operativo que aloja la infraestructura soberana de control de versiones de la plataforma — repositorios Git privados y alojamiento del [[design-system-substrate|sistema de diseño]] — en hardware propiedad del operador, sin enrutar el código fuente a través de un proveedor externo de alojamiento Git. Pertenece a la [[os-family-overview|familia de ocho SO]] y se empareja con el [[os-privategit-workbench|banco de trabajo de navegador]] para la autoría y revisión de archivos.

El entorno de escritorio [[os-workplace|os-workplace]] y el archivo [[totebox-os|Totebox]] son los consumidores principales del software alojado en `os-privategit`. El código fuente fluye desde `os-privategit` hacia el modelo de despliegue [[customer-first-ordering|cliente-primero]].

## Véase también

- [[os-privategit-workbench]] — el editor de archivos basado en navegador en os-privategit
- [[os-family-overview]] — la familia de ocho SO y dónde encaja os-privategit
- [[machine-based-auth]] — el modelo de autorización que rige el acceso a los repositorios privados
- [[deployment-patterns]] — cómo os-privategit aparece en las configuraciones de flota canónicas
