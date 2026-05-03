---
schema: foundry-doc-v1
title: "The Apprenticeship Substrate"
slug: apprenticeship-substrate.es
category: architecture
type: topic
quality: complete
short_description: "The Apprenticeship Substrate is the Foundry mechanism that routes code-shaped and editorial work first through a local Small Language Model, captures signed senior verdicts on every attempt, and uses the resulting preference pairs as continued-pretraining signal."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: apprenticeship-substrate.md
---
# El sustrato de aprendizaje (resumen)

La mayoría de los asistentes de escritura con IA empujan
silenciosamente a sus usuarios hacia una voz única. Investigación
de Cornell (arXiv 2409.11360, 2024) encontró que las sugerencias
de IA empujan a escritores no occidentales hacia el registro
occidental con tasas más altas y con ganancias de productividad
más pequeñas, porque los escritores gastan tiempo adicional
corrigiendo la deriva de la IA hacia su voz auténtica. La
disciplina anti-homogenización de Foundry es la postura
arquitectónica que resiste esa deriva explícitamente.

## Por qué existe

La observación capturada entrena al modelo sobre lo que escribió
el sénior. La **interacción** capturada — intento del aprendiz
más veredicto firmado del sénior — entrena con un orden de
magnitud más eficiencia por tupla. Es el hallazgo central de la
literatura RLHF / DPO / RLAIF de 2024-2026.

Cuatro precondiciones hacen funcionar esto, y las cuatro solo
se sostienen dentro de sustratos con forma Foundry: carta
constitucional por cliente (la Doctrina), identidades de firma
por cliente (`allowed_signers`), granularidad por tipo-de-tarea
por cliente (el libro de promoción), y pre-formación continuada
por cliente. Los hiperescaladores carecen estructuralmente de
las cuatro.

## Las tres etapas

| Etapa | Ruteo | Revisión sénior |
|---|---|---|
| `review` | El aprendiz intenta; el sénior revisa cada diff antes del commit | Cada diff |
| `spot-check` | El aprendiz commitea; el sénior revisa 1-en-N + anomalías auto-marcadas | Muestreado + marcado |
| `autonomous` | El aprendiz commitea autónomamente; auditoría mensual por lotes | Auditoría por lotes |

La promoción es automática al cruzar el umbral; la degradación
es automática ante cualquier reversión post-commit rastreada a
un diff del aprendiz.

## Brief, intento, veredicto

El sénior emite un **brief** en lugar de escribir el diff
directamente. El aprendiz responde con un **intento**:
razonamiento citando los invariantes del brief, una confianza
propia calibrada contra su registro previo del libro, y un diff
unificado. Si la confianza cae por debajo de 0.5, el aprendiz
escala sin diff.

El sénior lee el intento y firma un **veredicto**: `accept`,
`refine`, `reject`, o `defer-tier-c`. Los veredictos `refine`
y `reject` llevan notas de una oración — son los datos de
entrenamiento de mayor señal que produce el corpus. La firma
usa `ssh-keygen -Y sign` con etiqueta de espacio de nombres
que vincula la firma a este protocolo.

## Ruteo de producción vs. ruteo en sombra

Dos rutas corren en paralelo. **Producción** opera sobre tipos
de tarea graduados — elimina tokens del sénior en esa clase de
trabajo. **Sombra** opera sobre cada commit de forma de código
en cada cluster activo — el aprendiz produce lo que habría
hecho, la tupla (brief, intento, diff-real) entra al corpus
como tupla de entrenamiento, sin veredicto y sin firma. El
aprendiz se ejercita continuamente; el corpus crece en cada
trabajo.

Producción elimina tokens. Sombra genera los datos que gradúan
el próximo tipo. Las dos rutas se componen.

## Véase también

- [Documento canónico en inglés](topic-apprenticeship-substrate.md)
- [El sustrato compuesto](topic-compounding-substrate.md)
- [El modelo de contribuyentes en tres niveles](topic-contributor-model.md)
- [El sustrato de protocolo de lenguaje](topic-language-protocol-substrate.md)
