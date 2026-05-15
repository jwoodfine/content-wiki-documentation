---
schema: foundry-doc-v1
title: "El Sustrato de Aprendizaje"
slug: apprenticeship-substrate.es
lang: es
paired_with: apprenticeship-substrate.md
category: substrate
type: topic
quality: complete
short_description: "El mecanismo de plataforma que enruta el trabajo de código y editorial primero a través de un modelo de lenguaje pequeño local, captura veredictos de revisión firmados para cada intento, y usa los pares de preferencia resultantes como señal de pre-entrenamiento continuo."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites:
 - ni-51-102
---

La plataforma PointSav enruta cada tarea de código y editorial a través de un modelo de lenguaje pequeño local antes de que la vea un revisor sénior. El operador humano pasa de autor principal a verificador — y el desacuerdo firmado entre el intento del aprendiz y el veredicto del sénior produce datos de pares de preferencia que se componen en valor con el tiempo.

Tres etapas de enrutamiento se registran por tipo de tarea: `review` (cada diff del aprendiz revisado antes del commit), `spot-check` (el aprendiz commitea; se muestrea 1-en-N), y `autonomous` (el aprendiz commitea; auditoría mensual por lotes). Los umbrales de promoción son precisos: 50 veredictos aceptados con tasa de aceptación de 0,85 para pasar de `review` a `spot-check`; 100 veredictos con tasa de 0,95 y cero reversiones post-commit para alcanzar `autonomous`.

El enrutamiento se compone. Cada veredicto firmado es una tupla de entrenamiento; los tipos de tarea graduados eliminan permanentemente los tokens de autoría sénior en esa clase de trabajo; el enrutamiento en sombra genera datos de entrenamiento adicionales de cada otro commit de forma de código en toda la flota, sin paso de veredicto ni firma. El primer tipo de tarea registrado es `version-bump-manifest` — determinista, verificable, sin juicio arquitectónico. Se gradúa primero; el siguiente tipo se registra.

Cuatro condiciones hacen funcionar esta arquitectura: una carta de gobernanza por cliente, identidades de firma por cliente, granularidad por tipo-de-tarea por cliente en el libro de promoción, y pre-entrenamiento continuo por cliente. Las plataformas de IA gestionadas en la nube carecen estructuralmente de las cuatro — el entrenamiento sobre datos de interacción del cliente requiere agruparlos, lo que elimina la garantía de aislamiento por cliente. Por `[ni-51-102]`, la trayectoria hacia la eliminación de tokens en tipos de tarea graduados es prospectiva; la estructura de enrutamiento está operativa hoy.

## Descripción general

La observación capturada entrena al modelo sobre lo que escribió el sénior. La **interacción** capturada — intento del aprendiz más veredicto firmado del sénior — entrena con un orden de magnitud más eficiencia por tupla. Este es el hallazgo central de la literatura RLHF / DPO / RLAIF de 2024-2026: los datos de preferencia firmados son la entrada de entrenamiento más valiosa.

Este patrón de enrutamiento produce esas tuplas de interacción sobre trabajo de producción real, no sobre benchmarks sintéticos. Cada sesión ejercita al aprendiz; cada veredicto firmado es una tupla de entrenamiento; cada tipo de tarea graduado elimina tokens externos de forma monótona.

## Las tres etapas

| Etapa | Enrutamiento | Revisión sénior |
|---|---|---|
| `review` | El aprendiz intenta; el sénior revisa cada diff antes del commit | Cada diff |
| `spot-check` | El aprendiz commitea; el sénior revisa 1-en-N + anomalías auto-marcadas | Muestreado + marcado |
| `autonomous` | El aprendiz commitea autónomamente; auditoría mensual por lotes | Auditoría por lotes |

La promoción es automática al cruzar el umbral; la degradación es automática ante cualquier reversión post-commit rastreada a un diff del aprendiz.

## Brief, intento, veredicto

El sénior emite un **brief** en lugar de escribir el diff directamente. El brief declara qué se está haciendo, los invariantes que el diff debe preservar, las restricciones citadas, y la prueba de aceptación que el aprendiz debe hacer pasar.

El aprendiz responde con un **intento**: razonamiento citando los invariantes del brief, una confianza propia calibrada contra su registro previo del libro, y un diff unificado. Si la confianza cae por debajo de 0,5, el aprendiz escala sin diff.

El sénior lee el intento y firma un **veredicto**: `accept`, `refine`, `reject`, o `defer-tier-c`. Los veredictos `refine` y `reject` llevan notas de una oración — son los datos de entrenamiento de mayor señal que produce el corpus. La firma usa `ssh-keygen -Y sign` con una etiqueta de espacio de nombres que vincula la firma a este protocolo.

## Enrutamiento de producción vs. enrutamiento en sombra

**Enrutamiento de producción** opera sobre tipos de tarea graduados. El sénior emite un brief antes de escribir el diff; el intento del aprendiz es el diff candidato; en `accept`, el diff del aprendiz se incluye en el commit. Esto elimina los tokens de autoría sénior en tipos graduados.

**Enrutamiento en sombra** opera sobre cada otro commit de forma de código en cada cluster activo. Después de que el diff se escribe de la forma habitual, la sesión envía un brief al aprendiz; el aprendiz produce lo que habría hecho; la triple (brief, intento, diff-real) se captura al corpus como tupla de entrenamiento. Sin veredicto; sin firma. El aprendiz se ejercita continuamente; el corpus crece en cada trabajo del cluster.

Producción elimina tokens en tipos graduados. Sombra genera los datos que gradúan el siguiente tipo. Las dos rutas se componen.

## Véase también

- [[compounding-substrate]]
- [[contributor-model]]
- [[language-protocol-substrate]]
- [[trajectory-substrate]]
- [[customer-hostability]]
