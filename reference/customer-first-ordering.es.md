---
schema: foundry-doc-v1
title: "Ordenamiento cliente-primero"
slug: customer-first-ordering.es
category: reference
type: topic
quality: published
short_description: El principio de que un proveedor de software que construye algo que un cliente instalará debe construirlo en el mismo orden que el cliente lo instalará, en el mismo sustrato que el cliente usará.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: customer-first-ordering.md
---

## Resumen estratégico

El ordenamiento cliente-primero es la disciplina que previene que el desarrollo interno de un proveedor de software diverge de la experiencia operativa del cliente, haciendo que la secuencia de instalación del cliente sea la secuencia de construcción del proveedor.

## El principio

Al construir algo que un cliente instalará, construirlo en el mismo orden que el cliente lo instalará, en el mismo sustrato que el cliente usará. El espacio de trabajo de desarrollo del proveedor es la primera instalación numerada del producto que describe. Si la instalación del proveedor funciona limpiamente en ese orden en ese sustrato, el runbook del cliente es verdadero por construcción.

## Por qué importa el vendedor-como-primer-cliente

Las brechas en la experiencia del cliente emergen durante el desarrollo del proveedor en lugar de aparecer el primer día del cliente. Si un script de arranque falla, un archivo de configuración no está documentado o falta una dependencia en un runbook, el proveedor lo descubre antes de publicar.

## Responsabilidad de tres capas

El principio se asigna a una estructura de responsabilidad de tres capas: pasos de nivel operador (que reflejan lo que el cliente hace en los límites de hardware), pasos de nivel plataforma (instalar y configurar la plataforma), y pasos de nivel de características (construir los paquetes que el cliente instala). Una prueba útil: si el paso aparece en el runbook de instalación del cliente, pertenece a la capa de plataforma u operador. Si el paso es "construir el paquete que instala el cliente", pertenece a la capa de características.

## Excepciones documentadas

Algunos pasos no pueden ser utilizados internamente porque son estructuralmente imposibles de realizar desde dentro de un sistema en ejecución: pasos en el límite de hardware, pasos de publicación de paquetes, e investigación de preproducción que produce las recomendaciones que los clientes consumen.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
