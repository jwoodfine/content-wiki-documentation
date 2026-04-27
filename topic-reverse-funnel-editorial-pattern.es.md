---
title: "El patrón editorial de embudo invertido (resumen)"
slug: topic-reverse-funnel-editorial-pattern
category: architecture
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
cites:
  - ni-51-102
  - olmo3-allenai
---

El sustrato invierte el ciclo editorial convencional. La mayoría
de las canalizaciones de publicación colocan al Contribuyente
Creativo humano al INICIO del bucle — borradores, edición, envío
a lectores. El sustrato de Foundry coloca al Creativo al FINAL.
Las Tareas del clúster envían borradores en bruto hacia adelante
a una única puerta editorial; la puerta refina al registro; la
versión refinada sale en vivo; los Contribuyentes Creativos editan
el archivo publicado; sus ediciones alimentan el siguiente ciclo
de entrenamiento como datos de preferencia.

## Cómo funciona

Tres puertos de entrada — borradores de Tarea en
`~/Foundry/clones/<clúster>/.claude/drafts-outbound/`, borradores
de Root en `<repo>/.claude/drafts-outbound/`, borradores de Master
en `~/Foundry/.claude/drafts-outbound/` — alimentan una única
puerta editorial (`service-language`, el clúster project-language).
La puerta aplica cuatro disciplinas: gramática de vocabulario
prohibido, postura de divulgación continua de la BCSC `[ni-51-102]`,
resolución del registro de citas, generación del par bilingüe. La
salida refinada se entrega al repositorio de destino vía el
mecanismo estándar de `handoffs-outbound.md`.

## Por qué los hiperescaladores no pueden replicarlo

Tres razones estructurales:

- Los SLMs multi-inquilino no tienen un sustrato de pretraining
  continuado por inquilino — las ediciones del Creativo no pueden
  alimentar un modelo específico del inquilino.
- Los adaptadores de gramática editorial por inquilino están
  estructuralmente ausentes en los productos de IA gestionada.
- El bucle cerrado requiere datos de entrenamiento soberanos del
  inquilino — los hiperescaladores no pueden conceder esto sin
  desmantelar su modelo de negocio multi-inquilino.

## El ciclo continuo de entrenamiento

Cada edición Creativa se convierte en un par de preferencia DPO
`(refinado, editado-por-Creativo)`. El pretraining continuado
trimestral de OLMo `[olmo3-allenai]` absorbe el par. La línea de
base generada por el sustrato se acerca al 80% → 90% → 95% del
nivel del Creativo a lo largo del tiempo. La carga incremental
del Creativo cae monotónicamente; su apalancamiento crece. Se
mueven hacia arriba a la estrategia de marca, autoría de formas
novelísticas, arco narrativo — trabajo que el sustrato aún no
puede alcanzar.

## Modelo de Contribuyente de Tres Niveles

El Modelo de Contribuyente de Tres Niveles (Núcleo / Pagado /
Abierto) se asigna a la posición del ciclo:

- **Núcleo** (4-7 operadores): operan el sustrato; Tareas de
  clúster; durante todo el ciclo
- **Pagado** (50-100 Contribuyentes Creativos): editan la versión
  refinada publicada al FINAL del ciclo; arte + marca + voz
- **Abierto** (10K+ consumidores de wiki): consumen + citan +
  bifurcan fuera del ciclo

Los contribuyentes Pagados en este patrón no son redactores
técnicos. Son especialistas en oficio — diseñadores, editores
narrativos, contribuyentes de voz de marca.

## Trabajo planificado

Por la postura de divulgación continua de la BCSC (`[ni-51-102]`),
la trayectoria es `planificada` e `intencionada`. AS-2 (clúster
project-slm) integra `llguidance` en el Doorman; los adaptadores
de voz por inquilino destilan en el primer año; el ciclo
trimestral de OLMo opera a partir del primer pretraining
continuado.

## Véase también

- [El Sustrato Compuesto](topic-compounding-substrate.es.md)
- [El sustrato de aprendizaje](topic-apprenticeship-substrate.es.md)
- [Restricciones en tiempo de decodificación](topic-decode-time-constraints.es.md)
