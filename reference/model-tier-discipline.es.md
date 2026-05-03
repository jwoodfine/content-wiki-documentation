---
schema: foundry-doc-v1
title: "Disciplina de niveles de modelo"
slug: model-tier-discipline.es
category: reference
type: topic
quality: published
short_description: La disciplina para enrutar el trabajo al nivel de modelo de IA apropiado — pensamiento profundo, implementación o mecánico — para adaptar la capacidad del modelo a la forma del trabajo y controlar el costo de inferencia.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: model-tier-discipline.md
---

## Resumen estratégico

La disciplina de niveles de modelo es el enfoque estructurado que adapta la forma del trabajo a la capacidad del modelo, enruta el trabajo apropiado a niveles de menor costo y hace que la decisión de enrutamiento sea explícita y revisable.

## Tres niveles abstractos

**Pensamiento profundo.** Decisiones arquitectónicas, autoría doctrinal, análisis transversales, formulación de problemas novedosos, síntesis de múltiples fuentes. Ejemplos: elaborar una nueva convención, depurar un problema cuya causa raíz aún no está identificada.

**Implementación.** Seguir un plan establecido, trabajo delimitado a un componente, implementación de características bien especificadas, revisión de código contra convenciones ratificadas. Ejemplos: andamiar un nuevo módulo desde una especificación documentada, redactar un runbook desde una plantilla conocida.

**Mecánico.** Trabajo de coincidencia de patrones con entradas y salidas claras, sin juicio arquitectónico, estructura repetible. Ejemplos: movimientos de archivos, actualizaciones de números de versión, actualizaciones de filas de registro.

## El mecanismo preferido en sesión

Cuando una sesión de trabajo llega a una pausa natural y el siguiente bloque delimitado de trabajo encaja en un nivel inferior, la sesión despacha un subagente de primer plano en el nivel apropiado. El padre retiene su contexto y espera a que el subagente complete, luego revisa el resultado y lo confirma o pone en cola el siguiente bloque.

Cuatro propiedades gobiernan esto en la práctica: brief delimitado (una tarea, un resultado), serial en primer plano al escribir, umbral de confianza (despachar solo cuando hay alta confianza), y alcance de capa preservado.

## El encuadre de costo

La estructura de tres niveles produce un multiplicador efectivo significativo con presupuestos diarios de tokens fijos. Ejecutar trabajo mecánico en el nivel mecánico en lugar del nivel de pensamiento profundo extiende el presupuesto en aproximadamente un factor de quince. Un grupo de contribuidores que opera con disciplina de niveles puede mantener un volumen sustancialmente mayor de trabajo dentro del mismo costo de infraestructura.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ y Foundry™ son marcas comerciales no registradas de Woodfine Capital Projects Inc.*
