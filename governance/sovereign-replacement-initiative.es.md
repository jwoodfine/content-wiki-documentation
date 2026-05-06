---
schema: foundry-doc-v1
title: "Iniciativa de Reemplazo Soberano"
slug: sovereign-replacement-initiative
category: governance
type: topic
quality: stub
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: sovereign-replacement-initiative.md
cites: []
---

La Iniciativa de Reemplazo Soberano es el programa formal que registra cada dependencia foránea en un libro contable estructurado, aplica aislamiento de cuarentena hasta que un reemplazo nativo esté listo, y retira la dependencia una vez que el reemplazo alcanza paridad estructural.

## El problema estructural

Cualquier plataforma que haya pasado por una fase de transformación digital hereda componentes arquitectónicos de terceros que no diseñó. La dependencia de esos componentes — proveedores de autenticación en la nube propietarios, controladores de GPU foráneos, APIs de grafos comerciales — crea un riesgo estructural: si un proveedor de terceros cambia sus condiciones de servicio o depreca una API, la plataforma dependiente debe adaptarse bajo presión o detenerse.

## El libro contable de dependencias

La Iniciativa mantiene un libro contable físico de dependencias de terceros pendientes. Cada entrada registra la dependencia, el riesgo estructural que representa, y el estado de la iniciativa moonshot que construye el reemplazo.

El libro contable hace la deuda visible. La visibilidad evita que se acumule silenciosamente — una dependencia no registrada es una dependencia que no recibe priorización de ingeniería.

## Criterios de finalización

Una dependencia se retira del libro contable cuando la implementación nativa que la reemplaza alcanza **paridad estructural** — la misma funcionalidad, sin diferencias de comportamiento observables para los servicios descendentes. En ese punto, el directorio en cuarentena se elimina físicamente y la dependencia de terceros deja de estar presente en el despliegue.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licenciado bajo [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
